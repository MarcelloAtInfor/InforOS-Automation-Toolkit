"""
Create StartSimilarityWorkflow_Tool - Triggers ION workflows to re-train AI similarity models

Workflows:
- CSI_Item_similarity: Re-trains ItemName_Similarity_V2_CA model
- CSI_VendorName_similarity: Re-trains vendor name similarity model
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

# Tool definition
tool = {
    "name": "StartSimilarityWorkflow_Tool",
    "description": "Start ION workflows to re-train AI similarity models for vendor and item name matching",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "IONSERVICES/process/application",
        "api_docs": """Method: POST
Endpoint: /v1/workflow/start

Headers:
Content-Type: application/json

Query Parameters:

Parameter: logicalId
Format: STRING
Required: True
Description: Always use 'lid://infor.rpa.claudecode'

Body:
{
  "workflowName": "<workflow_name>",
  "instanceName": "<unique_instance_name>"
}

Supported Workflow Names:
- CSI_Item_similarity: Re-train item name matching model (use when new items are created)
- CSI_VendorName_similarity: Re-train vendor name matching model (use when new vendors are created)

Instance name should be unique - recommend using workflow name + timestamp (e.g., "VendorRetrain_20260131_143022")

Example request body:
{
  "workflowName": "CSI_VendorName_similarity",
  "instanceName": "VendorRetrain_20260131_143022"
}""",
        "headers": {},
        "responseInstructions": """The API responds with HTTP status indicating success or failure.

Success Response (HTTP 200):
- Empty body or JSON confirmation
- The workflow starts asynchronously in the background
- Do not wait for workflow completion - it runs independently

Error Responses:
- HTTP 400: Invalid request (check workflowName or instanceName)
- HTTP 404: Workflow not found (verify workflowName is exact)
- HTTP 401/403: Authentication issue

Key Points:
- Workflows run asynchronously - they will complete in the background
- No need to poll for status - just confirm the workflow was triggered
- Both workflows can be triggered in the same session if both vendor AND items were created""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [
        "Retrain similarity models",
        "Start model retraining workflow",
        "Update AI models",
        "Trigger vendor similarity training",
        "Trigger item similarity training"
    ],
    "stubResponse": "",
    "instructions": """Use this tool to trigger ION workflows that re-train AI similarity models.

WHEN TO USE:
- After creating a NEW vendor with VendorInsert_Tool_v2, trigger CSI_VendorName_similarity
- After creating NEW items with ItemInsert_Tool_v2, trigger CSI_Item_similarity
- Both workflows can be triggered in the same session if both types were created

PARAMETERS:
- workflowName: Exact workflow name (CSI_Item_similarity or CSI_VendorName_similarity)
- instanceName: Unique name using workflow + timestamp (e.g., "ItemRetrain_20260131_143022")
- logicalId: Always use "lid://infor.rpa.claudecode"

IMPORTANT:
- Only trigger if NEW entities were created (not if existing ones were found)
- Workflows run asynchronously - don't wait for completion
- Generate unique instanceName using current timestamp
- Report success/failure in the response but don't block on it"""
}

print("Creating StartSimilarityWorkflow_Tool")
print("=" * 60)
print(f"PUT {tools_url}\n")

# Save the tool definition for reference
tool_def_file = Path(__file__).parent / "similarity_workflow_tool_definition.json"
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
    response_file = Path(__file__).parent / "created_similarity_workflow_tool_response.json"
    with open(response_file, 'w') as f:
        json.dump(tool_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Failed to create tool")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
