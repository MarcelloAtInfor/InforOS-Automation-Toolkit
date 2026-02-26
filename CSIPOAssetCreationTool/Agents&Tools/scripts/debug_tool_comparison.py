"""
Deep comparison of VendorInsert vs ItemInsert tools to find what causes URL difference
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

response = requests.get(tools_url, headers=headers)
tools = response.json()

vendor_insert_v2 = next((t for t in tools if t['name'] == 'VendorInsert_Tool_v2'), None)
item_insert_v2 = next((t for t in tools if t['name'] == 'ItemInsert_Tool_v2'), None)
vendor_search_v2 = next((t for t in tools if t['name'] == 'VendorSearch_Tool_v2'), None)
item_search_v2 = next((t for t in tools if t['name'] == 'ItemSearch_Tool_v2'), None)

print("=" * 80)
print("COMPARING VENDOR vs ITEM TOOLS")
print("=" * 80)

def compare_tools(tool1, tool2, name1, name2):
    print(f"\n\n{'='*80}")
    print(f"{name1} vs {name2}")
    print(f"{'='*80}")

    if not tool1 or not tool2:
        print("One or both tools not found!")
        return

    # Compare top-level fields
    print(f"\n{name1} fields:")
    print(f"  type: {tool1.get('type')}")
    print(f"  status: {tool1.get('status')}")
    print(f"  servicePath: {tool1.get('data', {}).get('servicePath')}")

    print(f"\n{name2} fields:")
    print(f"  type: {tool2.get('type')}")
    print(f"  status: {tool2.get('status')}")
    print(f"  servicePath: {tool2.get('data', {}).get('servicePath')}")

    # Compare instructions
    print(f"\n{name1} instructions length: {len(tool1.get('instructions', ''))}")
    print(f"{name2} instructions length: {len(tool2.get('instructions', ''))}")

    print(f"\n{name1} instructions:")
    print(tool1.get('instructions', '')[:200])

    print(f"\n{name2} instructions:")
    print(tool2.get('instructions', '')[:200])

    # Compare api_docs length
    api_docs1 = tool1.get('data', {}).get('api_docs', '')
    api_docs2 = tool2.get('data', {}).get('api_docs', '')

    print(f"\n{name1} api_docs length: {len(api_docs1)}")
    print(f"{name2} api_docs length: {len(api_docs2)}")

    # Look for any mentions of <YOUR_SITE> or /api/v2/ in api_docs
    if '<YOUR_SITE>' in api_docs2 and '<YOUR_SITE>' not in api_docs1:
        print(f"\n⚠️ WARNING: {name2} api_docs contains '<YOUR_SITE>' but {name1} doesn't!")

    if '/api/v2/' in api_docs2:
        print(f"\n⚠️ WARNING: {name2} api_docs contains '/api/v2/'!")
        # Find where it appears
        idx = api_docs2.find('/api/v2/')
        print(f"  Context: ...{api_docs2[max(0,idx-50):idx+100]}...")

# Compare Insert tools
compare_tools(vendor_insert_v2, item_insert_v2, "VendorInsert_Tool_v2", "ItemInsert_Tool_v2")

# Compare Search tools
compare_tools(vendor_search_v2, item_search_v2, "VendorSearch_Tool_v2", "ItemSearch_Tool_v2")

# Save full tool configs for detailed inspection
if vendor_insert_v2 and item_insert_v2:
    with open(Path(__file__).parent / "vendor_insert_v2_full.json", 'w') as f:
        json.dump(vendor_insert_v2, f, indent=2)
    with open(Path(__file__).parent / "item_insert_v2_full.json", 'w') as f:
        json.dump(item_insert_v2, f, indent=2)
    print(f"\n\n[SAVED] Full tool configs saved for detailed inspection")
