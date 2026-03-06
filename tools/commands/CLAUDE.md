# CLAUDE.md - tools/commands

## Purpose
Shared, agent-agnostic command layer for Claude and Codex adapters.

This folder is the single source of truth for command contracts and executable command scripts that should be reusable across projects.

## Phase Scope
- Phase 0: Inventory and contract draft
- Phase 1: Scaffold and validation
- Phase 2+: Incremental command implementation

## Structure
- `commands.json`: command manifest
- `manifest.schema.json`: manifest schema
- `validate_manifest.py`: manifest/schema validator
- `common.py`: shared helpers (path bootstrap, output formatting, response envelope)
- `<command>.py`: one entrypoint script per command id
- `contracts/*.schema.json`: output contract schemas per command

## Output Contract Baseline
All command scripts should return this envelope:
```json
{
  "status": "ok|planned|error",
  "command": "command-id",
  "message": "human-readable summary",
  "data": {},
  "errors": []
}
```

## Current Status
- Manifest validation and setup verification are wired.
- Active commands implemented:
  - `query_ido.py`
  - `ido_lookup.py`
  - `infor_auth.py`
  - `ido_update.py`
  - `list_genai_assets.py`
  - `deploy_genai_asset.py`
  - `send_pulse.py`
  - `memory_manager.py`
- Deferred command:
  - `rpa_snippet.py` (scaffold mode)
- Agent playbooks:
  - `playbooks/infor_tool_builder.md`
  - `playbooks/infor_agent_builder.md`
  - `playbooks/idp_flow_manager.md`
  - `playbooks/ion_workflow_builder.md`

## Commands
Validate manifest:
```bash
python tools/commands/validate_manifest.py
```

Dry-run any scaffolded command:
```bash
python tools/commands/query_ido.py --dry-run
```

Memory workflow examples:
```bash
python tools/commands/memory_manager.py status
python tools/commands/memory_manager.py capture --target daily --text "Investigated issue X"
python tools/commands/memory_manager.py search --query "issue X" --output-mode table
python tools/commands/memory_manager.py promote --source memory/2026-03-06.md --target shared --text "Durable insight"
```
