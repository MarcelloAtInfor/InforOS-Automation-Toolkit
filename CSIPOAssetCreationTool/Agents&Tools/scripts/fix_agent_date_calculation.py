"""
Update UpdateOrderLineDates_Agent_v2 to fix the date calculation for previous Sunday
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# Updated agent with corrected date calculation
updated_agent = {
    "guid": "941b8d9c-054c-4ad3-b88c-b73adbee1ee7",  # Existing agent GUID
    "name": "UpdateOrderLineDates_Agent_v2",
    "description": "Agent to automate weekly updates of customer order line due dates to the previous Sunday (Ordered status only)",
    "type": "TOOLKIT",
    "inputs": None,
    "data": {
        "workflow": """You are an automated order management assistant for weekly due date updates.

WORKFLOW STEPS:

1. Calculate Previous Sunday (CRITICAL - GET THIS RIGHT):
   IMPORTANT: Use proper date calculation to find the most recent Sunday.

   In Python datetime, weekday() returns: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6

   To find the previous Sunday from any day:
   - If today is Sunday (weekday=6): go back 7 days to get last Sunday
   - If today is Monday (weekday=0): go back 1 day to get yesterday's Sunday
   - If today is Tuesday (weekday=1): go back 2 days
   - If today is Wednesday (weekday=2): go back 3 days
   - If today is Thursday (weekday=3): go back 4 days
   - If today is Friday (weekday=4): go back 5 days
   - If today is Saturday (weekday=5): go back 6 days

   Formula:
   - days_to_subtract = (today.weekday() + 1) if today.weekday() != 6 else 7

   Example: If today is Tuesday Jan 27, 2026 (weekday=1):
   - Days to subtract = 1 + 1 = 2
   - Previous Sunday = Jan 27 - 2 days = Jan 25, 2026

   Format the date as YYYYMMDD (e.g., "20260125" for Jan 25, 2026)

   VERIFY: Always double-check that your calculated date is actually a Sunday!

2. Query Order Lines (with Stat='O' filter):
   - Use QueryUpcomingOrders_Tool to get order lines
   - The tool now automatically filters for Stat='O' (Ordered status only)
   - Returns 20 order lines with soonest due dates
   - Store ALL _ItemId values for the batch update

3. Build Batch Update Request:
   CRITICAL: You must update ALL order lines in ONE API call

   Build a request body with this structure:
   {
     "IDOName": "SLCoitems",
     "RefreshAfterSave": true,
     "Changes": [
       // ONE object for EACH order line returned by the query
       {
         "Action": 2,
         "ItemId": "_ItemId from item 1",
         "Properties": [
           {
             "IsNull": false,
             "Modified": true,
             "Name": "DueDate",
             "Value": "YYYYMMDD (previous Sunday - MAKE SURE IT'S CORRECT)"
           }
         ]
       },
       {
         "Action": 2,
         "ItemId": "_ItemId from item 2",
         "Properties": [...]
       },
       // ... repeat for all items from query
     ]
   }

4. Execute Single Batch Update:
   - Call UpdateOrderDueDate_Tool ONCE with the complete Changes array
   - DO NOT call the tool multiple times
   - The Changes array must contain all order lines from step 2

5. Report Results:
   - Confirm how many order lines were updated
   - Show the previous Sunday date used (format as readable date)
   - List the order numbers updated

CRITICAL RULES:
- Double-check your Sunday date calculation - it must be correct!
- Only update order lines with Stat='O' (query tool handles this filter)
- Build the Changes array with ALL items before calling the update tool
- Call UpdateOrderDueDate_Tool exactly ONCE (not multiple times)
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
    "instructions": "Agent to automate weekly order line due date updates. Finds order lines with soonest due dates (Ordered status only) and updates them ALL in ONE batch call to previous Sunday. CRITICAL: Must calculate correct Sunday date!",
    "security": {
        "roles": []
    }
}

# API endpoint
agents_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

print("Updating UpdateOrderLineDates_Agent_v2 with corrected date calculation")
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
    print(f"  Updates:")
    print(f"    - Fixed date calculation for previous Sunday")
    print(f"    - Now filters for Stat='O' (Ordered status only)")

    logical_ids = agent_response.get('data', {}).get('logicalIds', [])
    if logical_ids:
        print(f"\nLogical ID: {logical_ids[0]}")
else:
    print(f"[ERROR] Failed to update agent")
    print(f"Response: {response.text}")

print()
print("=" * 60)
