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

# Updated VendorSearch_Tool_v2 with correct property names
tool = {
    "guid": "b7be3168-6771-4114-abe4-8c43530419ad",
    "name": "VendorSearch_Tool_v2",
    "description": "Search for vendors in SyteLine by vendor number or name",
    "type": "API_DOCS",
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: GET
Endpoint: /load/SLVendors

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:
- properties: VendNum,Name,VadAddr_1,VadCity,VadState,VadZip,Phone,ExternalEmailAddr,_ItemId
- filter: (optional) e.g., "VendNum = 'TESTV01'" or "Name LIKE '%Corp%'"
- recordCap: (optional) limit number of results, e.g., "10"

IMPORTANT Property Names:
- Phone (NOT VadPhone!)
- ExternalEmailAddr (NOT VadEmail!)

Filter Syntax:
- Use single quotes for string values: VendNum = 'ABC123'
- LIKE operator for partial match: Name LIKE '%Corp%'
- NOT double quotes (will cause IllegalFilterException)

Example request:
GET /load/SLVendors?properties=VendNum,Name,Phone,ExternalEmailAddr,_ItemId&filter=VendNum='ABC123'&recordCap=10""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object containing an Items array.

Example successful response:
{
  "Items": [
    {
      "VendNum": "ABC123",
      "Name": "Test Vendor Corporation",
      "VadAddr_1": "123 Main St",
      "VadCity": "New York",
      "VadState": "NY",
      "VadZip": "10001",
      "Phone": "555-1234",
      "ExternalEmailAddr": "vendor@example.com",
      "_ItemId": "PBT=[vendor] v.DT=[2024-01-01 12:00:00.000] v.ID=[guid]"
    }
  ],
  "Success": true,
  "Message": null,
  "MoreRowsExist": false
}

Empty result (vendor not found):
{
  "Items": [],
  "Success": true,
  "Message": null,
  "MoreRowsExist": false
}

Key Response Fields:
- Items: Array of vendor records (empty if no matches)
- Success: Boolean, true if query executed successfully
- _ItemId: Required for update operations""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-sonnet-4-5-20250929-v1:0"
        }
    },
    "status": 1,
    "instructions": """Use this tool to search for vendors in SyteLine.

Search by vendor number (exact match):
- filter: VendNum = 'ABC123'

Search by name (partial match):
- filter: Name LIKE '%Corp%'

IMPORTANT: Use correct property names:
- Phone (NOT VadPhone)
- ExternalEmailAddr (NOT VadEmail)

Returns array of matching vendors with _ItemId for updates."""
}

print("Updating VendorSearch_Tool_v2...")
print(f"GUID: {tool['guid']}")

# Update the tool via PUT
response = requests.put(f'{GENAI_CORE_URL()}/api/v1/tools', headers=headers, json=tool)

if response.status_code == 200:
    print("SUCCESS: Updated VendorSearch_Tool_v2")
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Tool Name: {result.get('name')}")
    print(f"Tool GUID: {result.get('guid')}")
    print(f"Status: {'Enabled' if result.get('status') == 1 else 'Disabled'}")
    print("\nFixed property names: Phone and ExternalEmailAddr (not VadPhone/VadEmail)")
else:
    print(f"FAILED: Could not update tool")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
