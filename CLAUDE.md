# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Documentation Rule (CRITICAL - NEVER SKIP)

**ALWAYS update CLAUDE.md and log.md files when making changes. This is mandatory, not optional.**

### CLAUDE.md
- Update whenever changes are made, discoveries are confirmed, or new patterns are established
- This is the knowledge base for future sessions - if it's not in CLAUDE.md, it will be forgotten
- Applies to EVERY level: root CLAUDE.md, subfolder CLAUDE.md files, including GAF_CLI

### log.md
- Update WHILE working, not just at the end - record completed steps, current status, discoveries, and next steps
- Use session dates as headers (e.g., `## Session Date: 2026-02-10`)
- This is the running history of the project and helps maintain context across sessions
- Applies to EVERY level: root log.md and all subfolder log.md files

### Git Commits (CRITICAL - NEVER SKIP)
- **ALWAYS make an atomic git commit at the end of every session** — no exceptions
- An "atomic commit" means: stage only the files changed during the session, write a clear commit message summarizing the work done, and commit before ending
- This ensures no work is ever lost between sessions and provides a clean history of changes
- Commit message should follow the pattern: `<type>: <concise summary>` (e.g., `feat:`, `fix:`, `refactor:`, `docs:`)
- If multiple logical units of work were done in a session, prefer one commit per logical unit
- This applies at EVERY level — whether working in root, a subfolder, or across multiple folders

## Repository Overview

This is a multi-product demonstration and automation repository for Infor OS (Operating System) platform. It serves as an umbrella organizer for multiple projects that may share knowledge, patterns, and integration points.

**Key Principle**: This is NOT a single codebase project. It's a collection of independent but related projects.

**Current structure** (3 top-level projects + shared utilities):

| Folder | Purpose |
|--------|---------|
| `CSIPOAssetCreationTool/` | Invoice Automation Enhancement — GenAI + RPA + IDP for SyteLine (v1.0 shipped) |
| `BOMGenerator/` | GenAI agent for multi-level Bill of Material creation from natural language |
| `GAF_CLI/` | GenAI Agent Factory CLI — Python toolkit for publishing, managing, and invoking GenAI tools and agents |
| `shared/` | Centralized authentication and configuration utilities |
| `tools/commands/` | Agent-agnostic shared command layer scaffold (manifest + command entrypoints for Claude/Codex adapters) |

### GAF_CLI (GenAI Agent Factory CLI)
**Location**: `./GAF_CLI` (internal to this repository)
**Purpose**: Python CLI toolkit for creating, managing, and invoking Infor OS GenAI tools and agents.

**Key Commands** (run from `GAF_CLI/` directory):
```bash
# Validate a spec before publishing
python -m src.cli.validate_spec specs/tools/YourTool.json

# Publish tools and agents
python -m src.cli.publish_tool specs/tools/YourTool.json
python -m src.cli.publish_agent specs/agents/YourAgent.json

# Update an existing asset (spec must include "guid" field)
python -m src.cli.update_asset specs/tools/YourTool.json

# List assets
python -m src.cli.list_assets --prefix GAF_SyteLine

# Invoke an agent (interactive or single prompt)
python -m src.cli.invoke_agent "Your prompt here"
python -m src.cli.invoke_agent -i                    # Interactive mode
python -m src.cli.invoke_agent "prompt" --json        # Raw JSON output
```

**Agent Invocation**: Uses `chat_sync` via GenAI Chat API (`/api/v1/chat/sync`). The `tools` parameter accepts a list of agent/tool names to route the prompt to. For long-running agents, use `--async` flag for async chat pattern.

**Authentication**: GAF_CLI has its own `src/shared/` module (separate from root `shared/`). It uses env var `IONAPI_FILE` or `.ionapi` in CWD for credentials. See `GAF_CLI/CLAUDE.md` for full documentation.

## Repository Structure

### shared/
**Purpose**: Centralized authentication and configuration utilities used across all projects

**Technology**: Python modules
- `auth.py`: OAuth 2.0 token generation, in-memory caching, auto-fetch, env-var credential resolution
- `config.py`: Tenant configuration and URL construction (derived from credentials, not hardcoded)

**Status**: Stable. Single source of truth for authentication.

**Credential Resolution** (in order):
1. `IONAPI_FILE` env var → path to `.ionapi` file
2. `.ionapi` in current working directory

**Setup**: Set the `IONAPI_FILE` environment variable to point to your `.ionapi` credentials file:
```bash
# Windows
set IONAPI_FILE=C:\path\to\your\credentials.ionapi

# Linux/Mac
export IONAPI_FILE=/path/to/your/credentials.ionapi
```

**Key Files**:
- `shared/auth.py` - Token generation (password grant), caching, auto-fetch
- `shared/config.py` - Service URL construction (from `iu` field in credentials)
- `shared/<your-credentials>.ionapi` - Credentials file (set `IONAPI_FILE` env var to point here)

See `shared/CLAUDE.md` for full API reference, usage patterns, and credential setup.

### GAF_CLI/
**Purpose**: Python CLI toolkit for creating, managing, and invoking Infor OS GenAI tools and agents.

**Contains**: 6 CLI commands, GenAI API client, spec validation engine, 7 tool specs + 1 agent spec.

**Note on `shared/` modules**: GAF_CLI has its own `src/shared/` (auth, config, validation, errors, http_client, logging — ~1,150 lines). This is separate from root `shared/` (~300 lines). Both coexist — different import paths (`from src.shared.*` vs `from shared.*`), different design (class-based vs function-based). Both now use `IONAPI_FILE` env var for credential resolution.

**Status**: Stable. See `GAF_CLI/CLAUDE.md` for full documentation.

### CSIPOAssetCreationTool/
**Purpose**: Invoice Automation Enhancement — GenAI-powered invoice processing with RPA, IDP, and SyteLine integration.

**Contains**: Agents&Tools, RPA, ION, IDM, IDP subfolders.

**Status**: v1.0 shipped. See `CSIPOAssetCreationTool/CLAUDE.md` for full project documentation.

### BOMGenerator/
**Purpose**: GenAI agent that generates realistic multi-level Bill of Material (BOM) data from natural language prompts.

**Contains**: 16 tools + 1 agent, test harness, verification scripts.

**Status**: Phases 0-4 complete. All assets deployed. See `BOMGenerator/CLAUDE.md` for full documentation.

## Global Working Requirements

### Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.**

This is a hard requirement, not a suggestion. Infor OS is NOT a typical local development stack:
- There is no local runtime to test against - validation requires the live Infor Cloud environment
- Missing domain knowledge (IDO names, property casing, API quirks) leads to MANY errors per phase
- Claude lacks direct access to verify results - only the user can confirm things work
- "Big bang" approaches (building all phases at once) create enormous messes that are painful to untangle

**The workflow for phased work is:**
1. Complete Phase N (code, specs, configs, etc.)
2. **STOP** - Present results to user and explicitly ask for testing/validation
3. **WAIT** - Do NOT proceed until the user confirms Phase N works correctly
4. Only after user approval, begin Phase N+1
5. Repeat until all phases are complete

**What "STOP" means:**
- Do NOT silently continue to the next phase
- Do NOT assume the phase worked because the code looks right
- Do NOT batch multiple phases together "for efficiency"
- DO summarize what was done, what needs testing, and how to test it
- DO ask the user to validate in their Infor environment

**This applies to:**
- Any work explicitly divided into phases by the user or by planning
- Multi-step implementations where each step depends on the previous
- Tool/agent creation workflows (create → test → iterate → next)
- Any work involving Infor platform APIs where results can't be verified locally

### Documentation Standards

**CLAUDE.md Files**:
- Every subfolder MUST have a `CLAUDE.md` file
- When working in a subfolder, ALWAYS read its `CLAUDE.md` first
- If `CLAUDE.md` is missing, ask the user about the folder's purpose before creating one
- When errors are fixed or solutions discovered, update the relevant `CLAUDE.md`
- Include folder-specific commands, architecture, and lessons learned

**log.md Files**:
- Every subfolder MUST have a `log.md` file
- ALWAYS update `log.md` while working to track:
  - Completed steps and current status
  - New discoveries and technical insights
  - Issues encountered and resolutions
  - Next steps and blockers
- Use session dates as headers (e.g., `## Session Date: 2026-01-28`)
- Log serves as running history across sessions

## Workspace Memory Layer

Use the repo memory layers intentionally:

- `CLAUDE.md`: durable agent-facing rules, architecture, and confirmed patterns
- `log.md`: session-by-session execution history
- `MEMORY.md`: durable repository memory that is safe to commit and safe to sync publicly
- `MEMORY.local.md`: optional local-only durable memory; never commit
- `memory/YYYY-MM-DD.md`: optional local daily notes; never commit

Guidance:
- Put durable repo rules and architectural truths in `CLAUDE.md`.
- Put completed work and chronological session history in `log.md`.
- Put durable working memory that is helpful but not instruction-like in `MEMORY.md`.
- Put personal preferences or machine-specific notes in `MEMORY.local.md`.
- Put short-lived investigation notes in `memory/YYYY-MM-DD.md`.

Memory promotion cadence:
- Review recent daily memory at the start of a new session only when continuing related work.
- Promote durable notes at major phase boundaries and before ending a substantial session.
- Do not promote after every small task or minor edit.
- Default review window is bounded to the current daily file plus at most the two most recent prior daily files.
- Use `MEMORY.md` only for commit-safe durable memory that can live in the public repo.
- Use `MEMORY.local.md` for local-only durable memory.

Session closeout checklist:
- Update `log.md` with what was done, validation, and next steps.
- Promote durable findings from daily memory when warranted.
- Update `CLAUDE.md` only if the session established durable new rules or patterns.
- Keep closeout bounded; do not scan broad history unless the session materially changed project context.

Shared CLI:
```bash
python tools/commands/memory_manager.py status
python tools/commands/memory_manager.py capture --target daily --text "Investigated issue X"
python tools/commands/memory_manager.py search --query "issue X" --output-mode table
python tools/commands/memory_manager.py get --path MEMORY.md --from 1 --lines 20
python tools/commands/memory_manager.py promote --source memory/2026-03-06.md --target shared --text "Durable insight"
```

## Navigation Guide

### When Starting Work in a Subfolder:
1. Read the subfolder's `CLAUDE.md` for context and architecture
2. Read the subfolder's `log.md` to understand recent work and status
3. If either file is missing, ask user about folder purpose
4. Update `log.md` throughout your work session
5. Update `CLAUDE.md` when solutions or patterns are confirmed

### When Creating New Subfolders:
1. Ask user about the folder's purpose and scope
2. Create `CLAUDE.md` with relevant architecture and commands
3. Create `log.md` to track progress from the start
4. Document integration points with existing folders if applicable

### When Errors Occur:
1. Document the error in the subfolder's `log.md`
2. After fixing, update `CLAUDE.md` with the solution for future reference
3. Include enough detail for future Claude instances to avoid the same issue

## Repository Purpose

This folder serves as:
1. **Organizer**: Logical grouping of related Infor OS work
2. **Knowledge Base**: Shared patterns and solutions across products
3. **Integration Hub**: Projects reference each other for end-to-end automation
4. **Context Preserver**: Documentation ensures continuity across sessions

## Getting Started

1. Determine which project is relevant to your task
2. Read that project's `CLAUDE.md` and `log.md`
3. If unclear, ask user which area to work in
4. Follow project-specific guidelines and patterns
5. Update documentation as you work

---

**Note**: This repository is actively developed with frequent discoveries. Always check `log.md` files for latest status and known issues. When in doubt, read the subfolder's documentation first.

## Cross-Agent Compatibility (Claude + Codex)

This repository now supports a shared, agent-agnostic workflow at the parent and subfolder levels.

- Shared human/agent guidance: `AGENT_GUIDE.md`
- Codex adapter: `AGENTS.md`
- Claude adapter/reference: `CLAUDE.md`
- Shared command scaffold: `tools/commands/` (`commands.json`, `manifest.schema.json`, `validate_manifest.py`, `verify_setup.py`)
  - Active commands: `query_ido.py`, `ido_lookup.py`, `infor_auth.py`, `ido_update.py`, `list_genai_assets.py`, `deploy_genai_asset.py`, `send_pulse.py`, `memory_manager.py`
  - Shared playbooks: `tools/commands/playbooks/*.md` with thin adapters in `.claude/agents/*.md`

Manual private->public sync is available from repo root:
- `powershell -File scripts/sync_public.ps1`
- `powershell -File scripts/sync_public.ps1 -Apply`

Sync policy is defined in `sync_public.json`.

