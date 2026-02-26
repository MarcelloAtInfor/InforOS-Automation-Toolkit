# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Folder Purpose

This folder contains Infor ION API documentation, integration scripts, and workflow specifications. ION (Infor Operating Network) is the integration middleware that connects Infor applications and enables workflow automation.

**Current Status**: Active development with working Pulse and Workflow API scripts.

## Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.** Infor OS is NOT a typical local development stack - there is no local runtime, domain knowledge gaps cause frequent errors, and only the user can validate results in the live environment. Do NOT batch multiple phases together. After each phase: summarize what was done, what needs testing, and WAIT for user confirmation before continuing. See root `CLAUDE.md` for full details.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Contents

### scripts/
Python scripts for interacting with ION APIs:

| Script | Purpose | Status |
|--------|---------|--------|
| `send_pulse_alert.py` | Send Pulse alerts with details tree | Working |
| `send_pulse_all_types.py` | Send Alert, Notification, and Task | Working |
| `send_pulse_creative_examples.py` | Advanced examples: deep trees, translations, views | Working |
| `get_workflow.py` | Download workflow definitions | Working |
| `create_workflow.py` | Create, activate, delete workflows | Working |
| `start_workflow.py` | Start workflow instances | Working |
| `create_rpa_notification_workflow.py` | RPA Invoice Notification workflow | Working |
| `start_rpa_notification_workflow.py` | Test RPA notification workflow | Working |
| `access_token.txt` | OAuth token (2hr expiry) | Auto-generated |

**Token Generation**:
```bash
# From repository root
python -m shared.auth ION/scripts
```

### workflow_definitions/
Downloaded workflow JSON definitions for reference:
- `CS_Credit_Approval_API.json`
- `CSI_Item_similarity.json`
- `CustomerOrderDiscountWorkflow.json`
- `DocumentApprovalWorkflow.json`
- `Send_Presentation.json`
- `RPA_Invoice_Notification.json` - RPA invoice processing notification with drillback links

### APIs/
Contains OpenAPI/Swagger specifications for ION REST APIs:

| File | Description |
|------|-------------|
| `IONProcessApplicationService.json` | Pulse alerts, notifications, tasks, workflows |
| `IONProcessModel.json` | Workflow definition and management |
| `IONScriptingModelAPI.json` | Script execution and management |

## ION Pulse API Reference

### Endpoints

| Type | Endpoint | Purpose |
|------|----------|---------|
| Alert | `POST /v1/pulse/alert/create` | Critical notifications with detail trees |
| Notification | `POST /v1/pulse/notification/create` | Informational messages with retention |
| Task | `POST /v1/pulse/task/create` | Actionable items with buttons |

**Base URL**: `https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/IONSERVICES/process/application`

### LogicalId Format (CRITICAL)

**Format**: `lid://infor.product.instance` (exactly 2 dots after `lid://`)

```
lid://infor.rpa.claudecode     # Correct
lid://infor.rpa                 # WRONG - only 1 dot
lid://infor.rpa.app.test        # WRONG - 3 dots
```

**Error if wrong**: `"Invalid dot separators ('.') number detected (only 2 is allowed)"`

### Pulse Type Comparison

| Feature | Alert | Notification | Task |
|---------|:-----:|:------------:|:----:|
| `message` (required) | YES | YES | YES |
| `category` | YES | YES | YES |
| `distribution` (required) | YES | YES | YES |
| `details` (tree structure) | YES | - | - |
| `parameters` (flat list) | - | YES | YES |
| `dueDate` | YES | - | YES |
| `priority` (HIGH/MEDIUM/LOW) | - | - | YES |
| `customActions` (buttons) | - | - | YES |
| `retention` (30/60/90 days) | - | YES | - |
| `contextId` / `subContextId` | - | YES | YES |
| `views` (drillback links) | YES | YES | YES |
| `translations` | YES | YES | YES |

### Message Formatting

**Confirmed Working**:
- Multiline messages with `\n` newlines
- Unicode emojis render correctly in Pulse UI
- Long messages (500+ characters) work fine
- Formatted text with indentation preserved

**Example**:
```python
message = """URGENT: Invoice Approval Required

Vendor: Acme Corporation
Amount: $47,832.50
Due Date: February 28, 2026

Please review and approve."""
```

### Alert: details (Tree Structure)

Alerts use a hierarchical `details` property for structured data display:

```json
{
  "message": "Invoice requires approval",
  "category": "AP Invoice",
  "details": {
    "name": "Invoice Details",
    "properties": [
      {"name": "Invoice #", "value": "INV-2026-00847", "dataType": "STRING"},
      {"name": "Amount", "value": "47832.50", "dataType": "DECIMAL"}
    ],
    "subLevels": [
      {
        "name": "Vendor Info",
        "properties": [
          {"name": "Vendor Name", "value": "Acme Corp", "dataType": "STRING"}
        ]
      }
    ]
  },
  "distribution": [{"identifier": "user-guid", "type": "USER", "sendMail": false}]
}
```

**TreeLevelProperty dataTypes**: `STRING`, `INTEGER`, `DECIMAL`, `BOOLEAN`, `DATE`, `DATETIME`

### Notification: parameters (Flat List)

Notifications use a flat `parameters` array:

```json
{
  "message": "Order shipped",
  "category": "Shipping",
  "retention": 60,
  "contextId": 789456,
  "parameters": [
    {"name": "Order Number", "value": "ORD-2026-789", "dataType": "STRING"},
    {"name": "Ship Date", "value": "2026-01-29", "dataType": "DATE"},
    {"name": "Weight", "value": "24.5", "dataType": "DECIMAL"}
  ],
  "distribution": [{"identifier": "user-guid", "type": "USER", "sendMail": false}]
}
```

### Task: customActions (Buttons)

Tasks can include action buttons. **CRITICAL**: Must include a matching STRING parameter.

```json
{
  "message": "Expense report requires approval",
  "category": "Expense Approval",
  "priority": "HIGH",
  "dueDate": "2026-01-31T17:00:00Z",
  "parameters": [
    {"name": "approvalDecision", "value": "", "dataType": "STRING"},
    {"name": "Employee", "value": "Sarah Johnson", "dataType": "STRING"},
    {"name": "Amount", "value": "2847.50", "dataType": "DECIMAL"}
  ],
  "customActions": {
    "parameterName": "approvalDecision",
    "buttons": [
      {"label": "Approve", "value": "APPROVED"},
      {"label": "Reject", "value": "REJECTED"},
      {"label": "Request Info", "value": "MORE_INFO"}
    ]
  },
  "distribution": [{"identifier": "user-guid", "type": "USER", "sendMail": false}]
}
```

**Error if parameter missing**: `"Custom Actions linked Parameter name X not specified as String Parameter"`

### Distribution Types

```json
{
  "distribution": [
    {"identifier": "<USER_GUID>", "type": "USER", "sendMail": false},
    {"identifier": "DistributionGroupName", "type": "GROUP", "sendMail": true}
  ]
}
```

- `USER`: IFS Identity2 GUID
- `GROUP`: IFS Distribution Group name
- `sendMail`: Send email notification (optional)

### Translations (Multi-Language Support)

Translations provide localized messages, categories, and labels. **Format is a map keyed by locale**.

```json
{
  "translations": {
    "es-ES": {
      "message": "Spanish message here",
      "category": "Spanish category",
      "parameterLabels": {
        "Lot Number": "Numero de Lote",
        "Part Number": "Numero de Pieza"
      },
      "viewLabels": {
        "lot_details": "Ver Detalles del Lote"
      }
    },
    "de-DE": {
      "message": "German message here",
      "category": "German category"
    }
  }
}
```

**Translation object fields**: `message`, `category`, `parameterLabels`, `viewLabels`

**CRITICAL**:
- `parameterLabels` keys must match parameter `name` values exactly
- `viewLabels` keys must match view `name` values exactly
- Format is `{locale: Translation}` map, NOT an array

### Views (Data Properties)

Views pass data properties for display or drillback context.

```json
{
  "views": [
    {
      "name": "lot_details",
      "label": "View Lot Details",
      "properties": [
        {"name": "lotNumber", "value": "LOT-2026-003847"},
        {"name": "partNumber", "value": "BRG-7890-HD"}
      ]
    }
  ]
}
```

**View object fields**: `name`, `label`, `properties`

**Note**: This structure is different from workflow views which use `viewId`, `drillback`, and `filters`.

## Authentication

ION APIs use standard Infor OAuth 2.0 authentication via the shared module:

```python
from shared.auth import get_auth_headers
from shared.config import get_base_url

headers = get_auth_headers()
url = get_base_url('IONSERVICES/process/application')
```

- Token expires after 2 hours
- Uses password grant with saak/sask credentials
- See `Agents&Tools/CLAUDE.md` for complete authentication details

## API Throttling

**Limit**: 10 calls per 10 seconds
**Error**: HTTP 429 (Too Many Requests)
**Recommendation**: Implement retry logic with exponential backoff

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400: Invalid dot separators | Wrong logicalId format | Use `lid://x.y.z` (exactly 2 dots) |
| 400: Custom Actions parameter not specified | Missing STRING parameter for customActions | Add parameter matching `parameterName` |
| 400: Missing input structures | Workflow has trees but no inputStructures provided | Add `inputStructures` array with tree data |
| 400: Variable value required | Empty string value in inputVariables | Use "N/A" or placeholder for empty values |
| 400: Variable datatype required | Missing dataType in inputVariables | Add `"dataType": "STRING"` to each variable |
| 401: Unauthorized | Expired token | Regenerate: `python -m shared.auth ION/scripts` |
| 429: Too Many Requests | Rate limit exceeded | Wait and retry with backoff |

## Integration Patterns

### RPA + ION Pulse
RPA workflows can send Pulse alerts/tasks for human-in-the-loop processing:
```
RPA Workflow (document processing)
    ↓
ION Pulse Task API (approval request)
    ↓
User takes action in Pulse
    ↓
RPA continues based on decision
```

### GenAI Agents + ION Pulse
GenAI agents can create alerts for exception handling:
```
GenAI Agent (invoice processing)
    ↓
Exception detected (vendor not found)
    ↓
ION Pulse Alert API (notify user)
```

## ION Workflow API Reference

### API Endpoints

**Model Service** (`{tenant}/IONSERVICES/process/model`):

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/workflows` | GET | List all workflows |
| `/v1/workflows/{name}` | GET | Get workflow definition |
| `/v1/workflows` | POST | Create new workflow |
| `/v1/workflows/{name}` | DELETE | Delete workflow |
| `/v1/workflows/{name}/activate` | PUT | Activate workflow |
| `/v1/workflows/{name}/deactivate` | PUT | Deactivate workflow |

**Application Service** (`{tenant}/IONSERVICES/process/application`):

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/workflow/start` | POST | Start workflow instance |
| `/v1/workflow/interface` | GET | List active workflows |

### Workflow Structure

```json
{
  "name": "WorkflowName",
  "description": "Description",
  "variables": [
    {
      "name": "InputVar",
      "dataType": "STRING",
      "workflowInput": true,
      "workflowOutput": false,
      "useValue": false
    }
  ],
  "views": [],
  "trees": [],
  "sequentialFlow": {
    "sequenceNumber": 0,
    "flowParts": [...]
  }
}
```

### FlowPart Types (LOWERCASE!)

| _type | Purpose |
|-------|---------|
| `usertask` | User tasks, notifications |
| `ifthenelse` | Conditional branching |
| `ionapi` | ION API calls |
| `scripting` | Script execution |
| `wait` | Timer/delay |
| `parallelflow` | Parallel execution |
| `loopbackflow` | Loop constructs |

### UserTask (Notification)

```json
{
  "_type": "usertask",
  "sequenceNumber": 1,
  "name": "SendNotification",
  "userTaskType": "NOTIFICATION",
  "taskMessage": "Message with [VariableName] substitution",
  "taskActionType": "StandardAction",
  "priority": "Medium",
  "workflowDistributionItems": [
    {"name": "user-guid", "distributionType": "USER", "sendEmail": false}
  ],
  "parameters": [
    {"variable": "VarName", "label": "Label", "readOnly": true}
  ]
}
```

**userTaskType values**: `NOTIFICATION`, `USER_TASK`

### Starting a Workflow Instance

**CRITICAL**: `inputVariables` require `dataType`!

```json
POST /v1/workflow/start?logicalId=lid://infor.rpa.claudecode

{
  "workflowName": "ClaudeCode_Test_Workflow",
  "instanceName": "Instance_001",
  "inputVariables": [
    {"name": "InputMessage", "value": "Hello!", "dataType": "STRING"},
    {"name": "SenderName", "value": "Claude Code", "dataType": "STRING"}
  ]
}
```

**Error without dataType**: `"Variable datatype required"`

### Starting Workflows with Tree Structures

**CRITICAL**: If workflow has `trees`, you MUST provide `inputStructures`!

```json
POST /v1/workflow/start?logicalId=lid://infor.rpa.claudecode

{
  "workflowName": "RPA_Invoice_Notification",
  "instanceName": "Instance_001",
  "inputVariables": [
    {"name": "VendorNumber", "value": "DEMO001", "dataType": "STRING"},
    {"name": "VendorName", "value": "Precision Tools Inc.", "dataType": "STRING"}
  ],
  "inputStructures": [
    {
      "name": "CreatedAssets",
      "subStructures": [
        {
          "name": "VendorInfo",
          "fields": [
            {"name": "VendorNumber", "value": "DEMO001", "dataType": "STRING"},
            {"name": "VendorName", "value": "Precision Tools Inc.", "dataType": "STRING"}
          ]
        },
        {
          "name": "POInfo",
          "fields": [
            {"name": "PONumber", "value": "DP00009000", "dataType": "STRING"}
          ]
        }
      ]
    }
  ]
}
```

**Error without inputStructures**: `"startWorkflow failed: Error validating input structures; Missing input structures: [TreeName]"`

**CRITICAL**: All input variable values must be non-empty. Use "N/A" as placeholder for empty values.

**Error with empty values**: `"Variable value required"`

### Variable dataTypes

`STRING`, `INTEGER`, `DECIMAL`, `BOOLEAN`, `DATETIME`, `DATE`, `USER`, `GROUP`, `STRUCTURE`

## Quick Start

### Pulse API

1. **Generate token**:
   ```bash
   python -m shared.auth ION/scripts
   ```

2. **Send a test alert**:
   ```bash
   cd ION/scripts
   python send_pulse_alert.py
   ```

3. **Send all three types**:
   ```bash
   cd ION/scripts
   PYTHONUTF8=1 python send_pulse_all_types.py
   ```

4. **Check Pulse inbox** in Infor OS for the messages

### Workflow API

1. **Generate token**:
   ```bash
   python -m shared.auth ION/scripts
   ```

2. **Download reference workflows**:
   ```bash
   cd ION/scripts
   python get_workflow.py
   ```

3. **Create and activate test workflow**:
   ```bash
   python create_workflow.py --activate
   ```

4. **Start workflow instance**:
   ```bash
   python start_workflow.py "Your message here"
   ```

5. **Check Pulse inbox** for the notification

### RPA Invoice Notification Workflow

1. **Generate token**:
   ```bash
   python -m shared.auth ION/scripts
   ```

2. **Create and activate workflow**:
   ```bash
   cd ION/scripts
   python create_rpa_notification_workflow.py --activate
   ```

3. **Test with SUCCESS data**:
   ```bash
   python start_rpa_notification_workflow.py
   ```

4. **Test with FAILURE data**:
   ```bash
   python start_rpa_notification_workflow.py --failure
   ```

5. **Check Pulse inbox** for notification with:
   - Variable substitution in message
   - Created Assets tree structure
   - Drillback links to PO and Vendor

---

**Last Updated**: 2026-01-30 - Creative Pulse examples with translations, views, deep trees
