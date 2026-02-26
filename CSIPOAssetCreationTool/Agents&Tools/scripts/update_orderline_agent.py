"""
Update the UpdateOrderLineDates_Agent_v2 with clearer batch update instructions
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# Updated agent with clearer batch instructions (include GUID to update existing)
updated_agent = {
    "guid": "941b8d9c-054c-4ad3-b88c-b73adbee1ee7",  # Existing agent GUID
    "name": "UpdateOrderLineDates_Agent_v2",
    "description": "Agent to automate weekly updates of customer order line due dates to the previous Sunday",
    "type": "TOOLKIT",
    "inputs": None,
    "data": {
        "workflow": """You are an automated order management assistant for weekly due date updates.

WORKFLOW STEPS:

1. Calculate Previous Sunday:
   - Find the most recent Sunday before today
   - Format the date as YYYYMMDD (e.g., "20260126")
   - This will be the new due date for all order lines

2. Query Order Lines:
   - Use QueryUpcomingOrders_Tool to get 20 order lines with soonest due dates
   - The tool returns an array of Items with _ItemId values
   - Store ALL 20 _ItemId values for the batch update

3. Build Batch Update Request:
   CRITICAL: You must update ALL 20 order lines in ONE API call

   Build a request body with this structure:
   {
     "IDOName": "SLCoitems",
     "RefreshAfterSave": true,
     "Changes": [
       // ONE object for EACH of the 20 order lines
       {
         "Action": 2,
         "ItemId": "_ItemId from item 1",
         "Properties": [
           {
             "IsNull": false,
             "Modified": true,
             "Name": "DueDate",
             "Value": "YYYYMMDD (previous Sunday)"
           }
         ]
       },
       {
         "Action": 2,
         "ItemId": "_ItemId from item 2",
         "Properties": [...]
       },
       // ... repeat for all 20 items
     ]
   }

4. Execute Single Batch Update:
   - Call UpdateOrderDueDate_Tool ONCE with the complete Changes array
   - DO NOT call the tool 20 times
   - The Changes array must contain all 20 order lines

5. Report Results:
   - Confirm how many order lines were updated
   - Show the previous Sunday date used
   - List the order numbers updated

CRITICAL RULES:
- Build the Changes array with ALL 20 items before calling the update tool
- Call UpdateOrderDueDate_Tool exactly ONCE (not 20 times)
- Each Change object needs Action=2, ItemId, and Properties array
- All dates must be in YYYYMMDD format (8 digits, no separators)""",
        "tools": [
            "QueryUpcomingOrders_Tool",
            "UpdateOrderDueDate_Tool"
        ],
        "logicalIds": [
            "lid://infor.syteline.update-orderline-dates-v2"
        ],
        "model": {
            "model": "CLAUDE",
            "version": "claude-3-7-sonnet-20250219-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [
        "Update order line due dates",
        "Run weekly order date update",
        "Set order lines to last Sunday",
        "Update 20 soonest order lines",
        "Make orders late for the week"
    ],
    "stubResponse": "",
    "instructions": "Agent to automate weekly order line due date updates. Finds 20 order lines with soonest due dates and updates them ALL in ONE batch call to previous Sunday.",
    "security": {
        "roles": []
    }
}

# API endpoint
agents_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

print("Updating UpdateOrderLineDates_Agent_v2 with batch update instructions")
print("=" * 60)
print()

# Update the agent
response = requests.put(agents_url, headers=headers, json=updated_agent)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    agent_response = response.json()
    print(f"[SUCCESS] Agent updated!")
    print(f"  Name: {agent_response.get('name')}")
    print(f"  GUID: {agent_response.get('guid')}")
    print(f"  Type: {agent_response.get('type')}")

    logical_ids = agent_response.get('data', {}).get('logicalIds', [])
    if logical_ids:
        print(f"\nLogical ID: {logical_ids[0]}")
else:
    print(f"[ERROR] Failed to update agent")
    print(f"Response: {response.text}")

print()
print("=" * 60)
