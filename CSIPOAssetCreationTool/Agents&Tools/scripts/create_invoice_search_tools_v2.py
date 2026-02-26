"""
Create three GenAI search tools for invoice automation (v2):
1. VendorSearch_Tool_v2 - Search for existing vendors
2. ItemSearch_Tool_v2 - Search for existing items
3. PoSearch_Tool_v2 - Search for existing purchase orders
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

# Tool 1: Vendor Search
tool1 = {
    "name": "VendorSearch_Tool_v2",
    "description": "Search for existing vendors in SyteLine by vendor name or vendor number",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: GET
ENDPOINT: /load/SLVendors

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties to return. Required fields: VendNum, Name, VadAddr_1, VadCity, VadState, VadZip, VadPhone, VadEmail, _ItemId

Parameter: filter
Format: STRING
Required: False
Description: SQL WHERE clause to filter results. Use 'VendNum = \"VENDOR123\"' for exact match or 'Name LIKE \"%ACME%\"' for partial name match

Parameter: recordCap
Format: INTEGER
Required: False
Description: Maximum number of records to return. Default: 10

Example Requests:

Search by vendor number (exact match):
/load/SLVendors?properties=VendNum,Name,VadAddr_1,VadCity,VadState,VadZip,VadPhone,VadEmail,_ItemId&filter=VendNum = "DEMO001"

Search by vendor name (partial match):
/load/SLVendors?properties=VendNum,Name,VadAddr_1,VadCity,VadState,VadZip,VadPhone,VadEmail,_ItemId&filter=Name LIKE "%ACME%"&recordCap=10

Response Format:
Returns JSON with Items array containing vendor records""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object containing an Items array with vendor details.

Example response:
{
  "Items": [
    {
      "VendNum": "DEMO001",
      "Name": "ACME Corporation",
      "VadAddr_1": "123 Main St",
      "VadCity": "Chicago",
      "VadState": "IL",
      "VadZip": "60601",
      "VadPhone": "312-555-0100",
      "VadEmail": "ap@acme.com",
      "_ItemId": "PBT=[vendor] ven.DT=[...] ven.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null
}

Key Response Fields:
- Items: Array of vendor objects (empty if not found)
- VendNum: Vendor number (7 char max, unique identifier)
- Name: Vendor name
- _ItemId: Record identifier for updates
- Success: Boolean indicating API call success

If no vendors match the search criteria, Items will be an empty array.""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [],
    "stubResponse": "",
    "instructions": """Use this tool to search for existing vendors before creating new ones.

Search options:
- By vendor number (exact match): filter=VendNum = "VENDOR123"
- By vendor name (partial match): filter=Name LIKE "%company name%"

Returns vendor details if found, empty Items array if not found.

Use when you need to:
- Check if a vendor already exists
- Look up vendor number by name
- Verify vendor information before inserting"""
}

# Tool 2: Item Search
tool2 = {
    "name": "ItemSearch_Tool_v2",
    "description": "Search for existing items in SyteLine by item code or description",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: GET
ENDPOINT: /load/SLItems

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties to return. Required fields: Item, Description, UM, ProductCode, _ItemId

Parameter: filter
Format: STRING
Required: False
Description: SQL WHERE clause to filter results. Use 'Item = \"ITEM-CODE\"' for exact match or 'Description LIKE \"%widget%\"' for partial description match

Parameter: recordCap
Format: INTEGER
Required: False
Description: Maximum number of records to return. Default: 10

Example Requests:

Search by item code (exact match):
/load/SLItems?properties=Item,Description,UM,ProductCode,_ItemId&filter=Item = "WIDGET-A"

Search by description (partial match):
/load/SLItems?properties=Item,Description,UM,ProductCode,_ItemId&filter=Description LIKE "%Premium Widget%"&recordCap=10

Response Format:
Returns JSON with Items array containing item records""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object containing an Items array with item details.

Example response:
{
  "Items": [
    {
      "Item": "WIDGET-A",
      "Description": "Premium Widget Type A",
      "UM": "EA",
      "ProductCode": "FG-100",
      "_ItemId": "PBT=[item] itm.DT=[...] itm.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null
}

Key Response Fields:
- Items: Array of item objects (empty if not found)
- Item: Item code (unique identifier)
- Description: Item description
- UM: Unit of measure (e.g., EA, LB, BOX)
- _ItemId: Record identifier for updates
- Success: Boolean indicating API call success

If no items match the search criteria, Items will be an empty array.""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [],
    "stubResponse": "",
    "instructions": """Use this tool to search for existing items before creating new ones.

Search options:
- By item code (exact match): filter=Item = "ITEM-CODE"
- By description (partial match): filter=Description LIKE "%text%"

Returns item details if found, empty Items array if not found.

Use when you need to:
- Check if an item already exists
- Look up item code by description
- Verify item information before inserting"""
}

# Tool 3: Purchase Order Search
tool3 = {
    "name": "PoSearch_Tool_v2",
    "description": "Search for existing purchase orders in SyteLine by PO number",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: GET
ENDPOINT: /load/SLPos

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties to return. Required fields: PoNum, VendNum, OrderDate, Whse, Stat, _ItemId

Parameter: filter
Format: STRING
Required: True
Description: SQL WHERE clause to filter by PO number. Use 'PoNum = \"PO-NUMBER\"' for exact match

Parameter: recordCap
Format: INTEGER
Required: False
Description: Maximum number of records to return. Default: 1 (should only find one PO by number)

Example Request:

Search by PO number:
/load/SLPos?properties=PoNum,VendNum,OrderDate,Whse,Stat,_ItemId&filter=PoNum = "DP00009000"&recordCap=1

Response Format:
Returns JSON with Items array containing PO record (or empty if not found)""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object containing an Items array with PO details.

Example response:
{
  "Items": [
    {
      "PoNum": "DP00009000",
      "VendNum": "DEMO001",
      "OrderDate": "20260128 00:00:00.000",
      "Whse": "MAIN",
      "Stat": "O",
      "_ItemId": "PBT=[po] po.DT=[...] po.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null
}

Key Response Fields:
- Items: Array with PO object (empty if not found)
- PoNum: Purchase order number (10 char, unique)
- VendNum: Vendor number associated with PO
- OrderDate: PO order date
- Whse: Warehouse
- Stat: Status (O=Open, C=Complete, etc.)
- _ItemId: Record identifier for updates
- Success: Boolean indicating API call success

If no PO matches the search criteria, Items will be an empty array.""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [],
    "stubResponse": "",
    "instructions": """Use this tool to search for existing purchase orders before creating new ones.

Search by PO number (exact match): filter=PoNum = "PO-NUMBER"

Returns PO details if found, empty Items array if not found.

Use when you need to:
- Check if a PO number is already in use
- Verify PO doesn't exist before creating
- Look up existing PO information"""
}

print("Creating Invoice Automation Search Tools (v2)")
print("=" * 60)
print()

# Create Tool 1: VendorSearch
print("Creating Tool 1: VendorSearch_Tool_v2")
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

# Create Tool 2: ItemSearch
print("Creating Tool 2: ItemSearch_Tool_v2")
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

# Create Tool 3: PoSearch
print("Creating Tool 3: PoSearch_Tool_v2")
print("-" * 60)
response3 = requests.put(tools_url, headers=headers, json=tool3)
print(f"Status Code: {response3.status_code}")

if response3.status_code == 200:
    tool3_response = response3.json()
    print(f"[SUCCESS] Tool 3 created!")
    print(f"  Name: {tool3_response.get('name')}")
    print(f"  GUID: {tool3_response.get('guid')}")
else:
    print(f"[ERROR] Failed to create Tool 3")
    print(f"Response: {response3.text}")

print()
print("=" * 60)

# Save tool definitions for reference
if response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200:
    tools_file = Path(__file__).parent / "invoice_search_tools_v2.json"
    with open(tools_file, 'w') as f:
        json.dump({
            "VendorSearch_Tool_v2": tool1_response,
            "ItemSearch_Tool_v2": tool2_response,
            "PoSearch_Tool_v2": tool3_response
        }, f, indent=2)
    print(f"\n[SUCCESS] Tool details saved to: {tools_file}")
