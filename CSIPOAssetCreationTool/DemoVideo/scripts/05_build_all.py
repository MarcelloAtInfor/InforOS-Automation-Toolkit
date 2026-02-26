"""
05_build_all.py — Full pipeline orchestrator for Demo Video.

Runs the pipeline steps in order:
  1. Generate slides (01_generate_slides.py)
  2. Generate audio (03_generate_audio.py) — skipped if all audio exists
  3. Assemble video (04_assemble_video.py)

Usage:
    python scripts/05_build_all.py                # Full pipeline
    python scripts/05_build_all.py --skip-slides  # Skip slide generation
    python scripts/05_build_all.py --skip-audio   # Skip audio generation
    python scripts/05_build_all.py --force         # Force regeneration of all assets
"""

import argparse
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = {
    "slides": SCRIPT_DIR / "01_generate_slides.py",
    "audio": SCRIPT_DIR / "03_generate_audio.py",
    "video": SCRIPT_DIR / "04_assemble_video.py",
}


def run_step(name: str, script: Path, extra_args: list[str] | None = None):
    """Run a pipeline step via subprocess, streaming output."""
    print(f"{'=' * 60}")
    print(f"  STEP: {name}")
    print(f"  Script: {script.name}")
    print(f"{'=' * 60}")
    print()

    cmd = [sys.executable, str(script)]
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, cwd=str(SCRIPT_DIR.parent))

    if result.returncode != 0:
        print(f"\nERROR: {name} failed (exit code {result.returncode})")
        sys.exit(result.returncode)

    print()


def main():
    parser = argparse.ArgumentParser(description="Run full DemoVideo pipeline")
    parser.add_argument("--skip-slides", action="store_true",
                        help="Skip slide generation step")
    parser.add_argument("--skip-audio", action="store_true",
                        help="Skip audio generation step")
    parser.add_argument("--force", action="store_true",
                        help="Force regeneration of all assets")
    args = parser.parse_args()

    print()
    print("DemoVideo Full Pipeline")
    print("=" * 60)
    print()

    # Step 1: Slides
    if args.skip_slides:
        print("Skipping slide generation (--skip-slides)\n")
    else:
        run_step("Generate Slides", SCRIPTS["slides"])

    # Step 2: Audio
    if args.skip_audio:
        print("Skipping audio generation (--skip-audio)\n")
    else:
        audio_args = []
        if args.force:
            audio_args.append("--force")
        run_step("Generate Audio", SCRIPTS["audio"], audio_args)

    # Step 3: Video
    run_step("Assemble Video", SCRIPTS["video"])

    print("=" * 60)
    print("  Pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
