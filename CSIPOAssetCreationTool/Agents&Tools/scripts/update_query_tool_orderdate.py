"""
Update QueryUpcomingOrders_Tool to order by CoOrderDate DESC (latest first)
instead of DueDate ASC (earliest first)
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

# Updated Tool 1 with CoOrderDate DESC ordering
tool1_updated = {
    "guid": "fb99c0c4-eaf0-4683-a823-0dba3e512113",  # Existing tool GUID
    "name": "QueryUpcomingOrders_Tool",
    "description": "Retrieve the 20 most recent customer order lines from SyteLine (Ordered status only, sorted by order date)",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: GET
ENDPOINT: /load/SLCoitems

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties to return. Required fields: CoNum, CoLine, Item, DueDate, QtyOrderedConv, Stat, CoOrderDate, _ItemId

Parameter: filter
Format: STRING
Required: True
Description: Filter to only include order lines with Ordered status. Use: Stat='O'

Parameter: orderBy
Format: STRING
Required: True
Description: Sort order for results. Use 'CoOrderDate DESC' to get lines from most recent orders first

Parameter: recordCap
Format: INTEGER
Required: True
Description: Maximum number of records to return. Use 20 to get the 20 most recent order lines

Example Request:

To get the 20 most recent order lines (Ordered status only):
/load/SLCoitems?properties=CoNum,CoLine,Item,DueDate,QtyOrderedConv,Stat,CoOrderDate,_ItemId&filter=Stat='O'&orderBy=CoOrderDate DESC&recordCap=20

Response Format:
The DueDate field is returned in format: YYYYMMDD HH:MM:SS.mmm (e.g., "20161205 00:00:00.000")
The CoOrderDate field is returned in format: YYYYMMDD HH:MM:SS.mmm (e.g., "20161114 00:00:00.000")
The Stat field shows order status: 'O'=Ordered, 'C'=Complete, 'P'=Planned""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object containing an Items array with order line details.

Example response:
{
  "Items": [
    {
      "CoNum": "DC00000106",
      "CoLine": "1",
      "Item": "FA-10000",
      "DueDate": "20161205 00:00:00.000",
      "CoOrderDate": "20161114 00:00:00.000",
      "QtyOrderedConv": "100.00000000",
      "Stat": "O",
      "_ItemId": "PBT=[coitem] coi.DT=[2014-09-09 15:09:03.160] coi.ID=[8b03ec75-871e-4207-b700-caefc63ba779]"
    }
  ],
  "MoreRowsExist": false,
  "Success": true,
  "Message": null
}

Key Response Fields:
- Items: Array of order line objects sorted by CoOrderDate descending (latest first), filtered to Stat='O' only
- CoNum: Customer order number
- CoLine: Line number within the order
- DueDate: Due date in YYYYMMDD HH:MM:SS.mmm format
- CoOrderDate: Order date in YYYYMMDD HH:MM:SS.mmm format
- Stat: Order status (will always be 'O' for Ordered due to filter)
- _ItemId: Required for updates (identifies the specific record)
- MoreRowsExist: Boolean indicating if more records are available
- Success: Boolean indicating API call success""",
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
    "instructions": """Use this tool to retrieve the 20 most recent customer order lines based on order date.

IMPORTANT:
- Only returns order lines with Stat='O' (Ordered status)
- Sorted by CoOrderDate DESC (most recent orders first, not due date)

Returns: Order number, line number, item, due date, order date, quantity, status, and item ID for each line.

The results are automatically sorted by order date (newest first), filtered to Ordered status only, and limited to 20 records.

Use when the user asks to:
- Get recent order lines
- Find most recently placed orders
- Retrieve order lines for due date updates
- Check latest orders"""
}

print("Updating QueryUpcomingOrders_Tool to order by CoOrderDate DESC")
print("=" * 60)
print()

# Update the tool
response = requests.put(tools_url, headers=headers, json=tool1_updated)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    tool_response = response.json()
    print(f"[SUCCESS] Tool updated!")
    print(f"  Name: {tool_response.get('name')}")
    print(f"  GUID: {tool_response.get('guid')}")
    print(f"  Ordering: Now uses CoOrderDate DESC (latest first)")
    print(f"  Filter: Stat='O' (Ordered status only)")
else:
    print(f"[ERROR] Failed to update tool")
    print(f"Response: {response.text}")

print()
print("=" * 60)
