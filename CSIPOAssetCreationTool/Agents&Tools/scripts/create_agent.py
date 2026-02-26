"""
Create a new GenAI agent via API
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
    "name": "CustomerSearch_Agent",
    "description": "Agent to help users search for and find customer information in the CSI/Syteline system",
    "type": "TOOLKIT",  # TOOLKIT = Agent, API_DOCS = Tool
    "inputs": None,
    "data": {
        "workflow": """You are a helpful customer search assistant for the CSI/Syteline system.

When users ask about customers:

1. Use the CustomerSearch_Tool to search for customers
2. For exact customer number searches, use filter: CustNum='CUSTOMER_NUMBER'
3. For name searches, use filter: Name LIKE 'PARTIAL_NAME%'
4. Always request properties: CustNum, Name, CustSeq at minimum
5. Set recordCap to limit results (e.g., 20 for broad searches)

Present results clearly:
- List customer number, name, and sequence
- If multiple customers found, list them in a readable format
- If no customers found, inform the user politely and suggest alternatives
- Be concise but friendly

Example interactions:
- "Find customer CUST001" → filter=CustNum='CUST001'
- "Search for customers with ABC in name" → filter=Name LIKE 'ABC%'
- "List all customers" → recordCap=20 (limited)""",
        "tools": [
            "CustomerSearch_Tool"  # The tool we created earlier
        ],
        "logicalIds": [
            "lid://infor.syteline.customer-search"  # Logical ID for this agent
        ],
        "model": {
            "model": "CLAUDE",
            "version": "claude-3-7-sonnet-20250219-v1:0"
        }
    },
    "status": 1,  # 1 = enabled
    "ignoreSearch": False,
    "utterances": [
        "Find customer {customer_number}",
        "Search for customers",
        "Look up customer information",
        "Find customer by name",
        "Does customer exist"
    ],
    "stubResponse": "",
    "instructions": "Agent to search for customers in CSI/Syteline. Uses CustomerSearch_Tool to query customer data by number or name. Returns customer details including number, name, and sequence.",
    "security": {
        "roles": []
    }
}

# API endpoint (same as tools)
agents_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = get_auth_headers()

print("Creating New GenAI Agent: CustomerSearch_Agent")
print("=" * 60)
print(f"PUT {agents_url}\n")

# Save the agent definition for reference
agent_def_file = Path(__file__).parent / "new_agent_definition.json"
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

    # Save the response
    response_file = Path(__file__).parent / "created_agent_response.json"
    with open(response_file, 'w') as f:
        json.dump(agent_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Failed to create agent")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
