"""
Get detailed information about a specific tool
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# Get tool GUID from command line or use default
tool_guid = "e4513d7a-45a9-4813-bc7d-9f79c89d416e"  # ItemSearch_Tool
if len(sys.argv) > 1:
    tool_guid = sys.argv[1]

# API endpoint
tool_url = f"{GENAI_CORE_URL()}/api/v1/tools/{tool_guid}"

headers = get_auth_headers()

print(f"Fetching Tool Details: {tool_guid}")
print("=" * 60)
print(f"GET {tool_url}\n")

response = requests.get(tool_url, headers=headers)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    tool = response.json()
    print(f"[SUCCESS] Tool Details Retrieved\n")

    print(f"Name: {tool.get('name')}")
    print(f"GUID: {tool.get('guid')}")
    print(f"Enabled: {tool.get('enabled')}")
    print(f"Description: {tool.get('description', 'N/A')[:200]}")

    # Save full tool details to file
    output_file = Path(__file__).parent / f"tool_detail_{tool.get('name', 'unknown')}.json"
    with open(output_file, 'w') as f:
        json.dump(tool, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"[SUCCESS] Full tool details saved to: {output_file}")
    print(f"\nKey fields in tool structure:")
    print(f"  - {', '.join(tool.keys())}")

else:
    print(f"[ERROR] Failed to fetch tool details")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
