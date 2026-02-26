"""
Query sample customer order lines to understand field structure
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

# API endpoint
url = f"{IDO_URL()}/load/SLCoitems"

headers = get_auth_headers()
headers['X-Infor-MongooseConfig'] = get_site()

# Query parameters - get just a few records with key fields
params = {
    'recordCap': 3,
    'properties': 'CoNum,CoLine,CustNum,Item,DueDate,QtyOrderedConv,Stat,_ItemId'
}

print("Querying Sample Customer Order Lines")
print("=" * 60)
print(f"GET {url}")
print(f"Parameters: {params}\n")

response = requests.get(url, headers=headers, params=params)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()

    print(f"[SUCCESS] Query successful!")
    print(f"Records returned: {len(data.get('Items', []))}")
    print(f"More rows exist: {data.get('MoreRowsExist')}\n")

    if data.get('Items'):
        print("Sample Order Lines:")
        print("-" * 60)
        for item in data['Items']:
            print(json.dumps(item, indent=2))
            print("-" * 60)

    # Save full response
    response_file = Path(__file__).parent / "coitems_sample.json"
    with open(response_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Query failed")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
