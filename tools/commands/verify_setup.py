"""Phase-1 setup verifier for shared command scaffold."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / "commands.json").read_text(encoding="utf-8"))

    # 1) Manifest schema validation
    rc = subprocess.call([sys.executable, str(base / "validate_manifest.py")])
    if rc != 0:
        return rc

    # 2) Entrypoint existence + dry-run viability
    failures: list[str] = []
    for cmd in manifest.get("commands", []):
        entrypoint = cmd["entrypoint"]
        script = base.parents[1] / Path(*entrypoint.split("/"))
        if not script.exists():
            failures.append(f"{cmd['id']}: missing entrypoint {script}")
            continue
        result = subprocess.run(
            [sys.executable, str(script), "--dry-run"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            failures.append(f"{cmd['id']}: dry-run failed ({result.returncode})")

    if failures:
        print("VERIFY FAILED")
        for item in failures:
            print(f" - {item}")
        return 1

    print("VERIFY OK: manifest + entrypoints + dry-run checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
