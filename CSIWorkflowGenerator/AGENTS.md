# AGENTS.md

## Startup Context (Required Every Session)
At the start of each new session in this repository, read these files first:
1. `AGENT_GUIDE.md` (cross-agent shared operating rules)
2. `../CLAUDE.md` if present (parent/org-level guidance)
3. `CLAUDE.md` (repo-level rules, conventions, and memory)
4. `log.md` (recent execution history and decisions)

If both files exist, treat them as authoritative project context before making plans or code changes.

## Session Workflow
1. Read `AGENT_GUIDE.md`, `../CLAUDE.md` (if present), `CLAUDE.md`, and `log.md` before doing substantive work.
2. Follow parent-level guidance first, then apply repo-specific constraints from `CLAUDE.md`.
3. After meaningful changes, append a concise entry to `log.md` with:
   - Date/time
   - What changed
   - Why
   - Open follow-ups

## Priority Order for Instructions
1. System/developer instructions from the runtime
2. This `AGENTS.md`
3. `AGENT_GUIDE.md`
4. `../CLAUDE.md` (if present)
5. `CLAUDE.md`
6. User request
7. Other repository docs

## Missing File Handling
- If `AGENT_GUIDE.md` is missing, continue with project-specific files.
- If `../CLAUDE.md` is missing, continue with repo-local context.
- If `CLAUDE.md` is missing, continue and note that startup memory was unavailable.
- If `log.md` is missing, create it on first write.
