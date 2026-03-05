# AGENT_GUIDE.md

## Purpose
Cross-agent operating guide for this project so Claude Code and Codex follow the same workflow and memory model.

## Source Of Truth
- Private working project is the source of truth.
- Public toolkit is updated only by explicit manual sync.
- Never publish credentials, tenant-specific secrets, or local-only runtime files.

## Startup Context (All Agents)
Read these files before substantive work:
1. `../CLAUDE.md` if present (parent/org context)
2. `CLAUDE.md` (project rules and architecture)
3. `log.md` (latest work state)

## Session Memory Pattern
- Stable knowledge and confirmed patterns go to `CLAUDE.md`.
- Session progress, test outcomes, and next steps go to `log.md`.
- Update both while working, not only at the end.

## Cross-Agent Compatibility Rules
- Keep shared workflows in agent-neutral files/scripts.
- Avoid agent-specific logic unless required by the runtime.
- If an agent-specific file exists (`AGENTS.md`, `CLAUDE.md`), keep it as an adapter that points back to this guide.

## Public Sync Policy
- Sync is manual and user-triggered.
- Use `scripts/sync_public.ps1` with `sync_public.json`.
- Default mode is dry-run preview.
- Use `-Apply` only when ready to copy.
- Commit and push are separate user-triggered actions.

## Suggested Sync Workflow
1. Finish and validate changes in private project.
2. Run dry-run preview:
   - `pwsh -File scripts/sync_public.ps1`
3. Apply sync:
   - `pwsh -File scripts/sync_public.ps1 -Apply`
4. Review diff in public repo, then commit/push when requested.
