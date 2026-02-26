"""
Verify that the order lines were actually updated in the database
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

# Query order lines with due date = 20260125 (previous Sunday)
print("Verifying updated order lines")
print("=" * 60)
print("Querying for order lines with DueDate = 20260125")
print()

query_url = f"{IDO_URL()}/load/SLCoitems"
query_params = {
    'properties': 'CoNum,CoLine,Item,DueDate',
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

print(f"[SUCCESS] Found {len(items)} order lines with DueDate = 20260125\n")

if items:
    print("Updated Order Lines:")
    print("-" * 60)
    for i, item in enumerate(items, 1):
        print(f"{i:2}. Order: {item.get('CoNum')}-{item.get('CoLine'):>2} | "
              f"Item: {item.get('Item'):12} | DueDate: {item.get('DueDate')}")
    print("-" * 60)
else:
    print("No order lines found with the updated due date.")

print("\n" + "=" * 60)
