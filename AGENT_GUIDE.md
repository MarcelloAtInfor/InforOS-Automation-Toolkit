# AGENT_GUIDE.md

## Purpose
Cross-agent operating guide for this folder so Claude Code and Codex follow the same workflow and memory model.

## Startup Context
Read before substantive work:
1. ../CLAUDE.md if present (parent context)
2. CLAUDE.md (folder-specific rules and architecture)
3. log.md (recent work state)
4. `MEMORY.local.md` if present and relevant to the task
5. `MEMORY.md` if present and relevant to the task
6. the current or most recent `memory/YYYY-MM-DD.md` file when continuing recent work

## Memory Pattern
- Put durable, confirmed behavior in CLAUDE.md.
- Put session-level progress and decisions in log.md.
- Put durable, commit-safe working memory in MEMORY.md.
- Put local-only durable memory in MEMORY.local.md.
- Put short-lived daily notes in memory/YYYY-MM-DD.md.

## Memory Promotion Cadence
- Promote durable notes from daily memory into `MEMORY.md` or `MEMORY.local.md` only at bounded checkpoints:
  - at the start of a new session when continuing prior work and recent daily memory contains durable findings
  - at the end of a major phase or after a substantial discovery set
  - before ending a long session with meaningful new context
- Do not promote after every small step, file read, or minor edit.
- Keep startup review bounded:
  - review the current daily file first
  - if needed, review at most the two most recent prior daily files
- Promote to `MEMORY.md` only when the information is commit-safe and useful to other contributors.
- Promote to `MEMORY.local.md` when the information is personal, machine-specific, or not suitable for the public repo.

## Session Closeout Checklist
- Update `log.md` with completed work, validation status, and next steps.
- If durable findings emerged, promote them from daily memory into `MEMORY.md` or `MEMORY.local.md`.
- Update `CLAUDE.md` only when new durable rules or confirmed patterns were established.
- Keep closeout bounded: do not reread broad history unless the session introduced substantial new context.

## Agent Compatibility
This folder is agent-agnostic by design.
- AGENTS.md is the Codex adapter.
- CLAUDE.md is the Claude adapter/reference.
- Shared operating behavior lives in this file.


