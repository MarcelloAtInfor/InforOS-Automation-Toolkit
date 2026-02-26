"""
Test updating with all key fields to see if we need more than just _ItemId and DueDate
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

# Step 1: Query to get ALL properties of one order line
print("Step 1: Querying for one order line with ALL properties")
print("=" * 60)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
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

if not query_data.get('Items') or len(query_data['Items']) == 0:
    print("\n[ERROR] No order lines found")
    exit(1)

# Get the first item
item = query_data['Items'][0]
print("Full Order Line Record:")
print(json.dumps(item, indent=2))

# Try update with key fields
print("\n" + "=" * 60)
print("Step 2: Calculate previous Sunday")
print("=" * 60)

today = datetime.now()
days_since_sunday = (today.weekday() + 1) % 7
if days_since_sunday == 0:
    days_since_sunday = 7
previous_sunday = today - timedelta(days=days_since_sunday)
new_due_date = previous_sunday.strftime('%Y%m%d')

print(f"New DueDate (YYYYMMDD): {new_due_date}")

# Test 1: Update with _ItemId + CoNum + CoLine + DueDate
print("\n" + "=" * 60)
print("Test 1: Update with _ItemId, CoNum, CoLine, DueDate")
print("=" * 60)

update_url = f"{IDO_URL()}/update/SLCoitems"
update_headers = get_auth_headers()
update_headers['X-Infor-MongooseConfig'] = get_site()

update_body = {
    "SLCoitems": [
        {
            "_ItemId": item.get('_ItemId'),
            "CoNum": item.get('CoNum'),
            "CoLine": item.get('CoLine'),
            "DueDate": new_due_date
        }
    ]
}

print("Update Request Body:")
print(json.dumps(update_body, indent=2))

update_response = requests.post(update_url, headers=update_headers, json=update_body)
print(f"\nStatus Code: {update_response.status_code}")
print("Update Response:")
print(json.dumps(update_response.json(), indent=2))

# Test 2: Try using CoNum and CoLine as identifiers instead of _ItemId
if not update_response.json().get('Success'):
    print("\n" + "=" * 60)
    print("Test 2: Update with CoNum + CoLine (no _ItemId)")
    print("=" * 60)

    update_body2 = {
        "SLCoitems": [
            {
                "CoNum": item.get('CoNum'),
                "CoLine": item.get('CoLine'),
                "DueDate": new_due_date
            }
        ]
    }

    print("Update Request Body:")
    print(json.dumps(update_body2, indent=2))

    update_response2 = requests.post(update_url, headers=update_headers, json=update_body2)
    print(f"\nStatus Code: {update_response2.status_code}")
    print("Update Response:")
    print(json.dumps(update_response2.json(), indent=2))

print("\n" + "=" * 60)
