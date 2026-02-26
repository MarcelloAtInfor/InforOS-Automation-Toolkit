#!/usr/bin/env python3
"""
Test: Create a job with "BOM" prefix to verify SLHighKeys auto-registration.

Steps:
1. Create a test item (BOM-PREFIX-TEST) if it doesn't exist
2. Create a standard job with Job='BOM0000001'
3. Query SLHighKeys to see if Prefix='BOM' entry was auto-created
4. Clean summary of results

Usage:
    python test_bom_prefix_job.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

SITE = get_site()

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def get_headers():
    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = SITE
    return headers


def ido_load(headers, ido, filter_str, properties="", record_cap=50):
    """Load records from an IDO."""
    url = f"{IDO_URL()}/load/{ido}"
    params = {"filter": filter_str, "recordCap": record_cap}
    if properties:
        params["properties"] = properties
    resp = requests.get(url, headers=headers, params=params)
    return resp


def ido_update(headers, ido, changes):
    """Insert/update records via IDO."""
    url = f"{IDO_URL()}/update/{ido}"
    payload = {
        "IDOName": ido,
        "RefreshAfterSave": True,
        "Changes": changes
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp


def step(num, msg):
    print(f"\n{'='*60}")
    print(f"  Step {num}: {msg}")
    print(f"{'='*60}")


def main():
    headers = get_headers()
    test_item = "BOM-PREFIX-TEST"
    test_job = "BOM0000001"  # Exactly 10 chars, no padding needed

    # ----- Step 1: Check/create test item -----
    step(1, f"Check if item '{test_item}' exists")
    resp = ido_load(headers, "SLItems", f"Item = '{test_item}'",
                    properties="Item,Description,UM,PMTCode,Stat")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        items = resp.json().get("Items", [])
        if items:
            print(f"  Item already exists: {json.dumps(items[0], indent=None)}")
        else:
            print(f"  Item not found. Creating '{test_item}'...")
            resp2 = ido_update(headers, "SLItems", [
                {
                    "Action": 1,
                    "Properties": [
                        {"IsNull": False, "Modified": True, "Name": "Item", "Value": test_item},
                        {"IsNull": False, "Modified": True, "Name": "Description", "Value": "BOM prefix test item (safe to delete)"},
                        {"IsNull": False, "Modified": True, "Name": "UM", "Value": "EA"},
                        {"IsNull": False, "Modified": True, "Name": "PMTCode", "Value": "M"},
                        {"IsNull": False, "Modified": True, "Name": "ProductCode", "Value": "FG-100"},
                        {"IsNull": False, "Modified": True, "Name": "CostType", "Value": "A"},
                        {"IsNull": False, "Modified": True, "Name": "CostMethod", "Value": "S"},
                    ]
                }
            ])
            print(f"  Insert HTTP {resp2.status_code}")
            if resp2.status_code == 200:
                data = resp2.json()
                if data.get("Success") is False:
                    print(f"  ERROR: {data.get('Message', 'Unknown error')}")
                    sys.exit(1)
                print(f"  Item created successfully")
            else:
                print(f"  ERROR: {resp2.text[:300]}")
                sys.exit(1)
    else:
        print(f"  ERROR: {resp.text[:300]}")
        sys.exit(1)

    # ----- Step 2: Check SLHighKeys BEFORE job insert -----
    step(2, "Check SLHighKeys BEFORE job insert (Prefix='BOM')")
    resp = ido_load(headers, "SLHighKeys", "Prefix = 'BOM'")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        items = resp.json().get("Items", [])
        print(f"  Records with Prefix='BOM': {len(items)}")
        for item in items:
            print(f"    HighKey={item.get('HighKey')}, TableColumnName={item.get('TableColumnName')}")
    else:
        print(f"  ERROR: {resp.text[:300]}")

    # ----- Step 3: Check if job already exists -----
    step(3, f"Check if job '{test_job}' already exists")
    resp = ido_load(headers, "SLJobs", f"Job = '{test_job}'",
                    properties="Job,Suffix,Item,Type,Stat")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        jobs = resp.json().get("Items", [])
        if jobs:
            print(f"  Job already exists: {json.dumps(jobs[0], indent=None)}")
            print(f"  Skipping job creation (already done).")
        else:
            # ----- Step 3b: Create the BOM-prefixed job -----
            print(f"  Job not found. Creating job '{test_job}' for item '{test_item}'...")
            resp2 = ido_update(headers, "SLJobs", [
                {
                    "Action": 1,
                    "Properties": [
                        {"IsNull": False, "Modified": True, "Name": "Job", "Value": test_job},
                        {"IsNull": False, "Modified": True, "Name": "Item", "Value": test_item},
                        {"IsNull": False, "Modified": True, "Name": "Suffix", "Value": "0"},
                        {"IsNull": False, "Modified": True, "Name": "Type", "Value": "S"},
                        {"IsNull": False, "Modified": True, "Name": "Stat", "Value": "F"},
                        {"IsNull": False, "Modified": True, "Name": "QtyReleased", "Value": "1.00"},
                        {"IsNull": False, "Modified": True, "Name": "Whse", "Value": "MAIN"},
                    ]
                }
            ])
            print(f"  Insert HTTP {resp2.status_code}")
            if resp2.status_code == 200:
                data = resp2.json()
                if data.get("Success") is False:
                    print(f"  ERROR: {data.get('Message', 'Unknown error')}")
                    # Print full response for debugging
                    print(f"  Full response: {json.dumps(data, indent=2)[:500]}")
                    sys.exit(1)
                print(f"  Job created successfully!")
                # Show the returned job record
                result_items = data.get("Items", [])
                if result_items:
                    job_rec = result_items[0]
                    job_num = job_rec.get("Job", "?")
                    print(f"  Returned Job value: '{job_num}' (repr: {repr(job_num)})")
            else:
                print(f"  ERROR: {resp2.text[:500]}")
                sys.exit(1)
    else:
        print(f"  ERROR: {resp.text[:300]}")
        sys.exit(1)

    # ----- Step 4: Check SLHighKeys AFTER job insert -----
    step(4, "Check SLHighKeys AFTER job insert (Prefix='BOM')")
    resp = ido_load(headers, "SLHighKeys", "Prefix = 'BOM'")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        items = resp.json().get("Items", [])
        print(f"  Records with Prefix='BOM': {len(items)}")
        if items:
            for item in items:
                print(f"    HighKey: '{item.get('HighKey')}'")
                print(f"    Prefix: '{item.get('Prefix')}'")
                print(f"    TableColumnName: '{item.get('TableColumnName')}'")
                print(f"    RowPointer: '{item.get('RowPointer')}'")
            print(f"\n  SUCCESS: SLHighKeys auto-registered the 'BOM' prefix!")
        else:
            print(f"  No BOM prefix entry found after job insert.")
            print(f"  SLHighKeys did NOT auto-register. Manual insert may be needed.")
    else:
        print(f"  ERROR: {resp.text[:300]}")

    # ----- Step 5: Also query all job entries to see full picture -----
    step(5, "All job.job entries in SLHighKeys (for reference)")
    resp = ido_load(headers, "SLHighKeys", "TableColumnName = 'job.job'",
                    properties="Prefix,HighKey,RowPointer")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        items = resp.json().get("Items") or []
        print(f"  Total job entries: {len(items)}")
        for item in items:
            prefix = item.get("Prefix") or "(null)"
            highkey = item.get("HighKey", "?")
            print(f"    Prefix='{prefix}' -> HighKey='{highkey}'")
    else:
        print(f"  ERROR: {resp.text[:300]}")

    print(f"\n{'='*60}")
    print(f"  Test complete.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
