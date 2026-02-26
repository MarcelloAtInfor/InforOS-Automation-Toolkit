"""
Get detailed information for a specific Document Processor Flow (DPF)
Usage: python get_dpf_details.py <dpf_guid>
"""
import json
import requests
import sys
from pathlib import Path

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDP_URL

# Get DPF GUID from command line or use default
if len(sys.argv) > 1:
    dpf_guid = sys.argv[1]
else:
    # Try to find CSI_COCreation_Extract from the list
    list_file = Path(__file__).parent.parent / "exports" / "dpf_list.json"
    if list_file.exists():
        with open(list_file, 'r') as f:
            dpf_list = json.load(f)
        # Search for CSI_COCreation_Extract
        for dpf in dpf_list.get('data', []):
            name = dpf.get('name', dpf.get('Name', ''))
            if 'COCreation' in name or 'CSI_CO' in name:
                dpf_guid = dpf.get('dpfGuid', dpf.get('DpfGuid', dpf.get('guid', '')))
                print(f"Found DPF: {name}")
                print(f"GUID: {dpf_guid}")
                break
        else:
            print("[ERROR] Could not find CSI_COCreation_Extract DPF.")
            print("Please provide a DPF GUID as argument: python get_dpf_details.py <guid>")
            exit(1)
    else:
        print("[ERROR] No DPF GUID provided and no dpf_list.json found.")
        print("Run list_dpfs.py first or provide GUID as argument.")
        exit(1)

# IDP API base URL
BASE_URL = IDP_URL()

# Get DPF details endpoint
url = f"{BASE_URL}/ui/v1/DocumentProcessorFlows/{dpf_guid}"

headers = get_auth_headers()

print(f"\nGetting DPF details from: {url}")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    result = response.json()
    print(f"\n[SUCCESS] DPF details retrieved!")

    # Pretty print the response
    print(f"\nResponse:")
    print(json.dumps(result, indent=2))

    # Save to file
    dpf_name = result.get('name', result.get('Name', 'unknown'))
    safe_name = dpf_name.replace(' ', '_').replace('/', '_')
    output_file = Path(__file__).parent.parent / "exports" / f"{safe_name}_details.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n[SUCCESS] Details saved to: {output_file}")

else:
    print(f"\n[ERROR] Failed to get DPF details")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
