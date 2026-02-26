"""
02_generate_voice_samples.py — Generate short ElevenLabs voice comparison samples.

Produces 3 MP3 files (one per voice) using the same sample text so you can
compare and pick the best narrator voice for the demo video.

Voices:
  - Adam:   deep professional male
  - Rachel: clear professional female
  - Antoni: warm conversational male

Usage:
    python scripts/02_generate_voice_samples.py

Requires ELEVENLABS_API_KEY in .env
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import ElevenLabs

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
SAMPLES_DIR = PROJECT_DIR / "assets" / "audio" / "samples"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SAMPLE_TEXT = (
    "This tool uses Infor OS and The Velocity Suite's advanced technologies "
    "to read an invoice and automatically create vendors, items, and purchase "
    "orders in SyteLine."
)

VOICES = [
    {"name": "Adam", "voice_id": "pNInz6obpgDQGcFmaJgB", "desc": "deep professional male"},
    {"name": "Rachel", "voice_id": "21m00Tcm4TlvDq8ikWAM", "desc": "clear professional female"},
    {"name": "Antoni", "voice_id": "ErXwobaYiN019PkySvjV", "desc": "warm conversational male"},
]

MODEL_ID = "eleven_multilingual_v2"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: Set ELEVENLABS_API_KEY in .env")
        sys.exit(1)

    client = ElevenLabs(api_key=api_key)
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Sample text ({len(SAMPLE_TEXT)} chars):")
    print(f"  \"{SAMPLE_TEXT}\"\n")

    total_chars = 0
    for voice in VOICES:
        print(f"Generating: {voice['name']} ({voice['desc']})...", end=" ", flush=True)
        audio_iter = client.text_to_speech.convert(
            voice_id=voice["voice_id"],
            text=SAMPLE_TEXT,
            model_id=MODEL_ID,
        )
        data = b"".join(audio_iter)
        out_path = SAMPLES_DIR / f"sample_{voice['name'].lower()}.mp3"
        with open(out_path, "wb") as f:
            f.write(data)
        total_chars += len(SAMPLE_TEXT)
        print(f"{len(data):,} bytes -> {out_path.name}")

    print(f"\nDone. {len(VOICES)} samples generated in {SAMPLES_DIR}")
    print(f"Characters used: {total_chars} (sample text x {len(VOICES)})")
    print("\nListen to each sample and pick your preferred voice.")
    print("Then update config/video_script.json -> tts.voice and tts.voice_id")


if __name__ == "__main__":
    main()
