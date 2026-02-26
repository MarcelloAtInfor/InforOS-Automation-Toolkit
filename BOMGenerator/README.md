# BOM Generator Agent

A GenAI agent that creates realistic multi-level Bill of Material (BOM) data in **Infor CloudSuite Industrial (SyteLine)** from natural language prompts. Powered by the **Infor GenAI Platform** and orchestrating 16 purpose-built tools, it creates all items, standard jobs, routing operations, resource groups, and BOM structures directly in SyteLine — no manual data entry required.

> **Example:** *"Create a 3-level BOM for a go-kart with a chassis sub-assembly containing a rear axle assembly"* produces all items, jobs, routings, and material links in SyteLine within minutes.

## What It Does

```
Natural Language Prompt
        |
        v
+-------------------+
|  BOM Generator    |     "Create a 5-level BOM for an
|  Agent            |      electric scooter with chassis
|  (Claude 4.5)     |      and powertrain sub-assemblies..."
+-------------------+
        |
        | 8-step workflow, 16 tools
        v
+-------------------+
|  Infor SyteLine   |
|  ERP System       |
+-------------------+
        |
        v
  Items + Standard Jobs + Routing
  + Resource Groups + Materials
  + Item-Job Linkages
```

The agent handles the complete BOM creation lifecycle:

- **Items** — creates part masters for assemblies and purchased components
- **Standard Jobs** — creates Type='S' jobs as BOM containers
- **Routing Operations** — adds manufacturing steps with work centers and time estimates
- **Resource Groups** — assigns labor/machine resources to each operation
- **BOM Materials** — links child components to parent assemblies
- **Item-Job Linkage** — connects items to their standard jobs so BOMs appear in the SyteLine UI

## Architecture

### SyteLine BOM Data Model

BOMs in SyteLine are structured around Standard Jobs:

```
SLItems (Item Master)
  +-- SLJobs (Standard Job, Type='S')
       |-- SLJobRoutes (Operations/Routing)
       |    +-- OperNum 10, 20, 30... with Work Centers
       |    +-- SLJrtResourceGroups (Resource assignments)
       |    +-- SLJrtSchs (Schedule driver + setup resource)
       +-- SLJobmatls (Materials/BOM components)
            +-- Materials linked to operations via OperNum
  +-- SLItemwhses (Item-Warehouse linkage via ItwhJob)
```

### Creation Order

SyteLine enforces a strict dependency chain. The agent follows this order:

| Step | IDO | Action |
|------|-----|--------|
| 1 | SLItems | Create all items (bottom-up: leaves first) |
| 2 | SLHighKeys | Look up next available BOM job number (if needed) |
| 3 | SLJobs | Create standard jobs for each assembly |
| 4 | SLJobRoutes | Add routing operations to each job |
| 5 | SLWcResourceGroups | Look up valid resource groups per work center |
| 6 | SLJrtResourceGroups | Insert resource group records per operation |
| 7 | SLJrtSchs | Set Setuprgid + SchedDrv per operation |
| 8 | SLJobmatls | Add material lines (children linked to operations) |
| 9 | SLItemwhses | Link items to standard jobs via ItwhJob |

### Tool Inventory (16 Tools + 1 Agent)

| Tool | IDO | Pattern | Purpose |
|------|-----|---------|---------|
| ItemSearch | SLItems | GET | Search items by code/description |
| ItemInsert | SLItems | POST | Create items (batch up to 5) |
| JobSearch | SLJobs | GET | Search standard jobs |
| JobInsert | SLJobs | POST | Create standard job for an item |
| JobNumberLookup | SLHighKeys | GET | Look up next available BOM job number |
| RoutingSearch | SLJobRoutes | GET | Search routing operations |
| RoutingInsert | SLJobRoutes | POST | Add routing operations (batch per job) |
| MaterialSearch | SLJobmatls | GET | Search BOM materials |
| MaterialInsert | SLJobmatls | POST | Add materials to BOM (batch per job) |
| WorkCenterSearch | SLWcs | GET | Search work centers |
| ResourceGroupLookup | SLWcResourceGroups | GET | Look up valid Rgid per work center |
| ResourceGroupInsert | SLJrtResourceGroups | POST | Add resource group records |
| JrtSchsLoad | SLJrtSchs | GET | Load schedule records (get _ItemId) |
| SetuprgidUpdate | SLJrtSchs | POST | Set Setuprgid + SchedDrv per operation |
| ItemWhseLoad | SLItemwhses | GET | Load item-warehouse records (get _ItemId) |
| ItemWhseUpdate | SLItemwhses | POST | Link item to standard job via ItwhJob |

All tools follow the naming convention `GAF_SyteLine_<Capability>_Tool_v1` and are deployed on the Infor GenAI Platform.

## Dynamic Chunking

The Infor GenAI Platform enforces a ~240-second gateway timeout per agent response. Each tool call takes 20-50 seconds depending on complexity. The agent uses **dynamic chunking** to stay within limits:

- **Tool call budget:** ~5 calls per chunk
- **Weighted budgeting:** LIGHT tools (item/job operations) allow 4 calls/chunk; HEAVY tools (routing, resource groups, materials) drop to 3 calls/chunk
- **Checkpoint sentinels:** `<<CHECKPOINT>>` at each pause, `<<COMPLETE>>` when finished
- **Async chat pattern:** Uses `POST /chat` (fire-and-forget) + polling instead of `POST /chat/sync` to eliminate the gateway timeout entirely

For a typical 2-level BOM (3 jobs), expect ~5-6 chunks over ~15-18 minutes. A 5-level BOM (9 jobs) takes ~8 productive chunks.

## Validated Test Results

| Test | Levels | Jobs | Items | Chunks | Time | Checks |
|------|--------|------|-------|--------|------|--------|
| BH-T03000 Birdhouse | 2 | 3 | 12 | 5 | ~16 min | 25/27 |
| ST-10000 Stool (ad-hoc) | 2 | 4 | 9 | 8 | ~25 min | 16/16 |
| GK-T09000 Go-Kart | 2 (wide) | 4 | ~19 | 6 | ~18 min | 44/44 |
| ES-T10000 Electric Scooter | **5** | 9 | 33 | 8 (productive) | ~90 min | 113/126 |

The ES-T10000 stress test created a **5-level deep BOM** with two branches both reaching level 5, 9 standard jobs, and 33 items. The agent completed successfully on the platform despite 22 async API system errors during the test.

## Scripts

### Test Prompt Generator

**`scripts/generate_prompt.py`** — Generates unique, ready-to-use test prompts with dynamic job number allocation.

```bash
python generate_prompt.py                          # Random template
python generate_prompt.py --template chair         # Specific template
python generate_prompt.py --desc "custom product"  # Custom description
python generate_prompt.py --list                   # Show all 8 templates
python generate_prompt.py --dry-run                # Preview without incrementing
python generate_prompt.py | clip                   # Copy to clipboard (Windows)
```

**8 built-in templates:**

| Template | Complexity | Jobs | Description |
|----------|------------|------|-------------|
| birdhouse | Simple | 5 | Wooden birdhouse with body + roof sub-assemblies |
| stool | Simple | 5 | 4-legged wooden stool |
| chair | Moderate | 10 | Wooden chair with seat, backrest, legs |
| desk-lamp | Moderate | 10 | Desk lamp with base, arm, shade |
| bookshelf | Moderate | 10 | 3-shelf bookshelf with frame |
| workbench | Complex (2-level) | 20 | Steel workbench with drawer sub-assembly |
| bicycle | Complex (2-level) | 20 | Mountain bike with wheel + drivetrain |
| go-kart | Complex (3-level) | 20 | Go-kart with nested rear axle assembly |

Each run produces a unique item prefix (T01, T02, ...) and queries SLHighKeys for the next available BOM job number range.

### Automated Test Harness

**`scripts/test_bom_agent.py`** — Runs the BOM Generator Agent end-to-end using the async chat pattern.

```bash
python test_bom_agent.py --case simple -v          # Birdhouse BOM
python test_bom_agent.py --case moderate -v         # Chair BOM
python test_bom_agent.py --case complex -v          # Mountain bike BOM
python test_bom_agent.py --all -v                   # Run all test cases
python test_bom_agent.py --prompt "Custom BOM" -v   # Custom prompt
```

Features:
- Auto-generates unique prompts via `generate_prompt.py`
- Uses async chat (`POST /chat` + polling) to bypass the 240s gateway timeout
- Detects `<<CHECKPOINT>>` and `<<COMPLETE>>` sentinels to manage multi-turn conversations
- Pre-allocates non-overlapping job ranges for batch (`--all`) runs

### BOM Verification

**`scripts/verify_bom.py`** — Recursively walks a BOM tree and validates 7 checks per assembly node.

```bash
python verify_bom.py BH-T03000 --deep     # Recursive verification
python verify_bom.py ES-T10000 --json      # JSON output
```

| # | Check | IDO | Severity |
|---|-------|-----|----------|
| 1 | Item exists | SLItems | FAIL |
| 2 | Standard job exists | SLJobs | FAIL |
| 3 | ItwhJob linkage | SLItemwhses | FAIL |
| 4 | Routing operations exist | SLJobRoutes | FAIL |
| 5 | Resource group per operation | SLJrtResourceGroups | FAIL |
| 6 | Setuprgid per operation | SLJrtSchs | FAIL |
| 7 | Materials exist | SLJobmatls | WARN |

## Usage

### Ad-Hoc (GenAI Chat UI)

Simply type a natural language prompt in the Infor GenAI Chat interface:

```
Create a BOM for a wooden bookshelf with 3 shelves and a frame assembly.
Use warehouse MAIN.
```

The agent will automatically look up the next available BOM job number and create all records.

### Automated (via GAF_CLI)

```bash
# Generate a unique test prompt
cd BOMGenerator/scripts
python generate_prompt.py --template birdhouse

# Run the automated test
python test_bom_agent.py --case simple -v

# Verify the results
python verify_bom.py <ITEM_CODE> --deep
```

### Programmatic (import as module)

```python
from generate_prompt import generate, lookup_next_job_number

result = generate(template_name="chair")
print(result["prompt"])       # Ready-to-use prompt
print(result["item_code"])    # e.g., "CH-T05000"
print(result["job_range"])    # e.g., ("BOM0000010", "BOM0000019")
```

## Prerequisites

- **Infor CloudSuite Industrial (SyteLine)** — with IDO Request Service access
- **Infor GenAI Platform** — for agent and tool deployment
- **GAF_CLI** — Python CLI toolkit for publishing/managing GenAI assets (see `../GAF_CLI/`)
- **Python 3.8+** — for scripts
- **ION API credentials** — `.ionapi` file or `IONAPI_FILE` environment variable

## Project Structure

```
BOMGenerator/
  README.md                              # This file
  CLAUDE.md                              # Development knowledge base
  log.md                                 # Session-by-session progress log
  BillOfMaterialGenerator.txt            # Broader project vision
  specs/
    tools/                               # 16 tool JSON specs
      GAF_SyteLine_ItemSearch_Tool_v1.json
      GAF_SyteLine_ItemInsert_Tool_v1.json
      GAF_SyteLine_JobSearch_Tool_v1.json
      GAF_SyteLine_JobInsert_Tool_v1.json
      GAF_SyteLine_JobNumberLookup_Tool_v1.json
      GAF_SyteLine_RoutingSearch_Tool_v1.json
      GAF_SyteLine_RoutingInsert_Tool_v1.json
      GAF_SyteLine_MaterialSearch_Tool_v1.json
      GAF_SyteLine_MaterialInsert_Tool_v1.json
      GAF_SyteLine_WorkCenterSearch_Tool_v1.json
      GAF_SyteLine_ResourceGroupLookup_Tool_v1.json
      GAF_SyteLine_ResourceGroupInsert_Tool_v1.json
      GAF_SyteLine_JrtSchsLoad_Tool_v1.json
      GAF_SyteLine_SetuprgidUpdate_Tool_v1.json
      GAF_SyteLine_ItemWhseLoad_Tool_v1.json
      GAF_SyteLine_ItemWhseUpdate_Tool_v1.json
    agents/                              # 1 agent JSON spec
      GAF_SyteLine_BomGenerator_Agent_v1.json
  scripts/
    generate_prompt.py                   # Test prompt generator
    test_bom_agent.py                    # Automated test harness
    verify_bom.py                        # BOM verification (7 checks/assembly)
    discover_highkeys.py                 # SLHighKeys discovery script
    discover_itwhse_wcs.py               # ItwhJob + work center discovery
    discover_resource_groups.py          # Resource group investigation
    discover_resource_groups_v2.py       # Resource group investigation v2
    ido_field_discovery.py               # IDO field testing
  discovery/
    ido_discovery.md                     # IDO discovery documentation
  examples/
    FA-10000_CurrentMaterials.csv        # Example BOM materials export
    FA-10000_CurrentOperations.csv       # Example operations export
```

## Key Design Decisions

### 1 Tool = 1 API Call
The GenAI tool framework executes exactly one HTTP call per tool invocation. Two-step operations (GET then POST) are split into separate Load and Update tools.

### Anti-Hallucination Guards
LLMs invent plausible but invalid IDO properties and URL segments. Every tool spec includes explicit property lists and URL construction constraints. The agent workflow includes hard error classification to prevent false success reports.

### Dynamic Job Numbers
The agent can either use job numbers from the prompt (for reproducible tests) or look up the next available BOM-prefixed number from SLHighKeys at runtime (for ad-hoc use).

### Bottom-Up Construction
Items are created leaf-first, then sub-assemblies, then top-level. This ensures all referenced items exist before being added as materials.

## Future Work

- True 3-level BOM validation (template fixed, pending re-test)
- Transactional data generation (sales orders, service orders)
- MRP/planning validation (run planning, verify suggested jobs/POs)
- Image-to-BOM capability
- Duplicate material prevention during error recovery
