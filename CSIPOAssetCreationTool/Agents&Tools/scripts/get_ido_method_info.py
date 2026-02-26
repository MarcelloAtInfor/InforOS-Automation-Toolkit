"""
Get IDO method information to understand stored procedure signatures.
"""
import requests
import json
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

headers = get_auth_headers()
headers['X-Infor-MongooseConfig'] = get_site()

# Get info about SLPoItems IDO
url = f"{IDO_URL()}/info/SLPoItems"
print(f"Getting IDO info from: {url}")
print("-" * 60)

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    # Look for receiving-related methods
    methods = data.get('Methods', [])
    print(f"Found {len(methods)} methods\n")

    # Print ALL methods
    for m in methods:
        name = m.get('Name', '')
        params = m.get('Parameters', [])
        print(f"{name} ({len(params)} params)")
else:
    print(f'Error: {response.status_code}')
    print(response.text[:1000])
