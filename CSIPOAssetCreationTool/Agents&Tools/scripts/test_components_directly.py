"""
Test the updated components directly without the agent
1. Verify query tool filters by Stat='O'
2. Calculate correct Sunday date
3. Perform batch update with correct date
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

print("=" * 70)
print("Step 1: Calculate Previous Sunday (CORRECTED)")
print("=" * 70)

# Correct date calculation
today = datetime.now()
print(f"Today: {today.strftime('%Y-%m-%d (%A)')}")
print(f"Today's weekday value: {today.weekday()} (0=Mon, 6=Sun)")

# Calculate days to go back to most recent Sunday
if today.weekday() == 6:  # Today is Sunday
    days_back = 7  # Go to last Sunday
else:
    days_back = today.weekday() + 1  # Days since last Sunday

previous_sunday = today - timedelta(days=days_back)
sunday_formatted = previous_sunday.strftime('%Y%m%d')

print(f"\nDays to go back: {days_back}")
print(f"Previous Sunday: {previous_sunday.strftime('%Y-%m-%d (%A)')}")
print(f"Formatted for API: {sunday_formatted}")

# Verify it's actually Sunday
if previous_sunday.weekday() != 6:
    print(f"\nERROR: Calculated date is not a Sunday!")
else:
    print(f"[OK] Verified: {previous_sunday.strftime('%Y-%m-%d')} is a Sunday")

print("\n" + "=" * 70)
print("Step 2: Query Order Lines with Stat='O' Filter")
print("=" * 70)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
    'properties': 'CoNum,CoLine,Item,Stat,DueDate,_ItemId',
    'filter': "Stat='O'",  # Only Ordered status
    'orderBy': 'DueDate ASC',
    'recordCap': '5'  # Test with just 5 lines
}
query_headers = get_auth_headers()
query_headers['X-Infor-MongooseConfig'] = get_site()

query_response = requests.get(query_url, headers=query_headers, params=query_params)
print(f"Query Status Code: {query_response.status_code}\n")

if query_response.status_code != 200:
    print(f"[ERROR] Query failed: {query_response.text}")
    exit(1)

query_data = query_response.json()
items = query_data.get('Items', [])

print(f"Found {len(items)} order lines with Stat='O':\n")
for item in items:
    print(f"  {item.get('CoNum')}-{item.get('CoLine'):>2} | "
          f"Stat: {item.get('Stat')} | DueDate: {item.get('DueDate')}")

if len(items) == 0:
    print("\n[WARNING] No order lines with Stat='O' found")
    exit(0)

# Verify all have Stat='O'
all_ordered = all(item.get('Stat') == 'O' for item in items)
if all_ordered:
    print(f"\n[OK] All {len(items)} order lines have Stat='O' (filter working!)")
else:
    print(f"\n[WARN]  WARNING: Some order lines don't have Stat='O'")

print("\n" + "=" * 70)
print("Step 3: Batch Update with Correct Sunday Date")
print("=" * 70)

# Build Changes array
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
                "Value": sunday_formatted  # Using correct Sunday date
            }
        ]
    }
    changes.append(change)

update_body = {
    "IDOName": "SLCoitems",
    "RefreshAfterSave": True,
    "Changes": changes
}

print(f"Updating {len(changes)} order lines to {sunday_formatted} ({previous_sunday.strftime('%Y-%m-%d')})")

update_url = f"{IDO_URL()}/update/SLCoitems"
update_headers = get_auth_headers()
update_headers['X-Infor-MongooseConfig'] = get_site()

update_response = requests.post(update_url, headers=update_headers, json=update_body)
print(f"\nUpdate Status Code: {update_response.status_code}")

update_data = update_response.json()
print(f"Success: {update_data.get('Success')}")
print(f"Message: {update_data.get('Message')}")

if update_data.get('Success'):
    print(f"\n[OK] [SUCCESS] Updated {len(changes)} order lines!")
    print(f"\nUpdated Orders:")
    for item in items:
        print(f"  {item.get('CoNum')}-{item.get('CoLine'):>2}")
    print(f"\nNew DueDate: {sunday_formatted} ({previous_sunday.strftime('%B %d, %Y - %A')})")
else:
    print(f"\n[ERROR] Update failed: {update_data.get('Message')}")

print("\n" + "=" * 70)
