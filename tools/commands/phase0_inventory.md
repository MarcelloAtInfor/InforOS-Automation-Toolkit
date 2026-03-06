# Phase 0 Inventory and Mapping

Date: 2026-03-05
Scope: `CC_OS_Project/.claude/commands/*.md` and `CC_OS_Project/.claude/agents/*.md`

## Summary
- Commands discovered: 8
- Agents discovered: 4
- Phase 0 disposition coverage: 12/12 complete

## Commands
| Source File | Capability | Primary Runtime Today | Target Shared Script | Disposition | Notes |
|---|---|---|---|---|---|
| `.claude/commands/query-ido.md` | Query SyteLine IDO data | Inline Python examples | `tools/commands/query_ido.py` | `port` | Phase 2 pilot candidate #1. |
| `.claude/commands/ido-lookup.md` | IDO discovery + metadata lookup | Inline Python examples | `tools/commands/ido_lookup.py` | `port` | Can call `query_ido.py` internally for metadata IDOs. |
| `.claude/commands/ido-update.md` | Insert/update/delete via IDO API | Inline Python examples | `tools/commands/ido_update.py` | `port` | Keep Action=4 delete rule as hard validation. |
| `.claude/commands/infor-auth.md` | Credential/token guidance | `shared/auth.py` module | `tools/commands/infor_auth.py` | `merge` | Keep thin wrapper around shared auth behavior, avoid duplicate token logic. |
| `.claude/commands/list-genai-assets.md` | List GenAI tools/agents | `GAF_CLI` CLI + raw API | `tools/commands/list_genai_assets.py` | `port` | Use GAF_CLI path when available; raw API fallback. |
| `.claude/commands/deploy-genai-asset.md` | Publish/update/enable/delete GenAI assets | `GAF_CLI` CLI + raw API | `tools/commands/deploy_genai_asset.py` | `port` | Validate spec path and operation mode before action. |
| `.claude/commands/send-pulse.md` | Build/send Pulse alert/notification/task | Inline payload patterns | `tools/commands/send_pulse.py` | `port` | Needs strict payload schema checks per type. |
| `.claude/commands/rpa-snippet.md` | Generate XAML snippets | Prompt templates | `tools/commands/rpa_snippet.py` | `defer` | Defer until command-core contracts are stable; high template/format variance. |

## Agents
| Source File | Capability | Target Playbook/Skill | Disposition | Notes |
|---|---|---|---|---|
| `.claude/agents/infor-tool-builder.md` | Build GenAI API_DOCS tools | `tools/commands/playbooks/infor_tool_builder.md` | `port` | Keep deployment path aligned to shared scripts + GAF_CLI. |
| `.claude/agents/infor-agent-builder.md` | Build GenAI TOOLKIT agents | `tools/commands/playbooks/infor_agent_builder.md` | `port` | Reuse shared deploy/list/auth commands. |
| `.claude/agents/ion-workflow-builder.md` | Build ION workflows + AES handlers | `tools/commands/playbooks/ion_workflow_builder.md` | `merge` | Merge with existing CSIWorkflowGenerator `wfgen.py` workflows, avoid duplicate orchestration logic. |
| `.claude/agents/idp-flow-manager.md` | Manage IDP DPF export/import/template flow | `tools/commands/playbooks/idp_flow_manager.md` | `defer` | Defer after command-core stabilization and preflight checks. |

## Phase 2 Pilot Recommendation
1. `query-ido` (`tools/commands/query_ido.py`)
2. `ido-lookup` (`tools/commands/ido_lookup.py`)

## Open Decisions Before Phase 1
1. Whether shared scripts should directly call `GAF_CLI` modules or shell out to `python -m src.cli.*`.
2. Final output mode defaults: `json` vs `table`.
3. Where Codex skill pack lives (`.codex/skills` in repo vs user-level install only).
