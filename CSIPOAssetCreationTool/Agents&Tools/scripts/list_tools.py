"""
List all GenAI tools using the API
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

# Get auth headers
headers = get_auth_headers()

print("Fetching GenAI Tools from API")
print("=" * 60)
print(f"GET {tools_url}\n")

response = requests.get(tools_url, headers=headers)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    tools = response.json()
    print(f"[SUCCESS] Found {len(tools)} tools\n")

    if tools:
        print("Tool List:")
        print("-" * 60)
        for i, tool in enumerate(tools, 1):
            name = tool.get('name', 'N/A')
            guid = tool.get('guid', 'N/A')
            enabled = tool.get('enabled', False)
            description = tool.get('description', 'No description')

            status = "[ENABLED]" if enabled else "[DISABLED]"
            print(f"\n{i}. {name} {status}")
            print(f"   GUID: {guid}")
            print(f"   Description: {description[:80]}{'...' if len(description) > 80 else ''}")

        # Save full tool data to file
        output_file = Path(__file__).parent / "tools_list.json"
        with open(output_file, 'w') as f:
            json.dump(tools, f, indent=2)

        print(f"\n{'-' * 60}")
        print(f"[SUCCESS] Full tool data saved to: {output_file}")
    else:
        print("No tools found in the system.")

else:
    print(f"[ERROR] Failed to fetch tools")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
