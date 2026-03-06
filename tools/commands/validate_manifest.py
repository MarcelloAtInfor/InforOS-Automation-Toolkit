"""Validate tools/commands/commands.json against manifest.schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    schema_path = root / "manifest.schema.json"
    manifest_path = root / "commands.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    try:
        import jsonschema  # type: ignore
    except ImportError:
        print("ERROR: jsonschema is required. Install with: pip install jsonschema")
        return 2

    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.path))
    if errors:
        print(f"INVALID: {len(errors)} schema error(s)")
        for err in errors:
            path = ".".join(str(x) for x in err.path) or "(root)"
            print(f" - {path}: {err.message}")
        return 1

    print("VALID: commands.json matches manifest.schema.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

