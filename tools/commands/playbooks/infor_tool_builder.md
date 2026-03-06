# Playbook: infor-tool-builder

## Goal
Create/update a GenAI tool spec and deploy it using shared commands.

## Workflow
1. Discover IDO and properties:
   - `python tools/commands/ido_lookup.py --mode collections --keyword "<domain>"`
   - `python tools/commands/ido_lookup.py --mode properties --collection-name "<IDO>"`
2. Validate auth readiness:
   - `python tools/commands/infor_auth.py`
3. Deploy tool asset:
   - `python tools/commands/deploy_genai_asset.py --operation create --spec-file <tool-spec.json>`
4. Verify deployment:
   - `python tools/commands/list_genai_assets.py --prefix <prefix> --asset-type API_DOCS`

## Rules
- One tool = one API call at runtime.
- Use exact IDO/property casing.
- Keep tool names stable and versioned.
