"""
Create a new GenAI tool via API
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# Define the new tool
new_tool = {
    "name": "CustomerSearch_Tool",
    "description": "Search for customers in CSI/Syteline by customer number or name",
    "type": "API_DOCS",
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",
        "api_docs": """Method: GET
ENDPOINT: /load/SLCustomers

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:

Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of customer properties to return. Example: CustNum, Name, CustSeq

Parameter: filter
Format: STRING
Required: False
Description: Filter expression for searching customers. Examples:
- By customer number: CustNum='CUST001'
- By name (partial match): Name LIKE 'ABC%'
- Multiple conditions: CustNum='CUST001' AND CustSeq=0

Parameter: recordCap
Format: INTEGER
Required: False
Description: Maximum number of records to return. Default: -1 (system default), 0 = unlimited

Example Requests:

To search for a specific customer by number:
/load/SLCustomers?properties=CustNum,Name,CustSeq&filter=CustNum='CUST001'

To search for customers by name (partial match):
/load/SLCustomers?properties=CustNum,Name,CustSeq&filter=Name LIKE 'ABC%'&recordCap=10

To get all customers (limited):
/load/SLCustomers?properties=CustNum,Name,CustSeq&recordCap=20""",
        "headers": {},
        "responseInstructions": """The API responds with a JSON object containing an Items array.

If customers are found, the Items array contains one or more objects with the requested properties.

Example response with results:
{
  "Items": [
    {
      "CustNum": "CUST001",
      "Name": "ABC Corporation",
      "CustSeq": 0,
      "_ItemId": "PBT=[custaddr] custaddr.ID=[guid]"
    }
  ],
  "MoreRowsExist": false,
  "Success": true,
  "Message": null
}

If no customers match the criteria, the Items array is empty:
{
  "Items": [],
  "MoreRowsExist": false,
  "Success": true,
  "Message": null
}

HTTP Status Codes:
- 200 OK: Successful API call (regardless of whether customers were found)
- 401 Unauthorized: Authentication failed
- 422 Validation Error: Invalid parameters

Key Response Fields:
- Items: Array of customer objects
- MoreRowsExist: Boolean indicating if more records are available
- Success: Boolean indicating API call success
- Message: Error message if Success is false""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-3-7-sonnet-20250219-v1:0"
        }
    },
    "status": 1,  # 1 = enabled
    "ignoreSearch": False,
    "utterances": [],
    "stubResponse": "",
    "instructions": """Use this tool to search for customers in CSI/Syteline by customer number or name.

Search options:
- Customer Number (CustNum): Exact match (e.g., CustNum='CUST001')
- Customer Name: Partial match using LIKE (e.g., Name LIKE 'ABC%')

Returns: Customer Number, Name, Sequence, and other requested properties.

Use when user asks to:
- Find a specific customer
- Verify customer existence
- List customers by criteria
- Get customer information for orders or inquiries

Examples: "Find customer CUST001", "Search for customers starting with ABC", "Does customer XYZ exist?"

Returns customer details if found, or empty result if not found."""
}

# API endpoint
tools_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

print("Creating New GenAI Tool: CustomerSearch_Tool")
print("=" * 60)
print(f"PUT {tools_url}\n")

# Save the tool definition for reference
tool_def_file = Path(__file__).parent / "new_tool_definition.json"
with open(tool_def_file, 'w') as f:
    json.dump(new_tool, f, indent=2)
print(f"Tool definition saved to: {tool_def_file}")

# Create the tool
response = requests.put(tools_url, headers=headers, json=new_tool)

print(f"\nStatus Code: {response.status_code}\n")

if response.status_code == 200:
    tool_response = response.json()
    print(f"[SUCCESS] Tool created successfully!\n")
    print(f"Tool Name: {tool_response.get('name')}")
    print(f"Tool GUID: {tool_response.get('guid')}")
    print(f"Status: {'Enabled' if tool_response.get('status') == 1 else 'Disabled'}")

    # Save the response
    response_file = Path(__file__).parent / "created_tool_response.json"
    with open(response_file, 'w') as f:
        json.dump(tool_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Failed to create tool")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
