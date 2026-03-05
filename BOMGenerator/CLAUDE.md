# BOMGenerator - CLAUDE.md

## Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.** Infor OS is NOT a typical local development stack - there is no local runtime, domain knowledge gaps cause frequent errors, and only the user can validate results in the live environment. Do NOT batch multiple phases together. After each phase: summarize what was done, what needs testing, and WAIT for user confirmation before continuing. See root `CLAUDE.md` for full details.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Purpose

GenAI agent that creates realistic multi-level Bill of Material (BOM) data in Infor CSI/SyteLine from natural language prompts. Accepts requests like "Create a 3-level BOM for a mountain bike" and creates all items, routing operations, and BOM structures directly in SyteLine.

## Architecture

### SyteLine BOM Data Model

BOMs in SyteLine are structured around **Standard Jobs** (`Type='S'`):

```
SLItems (Item Master)
  +-- SLJobs (Standard Job, Type='S', links Item to routing+materials)
       |-- SLJobRoutes (Operations/Routing for this item)
       |    +-- OperNum 10, 20, 30... with Work Centers
       +-- SLJobmatls (Materials/BOM components)
            +-- Materials linked to operations via OperNum + Sequence
```

### Creation Order (CRITICAL)

SyteLine enforces this dependency chain:
1. **SLItems** - All parts/assemblies must exist first
2. **SLHighKeys** (LOOKUP) - If prompt doesn't specify job numbers (or numbers are stale), call JobNumberLookup to get next available BOM number
3. **SLJobs** - Create standard job (`Type='S'`) for each parent/assembly item
4. **SLJobRoutes** - Add routing operations to the job (referenced by materials)
5. **SLWcResourceGroups** (LOOKUP) - Query actual valid Rgid for each work center used. **NEVER guess Rgid from naming convention.**
6. **SLJrtResourceGroups** - Insert resource group record for each operation using EXACT Rgid from step 5 (populates Resources grid)
7. **SLJrtSchs** - Set `Setuprgid` + `SchedDrv` on each operation (update, not insert -- records auto-created by step 4). SchedDrv from RgrpSLTYPE in step 5.
8. **SLJobmatls** - Add material lines (children), each linked to an operation via `OperNum`
9. **SLItemwhses** - Link item to its standard job by setting `ItwhJob` (required for Current Operations form)

**Steps 5 and 6 are independent** -- SLJrtResourceGroups insert does NOT auto-set SLJrtSchs.Setuprgid. Both must be set separately.

**SchedDrv alignment**: When updating SLJrtSchs.Setuprgid, also set `SchedDrv` to match the resource group type:
- Resource group suffix `LRG` (RgrpSLTYPE='L') -> `SchedDrv='L'` (Labor)
- Resource group suffix `MRG` (RgrpSLTYPE='M') -> `SchedDrv='M'` (Machine)
- Prevents "Sched Driver was X now is Y" warning in UI

### Tools (16 total)

All tools follow naming convention: `GAF_SyteLine_<Capability>_(Tool|Agent)_v<N>`

| Tool | IDO | Pattern | Purpose |
|------|-----|---------|---------|
| ItemSearch_Tool_v1 | SLItems | GET | Search items by code/description |
| ItemInsert_Tool_v1 | SLItems | POST | Create items (anti-hallucination guard) |
| JobSearch_Tool_v1 | SLJobs | GET | Search standard jobs (Type='S') |
| JobInsert_Tool_v1 | SLJobs | POST | Create standard job for an item |
| RoutingSearch_Tool_v1 | SLJobRoutes | GET | Search routing operations |
| RoutingInsert_Tool_v1 | SLJobRoutes | POST | Add routing operations (batch) |
| MaterialSearch_Tool_v1 | SLJobmatls | GET | Search BOM materials |
| MaterialInsert_Tool_v1 | SLJobmatls | POST | Add materials to BOM (batch) |
| JobNumberLookup_Tool_v1 | SLHighKeys | GET | Look up next available BOM job number |
| WorkCenterSearch_Tool_v1 | SLWcs | GET | Search work centers (ONLY Wc,Description,Dept) |
| ResourceGroupLookup_Tool_v1 | SLWcResourceGroups | GET | Look up actual valid Rgid per work center |
| ResourceGroupInsert_Tool_v1 | SLJrtResourceGroups | POST | Add resource group records per operation |
| JrtSchsLoad_Tool_v1 | SLJrtSchs | GET | Load SLJrtSchs records to get _ItemId |
| SetuprgidUpdate_Tool_v1 | SLJrtSchs | POST | Set Setuprgid + SchedDrv per operation |
| ItemWhseLoad_Tool_v1 | SLItemwhses | GET | Load SLItemwhses records to get _ItemId |
| ItemWhseUpdate_Tool_v1 | SLItemwhses | POST | Link item to standard job via ItwhJob |

### Agent

- `GAF_SyteLine_BomGenerator_Agent_v1` - Orchestrates all 16 tools with 8-step workflow, dynamic chunking (~5 tool calls per chunk to stay under 240s platform timeout)

### Tool Split Pattern (1 Tool = 1 API Call)

**CRITICAL**: The GenAI tool framework executes exactly ONE HTTP call per tool invocation. Two-step tools (GET then POST) do NOT work -- the framework reads `api_docs`, executes Step 1 only, and the tool invocation ends. Step 2 never fires.

**Solution**: Split two-step tools into separate Load (GET) and Update (POST) tools:
- Load tool: Makes GET call, returns `_ItemId` needed for the update
- Update tool: Makes POST call, requires `_ItemId` from the Load tool

**Applied to**: JrtSchsLoad/SetuprgidUpdate and ItemWhseLoad/ItemWhseUpdate

### GenAI Framework URL Construction (CRITICAL)

- The framework auto-constructs URLs as: `servicePath + endpoint_from_api_docs`
- `servicePath` is set in the tool spec (e.g., `"CSI/IDORequestService/ido"`)
- **All endpoints in api_docs MUST be relative** (e.g., `/load/SLItems`), never absolute
- If absolute paths are used, the service path gets doubled -> 404
- LLMs may hallucinate extra URL segments (tenant names, tool names, "api", "invoke") -- all tool specs and agent workflow include anti-hallucination constraints

## IDO Collections

### SLItems (Item Master)
- Key properties: Item, Description, UM, MatlType, PMTCode, ProductCode, AbcCode, CostType, CostMethod, Stat

### SLJobs (Standard Jobs - BOM Container)
- `Job` (NumSortedString) - 10 chars, left-padded with spaces (e.g., `"     99001"`)
- `Suffix` (Short Integer) - Always 0 for standard
- `Item` (String) - Item code this job is for
- `Type` (String) - 'S' = Standard (BOM template)
- `Stat` (String) - 'F' = Firm
- `QtyReleased` (Decimal) - Standard quantity (usually 1.00)
- `Whse` (String) - Warehouse code
- **Job number MUST be provided explicitly** - auto-assign does NOT work (NextKeys_mst error)
- **BOM prefix** (current): `BOM0000001` through `BOM9999999` — tracked by SLHighKeys, auto-registered
- Legacy range 90000-99999 (null prefix) is exhausted at 99902 — do NOT use

### SLJobRoutes (Routing Operations)
- `Job`, `Suffix`, `OperNum` (10, 20, 30...), `Wc` (work center code)
- `SetupHrsT`, `RunHrsTLbr`, `RunHrsTMch`

### SLJobmatls (BOM Materials/Components)
- `Job`, `Suffix`, `OperNum`, `Sequence` (1, 2, 3...)
- `Item` (child/component), `Description`, `MatlQtyConv` (qty per parent), `UM`
- `MatlType` ('M'=Material), `Units` ('U'=Unit), `RefType` ('I'=Inventory, 'J'=Job/sub-assembly, 'P'=Phantom)
- `AltGroup` (auto-increments: 1, 2, 3...), `ScrapFact` (0.00 default)

### SLHighKeys (Job Number Tracking)
- Tracks last-used key values per table/column/prefix combination
- Key properties: `TableColumnName` (e.g., `job.job`), `Prefix`, `HighKey` (last value), `SubKey`
- Primary table: `SLHighKeys` (TableType=3, writable)
- **IdoProperties returns 0 records** (metadata quirk) — but standard properties work for read/write
- Job entries: `TableColumnName = 'job.job'` — 15 entries across various prefixes
- HighKey is always 10 chars for jobs: `{Prefix}{zero-padded number}` (e.g., `SEQ0000007`, `DJ00000404`)
- **"BOM" prefix registered** — auto-created by SyteLine when `BOM0000001` was inserted. HighKey=`BOM0000001`
- **Auto-registration confirmed**: Inserting a job with a new prefix auto-creates the SLHighKeys entry
- Format with "BOM" prefix (3 chars): `BOM0000001` through `BOM9999999` (7 numeric digits)
- Old null-prefix range at `99902` (exhausted — do NOT use)
- **Dynamic lookup pattern** (for `generate_prompt.py`):
  - Query: `GET /load/SLHighKeys?filter=Prefix='BOM'&properties=HighKey`
  - Parse numeric portion of HighKey (e.g., `BOM0000001` → `1`)
  - Next available = parsed + 1, zero-padded back to 7 digits

### SLWcs (Work Centers - 88 available)
| Code | Description | Use For |
|------|-------------|---------|
| FA-400 | Final Assembly Area | Assembly operations |
| AS-500 | Assembly Area | Sub-assembly operations |
| MC-300 | Machining | Machining operations |
| CUT-10 | Cutting Area | Cutting operations |
| DRL-10 | Drilling Operations | Drilling |
| GRD-10 | Grinding Operations | Grinding |
| PNT-10 | Painting Area | Painting/finishing |
| INS-10 | Mfg. Inspection Area | Inspection |
| INS-20 | Inspection Center | Quality inspection |
| PG-300 | Outside Packaging | Packaging |
| PKG-10 | Packaging Station | Packaging |
| ST-100 | Warehouse Staging | Final staging |
| MLD-10 | Molding | Molding/casting |
| DRY-10 | Drying Area | Drying/curing |
| GLU-10 | Glue Area | Adhesive operations |
| WC-ASY | Assembly | General assembly |
| WC-FBR | Fabrication | General fabrication |
| WC-WLD | Welding | Welding operations |
| ENG-10 | Engineering | Engineering |
| SMP-10 | Metal Stamping | Stamping |
| PHANTM | Phantom Work Center | Phantom operations |

Also: Mountain bike (PS-*: 10 WCs), Automotive (AU-*: 14 WCs), Print/Paper (PP-*: 9 WCs), RV/Marine (RV-*, RD*, RM*: 13 WCs), Electronics (BX-*: 3 WCs), Shelving (S-*: 5 WCs).

### SLItemwhses (Item-Warehouse - Linkage to Standard Job)
- IDO: `SLItemwhses` (NOT `SLItwhses`)
- Keys: `Item`, `Whse`
- **`ItwhJob`** (writable) -- sets which standard job is the "current" BOM for this item+warehouse
- **`Job`** (read-only) -- automatically derived from `ItwhJob`
- **ItwhJob is NOT auto-populated** when creating a standard job -- must set explicitly via update
- **IDO quirk**: Load requests with `properties` param return 0 records -- must omit `properties` param

### SLJrtSchs (Job Route Schedules)
- Primary table: `jrt_sch`
- Writable: `Setuprgid`, `Setuprule`, `SchedDrv` (L=Labor, M=Machine)
- Keys: `Job`, `Suffix`, `OperNum`
- Records auto-created when routing operations are inserted via SLJobRoutes
- **Setuprgid is NOT auto-populated** -- must be set explicitly after routing insert
- Cross-IDO: After update, value shows as `JshSetuprgid` in SLJobRoutes (read-only there -- writes silently ignored)

### SLJrtResourceGroups (Resources Grid)
- Primary table: `jrtresourcegroup`
- Writable: `Job`, `Suffix`, `OperNum`, `Rgid`, `QtyResources`, `Resactn` (default 'S'), `Sequence` (default '1')
- Read-only: `RgrpDESCR`, `RgrpSLTYPE` (L/M/O), `Plant`, `RowPointer`
- **IDO quirk (INVERSE of SLItemwhses)**: MUST specify `properties` param to get data; omitting returns 0 records
- Rgid is **case-sensitive** (e.g., `Cut-10-MRG` not `CUT-10-MRG`)
- Invalid Rgid returns "The Group entered is not valid"; batch insert is atomic (1 bad Rgid rolls back ALL rows)

### SLWcResourceGroups (Work Center to Resource Group Mapping)
- 90 mappings across 88 work centers
- Properties: `Wc`, `Rgid`, `RgrpSLTYPE` (L/M/O), `QtyResources`
- Naming convention `<WC>-LRG`/`<WC>-MRG` is **unreliable** (e.g., PG-300 has `PG-300-MRG`, ST-100 has `ST-100-MRG1`)
- **ALWAYS look up actual Rgid** via ResourceGroupLookup tool -- NEVER guess
- Batch lookup: `Wc IN ('FA-400','INS-20','PG-300')` filter

## Key Discoveries

### GenAI Platform Constraints
- **Agent execution timeout: 240s is a `chat_sync` API gateway limit, NOT a model limit**: The 504 Gateway Timeout happens at the API gateway layer when using `POST /chat/sync`. The agent/model continues running on the platform — confirmed by checking Chat UI History after a "timeout" and finding the agent had completed successfully. **Solved**: Async chat pattern now in GAF_CLI (`client.chat()` + `client.poll_for_response()`). See GAF_CLI CLAUDE.md "Async Chat Pattern" section.
- **Chunking is still needed**: Even without the gateway timeout, chunking provides checkpoint/resume capability and keeps agent context manageable. The ~5 tool call budget per chunk remains a good practice.
- **Async chat API details**: `POST /chat` returns immediately with `{"message": "Message sent"}`. Messages (User + LLM) appear together once agent finishes (~2-3 min). Session IDs must be dashless hex (`uuid.uuid4().hex`). Pagination is 1-based (page=1, not 0). Items ordered newest-first. All async infrastructure now lives in GAF_CLI's `genai_client.py` — `chat()`, `get_session_messages()`, `poll_for_response()`.
- **Platform system errors ≠ agent failure**: "I'm sorry, a system error has occurred" responses from `POST /chat` do NOT necessarily mean the agent stopped. The agent may continue processing on the platform backend. During the ES-T10000 stress test, 22 out of 30 async API calls returned system errors, but the agent completed all work successfully (confirmed via Chat UI History and verify_bom.py). The test harness should treat system errors as "unknown progress" not "no progress."
- **Duplicate materials from error recovery**: When system errors interrupt the material insertion phase, the agent may re-insert materials on recovery without checking for existing records. This creates duplicate BOM lines. Functionally correct but cosmetically imperfect. Seen in ES-T10000 (SA-T10-GRIP had 6 materials instead of 3).
- **Tool call weight classification**: Not all tool calls take the same time. LIGHT tools (~20-30s): ItemSearch, ItemInsert, JobSearch, JobInsert, JobNumberLookup, WorkCenterSearch. HEAVY tools (~40-50s): RoutingInsert, ResourceGroupInsert, ResourceGroupLookup, JrtSchsLoad, SetuprgidUpdate, MaterialInsert, MaterialSearch, ItemWhseLoad, ItemWhseUpdate. For LIGHT-only chunks, checkpoint after 4 calls. If ANY call in a chunk is HEAVY, checkpoint after 3 calls instead. This prevents timeout in chunks dominated by heavy operations (e.g., routing+RG steps). Discovered from BH-T04000 timeout where chunk 4 had 5 all-heavy calls at 48s avg = 240s+.
- **Tools cannot be invoked directly** -- only agents can call tools. Test via agent prompts or a test handler agent.
- **Instructions field limit**: 900 characters max. Put details in `api_docs` (tools) or `workflow` (agents).
- **1 tool = 1 HTTP call**: Framework executes one API call per invocation. Split two-step operations into separate Load + Update tools.
- **Framework auto-prepends servicePath**: All api_docs endpoints must be relative. Absolute paths cause doubled URLs and 404s.

### LLM Anti-Hallucination
- LLMs invent plausible IDO properties (e.g., "Source" for SLItems, "ResourceGroup" for SLWcs). All insert/search tools include "ONLY use exact properties listed" constraints.
- LLMs hallucinate URL segments (tenant names, tool names, doubled service paths). All tools have relative-path constraints; agent has URL CONSTRUCTION RULE.
- Agent error handling: 404 = HARD ERROR (stop and report). ResourceGroupInsert and ItemWhseUpdate failures = HARD ERROR. Agent never says "non-blocking" for these.
- 5-point completion criteria: all must pass for "Complete" status; otherwise reports "INCOMPLETE -- X of Y criteria met".

### SyteLine BOM Model
- **BOM = Standard Job (Type='S')**: `SLBomListing`/`SLMaterialListing` are read-only views. Insert via SLJobs/SLJobRoutes/SLJobmatls.
- **Multi-level BOM**: Parent's material has `RefType='J'` for sub-assemblies. Child needs own Standard Job. Build bottom-up (leaves first).
- **Job numbers**: Must be explicit (auto-assign fails). 10 chars total. Use "BOM" prefix: `BOM0000001`+ (tracked by SLHighKeys). Old null-prefix range 90000-99999 is exhausted.
- **Operation numbers**: Increment by 10 (10, 20, 30...). Materials link via `OperNum`.

### Valid Values
- **PMTCode**: M (Manufactured), P (Purchased), T (Transferred). NO other values ("B" is NOT valid).
- **ProductCode**: Safe default **FG-100**. RM-100 is INVALID.

### IDO Metadata Discovery (CRITICAL)
NEVER conclude a field is not writable until metadata IDOs are queried. Use:
- **`IdoTables`**: Find tables joined by IDO. `TableType=3` = primary (writable).
- **`IdoProperties`**: Map property to underlying column and table.
- **`IdoCollections`**: Look up IDO by name.

Silent write failures (200 OK, value not persisted) = property on joined table. Find the IDO that owns that table as primary and write through it.

Full workflow: See `CSIPOAssetCreationTool/Agents&Tools/CLAUDE.md` -> "IDO Metadata Discovery via System IDOs"

### IDO Update Pattern
- Modified fields: `{IsNull: false, Modified: true, Name: "field", Value: "value"}`
- Key fields: `{IsNull: false, Modified: false, Name: "Job", Value: "..."}`
- `_ItemId`: from load response, included as non-modified property
- Workflow: Load record (get _ItemId) -> Build update payload -> POST

## Deployed Assets

| Asset | Type | GUID |
|-------|------|------|
| GAF_SyteLine_ItemSearch_Tool_v1 | Tool | fe474baf-5f54-4fcd-82ce-2be099a22646 |
| GAF_SyteLine_ItemInsert_Tool_v1 | Tool | 9350da81-020f-4755-accf-95bfd1efb151 |
| GAF_SyteLine_JobSearch_Tool_v1 | Tool | eb4e778a-3c98-45de-a2a1-eafe37c40000 |
| GAF_SyteLine_JobInsert_Tool_v1 | Tool | 20e5bc21-6338-46b7-a63e-aba7893c0f2d |
| GAF_SyteLine_RoutingSearch_Tool_v1 | Tool | d8d79954-74f3-4765-bd42-e6290fae8e58 |
| GAF_SyteLine_RoutingInsert_Tool_v1 | Tool | 48b61dae-19bd-48da-8183-fd69c3ce933d |
| GAF_SyteLine_MaterialSearch_Tool_v1 | Tool | b43415b8-21f7-49fc-a0e3-5140a3bc48fe |
| GAF_SyteLine_MaterialInsert_Tool_v1 | Tool | bf6466c3-b27c-40f7-8296-329cd40537e3 |
| GAF_SyteLine_WorkCenterSearch_Tool_v1 | Tool | a213d01a-6127-4850-9c6a-78d22479380b |
| GAF_SyteLine_ResourceGroupLookup_Tool_v1 | Tool | 50ec9bcd-54b4-48c9-90f8-addce9d90834 |
| GAF_SyteLine_ResourceGroupInsert_Tool_v1 | Tool | 3414da63-d060-43a2-8430-a913c59933ce |
| GAF_SyteLine_JrtSchsLoad_Tool_v1 | Tool | dfda76ea-1e26-4a77-aefd-070bf61ddb5d |
| GAF_SyteLine_SetuprgidUpdate_Tool_v1 | Tool | ddd0613e-1181-4fe5-87f1-22ee0f90bf9c |
| GAF_SyteLine_ItemWhseLoad_Tool_v1 | Tool | 7d63513e-218a-4da8-aa32-36355e91a8b8 |
| GAF_SyteLine_ItemWhseUpdate_Tool_v1 | Tool | d4659be6-5d9b-4e7d-b431-39f8b24aed2c |
| GAF_SyteLine_JobNumberLookup_Tool_v1 | Tool | 2db9d036-7e62-497d-af8f-162f5026c48d |
| GAF_SyteLine_BomGenerator_Agent_v1 | Agent | 381607bb-bb48-40dd-bfa8-84873a3dc3cf |

Agent logical ID: `lid://infor.syteline.bom-generator-v1`

## GAF_CLI

**Location**: `../GAF_CLI` (sibling directory at repo root)

```bash
# Run from GAF_CLI/ directory:
cd ../GAF_CLI

# Validate spec
python -m src.cli.validate_spec "../BOMGenerator/specs/tools/YourTool.json"

# Publish / Update
python -m src.cli.publish_tool "../BOMGenerator/specs/tools/YourTool.json"
python -m src.cli.publish_agent "../BOMGenerator/specs/agents/YourAgent.json"
python -m src.cli.update_asset "../BOMGenerator/specs/tools/YourTool.json"   # spec must include "guid"

# Invoke BOM Generator Agent
python -m src.cli.invoke_agent -a GAF_SyteLine_BomGenerator_Agent_v1 "Create a wooden chair BOM" --json
python -m src.cli.invoke_agent -a GAF_SyteLine_BomGenerator_Agent_v1 -i   # Interactive
```

### Test Prompt Generator

**File**: `scripts/generate_prompt.py`

Generates unique, ready-to-use test prompts with:
- Unique item prefixes from local sequence counter (`scripts/.test_sequence`)
- Dynamic job number ranges from SLHighKeys API lookup
- Sentinel tokens for automated test harness (`<<CHECKPOINT>>`, `<<COMPLETE>>`)
- Pipe-friendly output (prompt to stdout, metadata to stderr)

```bash
python generate_prompt.py                          # Random template
python generate_prompt.py --template chair         # Specific template
python generate_prompt.py --desc "custom thing"    # Custom description
python generate_prompt.py --list                   # Show all 8 templates
python generate_prompt.py --dry-run                # Preview without incrementing
python generate_prompt.py | clip                   # Copy to clipboard (Windows)
```

**Templates** (8 built-in):

| Name | Prefix | Complexity | Jobs | Description |
|------|--------|------------|------|-------------|
| birdhouse | BH | simple | 5 | Wooden birdhouse with 2 sub-assemblies (body + roof), panels, screws, perch |
| stool | ST | simple | 5 | 4-legged wooden stool |
| chair | CH | moderate | 10 | Wooden chair with seat, backrest, 4 legs |
| desk-lamp | DL | moderate | 10 | Desk lamp with base, arm, shade |
| bookshelf | BS | moderate | 10 | 3-shelf bookshelf with frame |
| workbench | WB | complex (2-lvl) | 20 | Steel workbench with drawer sub-assembly |
| bicycle | MB | complex (2-lvl) | 20 | Mountain bike with wheel + drivetrain sub-assemblies |
| go-kart | GK | complex (3-lvl) | 20 | Go-kart with chassis (containing rear axle sub-assy), engine, steering — true 3-level nesting |

**Uniqueness mechanism**: Sequence file `scripts/.test_sequence` stores an integer (auto-created on first run). Each run increments it. Seq 1 → item prefix `T01`, seq 2 → `T02`, etc. Example item code: `BH-T01000`.

**Job number allocation**: Queries `SLHighKeys` for `Prefix='BOM'` to find last-used BOM job number, then allocates a range (5/10/20 depending on complexity). Falls back to sequence-based range if API unavailable.

**Also importable as module**:
```python
from generate_prompt import generate, generate_for_case, lookup_next_job_number
result = generate(template_name="chair")  # Returns dict with prompt, item_code, job_range, etc.
```

### Automated Test Script

**File**: `scripts/test_bom_agent.py`

Uses GAF_CLI's async chat pattern (`client.chat()` + `client.poll_for_response()`) to bypass the 240s gateway timeout. Auto-continues through agent checkpoints via sentinel detection. Prompts auto-generated via `generate_prompt.py` with unique item codes and dynamic job numbers.

```bash
python test_bom_agent.py --case simple -v          # Simple birdhouse BOM
python test_bom_agent.py --case moderate -v         # Moderate chair BOM
python test_bom_agent.py --case complex -v          # Complex mountain bike BOM
python test_bom_agent.py --all -v                   # Run all test cases
python test_bom_agent.py --prompt "Custom BOM" -v   # Custom prompt
python test_bom_agent.py --case simple -v --poll-interval 15 --max-polls 30
```

Case mapping: `simple` → birdhouse, `moderate` → chair, `complex` → bicycle. Each run auto-generates unique item prefixes and pre-allocates non-overlapping job number ranges for batch (`--all`) runs.

### BOM Verification Script

**File**: `scripts/verify_bom.py`

Recursively walks a BOM tree and validates 7 checks per assembly node via IDO API queries:

| # | Check | IDO | Severity | Notes |
|---|-------|-----|----------|-------|
| 1 | Item exists | SLItems | FAIL | |
| 2 | Standard job exists | SLJobs | FAIL (top-level) / INFO (leaf) | |
| 3 | ItwhJob linkage | SLItemwhses | FAIL | properties=None (IDO quirk) |
| 4 | Routing ops exist | SLJobRoutes | FAIL | |
| 5 | Resource group per op | SLJrtResourceGroups | FAIL | MUST specify properties (inverse quirk) |
| 6 | Setuprgid per op | SLJrtSchs | FAIL | Also reports SchedDrv value |
| 7 | Materials exist | SLJobmatls | WARN if empty | |

**ItwhJob check (#3)** is the critical addition — without it, the validator gave false positives because it queried SLJobs directly (which works regardless of UI traversal). The SyteLine UI traverses `Item -> ItwhJob -> Job -> Materials -> sub-assembly -> ItwhJob -> ...`. Missing ItwhJob = UI dead-end.

**API calls per assembly**: 7 (SLItems + SLJobs + SLItemwhses + SLJobRoutes + SLJrtResourceGroups + SLJrtSchs + SLJobmatls). RG and Setuprgid calls are batched per job (one API call covers all operations).

```bash
python verify_bom.py GK-T09000 --deep    # Recursive verification
python verify_bom.py ES-T10000 --json     # JSON output
```

## GAF_CLI Validation Requirements

- Name format: `^GAF_[A-Za-z0-9]+_[A-Za-z0-9]+_(Tool|Agent)_v\d+$`
- No hardcoded tenant URLs
- No blank lines in `api_docs`
- No auth documentation in `api_docs`
- `api_docs` must include `Example Request:` section
- `responseInstructions` must include `---DEBUG---` template with FULL_URL, FULL_RESPONSE, ---END DEBUG---
- Tools: `data.api_docs` and `data.responseInstructions` required
- Agents: `data.tools` array and `data.workflow` required

## File Structure

```
BOMGenerator/
  CLAUDE.md                          # This file
  log.md                             # Progress tracking
  BillOfMaterialGenerator.txt        # Broader project vision (future features)
  discovery/
    ido_discovery.md                 # Full IDO discovery documentation
  specs/
    tools/                           # 15 tool JSON specs (for GAF_CLI)
    agents/                          # 1 agent JSON spec (for GAF_CLI)
    _backup_v1/                      # Backup of v1 specs (pre-dynamic-chunking)
  scripts/
    generate_prompt.py               # Test prompt generator (unique items + dynamic job numbers)
    test_bom_agent.py                # Automated multi-turn test harness
    verify_bom.py                    # BOM verification via IDO API queries (7 checks per assembly)
    .test_sequence                   # Local sequence counter (auto-created, not committed)
    discover_highkeys.py             # SLHighKeys IDO discovery (job number tracking)
    test_bom_prefix_job.py           # BOM prefix auto-registration test
    discover_itwhse_wcs.py           # ItwhJob linkage + WC catalog discovery
    discover_resource_groups.py      # Resource group investigation v1
    discover_resource_groups_v2.py   # Resource group investigation v2
    ido_field_discovery.py           # IDO field testing scripts
    ido_field_discovery_2.py
    ido_field_discovery_3.py
    access_token.txt                 # Auth token (2hr expiry)
    _archived_smoke_test_async_chat.py  # Archived — async pattern now in GAF_CLI
    test_logs/                       # Auto-generated test output (gitignored)
```

## Project Status

**Current**: Async chat pattern validated — `POST /chat` + polling eliminates 240s gateway timeout

**What's validated and working**:
- All 16 tools + agent deployed and functional
- **ES-T10000 Electric Scooter (5-level)**: stress test — 5-level deep BOM, 9 jobs (BOM0000813-821), 33 items, 56/56 checks passed. Two branches both reach level 5. Agent completed on platform despite 22 async API system errors. Duplicate materials from system error recovery (known issue).
- **GK-T09000 Go-Kart (2-level wide, mislabeled 3-level)**: 6 chunks/1098s, 44/44 checks passed — 4 jobs (BOM0000809-812), 3 sub-assemblies (chassis/engine/steering), 18 materials, 12 routing ops. Agent produced 2 levels despite "3-level" in prompt — root cause: flat description + no depth verification (both fixed 2026-02-13)
- **BH-T03000 Birdhouse**: first fully automated test (test_bom_agent.py → verify_bom.py), 12/12 checks passed
- **ST-10000 Stool (ad-hoc)**: ad-hoc prompt test (no job numbers in prompt), agent called JobNumberLookup → BOM0000805-808, 16/16 checks passed
- BH-10000 Birdhouse: first manual end-to-end BOM creation
- Dynamic chunking with weighted tool-call budgeting (LIGHT-only: 4 calls/chunk, HEAVY: 3 calls/chunk), sentinel-based checkpoint detection (`<<CHECKPOINT>>`, `<<COMPLETE>>`)
- Resource groups (SLJrtResourceGroups + SLJrtSchs.Setuprgid + SchedDrv alignment)
- ItwhJob linkage (BOM visible in Current Operations/Materials forms)
- ResourceGroupLookup tool replaces unreliable naming convention guessing
- **SLHighKeys "BOM" prefix**: auto-registered, dynamic job number lookup confirmed working
- **Phase 2 backward compat**: agent uses prompt-specified job numbers when provided (validated by automated test)
- **Phase 2 ad-hoc self-serve**: agent calls JobNumberLookup when no job numbers in prompt (validated: ST-10000 stool)
- **Multi-level BOM**: agent creates 2- and 5-level hierarchies with sub-assemblies (validated: BH-T03000 2-level, ES-T10000 5-level). GK-T09000 was intended as 3-level but only produced 2-level wide — true 3-level not yet validated (template + agent fixed 2026-02-13, pending re-test)

**Test Prompt Generator + Dynamic Job Numbers**:
- Phase 0 (SLHighKeys discovery): COMPLETE and validated
- Phase 1 (prompt generator): COMPLETE and validated — natural language prompts with `---DEBUG---` error surfacing and `<<CHECKPOINT>>`/`<<COMPLETE>>` sentinels
- Phase 2 (JobNumberLookup): Tool published (GUID: `2db9d036-7e62-497d-af8f-162f5026c48d`), agent updated from 15→16 tools — backward compat validated, ad-hoc path validated

**Remaining work**:
- **True 3-level BOM validation**: Re-run go-kart template (fixed with nested rear-axle assembly + agent depth verification) to confirm actual 3-level depth. GK-T09000 was only 2-level wide.
- Test data cleanup (TEST-BOM-001, BOMTEST-001/003, GB-10000, TB-10001, BH-10000, BH-T03000, BOM-PREFIX-TEST, ST-10000, GK-T09000, ES-T10000 items)
- Duplicate material cleanup for ES-T10000 (SA-T10-GRIP, SA-T10-HBAR, SA-T10-CELL, SA-T10-BATT have doubled material lines)
- Broader vision items from `BillOfMaterialGenerator.txt` (transactional data, MRP validation, image-to-BOM)

