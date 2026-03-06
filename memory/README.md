# Local Daily Memory

This folder is for local daily notes in the canonical format:

- `memory/YYYY-MM-DD.md`

These files are intentionally ignored by git. They are meant for:

- session notes
- scratch context that should survive agent resets
- investigation breadcrumbs
- temporary reminders that do not belong in `CLAUDE.md` or `MEMORY.md`

Use the shared command to work with memory files:

```bash
python tools/commands/memory_manager.py status
python tools/commands/memory_manager.py capture --target daily --text "Investigated BOM timeout behavior"
python tools/commands/memory_manager.py search --query "timeout behavior" --output-mode table
python tools/commands/memory_manager.py promote --source memory/2026-03-06.md --target local --from 1 --lines 20
```

Promotion cadence:

- Promote durable notes when finishing a substantial phase or before ending a long session.
- Skip promotion for minor edits or short exploratory checks.
- Review only recent files by default; do not scan the full history each session.
