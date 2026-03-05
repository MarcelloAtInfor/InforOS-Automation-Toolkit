# CSIWorkflowGenerator

Generate CSI (CloudSuite Industrial) workflow assets from compact JSON specs:
- ION workflow JSON
- AES event handlers (trigger + payload mapping)

This project is intentionally **agent-agnostic** for development with either:
- Claude Code
- Codex

## Agent-Agnostic Model

Core behavior is shared in:
- `AGENT_GUIDE.md`

Agent adapter files:
- `AGENTS.md` (Codex adapter)
- `CLAUDE.md` (Claude adapter + deep project reference)

Both adapters point to the same operating model so workflows and scripts remain portable across agents.

## What To Read First

1. `AGENT_GUIDE.md`
2. `CLAUDE.md`
3. `log.md` (private working history; not synced to public)

## Main CLI

```powershell
python scripts/wfgen.py create workflow_specs/<spec>.json --live --activate
python scripts/wfgen.py render workflow_specs/<spec>.json
python scripts/wfgen.py validate workflow_specs/<spec>.json --live
python scripts/wfgen.py status <WorkflowName>
python scripts/wfgen.py delete <WorkflowName>
```

## Private -> Public Sync

Private repo is source of truth. Public updates are manual and sanitized.

```powershell
powershell -File scripts/sync_public.ps1          # dry-run preview
powershell -File scripts/sync_public.ps1 -Apply   # copy allowed files
```

Sync policy lives in:
- `sync_public.json` (allowlist + deny globs)

`log.md` is private-only by policy.
