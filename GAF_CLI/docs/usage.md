# Usage Guide

## Prerequisites

Before using the Agent Factory, ensure you have:

1. **Python 3.11+** installed
2. **.ionapi credentials file** from Infor OS tenant
3. **IONAPI_FILE environment variable** pointing to your .ionapi file

### Setting Up Credentials

1. Download your .ionapi file from Infor OS ION API admin
2. Set environment variable:
   ```bash
   # Windows
   set IONAPI_FILE=C:\path\to\your\credentials.ionapi

   # Linux/Mac
   export IONAPI_FILE=/path/to/your/credentials.ionapi
   ```
3. Never commit .ionapi files to git (add to .gitignore)

### Installing Dependencies

```bash
pip install -r requirements.txt
```

---

## Tutorial: Your First Factory Tool

This tutorial walks through creating and publishing a tool using the Factory Agent.

### Step 1: Verify Setup

First, verify your credentials work by listing existing tools:

```bash
python -m src.cli.list_assets --prefix GAF
```

**Expected output:**
```
Found 6 tools:
- GAF_GenAI_ListAssets_Tool_v1 (<GUID>)
- GAF_GenAI_GetAsset_Tool_v1 (<GUID>)
- GAF_GenAI_CreateTool_Tool_v1 (<GUID>)
- GAF_GenAI_CreateAgent_Tool_v1 (<GUID>)
- GAF_GenAI_UpdateAsset_Tool_v1 (<GUID>)
- GAF_GenAI_AgentFactory_Agent_v1 (<GUID>)
```

### Step 2: Request a Tool via Factory Agent

Ask the Factory Agent to create a simple tool:

```bash
python -m src.cli.invoke_agent "Create a tool called GAF_GenAI_HelloWorld_Tool_v1 that returns a greeting message"
```

**Expected output:**
```
Invoking Factory Agent...

DRAFT: GAF_GenAI_HelloWorld_Tool_v1

{
  "name": "GAF_GenAI_HelloWorld_Tool_v1",
  "description": "Returns a greeting message",
  "type": "API_DOCS",
  ...
}

To publish this tool, type: CONFIRM PUBLISH
```

### Step 3: Review and Confirm

The agent shows a DRAFT before publishing. Review the specification carefully:
- Name follows convention: `GAF_<product>_<Capability>_Tool_v<N>`
- Type is API_DOCS (correct for tools)
- No hardcoded tenant URLs in servicePath

If satisfied, confirm:

```bash
CONFIRM PUBLISH
```

**Expected output:**
```
Publishing GAF_GenAI_HelloWorld_Tool_v1...
SUCCESS: Tool created with GUID <GUID>
```

### Step 4: Verify Publication

List assets to confirm your tool exists:

```bash
python -m src.cli.list_assets --prefix GAF_GenAI_HelloWorld
```

**Expected output:**
```
Found 1 tools:
- GAF_GenAI_HelloWorld_Tool_v1 (<GUID>)
```

### Step 5: Cleanup (Optional)

For test tools, you can delete via the Infor OS UI or run smoke_test.py which includes cleanup.

---

## Tutorial: Publishing from JSON Spec

If you have a pre-written JSON specification:

### Step 1: Create Spec File

Create `specs/tools/MyTool.json`:

```json
{
  "name": "GAF_GenAI_MyTool_Tool_v1",
  "description": "My custom tool description",
  "type": "API_DOCS",
  "instructions": "Brief instructions for the tool",
  "inputs": [],
  "data": {
    "servicePath": "GENAI/coresvc",
    "api_docs": "Method: GET\nEndpoint: /api/v1/tools",
    "headers": {},
    "responseInstructions": "Parse the response",
    "returnDirect": false,
    "model": {
      "model": "CLAUDE",
      "version": "claude-3-7-sonnet-20250219-v1:0"
    }
  },
  "status": 1,
  "utterances": []
}
```

### Step 2: Publish Tool

```bash
python -m src.cli.publish_tool specs/tools/MyTool.json
```

**Expected output:**
```
Validating spec...
Publishing GAF_GenAI_MyTool_Tool_v1...
SUCCESS: Tool created with GUID <GUID>
```

---

## Tutorial: Running Smoke Test

Verify the entire factory loop works:

```bash
python scripts/smoke_test.py
```

**Expected output:**
```
=== Smoke Test Started ===
Step 1: Invoking Factory Agent to draft HelloWorld tool...
  PASS: Received draft with CONFIRM prompt
Step 2: Sending CONFIRM PUBLISH...
  PASS: Tool created
Step 3: Verifying tool in asset list...
  PASS: GAF_GenAI_HelloWorld_Tool_v1 found
Step 4: Cleanup...
  PASS: Test tool deleted
=== Smoke Test PASSED ===
```

---

## CLI Reference

Quick reference for all CLI commands. For tutorials, see sections above.

### list_assets.py

List GenAI tools and agents with optional filtering.

**Usage:**
```bash
python -m src.cli.list_assets [--prefix PREFIX] [--type TYPE]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| --prefix | No | Filter by name prefix (e.g., "GAF") |
| --type | No | Filter by asset type (e.g., "API_DOCS", "TOOLKIT") |

**Examples:**

List all assets:
```bash
python -m src.cli.list_assets
```

List Factory tools only:
```bash
python -m src.cli.list_assets --prefix GAF --type API_DOCS
```

**Output:**
```
Found 5 tools:
- GAF_GenAI_ListAssets_Tool_v1 (<GUID>)
- GAF_GenAI_GetAsset_Tool_v1 (<GUID>)
...
```

---

### publish_tool.py

Publish a tool from JSON specification file.

**Usage:**
```bash
python -m src.cli.publish_tool <spec_file>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| spec_file | Yes | Path to JSON specification file |

**Example:**
```bash
python -m src.cli.publish_tool specs/tools/GAF_GenAI_ListAssets_Tool_v1.json
```

**Output (success):**
```
Validating spec...
Publishing GAF_GenAI_ListAssets_Tool_v1...
SUCCESS: Tool created with GUID b5707a26-301b-493d-8000-3cc0b214ee96
```

**Output (validation error):**
```
Validating spec...
ERROR: Invalid name format. Expected: GAF_<product>_<Capability>_Tool_v<N>
```

---

### publish_agent.py

Publish a TOOLKIT agent from JSON specification file.

**Usage:**
```bash
python -m src.cli.publish_agent <spec_file>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| spec_file | Yes | Path to JSON specification file |

**Example:**
```bash
python -m src.cli.publish_agent specs/agents/GAF_GenAI_AgentFactory_Agent_v1.json
```

**Output:**
```
Validating spec...
WARNING: Agent type is TOOLKIT (expected for orchestration)
Publishing GAF_GenAI_AgentFactory_Agent_v1...
SUCCESS: Agent created with GUID 7a047f6f-fb88-4488-bc55-25f576e887c9
```

**Note:** Warns if type is not TOOLKIT, but allows publish for flexibility.

---

### update_asset.py

Update an existing tool or agent by GUID.

**Usage:**
```bash
python -m src.cli.update_asset <spec_file>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| spec_file | Yes | Path to JSON specification with "guid" field |

**Requirements:**
- Spec file MUST include "guid" field with existing asset's GUID
- All fields are replaced (full replacement semantics, not patch)

**Example:**
```bash
python -m src.cli.update_asset specs/tools/GAF_GenAI_ListAssets_Tool_v1.json
```

**Output (success):**
```
Updating GAF_GenAI_ListAssets_Tool_v1 (<GUID>)...
SUCCESS: Asset updated
```

**Output (missing GUID):**
```
ERROR: Spec must include "guid" field for update operations.
Use publish_tool.py or publish_agent.py for new assets.
```

---

### invoke_agent.py

Invoke the Factory Agent via Chat API.

**Usage:**
```bash
python -m src.cli.invoke_agent "<prompt>" [--interactive]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| prompt | Yes (unless --interactive) | Natural language request |
| --interactive | No | Start interactive session for multi-turn conversation |

**Single-shot example:**
```bash
python -m src.cli.invoke_agent "List all tools with prefix GAF"
```

**Interactive example:**
```bash
python -m src.cli.invoke_agent --interactive
> Create a tool called GAF_GenAI_Test_Tool_v1
[Agent shows DRAFT]
> CONFIRM PUBLISH
[Agent publishes tool]
> exit
```

**Common prompts:**
- "List all tools" - Uses ListAssets tool
- "Get details for GAF_GenAI_ListAssets_Tool_v1" - Uses GetAsset tool
- "Create a tool called GAF_Product_Capability_Tool_v1 that does X" - Drafts new tool
- "Update GAF_GenAI_HelloWorld_Tool_v1 to change description" - Fetches and proposes update

---

### smoke_test.py

End-to-end verification of factory loop.

**Usage:**
```bash
python scripts/smoke_test.py
```

**What it tests:**
1. Invoke Factory Agent to draft HelloWorld tool
2. Send CONFIRM PUBLISH to create tool
3. Verify tool appears in asset list
4. Cleanup: Delete test tool

**Output (success):**
```
=== Smoke Test Started ===
Step 1: Draft... PASS
Step 2: Confirm... PASS
Step 3: Verify... PASS
Step 4: Cleanup... PASS
=== Smoke Test PASSED ===
```

**Output (failure):**
```
=== Smoke Test Started ===
Step 1: Draft... PASS
Step 2: Confirm... FAIL
ERROR: API returned 500 - Internal Server Error
```

**Exit codes:**
- 0: All steps passed
- 1: Test failed (details to stderr)

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| IONAPI_FILE | Yes | Path to .ionapi credentials file |
| LOG_LEVEL | No | Logging level (DEBUG, INFO, WARNING, ERROR). Default: INFO |

---

## Common Errors

### "Invalid name format"
**Cause:** Tool/agent name doesn't follow `GAF_<product>_<Capability>_(Tool|Agent)_v<N>` pattern.
**Fix:** Rename to match pattern exactly.

### "GUID required for update"
**Cause:** Using update_asset.py without "guid" field in spec.
**Fix:** Add "guid" field or use publish_tool.py for new assets.

### "Token acquisition failed"
**Cause:** Invalid .ionapi file or network issue.
**Fix:** Verify IONAPI_FILE path and file contents. Check network connectivity to Infor OS.

### "API returned 500"
**Cause:** Infor OS platform transient error.
**Fix:** Retry after a few seconds. If persistent, check Infor OS status.
