# DemoVideo - CLAUDE.md

## Purpose

Python pipeline to produce a ~2 minute demo video for the CSI PO Asset Creation Tool. Generates slides (Pillow), voiceover (ElevenLabs TTS), and assembles them into MP4 (ffmpeg-native, NVENC GPU).

**Pipeline**: Generated slides + user-provided screenshots + ElevenLabs narration -> MP4 video

## Folder Structure

```
DemoVideo/
├── config/
│   ├── video_script.json    # Master config: slides, narration text, timing, voice
│   ├── colors.json          # Brand color palette
│   └── fonts.json           # System font paths (Calibri, Segoe UI)
├── scripts/
│   ├── 01_generate_slides.py       # Pillow slide renderer (4 templates)
│   ├── 02_generate_voice_samples.py # ElevenLabs voice comparison
│   ├── 03_generate_audio.py        # Full narration TTS
│   ├── 04_assemble_video.py        # MoviePy v2 video assembly
│   └── 05_build_all.py             # Orchestrator (01 -> 03 -> 04)
├── assets/
│   ├── screenshots/          # User-provided PNGs (placeholders initially)
│   ├── slides/               # Generated slide PNGs
│   └── audio/                 # Per-section narration MP3s
│       └── samples/          # Voice comparison samples
└── output/
    └── CSI_Invoice_Automation_Demo.mp4
```

## Running the Pipeline

```bash
cd CSIPOAssetCreationTool/DemoVideo

# Generate slides only
python scripts/01_generate_slides.py

# Generate voice samples (requires ELEVENLABS_API_KEY in .env)
python scripts/02_generate_voice_samples.py

# Generate full narration audio
python scripts/03_generate_audio.py

# Assemble video (requires ffmpeg)
python scripts/04_assemble_video.py

# Full pipeline (01 -> 03 -> 04)
python scripts/05_build_all.py
```

## Configuration

All content is driven by `config/video_script.json`. To change narration, timing, or slide content, edit the JSON — no Python changes needed.

### video_script.json Structure
- `video`: resolution (1920x1080), fps (24), crossfade duration, output path
- `tts`: ElevenLabs model, voice name, voice_id
- `sections[]`: 8 sections, each with id, type, duration, narration text, and type-specific fields

### Slide Templates
1. **title_card** — gradient background, centered title + subtitle + footer
2. **architecture_diagram** — 6 colored boxes with arrow connectors; supports progressive highlights
3. **screenshot_frame** — screenshot/placeholder with title bar + caption bar
4. **closing_card** — 2x2 metrics grid, tagline, footer

### Progressive Highlight System (Architecture Section)

The architecture overview section supports a `highlights` array in `video_script.json` that generates spotlight sub-slides:

```json
"highlights": [
  {"boxes": [],     "duration": 3.5},   // Overview (all normal)
  {"boxes": [0],    "duration": 2.5},   // Spotlight Invoice PDF
  {"boxes": [1],    "duration": 2.5},   // Spotlight RPA
  ...
]
```

**Visual treatment**:
- **Active box**: normal color + 3px white border (glow)
- **Dimmed boxes**: color darkened to 35% brightness
- **Arrows**: adjacent to active box stay accent color; others dimmed

**Slide generation**: `01_generate_slides.py` produces `02_architecture_overview.png` (overview) plus `_h1.png` through `_h5.png` (one per non-empty highlight entry). Empty `boxes: []` reuses the overview slide.

**Video assembly**: `04_assemble_video.py` builds a sequence of `ImageClip`s with 0.3s crossfade between steps, then attaches the single audio track. The composite participates in the main section concatenation as usual.

## Dependencies

- **Pillow** 11.3.0 (slide generation) — installed
- **elevenlabs** 2.36.1 (TTS) — installed
- **python-dotenv** (env loading) — installed
- **imageio-ffmpeg** 0.6.0 (bundles ffmpeg binary) — installed
- **moviepy** 2.2.1 (installed but no longer used for assembly; kept as dependency)
- **pydub** (optional, for `--boost` volume adjustment) — NOT YET INSTALLED

**Install all dependencies**: `pip install "pillow<12.0" elevenlabs python-dotenv imageio-ffmpeg`

## Key Decisions

| Decision | Reason |
|---|---|
| Pillow for slides, not MoviePy TextClip | Full layout control, avoids MoviePy v2 font issues |
| One audio file per section | Selective re-generation saves ElevenLabs chars |
| Config-driven (video_script.json) | Iterate by editing JSON, not Python |
| ffmpeg-native assembly (not MoviePy) | ~90x faster: 8s vs 12min. Uses -loop 1, xfade, NVENC |
| Placeholder screenshots | Pipeline runs before real screenshots exist |
| Duration = max(config, audio + 0.5s) | Prevents narration cutoff |
| Branding: "Infor OS and The Velocity Suite" | Used in all narration, footers, tagline, metrics |

## ElevenLabs TTS Details

- **Voice**: Rachel (voice_id: `21m00Tcm4TlvDq8ikWAM`) — clear professional female
- **Model**: `eleven_multilingual_v2`
- **Output format**: `mp3_44100_128`
- **API key**: in `.env` (ELEVENLABS_API_KEY) — has TTS permission, lacks voices_read (not needed)
- **SDK pattern**: `client.text_to_speech.convert()` returns `Iterator[bytes]`, join with `b"".join()`
- **Characters used so far**: ~4,300 of 30,000/month (~2,800 initial + ~1,500 pronunciation fix)
- **Pronunciation tricks**:
  - "In-fohr" produces correct "IN-FOR" sound in most contexts (tested: "In-for" still said "IN-FER")
  - "Inn-for" works better before "Robotic Process Automation" (avoids R-blending from "In-fohr")
  - Add comma after "In-fohr" before vowel-starting words like "O S" to prevent linking-R artifacts ("IN-FOR-HAR")
  - "Ion" (single word) instead of "I O N" so TTS doesn't spell it out
  - Expanded acronyms sound more natural than spaced letters: "Robotic Process Automation" not "R P A", "Document Processor" not "I D P", "Generative AI" not "Gen A I", "PDF" not "P D F", "purchase order number" not "P O number"
  - Keep "O S" spaced (sounds correct), "AI" unspaced for short references
- **Regenerate single section**: `python scripts/03_generate_audio.py --section opening_hook --force`
- **Volume boost**: `python scripts/03_generate_audio.py --force --boost 6` (needs `pip install pydub`)
- User noted Rachel may need to be louder — test with `--boost 3` or `--boost 6` during Phase 4

## Screenshots (Phase 5 — Complete)

| File | Source |
|---|---|
| `rpa_watch.png` | RPA Studio with DemoInvoiceLoader |
| `idp_extract.png` | IDP extraction results |
| `genai_agent.png` | GenAI Prompt Playground tool calls |
| `syteline_po.png` | SyteLine PO form |
| `pulse_alert.png` | Infor OS Pulse inbox |

## Video Assembly Details (04_assemble_video.py)

- **Engine**: ffmpeg-native (bypass MoviePy for ~90x faster rendering)
- **Input**: 13 slide PNGs (8 base + 5 highlight variants) + 8 narration MP3s
- **Output**: `output/CSI_Invoice_Automation_Demo.mp4` (H.264 + AAC)
- **Duration calc**: `max(config_duration, audio_duration + 0.5s)` per section
- **Transitions**: ffmpeg `xfade=transition=fade` filter (0.5s between sections, 0.3s between highlight steps)
- **Encoding**: NVENC GPU (h264_nvenc) by default, CPU fallback (libx264)
- **Render time**: ~8 seconds with GPU (RTX 4090), ~10s CPU — down from ~12 min with MoviePy
- **Audio mixing**: `adelay` + `amix` positions each section's audio at correct timeline offset

**CLI flags**:
- `--no-audio` — assemble without audio (faster testing)
- `--section <id>` — render a single section as standalone clip (preview to `output/preview_<id>.mp4`)
- `--cpu` — force CPU encoding (libx264) instead of GPU

**Key technical details**:
- Static slides use ffmpeg's `-loop 1` (no per-frame Python processing)
- `fps=24,format=yuv420p` filter required for xfade compatibility
- Do NOT use `setpts=PTS-STARTPTS` — it destroys frame rate metadata and breaks xfade
- ffmpeg bundled via imageio-ffmpeg (`get_ffmpeg_exe()`)
- `-pix_fmt yuv420p -profile:v high` required for Windows Media Player compatibility (NVENC defaults to yuv444p High 4:4:4)
- `-ar 44100 -ac 2` forces standard audio sample rate (loudnorm can resample to 96kHz)
- `loudnorm=I=-16:TP=-1.5:LRA=11` (EBU R128) applied per audio track for consistent volume across sections

## Pipeline Orchestrator (05_build_all.py)

Runs the full pipeline: slides -> audio -> video via subprocess.

**CLI flags**:
- `--skip-slides` — skip slide generation
- `--skip-audio` — skip audio generation
- `--force` — force regeneration of all assets (passed to audio script)

## Phases

- **Phase 1**: Scaffolding + slide generation — COMPLETE
- **Phase 2**: Voice selection — COMPLETE (Rachel selected)
- **Phase 3**: Full audio generation — COMPLETE (8 MP3s generated, ~6,500 chars total)
- **Phase 4**: Video assembly — COMPLETE (ffmpeg-native, NVENC GPU, ~8s render)
- **Phase 4b**: Pronunciation V2 + architecture highlights — COMPLETE
- **Phase 4c**: Pronunciation V3 + highlight sync + loudness normalization — COMPLETE
- **Phase 5**: Real screenshots + final polish — COMPLETE

