"""
Rollback the 20 order lines to their original due date: 2017-01-01
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

# Order lines to rollback
orders_to_rollback = [
    ("DC00000120", "1"),
    ("DC00000120", "2"),
    ("DC00000120", "3"),
    ("DC00000120", "4"),
    ("DC00000117", "1"),
    ("DC00000117", "2"),
    ("DC00000117", "3"),
    ("DC00000117", "4"),
    ("DC00000115", "2"),
    ("DC00000115", "6"),
    ("DC00000113", "1"),
    ("DC00000113", "2"),
    ("DC00000111", "5"),
    ("DC00000110", "1"),
    ("DC00000110", "2"),
    ("DC00000110", "3"),
    ("DC00000110", "4"),
    ("DC00000106", "1"),
    ("DC00000106", "2"),
    ("DC00000106", "3"),
]

print("Step 1: Querying for _ItemId values")
print("=" * 70)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_headers = get_auth_headers()
query_headers['X-Infor-MongooseConfig'] = get_site()

# Build filter to get all 20 order lines
filter_parts = []
for co_num, co_line in orders_to_rollback:
    filter_parts.append(f"(CoNum='{co_num}' AND CoLine='{co_line}')")
filter_clause = " OR ".join(filter_parts)

query_params = {
    'properties': 'CoNum,CoLine,DueDate,_ItemId',
    'filter': filter_clause,
    'recordCap': '50'
}

query_response = requests.get(query_url, headers=query_headers, params=query_params)
print(f"Query Status Code: {query_response.status_code}\n")

if query_response.status_code != 200:
    print(f"[ERROR] Query failed: {query_response.text}")
    exit(1)

query_data = query_response.json()
items = query_data.get('Items', [])

print(f"Found {len(items)} order lines to rollback\n")

if len(items) == 0:
    print("[ERROR] No order lines found")
    exit(1)

# Display what we found
for item in items:
    print(f"  {item.get('CoNum')}-{item.get('CoLine'):>2} | Current DueDate: {item.get('DueDate')}")

print(f"\n" + "=" * 70)
print("Step 2: Building rollback update request")
print("=" * 70)

# Build the Changes array
changes = []
for item in items:
    change = {
        "Action": 2,
        "ItemId": item.get('_ItemId'),
        "Properties": [
            {
                "IsNull": False,
                "Modified": True,
                "Name": "DueDate",
                "Value": "20170101"  # January 1, 2017
            }
        ]
    }
    changes.append(change)

update_body = {
    "IDOName": "SLCoitems",
    "RefreshAfterSave": True,
    "Changes": changes
}

print(f"Prepared {len(changes)} changes to rollback to 2017-01-01")

# Execute the rollback
print(f"\n" + "=" * 70)
print("Step 3: Executing rollback update")
print("=" * 70)

update_url = f"{IDO_URL()}/update/SLCoitems"
update_headers = get_auth_headers()
update_headers['X-Infor-MongooseConfig'] = get_site()

update_response = requests.post(update_url, headers=update_headers, json=update_body)
print(f"Update Status Code: {update_response.status_code}")

update_data = update_response.json()
print(f"\nUpdate Response:")
print(f"  Success: {update_data.get('Success')}")
print(f"  Message: {update_data.get('Message')}")

if update_data.get('Success'):
    print(f"\n[SUCCESS] Rolled back {len(changes)} order lines to 2017-01-01!")

    # List the orders
    print(f"\nRolled Back Orders:")
    for item in items:
        print(f"  {item.get('CoNum')}-{item.get('CoLine'):>2}")
else:
    print(f"\n[ERROR] Rollback failed: {update_data.get('Message')}")

print("\n" + "=" * 70)
