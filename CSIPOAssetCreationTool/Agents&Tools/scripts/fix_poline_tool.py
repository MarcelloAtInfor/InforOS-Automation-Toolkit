import requests
import json
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# API endpoint and headers
headers = get_auth_headers()

# Updated PoLineInsert_Tool_v2 with simplified api_docs matching working tools
tool = {
    "guid": "901ce71a-5e5f-4802-9142-5b4a98ab1945",
    "name": "PoLineInsert_Tool_v2",
    "description": "Create purchase order line items in SyteLine (supports batch insert of multiple lines)",
    "type": "API_DOCS",
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: POST
Endpoint: /update/SLPoItems

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Body:
The body contains PO line item details in the Changes array.

CRITICAL: This endpoint uses the IDOName/Changes structure.
CRITICAL: Insert ALL line items for a PO in a SINGLE API call.

Single line example:
{
  "IDOName": "SLPoItems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 1,
      "Properties": [
        {"IsNull": false, "Modified": true, "Name": "PoNum", "Value": "DP00009000"},
        {"IsNull": false, "Modified": true, "Name": "PoLine", "Value": "1"},
        {"IsNull": false, "Modified": true, "Name": "Item", "Value": "WIDGET-A"},
        {"IsNull": false, "Modified": true, "Name": "QtyOrderedConv", "Value": "10.00"},
        {"IsNull": false, "Modified": true, "Name": "UM", "Value": "EA"},
        {"IsNull": false, "Modified": true, "Name": "Stat", "Value": "O"},
        {"IsNull": false, "Modified": true, "Name": "DueDate", "Value": "2026-02-27"},
        {"IsNull": false, "Modified": true, "Name": "Whse", "Value": "MAIN"}
      ]
    }
  ]
}

BATCH insert (multiple lines in one call):
{
  "IDOName": "SLPoItems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 1,
      "Properties": [
        {"IsNull": false, "Modified": true, "Name": "PoNum", "Value": "DP00009000"},
        {"IsNull": false, "Modified": true, "Name": "PoLine", "Value": "1"},
        {"IsNull": false, "Modified": true, "Name": "Item", "Value": "WIDGET-A"},
        {"IsNull": false, "Modified": true, "Name": "QtyOrderedConv", "Value": "10.00"},
        {"IsNull": false, "Modified": true, "Name": "UM", "Value": "EA"},
        {"IsNull": false, "Modified": true, "Name": "Stat", "Value": "O"},
        {"IsNull": false, "Modified": true, "Name": "DueDate", "Value": "2026-02-27"},
        {"IsNull": false, "Modified": true, "Name": "Whse", "Value": "MAIN"}
      ]
    },
    {
      "Action": 1,
      "Properties": [
        {"IsNull": false, "Modified": true, "Name": "PoNum", "Value": "DP00009000"},
        {"IsNull": false, "Modified": true, "Name": "PoLine", "Value": "2"},
        {"IsNull": false, "Modified": true, "Name": "Item", "Value": "GADGET-B"},
        {"IsNull": false, "Modified": true, "Name": "QtyOrderedConv", "Value": "5.00"},
        {"IsNull": false, "Modified": true, "Name": "UM", "Value": "EA"},
        {"IsNull": false, "Modified": true, "Name": "Stat", "Value": "O"},
        {"IsNull": false, "Modified": true, "Name": "DueDate", "Value": "2026-02-27"},
        {"IsNull": false, "Modified": true, "Name": "Whse", "Value": "MAIN"}
      ]
    }
  ]
}

Field Definitions:
Action: Integer, 1 = insert
PoNum: STRING, PO number (must exist)
PoLine: STRING, line number ("1", "2", etc.)
Item: STRING, item code (must exist)
QtyOrderedConv: STRING, quantity as decimal (e.g., "10.00")
UM: STRING, unit of measure
Stat: STRING, status (default: "O" for ordered)
DueDate: STRING, format "YYYY-MM-DD" (e.g., "2026-02-27")
Whse: STRING, warehouse (must match PO's warehouse)

IMPORTANT:
- Insert ALL line items in ONE API call
- Use multiple objects in Changes array for batch insert
- DueDate format is "YYYY-MM-DD"
- QtyOrderedConv must include decimals (e.g., "10.00")
- All Properties listed above must be included for each line""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success or failure.

Example successful response:
{
  "Success": true,
  "Message": null,
  "RefreshItems": [...]
}

Example error response:
{
  "Success": false,
  "Message": "Error details",
  "RefreshItems": null
}

Key Response Fields:
- Success: Boolean indicating if insert succeeded
- Message: Error message if Success is false
- RefreshItems: Array with created PO line records""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "instructions": """Use this tool to create PO line items in SyteLine.

CRITICAL: Insert ALL line items for a PO in a SINGLE API call!
Build the complete Changes array with all lines before calling this tool.

Required fields (for each line):
- PoNum: PO number
- PoLine: Line number as string ("1", "2", etc.)
- Item: Item code
- QtyOrderedConv: Quantity with decimals (e.g., "10.00")
- UM: Unit of measure
- Stat: Default "O" (ordered)
- DueDate: Format "YYYY-MM-DD" (e.g., "2026-02-27")
- Whse: Warehouse (must match PO's warehouse)

If DueDate not provided, default to 30 days from today.

Returns success status and created line items."""
}

print("Updating PoLineInsert_Tool_v2...")
print(f"GUID: {tool['guid']}")

# Update the tool via PUT
response = requests.put(f'{GENAI_CORE_URL()}/api/v1/tools', headers=headers, json=tool)

if response.status_code == 200:
    print("SUCCESS: Updated PoLineInsert_Tool_v2")
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Tool Name: {result.get('name')}")
    print(f"Tool GUID: {result.get('guid')}")
    print(f"Status: {'Enabled' if result.get('status') == 1 else 'Disabled'}")
    print("\nSimplified api_docs format to match working tools (ItemInsert, PoInsert)")
else:
    print(f"FAILED: Could not update tool")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
