# Infor OS Automation & Demo Projects

> **Note**: The public version of this repository is at [MarcelloAtInfor/InforOS-Automation-Toolkit](https://github.com/MarcelloAtInfor/InforOS-Automation-Toolkit). This private repo is the active working copy with credentials and tenant-specific configuration. Push sanitized updates to the public repo periodically via `git archive`.

A collection of independent but related projects demonstrating automation capabilities on the **Infor OS** (Operating System) platform, targeting **Infor CloudSuite Industrial (SyteLine)**.

Each project uses different combinations of Infor platform services — GenAI agents, RPA workflows, Intelligent Document Processing (IDP), ION integration, and Document Management (IDM) — to automate manufacturing and supply chain operations.

---

## Repository Structure

```
CC_OS_Project/
├── BOMGenerator/              # GenAI agent: natural language → multi-level BOMs in SyteLine
├── CSIPOAssetCreationTool/    # Invoice automation: GenAI + RPA + IDP → vendor/item/PO creation
├── GAF_CLI/                   # GenAI Agent Factory CLI: publish, manage, invoke GenAI tools & agents
├── shared/                    # Centralized OAuth 2.0 auth & config (used by all projects)
├── .claude/                   # Claude Code slash commands & agent definitions
├── CLAUDE.md                  # Claude Code project instructions (AI assistant context)
├── README.md                  # This file
└── log.md                     # Root-level progress log across all projects
```

---

## Projects

### BOMGenerator

**What it does**: A GenAI agent that creates realistic multi-level **Bill of Material (BOM)** data in SyteLine from natural language prompts. You describe what you want ("Create a 3-level BOM for a mountain bike") and the agent creates all items, standard jobs, routing operations, resource groups, and material structures directly in the live ERP system.

**Technology stack**:
- 16 GenAI tools + 1 orchestrating agent deployed on the Infor GenAI platform
- Tools interact with SyteLine via IDO REST APIs (SLItems, SLJobs, SLJobRoutes, SLJobmatls, etc.)
- Automated test harness with prompt generation, async agent invocation, and BOM verification
- Dynamic chunking with weighted tool-call budgeting to stay within platform timeout limits

**Key components**:

| Folder | Contents |
|--------|----------|
| `specs/tools/` | 16 GenAI tool JSON specs (ItemSearch, ItemInsert, JobInsert, RoutingInsert, MaterialInsert, ResourceGroupLookup, etc.) |
| `specs/agents/` | 1 GenAI agent spec that orchestrates all 16 tools in an 8-step workflow |
| `scripts/generate_prompt.py` | Test prompt generator with 8 built-in templates (birdhouse to go-kart) |
| `scripts/test_bom_agent.py` | Automated multi-turn test harness using async chat pattern |
| `scripts/verify_bom.py` | Recursive BOM tree validator (7 checks per assembly node) |
| `scripts/discover_*.py` | IDO discovery scripts used during development |
| `discovery/` | IDO discovery documentation |

**Status**: Operational. Validated up to 5-level deep BOMs (33 items, 9 standard jobs). See `BOMGenerator/CLAUDE.md` for full architecture and test results.

---

### CSIPOAssetCreationTool

**What it does**: An end-to-end **invoice automation** system. RPA bots pick up invoice documents, IDP extracts structured data, and a GenAI agent creates or matches vendors, items, and purchase orders in SyteLine — automating what would otherwise be manual data entry.

**Technology stack**:
- GenAI agents and tools on the Infor GenAI platform (Claude 4.5 Sonnet)
- Infor RPA Studio workflows (XAML)
- Infor Document Processor (IDP) for AI-powered data extraction
- ION workflows for event-driven orchestration
- IDM for document storage and retrieval

**Key components**:

| Folder | Contents |
|--------|----------|
| `Agents&Tools/` | GenAI agent/tool development — InvoiceAutomation_Agent_v2 (7 tools), CustomerSearch, UpdateOrderLineDates |
| `RPA/` | 25+ RPA workflow projects — DemoInvoiceLoader is the GenAI integration reference project |
| `IDP/` | Document Processor flow management scripts, DPF analysis, V1 vs V2 comparison |
| `ION/` | ION workflow definitions, API documentation, Pulse alert patterns |
| `IDM/` | Document Management API patterns and integration guide |

**Cross-project data flow**:
```
Invoice Document
  → IDM (document storage)
  → IDP (AI data extraction: vendor, items, prices, quantities)
  → RPA (orchestration: pick up document, call IDP, call GenAI agent)
  → GenAI Agent (business logic: match/create vendor, items, PO in SyteLine)
  → ION (notifications, workflow triggers)
```

**Status**: v1.0 shipped (2026-02-03). See `CSIPOAssetCreationTool/CLAUDE.md` for full project documentation.

---

### shared

**What it does**: Centralized Python module for **OAuth 2.0 authentication** and **Infor OS service URL construction**. Both projects import from this module to authenticate API calls.

**Contents** (~250 lines total):

| File | Purpose |
|------|---------|
| `auth.py` | OAuth 2.0 token generation (password grant), token loading, auth header construction |
| `config.py` | Tenant ID lookup, base URL construction, service-specific URL builders |
| `__init__.py` | Public API — exports all functions and constants |

**Service URLs provided**:
- `IDO_URL()` — SyteLine data operations (`/CSI/IDORequestService/ido`)
- `GENAI_CORE_URL()` — GenAI tool/agent management (`/GENAI/coresvc`)
- `GENAI_CHAT_URL()` — GenAI agent execution (`/GENAI/chatsvc`)
- `IDP_URL()` — Document processing (`/COLEMANDDP/iddpuisvc`)

**Usage from any project script**:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # repo root

from shared.auth import get_auth_headers
from shared.config import IDO_URL

headers = get_auth_headers()  # Auto-fetches and caches OAuth token
# Now make API calls with headers
```

See `shared/CLAUDE.md` for the complete API reference.

---

## .claude — Claude Code Configuration

The `.claude/` directory contains slash commands and agent definitions for **Claude Code** (Anthropic's AI coding assistant). These provide domain-specific automation shortcuts for working with this repository.

**Commands** (invoke via `/command-name` in Claude Code):

| Command | Purpose |
|---------|---------|
| `/deploy-genai-asset` | Deploy a GenAI tool or agent to the Infor platform |
| `/list-genai-assets` | List deployed GenAI tools and agents |
| `/query-ido` | Quick IDO data query against SyteLine |
| `/ido-lookup` | IDO property discovery (find fields, tables, writability) |
| `/ido-update` | SyteLine record insert/update/delete |
| `/infor-auth` | Generate and manage ION API OAuth tokens |
| `/send-pulse` | Send ION Pulse notifications |
| `/rpa-snippet` | Generate RPA XAML workflow snippets |

**Agent definitions** (specialized Claude Code behaviors):

| Agent | Purpose |
|-------|---------|
| `infor-tool-builder` | Guide for creating new GenAI tool specs |
| `infor-agent-builder` | Guide for creating new GenAI agent specs |
| `idp-flow-manager` | IDP Document Processor flow management |
| `ion-workflow-builder` | ION workflow creation assistance |

---

## Getting Started

### Prerequisites

- **Python 3.9+** with `requests` package
- **Infor OS tenant** with CloudSuite Industrial (SyteLine) configured
- **ION API credentials** (`.ionapi` file) — obtained from Infor OS Portal:
  1. Navigate to **API Gateway > Authorized Apps > Backend Service**
  2. Create a service account and download the `.ionapi` credentials file

### Setup

1. **Clone the repo** and place your `.ionapi` file in the repo root (gitignored by default)

2. **Run the interactive setup**:
   ```bash
   python setup.py
   ```
   This will:
   - Validate your `.ionapi` credentials and test connectivity
   - Discover available SyteLine sites
   - Optionally resolve approver users (email → IFS GUID)
   - Optionally extract a service account token from an exported ION workflow
   - Write a `tenant_config.json` file (gitignored) that all projects read from

3. **Verify**:
   ```bash
   python -c "from shared.tenant import get_site; print(get_site())"
   ```

See `tenant_config.example.json` for the expected config structure.

### Authentication

All projects use OAuth 2.0 (password grant) via the centralized `shared/` module. Tokens are auto-fetched and cached — no manual token management required.

```python
from shared.auth import get_auth_headers
headers = get_auth_headers()  # Auto-fetches and caches OAuth token
```

---

### GAF_CLI

**What it does**: A Python CLI toolkit for creating, managing, and invoking Infor OS **GenAI tools and agents** programmatically. Implements a self-referential system where the Factory Agent can create and manage its own tools. Used by BOMGenerator and CSIPOAssetCreationTool for publishing specs to the GenAI platform.

**Technology stack**:
- 6 CLI commands: validate, publish (tool/agent), update, list, invoke
- GenAI API client with sync and async chat support
- Spec validation engine (~600 lines, type-specific checks)
- HTTP client with exponential backoff retry
- Credential redaction logging

**Key components**:

| Folder | Contents |
|--------|----------|
| `src/cli/` | 6 CLI commands (validate_spec, publish_tool, publish_agent, update_asset, list_assets, invoke_agent) |
| `src/infor_os/` | GenAI API client (sync/async chat, tool CRUD, session management) |
| `src/shared/` | Auth, config, validation, errors, HTTP client, logging (separate from root `shared/`) |
| `specs/tools/` | 6 Factory tool JSON specs |
| `specs/agents/` | 1 Factory Agent spec |

**Key operations** (run from `GAF_CLI/` directory):
```bash
python -m src.cli.validate_spec path/to/spec.json    # Validate before publishing
python -m src.cli.publish_tool path/to/tool.json      # Publish new tool
python -m src.cli.publish_agent path/to/agent.json    # Publish new agent
python -m src.cli.update_asset path/to/spec.json      # Update existing (requires "guid" in spec)
python -m src.cli.invoke_agent "prompt" --json         # Invoke an agent
python -m src.cli.invoke_agent "prompt" --async        # Async mode (long-running agents)
```

**Status**: Stable. See `GAF_CLI/CLAUDE.md` for full documentation.

---

## Documentation Convention

Each project and subfolder maintains two documentation files:

- **`CLAUDE.md`** — Knowledge base: architecture, API patterns, key discoveries, lessons learned. Read this first when working in any folder.
- **`log.md`** — Running history: session-by-session progress log with dates, decisions, and test results.

These files are the primary source of truth for project context. They are updated continuously during development to preserve knowledge across sessions.
