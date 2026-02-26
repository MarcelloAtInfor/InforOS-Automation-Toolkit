"""
Test updating a single order line due date directly via SyteLine REST API
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

# Step 1: Query to get one order line
print("Step 1: Querying for one order line")
print("=" * 60)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
    'properties': 'CoNum,CoLine,Item,DueDate,_ItemId',
    'orderBy': 'DueDate ASC',
    'recordCap': '1'
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
print("Query Response:")
print(json.dumps(query_data, indent=2))

if not query_data.get('Items') or len(query_data['Items']) == 0:
    print("\n[ERROR] No order lines found")
    exit(1)

# Get the first item
item = query_data['Items'][0]
item_id = item.get('_ItemId')
current_due_date = item.get('DueDate')

print(f"\nFound Order Line:")
print(f"  CoNum: {item.get('CoNum')}")
print(f"  CoLine: {item.get('CoLine')}")
print(f"  Item: {item.get('Item')}")
print(f"  Current DueDate: {current_due_date}")
print(f"  _ItemId: {item_id}")

# Step 2: Calculate previous Sunday
print("\n" + "=" * 60)
print("Step 2: Calculate previous Sunday")
print("=" * 60)

today = datetime.now()
days_since_sunday = (today.weekday() + 1) % 7
if days_since_sunday == 0:
    days_since_sunday = 7
previous_sunday = today - timedelta(days=days_since_sunday)
new_due_date = previous_sunday.strftime('%Y%m%d')

print(f"Today: {today.strftime('%Y-%m-%d')}")
print(f"Previous Sunday: {previous_sunday.strftime('%Y-%m-%d')}")
print(f"New DueDate (YYYYMMDD): {new_due_date}")

# Step 3: Update the order line
print("\n" + "=" * 60)
print("Step 3: Update order line due date")
print("=" * 60)

update_url = f"{IDO_URL()}/update/SLCoitems"
update_headers = get_auth_headers()
update_headers['X-Infor-MongooseConfig'] = get_site()

update_body = {
    "SLCoitems": [
        {
            "_ItemId": item_id,
            "DueDate": new_due_date
        }
    ]
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
        print("\n[SUCCESS] Order line due date updated!")
    else:
        print(f"\n[ERROR] Update failed: {update_data.get('Message')}")
else:
    print(f"\n[ERROR] Update request failed")

print("\n" + "=" * 60)
