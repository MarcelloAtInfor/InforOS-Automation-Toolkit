"""
03_generate_audio.py — Generate full narration audio from video_script.json.

Produces one MP3 per section using ElevenLabs TTS. Reads voice config from
video_script.json (tts.voice_id, tts.model).

Usage:
    python scripts/03_generate_audio.py              # Generate all sections
    python scripts/03_generate_audio.py --section opening_hook   # Single section
    python scripts/03_generate_audio.py --boost 6    # Boost volume by 6 dB

Requires ELEVENLABS_API_KEY in .env
"""

import argparse
import json
import os
import struct
import sys
import wave
import io
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "config"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"

# ---------------------------------------------------------------------------
# Load configuration
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Volume boost (pure Python, no ffmpeg needed)
# ---------------------------------------------------------------------------

def boost_mp3_volume(mp3_bytes: bytes, db: float) -> bytes:
    """Boost MP3 volume using pydub if available, otherwise return unchanged."""
    if db == 0:
        return mp3_bytes
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(io.BytesIO(mp3_bytes))
        audio = audio + db  # pydub uses dB directly
        buf = io.BytesIO()
        audio.export(buf, format="mp3")
        return buf.getvalue()
    except ImportError:
        print("  WARNING: pydub not installed, skipping volume boost. Install with: pip install pydub")
        return mp3_bytes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate narration audio")
    parser.add_argument("--section", type=str, default=None,
                        help="Generate only this section ID (e.g., opening_hook)")
    parser.add_argument("--boost", type=float, default=0,
                        help="Volume boost in dB (e.g., 3, 6). Requires pydub.")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate all sections even if audio already exists")
    args = parser.parse_args()

    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: Set ELEVENLABS_API_KEY in .env")
        sys.exit(1)

    config = load_json(CONFIG_DIR / "video_script.json")
    tts_cfg = config["tts"]
    voice_id = tts_cfg["voice_id"]
    model_id = tts_cfg["model"]

    if not voice_id:
        print("ERROR: Set tts.voice_id in video_script.json (run 02_generate_voice_samples.py first)")
        sys.exit(1)

    import httpx
    client = ElevenLabs(
        api_key=api_key,
        timeout=120,  # 2 min timeout (default 240 but streaming can stall)
    )
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    sections = config["sections"]
    if args.section:
        sections = [s for s in sections if s["id"] == args.section]
        if not sections:
            print(f"ERROR: Section '{args.section}' not found")
            sys.exit(1)

    # Skip sections that already have audio (unless --force)
    if not args.section:
        to_generate = []
        for s in sections:
            out = AUDIO_DIR / f"{s['id']}.mp3"
            if out.exists() and not args.force:
                print(f"  [{s['id']}] Already exists, skipping (use --force to regenerate)")
            else:
                to_generate.append(s)
        sections = to_generate

    total_chars = 0
    print(f"Voice: {tts_cfg['voice']} ({voice_id})")
    print(f"Model: {model_id}")
    if args.boost:
        print(f"Volume boost: +{args.boost} dB")
    print()

    max_retries = 2
    for i, section in enumerate(sections):
        section_id = section["id"]
        narration = section.get("narration", "")
        if not narration:
            print(f"  [{section_id}] No narration, skipping")
            continue

        print(f"  [{section_id}] {len(narration)} chars...", end=" ", flush=True)

        data = None
        for attempt in range(max_retries + 1):
            try:
                audio_iter = client.text_to_speech.convert(
                    voice_id=voice_id,
                    text=narration,
                    model_id=model_id,
                    output_format="mp3_44100_128",
                    voice_settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.75,
                        style=0.0,
                        use_speaker_boost=True,
                    ),
                )
                data = b"".join(audio_iter)
                break
            except Exception as e:
                if attempt < max_retries:
                    import time
                    print(f"\n    Retry {attempt + 1}/{max_retries} ({e.__class__.__name__})...", end=" ", flush=True)
                    time.sleep(2)
                else:
                    print(f"\n    FAILED after {max_retries + 1} attempts: {e}")
                    continue

        if data is None:
            continue

        if args.boost:
            data = boost_mp3_volume(data, args.boost)

        out_path = AUDIO_DIR / f"{section_id}.mp3"
        with open(out_path, "wb") as f:
            f.write(data)

        total_chars += len(narration)
        print(f"{len(data):,} bytes -> {out_path.name}")

    print(f"\nDone. Characters used this run: {total_chars}")
    print(f"Audio files in: {AUDIO_DIR}")


if __name__ == "__main__":
    main()
