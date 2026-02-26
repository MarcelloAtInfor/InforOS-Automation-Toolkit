"""
List all Document Processor Flows (DPFs) in the IDP system
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDP_URL

# IDP API base URL
BASE_URL = IDP_URL()

# List DPFs endpoint
url = f"{BASE_URL}/ui/v1/DocumentProcessorFlows/List"

headers = get_auth_headers()

# GridFilters request body
payload = {
    "currentPage": 1,
    "pageSize": 100,
    "sortColumn": "name",
    "sortDirection": "ASC",
    "reqFilterExpression": []
}

print(f"Listing DPFs from: {url}")
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    result = response.json()
    print(f"\n[SUCCESS] DPFs retrieved successfully!")

    # Pretty print the response
    print(f"\nResponse:")
    print(json.dumps(result, indent=2))

    # Save full response for reference
    output_file = Path(__file__).parent.parent / "exports" / "dpf_list.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n[SUCCESS] Full response saved to: {output_file}")

    # Extract and display DPF names and GUIDs if available
    if 'data' in result:
        print(f"\n{'='*60}")
        print("Document Processor Flows:")
        print(f"{'='*60}")
        for dpf in result.get('data', []):
            name = dpf.get('name', dpf.get('Name', 'Unknown'))
            guid = dpf.get('dpfGuid', dpf.get('DpfGuid', dpf.get('guid', 'Unknown')))
            print(f"  - {name}")
            print(f"    GUID: {guid}")
            print()

else:
    print(f"\n[ERROR] Failed to list DPFs")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
