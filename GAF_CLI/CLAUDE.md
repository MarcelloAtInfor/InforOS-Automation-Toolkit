# Infor OS GenAI Agent Factory

A Python CLI toolkit for creating and managing Infor OS GenAI tools and agents. The Factory Agent uses a two-step DRAFT -> CONFIRM PUBLISH workflow for safe asset creation.

**Location**: This project lives at `CC_OS_Project/GAF_CLI/` (migrated from standalone repo on 2026-02-13). Original GitHub repo: `MarcelloAtInfor/GAF_CLI` (archived reference).

**Note on `shared/` modules**: This project has its own `src/shared/` (auth, config, validation, errors, http_client, logging). This is separate from the root `CC_OS_Project/shared/` module. Both coexist with different import paths (`from src.shared.*` vs `from shared.*`).

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Critical Rules

**IMPORTANT: Naming Convention**
All Factory assets MUST follow this pattern exactly:
```
GAF_<product>_<Capability>_(Tool|Agent)_v<N>
```

Components:
- `GAF_` - Required prefix (GenAI Agent Factory)
- `<product>` - Product area (e.g., GenAI, SyteLine, IDP)
- `<Capability>` - What it does in PascalCase (e.g., ListAssets, CreateTool)
- `Tool` or `Agent` - Asset type
- `v<N>` - Version number (v1, v2, etc.)

Examples:
- GAF_GenAI_ListAssets_Tool_v1
- GAF_GenAI_AgentFactory_Agent_v1
- GAF_SyteLine_InventoryLookup_Tool_v1

**YOU MUST validate naming before creating any asset.**

---

**IMPORTANT: Asset Types**
- Tools -> type: `"API_DOCS"` (ONLY this type for CRUD operations)
- Agents -> type: `"TOOLKIT"` (ONLY this type for agent orchestration)

**NEVER use:** `"SCRIPT"`, `"API"`, `"DOCUMENT_RETRIEVER"`, `"OPENAPI_SCHEMA"`

**WHY:** Infor OS GenAI platform requirements. Other types fail or behave incorrectly.

---

**IMPORTANT: Portability**
Specs MUST NOT contain:
- Hardcoded tenant URLs (use relative `servicePath`)
- Environment identifiers (no "DEV", "PROD", tenant names)
- Absolute paths

Use `servicePath: "GENAI/coresvc"` not `servicePath: "https://mingle.../GENAI/coresvc"`

---

**IMPORTANT: Two-Step Workflow**
When creating assets via Factory Agent:
1. DRAFT is shown first - user reviews the spec
2. `CONFIRM PUBLISH` (exact phrase, case-insensitive) triggers actual creation
3. Without CONFIRM, nothing is published (safe default)

This is the RECOMMENDED pattern. Direct publish via CLI scripts (publish_tool.py, publish_agent.py) is allowed for trusted users who validate manually.

## Common Patterns

### Creating a New Tool
1. Write JSON or YAML spec following naming convention
2. Set type to "API_DOCS"
3. Include servicePath (relative), api_docs, headers, responseInstructions
4. Validate: `python -m src.cli.validate_spec specs/tools/YourTool.json`
5. Run: `python -m src.cli.publish_tool specs/tools/YourTool.json`

### Creating a New Agent
1. Write JSON spec following naming convention
2. Set type to "TOOLKIT"
3. Include data.tools array with tool names/GUIDs to orchestrate
4. Include data.workflow with operational instructions
5. Run: `python -m src.cli.publish_agent specs/agents/YourAgent.json`

### Updating an Existing Asset
1. Get current spec: `python -m src.cli.list_assets --prefix <name>`
2. Add "guid" field to spec with the asset's GUID
3. Make changes (full replacement - include all fields)
4. Run: `python -m src.cli.update_asset specs/tools/YourTool.json`

### Version Bumps
- **Bug fixes, clarifications:** Update in place (same _v1)
- **Breaking changes:** Create new version (_v2)
- Breaking = input schema changes, behavior changes, type changes

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Missing `GAF_` prefix | Validation rejects | Add `GAF_` to name |
| Wrong type for tools | API returns 500 | Use `"API_DOCS"` |
| Wrong type for agents | Won't orchestrate tools | Use `"TOOLKIT"` |
| Hardcoded tenant URL | Won't work in other environments | Use relative servicePath |
| Missing GUID for update | Creates duplicate instead | Add "guid" field from existing asset |
| Instructions too long | API rejects >900 chars | Move details to data.workflow |
| Blank lines in api_docs | Validation fails | Remove empty lines from data.api_docs |
| Auth docs in api_docs | Platform handles auth | Remove all Authentication/Bearer token mentions |
| Missing Example Request | Validation fails | Add "Example Request:" section to api_docs |
| Missing debug template | Validation fails | Add debug statement to responseInstructions |
| Type-name mismatch | Validation fails | Name ending in `_Tool_v*` must have type `API_DOCS`, `_Agent_v*` must have type `TOOLKIT` |
| Agent missing tools | Validation fails | Add `data.tools` array with at least one tool |
| Agent missing workflow | Validation fails | Add `data.workflow` with operational instructions |

## Validation by Asset Type

The validator applies type-specific checks:

| Validation | Tools (API_DOCS) | Agents (TOOLKIT) |
|------------|------------------|------------------|
| Required fields (name, instructions, type, data) | Yes | Yes |
| Naming convention (GAF_*_Tool/Agent_v*) | Yes | Yes |
| Type-name consistency | Yes | Yes |
| Portability (no hardcoded URLs) | Yes | Yes |
| `data.api_docs` required | Yes | No |
| `data.api_docs` whitespace | Yes | No |
| `data.api_docs` no auth docs | Yes | No |
| `data.api_docs` Example Request | Yes | No |
| `data.responseInstructions` required | Yes | No |
| `data.responseInstructions` debug template | Yes | No |
| `data.tools` array required | No | Yes |
| `data.workflow` required | No | Yes |

## Adding New Factory Tools

Step-by-step guide:

1. **Create spec file:** `specs/tools/GAF_<product>_<Capability>_Tool_v1.json`

2. **Required fields:**
   ```json
   {
     "name": "GAF_<product>_<Capability>_Tool_v1",
     "description": "Brief description",
     "type": "API_DOCS",
     "instructions": "Short instructions (<200 chars)",
     "inputs": [],
     "data": {
       "servicePath": "GENAI/coresvc",
       "api_docs": "Method: GET\nEndpoint: /api/v1/...\nExample Request:\nGET /api/v1/...",
       "headers": {},
       "responseInstructions": "How to parse response\n\nCRITICAL - IF ERROR OCCURS INCLUDE THE BELOW IN RESPONSE:\n---DEBUG---\nFULL_URL: [The complete URL that was called]\nFULL_PAYLOAD: [The exact request body sent (JSON format)]\nFULL_RESPONSE: [The complete API response received]\n---END DEBUG---",
       "returnDirect": false,
       "model": {
         "model": "CLAUDE",
         "version": "claude-3-7-sonnet-20250219-v1:0"
       }
     },
     "status": 1,
     "utterances": []
   }
   ```

3. **Validate locally:** `python -m src.cli.validate_spec specs/tools/YourTool.json`

4. **Publish:** `python -m src.cli.publish_tool specs/tools/YourTool.json`

5. **Verify:** `python -m src.cli.list_assets --prefix GAF_<product>_<Capability>`

6. **Test:** Run smoke_test.py or invoke manually

## Extensibility: Product-Specific Factories

The naming convention supports future product-specific factories:

- `GAF_SyteLine_*` - SyteLine/CSI factory tools
- `GAF_IDP_*` - Intelligent Document Processing tools
- `GAF_IDM_*` - Infor Document Management tools
- `GAF_RPA_*` - RPA automation tools
- `GAF_ION_*` - ION integration tools

Each product factory follows the same pattern:
1. Create `GAF_<product>_*_Tool_v1` specs
2. Create `GAF_<product>_*_Agent_v1` TOOLKIT to orchestrate them
3. Register tools in the agent's data.tools array

## Error Handling Patterns

### Retry Behavior
- HTTP client retries with exponential backoff (0s, 2s, 4s, 8s, 16s)
- backoff_factor=1
- Retries on 429, 500, 502, 503, 504

### Error Response Format
```python
{
  "error": "error_type",
  "message": "Human-readable description"
}
```

### Logging
- All credentials redacted (***REDACTED***)
- Set LOG_LEVEL=DEBUG for troubleshooting
- Logs to stderr, results to stdout

## Test Checklist

Before committing changes:

- [ ] Run `python scripts/smoke_test.py` - all 4 steps pass
- [ ] Verify in Infor OS GenAI UI - asset appears with correct name
- [ ] Test via invoke_agent.py - agent can use the tool
- [ ] Cleanup test assets after verification

## Key Files

| File | Purpose |
|------|---------|
| src/cli/list_assets.py | List tools/agents |
| src/cli/publish_tool.py | Publish tool from spec |
| src/cli/publish_agent.py | Publish agent from spec |
| src/cli/update_asset.py | Update existing asset |
| src/cli/invoke_agent.py | Invoke any agent via Chat API (-a flag, --async flag, defaults to Factory Agent) |
| src/cli/validate_spec.py | Validate spec before publish (JSON/YAML) |
| scripts/smoke_test.py | End-to-end verification |
| src/infor_os/genai_client.py | API client (sync + async chat, session polling) |
| src/shared/validation.py | Type-specific naming/portability/field validation |

## Async Chat Pattern

For long-running agents that exceed the 240-second `POST /chat/sync` API gateway timeout, use the async chat pattern:

```python
import uuid
from src.infor_os.genai_client import GenAIClient

client = GenAIClient()
session_id = uuid.uuid4().hex  # dashless hex format required

# Fire-and-forget submit
client.chat(prompt="...", tools=["AgentName"], session=session_id)

# Poll for response (returns (content, new_count, elapsed))
content, count, elapsed = client.poll_for_response(
    session_id=session_id,
    expected_count=1,       # after 1st submit: expect > 1 msg
    poll_interval=10,       # seconds between polls
    max_polls=60,           # max attempts
    on_poll=my_callback     # optional: fn(attempt, elapsed, count, expected)
)
```

**Key behaviors**:
- `POST /chat` returns immediately (~1-2s). Agent processes asynchronously on platform.
- Messages (User + LLM) appear simultaneously once agent finishes (~2-3 min per chunk).
- Session IDs must be dashless hex (`uuid.uuid4().hex`). Dashed UUIDs cause polling to return 0 results.
- Pagination is 1-based (`page=1`). Page 0 returns 422.
- `GET /sessions/{id}/messages` returns items newest-first. Response format may vary (list vs paginated dict) — `get_session_messages()` normalizes this.
- `poll_for_response()` catches transient HTTP errors per attempt without aborting the loop.

**CLI usage**:
```bash
python -m src.cli.invoke_agent --async "Your prompt here"
python -m src.cli.invoke_agent --async -a AgentName -i  # Interactive async
python -m src.cli.invoke_agent --async --poll-interval 15 --max-polls 30 "Prompt"
```
