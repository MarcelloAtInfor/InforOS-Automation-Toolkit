"""Manage repo memory files for shared and local agent workflows."""
from __future__ import annotations

import argparse
import sys
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from common import build_result, emit_result, get_repo_root

COMMAND_ID = "memory-manager"
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
WORD_RE = re.compile(r"[A-Za-z0-9_]{2,}")

REPO_ROOT = get_repo_root()
SHARED_MEMORY_PATH = REPO_ROOT / "MEMORY.md"
LOCAL_MEMORY_PATH = REPO_ROOT / "MEMORY.local.md"
MEMORY_DIR = REPO_ROOT / "memory"

SHARED_MEMORY_TEMPLATE = """# Repository Memory

Use this file for durable, non-sensitive memory that is safe to commit and safe
to sync to the public repository.

## Keep Here
- Stable repository workflows
- Cross-project integration notes
- Durable lessons learned that are useful across sessions
- Information that should be visible to any contributor

## Do Not Put Here
- Secrets, tokens, or tenant-specific values
- Personal reminders that only belong on one machine
- Temporary scratch notes better suited for daily files

## Durable Notes
- Document confirmed patterns here as they become durable.
"""

LOCAL_MEMORY_TEMPLATE = """# Local Memory

Use this file for durable local-only memory that should never be committed.

## Good Uses
- Personal preferences for local AI workflows
- Machine-specific setup notes
- Private reminders that are not appropriate for `MEMORY.md`

## Durable Notes
- Add local-only notes here.
"""

DAILY_MEMORY_TEMPLATE = """# Daily Memory - {date}

Use this file for session notes, investigations, and short-lived context.

## Entries
"""


@dataclass
class SearchHit:
    path: str
    start_line: int
    end_line: int
    score: float
    snippet: str
    source: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "score": round(self.score, 2),
            "source": self.source,
            "snippet": self.snippet,
        }


def _today_string() -> str:
    return date.today().isoformat()


def _relative_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _ensure_file(path: Path, template: str) -> None:
    if path.exists():
        return
    _ensure_parent(path)
    path.write_text(template, encoding="utf-8")


def _ensure_daily_file(day: str) -> Path:
    path = MEMORY_DIR / f"{day}.md"
    _ensure_file(path, DAILY_MEMORY_TEMPLATE.format(date=day))
    return path


def _managed_daily_files() -> list[Path]:
    if not MEMORY_DIR.exists():
        return []
    files: list[Path] = []
    for path in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
        if path.name == "README.md":
            continue
        files.append(path)
    return files


def _resolve_scope_files(scope: str) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    if scope in {"all", "local"} and LOCAL_MEMORY_PATH.exists():
        entries.append(("local", LOCAL_MEMORY_PATH))
    if scope in {"all", "shared"} and SHARED_MEMORY_PATH.exists():
        entries.append(("shared", SHARED_MEMORY_PATH))
    if scope in {"all", "daily"}:
        entries.extend(("daily", path) for path in _managed_daily_files())
    return entries


def _safe_memory_path(raw_path: str) -> Path:
    candidate = Path(raw_path)
    resolved = candidate.resolve() if candidate.is_absolute() else (REPO_ROOT / candidate).resolve()

    if resolved == SHARED_MEMORY_PATH.resolve():
        return resolved
    if resolved == LOCAL_MEMORY_PATH.resolve():
        return resolved

    try:
        relative = resolved.relative_to(MEMORY_DIR.resolve())
    except ValueError as exc:
        raise ValueError("path is outside managed memory files") from exc

    if resolved.name == "README.md" or resolved.suffix.lower() != ".md":
        raise ValueError("path is outside managed memory files")
    return resolved


def _normalize_query_tokens(query: str) -> list[str]:
    seen: set[str] = set()
    tokens: list[str] = []
    for token in WORD_RE.findall(query.lower()):
        if token not in seen:
            seen.add(token)
            tokens.append(token)
    return tokens


def _daily_recency_bonus(path: Path) -> float:
    match = DATE_RE.match(path.name)
    if not match:
        return 0.25
    try:
        file_day = date.fromisoformat(match.group(1))
    except ValueError:
        return 0.25
    age_days = max(0, (date.today() - file_day).days)
    return 1.0 / (1.0 + (age_days / 7.0))


def _source_bonus(source: str, path: Path) -> float:
    if source == "daily":
        return _daily_recency_bonus(path)
    if source == "local":
        return 0.35
    return 0.2


def _build_match_windows(match_lines: list[int], context_lines: int) -> list[tuple[int, int]]:
    if not match_lines:
        return []
    windows: list[tuple[int, int]] = []
    start = match_lines[0]
    end = match_lines[0]
    for line_no in match_lines[1:]:
        if line_no <= end + (context_lines * 2) + 1:
            end = line_no
            continue
        windows.append((start, end))
        start = line_no
        end = line_no
    windows.append((start, end))
    return windows


def _search_file(
    *,
    source: str,
    path: Path,
    query: str,
    tokens: list[str],
    context_lines: int,
) -> list[SearchHit]:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []

    lines = content.splitlines()
    query_lower = query.lower().strip()
    match_lines: list[int] = []

    for idx, line in enumerate(lines, start=1):
        line_lower = line.lower()
        if query_lower and query_lower in line_lower:
            match_lines.append(idx)
            continue
        if tokens and any(token in line_lower for token in tokens):
            match_lines.append(idx)

    hits: list[SearchHit] = []
    for match_start, match_end in _build_match_windows(match_lines, context_lines):
        start_line = max(1, match_start - context_lines)
        end_line = min(len(lines), match_end + context_lines)
        snippet = "\n".join(lines[start_line - 1 : end_line]).strip()
        snippet_lower = snippet.lower()
        score = 0.0
        if query_lower:
            score += snippet_lower.count(query_lower) * 10.0
        for token in tokens:
            score += float(snippet_lower.count(token))
        score += _source_bonus(source, path)
        if score <= 0:
            continue
        hits.append(
            SearchHit(
                path=_relative_to_repo(path),
                start_line=start_line,
                end_line=end_line,
                score=score,
                snippet=snippet,
                source=source,
            )
        )
    return hits


def _append_entry(path: Path, entry: str, section: str | None = None) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    pieces: list[str] = []
    if existing and not existing.endswith("\n"):
        pieces.append("\n")
    if section:
        pieces.extend(["\n", f"## {section}\n"])
    pieces.append(f"{entry}\n")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("".join(pieces))


def _read_excerpt(path: Path, from_line: int | None, lines: int | None) -> tuple[str, int, int]:
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    split_lines = content.splitlines()
    start = max(1, from_line or 1)
    count = max(1, lines or len(split_lines))
    excerpt = "\n".join(split_lines[start - 1 : start - 1 + count])
    return excerpt, start, count


def run_status() -> dict[str, Any]:
    rows = [
        {
            "scope": "shared",
            "path": _relative_to_repo(SHARED_MEMORY_PATH),
            "exists": SHARED_MEMORY_PATH.exists(),
            "tracked": True,
            "description": "Commit-safe durable repository memory.",
        },
        {
            "scope": "local",
            "path": _relative_to_repo(LOCAL_MEMORY_PATH),
            "exists": LOCAL_MEMORY_PATH.exists(),
            "tracked": False,
            "description": "Local durable memory kept out of git.",
        },
        {
            "scope": "daily",
            "path": _relative_to_repo(MEMORY_DIR),
            "exists": MEMORY_DIR.exists(),
            "tracked": False,
            "description": "Daily note directory for memory/YYYY-MM-DD.md files.",
        },
    ]
    daily_files = [
        {
            "path": _relative_to_repo(path),
            "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        }
        for path in _managed_daily_files()[:10]
    ]
    return build_result(
        status="ok",
        command=COMMAND_ID,
        message="Memory paths resolved.",
        data={"paths": rows, "recent_daily_files": daily_files},
    )


def run_capture(*, target: str, text: str, day: str | None, section: str | None) -> dict[str, Any]:
    if target == "shared":
        _ensure_file(SHARED_MEMORY_PATH, SHARED_MEMORY_TEMPLATE)
        target_path = SHARED_MEMORY_PATH
        entry = f"- {text.strip()}"
    elif target == "local":
        _ensure_file(LOCAL_MEMORY_PATH, LOCAL_MEMORY_TEMPLATE)
        target_path = LOCAL_MEMORY_PATH
        entry = f"- {text.strip()}"
    else:
        resolved_day = day or _today_string()
        target_path = _ensure_daily_file(resolved_day)
        timestamp = datetime.now().strftime("%H:%M")
        entry = f"- {timestamp} {text.strip()}"

    _append_entry(target_path, entry, section=section)
    return build_result(
        status="ok",
        command=COMMAND_ID,
        message=f"Appended note to {_relative_to_repo(target_path)}.",
        data={
            "target": target,
            "path": _relative_to_repo(target_path),
            "entry": entry,
            "section": section,
        },
    )


def run_search(*, query: str, scope: str, max_results: int, context_lines: int) -> dict[str, Any]:
    query_clean = query.strip()
    if not query_clean:
        return build_result(
            status="error",
            command=COMMAND_ID,
            message="Missing search query.",
            errors=["Provide --query with one or more search terms."],
        )

    tokens = _normalize_query_tokens(query_clean)
    hits: list[SearchHit] = []
    for source, path in _resolve_scope_files(scope):
        hits.extend(
            _search_file(
                source=source,
                path=path,
                query=query_clean,
                tokens=tokens,
                context_lines=context_lines,
            )
        )

    hits.sort(key=lambda item: (-item.score, item.path, item.start_line))
    rows = [hit.as_dict() for hit in hits[:max_results]]
    return build_result(
        status="ok",
        command=COMMAND_ID,
        message=f"Found {len(rows)} memory hit(s).",
        data={
            "query": query_clean,
            "scope": scope,
            "count": len(rows),
            "results": rows,
        },
    )


def run_get(*, raw_path: str, from_line: int | None, lines: int | None) -> dict[str, Any]:
    try:
        path = _safe_memory_path(raw_path)
    except ValueError as exc:
        return build_result(
            status="error",
            command=COMMAND_ID,
            message="Invalid memory path.",
            errors=[str(exc)],
        )

    if not path.exists():
        return build_result(
            status="ok",
            command=COMMAND_ID,
            message="Memory file does not exist yet.",
            data={"path": _relative_to_repo(path), "text": ""},
        )

    content = path.read_text(encoding="utf-8")
    if from_line is None and lines is None:
        return build_result(
            status="ok",
            command=COMMAND_ID,
            message="Memory file loaded.",
            data={"path": _relative_to_repo(path), "text": content},
        )

    excerpt, start, count = _read_excerpt(path, from_line, lines)
    return build_result(
        status="ok",
        command=COMMAND_ID,
        message="Memory excerpt loaded.",
        data={
            "path": _relative_to_repo(path),
            "from": start,
            "lines": count,
            "text": excerpt,
        },
    )


def run_promote(
    *,
    source_path: str,
    target: str,
    text: str | None,
    from_line: int | None,
    lines: int | None,
    section: str | None,
) -> dict[str, Any]:
    try:
        source = _safe_memory_path(source_path)
    except ValueError as exc:
        return build_result(
            status="error",
            command=COMMAND_ID,
            message="Invalid source memory path.",
            errors=[str(exc)],
        )

    if target not in {"shared", "local"}:
        return build_result(
            status="error",
            command=COMMAND_ID,
            message="Invalid promote target.",
            errors=["Target must be shared or local."],
        )

    if not source.exists():
        return build_result(
            status="error",
            command=COMMAND_ID,
            message="Source memory file does not exist.",
            errors=[_relative_to_repo(source)],
        )

    if target == "shared":
        _ensure_file(SHARED_MEMORY_PATH, SHARED_MEMORY_TEMPLATE)
        destination = SHARED_MEMORY_PATH
    else:
        _ensure_file(LOCAL_MEMORY_PATH, LOCAL_MEMORY_TEMPLATE)
        destination = LOCAL_MEMORY_PATH

    if text and text.strip():
        entry = f"- {text.strip()}"
        promoted_text = text.strip()
        source_meta: dict[str, Any] = {"path": _relative_to_repo(source)}
    else:
        excerpt, start, count = _read_excerpt(source, from_line, lines)
        promoted_text = excerpt.strip()
        if not promoted_text:
            return build_result(
                status="error",
                command=COMMAND_ID,
                message="Nothing to promote.",
                errors=["Provide --text or a non-empty --from/--lines range."],
            )
        entry = f"- Promoted from {_relative_to_repo(source)}:{start}\n{promoted_text}"
        source_meta = {"path": _relative_to_repo(source), "from": start, "lines": count}

    _append_entry(destination, entry, section=section)
    return build_result(
        status="ok",
        command=COMMAND_ID,
        message=f"Promoted note into {_relative_to_repo(destination)}.",
        data={
            "target": target,
            "destination": _relative_to_repo(destination),
            "source": source_meta,
            "section": section,
            "entry": entry,
        },
    )


def _emit_for_mode(result: dict[str, Any], output_mode: str) -> None:
    if output_mode == "table" and result.get("status") == "ok":
        data = result.get("data", {})
        if isinstance(data, dict):
            rows = data.get("results") or data.get("paths") or data.get("recent_daily_files")
            if isinstance(rows, list) and rows and all(isinstance(row, dict) for row in rows):
                emit_result({"data": rows}, output_mode="table")
                return
    emit_result(result, output_mode="json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage repo memory files.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-mode", choices=["json", "table"], default="json")

    output_parent = argparse.ArgumentParser(add_help=False)
    output_parent.add_argument("--output-mode", choices=["json", "table"], default="json")

    subparsers = parser.add_subparsers(dest="action")
    subparsers.add_parser(
        "status",
        help="Show managed memory paths and recent daily files.",
        parents=[output_parent],
    )

    capture_parser = subparsers.add_parser(
        "capture",
        help="Append a note to a memory file.",
        parents=[output_parent],
    )
    capture_parser.add_argument("--target", choices=["daily", "shared", "local"], default="daily")
    capture_parser.add_argument("--text", help="Text to append.")
    capture_parser.add_argument("--date", help="Override daily file date (YYYY-MM-DD).")
    capture_parser.add_argument("--section", help="Optional heading appended before the entry.")

    search_parser = subparsers.add_parser(
        "search",
        help="Search across memory files.",
        parents=[output_parent],
    )
    search_parser.add_argument("--query", help="Query string to search for.")
    search_parser.add_argument("--scope", choices=["all", "shared", "local", "daily"], default="all")
    search_parser.add_argument("--max-results", type=int, default=8)
    search_parser.add_argument("--context-lines", type=int, default=1)

    get_parser = subparsers.add_parser(
        "get",
        help="Read a managed memory file.",
        parents=[output_parent],
    )
    get_parser.add_argument("--path", help="Managed memory file path.")
    get_parser.add_argument("--from", dest="from_line", type=int)
    get_parser.add_argument("--lines", type=int)

    promote_parser = subparsers.add_parser(
        "promote",
        help="Promote distilled notes or excerpts into shared/local durable memory.",
        parents=[output_parent],
    )
    promote_parser.add_argument("--source", help="Managed source memory file path.")
    promote_parser.add_argument("--target", choices=["shared", "local"], required=True)
    promote_parser.add_argument("--text", help="Distilled text to promote.")
    promote_parser.add_argument("--from", dest="from_line", type=int)
    promote_parser.add_argument("--lines", type=int)
    promote_parser.add_argument("--section", help="Optional heading appended before the entry.")

    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command=COMMAND_ID,
                message="Dry-run only.",
                data={"args": vars(args)},
            ),
            output_mode="json",
        )
        return 0

    action = args.action or "status"
    if action == "status":
        result = run_status()
    elif action == "capture":
        if not args.text:
            result = build_result(
                status="error",
                command=COMMAND_ID,
                message="Missing capture text.",
                errors=["Provide --text to append a note."],
            )
        else:
            result = run_capture(
                target=args.target,
                text=args.text,
                day=args.date,
                section=args.section,
            )
    elif action == "search":
        result = run_search(
            query=args.query or "",
            scope=args.scope,
            max_results=max(1, args.max_results),
            context_lines=max(0, args.context_lines),
        )
    elif action == "get":
        if not args.path:
            result = build_result(
                status="error",
                command=COMMAND_ID,
                message="Missing memory path.",
                errors=["Provide --path for a managed memory file."],
            )
        else:
            result = run_get(
                raw_path=args.path,
                from_line=args.from_line,
                lines=args.lines,
            )
    elif action == "promote":
        if not args.source:
            result = build_result(
                status="error",
                command=COMMAND_ID,
                message="Missing promote source path.",
                errors=["Provide --source for a managed memory file."],
            )
        else:
            result = run_promote(
                source_path=args.source,
                target=args.target,
                text=args.text,
                from_line=args.from_line,
                lines=args.lines,
                section=args.section,
            )
    else:
        result = build_result(
            status="error",
            command=COMMAND_ID,
            message="Unknown action.",
            errors=[f"Unsupported action: {action}"],
        )

    _emit_for_mode(result, args.output_mode)
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
