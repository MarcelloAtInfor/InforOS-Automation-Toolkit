# CSIWorkflowGenerator - Project Plan

## Context

CSI (CloudSuite Industrial) workflows require coordinating two systems: **AES** (Application Event System) in the ERP for triggers, and **ION** workflows in Infor OS for approval routing and write-back. Today, building a single workflow requires manually configuring AES event handlers (events, handlers, actions, conditions) in SyteLine AND creating ION workflow JSON (variables, flowparts, ionapi calls, conditions) -- a tedious, error-prone process.

This project automates that end-to-end: describe a workflow in natural language, and the tooling generates both the AES configuration and ION workflow definition, deploys them, and validates the result.

**Goal 1** (first): Claude Code + local Python scripts create complete workflows.
**Goal 2** (later): Port tooling to Infor GenAI platform as agents/tools for others.

---

## Existing Infrastructure to Reuse

| Asset | Path | Purpose |
|-------|------|---------|
| Auth module | `shared/auth.py` | OAuth 2.0 tokens with auto-cache |
| Config module | `shared/config.py` | Service URL construction |
| ION workflow scripts | `CSIPOAssetCreationTool/ION/scripts/create_workflow.py` | Create/activate/delete workflows |
| ION start script | `CSIPOAssetCreationTool/ION/scripts/start_workflow.py` | Start workflow instances |
| Credit Approval ref | `CSIPOAssetCreationTool/ION/workflow_definitions/CS_Credit_Approval_API.json` | Working workflow to clone |
| Discount Approval ref | `CSIPOAssetCreationTool/ION/workflow_definitions/CustomerOrderDiscountWorkflow.json` | Advanced patterns (trees, parallel, timeout) |
| GAF_CLI | `GAF_CLI/` | GenAI tool/agent publishing |
| AES Guide PDF | `08_ARCHIVE/Legacy-Systems/Mongoose/Documents/AES_Guide.pdf` | 212-page AES reference |

---

## Phase 0: Project Setup + AES Discovery + Knowledge Base

**Goal**: Scaffold the project, extract the AES Guide into a searchable knowledge base, discover AES-related IDOs in SyteLine, and document findings.

### Why This Phase First
AES is the biggest knowledge gap. The 212-page AES guide contains critical domain knowledge (event types, action types, expression syntax, suspension mechanics, InWorkflow pattern) that must be extracted into a structured reference before we can build tooling. We also need to discover whether AES configuration is exposed via IDO API.

### Key AES Findings (from PDF analysis)

**Architecture**: Events -> Event Handlers -> Event Actions -> Event Action Parameters

**Framework Events for Workflow Triggers**:
- `IdoOnItemUpdate` / `IdoOnItemInsert` / `IdoOnItemDelete` -- the main ones for field-change triggers
- Only these three can be **suspended** (pausing execution to await approval)
- Suspension sets `InWorkflow=1` on the record, preventing re-triggers

**Event Handler Config Fields**: Event Name, Applies to Objects (IDO name), Applies to Initiators, Handler Sequence, Synchronous, Suspend, Active, Transactional, Initial State, Initial Action

**Action Types**: Prompt (approval), Notify, Fail, Finish, Set Values, Branch, Goto, Generate Event, Call Database Method, Call IDO Method, Dispatch IDO Request, Execute IDO Request, Load Collection, Load IDO Row, Update Collection, Call Web Service, Wait, Sleep

**Expression Syntax**: `V(var)`, `GC(const)`, `E(param)`, `P(property)`, `PROPERTYMODIFIED("field")`, `CONDITION(expr)`, `SUBSTITUTE("text {0}", P("field"))`, `VOTINGRESULT(actionSeq)`, `IF(bool, trueExpr, falseExpr)`, `DBFUNCTION("funcName", args)`

**Expression Operators**: `=`, `!=`/`<>`, `>`, `<`, `>=`, `<=`, `AND`, `OR`, `NOT`, `+` (add/concat), `-`, `*`, `/`, `LIKE`, `IN`/`:`, `!:`

**Suspension Mechanics (Critical for Approval Workflows)**:
- Two stages: suspend-validating (in transaction, rolled back) and suspend-committing (actual execution)
- On suspend: `InWorkflow` property set to 1 on the record
- On success: standard processing committed + InWorkflow cleared
- On failure: standard processing prevented + InWorkflow cleared

**Design Forms**: Events, Event Triggers, Event Handlers, Event Actions, Event Handler Diagram, Event Handler Sequence, Event Variable Groups, Event Global Constants

### Deliverables

```
CSIWorkflowGenerator/
  CLAUDE.md                              # Project documentation
  log.md                                 # Session log
  reference/
    AES_Knowledge_Base.md                # Extracted from 212-page PDF (structured)
    CS_Credit_Approval_API.json          # Copy of reference workflow
    CustomerOrderDiscountWorkflow.json   # Copy of reference workflow
  scripts/
    extract_aes_guide.py                 # Parse PDF -> markdown knowledge base
    discover_aes_idos.py                 # Query SyteLine for AES IDO names/properties
```

### `discover_aes_idos.py` Logic
Query SyteLine `IdoCollections` for Event-related IDOs:
- Search patterns: `SLEvent%`, `Event%`, `%EventHandler%`, `%EventAction%`, `%AES%`
- For matches: query `IdoProperties` for field names, `IdoTables` for primary table (TableType=3)
- Try loading sample data from discovered IDOs
- Look for existing Credit Approval handler if possible

### `extract_aes_guide.py` Logic
Use PyMuPDF to extract text from the 212-page PDF, chunk by chapter/section, and write a structured markdown reference covering:
- Event types and framework events table
- Event handler configuration fields
- Action types with parameters and syntax
- Expression syntax, operators, and functions
- Suspension mechanics and InWorkflow pattern
- Credit approval and PO approval scenario walkthroughs

### Validation
1. User runs `discover_aes_idos.py` -- confirms connection and reviews discovered IDOs
2. `AES_Knowledge_Base.md` is reviewed for accuracy and completeness
3. Reference workflow JSONs are copied and verified
4. CLAUDE.md documents all findings (especially: are AES IDOs writable via API?)

**STOP for user validation.**

---

## Phase 1: ION Workflow JSON Builder

**Goal**: Build a Python module that programmatically constructs ION workflow JSON. Prove it by generating a clone of the Credit Approval workflow that deploys successfully.

### Why Build a Builder
ION workflow JSON is deeply nested: ionapi flowparts contain JSON-encoded `method` strings with embedded `$value()` tokens, conditions use XML strings, assignments have serialized JSON. A builder abstracts this complexity.

### Files

```
CSIWorkflowGenerator/
  src/
    __init__.py
    workflow_builder/
      __init__.py
      models.py          # Dataclasses: WorkflowVariable, WorkflowView, DistributionItem, etc.
      builder.py          # WorkflowBuilder: assembles components -> complete JSON dict
      flowparts.py        # Factory functions for each flowpart type
      conditions.py       # XML condition string builder
      ionapi.py           # ION API call builder (IDO load/update method structures)
  scripts/
    build_credit_approval.py   # Reconstruct CS_Credit_Approval from builder
    deploy_workflow.py         # Create + activate + start (wraps existing ION scripts pattern)
```

### Key Design

**FlowPart types** (all lowercase in JSON):
- `usertask` -- NOTIFICATION or USER_TASK with action buttons
- `assignment` -- VALUE_ASSIGNMENT, VARIABLE_ASSIGNMENT, EXPRESSION_ASSIGNMENT
- `ionapi` -- IDO load (GET) and update (POST) via SyteLine REST API
- `ifthenelse` -- XML condition string with trueBranch/falseBranch
- `subworkflow` -- nested sequential flow
- `parallelflow` -- ONE_IN or ALL_IN join
- `wait` -- timer/delay (HOURS, DAYS, etc.)

**ION API builder** (`ionapi.py`) handles the tricky nested structure:
- Builds `method` (JSON-encoded string) + `ionApiMethod` (dict) in sync
- Builds `inputBody` with `$value(VarName)` substitution for updates
- Maps workflow variables to API inputs/outputs via `wfVariableName` and JSONPath `$.Items[0].PropertyName`

**Condition builder** (`conditions.py`):
- Generates XML: `<Condition><UsedSubcondition>Name</UsedSubcondition><Subconditions><Subcondition><Name>...</Name><Type>AttributeValueComparison</Type><AttributeName>VarName</AttributeName><ComparisonOperator>Equal</ComparisonOperator><Value>Val</Value></Subcondition></Subconditions></Condition>`

### Validation
1. `python scripts/build_credit_approval.py` produces JSON structurally equivalent to reference (modulo name, serviceAccount, timestamps)
2. `python scripts/deploy_workflow.py output/CS_Credit_Approval_Clone.json --activate` succeeds
3. User confirms cloned workflow appears in ION Workflow Administration
4. User starts an instance and confirms usertask in Pulse with correct variables and drillback

**STOP for user validation.**

---

## Phase 2: Workflow Templates + Parameterization

**Goal**: Build a template system that takes a compact YAML workflow spec and generates complete ION workflow JSON. Validate with Credit Approval and Discount Approval templates.

### Why Templates
The builder from Phase 1 requires writing Python code per workflow. Templates let us describe workflows in ~30-40 lines of YAML instead of 600+ lines of JSON, making it feasible for the NL parser (Phase 4) to produce output.

### Files

```
CSIWorkflowGenerator/
  src/
    templates/
      __init__.py
      schema.py           # WorkflowSpec dataclass (the compact input format)
      renderer.py          # WorkflowSpec -> WorkflowBuilder -> JSON
      presets.py           # Common patterns (approval_task, ido_load, ido_update, etc.)
    config/
      __init__.py
      tenant.py            # Tenant-specific config (site, user GUIDs, service accounts)
  templates/
    credit_approval.yaml
    order_discount.yaml
  scripts/
    render_template.py     # CLI: YAML -> workflow JSON
```

### Template Format Example (Credit Approval)
```yaml
name: CS_Credit_Approval_v2
description: "CSI Credit Approval Workflow"

variables:
  - {name: CustNum, type: STRING, input: true}
  - {name: CustName, type: STRING, input: true}
  - {name: OldCreditLimit, type: STRING, input: true}
  - {name: NewCreditLimit, type: STRING, input: true}
  - {name: RowPointer, type: STRING, input: true}
  - {name: MGConfig, type: STRING, input: true}
  # Internal vars (ApproveReject, Filter, UpdatePropertyValue, ItemID) auto-created

views:
  - name: CustomerDrillBack
    viewSet: "infor.syteline (SyteLineViews)"
    view: CustomerView
    params: {ID1: "$CustNum"}

flow:
  - type: approval_task
    name: Review
    message: "Customer - [CustName] - Credit Limit has changed..."
    buttons: [Approve, Reject]
    resultVariable: ApproveReject
    distribution: "$approvers"

  - type: subworkflow
    name: "Update Record"
    steps:
      - type: assignment
        assign: [{var: Filter, expression: "\"RowPointer='\" & [RowPointer] & \"'\""}]
      - type: ido_branch
        condition: {var: ApproveReject, equals: Approved}
        true_value: {var: NewCreditLimit, target: UpdatePropertyValue}
        false_value: {var: OldCreditLimit, target: UpdatePropertyValue}
      - type: ido_load
        ido: SLCustomers
        properties: "Name,CustNum,CreditLimit,CustSeq,RowPointer"
        output: {ItemID: "$.Items[0]._ItemId"}
      - type: ido_update
        ido: SLCustomers
        updates: [{field: CreditLimit, var: UpdatePropertyValue}, {field: InWorkflow, value: "0"}]

  - type: notification
    name: Notify
    message: "...has been [ApproveReject]."
    distribution: "$notifyees"
```

### Renderer Logic
1. Read YAML spec
2. Auto-create internal variables based on flow requirements
3. Resolve `$approvers`/`$notifyees` from tenant config
4. Expand high-level flow types into full flowpart dicts via Phase 1 builder
5. Return complete workflow JSON

### Validation
1. Both templates render to valid JSON and deploy successfully
2. Template YAML is ~10x smaller than output JSON
3. User validates both workflows work end-to-end in Pulse

**STOP for user validation.**

---

## Phase 3: AES Configuration Builder

**Goal**: Build tooling to create AES event handlers and actions. Approach depends on Phase 0 findings.

### Path A: AES IDOs Are Writable (API automation)

```
CSIWorkflowGenerator/
  src/
    aes_builder/
      __init__.py
      models.py           # EventHandler, EventAction, EventCondition dataclasses
      builder.py           # Create handlers via IDO update API
      discovery.py         # Query existing AES configs
  scripts/
    create_aes_trigger.py  # Create trigger for IDO + field + workflow
    list_aes_triggers.py   # List existing handlers
```

### Path B: AES Is UI-Only (instruction generation)

```
CSIWorkflowGenerator/
  src/
    aes_builder/
      __init__.py
      generator.py         # Generate step-by-step UI instructions
      templates.py         # Common AES patterns
  scripts/
    generate_aes_instructions.py  # Output setup guide with exact field values
```

### Credit Approval AES Pattern (from AES Guide Scenarios)
1. **Event**: `IdoOnItemUpdate`, **Object**: `SLCustomers`
2. **Handler**: Synchronous=Yes, Suspend=Yes
3. **Action 10** (Finish): `CONDITION(NOT PROPERTYMODIFIED("CreditLimit"))` -- skip if CreditLimit not changed
4. **Action 20** (Prompt): Send approval request to credit manager
   - `TO(GC(CreditMgr))`
   - `SUBJECT(SUBSTITUTE("Credit limit change request for customer ID: {0}", P("CustNum")))`
   - `BODY(SUBSTITUTE("...request for credit limit change to ${0} for {1}...", P("CreditLimit"), P("Name"), P("CustNum")))`
   - `QUESTION("Do you approve this credit limit change?")`
   - `CHOICES("1,sYes,0,sNo")`
5. **Action 30** (Fail): `CONDITION(VOTINGRESULT(20) = 0)` -- fail if credit manager votes No
6. After handler: on fail -> rollback, on success -> commit + clear InWorkflow

### Alternative: ION-Triggered AES Pattern (from existing CS_Credit_Approval_API.json)
Instead of using AES Prompt (internal messaging), AES can:
1. Set `InWorkflow=1` on the record
2. Call ION API to start an ION workflow (passing CustNum, CustName, OldCreditLimit, NewCreditLimit, RowPointer, MGConfig)
3. ION workflow handles the approval UI (Pulse tasks)
4. ION workflow calls back to SyteLine API to update record + clear InWorkflow

### Validation
1. AES trigger created (via API or manually following instructions)
2. End-to-end: change credit limit in SyteLine -> AES fires -> workflow starts -> approval in Pulse -> write-back completes

**STOP for user validation.**

---

## Phase 4: Natural Language Parser

**Goal**: Build the parser that converts natural language workflow descriptions into WorkflowSpec YAML (Phase 2 format).

### Files

```
CSIWorkflowGenerator/
  src/
    parser/
      __init__.py
      workflow_parser.py    # NL text -> WorkflowSpec
      prompts.py            # LLM prompt templates for structured extraction
      ido_metadata.py       # Validate IDO/property names against live SyteLine
      user_resolver.py      # Resolve user names to IFS GUIDs
  scripts/
    parse_workflow.py       # CLI: NL description -> WorkflowSpec YAML
    generate_workflow.py    # CLI: NL -> JSON (parse + render)
```

### Parsing Strategy
Claude Code acts as the AI engine (local, no GenAI platform needed). The parser:
1. Extracts trigger info: IDO name, monitored field, guard condition pattern
2. Extracts workflow variables: what data needs to flow through the workflow
3. Extracts flow logic: approval/notification/condition/timeout patterns
4. Validates IDO names and properties against live SyteLine metadata (`ido_metadata.py`)
5. Resolves user/group references against tenant directory
6. Assembles WorkflowSpec

### IDO Metadata Validation (`ido_metadata.py`)
```python
def validate_ido_exists(ido_name: str) -> bool:
    """Query IdoCollections to verify the IDO exists."""

def validate_properties(ido_name: str, properties: list[str]) -> dict:
    """Query IdoProperties to verify property names and casing."""

def get_writable_properties(ido_name: str) -> list[str]:
    """Find properties on primary table (TableType=3) that are writable."""
```

### Validation
1. Known workflow descriptions produce correct specs matching Credit/Discount patterns
2. IDO and property validation catches case-sensitivity errors
3. User reviews generated specs and confirms intent capture

**STOP for user validation.**

---

## Phase 5: End-to-End Orchestrator + CLI

**Goal**: Unify all components into a single CLI that goes from natural language to deployed workflow.

### Files

```
CSIWorkflowGenerator/
  src/
    orchestrator/
      __init__.py
      pipeline.py           # NL -> parse -> render -> deploy -> AES setup
      validator.py           # Pre-deployment JSON validation
  scripts/
    wfgen.py                # Main CLI entry point
```

### CLI Commands
```bash
python scripts/wfgen.py create "When customer credit limit changes, require approval..."
python scripts/wfgen.py parse "description..."         # NL -> spec YAML only
python scripts/wfgen.py render spec.yaml               # Spec -> workflow JSON only
python scripts/wfgen.py deploy workflow.json            # Deploy + activate
python scripts/wfgen.py aes-setup workflow.json         # Configure AES trigger
python scripts/wfgen.py list                            # List deployed workflows
python scripts/wfgen.py status WorkflowName             # Check workflow status
python scripts/wfgen.py delete WorkflowName             # Clean up
```

### Pipeline Flow
```
NL Description
  -> parser.parse() -> WorkflowSpec (YAML)
  -> renderer.render() -> Workflow JSON
  -> validator.validate() -> validation report
  -> deployer.create_and_activate() -> deployed workflow
  -> aes_builder.create_trigger() -> AES configured
```

### Validation
1. Full pipeline: `wfgen create "<credit approval description>"` produces working workflow
2. End-to-end: field change -> AES -> workflow -> approval -> write-back
3. All individual commands work independently

**STOP for user validation.**

---

## Phase 6: Additional Patterns + Robustness

**Goal**: Expand beyond single-approval to handle additional common workflow types. Add error handling and hardening.

### New Patterns to Support
1. **Multi-level approval**: Sequential approvers (manager -> director -> VP based on amount thresholds)
2. **Parallel review**: Multiple people review simultaneously (ONE_IN or ALL_IN join)
3. **Timeout with escalation**: If no response in N days, escalate to next level or auto-reject
4. **Notification-only**: No approval needed, just notify on event (simplest case)
5. **Conditional routing**: Different paths based on field values (not just approve/reject)

### New Files
```
CSIWorkflowGenerator/
  src/
    templates/patterns/
      approval.py            # Single-level approval (existing)
      multi_approval.py      # Multi-level approval chain
      parallel_review.py     # Parallel review with join
      notification_only.py   # Simple notification
      conditional_route.py   # Field-value-based routing
    workflow_builder/
      validator.py           # JSON schema validation for generated workflows
    orchestrator/
      retry.py               # Retry logic for API calls (429, transient errors)
  templates/
    multi_level_po_approval.yaml
    quality_hold_notification.yaml
```

### Validation
- Each new pattern deploys and functions end-to-end
- At least 2 new patterns tested with real data
- Error handling covers: API failures, invalid IDO names, duplicate workflow names

**STOP for user validation.**

---

## Phase 7: GenAI Platform Tools (Goal 2)

**Goal**: Package local tooling as Infor GenAI platform tools following BOMGenerator pattern.

### Tools to Create
```
CSIWorkflowGenerator/
  specs/tools/
    GAF_ION_WorkflowCreate_Tool_v1.json     # POST /v1/workflows
    GAF_ION_WorkflowActivate_Tool_v1.json   # PUT /v1/workflows/{name}/activate
    GAF_ION_WorkflowGet_Tool_v1.json        # GET /v1/workflows/{name}
    GAF_ION_WorkflowList_Tool_v1.json       # GET /v1/workflows
    GAF_ION_WorkflowStart_Tool_v1.json      # POST /v1/workflow/start
    GAF_ION_WorkflowDelete_Tool_v1.json     # DELETE /v1/workflows/{name}
    GAF_SyteLine_IdoMetadata_Tool_v1.json   # GET /load/IdoProperties (validate IDO/fields)
```

If AES is API-accessible (Phase 0/3 results):
```
    GAF_SyteLine_AESCreate_Tool_v1.json     # Create AES event handler via IDO
    GAF_SyteLine_AESList_Tool_v1.json       # List existing AES handlers via IDO
```

### Tool Spec Pattern
Each follows the BOMGenerator format:
- `type: "API_DOCS"`, naming: `GAF_<Product>_<Capability>_Tool_v<N>`
- `servicePath`: relative (e.g., `IONSERVICES/process/model`)
- `api_docs`: method, endpoint (relative), headers, parameters, example request
- `responseInstructions`: parsing guidance + `---DEBUG---` template
- 1 tool = 1 HTTP call (framework constraint)

### Validation
1. All specs pass GAF_CLI validation: `python -m src.cli.validate_spec <spec>`
2. All tools publish successfully: `python -m src.cli.publish_tool <spec>`
3. Each tool individually testable via GenAI Chat
4. Tools confirmed working in GenAI Chat UI

**STOP for user validation.**

---

## Phase 8: GenAI Platform Agent (Goal 2)

**Goal**: Create the orchestrating GenAI agent that accepts NL workflow descriptions and uses Phase 7 tools to build complete workflows.

### Agent Spec
```
CSIWorkflowGenerator/
  specs/agents/
    GAF_ION_WorkflowGenerator_Agent_v1.json
```

- `type: "TOOLKIT"`, `data.tools`: all tool names from Phase 7
- `data.workflow`: detailed operational instructions encoding all domain knowledge:
  - How to parse NL descriptions
  - Required workflow variable patterns
  - ION flowpart structure rules (lowercase types, XML conditions, etc.)
  - Step-by-step creation sequence
  - Error handling and anti-hallucination rules
  - 240-second timeout management with checkpointing

### Agent Workflow Steps
1. Parse intent: extract trigger IDO, monitored field, approval pattern
2. Validate: call IdoMetadata tool to verify IDO/property names
3. Build variables: construct variables list based on workflow type
4. Build flowparts: assemble JSON workflow structure
5. Create workflow: call WorkflowCreate tool
6. Activate: call WorkflowActivate tool
7. Report: return workflow name, status, and AES setup instructions

### Validation
1. Agent spec passes GAF_CLI validation and publishes successfully
2. Agent invocable via CLI: `python -m src.cli.invoke_agent "Create a credit approval workflow..."`
3. Agent creates a valid, activatable workflow from NL description
4. Full end-to-end test through GenAI Chat UI

---

## Phase Dependencies

```
Phase 0 (Setup + AES Discovery + Knowledge Base)
  |
Phase 1 (ION Workflow JSON Builder)
  |
Phase 2 (Templates + Parameterization)
  |
Phase 3 (AES Configuration Builder) -- approach depends on Phase 0 findings
  |
Phase 4 (Natural Language Parser)
  |
Phase 5 (End-to-End Orchestrator CLI)
  |
Phase 6 (Additional Patterns + Robustness)
  |
Phase 7 (GenAI Platform Tools)       -- Goal 2 begins
  |
Phase 8 (GenAI Platform Agent)
```

## Key Risks & Open Questions

1. **Service Account**: ION workflow `ionapi` flowparts require an encrypted `serviceAccount` field. The reference workflows have these. We need to determine how to obtain/reuse one for new workflows.
2. **AES API Access**: Phase 0 determines if AES event handlers can be created/configured via IDO API. If not, Phase 3 falls back to generating step-by-step UI instructions.
3. **ION Workflow Versioning**: Updating an existing active workflow may require deactivate -> delete -> recreate -> activate cycle.
4. **Expression Complexity**: AES expressions have a rich grammar (Appendix C of AES Guide). The NL parser needs to generate valid expressions for conditions, property checks, and variable assignments.

## Verification Strategy

Each phase has explicit validation criteria requiring user confirmation in the live Infor environment. No phase proceeds without prior phase validation. The Credit Approval workflow serves as the golden reference throughout -- if the generated output matches the working reference, the tooling is correct.
