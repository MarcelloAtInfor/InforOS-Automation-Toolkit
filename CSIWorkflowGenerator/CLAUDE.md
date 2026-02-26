# CLAUDE.md — CSIWorkflowGenerator

## Project Overview

CSIWorkflowGenerator automates CSI (CloudSuite Industrial) workflow creation by generating both **AES event handler configurations** and **ION workflow JSON** from compact spec JSON (~100 lines -> 600+ line deployable output).

**Goal 1** (current): Claude Code + local Python scripts create complete workflows.
**Goal 2** (future): Port tooling to Infor GenAI platform as agents/tools.

## Architecture

```
CSIWorkflowGenerator/
  CLAUDE.md                     # This file — project documentation
  log.md                        # Session log / running history
  plan.md                       # Full project plan (Phases 0-8)
  reference/
    AES_Knowledge_Base.md       # Structured AES reference (593KB, 16 chapters from PDF)
    PHASE_NOTES.md              # Detailed per-phase documentation (moved from CLAUDE.md)
    CS_Credit_Approval_API.json # Reference ION workflow (simple approval)
    CustomerOrderDiscountWorkflow.json  # Reference ION workflow (advanced patterns)
    AES_ue_CreditLimitWorkflow_API.json # Reference AES handler (7-action pattern)
  templates/
    credit_approval.json        # Credit Approval spec (with aes_trigger)
    order_discount.json         # Order Discount spec (parallel timeout pattern)
    order_line_discount_approval.json  # Order Line Discount spec (with aes_trigger)
    credit_hold_notification.json      # Credit Hold notification-only spec (Phase 6A)
  scripts/
    wfgen.py                    # Unified CLI: create/render/validate/aes/status/delete
    render_template.py          # Render spec JSON -> ION workflow JSON (with --diff, --deploy)
    validate_spec.py            # Validate spec JSON (structural, referential, tenant, live)
    generate_workflow.py        # Full pipeline: validate + render + deploy
    deploy_workflow.py          # Create/activate/delete workflows via ION API
    query_aes.py                # Discover/export existing AES handlers via IDO API
    build_credit_approval.py    # Reconstruct Credit Approval workflow (validation)
    build_credit_handler.py     # Reconstruct AES credit limit handler (validation)
    extract_aes_guide.py        # PyMuPDF PDF -> markdown knowledge base (one-shot)
  src/
    http_client.py              # Resilient HTTP: timeout, retry, Infor error parsing
    config/tenant.py            # Tenant config: site, service account, user registry
    aes_builder/
      models.py                 # EventHandler, EventAction dataclasses (IDO mapping)
      expressions.py            # AES expression/parameter string builders
      builder.py                # AESBuilder: query, create, delete handlers via IDO API
      spec_handler.py           # Generate handler from spec's aes_trigger section
    workflow_builder/
      models.py                 # Dataclasses for workflow components
      builder.py                # WorkflowBuilder: assembles components -> JSON
      flowparts.py              # Factory functions for each flowpart type
      conditions.py             # XML condition string builder
      ionapi.py                 # ION API call builder (IDO load/update)
    parser/
      validator.py              # SpecValidator: 3-level validation (structural, referential, live)
      user_resolver.py          # Validate distribution user keys against tenant config
      ido_metadata.py           # IdoMetadataClient: live IDO/property validation
    templates/
      schema.py                 # Dataclasses for spec structure + AesTriggerSpec
      presets.py                # Factory functions: spec step -> flowpart dict
      renderer.py               # Main pipeline: WorkflowSpec -> WorkflowBuilder -> JSON
  .claude/commands/
    parse-workflow.md           # NL-to-spec parsing slash command
  output/                       # Generated workflow JSON files
```

## Shared Infrastructure

| Asset | Import | Purpose |
|-------|--------|---------|
| `shared/auth.py` | `from shared.auth import get_auth_headers` | OAuth 2.0 tokens with auto-cache |
| `shared/config.py` | `from shared.config import get_base_url, IDO_URL` | Service URL construction |
| `shared/tenant.py` | `from shared.tenant import get_site, get_logical_id` | Tenant config (site, logical ID, users) |

**Path setup** for scripts in `scripts/`:
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # repo root (for shared/)
sys.path.insert(0, str(Path(__file__).parent.parent))          # project root (for src/)
```

**SyteLine site config**: Loaded from `tenant_config.json` via `shared.tenant.get_site()` (set via `X-Infor-MongooseConfig` header). Run `python setup.py` to configure.

## Unified CLI (`wfgen.py`)

The primary entry point for all workflow operations:

```bash
# Full pipeline: validate + render + deploy ION workflow + create AES handler
python scripts/wfgen.py create templates/spec.json --live --activate
python scripts/wfgen.py create templates/spec.json --update --activate  # delete+recreate on 409

# Render only (no deploy)
python scripts/wfgen.py render templates/spec.json
python scripts/wfgen.py render templates/spec.json --diff reference/ref.json

# Validate only
python scripts/wfgen.py validate templates/spec.json --live

# AES handler only (from spec)
python scripts/wfgen.py aes templates/spec.json --deploy --diff reference/ref.json

# Check workflow status
python scripts/wfgen.py status WorkflowName

# Delete both ION workflow and AES handler
python scripts/wfgen.py delete WorkflowName
```

## Spec Step Types

| Type | Description | Renders to |
|------|-------------|------------|
| `approval_task` | User task with action buttons | `usertask()` with USER_TASK type |
| `notification` | Notification task (no buttons) | `usertask()` with NOTIFICATION type |
| `assignment` | Variable assignment(s) | `assignment()` |
| `ido_branch` | Condition + two variable assignments | `ifthenelse()` wrapping `assignment()` |
| `ido_load` | IDO GET query | `ionapi_flowpart(build_ido_load())` |
| `ido_update` | IDO POST update | `ionapi_flowpart(build_ido_update())` |
| `subworkflow` | Container for child steps | `subworkflow()` with recursive render |
| `parallel` | Multiple branch lists with join type | `parallel()` with `sequentialFlows` |
| `wait` | Timer flowpart | `wait()` |
| `condition` | Generic if/then/else | `ifthenelse()` with recursive render |

## AES Trigger Spec Format

Specs can declare an `aes_trigger` section to auto-generate the 7-action ION API handler:

```json
{
  "aes_trigger": {
    "event": "IdoOnItemUpdate",
    "ido": "SLCustomers",
    "monitored_field": "CreditLimit",
    "workflow_inputs": {
      "CustName": "Name",
      "MGConfig": "CONFIGNAME()",
      "OldCreditLimit": "ROUND(E(OldCreditLimit), 2)"
    },
    "applies_to_initiators": "Form.Customers",
    "handler_sequence": 200,
    "notes_ido": "SLObjectNotes",
    "notes_object_type": "customer"
  }
}
```

**`workflow_inputs` value syntax**: Plain property name (`"CustNum"`) -> auto-wrapped as `P("CustNum")`. AES expression (`"CONFIGNAME()"`) -> used as-is.

## IDO Query Patterns

```python
# Load records
url = f"{IDO_URL()}/load/{ido_name}"
params = {"properties": "Field1,Field2", "filter": "FieldName = 'value'", "recordCap": 100}
resp = requests.get(url, headers=headers, params=params)
items = resp.json().get("Items", [])

# Insert/Update records
url = f"{IDO_URL()}/update/{ido_name}"
payload = {
    "IDOName": ido_name,
    "RefreshAfterSave": True,
    "Changes": [{"Action": 1, "Properties": [{"Name": "Field", "Value": "val", "Modified": True, "IsNull": False}]}]
}
resp = requests.post(url, headers=headers, json=payload)
```

## Critical Gotchas

### AES Handler Deployment

1. **`AppliesToInitiators` prevents infinite loops** — ALWAYS set to the originating form name (e.g., `"Form.Customers"`). Without this, the handler fires on API/IDO updates too, and the ION workflow's write-back creates an infinite AES->ION->AES loop. Use the form-to-IDO lookup API to resolve form names (see IDO API Quirks #6).

2. **`AccessAs` should be `"ue_"`** — places handler in user-extension namespace so it's visible in the AES config UI.

3. **Handler uses synchronous=true, suspend=false** — opposite of what you'd expect. InWorkflow flag is managed explicitly via `SETPROPVALUES("InWorkflow" = "1")`.

4. **ION trigger uses InvokeMethod, not CallWorkflow** — SetValues builds a JSON payload, then InvokeMethod calls `IONAPIMethods.InvokeIONAPIMethod2` to POST to `/process/application/v1/workflow/start`.

5. **`notify_email` is a debug artifact** — The reference handler's action 35 (type=1 Notify) that emails workflow params was for debugging only. Do NOT include it in production handlers. The `notify_email` field in `aes_trigger` specs is optional and should generally be omitted.

6. **Standard handler pattern is 5 or 6 actions** — Guard (10), Load old value (20), Set API params (25), Invoke ION API (30), Lock record + revert (40), and optionally Log to notes (50). Action 35 (debug notify) is NOT standard.

### ION Workflow Quirks

1. **DECIMAL/INTEGER variables need numeric initial values** — ION rejects empty string `''` for non-STRING types. Auto-created variables must set `initialValue` to `"0"` for DECIMAL/INTEGER, `"false"` for BOOLEAN.

2. **Duplicate workflow returns 400, not 409** — Creating a workflow that already exists returns `400 Bad Request` with `"workflow already exists with the same name"` (not 409 Conflict). The `--update` flag handles both.

3. **Compound condition XML (`BooleanCombination`) rejected by ION** — Our `build_compound_condition()` generates XML that ION's activation validator cannot parse. Error: `Cannot invoke "Condition.getUsedSubcondition()" because "cond" is null`. Simple conditions (`AttributeValueComparison`) work. Needs investigation: download a working compound condition from ION Desk UI to compare XML format.

4. **Notification messages cannot reference parallel branch button variables** — Variables set by `button_variable` in parallel branches (e.g. `PurchasingResult`) cause activation error: `PARAMETER_X0_CANNOT_BE_USED_IN_THE_SUMMARY_NOTIFICATION_MESSAGE`. Workaround: show them as task params instead of in `[VarName]` message text.

### IDO API Quirks

1. **Insert responses don't include RowPointer** — EventHandlers/EventActions inserts return `{"Success": true, "RefreshItems": null}`. Workaround: query by description after insert.

2. **Delete (Action=3) silently fails on EventHandlers AND EventActions** — returns success but records persist. The SyteLine UI uses a confirmation popup for deletion, suggesting a custom stored procedure or IDO method is required. Research needed. The `--update` flag on `wfgen create` skips AES handler recreation if it already exists.

3. **Sequence numbers 1-124 occupied** on `IdoOnItemUpdate` — use seq >= 200 for custom handlers.

4. **IDO metadata filter field is `CollectionName`** (NOT `IdoName`) when querying `IdoProperties` and `IdoCollections`. Also, the data type field is `DataType` (NOT `PropertyDataType`).

5. **EventActions update requires `_ItemId`** — load the record first to get `_ItemId`, then include it in the update payload. Also requires `EventHandlerRowPointer` and `EvrEventName` as key properties.

6. **Form-to-IDO lookup API** — Resolve a form name to its primary IDO:
   ```
   POST {IDO_URL}/invoke/WBDataViews?method=GetFormPrimaryCollection
   Body: ["FormName", "", ""]
   Response: {"Parameters": ["FormName", "SLItems", ""], "Success": true}
   ```
   Use this to resolve `AppliesToInitiators` form names programmatically.

7. **Handler resequencing SP** — After inserting handlers, call `ReorderNewEventHandlersSp` to auto-assign sequences:

8. **SLPoItems property names** — `VendNum` does NOT exist on SLPoItems. Use `PoVendNum` instead. `Description` is correct for item description (PropertyType 0, on primary `poitem` table).
   ```
   POST {IDO_URL}/invoke/EventHandlers?method=ReorderNewEventHandlersSp
   Body: ["EventName"]
   ```

### IDO Property Types (CRITICAL for AES triggers)

**Only use PropertyType 0 or 1 as `monitored_field` in AES triggers.**

| PropertyType | Name | Can trigger AES? | Example |
|--------------|------|-----------------|---------|
| 0 | BoundToColumn | YES — real database column | `CreditLimit`, `Stat`, `VendNum` |
| 1 | Derived | YES — calculated from bound columns | `DerCustName`, `DerStatFormatted` |
| 2 | Unbound | NO — temporary form variable, not persisted | `Amount`, `AmtTot` |
| 3 | SubCollection | NO — child collection reference | `SLCoitems`, `SLPoItems` |

**To check PropertyType**: Query `IdoProperties` with `CollectionName = '{ido}'` and include `PropertyType` in properties list.

### AES Expression Context

- **`V(var)`** — handler variable (use in notify BODY, SUBJECT, etc.)
- **`RV(var)`** — method return value (use ONLY within the same InvokeMethod/LoadCollection action)
- **`E(param)`** — event parameter (use in any action)
- Do NOT use `RV()` in notify actions — use `V()` instead.

### IFS User API

- **Endpoint**: `{base}/ifsservice/usermgt/v2/users/search/identity2byemail`
- **Method**: POST `{"email": "user@example.com"}` → returns `{"response": {"userlist": [{"id": "ifs-guid"}]}}`
- **Batch**: `identity2byemaillist` with `{"emails": [...]}`
- **Swagger**: `IFSService.json` — service proxy name is `ifsservice`

### Workflow Builder

- **Dual encoding**: ionapi flowparts maintain both `method` (JSON string with nulls) and `ionApiMethod` (compact dict) in sync.
- **serviceAccount reuse**: Encrypted tokens extracted from reference workflows. Same tenant = same token.
- **Variable-bound IDO params**: `ido_var`/`properties_var` enable dynamic IDO configuration at runtime.
- **Distribution uses named user keys** — spec `distribution` field takes individual user keys from tenant config (e.g. `"user1"` or `["user1", "user2"]`). No group abstraction exists yet; IFS group support is a future phase.

## AES Expression Syntax Quick Reference

`V(var)`, `P(property)`, `E(param)`, `PROPERTYMODIFIED("field")`, `CONDITION(expr)`, `SUBSTITUTE("text {0}", P("field"))`, `VOTINGRESULT(seq)`, `IF(bool, true, false)`, `CONFIGNAME()`, `USERNAME()`, `CURDATETIME()`, `ROUND(val, dec)`

## Parent Project Slash Commands & Agents

The parent project (`CC_OS_Project/.claude/`) provides reusable commands:

| Command | Purpose |
|---------|---------|
| `/query-ido` | Query records from a SyteLine IDO collection |
| `/ido-lookup` | Discover available properties for an IDO |
| `/ido-update` | Create, update, or delete IDO records |
| `/infor-auth` | Generate or refresh an OAuth 2.0 token |
| `/deploy-genai-asset` | Deploy a GenAI tool or agent definition |
| `/list-genai-assets` | List deployed GenAI assets |
| `/send-pulse` | Send ION Pulse alerts/notifications |
| `/rpa-snippet` | Generate XAML snippets for RPA Studio |

**When to use what**:
- **IDO metadata discovery**: `/query-ido` + `/ido-lookup`
- **Ad-hoc IDO queries**: `/query-ido`
- **AES handler queries**: `query_aes.py` (AES-specific formatting)
- **Workflow deployment**: `wfgen.py` or `deploy_workflow.py`

## Reference Files

| File | Content |
|------|---------|
| `reference/CS_Credit_Approval_API.json` | Simple approval: AES -> UserTask -> IDO write-back |
| `reference/CustomerOrderDiscountWorkflow.json` | Advanced: parallel flows, decision trees, timeouts |
| `reference/AES_ue_CreditLimitWorkflow_API.json` | 7-action ION API handler pattern |
| `reference/AES_Knowledge_Base.md` | Full AES guide (593KB, 16 chapters) |
| `reference/PHASE_NOTES.md` | Detailed per-phase documentation |

## Phase Status

| Phase | Goal | Status |
|-------|------|--------|
| 0 | Project Setup + AES Discovery + Knowledge Base | COMPLETE |
| 1 | ION Workflow JSON Builder | COMPLETE |
| 2A | Workflow Template System (Core) | COMPLETE |
| 2B | Advanced Patterns (Parallel, Wait, Condition) | COMPLETE |
| 3A | AES Configuration Builder | COMPLETE |
| 3B | AES Deployment + End-to-End | COMPLETE (deployed + validated) |
| 4 | Natural Language Parser | COMPLETE (live validated) |
| 5 | End-to-End Orchestrator CLI | COMPLETE (live validated) |
| 6A | Notification-Only Pattern | COMPLETE (live validated) |
| 6B-C | Multi-Level, Parallel ALL_IN | COMPLETE (live validated) |
| 6D | Compound Conditions | BLOCKED — BooleanCombination XML rejected by ION |
| 6E | HTTP Robustness Hardening | COMPLETE (live validated) |
| 7 | GenAI Platform Tools (Goal 2) | Not started |
| 8 | GenAI Platform Agent (Goal 2) | Not started |
