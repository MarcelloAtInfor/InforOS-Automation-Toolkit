"""
Create a GenAI agent to automate weekly order line due date updates
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# Define the new agent
new_agent = {
    "name": "UpdateOrderLineDates_Agent_v2",
    "description": "Agent to automate weekly updates of customer order line due dates to the previous Sunday",
    "type": "TOOLKIT",  # TOOLKIT = Agent, API_DOCS = Tool
    "inputs": None,
    "data": {
        "workflow": """You are an automated order management assistant for weekly due date updates.

WORKFLOW STEPS:

1. Calculate Previous Sunday:
   - Find the most recent Sunday before today
   - Format the date as YYYYMMDD (e.g., "20260125")
   - This will be the new due date for all order lines

2. Query Order Lines:
   - Use QueryUpcomingOrders_Tool to get 20 order lines with soonest due dates
   - The tool automatically sorts by DueDate ascending and limits to 20 records
   - No parameters needed - the tool is pre-configured

3. Update Due Dates:
   - Use UpdateOrderDueDate_Tool to update all 20 order lines
   - Build a request with all _ItemId values from step 2
   - Set all DueDate fields to the previous Sunday date from step 1
   - Execute in a single API call (batch update)

4. Report Results:
   - Confirm how many order lines were updated
   - Show the previous Sunday date used
   - List the order numbers that were updated

IMPORTANT NOTES:
- Execute all steps automatically without asking for confirmation
- Use the _ItemId exactly as returned from the query (do not modify)
- Date format for updates is YYYYMMDD (8 digits, no separators)
- All 20 order lines should be updated to the same date (previous Sunday)""",
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
    "status": 1,  # 1 = enabled
    "ignoreSearch": False,
    "utterances": [
        "Update order line due dates",
        "Run weekly order date update",
        "Set order lines to last Sunday",
        "Update 20 soonest order lines",
        "Make orders late for the week"
    ],
    "stubResponse": "",
    "instructions": "Agent to automate weekly order line due date updates. Finds 20 order lines with soonest due dates and updates them to previous Sunday. Runs automatically without confirmation.",
    "security": {
        "roles": []
    }
}

# API endpoint (same as tools)
agents_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

print("Creating New GenAI Agent: UpdateOrderLineDates_Agent_v2")
print("=" * 60)
print(f"PUT {agents_url}\n")

# Save the agent definition for reference
agent_def_file = Path(__file__).parent / "orderline_agent_definition.json"
with open(agent_def_file, 'w') as f:
    json.dump(new_agent, f, indent=2)
print(f"Agent definition saved to: {agent_def_file}")

# Create the agent
response = requests.put(agents_url, headers=headers, json=new_agent)

print(f"\nStatus Code: {response.status_code}\n")

if response.status_code == 200:
    agent_response = response.json()
    print(f"[SUCCESS] Agent created successfully!\n")
    print(f"Agent Name: {agent_response.get('name')}")
    print(f"Agent GUID: {agent_response.get('guid')}")
    print(f"Type: {agent_response.get('type')}")
    print(f"Status: {'Enabled' if agent_response.get('status') == 1 else 'Disabled'}")

    # Extract logical IDs
    logical_ids = agent_response.get('data', {}).get('logicalIds', [])
    if logical_ids:
        print(f"\nLogical IDs:")
        for lid in logical_ids:
            print(f"  - {lid}")
            print(f"\nTo invoke this agent via Chat API, use header:")
            print(f'  x-infor-logicalidprefix: {lid}')

    # Extract tools
    tools = agent_response.get('data', {}).get('tools', [])
    if tools:
        print(f"\nTools assigned ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool}")

    # Save the response
    response_file = Path(__file__).parent / "created_orderline_agent_response.json"
    with open(response_file, 'w') as f:
        json.dump(agent_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Failed to create agent")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
