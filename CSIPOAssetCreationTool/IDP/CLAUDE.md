# IDP (Infor Document Processor)

This folder contains API documentation and development resources for Infor Document Processor (IDP), an AI-powered intelligent document processing solution.

## Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.** Infor OS is NOT a typical local development stack - there is no local runtime, domain knowledge gaps cause frequent errors, and only the user can validate results in the live environment. Do NOT batch multiple phases together. After each phase: summarize what was done, what needs testing, and WAIT for user confirmation before continuing. See root `CLAUDE.md` for full details.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Purpose

Infor Document Processor automates the extraction of data from unstructured documents (invoices, purchase orders, etc.) using AI/ML capabilities. This folder supports:
- API integration development
- Document Processor Flow (DPF) configuration management
- Automation scripts for IDP operations

## API Overview

### Base URL
```
https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/COLEMANDDP/iddpuisvc
```

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ui/v{ver}/DocumentProcessorFlows/List` | POST | List all Document Processor Flows |
| `/ui/v{ver}/DocumentProcessorFlows/{guid}` | GET | Get specific DPF by GUID |
| `/ui/v{ver}/ExportDPF` | POST | Export DPF configurations |
| `/ui/v{ver}/ImportDPF` | POST | Import DPF configurations (multipart/form-data) |
| `/t2v/v1/GetT2VTags` | POST | Get Time-to-Value tags |
| `/t2v/v1/GetTagResources` | POST | Get resources associated with a tag |

### Request Patterns

**GridFilters** (for listing/filtering):
```json
{
  "currentPage": 1,
  "pageSize": 100,
  "sortColumn": "columnName",
  "sortDirection": "ASC",
  "reqFilterExpression": [
    {
      "columnId": "fieldName",
      "filterOperator": "equals",
      "value": "filterValue",
      "filterType": "string"
    }
  ]
}
```

**DPF Export Request**:
```json
[
  { "dpfGuid": "guid-here" }
]
```

## Authentication

Uses the centralized `shared/` module for OAuth 2.0 authentication.

**Token Generation**:
```bash
# From repo root
python -m shared.auth IDP/scripts
```

**Using in Scripts**:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.auth import get_auth_headers
from shared.config import IDP_URL

headers = get_auth_headers()
url = f"{IDP_URL()}/ui/v1/DocumentProcessorFlows/List"
```

**Quick Reference**:
- OAuth 2.0 password grant type
- Service account keys: `saak` (username), `sask` (password)
- Token expiry: 2 hours
- Credentials: your `.ionapi` file (see repo root setup)

## Folder Structure

```
IDP/
├── CLAUDE.md           # This file
├── log.md              # Progress tracking
├── API_DOCs/           # API specifications
│   └── IDDPUIService.json   # IDP UI Service Swagger spec
├── scripts/            # Automation scripts
│   ├── get_idp_token.py     # OAuth token generation
│   ├── list_dpfs.py         # List all DPFs
│   ├── get_dpf_details.py   # Get DPF by GUID
│   ├── export_dpf.py        # Export DPF config
│   ├── import_dpf.py        # Import DPF config
│   └── create_ap_invoice_from_template.py  # Generate new DPF
├── exports/            # Exported DPF backups
│   ├── CSI_APInvoice_Extract_V2.json   # New prompt structure template
│   ├── CSI_APInvoice_Extract_V3.json   # Old prompt structure template (RPA compatible)
│   ├── CSI_APInvoice_Extract_V1.json   # Legacy (deprecated)
│   └── dpf_list.json                   # Current DPF inventory
└── configs/            # DPF configurations for import
    └── AP_Invoice_Extract_v3.json
```

## Available DPFs

### CSI_APInvoice_Extract_V2 (New Prompt Structure)
**GUID**: `d6635c5e-b1be-410f-afda-c5ee7cc59663`
**Purpose**: AP Invoice extraction - Full-featured, UI-created version
**Status**: Active, Working
**Prompt Structure**: `1` (New)
**RPA Compatible**: No - RPA doesn't support new prompt structure

**Features**:
- Document Classification + Entity Classification activities (2 activities)
- 27 entity fields (comprehensive vendor, buyer, invoice data)
- 13 line item table columns
- "Other" document class for unrecognized documents
- Modern prompt structure with separate System/Task prompts
- Quality assurance validations included

**Entity Fields** (27):
- Vendor: Name, Address, Email, Phone, Fax
- Buyer: Name, Address, Email, Phone, Fax
- Invoice: Number, Date, Type, Currency, Payment Terms
- Order: Number, Date, PO Number, PO Date
- Amounts: Sub Total, Total Amount, VAT/Tax, Discount, Shipping/Handling
- Addresses: Billing, Shipping, Remit
- Other: Delivery Numbers

**Line Items Table** (13 columns):
- Item Code, Description, Line Number
- Quantity Shipped, Quantity Ordered, Quantity BackOrder
- Unit Price, UOM, Discount, Line Total, Tax
- PO Number, Packing Slip Number

### CSI_APInvoice_Extract_V3 (Old Prompt Structure - RPA Compatible)
**GUID**: `df7b98b0-45fc-45c7-9e68-e529b574cf31`
**Purpose**: AP Invoice extraction - Old prompt structure for RPA compatibility
**Status**: Active, Working
**Prompt Structure**: `0` (Old/Legacy)
**RPA Compatible**: Yes

**Features**:
- Entity Classification activity only (1 activity, no Document Classification)
- 27 entity fields (same as V2)
- 13 line item table columns (same as V2)
- Single document class (no "Other" class needed)
- Legacy prompt structure with combined prompts
- Uses same baseModelID as V2

**Key Differences from V2**:
- No Document Classification activity
- No "Other" document class
- `promptStructure`: `0` instead of `1`
- `ocrType`: `null` instead of `""`
- `dcPrompt`: `null` (no document classification prompt)
- Different prompt markers (no System/Task split)

**Use Case**: When integrating with Infor RPA workflows that don't support the new prompt structure format.

### CSI_APInvoice_Extract (V1 - Deprecated)
**GUID**: `65523b7f-5037-4e3b-8eb9-5de286e2df76`
**Purpose**: AP Invoice extraction - Initial API-created version
**Status**: Deprecated - Use V2 or V3 instead

**Entity Fields** (13):
- Vendor Name, Address Line 1, City, State, Zip, Phone, Email
- Invoice Number, Invoice Date, Payment Terms, Currency Code
- PO Reference, Notes

**Line Items Table** (7 columns):
- Line Number, Item Code, Description, Quantity
- Unit of Measure, Unit Price, Due Date

### CSI_COCreation_Extract
**GUID**: `b748089d-b811-4b29-bf96-9220696e2b3a`
**Purpose**: Purchase Order data extraction

## Scripts Usage

```bash
# Generate OAuth token (required first)
python scripts/get_idp_token.py

# List all DPFs
python scripts/list_dpfs.py

# Get DPF details
python scripts/get_dpf_details.py <guid>

# Export DPF
python scripts/export_dpf.py <guid> [output_filename]

# Import DPF
python scripts/import_dpf.py <config_file.json>
```

## Integration Points

- **RPA**: RPA workflows can trigger IDP for document processing, then consume extracted data
- **IDM**: Documents stored in IDM can be sent to IDP for data extraction
- **Agents&Tools**: GenAI agents may orchestrate IDP workflows for intelligent automation
- **ION Workflows**: ION can route documents to IDP based on business rules

## Common Use Cases

1. **Invoice Processing**: Extract vendor, amounts, line items from AP invoices
2. **PO Matching**: Match invoice data against purchase orders
3. **DPF Management**: Export/import flow configurations between environments
4. **Bulk Processing**: Process document batches via API automation

## Development Notes

- API version is specified in path (e.g., `/ui/v1/...`)
- GUIDs are used to identify Document Processor Flows
- Import uses multipart/form-data with `datajsonfile` field
- Filter expressions support standard operators (equals, contains, etc.)

### DPF Import Format
- Must be JSON array: `[{ dpf_object }]`
- Creating new DPF requires valid datetime strings (not null)
- Best approach: Use `export_dpf.py` to get template, modify with `create_ap_invoice_from_template.py`
- Direct JSON creation often fails - always base on exported template

### Prompt Structure

IDP supports two prompt structure formats controlled by the `promptStructure` field:

#### New Prompt Structure (promptStructure=1)
Used by V2. Separates System and Task prompts for each activity:
```
$Document Classification System Prompt Start$...$Document Classification System Prompt End$
$Document Classification Task Prompt Start$...$Document Classification Task Prompt End$
$Entity Classification System Prompt Start$...$Entity Classification System Prompt End$
$Entity Classification Task Prompt Start$...$Entity Classification Task Prompt End$
$Table Detection System Prompt Start$...$Table Detection System Prompt End$
$Table Detection Task Prompt Start$...$Table Detection Task Prompt End$
```

#### Old Prompt Structure (promptStructure=0)
Used by V3. Combines prompts into single blocks (RPA compatible):
```
$Entity Classification Prompt Start$...$Entity Classification Prompt End$
$Table Detection Prompt Start$...$Table Detection Prompt End$
```

**Note**: Old prompt structure does NOT use Document Classification - prompts go directly into the Entity Classification and Table Detection sections.

## DPF Prompt Structure Comparison (V2 vs V3)

Two working DPF templates are available for different use cases:
- **V2 (New Prompt Structure)**: Full-featured, use when RPA compatibility not needed
- **V3 (Old Prompt Structure)**: RPA-compatible, simpler structure

### Structural Differences

| Component | V2 (New Prompt Structure) | V3 (Old Prompt Structure) |
|-----------|---------------------------|---------------------------|
| `promptStructure` | `1` | `0` |
| Activities | Document Classification + Entity Classification | Entity Classification only |
| Document Classes | Main class + "Other" fallback | Single class (no "Other") |
| `ocrType` | `""` (empty string) | `null` |
| `dcPrompt` | Full DC prompt | `null` |
| Prompt Markers | Separate System/Task prompts | Combined single prompts |
| RPA Compatible | No | Yes |

### Activity Configuration

**V2 (New Prompt Structure) - Two Activities Required**:
```json
"activities": [
  {
    "activityTypeId": 1,
    "activityName": "Document Classification",
    "activityProviderId": 9
  },
  {
    "activityTypeId": 2,
    "activityName": "Entity Classification",
    "activityProviderId": 10
  }
]
```

**V3 (Old Prompt Structure) - Single Activity**:
```json
"activities": [
  {
    "activityTypeId": 2,
    "activityName": "Entity Classification",
    "activityProviderId": 10
  }
]
```

### Document Classes

**V2**: Requires "Other" class for document validation
```json
"documentClasses": [
  { "documentName": "Other", "description": "Document which does not belong to any of the previously mentioned classes..." },
  { "documentName": "AP_Invoice_Extraction", ... }
]
```

**V3**: Single class only
```json
"documentClasses": [
  { "documentName": "AP_Invoice_Extraction", ... }
]
```

### Prompt Format Comparison

**V2 Entity Classification Prompt** (ecPrompt):
```
$Entity Classification System Prompt Start$
You are an expert document processing system...
$Entity Classification System Prompt End$

$Entity Classification Task Prompt Start$
<background>...</background>
<task>...</task>
<extraction_guidelines>...</extraction_guidelines>
<Quality_Assurance_Validations>...</Quality_Assurance_Validations>
<entities>...</entities>
<output_format>...</output_format>
$Entity Classification Task Prompt End$

$Table Detection System Prompt Start$...$Table Detection System Prompt End$
$Table Detection Task Prompt Start$...$Table Detection Task Prompt End$
```

**V3 Entity Classification Prompt** (ecPrompt):
```
$Entity Classification Prompt Start$
User: You are an expert Document-Based Question-Answering tool...
<entities>...</entities>
Clues:
[Field descriptions...]
<instructions>...</instructions>
Expert:
$Entity Classification Prompt End$

$Table Detection Prompt Start$
User:
You are an expert document-based table extractor...
[Table extraction instructions...]
$Table Detection Prompt End$
```

### Key Differences in Prompt Content

| Aspect | V2 (New) | V3 (Old) |
|--------|----------|----------|
| Role definition | System prompt separate | Inline with "User:" prefix |
| Field descriptions | In `<entities>` block | Listed as "Clues:" |
| Instructions format | XML-style tags | Numbered list |
| Output format | `<result>` tags with JSON | Same, but simpler |
| Confidence values | Ordinal (Very Low to Very High) | Numeric (0-100) |
| Response markers | `<result></result>` | `<result></result>` |

### Confidence Levels

**V2 (Ordinal)**:
- Very Low, Low, Medium, High, Very High

**V3 (Numeric)**:
- 0-100 percentage scale

### When to Use Each

**Use V2 (New Prompt Structure) when**:
- Building standalone IDP workflows
- Using IDP UI for processing
- Need document classification before extraction
- Want enhanced prompt capabilities

**Use V3 (Old Prompt Structure) when**:
- Integrating with Infor RPA workflows
- RPA project doesn't support new prompt structure
- Need simpler, single-activity configuration
- Legacy system compatibility required

### Creating New DPFs

**For V2 (New Prompt Structure)**:
1. Export `CSI_APInvoice_Extract_V2.json` as template
2. Modify entity fields and descriptions
3. Update prompts while preserving marker structure
4. Ensure Document Classification + Entity Classification activities
5. Include "Other" document class

**For V3 (Old Prompt Structure)**:
1. Export `CSI_APInvoice_Extract_V3.json` as template
2. Modify entity fields and descriptions
3. Update prompts using old marker format
4. Keep single Entity Classification activity
5. Single document class only

### baseModelID Note
Both V2 and V3 use `baseModelID: "1b3574e9-5330-43af-a010-0f658d4162cb"` (Infor's pre-built invoice model). This is optional - custom document types won't have a base model available. Set to `""` for fully custom DPFs.

## Related Documentation

- `Agents&Tools/CLAUDE.md` - Authentication and ION API patterns
- `RPA/CLAUDE.md` - RPA integration patterns
- `IDM/CLAUDE.md` - Document management integration

