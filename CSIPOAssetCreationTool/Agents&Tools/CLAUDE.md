# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### CLAUDE.md
When the user confirms that changes or discoveries are good/correct, update this CLAUDE.md file with the new information. This ensures future Claude Code sessions have access to accumulated knowledge.

### log.md
Always update log.md to track project progress. Record completed steps, current status, new discoveries, and next steps. This serves as the running history of the project and helps maintain context across sessions.

## Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.** Infor OS is NOT a typical local development stack - there is no local runtime, domain knowledge gaps cause frequent errors, and only the user can validate results in the live environment. Do NOT batch multiple phases together. After each phase: summarize what was done, what needs testing, and WAIT for user confirmation before continuing. See root `CLAUDE.md` for full details.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Project Purpose

This repository documents exploration and development of GenAI assets (tools and agents) within Infor's platform. The goal is to automate workflows by creating tools that call APIs and agents that orchestrate those tools.

## Infor GenAI Architecture

### Tools
Tools are API wrappers that connect to Infor API Gateway endpoints. Each tool requires:
- **Name** and **Model** (e.g., Claude 3.7 Sonnet)
- **Source**: API endpoint from API Gateway (e.g., "CSI/IDORequestService/ido")
- **API Request Instructions**: Method, endpoint path, headers, query parameters
- **API Response Instructions**: How the LLM should interpret responses

### Agents
Agents orchestrate tools (up to 50 per agent). Each agent requires:
- **Name**, **Logical ID**, and **Model**
- **Instructions and Task Control**: Workflow guidelines for how/when to use tools
- **Tools**: Selected from the GenAI Tools library

### Platform Limits
- **Agent execution timeout: 240 seconds (HARD LIMIT)**: The GenAI platform returns 504 Gateway Timeout if an agent turn exceeds 240s. For agents with many tool calls, work must be split into chunks using sentinel-based checkpoints (e.g., `<<CHECKPOINT>>`/`<<COMPLETE>>`) and multi-turn "continue" patterns. Budget ~5-7 tool calls per chunk to stay safely under the limit.
- **Instructions field**: 900 characters max. Put detailed instructions in `api_docs` (tools) or `workflow` (agents).
- **Tools per agent**: Up to 50.
- **1 tool = 1 HTTP call**: Framework executes one API call per tool invocation.

### Platform Access
- UI: https://mingle-portal.inforcloudsuite.com/<YOUR_TENANT>
- API Documentation: https://developer.infor.com/
- Interface navigation: Prompt Playground → Factory (Tools, Agents, Chat) → Admin

## Development Approach

The preferred approach is REST API-based development (rather than browser automation via Chrome MCP) for creating and managing tools/agents programmatically.

## API Structure

### Base URLs
- **Core Service**: `https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/coresvc`
- **Chat Service**: `https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/chatsvc`
- **SyteLine REST**: Backend API that tools call to access Infor data

### Authentication
All APIs use Bearer token authentication via the **centralized `shared/` module**:
```
Authorization: Bearer <token>
```

**Obtaining Access Tokens:**

Tokens expire after 2 hours. Use the centralized auth module:

```bash
# Generate a new token (from repo root)
python -m shared.auth Agents&Tools/scripts

# Or run the convenience wrapper
python Agents&Tools/scripts/get_token_password_grant.py
```

**Using in Scripts:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL, IDO_URL

# Get auth headers (auto-fetches and caches token)
headers = get_auth_headers()

# Get service URLs
tools_url = f"{GENAI_CORE_URL()}/api/v1/tools"
ido_url = f"{IDO_URL()}/load/SLVendors"
```

**Important**: Uses password grant type with `saak` (username) and `sask` (password) from the `.ionapi` file. Credentials stored in your `.ionapi` file (see repo root `shared/` setup).

### Key API Endpoints

#### Tools Management (Core Service)
- `GET /api/v1/tools` - List all tools
- `GET /api/v1/tools/{tool_guid}` - Get specific tool
- `PUT /api/v1/tools` - Create or update tool (upsert)
- `POST /api/v1/tools` - Bulk create tools
- `DELETE /api/v1/tools/{tool_guid}` - Delete tool
- `PUT /api/v1/tools/enable` - Enable/disable tool

#### Chat/Agent Execution (Chat Service)
- `POST /api/v1/chat` - Execute chat with agent (requires `x-infor-logicalidprefix` header)
- `POST /api/v1/chat/sync` - Synchronous chat execution
- `POST /api/v1/prompt` - Execute single prompt
- `GET /api/v1/sessions` - List chat sessions
- `GET /api/v1/models` - Get available models

#### Backend Data Access (SyteLine REST)
Tools use these endpoints to query/modify data:
- `GET /load/{ido}` - Load records from collection (with filter, properties, orderBy)
- `POST /update/{ido}` - Insert, update, or delete records
- `GET /info/{ido}` - Get collection metadata
- `POST /invoke/{ido}?method={methodName}` - Invoke stored procedure/method
- Headers: `Authorization`, `X-Infor-MongooseConfig`

#### Invoke Endpoint Pattern (for Stored Procedures)
The `/invoke/{ido}?method={methodName}` endpoint calls stored procedures:

```
POST /invoke/{ido}?method={methodName}
Headers:
  X-Infor-MongooseConfig: <YOUR_SITE>
Body:
  ["param1", "param2", ...]  // Array of string parameters
```

**Parameter Format:**
- All parameters must be strings (even numeric values like "0.0")
- DateTime format: ISO 8601 (e.g., "2026-01-31T12:30:05")
- Empty parameters: Use empty string ""
- Parameter order is critical - matches stored procedure signature

**CAUTION:** Some stored procedures (e.g., PO Receiving) use session-scoped temp tables that don't work across separate REST API calls. Each REST call gets a different database SessionID, so multi-step procedures that expect the same session will fail silently.

### Tool Creation Pattern

A tool is an API wrapper that requires:
1. **Basic Info**: name, model selection (e.g., Claude 3.7 Sonnet), enabled status
2. **Description**: What the tool does, use cases, parameter examples
3. **Source**: API endpoint from API Gateway (selected from dropdown or specified)
4. **API Request Instructions**: HTTP method, endpoint path, headers, query parameters with format/type
5. **API Response Instructions**: How LLM should interpret the JSON response

Example tool structure for API creation:
```json
{
  "name": "ItemSearch_Tool",
  "description": "Search for items in CSI/Syteline inventory",
  "enabled": true,
  "model": "claude-3-7-sonnet",
  "source": "CSI/IDORequestService/ido",
  "request": {
    "method": "GET",
    "endpoint": "/load/SLItems",
    "headers": {
      "X-Infor-MongooseConfig": "<YOUR_SITE>"
    },
    "parameters": [
      {
        "name": "properties",
        "type": "STRING",
        "required": true,
        "description": "Comma-delimited list of properties (e.g., 'Item,Description,UnitOfMeasure')"
      },
      {
        "name": "filter",
        "type": "STRING",
        "required": false,
        "description": "SQL WHERE clause (e.g., 'Item LIKE \"A%\"')"
      }
    ]
  },
  "response": {
    "description": "Returns JSON with 'Items' array containing item records",
    "interpretation": "Extract relevant fields from Items array. Success field indicates if call succeeded."
  }
}
```

### CRITICAL: api_docs Format for Tools

**The LLM agent is extremely sensitive to whitespace in the `api_docs` field.** A single blank line after `Headers:` causes URL malformation and 404 errors.

**CORRECT FORMAT (use this):**
```
Method: POST
Endpoint: /update/SLVendors

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Body:
{...}
```

**WRONG FORMAT (causes 404 errors):**
```
Method: POST
Endpoint: /update/SLVendors

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Body:
{...}
```

The blank line after `Headers:` causes the LLM to insert garbage like `/<YOUR_TENANT>/api/ido/` into the URL path.

**When creating/updating tools:**
1. NO blank line between `Headers:` and the header value
2. Use `Endpoint:` (capitalized), not `ENDPOINT:` (all caps)
3. Keep api_docs simple - match the working tools format exactly

### Dynamic Site Configuration (Multi-Tenant Support)

Tools can use `<site>` placeholder instead of hardcoded tenant values to support multiple tenants.

**In tool api_docs:**
```
Headers:
X-Infor-MongooseConfig: <site>
```

**In tool instructions, add:**
```
SITE PARAMETER (REQUIRED):
- The <site> placeholder must be filled with the site value from the agent's input
- Format: [TENANT]_DALS (e.g., "<YOUR_SITE>")
```

**In agent workflow:**
```
SITE CONFIGURATION (CRITICAL):
- Extract the "site" value from input at START of processing
- Pass this value to ALL tool calls as the <site> placeholder
- If site is NOT provided in input: STOP and ask user for site value
```

**Agent input format with site:**
```json
{
  "site": "<YOUR_SITE>",
  "vendor": {...},
  "purchaseOrder": {...},
  "lineItems": [...]
}
```

**Benefits:**
- Same tools/agents work across multiple tenants
- RPA can pass different site values per environment
- No need to maintain separate tool versions per tenant

### Agent Creation and Execution Pattern

**CORRECTION**: Agents CAN be created via REST API using the same `/api/v1/tools` endpoint as tools.

**Key Difference**:
- Tools use `"type": "API_DOCS"`
- Agents use `"type": "TOOLKIT"`

**Agent Structure**:
```json
{
  "name": "MyAgent",
  "type": "TOOLKIT",
  "data": {
    "workflow": "Instructions for the agent...",
    "tools": ["Tool1_Name", "Tool2_Name"],
    "logicalIds": ["lid://company.domain.agent-name"],
    "model": {
      "model": "CLAUDE",
      "version": "claude-3-7-sonnet-20250219-v1:0"
    }
  },
  "status": 1,
  "utterances": ["Sample phrase 1", "Sample phrase 2"],
  "instructions": "Short description of agent"
}
```

**Agent Invocation via Chat API**:
```bash
curl -X POST https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/chatsvc/api/v1/chat/sync \
  -H "Authorization: Bearer <token>" \
  -H "x-infor-logicalidprefix: lid://company.domain.agent-name" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Execute the task"
  }'
```

### SyteLine Update API Format

**CRITICAL**: The SyteLine REST API `/update/{ido}` endpoint requires a specific format that differs from the simplified format in some documentation.

**Correct Format for Batch Updates**:
```json
{
  "IDOName": "SLCoitems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 2,
      "ItemId": "PBT=[coitem] coi.DT=[2014-06-30 15:38:01.877] coi.ID=[guid]",
      "Properties": [
        {
          "IsNull": false,
          "Modified": true,
          "Name": "DueDate",
          "Value": "20260126"
        }
      ]
    }
  ]
}
```

**Field Definitions**:
- `IDOName`: The IDO collection name (e.g., "SLCoitems", "SLVendors", "SLItems", "SLPOs")
  - **CRITICAL**: IDO names are case-sensitive! Use exact casing:
    - ✅ `SLPOs` (Purchase Orders - note capital O)
    - ❌ `SLPos` (will return 404)
    - ✅ `SLItems` (Items)
    - ✅ `SLVendors` (Vendors)
    - ✅ `SLCoitems` (Customer Order Items)
    - ✅ `SLPoItems` (Purchase Order Items)
- `RefreshAfterSave`: Boolean, typically `true` to get updated data back
- `Changes`: Array of change objects (batch multiple updates in one call)
- `Action`: Integer, `1` = insert, `2` = update, `4` = delete (NOT `3` — Action `3` is a no-op that returns success without deleting)
- `ItemId`: The `_ItemId` value from query results (unique identifier)
- `Properties`: Array of property changes (can include multiple properties)
- `IsNull`: Boolean, `false` for value updates
- `Modified`: Boolean, `true` to apply the change
- `Name`: Property name to update (e.g., "DueDate")
- `Value`: New value in appropriate format (dates: "YYYYMMDD")

**Common Mistake**: Using simplified format like `{"SLCoitems": [{"_ItemId": "...", "DueDate": "..."}]}` will fail.

**Best Practice**: Always batch updates in a single Changes array rather than making multiple API calls.

### Discovering IDO Properties

**IMPORTANT**: Before creating tools that interact with IDOs, use the `/info/{ido}` endpoint to discover the correct property names.

**How to Query IDO Properties**:
```bash
GET {base}/CSI/IDORequestService/ido/info/SLVendors
Headers:
  Authorization: Bearer <token>
  X-Infor-MongooseConfig: <YOUR_SITE>
```

**Response**: Returns metadata including all available properties, their types, and constraints.

### IDO Metadata Discovery via System IDOs (CRITICAL - NEVER SKIP)

**NEVER conclude that a field is not writable via API until you have queried the IDO metadata system IDOs.**

The `/info/{ido}` endpoint shows properties, but it does NOT reveal whether writes will actually persist. Some IDO properties appear writable in metadata but silently ignore updates because the property lives on a **joined table**, not the IDO's primary table. The IDO only writes to its primary table — writes to joined table columns succeed (return 200 OK) but are silently discarded.

**When to use this technique**:
- A property update returns success but the value doesn't persist (silent write failure)
- You need to understand which tables back an IDO
- You want to find the correct IDO to write to for a specific database column
- Before concluding ANY field "cannot be set via API"

**System Metadata IDOs** (queryable via the same `/load/{ido}` endpoint as business data):

| IDO | Purpose | Key Properties |
|-----|---------|---------------|
| `IdoCollections` | Find IDO by name | `CollectionName`, `ServerAssembly`, `ExtensionClassAssembly` |
| `IdoTables` | Find tables joined by an IDO | `CollectionName`, `TableName`, `TableAlias`, `JoinType` (0=INNER, 1=LEFT), `TableType` (3=Primary) |
| `IdoProperties` | Map property → column → table | `CollectionName`, `PropertyName`, `ColumnName`, `ColumnTableAlias`, `ColumnTableName` |

**Workflow for diagnosing silent write failures**:

1. **Identify the property that won't persist**: e.g., `JshSetuprgid` on `SLJobRoutes`
2. **Find which table the property maps to**:
   ```
   GET /load/IdoProperties?filter=CollectionName='SLJobRoutes' AND PropertyName='JshSetuprgid'&properties=PropertyName,ColumnName,ColumnTableAlias,ColumnTableName
   ```
   → Result: column `setuprgid` on table `jrt_sch` (alias `jsh`)
3. **Check if that table is the IDO's primary table**:
   ```
   GET /load/IdoTables?filter=CollectionName='SLJobRoutes' AND TableName='jrt_sch'&properties=TableName,TableType,JoinType
   ```
   → Result: `TableType=0` (NOT primary) — this is why writes are silently ignored
4. **Find which IDO HAS that table as primary**:
   ```
   GET /load/IdoTables?filter=TableName='jrt_sch' AND TableType=3&properties=CollectionName,TableName,TableType
   ```
   → Result: `SLJrtSchs` — **this is the IDO to use for writes**
5. **Write via the correct IDO**: Use `SLJrtSchs` to update `Setuprgid` instead of `SLJobRoutes`

**Real-world example (BOMGenerator project)**: Initially concluded resource groups "cannot be set via API" because updates to `SLJobRoutes.JshSetuprgid` returned success but didn't persist. After querying the metadata IDOs, discovered `jrt_sch` is a joined table on `SLJobRoutes` but the PRIMARY table on `SLJrtSchs`. Writing `Setuprgid` through `SLJrtSchs` worked immediately. **The metadata IDOs completely reversed the conclusion.**

**Key lesson**: SyteLine IDOs often join 10-20+ tables, but can only write to their primary table. A property being present and even marked `ReadOnly=False` does NOT guarantee writes will persist. Always verify the table ownership via `IdoTables` when writes fail silently.

**Common Property Names** (case-sensitive):

**SLVendors**:
- VendNum (vendor number, EXACTLY 7 chars - pad with zeros: "MWF" → "MWF0001")
- Name (vendor name)
- VadAddr_1 (address line 1)
- VadCity, VadState, VadZip (location)
- **Phone** (NOT VadPhone!)
- **ExternalEmailAddr** (NOT VadEmail!)
- TermsCode, CurrCode, BankCode

**SLItems**:
- Item (item code, unique)
- Description (item description)
- UM (unit of measure)
- MatlType, PMTCode, ProductCode
- AbcCode, CostType, CostMethod, Stat

**SLPOs** (Purchase Orders):
- PoNum (PO number, exactly 10 characters)
- VendNum (vendor number - CRITICAL for linking PO to vendor)
- TermsCode, Stat, Type, Whse, PoCurrCode

**SLPoItems** (Purchase Order Lines):
- PoNum, PoLine (line number)
- Item, QtyOrderedConv, UM
- Stat (status: "O" = Ordered, "P" = Planned - use "O" for new PO lines)
- DueDate (format: "YYYY-MM-DD"), Whse

**Filter Syntax**:
- Use **single quotes** for string values: `Item = 'WIDGET-A'`
- LIKE operator for partial match: `Name LIKE '%Corp%'`
- NOT double quotes (will cause IllegalFilterException)

## Successful Implementation: Order Line Due Date Updates

### Use Case
Automate weekly task to update customer order line due dates to the previous Sunday (making them "late" for the week).

### Solution Components

**Tool 1: QueryUpcomingOrders_Tool**
- Endpoint: GET `/load/SLCoitems`
- Filter: `Stat='O'` (Ordered status only)
- Order by: `CoOrderDate DESC` (most recent orders first)
- Limit: 20 records
- Returns: CoNum, CoLine, Item, DueDate, CoOrderDate, Stat, _ItemId

**Tool 2: UpdateOrderDueDate_Tool**
- Endpoint: POST `/update/SLCoitems`
- Format: IDOName/Changes structure with batch updates
- Updates: Multiple order lines in single API call

**Agent: UpdateOrderLineDates_Agent_v2**
- Logical ID: `lid://infor.syteline.update-orderline-dates-v2`
- Workflow:
  1. Calculate previous Sunday date (correct weekday calculation)
  2. Query 20 most recent order lines (Stat='O' only)
  3. Build Changes array with all 20 items
  4. Execute single batch update to previous Sunday
  5. Report results

### Key Learnings

**Date Calculation for Previous Sunday**:
```python
# Correct calculation
today = datetime.now()
if today.weekday() == 6:  # Today is Sunday
    days_back = 7
else:
    days_back = today.weekday() + 1  # Days since last Sunday
previous_sunday = today - timedelta(days=days_back)
```

**Status Filter**: Always filter by `Stat='O'` to only include Ordered status (not Complete 'C' or Planned 'P')

**Ordering**: Use `CoOrderDate DESC` to target most recent orders rather than `DueDate ASC`

**Batch Updates**: Build complete Changes array before calling update tool (not multiple calls)


