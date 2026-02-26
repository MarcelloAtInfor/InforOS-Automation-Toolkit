# CSIPOAssetCreationTool - CLAUDE.md

## Project Overview

**Invoice Automation Enhancement** — GenAI-powered invoice automation system that processes invoices via RPA, extracts data with IDP, and creates vendors/items/POs in SyteLine. v1.0 shipped 2026-02-03 with price handling, proper item sourcing, and debugging capabilities.

See `.planning/PROJECT.md` for full requirements and key decisions.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Project Structure

### Agents&Tools/
**Purpose**: Infor GenAI platform development - creating AI agents and API tools programmatically

**Technology**: REST APIs, Python scripts, JSON configuration
- GenAI Tools: API wrappers that call Infor Cloud Suite endpoints
- GenAI Agents: AI orchestrators that use multiple tools
- OAuth 2.0 authentication with 2-hour token expiry
- Claude 4.5 Sonnet model integration

**Status**: Most mature and actively developed. Production-ready components available.

**Completed Implementations**:
- CustomerSearch_Agent - Search customers by name/number
- UpdateOrderLineDates_Agent_v2 - Batch update 20+ order line due dates (weekly automation)
- InvoiceAutomation_Agent_v2 - 7 tools for end-to-end invoice processing (vendor/item/PO creation)

**Key Discoveries Documented**:
- OAuth 2.0 password grant with saak/sask (not client_credentials)
- IDO naming case-sensitivity (SLPOs not SLPos)
- SyteLine update format (IDOName/Changes structure)
- **Tools cannot be invoked directly** — only agents can call tools
- Tool api_docs formatting for reliable LLM parsing
- Dynamic site configuration for multi-tenant support (`<site>` placeholder)

**Key Files**:
- `Agents&Tools/CLAUDE.md` - Complete API documentation and architecture
- `Agents&Tools/log.md` - Detailed progress log with discoveries and solutions
- `Agents&Tools/scripts/*.py` - Token generation and API interaction scripts

### RPA/
**Purpose**: Infor RPA Studio automation workflows for business process automation

**Technology**: XAML workflow files, Infor RPA Studio, VBScript expressions
- 25+ independent RPA projects
- Document processing, invoice handling, email automation
- Multi-tenant deployments across Infor Cloud Suite environments
- Integration with ION API, IDM, Data Lake, Office 365

**Status**: Established collection with active development. Comprehensive documentation including XAML syntax rules.

**Recent Development**:
- DemoInvoiceLoader project - End-to-end GenAI agent integration
  - 6 XAML workflow files (OCR extraction, GenAI agent call, file management)
  - Configurable arguments with defaults for end-user scheduling
  - Multiple bug fixes (ContinueOnError patterns, path detection, polling optimization)
- RPA_Activities_Reference.md - Comprehensive activity catalog from 298-page user guide

**Key Discoveries Documented**:
- XAML syntax rules (no XML comments, VBScript brackets, ViewStateData requirements)
- ContinueOnError best practices (which activities need True vs False)
- Argument default values pattern (set on Activity element, not in x:Members)
- Two OCR options: DocumentOC (simple) vs ExtractDataActivity (requires IDP flow)

**Key Files**:
- `RPA/CLAUDE.md` - Architectural guide with XAML syntax rules
- `RPA/DOCs/RPA_Activities_Reference.md` - Activity catalog and best practices
- `RPA/DemoInvoiceLoader/` - GenAI integration reference project

### ION/
**Purpose**: Infor ION workflow definitions and API documentation

**Technology**: ION workflows, API specifications
- Process application services (workflow instances, Pulse alerts)
- Scripting model APIs
- Process model definitions

**Status**: Documentation repository. CLAUDE.md created with API patterns.

**Key Details**:
- API throttling: 10 calls per 10 seconds (429 if exceeded)
- Date format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)
- Integration patterns documented for RPA + ION and GenAI + ION

**Key Files**:
- `ION/CLAUDE.md` - API patterns and integration guide
- `ION/API_DOCS/*.json` - ION API specifications (Process, Model, Scripting)

### IDM/
**Purpose**: Infor Document Management configurations or integrations

**Technology**: REST APIs for document upload, download, search, and entity attachment

**Status**: Documentation created. Awaiting first implementation.

**Key Details**:
- API patterns documented from RPA integration examples
- Common patterns: Upload & Attach, Search & Process, Document Retrieval for AI
- Uses same OAuth 2.0 authentication as other Infor APIs

**Key Files**:
- `IDM/CLAUDE.md` - API patterns and integration guide

### IDP/
**Purpose**: Infor Document Processor - AI-powered intelligent document processing

**Technology**: REST APIs, Document Processor Flows (DPF), AI/ML extraction
- Automates data extraction from unstructured documents (invoices, POs, etc.)
- Document Processor Flow management via API
- Time-to-Value (T2V) tag configuration
- Export/Import DPF configurations between environments

**Status**: Active development. Scripts created, DPF analysis complete.

**Completed**:
- Python scripts: get_idp_token, list_dpfs, get_dpf_details, export_dpf, import_dpf, create_ap_invoice_from_template
- V1 vs V2 DPF comparison analysis
- Best practices documented for creating working DPFs

**Key Discoveries**:
- Working DPF requires: Document Classification activity + "Other" class + promptStructure=1
- API-created DPFs (V1) had issues; UI-created (V2) work reliably
- Recommended DPF: CSI_APInvoice_Extract_V2 (27 fields, 13 line item columns)

**Key Files**:
- `IDP/CLAUDE.md` - API documentation, DPF best practices, V1 vs V2 comparison
- `IDP/scripts/*.py` - DPF management automation
- `IDP/API_DOCs/IDDPUIService.json` - IDP UI Service Swagger spec

### DemoVideo/
**Purpose**: Python pipeline to produce a ~2 minute demo video showcasing the end-to-end invoice automation pipeline.

**Technology**: Pillow (slide generation), ElevenLabs (TTS voiceover), MoviePy v2 (video assembly)
- Config-driven from `video_script.json` — edit JSON to change content/timing
- 4 Pillow slide templates: title_card, architecture_diagram, screenshot_frame, closing_card
- 8 sections: opening hook, architecture diagram, 5 demo steps, closing metrics
- Placeholder screenshot system — full pipeline works before real screenshots exist

**Status**: Phase 1 complete (scaffolding + slides). Phases 2-5 pending (voice, audio, video, screenshots).

**Key Files**:
- `DemoVideo/CLAUDE.md` - Full documentation and phase status
- `DemoVideo/config/video_script.json` - Master config (slides, narration, timing)
- `DemoVideo/scripts/01_generate_slides.py` - Slide renderer
- `DemoVideo/scripts/05_build_all.py` - Full pipeline orchestrator

## Cross-Project Relationships

Projects within CSIPOAssetCreationTool reference or complement each other:
- **RPA → Agents&Tools**: RPA workflows call GenAI agents for AI-powered processing
- **RPA → ION**: RPA may trigger or be triggered by ION workflows
- **RPA → IDM**: RPA workflows upload/download documents via IDM
- **Agents&Tools → ION API**: GenAI tools call Infor Cloud Suite via ION API
- **IDP → IDM**: IDP processes documents stored in IDM
- **RPA → IDP**: RPA workflows can trigger IDP for document processing
- **Agents&Tools → IDP**: GenAI agents can orchestrate IDP workflows

When working in one area, be aware of potential integration points with other areas.

## Common Integration Patterns

### Infor Platform Authentication

All CSI projects use the centralized `shared/` module at the repository root for authentication:
- Token expires after 2 hours
- Uses password grant type (not client_credentials)
- Service account keys: `saak` (username) and `sask` (password)
- Credentials stored in: `shared/<your-credentials>.ionapi` (at repo root)

**Token Generation** (from repo root):
```bash
python -m shared.auth CSIPOAssetCreationTool/Agents&Tools/scripts   # For Agents&Tools scripts
python -m shared.auth CSIPOAssetCreationTool/IDP/scripts            # For IDP scripts
```

**Using in Scripts** (import pattern for CSI scripts):
```python
import sys
from pathlib import Path

# Navigate up to repo root (adjust depth based on script location)
# From CSIPOAssetCreationTool/<subfolder>/scripts/:
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.auth import get_auth_headers, request_token
from shared.config import GENAI_CORE_URL, IDO_URL, IDP_URL

headers = get_auth_headers()
url = f"{GENAI_CORE_URL()}/api/v1/tools"
```

### Infor Cloud Suite Multi-Tenant

Projects target tenant: `<YOUR_TENANT>`
- Base URL: `https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>`
- UI: `https://mingle-portal.inforcloudsuite.com/<YOUR_TENANT>`

### IDO Collections (SyteLine)

When working with Infor CloudSuite Industrial data:
- IDO names are case-sensitive (e.g., `SLPOs` not `SLPos`)
- Common IDOs: `SLVendors`, `SLItems`, `SLPOs`, `SLCoitems`, `SLPoItems`
- Operations: `/load/{ido}` (query), `/update/{ido}` (insert/update/delete)

### IDO Metadata Discovery (CRITICAL TECHNIQUE)

**NEVER conclude that a field cannot be written via API without first querying the IDO metadata system IDOs.** SyteLine IDOs often join 10-20+ tables but can only write to their primary table. A property update may return success (200 OK) but silently discard the value because the column lives on a joined table, not the primary one.

**System Metadata IDOs** (queryable via `/load/{ido}` like any business data):
- **`IdoCollections`** — Look up IDO by name (server assembly, extension class)
- **`IdoTables`** — Find which tables an IDO joins. `TableType=3` = primary (writable) table. Joined tables (`TableType=0`) are read-only even if properties show `ReadOnly=False`
- **`IdoProperties`** — Map a property name to its underlying column and table. Reveals which table alias a property writes to

**When a write fails silently**: Query `IdoProperties` to find the table, then query `IdoTables` with `TableType=3` to find the IDO that owns that table as primary. Write through THAT IDO instead.

**See `Agents&Tools/CLAUDE.md` → "IDO Metadata Discovery via System IDOs"** for the full step-by-step workflow with examples.

## GAF_CLI

GAF_CLI (GenAI Agent Factory CLI) is used for publishing tools and agents. It lives at `../GAF_CLI` (sibling directory at repo root). See the root repository `CLAUDE.md` for full GAF_CLI documentation and commands.
