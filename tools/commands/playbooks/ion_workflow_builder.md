# Playbook: ion-workflow-builder

## Goal
Build/deploy ION workflows and related AES handlers consistently.

## Workflow
1. Use CSIWorkflowGenerator commands for workflow lifecycle:
   - `python CSIWorkflowGenerator/scripts/wfgen.py validate <spec>`
   - `python CSIWorkflowGenerator/scripts/wfgen.py render <spec>`
   - `python CSIWorkflowGenerator/scripts/wfgen.py create <spec> --live --activate`
2. Use shared command core for auxiliary IDO metadata lookups when needed:
   - `python tools/commands/ido_lookup.py ...`
3. Record deployment/test outcomes in relevant `log.md`.

## Rules
- Keep workflow and AES logic in project code, not adapter markdown.
- Use `wfgen delete` for cleanup where needed.
