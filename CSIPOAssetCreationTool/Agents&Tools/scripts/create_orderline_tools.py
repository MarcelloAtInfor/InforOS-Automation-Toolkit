"""
Create two GenAI tools for the weekly order line due date update workflow:
1. QueryUpcomingOrders_Tool - Get 20 order lines with soonest due dates
2. UpdateOrderDueDate_Tool - Update due date for specific order lines
"""
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# API endpoint
tools_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

# Tool 1: Query upcoming order lines
tool1 = {
    "name": "QueryUpcomingOrders_Tool",
    "description": "Retrieve the 20 customer order lines with the soonest upcoming due dates from SyteLine",
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
Description: Comma-separated list of properties to return. Required fields: CoNum, CoLine, Item, DueDate, QtyOrderedConv, Stat, _ItemId

Parameter: orderBy
Format: STRING
Required: True
Description: Sort order for results. Use 'DueDate ASC' to get lines with soonest due dates first

Parameter: recordCap
Format: INTEGER
Required: True
Description: Maximum number of records to return. Use 20 to get the 20 soonest due date lines

Example Request:

To get the 20 order lines with soonest due dates:
/load/SLCoitems?properties=CoNum,CoLine,Item,DueDate,QtyOrderedConv,Stat,_ItemId&orderBy=DueDate ASC&recordCap=20

Response Format:
The DueDate field is returned in format: YYYYMMDD HH:MM:SS.mmm (e.g., "20161205 00:00:00.000")""",
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
      "QtyOrderedConv": "100.00000000",
      "Stat": "C",
      "_ItemId": "PBT=[coitem] coi.DT=[2014-09-09 15:09:03.160] coi.ID=[8b03ec75-871e-4207-b700-caefc63ba779]"
    }
  ],
  "MoreRowsExist": false,
  "Success": true,
  "Message": null
}

Key Response Fields:
- Items: Array of order line objects sorted by DueDate ascending
- CoNum: Customer order number
- CoLine: Line number within the order
- DueDate: Due date in YYYYMMDD HH:MM:SS.mmm format
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
    "instructions": """Use this tool to retrieve the 20 customer order lines with the soonest upcoming due dates.

Returns: Order number, line number, item, due date, quantity, status, and item ID for each line.

The results are automatically sorted by due date (earliest first) and limited to 20 records.

Use when the user asks to:
- Get upcoming order lines
- Find orders with soonest due dates
- Retrieve order lines for due date updates
- Check which orders are coming due soon"""
}

# Tool 2: Update order line due date
tool2 = {
    "name": "UpdateOrderDueDate_Tool",
    "description": "Update the due date for specific customer order lines in SyteLine",
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

The body must be a JSON object with an "SLCoitems" array containing update operations.

Parameter: _ItemId
Format: STRING
Required: True
Description: The unique identifier for the order line record (obtained from query results)

Parameter: DueDate
Format: STRING
Required: True
Description: New due date in YYYYMMDD format (e.g., "20260125" for January 25, 2026)

Example Request Body:

{
  "SLCoitems": [
    {
      "_ItemId": "PBT=[coitem] coi.DT=[2014-09-09 15:09:03.160] coi.ID=[8b03ec75-871e-4207-b700-caefc63ba779]",
      "DueDate": "20260125"
    }
  ]
}

To update multiple lines at once, include multiple objects in the SLCoitems array:

{
  "SLCoitems": [
    {
      "_ItemId": "PBT=[coitem] coi.DT=[...] coi.ID=[guid1]",
      "DueDate": "20260125"
    },
    {
      "_ItemId": "PBT=[coitem] coi.DT=[...] coi.ID=[guid2]",
      "DueDate": "20260125"
    }
  ]
}

Important Notes:
- The _ItemId must match exactly as returned from the query
- DueDate format is YYYYMMDD (8 digits, no separators or time portion)
- The API will validate the date format and return an error if invalid""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success or failure of the update.

Example successful response:
{
  "Items": [
    {
      "_ItemId": "PBT=[coitem] coi.DT=[...] coi.ID=[guid]",
      "DueDate": "20260125 00:00:00.000"
    }
  ],
  "Success": true,
  "Message": null,
  "RowsAffected": 1
}

Example error response:
{
  "Success": false,
  "Message": "Invalid date format",
  "Items": []
}

Key Response Fields:
- Success: Boolean indicating if the update succeeded
- Message: Error message if Success is false, null otherwise
- Items: Array of updated records (may be empty on error)
- RowsAffected: Number of records successfully updated

HTTP Status Codes:
- 200 OK: Update processed (check Success field for actual result)
- 401 Unauthorized: Authentication failed
- 422 Validation Error: Invalid request body or parameters""",
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
    "instructions": """Use this tool to update the due date for customer order lines.

Input requirements:
- _ItemId: The unique record identifier (from query results)
- DueDate: New date in YYYYMMDD format (e.g., "20260125")

Can update single or multiple order lines in one request.

Use when the user asks to:
- Update due dates for order lines
- Change when orders are due
- Set new due dates
- Modify order line due dates"""
}

print("Creating Order Line Management Tools")
print("=" * 60)
print()

# Create Tool 1
print("Creating Tool 1: QueryUpcomingOrders_Tool")
print("-" * 60)
response1 = requests.put(tools_url, headers=headers, json=tool1)
print(f"Status Code: {response1.status_code}")

if response1.status_code == 200:
    tool1_response = response1.json()
    print(f"[SUCCESS] Tool 1 created!")
    print(f"  Name: {tool1_response.get('name')}")
    print(f"  GUID: {tool1_response.get('guid')}")
else:
    print(f"[ERROR] Failed to create Tool 1")
    print(f"Response: {response1.text}")

print()

# Create Tool 2
print("Creating Tool 2: UpdateOrderDueDate_Tool")
print("-" * 60)
response2 = requests.put(tools_url, headers=headers, json=tool2)
print(f"Status Code: {response2.status_code}")

if response2.status_code == 200:
    tool2_response = response2.json()
    print(f"[SUCCESS] Tool 2 created!")
    print(f"  Name: {tool2_response.get('name')}")
    print(f"  GUID: {tool2_response.get('guid')}")
else:
    print(f"[ERROR] Failed to create Tool 2")
    print(f"Response: {response2.text}")

print()
print("=" * 60)

# Save tool definitions for reference
if response1.status_code == 200 and response2.status_code == 200:
    tools_file = Path(__file__).parent / "orderline_tools.json"
    with open(tools_file, 'w') as f:
        json.dump({
            "QueryUpcomingOrders_Tool": tool1_response,
            "UpdateOrderDueDate_Tool": tool2_response
        }, f, indent=2)
    print(f"\n[SUCCESS] Tool details saved to: {tools_file}")
