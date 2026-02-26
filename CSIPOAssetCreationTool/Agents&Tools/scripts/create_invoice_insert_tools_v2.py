"""
Create four GenAI insert tools for invoice automation (v2):
1. VendorInsert_Tool_v2 - Create new vendors
2. ItemInsert_Tool_v2 - Create new items (with Description added)
3. PoInsert_Tool_v2 - Create new purchase orders (with VendNum added)
4. PoLineInsert_Tool_v2 - Create PO line items (batch capable)
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

# Tool 1: Vendor Insert
tool1 = {
    "guid": "76ad5987-6071-45b8-a059-a649ded28ecb",  # Existing tool GUID for update
    "name": "VendorInsert_Tool_v2",
    "description": "Create a new vendor in SyteLine with comprehensive vendor information",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: POST
Endpoint: /update/SLVendors

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Body:
The body contains vendor details in the Changes array:

{
  "IDOName": "SLVendors",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 1,
      "Properties": [
        {"IsNull": false, "Modified": true, "Name": "VendNum", "Value": "DEMO001"},
        {"IsNull": false, "Modified": true, "Name": "Name", "Value": "ACME Corporation"},
        {"IsNull": false, "Modified": true, "Name": "VadAddr_1", "Value": "123 Main St"},
        {"IsNull": false, "Modified": true, "Name": "VadCity", "Value": "Chicago"},
        {"IsNull": false, "Modified": true, "Name": "VadStateCode", "Value": "IL"},
        {"IsNull": false, "Modified": true, "Name": "VadZip", "Value": "60601"},
        {"IsNull": false, "Modified": true, "Name": "VadCountry", "Value": "USA"},
        {"IsNull": false, "Modified": true, "Name": "TermsCode", "Value": "N30"},
        {"IsNull": false, "Modified": true, "Name": "CurrCode", "Value": "USD"},
        {"IsNull": false, "Modified": true, "Name": "BankCode", "Value": "BK1"},
        {"IsNull": false, "Modified": true, "Name": "AutoVoucherMethod", "Value": "P"}
      ]
    }
  ]
}

NOTE: Action 1 means insert. VendNum must be exactly 7 characters (pad with zeros). All properties above are required.""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success or failure.

Example successful response:
{
  "Items": [
    {
      "VendNum": "DEMO001",
      "Name": "ACME Corporation",
      "_ItemId": "PBT=[vendor] ven.DT=[...] ven.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null
}

Example error response (duplicate VendNum):
{
  "Success": false,
  "Message": "Vendor number already exists",
  "Items": []
}

Key Response Fields:
- Success: Boolean indicating if insert succeeded
- Message: Error message if Success is false
- Items: Array with created vendor record (includes _ItemId)
- _ItemId: Unique identifier for the created vendor""",
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
    "instructions": """Use this tool to create a new vendor in SyteLine.

IMPORTANT: Always use VendorSearch_Tool_v2 first to ensure the vendor doesn't already exist!

Required fields:
- VendNum: EXACTLY 7 chars, unique (pad with zeros: "MWF" → "MWF0001")
- Name: Vendor name
- VadAddr_1: Address
- VadCity, VadStateCode, VadZip: Location
- VadCountry: Default "USA"
- TermsCode: Payment terms (N30, N45, COD, 2%, 4%, TBD)
- CurrCode: Default "USD"
- BankCode: Default "BK1"
- AutoVoucherMethod: Default "P"

Returns the created vendor with VendNum and _ItemId."""
}

# Tool 2: Item Insert (with Description added!)
tool2 = {
    "guid": "2762bfa4-f36b-4bb9-9228-310030487cee",  # Existing tool GUID for update
    "name": "ItemInsert_Tool_v2",
    "description": "Create a new item in SyteLine with item code, description, material cost, and sourcing",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: POST
Endpoint: /update/SLItems

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Body:
The body contains item details in the Changes array:

{
  "IDOName": "SLItems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 1,
      "Properties": [
        {"IsNull": false, "Modified": true, "Name": "Item", "Value": "ITEM-CODE"},
        {"IsNull": false, "Modified": true, "Name": "Description", "Value": "Item Description"},
        {"IsNull": false, "Modified": true, "Name": "UM", "Value": "EA"},
        {"IsNull": false, "Modified": true, "Name": "MatlType", "Value": "M"},
        {"IsNull": false, "Modified": true, "Name": "PMTCode", "Value": "M"},
        {"IsNull": false, "Modified": true, "Name": "ProductCode", "Value": "FG-100"},
        {"IsNull": false, "Modified": true, "Name": "AbcCode", "Value": "B"},
        {"IsNull": false, "Modified": true, "Name": "CostType", "Value": "A"},
        {"IsNull": false, "Modified": true, "Name": "CostMethod", "Value": "S"},
        {"IsNull": false, "Modified": true, "Name": "Stat", "Value": "A"},
        {"IsNull": false, "Modified": true, "Name": "Source", "Value": "P"},
        {"IsNull": false, "Modified": true, "Name": "CurMatCost", "Value": "0.00"}
      ]
    }
  ]
}

NOTE: Action 1 means insert. Source="P" indicates Purchased item. CurMatCost should be set to the unit price from the invoice.""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success or failure.

Example successful response:
{
  "Items": [
    {
      "Item": "WIDGET-A",
      "Description": "Premium Widget Type A",
      "UM": "EA",
      "Source": "P",
      "CurMatCost": "0.00",
      "_ItemId": "PBT=[item] itm.DT=[...] itm.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null
}

Example error response (duplicate Item):
{
  "Success": false,
  "Message": "Item code already exists",
  "Items": []
}

Key Response Fields:
- Success: Boolean indicating if insert succeeded
- Message: Error message if Success is false
- Items: Array with created item record (includes _ItemId)
- _ItemId: Unique identifier for the created item""",
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
    "instructions": """Use this tool to create a new item in SyteLine.

IMPORTANT: Always use ItemSearch_Tool_v2 first to ensure the item doesn't already exist!

Required fields:
- Item: Item code (unique)
- Description: Item description (CRITICAL - was missing in v1!)
- UM: Unit of measure (EA, LB, BOX, etc.)
- MatlType: Default "M"
- PMTCode: Default "M"
- ProductCode: Product code
- AbcCode: Default "B"
- CostType: Default "A"
- CostMethod: Default "S"
- Stat: Default "A" (active)
- Source: Set to "P" (Purchased) for all invoice-created items
- CurMatCost: Material cost from invoice unit price (e.g., "125.50")

Returns the created item with Item code and _ItemId."""
}

# Tool 3: PO Insert (with VendNum added!)
tool3 = {
    "guid": "4ed7b512-6fec-4c20-b69d-3b9598c69ecf",  # Existing tool GUID for update
    "name": "PoInsert_Tool_v2",
    "description": "Create a new purchase order in SyteLine linked to a vendor",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: POST
Endpoint: /update/SLPOs

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Body:
The body contains PO details in the Changes array:

{
  "IDOName": "SLPOs",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 1,
      "Properties": [
        {"IsNull": false, "Modified": true, "Name": "PoNum", "Value": "DP00009000"},
        {"IsNull": false, "Modified": true, "Name": "VendNum", "Value": "DEMO001"},
        {"IsNull": false, "Modified": true, "Name": "TermsCode", "Value": "N30"},
        {"IsNull": false, "Modified": true, "Name": "Stat", "Value": "O"},
        {"IsNull": false, "Modified": true, "Name": "Type", "Value": "R"},
        {"IsNull": false, "Modified": true, "Name": "Whse", "Value": "MAIN"},
        {"IsNull": false, "Modified": true, "Name": "PoCurrCode", "Value": "USD"}
      ]
    }
  ]
}

NOTE: Action 1 means insert. PoNum must be exactly 10 characters. VendNum links PO to vendor.""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success or failure.

Example successful response:
{
  "Items": [
    {
      "PoNum": "DP00009000",
      "VendNum": "DEMO001",
      "Stat": "O",
      "_ItemId": "PBT=[po] po.DT=[...] po.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null
}

Example error response (duplicate PoNum):
{
  "Success": false,
  "Message": "Purchase order number already exists",
  "Items": []
}

Example error response (invalid VendNum):
{
  "Success": false,
  "Message": "Vendor not found",
  "Items": []
}

Key Response Fields:
- Success: Boolean indicating if insert succeeded
- Message: Error message if Success is false
- Items: Array with created PO record (includes _ItemId)
- _ItemId: Unique identifier for the created PO""",
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
    "instructions": """Use this tool to create a new purchase order in SyteLine.

IMPORTANT: Always use PoSearch_Tool_v2 first to ensure the PO doesn't already exist!

Required fields:
- PoNum: Exactly 10 characters, unique
- VendNum: Vendor number - EXACTLY 7 chars (CRITICAL - was missing in v1!)
- TermsCode: Payment terms (N30, N45, COD, etc.)
- Stat: Default "O" (open)
- Type: Default "R" (regular)
- Whse: Warehouse (MAIN, etc.)
- PoCurrCode: Default "USD"

The VendNum must come from a vendor that was either:
1. Created using VendorInsert_Tool_v2
2. Found using VendorSearch_Tool_v2

Returns the created PO with PoNum and _ItemId."""
}

# Tool 4: PO Line Insert (batch capable)
tool4 = {
    "guid": "901ce71a-5e5f-4802-9142-5b4a98ab1945",  # Existing tool GUID for update
    "name": "PoLineInsert_Tool_v2",
    "description": "Create purchase order line items in SyteLine (supports batch insert of multiple lines)",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: POST
Endpoint: /update/SLPoItems

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Body:
The body contains PO line details in the Changes array. Use multiple objects in Changes for batch insert:

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

NOTE: Action 1 means insert. DueDate format is YYYY-MM-DD. QtyOrderedConv must include decimals. All properties above are required for each line.""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object indicating success or failure.

Example successful response (batch insert):
{
  "Items": [
    {
      "PoNum": "DP00009000",
      "PoLine": "1",
      "Item": "WIDGET-A",
      "_ItemId": "PBT=[poitem] poi.DT=[...] poi.ID=[guid1]"
    },
    {
      "PoNum": "DP00009000",
      "PoLine": "2",
      "Item": "GADGET-B",
      "_ItemId": "PBT=[poitem] poi.DT=[...] poi.ID=[guid2]"
    }
  ],
  "Success": true,
  "Message": null
}

Example error response:
{
  "Success": false,
  "Message": "Item not found",
  "Items": []
}

Key Response Fields:
- Success: Boolean indicating if insert succeeded
- Message: Error message if Success is false
- Items: Array with all created PO line records (includes _ItemId for each)
- _ItemId: Unique identifier for each created line""",
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
    "instructions": """Use this tool to create PO line items in SyteLine.

CRITICAL: Insert ALL line items for a PO in a SINGLE API call!
Build the complete Changes array with all lines before calling this tool.

Required fields (for each line):
- PoNum: PO number (from PoInsert_Tool_v2)
- PoLine: Line number as string ("1", "2", etc.)
- Item: Item code (from ItemInsert_Tool_v2 or ItemSearch_Tool_v2)
- QtyOrderedConv: Quantity with decimals (e.g., "10.00")
- UM: Unit of measure (must match item's UM)
- Stat: Default "O" (ordered)
- DueDate: Format "YYYY-MM-DD" (e.g., "2026-02-27")
- Whse: Warehouse (must match PO's warehouse)

If DueDate not provided, default to 30 days from today.

Returns array of created line items with _ItemId for each."""
}

print("Creating Invoice Automation Insert Tools (v2)")
print("=" * 60)
print()

# Create Tool 1: VendorInsert
print("Creating Tool 1: VendorInsert_Tool_v2")
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

# Create Tool 2: ItemInsert
print("Creating Tool 2: ItemInsert_Tool_v2")
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

# Create Tool 3: PoInsert
print("Creating Tool 3: PoInsert_Tool_v2")
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

# Create Tool 4: PoLineInsert
print("Creating Tool 4: PoLineInsert_Tool_v2")
print("-" * 60)
response4 = requests.put(tools_url, headers=headers, json=tool4)
print(f"Status Code: {response4.status_code}")

if response4.status_code == 200:
    tool4_response = response4.json()
    print(f"[SUCCESS] Tool 4 created!")
    print(f"  Name: {tool4_response.get('name')}")
    print(f"  GUID: {tool4_response.get('guid')}")
else:
    print(f"[ERROR] Failed to create Tool 4")
    print(f"Response: {response4.text}")

print()
print("=" * 60)

# Save tool definitions for reference
if all([response1.status_code == 200, response2.status_code == 200,
        response3.status_code == 200, response4.status_code == 200]):
    tools_file = Path(__file__).parent / "invoice_insert_tools_v2.json"
    with open(tools_file, 'w') as f:
        json.dump({
            "VendorInsert_Tool_v2": tool1_response,
            "ItemInsert_Tool_v2": tool2_response,
            "PoInsert_Tool_v2": tool3_response,
            "PoLineInsert_Tool_v2": tool4_response
        }, f, indent=2)
    print(f"\n[SUCCESS] Tool details saved to: {tools_file}")
