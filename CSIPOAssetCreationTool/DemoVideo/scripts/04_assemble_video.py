"""
04_assemble_video.py — ffmpeg-native video assembler for Demo Video pipeline.

Uses ffmpeg directly for dramatically faster rendering (~10-30x vs MoviePy):
- Static slides use ffmpeg's -loop 1 (no per-frame Python processing)
- Crossfades use ffmpeg's xfade video filter
- NVENC GPU encoding (h264_nvenc) on NVIDIA GPUs with CPU fallback

Usage:
    python scripts/04_assemble_video.py              # Full assembly
    python scripts/04_assemble_video.py --no-audio   # Slides only (faster testing)
    python scripts/04_assemble_video.py --section architecture_overview
    python scripts/04_assemble_video.py --cpu        # Force CPU encoding (libx264)
"""

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "config"
SLIDES_DIR = PROJECT_DIR / "assets" / "slides"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
OUTPUT_DIR = PROJECT_DIR / "output"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_ffmpeg() -> str:
    """Get path to ffmpeg bundled with imageio-ffmpeg."""
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe_audio_duration(ffmpeg: str, path: Path) -> float:
    """Get audio file duration using ffmpeg -i (no ffprobe needed)."""
    result = subprocess.run(
        [ffmpeg, "-i", str(path)],
        capture_output=True, text=True
    )
    for line in result.stderr.split("\n"):
        line = line.strip()
        if line.startswith("Duration:"):
            ts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = ts.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Segment:
    """A visual segment: one static slide shown for a duration."""
    image: Path
    duration: float


@dataclass
class AudioEntry:
    """An audio track positioned at an offset in the final timeline."""
    path: Path
    offset: float  # seconds from video start


# ---------------------------------------------------------------------------
# Build segment + audio lists from config
# ---------------------------------------------------------------------------

def resolve_slide(section_idx: int, section_id: str,
                  section_filter: str | None) -> Path | None:
    """Find the base slide PNG for a section."""
    if section_filter:
        for c in sorted(SLIDES_DIR.glob("*.png")):
            parts = c.stem.split("_", 1)
            if len(parts) > 1 and parts[1] == section_id:
                return c
        return None
    return SLIDES_DIR / f"{section_idx + 1:02d}_{section_id}.png"


def build_plan(sections: list[dict], main_cf: float, no_audio: bool,
               section_filter: str | None, ffmpeg: str
               ) -> tuple[list[Segment], list[float], list[AudioEntry]]:
    """Build flat segment list, crossfade list, and audio entries.

    Returns:
        segments: list of (image, duration) for each visual segment
        crossfades: crossfade duration between segments[i] and segments[i+1]
                    (length = len(segments) - 1)
        audio_entries: audio tracks positioned at correct timeline offsets
    """
    segments: list[Segment] = []
    crossfades: list[float] = []
    audio_entries: list[AudioEntry] = []

    # Running timeline position: where the next segment starts in the video
    timeline = 0.0

    for si, section in enumerate(sections):
        sid = section["id"]
        cfg_dur = section["duration"]
        highlights = section.get("highlights")

        slide = resolve_slide(si, sid, section_filter)
        if slide is None or not slide.exists():
            print(f"  WARNING: Slide not found for '{sid}', skipping")
            continue

        # Audio
        audio_path = AUDIO_DIR / f"{sid}.mp3"
        audio_dur = 0.0
        if not no_audio and audio_path.exists():
            audio_dur = probe_audio_duration(ffmpeg, audio_path)

        section_dur = max(cfg_dur, audio_dur + 0.5)
        section_start = timeline

        is_last_section = (si == len(sections) - 1)

        if highlights and len(highlights) > 0:
            sub_cf = 0.3
            prefix = f"{si + 1:02d}_{sid}" if not section_filter else None
            n_h = len(highlights)

            # Compute highlight durations; extend last to fill section duration
            raw_durs = [h["duration"] for h in highlights]
            if n_h > 1:
                net_first = sum(raw_durs[:-1]) - (n_h - 2) * sub_cf
                last_dur = section_dur - net_first + sub_cf
            else:
                last_dur = section_dur
            raw_durs[-1] = max(raw_durs[-1], last_dur)

            for h_idx, highlight in enumerate(highlights):
                h_boxes = highlight["boxes"]
                h_dur = raw_durs[h_idx]

                # Resolve highlight slide PNG
                if not h_boxes:
                    h_path = slide  # overview (empty boxes = base slide)
                else:
                    if prefix:
                        h_path = SLIDES_DIR / f"{prefix}_h{h_idx}.png"
                    else:
                        h_path = slide
                        for c in sorted(SLIDES_DIR.glob("*.png")):
                            if c.stem.endswith(f"_{sid}_h{h_idx}"):
                                h_path = c
                                break
                    if not h_path.exists():
                        h_path = slide

                segments.append(Segment(h_path, h_dur))
                timeline += h_dur

                # Crossfade to next segment
                is_last_h = (h_idx == n_h - 1)
                if is_last_h and is_last_section:
                    pass  # no crossfade after final segment
                elif is_last_h:
                    crossfades.append(main_cf)
                    timeline -= main_cf
                else:
                    crossfades.append(sub_cf)
                    timeline -= sub_cf

            print(f"  [{si+1}/{len(sections)}] {sid}: {section_dur:.1f}s "
                  f"(audio={audio_dur:.1f}s, {n_h} highlight steps)")
        else:
            segments.append(Segment(slide, section_dur))
            timeline += section_dur

            if not is_last_section:
                crossfades.append(main_cf)
                timeline -= main_cf

            print(f"  [{si+1}/{len(sections)}] {sid}: {section_dur:.1f}s "
                  f"(audio={audio_dur:.1f}s)")

        # Audio entry for this section
        if not no_audio and audio_path.exists():
            audio_entries.append(AudioEntry(audio_path, section_start))

    return segments, crossfades, audio_entries


# ---------------------------------------------------------------------------
# FFmpeg command builder
# ---------------------------------------------------------------------------

def build_ffmpeg_cmd(ffmpeg: str, segments: list[Segment],
                     crossfades: list[float], audio_entries: list[AudioEntry],
                     output: Path, fps: int, use_gpu: bool) -> list[str]:
    """Build the complete ffmpeg command with filter_complex."""
    cmd = [ffmpeg, "-y"]

    # --- Inputs ---
    # Video: one -loop 1 input per segment
    for seg in segments:
        cmd += ["-loop", "1", "-framerate", str(fps),
                "-t", f"{seg.duration:.3f}", "-i", str(seg.image)]
    n_vid = len(segments)

    # Audio: one input per section audio
    for ae in audio_entries:
        cmd += ["-i", str(ae.path)]
    n_aud = len(audio_entries)

    # --- Filter complex ---
    filters = []

    # Prepare each video input (constant fps + pixel format for xfade + H.264)
    for i in range(n_vid):
        filters.append(
            f"[{i}:v]fps={fps},format=yuv420p[v{i}]"
        )

    # Chain xfade filters between consecutive segments
    if n_vid == 1:
        video_label = "v0"
    else:
        # offset tracks the time in the output at which each xfade starts
        offset = segments[0].duration - crossfades[0]
        prev_label = "v0"

        for j in range(len(crossfades)):
            cf = crossfades[j]
            out_label = f"vx{j}"
            filters.append(
                f"[{prev_label}][v{j+1}]xfade=transition=fade"
                f":duration={cf:.3f}:offset={offset:.3f}[{out_label}]"
            )
            prev_label = out_label
            # Advance offset for next xfade
            if j < len(crossfades) - 1:
                offset += segments[j + 1].duration - crossfades[j + 1]

        video_label = prev_label

    # Audio: normalize loudness per track, then adelay to timeline position, then amix
    # loudnorm (EBU R128) ensures consistent volume across all sections
    if n_aud > 0:
        for i, ae in enumerate(audio_entries):
            inp_idx = n_vid + i
            delay_ms = int(ae.offset * 1000)
            norm = "loudnorm=I=-16:TP=-1.5:LRA=11"
            if delay_ms > 0:
                filters.append(
                    f"[{inp_idx}:a]{norm},adelay={delay_ms}|{delay_ms}[a{i}]"
                )
            else:
                filters.append(f"[{inp_idx}:a]{norm}[a{i}]")

        a_labels = "".join(f"[a{i}]" for i in range(n_aud))
        filters.append(
            f"{a_labels}amix=inputs={n_aud}:duration=longest:normalize=0[aout]"
        )
        audio_label = "aout"
    else:
        audio_label = None

    # Assemble filter_complex string
    cmd += ["-filter_complex", ";\n".join(filters)]

    # Map outputs
    cmd += ["-map", f"[{video_label}]"]
    if audio_label:
        cmd += ["-map", f"[{audio_label}]"]

    # Encoding settings
    # -pix_fmt yuv420p + -profile high: forces WMP-compatible H.264
    # (NVENC defaults to yuv444p High 4:4:4 which WMP can't play)
    if use_gpu:
        cmd += ["-c:v", "h264_nvenc", "-preset", "p4",
                "-rc", "vbr", "-cq", "23",
                "-pix_fmt", "yuv420p", "-profile:v", "high"]
    else:
        cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-pix_fmt", "yuv420p", "-profile:v", "high"]

    if audio_label:
        # -ar 44100 -ac 2: force standard sample rate + stereo
        # (loudnorm can resample to 96kHz mono which WMP can't handle)
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]

    cmd += ["-shortest", str(output)]

    return cmd


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Assemble demo video from slides + audio (ffmpeg-native)")
    parser.add_argument("--no-audio", action="store_true",
                        help="Assemble without audio (faster testing)")
    parser.add_argument("--section", type=str, default=None,
                        help="Render a single section (e.g., opening_hook)")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU encoding (libx264) instead of GPU")
    args = parser.parse_args()

    config = load_json(CONFIG_DIR / "video_script.json")
    video_cfg = config["video"]
    fps = video_cfg["fps"]
    main_cf = video_cfg["crossfade_duration"]
    output_file = PROJECT_DIR / video_cfg["output_file"]

    sections = config["sections"]
    if args.section:
        sections = [s for s in sections if s["id"] == args.section]
        if not sections:
            print(f"ERROR: Section '{args.section}' not found")
            sys.exit(1)
        output_file = OUTPUT_DIR / f"preview_{args.section}.mp4"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ffmpeg = get_ffmpeg()
    encoder = "CPU (libx264)" if args.cpu else "GPU (h264_nvenc)"

    print(f"Assembling {len(sections)} section(s)...")
    print(f"  Resolution: {video_cfg['resolution'][0]}x{video_cfg['resolution'][1]}")
    print(f"  FPS: {fps}")
    print(f"  Crossfade: {main_cf}s")
    print(f"  Encoder: {encoder}")
    print()

    segments, crossfades, audio_entries = build_plan(
        sections, main_cf, args.no_audio, args.section, ffmpeg
    )

    if not segments:
        print("ERROR: No segments to assemble")
        sys.exit(1)

    print(f"\n  Total segments: {len(segments)}")
    print(f"  Crossfades: {len(crossfades)}")
    if audio_entries:
        print(f"  Audio tracks: {len(audio_entries)}")

    # Build ffmpeg command
    use_gpu = not args.cpu
    cmd = build_ffmpeg_cmd(
        ffmpeg, segments, crossfades, audio_entries,
        output_file, fps, use_gpu
    )

    print(f"\nEncoding to {output_file}...")
    t0 = time.time()

    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0

    # If GPU encoding failed, retry with CPU
    if result.returncode != 0 and use_gpu:
        print(f"  GPU encoding failed, retrying with CPU (libx264)...")
        cmd = build_ffmpeg_cmd(
            ffmpeg, segments, crossfades, audio_entries,
            output_file, fps, use_gpu=False
        )
        t0 = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - t0
        encoder = "CPU (libx264) [fallback]"

    if result.returncode != 0:
        print(f"\nERROR: ffmpeg failed (exit code {result.returncode})")
        # Show last 2000 chars of stderr for debugging
        print(result.stderr[-2000:])
        sys.exit(1)

    # Summary
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"\nDone in {elapsed:.1f}s!")
    print(f"  Output: {output_file}")
    print(f"  File size: {file_size_mb:.1f} MB")
    print(f"  Encoder: {encoder}")


if __name__ == "__main__":
    main()
