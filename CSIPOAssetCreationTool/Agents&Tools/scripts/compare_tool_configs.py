"""
Compare old vs new tool configurations to find differences
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

# Get all tools
response = requests.get(tools_url, headers=headers)
tools = response.json()

# Find old and new ItemInsert tools
old_item_insert = next((t for t in tools if t['name'] == 'ItemInsert_Tool'), None)
new_item_insert = next((t for t in tools if t['name'] == 'ItemInsert_Tool_v2'), None)

print("=" * 60)
print("COMPARING ItemInsert_Tool (old) vs ItemInsert_Tool_v2 (new)")
print("=" * 60)

if old_item_insert:
    print("\nOLD ItemInsert_Tool:")
    print(f"  servicePath: {old_item_insert.get('data', {}).get('servicePath')}")
    print(f"  First 200 chars of api_docs:")
    print(f"  {old_item_insert.get('data', {}).get('api_docs', '')[:200]}")

if new_item_insert:
    print("\nNEW ItemInsert_Tool_v2:")
    print(f"  servicePath: {new_item_insert.get('data', {}).get('servicePath')}")
    print(f"  First 200 chars of api_docs:")
    print(f"  {new_item_insert.get('data', {}).get('api_docs', '')[:200]}")

# Save full old tool config for inspection
if old_item_insert:
    with open(Path(__file__).parent / "old_iteminsert_full.json", 'w') as f:
        json.dump(old_item_insert, f, indent=2)
    print(f"\n[SAVED] Full old tool config to: old_iteminsert_full.json")

if new_item_insert:
    with open(Path(__file__).parent / "new_iteminsert_full.json", 'w') as f:
        json.dump(new_item_insert, f, indent=2)
    print(f"[SAVED] Full new tool config to: new_iteminsert_full.json")
