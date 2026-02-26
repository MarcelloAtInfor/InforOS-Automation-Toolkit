"""
Import a Document Processor Flow (DPF) configuration
Usage: python import_dpf.py <config_file.json>
"""
import json
import requests
import sys
from pathlib import Path

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers, request_token
from shared.config import IDP_URL

# Get config file from command line
if len(sys.argv) > 1:
    config_path = Path(sys.argv[1])
    if not config_path.is_absolute():
        # Try relative to configs directory
        config_path = Path(__file__).parent.parent / "configs" / sys.argv[1]
else:
    # Default to AP_Invoice_Extract.json
    config_path = Path(__file__).parent.parent / "configs" / "AP_Invoice_Extract.json"

if not config_path.exists():
    print(f"[ERROR] Config file not found: {config_path}")
    print("Please provide a valid config file path.")
    exit(1)

print(f"Loading config from: {config_path}")

# IDP API base URL
BASE_URL = IDP_URL()

# Import DPF endpoint - uses multipart/form-data
url = f"{BASE_URL}/ui/v1/ImportDPF"

# Get token for Authorization header only (don't set Content-Type for multipart)
access_token = request_token()
headers = {
    "Authorization": f"Bearer {access_token}"
    # Note: Don't set Content-Type - requests will set it automatically for multipart
}

# Read the config file and send as multipart form data
with open(config_path, 'rb') as f:
    files = {
        'datajsonfile': (config_path.name, f, 'application/json')
    }

    print(f"\nImporting DPF to: {url}")
    response = requests.post(url, headers=headers, files=files)

if response.status_code == 200:
    result = response.json() if response.text else {}
    print(f"\n[SUCCESS] DPF imported successfully!")

    if result:
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))

    # Verify by listing DPFs
    print("\n[INFO] Run list_dpfs.py to verify the new DPF was created.")

elif response.status_code == 201:
    print(f"\n[SUCCESS] DPF created successfully!")
    if response.text:
        print(f"\nResponse:")
        print(json.dumps(response.json(), indent=2))

else:
    print(f"\n[ERROR] Failed to import DPF")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
