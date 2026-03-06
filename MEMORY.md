# Repository Memory

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
- Root agent memory model:
  - `CLAUDE.md` stores durable agent-facing rules and architecture.
  - `log.md` stores session history and progress.
  - `MEMORY.md` stores durable, commit-safe working memory.
  - `MEMORY.local.md` and `memory/YYYY-MM-DD.md` are local-only memory layers.
