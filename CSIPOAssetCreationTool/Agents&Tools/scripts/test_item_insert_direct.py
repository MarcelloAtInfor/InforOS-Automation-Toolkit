"""
Test ItemInsert_Tool_v2 directly by calling the API endpoint
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

# API endpoint for direct IDO call
ido_url = f"{IDO_URL()}/update/SLItems"

headers = get_auth_headers()
headers['X-Infor-MongooseConfig'] = get_site()

# Test item data
test_item = {
    "IDOName": "SLItems",
    "RefreshAfterSave": True,
    "Changes": [
        {
            "Action": 1,
            "Properties": [
                {"IsNull": False, "Modified": True, "Name": "Item", "Value": "TEST-DIRECT"},
                {"IsNull": False, "Modified": True, "Name": "Description", "Value": "Test Direct API Call"},
                {"IsNull": False, "Modified": True, "Name": "UM", "Value": "EA"},
                {"IsNull": False, "Modified": True, "Name": "MatlType", "Value": "M"},
                {"IsNull": False, "Modified": True, "Name": "PMTCode", "Value": "M"},
                {"IsNull": False, "Modified": True, "Name": "ProductCode", "Value": "FG-100"},
                {"IsNull": False, "Modified": True, "Name": "AbcCode", "Value": "B"},
                {"IsNull": False, "Modified": True, "Name": "CostType", "Value": "A"},
                {"IsNull": False, "Modified": True, "Name": "CostMethod", "Value": "S"},
                {"IsNull": False, "Modified": True, "Name": "Stat", "Value": "A"}
            ]
        }
    ]
}

print("Testing Direct ItemInsert API Call")
print("=" * 60)
print(f"POST {ido_url}")
print(f"\nRequest Body:")
print(json.dumps(test_item, indent=2))
print()

# Make the request
response = requests.post(ido_url, headers=headers, json=test_item)

print(f"Status Code: {response.status_code}")
print(f"\nResponse:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 200:
    result = response.json()
    if result.get('Success'):
        print("\n[SUCCESS] Item created successfully!")
    else:
        print(f"\n[ERROR] Item creation failed: {result.get('Message')}")
else:
    print("\n[ERROR] API call failed")
