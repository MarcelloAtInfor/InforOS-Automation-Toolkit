# CSI PO Asset Creation Tool

An end-to-end **invoice automation system** for **Infor CloudSuite Industrial (SyteLine)** that combines RPA, GenAI, and Intelligent Document Processing to automatically process vendor invoices â€” extracting data from PDFs and creating vendors, items, and purchase orders directly in the ERP system. No manual data entry required.

**v1.0 shipped February 2026** with price handling, item sourcing, and debug capabilities.

## How It Works

```
Invoice PDF arrives
        |
        v
+-------------------+       +-------------------+       +-------------------+
|   Infor RPA       |  -->  |   Infor IDP       |  -->  |   Infor GenAI     |
|   (Orchestrator)  |       |   (Extraction)    |       |   (Processing)    |
+-------------------+       +-------------------+       +-------------------+
  Watches folder,             AI-powered OCR,             Agent with 9 tools
  manages flow,               extracts vendor,            creates/links all
  sends notifications         line items, prices          SyteLine records
        |                                                        |
        v                                                        v
+-------------------+                                  +-------------------+
|   File Management |                                  |   SyteLine ERP    |
+-------------------+                                  +-------------------+
  Success/Failure                                        Vendors, Items,
  folder routing                                         POs, PO Lines
```

### Processing Pipeline

1. **RPA watches** a folder for incoming invoice PDFs
2. **IDP extracts** vendor info, line items, quantities, and unit prices using AI/ML
3. **RPA formats** the extracted data into a structured JSON payload
4. **GenAI agent** receives the payload and executes a multi-step workflow:
   - Searches for existing vendor (avoids duplicates)
   - Creates vendor if new (with address, phone, terms)
   - Searches for existing items (avoids duplicates)
   - Creates items if new (with pricing and sourcing)
   - Creates purchase order linked to vendor
   - Creates PO line items in batch
   - Triggers AI model retraining for vendor/item similarity
5. **RPA moves** the processed file to success/failure folder
6. **Pulse notification** sent with results summary

## Architecture

This project integrates five Infor platform services:

| Component | Service | Role |
|-----------|---------|------|
| **Agents&Tools** | Infor GenAI Platform | AI agents and API tools for SyteLine data operations |
| **RPA** | Infor RPA Studio | Workflow orchestration, file handling, notifications |
| **IDP** | Infor Document Processor | AI-powered invoice data extraction |
| **ION** | Infor Operating Network | Workflow automation, Pulse alerts, API middleware |
| **IDM** | Infor Document Management | Document storage and entity attachment |

### GenAI Agent: InvoiceAutomation_Agent_v2

The core processing engine â€” a GenAI agent orchestrating 9 tools:

| Tool | IDO | Purpose |
|------|-----|---------|
| VendorSearch_Tool_v2 | SLVendors | Search vendors by name/number |
| VendorInsert_Tool_v2 | SLVendors | Create vendor with address, phone, terms |
| ItemSearch_Tool_v2 | SLItems | Search items by code/description |
| ItemInsert_Tool_v2 | SLItems | Create item with CurMatCost + Source="P" |
| PoSearch_Tool_v2 | SLPOs | Search existing purchase orders |
| PoInsert_Tool_v2 | SLPOs | Create purchase order linked to vendor |
| PoLineInsert_Tool_v2 | SLPoItems | Create PO line items in batch |
| StartItemSimilarityWorkflow | ION | Trigger AI model retraining for items |
| StartVendorNameSimilarityWorkflow | ION | Trigger AI model retraining for vendors |

**Agent workflow:** Vendor lookup/creation -> Item lookup/creation -> PO creation -> PO line creation -> AI retraining

### Other Deployed Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| CustomerSearch_Agent | Search SyteLine customers by name/number | 1 |
| UpdateOrderLineDates_Agent_v2 | Batch update 20+ order line due dates to previous Sunday | 2 |

### RPA: DemoInvoiceLoader

The orchestration layer â€” 6 XAML workflows built in Infor RPA Studio:

| Workflow | Purpose |
|----------|---------|
| `MainPage.xaml` | Entry point â€” folder watch, file iteration, argument configuration |
| `ExtractOCRData.xaml` | IDP document processing trigger and OCR data extraction |
| `FormatDataForGenAI.xaml` | Transform extracted data into structured JSON for the GenAI agent |
| `SendToGenAIAgent.xaml` | Call GenAI agent via ION API and handle response |
| `ParseAgentResponse.xaml` | Parse agent response to extract PO number, status, errors |
| `MoveFileToSuccessFailure.xaml` | Route processed files to success/failure folders |

Additional supporting workflows for notifications and error handling.

**Features:**
- Configurable arguments with defaults for end-user scheduling
- `enableDebugMode` flag opens PowerShell window tailing the log file
- 25+ sample invoice generators for testing
- 25+ additional RPA projects in `PAST_PROJECTS/` for reference

### IDP: Document Processor Flows

AI-powered extraction using Infor Document Processor:

- **CSI_APInvoice_Extract_V2** â€” production DPF with 27 fields and 13 line item columns
- Python scripts for DPF management: list, export, import, create
- V1 vs V2 analysis documented (V2 recommended â€” created via UI for reliability)

### ION: Workflow Automation & Pulse Alerts

Integration middleware scripts and workflow definitions:

- **Pulse alerts** â€” send alerts, notifications, and tasks with details trees
- **Workflow management** â€” create, activate, start workflow instances via API
- **RPA Invoice Notification** â€” dedicated workflow with drillback links
- 6 workflow definitions for reference

### IDM: Document Management

Document storage integration (used by RPA for invoice PDF management):

- REST API for upload, download, search, and entity attachment
- Integrated across RPA workflows for document lifecycle management

## Tech Stack

| Technology | Version/Details |
|------------|----------------|
| Infor CloudSuite Industrial (SyteLine) | ERP backend via ION API |
| Infor GenAI Platform | Claude Sonnet 4.5 model |
| Infor RPA Studio | XAML workflow engine |
| Infor Document Processor (IDP) | AI/ML document extraction |
| Infor ION | API middleware + Pulse notifications |
| Python | Scripts for tool deployment, token management, IDP automation |
| OAuth 2.0 | Password grant with saak/sask credentials, 2-hour token expiry |

## Key Technical Discoveries

### IDO Metadata Discovery

SyteLine IDOs join 10-20+ tables but only write to their primary table. Updates to properties on joined tables return success (200 OK) but silently discard values. Use the system metadata IDOs to diagnose:

- **`IdoCollections`** â€” look up IDO by name
- **`IdoTables`** â€” find tables joined by IDO (`TableType=3` = primary/writable)
- **`IdoProperties`** â€” map property to underlying column and table

### api_docs Formatting

The GenAI LLM is extremely sensitive to whitespace in tool specs. A single blank line after `Headers:` in api_docs causes URL malformation and 404 errors.

### Multi-Tenant Support

Tools use `<site>` placeholder instead of hardcoded tenant values. The agent extracts the site value from input at runtime and passes it to all tool calls, enabling the same tools/agents to work across multiple tenants.

### IDO Naming

IDO names are case-sensitive: `SLPOs` (not `SLPos`), `SLItems`, `SLVendors`, `SLPoItems`.

## Project Structure

```
CSIPOAssetCreationTool/
  README.md                              # This file
  CLAUDE.md                              # Development knowledge base
  log.md                                 # Session-by-session progress log
  .planning/
    PROJECT.md                           # Requirements and key decisions
  Agents&Tools/
    CLAUDE.md                            # GenAI architecture and API docs
    log.md                               # Agent/tool development history
    scripts/
      create_invoice_agent_v2.py         # Invoice agent deployment
      create_invoice_insert_tools_v2.py  # Insert tool deployment
      create_invoice_search_tools_v2.py  # Search tool deployment
      create_orderline_agent.py          # Order line agent deployment
      create_orderline_tools.py          # Order line tool deployment
      ...
    APIs/
      GenAiCoreService.json              # GenAI Core API spec
      GenAiChatService.json              # GenAI Chat API spec
      SyteLineRESTv2.json               # SyteLine REST API spec
      IONProcessApplicationService.json  # ION API spec
      ...
    docs/
      Invoice_Agent_v2_Fixes.md          # Agent fix documentation
      Invoice_Payload_Optimization.md    # Payload optimization notes
      OAuth_Token_Authentication.md      # Auth documentation
      PurchaseOrderReceiving.json        # PO receiving API spec
  RPA/
    CLAUDE.md                            # RPA architecture and XAML rules
    log.md                               # RPA development history
    DemoInvoiceLoader/                   # Main invoice automation project
      MainPage.xaml                      # Entry point workflow
      ExtractOCRData.xaml                # IDP extraction
      FormatDataForGenAI.xaml            # Data formatting
      SendToGenAIAgent.xaml              # GenAI agent call
      ParseAgentResponse.xaml            # Response parsing
      MoveFileToSuccessFailure.xaml      # File routing
      generate_*.py                      # Test invoice generators
      Documents/                         # Sample invoices
    DOCs/
      RPA_Activities_Reference.md        # Activity catalog (from 298-page guide)
    PAST_PROJECTS/                       # 25+ reference RPA projects
  IDP/
    CLAUDE.md                            # IDP API docs and DPF best practices
    log.md                               # IDP development history
    scripts/                             # DPF management scripts
    API_DOCs/                            # IDP API spec
    configs/                             # DPF configurations
    exports/                             # Exported DPF definitions
  ION/
    CLAUDE.md                            # ION API patterns and Pulse reference
    log.md                               # ION development history
    scripts/                             # Pulse alerts, workflow management
    APIs/                                # ION API specs
    workflow_definitions/                # Downloaded workflow definitions
  IDM/
    CLAUDE.md                            # IDM API patterns
    log.md                               # IDM development history
```

## Prerequisites

- **Infor CloudSuite Industrial (SyteLine)** â€” with IDO Request Service access
- **Infor GenAI Platform** â€” for agent and tool hosting
- **Infor RPA Studio** â€” for workflow editing and deployment
- **Infor IDP** â€” for document processor flow configuration
- **Python 3.8+** â€” for deployment scripts and utilities
- **ION API credentials** â€” `.ionapi` file with saak/sask service account keys

## Authentication

All components use centralized OAuth 2.0 via the shared module at the repository root:

```bash
# Generate a new token (2-hour expiry)
python -m shared.auth CSIPOAssetCreationTool/Agents&Tools/scripts
python -m shared.auth CSIPOAssetCreationTool/IDP/scripts
python -m shared.auth CSIPOAssetCreationTool/ION/scripts
```

## Deployment

### GenAI Tools and Agents

Tools and agents are deployed via Python scripts using the GenAI Core Service API:

```bash
cd CSIPOAssetCreationTool/Agents&Tools/scripts

# Deploy invoice processing tools
python create_invoice_search_tools_v2.py
python create_invoice_insert_tools_v2.py

# Deploy the invoice automation agent
python create_invoice_agent_v2.py
```

Or use the GAF_CLI toolkit (at `../GAF_CLI/`) for spec-based publishing.

### RPA Workflows

1. Open `RPA/DemoInvoiceLoader/` in Infor RPA Studio
2. Configure arguments (input folder path, tenant, credentials)
3. Deploy to target Infor Cloud Suite environment via Studio

## Cross-Project Integration

```
                    +------------------+
                    |   Invoice PDF    |
                    +------------------+
                            |
              +-------------+-------------+
              |                           |
     +--------v--------+       +---------v--------+
     |      RPA         |       |      IDM          |
     |  (Orchestrator)  |<----->|  (Doc Storage)    |
     +--------+---------+       +------------------+
              |
     +--------v--------+
     |      IDP         |
     |  (AI Extraction) |
     +--------+---------+
              |
     +--------v--------+       +------------------+
     | Agents&Tools     |       |      ION          |
     | (GenAI Agent)    |------>|  (Workflows +     |
     +--------+---------+       |   Pulse Alerts)   |
              |                 +------------------+
     +--------v--------+
     |    SyteLine      |
     |  (ERP System)    |
     +------------------+
```

## Future Work

- PO receiving automation (stored procedure integration)
- Expanded IDP flows for additional document types
- IDM direct integration for automated document archival
- Multi-tenant deployment across additional SyteLine environments


## Agent-Agnostic Usage (Claude + Codex)

This folder is designed to work with both Claude Code and Codex.

Shared guide:
- AGENT_GUIDE.md

Agent adapter files:
- AGENTS.md (Codex)
- CLAUDE.md (Claude)

Read order:
1. AGENT_GUIDE.md
2. CLAUDE.md
3. log.md


