"""
Test the correct API format directly (batch update of 2 order lines)
"""
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

# Step 1: Query to get 2 order lines
print("Step 1: Querying for 2 order lines")
print("=" * 60)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
    'properties': 'CoNum,CoLine,Item,DueDate,_ItemId',
    'orderBy': 'DueDate ASC',
    'recordCap': '2'
}
query_headers = get_auth_headers()
query_headers['X-Infor-MongooseConfig'] = get_site()

query_response = requests.get(query_url, headers=query_headers, params=query_params)
print(f"Status Code: {query_response.status_code}\n")

if query_response.status_code != 200:
    print(f"[ERROR] Query failed")
    print(f"Response: {query_response.text}")
    exit(1)

query_data = query_response.json()
items = query_data.get('Items', [])

if len(items) < 2:
    print("\n[ERROR] Need at least 2 order lines")
    exit(1)

print(f"Found {len(items)} order lines:")
for item in items:
    print(f"  {item.get('CoNum')}-{item.get('CoLine')} | Item: {item.get('Item')} | DueDate: {item.get('DueDate')}")

# Calculate previous Sunday
today = datetime.now()
days_since_sunday = (today.weekday() + 1) % 7
if days_since_sunday == 0:
    days_since_sunday = 7
previous_sunday = today - timedelta(days=days_since_sunday)
new_due_date = previous_sunday.strftime('%Y%m%d')

print(f"\nNew DueDate: {new_due_date} (previous Sunday)")

# Step 2: Build correct API format
print("\n" + "=" * 60)
print("Step 2: Update using correct API format")
print("=" * 60)

update_url = f"{IDO_URL()}/update/SLCoitems"
update_headers = get_auth_headers()
update_headers['X-Infor-MongooseConfig'] = get_site()

# Build Changes array with correct format
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
                "Value": new_due_date
            }
        ]
    }
    changes.append(change)

update_body = {
    "IDOName": "SLCoitems",
    "RefreshAfterSave": True,
    "Changes": changes
}

print("Update Request Body:")
print(json.dumps(update_body, indent=2))

update_response = requests.post(update_url, headers=update_headers, json=update_body)
print(f"\nStatus Code: {update_response.status_code}")
print("\nUpdate Response:")
print(json.dumps(update_response.json(), indent=2))

if update_response.status_code == 200:
    update_data = update_response.json()
    if update_data.get('Success'):
        print(f"\n[SUCCESS] Updated {len(items)} order lines!")
    else:
        print(f"\n[ERROR] Update failed: {update_data.get('Message')}")
else:
    print(f"\n[ERROR] Update request failed")

print("\n" + "=" * 60)
