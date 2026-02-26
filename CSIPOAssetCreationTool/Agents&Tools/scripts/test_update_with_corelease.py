"""
Test updating with CoRelease field included (composite key: CoNum + CoLine + CoRelease)
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

# Step 1: Query to get one order line with CoRelease
print("Step 1: Querying for one order line")
print("=" * 60)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
    'properties': 'CoNum,CoLine,CoRelease,Item,DueDate,_ItemId',
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
print(f"\nFound Order Line:")
print(f"  CoNum: {item.get('CoNum')}")
print(f"  CoLine: {item.get('CoLine')}")
print(f"  CoRelease: {item.get('CoRelease')}")
print(f"  Item: {item.get('Item')}")
print(f"  Current DueDate: {item.get('DueDate')}")
print(f"  _ItemId: {item.get('_ItemId')}")

# Calculate previous Sunday
today = datetime.now()
days_since_sunday = (today.weekday() + 1) % 7
if days_since_sunday == 0:
    days_since_sunday = 7
previous_sunday = today - timedelta(days=days_since_sunday)
new_due_date = previous_sunday.strftime('%Y%m%d')

print(f"\nNew DueDate (YYYYMMDD): {new_due_date}")

# Test 1: Update with CoNum, CoLine, CoRelease, DueDate
print("\n" + "=" * 60)
print("Test 1: Update with CoNum + CoLine + CoRelease + DueDate")
print("=" * 60)

update_url = f"{IDO_URL()}/update/SLCoitems"
update_headers = get_auth_headers()
update_headers['X-Infor-MongooseConfig'] = get_site()

update_body = {
    "SLCoitems": [
        {
            "CoNum": item.get('CoNum'),
            "CoLine": item.get('CoLine'),
            "CoRelease": item.get('CoRelease'),
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

# Test 2: Try with _ItemId + CoNum + CoLine + CoRelease
if not update_response.json().get('Success'):
    print("\n" + "=" * 60)
    print("Test 2: Update with _ItemId + all key fields")
    print("=" * 60)

    update_body2 = {
        "SLCoitems": [
            {
                "_ItemId": item.get('_ItemId'),
                "CoNum": item.get('CoNum'),
                "CoLine": item.get('CoLine'),
                "CoRelease": item.get('CoRelease'),
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
