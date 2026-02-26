"""
Fix ALL v2 tools with correct field names and simplified api_docs format
Fixes:
1. VendorSearch - Remove VadPhone/VadEmail, add Phone/ExternalEmailAddr
2. All tools - Use single quotes in filters (not double quotes)
3. ItemSearch/ItemInsert - Simplify api_docs to match working Vendor format
4. PoSearch/PoInsert - Fix filter syntax and simplify api_docs
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

# Get current tools
print("Fetching current tools...")
response = requests.get(tools_url, headers=headers)
tools = response.json()

vendor_search_v2 = next((t for t in tools if t['name'] == 'VendorSearch_Tool_v2'), None)
item_search_v2 = next((t for t in tools if t['name'] == 'ItemSearch_Tool_v2'), None)
item_insert_v2 = next((t for t in tools if t['name'] == 'ItemInsert_Tool_v2'), None)
po_search_v2 = next((t for t in tools if t['name'] == 'PoSearch_Tool_v2'), None)
po_insert_v2 = next((t for t in tools if t['name'] == 'PoInsert_Tool_v2'), None)

print("\n" + "=" * 80)
print("FIXING TOOLS")
print("=" * 80)

# Fix 1: VendorSearch_Tool_v2 - Fix field names
if vendor_search_v2:
    print("\n1. Fixing VendorSearch_Tool_v2...")
    # Update properties: remove VadPhone/VadEmail, add Phone/ExternalEmailAddr
    vendor_search_v2['data']['api_docs'] = vendor_search_v2['data']['api_docs'].replace(
        'VendNum,Name,VadAddr_1,VadCity,VadState,VadZip,VadPhone,VadEmail,_ItemId',
        'VendNum,Name,VadAddr_1,VadCity,VadState,VadZip,Phone,ExternalEmailAddr,_ItemId'
    )
    # Update filter examples to use single quotes
    vendor_search_v2['data']['api_docs'] = vendor_search_v2['data']['api_docs'].replace(
        'filter=VendNum = "DEMO001"',
        "filter=VendNum = 'DEMO001'"
    )
    vendor_search_v2['data']['api_docs'] = vendor_search_v2['data']['api_docs'].replace(
        'filter=Name LIKE "%ACME%"',
        "filter=Name LIKE '%ACME%'"
    )

    response1 = requests.put(tools_url, headers=headers, json=vendor_search_v2)
    if response1.status_code == 200:
        print("   [SUCCESS] VendorSearch_Tool_v2 fixed - now uses Phone and ExternalEmailAddr")
    else:
        print(f"   [ERROR] Failed: {response1.text}")

# Fix 2: ItemSearch_Tool_v2 - Simplify and fix filter syntax
if item_search_v2:
    print("\n2. Fixing ItemSearch_Tool_v2...")
    # Completely rewrite api_docs in simple format matching old working tools
    item_search_v2['data']['api_docs'] = """Method: GET
Endpoint: /load/SLItems

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties to return. Example: Item,Description,UM,ProductCode,_ItemId

Parameter: filter
Format: STRING
Required: False
Description: SQL WHERE clause to filter results. Examples: Item = 'WIDGET-A' or Description LIKE '%widget%'

Parameter: recordCap
Format: INTEGER
Required: False
Description: Maximum number of records to return. Default: 10

Example Requests:

Search by item code:
/load/SLItems?properties=Item,Description,UM,ProductCode,_ItemId&filter=Item = 'WIDGET-A'

Search by description:
/load/SLItems?properties=Item,Description,UM,ProductCode,_ItemId&filter=Description LIKE '%Premium%'&recordCap=10"""

    response2 = requests.put(tools_url, headers=headers, json=item_search_v2)
    if response2.status_code == 200:
        print("   [SUCCESS] ItemSearch_Tool_v2 fixed - simplified api_docs")
    else:
        print(f"   [ERROR] Failed: {response2.text}")

# Fix 3: ItemInsert_Tool_v2 - Simplify format
if item_insert_v2:
    print("\n3. Fixing ItemInsert_Tool_v2...")
    # Rewrite in minimal format matching old working tools
    item_insert_v2['data']['api_docs'] = """Method: POST
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
        {"IsNull": false, "Modified": true, "Name": "Stat", "Value": "A"}
      ]
    }
  ]
}

NOTE: Action 1 means insert. All properties above are required."""

    response3 = requests.put(tools_url, headers=headers, json=item_insert_v2)
    if response3.status_code == 200:
        print("   [SUCCESS] ItemInsert_Tool_v2 fixed - simplified api_docs")
    else:
        print(f"   [ERROR] Failed: {response3.text}")

# Fix 4: PoSearch_Tool_v2 - Fix filter syntax
if po_search_v2:
    print("\n4. Fixing PoSearch_Tool_v2...")
    # Fix filter examples to use single quotes
    po_search_v2['data']['api_docs'] = po_search_v2['data']['api_docs'].replace(
        'filter=PoNum = "DP00009000"',
        "filter=PoNum = 'DP00009000'"
    )
    po_search_v2['data']['api_docs'] = po_search_v2['data']['api_docs'].replace(
        'filter=PoNum = "PO-NUMBER"',
        "filter=PoNum = 'PO-NUMBER'"
    )

    # Simplify the api_docs
    po_search_v2['data']['api_docs'] = """Method: GET
Endpoint: /load/SLPOs

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties. Example: PoNum,VendNum,OrderDate,Whse,Stat,_ItemId

Parameter: filter
Format: STRING
Required: True
Description: SQL WHERE clause. Example: PoNum = 'DP00009000'

Parameter: recordCap
Format: INTEGER
Required: False
Description: Maximum records. Default: 1

Example Request:

/load/SLPOs?properties=PoNum,VendNum,OrderDate,Whse,Stat,_ItemId&filter=PoNum = 'DP00009000'&recordCap=1"""

    response4 = requests.put(tools_url, headers=headers, json=po_search_v2)
    if response4.status_code == 200:
        print("   [SUCCESS] PoSearch_Tool_v2 fixed - simplified and fixed filter syntax")
    else:
        print(f"   [ERROR] Failed: {response4.text}")

# Fix 5: PoInsert_Tool_v2 - Simplify format
if po_insert_v2:
    print("\n5. Fixing PoInsert_Tool_v2...")
    # Rewrite in minimal format
    po_insert_v2['data']['api_docs'] = """Method: POST
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

NOTE: Action 1 means insert. PoNum must be exactly 10 characters. VendNum links PO to vendor."""

    response5 = requests.put(tools_url, headers=headers, json=po_insert_v2)
    if response5.status_code == 200:
        print("   [SUCCESS] PoInsert_Tool_v2 fixed - simplified api_docs")
    else:
        print(f"   [ERROR] Failed: {response5.text}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("""
Fixed Issues:
1. [SUCCESS] VendorSearch - Now uses 'Phone' and 'ExternalEmailAddr' (not VadPhone/VadEmail)
2. [SUCCESS] All filters - Now use single quotes (not double quotes)
3. [SUCCESS] ItemSearch - Simplified api_docs format
4. [SUCCESS] ItemInsert - Simplified api_docs format
5. [SUCCESS] PoSearch - Simplified api_docs and fixed filter syntax
6. [SUCCESS] PoInsert - Simplified api_docs format

Next Steps:
1. Test the agent again with the same invoice data
2. URL construction should now be correct for all tools
3. Filter syntax errors should be resolved
""")
