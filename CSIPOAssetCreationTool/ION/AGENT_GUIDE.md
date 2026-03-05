# AGENT_GUIDE.md

## Purpose
Cross-agent operating guide for this folder so Claude Code and Codex follow the same workflow and memory model.

## Startup Context
Read before substantive work:
1. ../CLAUDE.md if present (parent context)
2. CLAUDE.md (folder-specific rules and architecture)
3. log.md (recent work state)

## Memory Pattern
- Put durable, confirmed behavior in CLAUDE.md.
- Put session-level progress and decisions in log.md.

## Agent Compatibility
This folder is agent-agnostic by design.
- AGENTS.md is the Codex adapter.
- CLAUDE.md is the Claude adapter/reference.
- Shared operating behavior lives in this file.


