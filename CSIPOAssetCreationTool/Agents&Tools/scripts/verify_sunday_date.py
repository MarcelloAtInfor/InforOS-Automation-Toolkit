"""
Verify that order lines were updated to the correct Sunday date (2026-01-25)
and that only Stat='O' orders were updated
"""
import json
import requests
from pathlib import Path
from datetime import datetime
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

# Verify what day 2026-01-25 is
date_20260125 = datetime(2026, 1, 25)
print(f"Date Verification:")
print(f"  2026-01-25 is: {date_20260125.strftime('%A, %B %d, %Y')}")
print(f"  (Should be Sunday)")
print()

# Query order lines updated to 2026-01-25
print("=" * 70)
print("Checking for order lines with DueDate = 20260125")
print("=" * 70)

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
    'properties': 'CoNum,CoLine,Item,Stat,DueDate',
    'filter': "DueDate = '20260125 00:00:00.000'",
    'recordCap': '50'
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

print(f"Found {len(items)} order lines with DueDate = 20260125\n")

if items:
    print("Order Lines Updated:")
    print("-" * 70)
    stat_o_count = 0
    for i, item in enumerate(items, 1):
        stat = item.get('Stat')
        if stat == 'O':
            stat_o_count += 1
        print(f"{i:2}. {item.get('CoNum')}-{item.get('CoLine'):>2} | "
              f"Item: {item.get('Item'):12} | Stat: {stat} | "
              f"DueDate: {item.get('DueDate')}")
    print("-" * 70)
    print(f"\nSummary:")
    print(f"  Total updated: {len(items)}")
    print(f"  With Stat='O': {stat_o_count}")
    if stat_o_count == len(items):
        print(f"  ✅ All updated orders have Stat='O' (correct!)")
    else:
        print(f"  ⚠️  Some orders have different status")
else:
    print("No order lines found with DueDate = 20260125")
    print("The agent may not have run yet or used a different date.")

print("\n" + "=" * 70)
