"""
Export a Document Processor Flow (DPF) configuration
Usage: python export_dpf.py <dpf_guid> [output_filename]
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
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
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
                output_name = 'CSI_COCreation_Extract_backup.json'
                print(f"Found DPF: {name}")
                print(f"GUID: {dpf_guid}")
                break
        else:
            print("[ERROR] Could not find CSI_COCreation_Extract DPF.")
            print("Please provide a DPF GUID as argument: python export_dpf.py <guid>")
            exit(1)
    else:
        print("[ERROR] No DPF GUID provided and no dpf_list.json found.")
        print("Run list_dpfs.py first or provide GUID as argument.")
        exit(1)

# IDP API base URL
BASE_URL = IDP_URL()

# Export DPF endpoint
url = f"{BASE_URL}/ui/v1/ExportDPF"

headers = get_auth_headers()

# Request body - array of DPF GUIDs
payload = [
    {"dpfGuid": dpf_guid}
]

print(f"\nExporting DPF from: {url}")
print(f"DPF GUID: {dpf_guid}")
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    # The export might return JSON or a file
    content_type = response.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        result = response.json()
        print(f"\n[SUCCESS] DPF exported!")
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))

        # Save to file
        if not output_name:
            output_name = f"dpf_export_{dpf_guid[:8]}.json"
        output_file = Path(__file__).parent.parent / "exports" / output_name
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n[SUCCESS] Export saved to: {output_file}")
    else:
        # Save raw response
        if not output_name:
            output_name = f"dpf_export_{dpf_guid[:8]}.dat"
        output_file = Path(__file__).parent.parent / "exports" / output_name
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"\n[SUCCESS] Export saved to: {output_file}")
        print(f"Content-Type: {content_type}")
        print(f"Size: {len(response.content)} bytes")

else:
    print(f"\n[ERROR] Failed to export DPF")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
