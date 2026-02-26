"""
Update the UpdateOrderDueDate_Tool with the correct API format
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

# Updated Tool 2 with correct API format (include GUID to update existing)
tool2_updated = {
    "guid": "43fb60c7-276d-4ad9-b25e-97f2e321cd8b",  # Existing tool GUID
    "name": "UpdateOrderDueDate_Tool",
    "description": "Update the due date for multiple customer order lines in SyteLine using batch update",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: POST
ENDPOINT: /update/SLCoitems

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>
Content-Type: application/json

Request Body (JSON):

The body must follow this exact structure for batch updates:

{
  "IDOName": "SLCoitems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 2,
      "ItemId": "PBT=[coitem] coi.DT=[...] coi.ID=[guid]",
      "Properties": [
        {
          "IsNull": false,
          "Modified": true,
          "Name": "DueDate",
          "Value": "YYYYMMDD"
        }
      ]
    }
  ]
}

CRITICAL: You MUST include ALL order lines in the Changes array. Each order line from the query results must have its own change object in the array.

Parameters:

IDOName: Always "SLCoitems" (STRING, Required)
RefreshAfterSave: Always true (BOOLEAN, Required)
Changes: Array of change objects (ARRAY, Required)

Each change object contains:
- Action: Always 2 for updates (INTEGER, Required)
- ItemId: The _ItemId from query results (STRING, Required)
- Properties: Array with one property object (ARRAY, Required)

Each property object contains:
- IsNull: Always false (BOOLEAN, Required)
- Modified: Always true (BOOLEAN, Required)
- Name: Always "DueDate" (STRING, Required)
- Value: New due date in YYYYMMDD format (STRING, Required)

Example for updating 3 order lines:

{
  "IDOName": "SLCoitems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 2,
      "ItemId": "PBT=[coitem] coi.DT=[2014-06-30 15:38:01.877] coi.ID=[guid1]",
      "Properties": [
        {
          "IsNull": false,
          "Modified": true,
          "Name": "DueDate",
          "Value": "20260126"
        }
      ]
    },
    {
      "Action": 2,
      "ItemId": "PBT=[coitem] coi.DT=[2014-06-30 15:38:01.877] coi.ID=[guid2]",
      "Properties": [
        {
          "IsNull": false,
          "Modified": true,
          "Name": "DueDate",
          "Value": "20260126"
        }
      ]
    },
    {
      "Action": 2,
      "ItemId": "PBT=[coitem] coi.DT=[2014-06-30 15:38:01.877] coi.ID=[guid3]",
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
}""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success of the batch update.

Example successful response:
{
  "Success": true,
  "Message": null,
  "Items": [...updated items...],
  "RowsAffected": 20
}

Example error response:
{
  "Success": false,
  "Message": "Error description",
  "Items": []
}

Key Response Fields:
- Success: Boolean indicating if the batch update succeeded
- Message: Error message if Success is false
- Items: Array of updated records
- RowsAffected: Total number of records successfully updated

HTTP Status Codes:
- 200 OK: Update processed (check Success field)
- 401 Unauthorized: Authentication failed
- 422 Validation Error: Invalid request format""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-3-7-sonnet-20250219-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [],
    "stubResponse": "",
    "instructions": """CRITICAL: Use this tool to update ALL order lines at once in a single batch operation.

Input structure:
- IDOName: "SLCoitems"
- RefreshAfterSave: true
- Changes: Array with one object per order line

For each order line:
- Action: 2
- ItemId: The _ItemId from query results
- Properties: Array with DueDate property

You MUST include ALL 20 order lines in the Changes array. Do NOT call this tool 20 times - call it ONCE with all 20 changes.

Date format: YYYYMMDD (e.g., "20260126")"""
}

print("Updating UpdateOrderDueDate_Tool with correct API format")
print("=" * 60)
print()

# Update the tool
response = requests.put(tools_url, headers=headers, json=tool2_updated)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    tool_response = response.json()
    print(f"[SUCCESS] Tool updated!")
    print(f"  Name: {tool_response.get('name')}")
    print(f"  GUID: {tool_response.get('guid')}")
else:
    print(f"[ERROR] Failed to update tool")
    print(f"Response: {response.text}")

print()
print("=" * 60)
