"""
Query the old invoice tools to see what IDO collections and endpoints they used
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
print("Fetching all tools to find old invoice tools...")
response = requests.get(tools_url, headers=headers)

if response.status_code == 200:
    tools = response.json()

    # Find invoice-related tools (old versions)
    invoice_tools = [t for t in tools if 'invoice' in t.get('name', '').lower() or
                     'vendor' in t.get('name', '').lower() or
                     'item' in t.get('name', '').lower() or
                     'po' in t.get('name', '').lower()]

    print(f"\nFound {len(invoice_tools)} invoice-related tools:\n")

    for tool in invoice_tools:
        print(f"Tool: {tool.get('name')}")
        print(f"  GUID: {tool.get('guid')}")
        print(f"  Type: {tool.get('type')}")

        # Check if it has api_docs with endpoint info
        api_docs = tool.get('data', {}).get('api_docs', '')
        if api_docs:
            # Extract endpoint from api_docs
            lines = api_docs.split('\n')
            for line in lines:
                if 'ENDPOINT:' in line or '/load/' in line or '/update/' in line:
                    print(f"  {line.strip()}")

        print()

    # Save detailed info on old ItemInsert and PoInsert tools
    print("\n" + "="*60)
    print("Checking old ItemInsert and PoInsert tools for IDO names:")
    print("="*60)

    for tool in invoice_tools:
        if 'iteminsert' in tool.get('name', '').lower() and 'v2' not in tool.get('name', '').lower():
            print(f"\nOLD ItemInsert_Tool:")
            api_docs = tool.get('data', {}).get('api_docs', '')
            if '/update/' in api_docs:
                # Find the IDOName
                for line in api_docs.split('\n'):
                    if 'ENDPOINT:' in line or 'IDOName' in line or '/update/' in line:
                        print(f"  {line.strip()}")

        if 'poinsert' in tool.get('name', '').lower() and 'line' not in tool.get('name', '').lower() and 'v2' not in tool.get('name', '').lower():
            print(f"\nOLD PoInsert_Tool:")
            api_docs = tool.get('data', {}).get('api_docs', '')
            if '/update/' in api_docs:
                # Find the IDOName
                for line in api_docs.split('\n'):
                    if 'ENDPOINT:' in line or 'IDOName' in line or '/update/' in line:
                        print(f"  {line.strip()}")

else:
    print(f"[ERROR] Failed to fetch tools")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
