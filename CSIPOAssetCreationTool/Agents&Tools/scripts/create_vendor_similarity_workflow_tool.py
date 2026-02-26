"""
Create StartVendorNameSimilarityWorkflow_Tool - Triggers ION workflow to re-train vendor name similarity model

Hardcoded to CSI_VendorName_similarity workflow to avoid LLM URL malformation issues.
This is a simplified version split from the original StartSimilarityWorkflow_Tool.
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# API endpoint
tools_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

# Tool definition - simplified api_docs to avoid LLM URL malformation
tool = {
    "name": "StartVendorNameSimilarityWorkflow_Tool",
    "description": "Start ION workflow to re-train AI vendor name similarity model (CSI_VendorName_similarity)",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "IONSERVICES/process/application",
        "api_docs": """Method: POST
Endpoint: /v1/workflow/start?logicalId=lid://infor.rpa.claudecode

Headers:
Content-Type: application/json

Body:
{
  "workflowName": "CSI_VendorName_similarity",
  "instanceName": "<unique_instance_name>"
}

The instanceName should be unique - use format: VendorRetrain_YYYYMMDD_HHMMSS (e.g., "VendorRetrain_20260131_143022")""",
        "headers": {},
        "responseInstructions": """The API responds with HTTP status indicating success or failure.

Success Response (HTTP 200):
- Empty body or JSON confirmation
- The workflow starts asynchronously in the background
- Do not wait for workflow completion - it runs independently

Error Responses:
- HTTP 400: Invalid request (check instanceName format)
- HTTP 404: Workflow not found
- HTTP 401/403: Authentication issue

Key Points:
- Workflow runs asynchronously - it will complete in the background
- No need to poll for status - just confirm the workflow was triggered""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [
        "Retrain vendor similarity model",
        "Start vendor model retraining",
        "Trigger vendor name similarity training"
    ],
    "stubResponse": "",
    "instructions": """Use this tool to trigger the CSI_VendorName_similarity workflow that re-trains the AI vendor name similarity model.

WHEN TO USE:
- After creating a NEW vendor with VendorInsert_Tool_v2
- Only trigger if a new vendor was actually CREATED (not just found by search)

PARAMETERS:
- instanceName: Unique name using format VendorRetrain_YYYYMMDD_HHMMSS (e.g., "VendorRetrain_20260131_143022")

IMPORTANT:
- The workflowName is hardcoded to "CSI_VendorName_similarity"
- The logicalId is hardcoded in the query string
- Workflow runs asynchronously - don't wait for completion
- Generate unique instanceName using current timestamp
- Report success/failure in the response but don't block on it"""
}

print("Creating StartVendorNameSimilarityWorkflow_Tool")
print("=" * 60)
print(f"PUT {tools_url}\n")

# Save the tool definition for reference
tool_def_file = Path(__file__).parent / "vendor_similarity_workflow_tool_definition.json"
with open(tool_def_file, 'w') as f:
    json.dump(tool, f, indent=2)
print(f"Tool definition saved to: {tool_def_file}")

# Create the tool
response = requests.put(tools_url, headers=headers, json=tool)

print(f"\nStatus Code: {response.status_code}\n")

if response.status_code == 200:
    tool_response = response.json()
    print(f"[SUCCESS] Tool created successfully!\n")
    print(f"Tool Name: {tool_response.get('name')}")
    print(f"Tool GUID: {tool_response.get('guid')}")
    print(f"Type: {tool_response.get('type')}")
    print(f"Status: {'Enabled' if tool_response.get('status') == 1 else 'Disabled'}")

    # Update the definition file with the GUID from the response
    tool['guid'] = tool_response.get('guid')
    with open(tool_def_file, 'w') as f:
        json.dump(tool, f, indent=2)

    # Save the full response
    response_file = Path(__file__).parent / "created_vendor_similarity_workflow_tool_response.json"
    with open(response_file, 'w') as f:
        json.dump(tool_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Failed to create tool")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
