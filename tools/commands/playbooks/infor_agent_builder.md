# Playbook: infor-agent-builder

## Goal
Create/update GenAI TOOLKIT agents that orchestrate deployed tools.

## Workflow
1. Confirm required tools are deployed:
   - `python tools/commands/list_genai_assets.py --asset-type API_DOCS --prefix <prefix>`
2. Validate auth:
   - `python tools/commands/infor_auth.py`
3. Deploy agent asset:
   - `python tools/commands/deploy_genai_asset.py --operation create --spec-file <agent-spec.json>`
4. Verify agent visibility:
   - `python tools/commands/list_genai_assets.py --asset-type TOOLKIT --prefix <prefix>`

## Rules
- Agents reference already-deployed tool names.
- Keep logical IDs and naming conventions explicit in specs.
