# Phase Notes — CSIWorkflowGenerator

Detailed per-phase documentation moved from CLAUDE.md to reduce context size. See CLAUDE.md for current architecture, key patterns, and active gotchas.

---

## Phase 0: Project Setup + AES Discovery + Knowledge Base

**Status**: COMPLETE (2026-02-13)

### Discovery Results

**All SyteLine IDOs are writable** via the update API. Phase 3 uses Approach A (direct API-based AES configuration).

**IDO metadata query pattern**: Use `CollectionName` (NOT `IdoName`) when filtering `IdoProperties` and `IdoCollections` system IDOs.

### Core AES IDOs (3 primary)

**Events** (15 properties, table: `Event`, server: MGCore):
- Key: `EventName` [REQUIRED]
- Writable: `AccessAs`, `Description`, `IsFrameworkEvent`, `IsFrameworkIDOEvent`, `IsFrameworkIDOSuspendableEvent`, `InWorkflow`, `NoteExistsFlag`, `ReadOnlyRecord`
- Read-only: `CreateDate`, `CreatedBy`, `RecordDate`, `RowPointer`, `UpdatedBy`, `DifferentAccessAs`

**EventHandlers** (42 properties, table: `EventHandler`, server: MGCore):
- Keys: `EventName` [KEY:1], `Sequence` [KEY:2]
- Key writable fields: `Active`, `Synchronous`, `Suspend`, `Transactional`, `AppliesToInitiators`, `IDOCollections` (maps to AppliesToObjects), `Description`, `IgnoreFailure`, `Obsolete`, `Overridable`, `InitialAction`, `InitialState`, `MethodToCall`, `Purpose`, `TriggeringProperty`
- Has sub-collection: `EventActions` (Object type)
- Read-only: `AppliesToObjects`, `CreatedBy`, `RecordDate`, `RowPointer`, `UpdatedBy`

**EventActions** (31 properties, table: `EventAction`, server: MGCore):
- Keys: `EventHandlerRowPointer` [KEY:1], `EvrEventName` [KEY:2], `RowPointer` [KEY:3]
- Key writable fields: `ActionType` [REQUIRED], `Sequence` [REQUIRED], `Description`, `Parameters`, `NewSequence`
- Has sub-collection: `EventActionVariableAccess` (Object type)
- Read-only: `EventName`, `EventHandlerSequence`, `ExpandedParameters`, `SubstitutedParameters`

### Additional AES IDOs Discovered (36 total)

- **Configuration**: `EventTriggers` (23 props), `EventGlobalConstants` (11), `EventInitialStates` (11), `EventInitialVariables` (16), `EventConditionPredicate` (25)
- **Runtime/Status**: `EventStates` (30), `EventHandlerStates` (35), `EventActionStates` (21), `EventQueues` (27), `QueuedEventHandlers` (10)
- **Parameters**: `EventParameters` (16), `EventInputParameters` (16), `EventOutputParameters` (15), `EventTriggerParameters` (10)
- **Messaging**: `EventMessages` (37), `EventMessageCategories` (9), `EventMessageVariables` (25)
- **Revisions**: `EventRevisions` (9), `EventHandlerRevisions` (26), `EventActionRevisions` (14)
- **Views**: `EventNames` (3), `EventVariables` (17), `EventActionVariableAccess` (11), `EventMyWorkflowsViews` (18), `EventAttachmentsViews` (15)
- **Prompt/Voting**: `EventCurrentPromptResultsViews` (38), `EventCurrentPromptSummaryViews` (28), `EventCurrentPromptVotersViews` (36)
- **Lookup**: `IdoEventHandlerAppliesToObjects` (3), `IdoEventHandlerAppliesToTasks` (3)
- **Portal**: `SLEventMessages` (6), `SLEventStates` (9)
- **Generic**: `EventAction_GenericParms` (12)

**AES Knowledge Base**: `reference/AES_Knowledge_Base.md` -- 593KB, 12,893 lines, 16 chapters extracted from 212-page PDF.

**Note**: Empty records were created during an earlier writability test and may need cleanup in Events, EventHandlers, EventActions tables.

---

## Phase 1: ION Workflow JSON Builder

**Status**: COMPLETE (deployed and validated in live ION environment)

### Builder Module (`src/workflow_builder/`)

The builder abstracts ION workflow JSON complexity through composable Python dataclasses:

```python
from src.workflow_builder import (
    WorkflowBuilder, WorkflowVariable, WorkflowView, ViewParameter,
    DistributionItem, ActionButton, TaskParameter, Assignment, DueDate,
    usertask, assignment, ionapi_flowpart, ifthenelse, subworkflow,
    build_condition, build_ido_load, build_ido_update,
)

wf = (WorkflowBuilder("MyWorkflow", "Description")
      .add_variable(WorkflowVariable("Var1", workflow_input=True))
      .add_flowpart(usertask(...))
      .add_flowpart(assignment(...)))

workflow_json = wf.to_json()
workflow_dict = wf.build()
```

### Key Design Decisions

- **Dual encoding**: ionapi flowparts maintain both `method` (JSON string with nulls) and `ionApiMethod` (compact dict without nulls) in sync automatically.
- **Assignment sync**: Assignment flowparts maintain both `serializedAssignments` (JSON string with treePath/personFullName nulls) and `listOfAllAssignments` (compact list) in sync.
- **serviceAccount reuse**: Encrypted tokens are extracted from reference workflows rather than generated. Same tenant = same token works.
- **FlowPart types supported**: `usertask`, `assignment`, `ionapi`, `ifthenelse`, `subworkflow`, `parallel`, `wait`

### Scripts

```bash
python scripts/build_credit_approval.py          # Build + compare vs reference
python scripts/build_credit_approval.py --diff    # Detailed JSON diff
python scripts/deploy_workflow.py output/file.json --activate   # Deploy + activate
python scripts/deploy_workflow.py --delete Name                  # Delete
python scripts/deploy_workflow.py --status Name                  # Check status
python scripts/deploy_workflow.py --get Name                     # Download JSON
```

### Validation Result

Zero structural differences against `CS_Credit_Approval_API` reference across all 10 variables, 1 view, 3 top-level flowparts.

---

## Phase 2A: Workflow Template System

**Status**: COMPLETE (validated zero-diff against reference)

### Template System (`src/templates/` + `src/config/`)

Reduces workflow authoring from ~200 lines of Python to ~117 lines of JSON:

```python
from src.templates import load_spec, render
from src.config.tenant import load_default

spec = load_spec("templates/credit_approval.json")
tenant = load_default()
result = render(spec, tenant)  # -> ION workflow dict
```

### Architecture

| Module | Purpose |
|--------|---------|
| `src/config/tenant.py` | Tenant config: site, service account, user registry, distribution groups |
| `src/templates/schema.py` | Dataclasses for spec structure + `from_dict()` parser |
| `src/templates/presets.py` | Factory functions: spec step type -> Phase 1 builder calls |
| `src/templates/renderer.py` | Main pipeline: WorkflowSpec + TenantConfig -> workflow dict |

### Key Design Decisions

- **JSON spec format** (not YAML): No dependency, consistent with output format, natural for LLM generation.
- **Auto-variable creation**: Renderer scans flow steps and auto-creates internal variables (ApproveReject, Filter, UpdatePropertyValue, ItemID).
- **Auto-sequence numbering**: Position-based (1, 2, 3...) within each scope.
- **Normalized comparison**: Sort arrays by natural keys for order-independent structural comparison.
- **Presets as factory functions**: Each step type maps to Phase 1 builder functions. Zero reimplementation.

### Validation Result

Zero structural differences — 10 variables (6 explicit + 4 auto-created), 1 view, 3 flowparts match reference exactly.

---

## Phase 2B: Advanced Workflow Patterns (Customer Order Discount)

**Status**: COMPLETE (validated zero-diff against reference)

### What Phase 2B Added

Three new step types completing all ION workflow flowpart types:

| Step Type | Description | Renders to |
|-----------|-------------|------------|
| `parallel` | Multiple branch lists with join type | `parallel()` with `sequentialFlows` |
| `wait` | Timer flowpart | `wait()` |
| `condition` | Generic if/then/else with arbitrary branches | `ifthenelse()` with recursive render |

### Additional Capabilities

- **Variable-bound IDO parameters**: `ido_var` / `properties_var` for dynamic IDO configuration
- **Tree definitions**: Hierarchical data display in Pulse task forms
- **Per-user send_email**: Distribution groups support per-user email settings via `UserEntry.send_email`
- **ionapi description**: Optional description parameter for API call descriptions

### Bug Fixes

- `flowparts.py`: Fixed `parallel()` to use `"sequentialFlows"` instead of `"branches"`
- `ionapi.py`: Made `inputBody` nullable in `_build_ionapi_method()`

### Validation Result

Both templates zero-diff: Credit Approval (10 vars, 1 view, 3 flowparts) + Customer Order Discount (12 vars, 1 view, 1 tree, 5 flowparts).

---

## Phase 3A: AES Configuration Builder (Discovery + Builder Module)

**Status**: COMPLETE

### AES Builder Module (`src/aes_builder/`)

```python
from src.aes_builder import AESBuilder, EventHandler, EventAction
from src.aes_builder import condition, property_modified, prop, var
from src.aes_builder import call_workflow_params, set_variable_params

builder = AESBuilder()
handler = builder.load_handler_with_actions("IdoOnItemUpdate", "%CreditLimit%")
ref = builder.export_handler(handler)  # -> JSON-serializable dict
```

### Architecture

| Module | Purpose |
|--------|---------|
| `src/aes_builder/models.py` | `EventHandler` + `EventAction` dataclasses with IDO serialization |
| `src/aes_builder/expressions.py` | Factory functions for AES parameter/expression strings |
| `src/aes_builder/builder.py` | `AESBuilder` class: query, create, delete via IDO API |

### Models (`models.py`)

**EventHandler** — maps to `EventHandlers` IDO:
- Fields: `event_name`, `sequence`, `description`, `ido_collections`, `synchronous`, `suspend`, `active`, `transactional`, `ignore_failure`, `overridable`, `triggering_property`, `applies_to_initiators`, `access_as`, `actions`, `row_pointer`
- `to_insert_properties()`, `from_ido_record()`, `to_dict()` serialization methods
- Booleans serialized as `"1"`/`"0"` strings (SyteLine convention)

**EventAction** — maps to `EventActions` IDO:
- Fields: `sequence`, `action_type`, `parameters`, `description`, `row_pointer`, `event_handler_row_pointer`, `event_name`
- `event_handler_row_pointer` links to parent (set during creation)

### Expression Builders (`expressions.py`)

**Base expressions**: `condition`, `not_condition`, `property_modified`, `prop`, `var`, `event_param`, `result_expr`, `return_var`, `substitute`, `round_expr`, `configname`, `username`, `curdatetime`

**Compound patterns**: `finish_unless_modified`, `finish_with_result`, `fail_if_rejected`

**Parameter line builders**: `setvarvalues_params`, `setpropvalues_params`, `load_collection_params`, `invoke_method_params`, `call_workflow_params`, `notify_params`, `build_ion_workflow_start_params`

### AESBuilder (`builder.py`)

- **Query**: `load_handlers()`, `load_actions()`, `load_handler_with_actions()`, `export_handler()`
- **Create**: `create(handler)` — two-step: insert handler -> extract RowPointer -> insert actions
- **Delete**: `delete_handler(event_name, sequence)` — delete actions first, then handler
- **Update**: `set_handler_active(event_name, sequence, active)` — toggle Active flag

### Action Type Codes

| Code | Constant | Name |
|------|----------|------|
| `1` | `ACTION_NOTIFY` | Notify |
| `10` | `ACTION_FINISH` | Finish |
| `12` | `ACTION_SET_VALUES` | SetValues |
| `14` | `ACTION_LOAD_COLLECTION` | LoadCollection |
| `21` | `ACTION_INVOKE_METHOD` | InvokeMethod |
| `29` | `ACTION_SEND_BOD` | SendBOD |

### ION Workflow Trigger Pattern

Does NOT use native `CallWorkflow`. Instead uses:
1. `SetValues` (type 12) with `SETVARVALUES()` to build a JSON payload
2. `InvokeMethod` (type 21) calling `IONAPIMethods.InvokeIONAPIMethod2` which POSTs to `/process/application/v1/workflow/start`

### The 7-Action Handler Pattern

1. Action 10: Finish — skip if monitored field not modified
2. Action 20: LoadCollection — get old field value via IDO query
3. Action 25: SetValues — build ION workflow start JSON payload
4. Action 30: InvokeMethod — call ION API to start workflow
5. Action 35: Notify — debug email with parameters (optional)
6. Action 40: SetValues — set InWorkflow=1 AND rollback field to old value
7. Action 50: InvokeMethod — log note in SLObjectNotes

### Scripts

```bash
python scripts/query_aes.py                           # List IdoOnItemUpdate handlers
python scripts/query_aes.py --handler ue_CreditLimit   # Search by description
python scripts/query_aes.py --handler ue_CreditLimit --export  # Export to reference/
python scripts/query_aes.py --ido SLCustomers          # Filter by IDO
python scripts/query_aes.py --all                      # All events
```

---

## Phase 3B: AES Deployment + End-to-End Validation

**Status**: COMPLETE (deployed and validated end-to-end in live SyteLine environment)

### What Phase 3B Added

Build script (`scripts/build_credit_handler.py`) reconstructing the 7-action credit limit handler from code.

### Bug Fixes

- `expressions.py`: Fixed `notify_params()` to use `\n` separators
- `expressions.py`: Added trailing `\n` to `build_ion_workflow_start_params()`

### Deploy Safety

- `--deploy`: Deactivates original handler first, creates clone. If creation fails, reactivates original.
- `--delete`: Deactivates clone and reactivates original.
- IDO `Action=3` deletes return success but don't remove EventHandler records — use deactivation instead.
- Verifies actual stored sequence post-creation (system may auto-assign).

### Scripts

```bash
python scripts/build_credit_handler.py              # Build + compare vs reference
python scripts/build_credit_handler.py --diff       # Detailed diff
python scripts/build_credit_handler.py --deploy     # Deploy (deactivates old handler)
python scripts/build_credit_handler.py --delete     # Delete + reactivate old
```

### Deployment Validation (2026-02-14)

Successfully deployed `ue_CreditLimitWorkflow_Clone` (seq=200) — AES fires on Credit Limit change, ION workflow starts, Pulse approval appears, credit limit rolled back, InWorkflow=1 set, approval completes cycle.

---

## Phase 4: Natural Language Parser

**Status**: COMPLETE (live validated 2026-02-14)

### Parser Module (`src/parser/`)

| Module | Purpose |
|--------|---------|
| `src/parser/validator.py` | `SpecValidator`: 3-level validation (structural, referential, live IDO) |
| `src/parser/user_resolver.py` | Distribution group resolution against tenant config |
| `src/parser/ido_metadata.py` | `IdoMetadataClient`: live SyteLine IDO/property validation |

### IdoMetadataClient

```python
from src.parser.ido_metadata import IdoMetadataClient

client = IdoMetadataClient()
client.ido_exists("SLCustomers")
client.get_properties("SLCustomers")
client.property_exists("SLCustomers", "CreditLimit")
client.find_case_match("SLCustomers", "creditlimit")
client.suggest_ido("SLCustomer")
client.suggest_property("SLCustomers", "CreditLim")
```

### Validator Levels

| Level | Checks | Network Required |
|-------|--------|-----------------|
| 1 — Structural | Required fields, valid enums, IDO reference completeness | No |
| 2 — Referential | Variable/view/tree cross-references, distribution groups | No (tenant config) |
| 3 — Live | IDO existence, property existence, case matching | Yes (SyteLine API) |

### Scripts

```bash
python scripts/validate_spec.py templates/credit_approval.json --tenant  # Structural + referential
python scripts/validate_spec.py templates/credit_approval.json --live    # + live IDO checks
python scripts/generate_workflow.py templates/spec.json --live --diff ref.json  # Full pipeline
python scripts/generate_workflow.py templates/spec.json --validate-only --live  # Validate only
```

### Slash Command: `/parse-workflow`

NL-to-spec parsing at `.claude/commands/parse-workflow.md`. Provides structured 6-step workflow, complete field reference for all 10 step types, valid enums, and pattern templates.

---

## Phase 5: End-to-End Orchestrator CLI

**Status**: COMPLETE (awaiting live deployment validation)

### Deliverables

1. **D1 — Schema Extension** (`schema.py`): `AesTriggerSpec` dataclass, wired into `WorkflowSpec`
2. **D2 — Spec Handler Generator** (`spec_handler.py`): `build_handler_from_spec(spec, logical_id)` generates 7-action pattern
3. **D3 — Validator Extension** (`validator.py`): AES trigger validation at all 3 levels
4. **D4 — Unified CLI** (`wfgen.py`): 6 subcommands — create, render, validate, aes, status, delete
5. **D5 — Slash Command Update**: Added `aes_trigger` field reference to `/parse-workflow`
6. **D6 — Template Updates**: Added `aes_trigger` to credit_approval.json and order_line_discount_approval.json

### Unified CLI Usage

```bash
python scripts/wfgen.py create templates/spec.json --live --activate   # Full pipeline
python scripts/wfgen.py render templates/spec.json --diff ref.json     # Render + diff
python scripts/wfgen.py validate templates/spec.json --live            # Validate only
python scripts/wfgen.py aes templates/spec.json --deploy --diff ref    # AES handler only
python scripts/wfgen.py status WorkflowName                            # Check status
python scripts/wfgen.py delete WorkflowName                            # Delete both
```

### AES Trigger Spec Format

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
    "notify_email": "user@example.com",
    "notes_ido": "SLObjectNotes",
    "notes_object_type": "customer"
  }
}
```

**`workflow_inputs` value syntax**: Plain property name → auto-wrapped as `P("name")`. AES expression → used as-is.
