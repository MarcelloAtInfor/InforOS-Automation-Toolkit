# Playbook: idp-flow-manager

## Goal
Manage IDP DPF flows using export/template/import lifecycle.

## Workflow
1. Validate auth:
   - `python tools/commands/infor_auth.py`
2. List current GenAI assets if orchestration tools are involved:
   - `python tools/commands/list_genai_assets.py --prefix <prefix>`
3. Use project-specific IDP scripts for export/import.
4. Track changes in project `CLAUDE.md` and `log.md`.

## Rules
- Prefer template-based DPF creation over from-scratch payloads.
- Keep DPF GUID/name mappings documented.
