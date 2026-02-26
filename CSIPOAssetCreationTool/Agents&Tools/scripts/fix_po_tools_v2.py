"""
Fix PoInsert_Tool_v2 and PoSearch_Tool_v2 to use correct IDO name: SLPOs (not SLPos)
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

# Get current tools to retrieve their definitions
response = requests.get(tools_url, headers=headers)
tools = response.json()

# Find PoSearch_Tool_v2 and PoInsert_Tool_v2
po_search_tool = next((t for t in tools if t['name'] == 'PoSearch_Tool_v2'), None)
po_insert_tool = next((t for t in tools if t['name'] == 'PoInsert_Tool_v2'), None)

if not po_search_tool or not po_insert_tool:
    print("[ERROR] Could not find PO tools")
    exit(1)

print("Fixing PO Tools - Changing SLPos to SLPOs")
print("=" * 60)

# Fix PoSearch_Tool_v2
print("\n1. Fixing PoSearch_Tool_v2...")
po_search_tool['data']['api_docs'] = po_search_tool['data']['api_docs'].replace('/load/SLPos', '/load/SLPOs')
po_search_tool['data']['api_docs'] = po_search_tool['data']['api_docs'].replace('SLPos?', 'SLPOs?')

response1 = requests.put(tools_url, headers=headers, json=po_search_tool)
if response1.status_code == 200:
    print(f"[SUCCESS] PoSearch_Tool_v2 updated - now uses SLPOs")
else:
    print(f"[ERROR] Failed to update PoSearch_Tool_v2: {response1.text}")

# Fix PoInsert_Tool_v2
print("\n2. Fixing PoInsert_Tool_v2...")
po_insert_tool['data']['api_docs'] = po_insert_tool['data']['api_docs'].replace('/update/SLPos', '/update/SLPOs')
po_insert_tool['data']['api_docs'] = po_insert_tool['data']['api_docs'].replace('"IDOName": "SLPos"', '"IDOName": "SLPOs"')
po_insert_tool['data']['api_docs'] = po_insert_tool['data']['api_docs'].replace('IDOName: "SLPos"', 'IDOName: "SLPOs"')

response2 = requests.put(tools_url, headers=headers, json=po_insert_tool)
if response2.status_code == 200:
    print(f"[SUCCESS] PoInsert_Tool_v2 updated - now uses SLPOs")
else:
    print(f"[ERROR] Failed to update PoInsert_Tool_v2: {response2.text}")

print("\n" + "=" * 60)
print("Fix complete! Both tools now use the correct IDO name: SLPOs")
