"""Common helpers for shared command scripts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def get_repo_root() -> Path:
    """Return CC_OS_Project repo root."""
    return Path(__file__).resolve().parents[2]


def ensure_repo_import_path() -> None:
    """Ensure repo root is importable so `shared.*` imports work."""
    root = str(get_repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)


def build_result(
    *,
    status: str,
    command: str,
    message: str,
    data: Any | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    """Standard envelope used by all command entrypoints."""
    return {
        "status": status,
        "command": command,
        "message": message,
        "data": data if data is not None else {},
        "errors": errors or [],
    }


def _render_table(rows: list[dict[str, Any]]) -> str:
    """Render a simple ASCII table for list-of-dict data."""
    if not rows:
        return "(no rows)"

    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                keys.append(key)
                seen.add(key)

    widths: dict[str, int] = {k: len(k) for k in keys}
    for row in rows:
        for key in keys:
            widths[key] = max(widths[key], len(str(row.get(key, ""))))

    header = " | ".join(f"{k:<{widths[k]}}" for k in keys)
    sep = "-+-".join("-" * widths[k] for k in keys)
    body = [
        " | ".join(f"{str(row.get(k, '')):<{widths[k]}}" for k in keys)
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def emit_result(result: dict[str, Any], output_mode: str = "json") -> None:
    """Print result in the requested output mode."""
    if output_mode == "table":
        data = result.get("data")
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            print(_render_table(data))
            return
    print(json.dumps(result, indent=2, ensure_ascii=False))


def load_json_file(path: str) -> Any:
    """Load JSON from a file path."""
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def run_planned_stub(command_id: str, args: dict[str, Any]) -> int:
    """Return a consistent planned-status response for scaffold commands."""
    result = build_result(
        status="planned",
        command=command_id,
        message="Scaffold only. Command implementation is scheduled for a later phase.",
        data={"args": args},
    )
    emit_result(result, output_mode="json")
    return 0
