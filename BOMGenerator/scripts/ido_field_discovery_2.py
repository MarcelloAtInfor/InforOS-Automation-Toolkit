#!/usr/bin/env python3
"""
Round 2 discovery: Valid ProductCodes, SLJobs Job number requirements,
and deeper investigation of existing standard job properties.
"""

import json
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

SITE = get_site()


def load_ido(headers, ido_name, filter_str, properties, record_cap=20):
    """Query IDO records."""
    url = f"{IDO_URL()}/load/{ido_name}"
    h = {**headers, "X-Infor-MongooseConfig": SITE}
    params = {"properties": properties, "filter": filter_str, "recordCap": record_cap}
    resp = requests.get(url, headers=h, params=params)
    print(f"\n--- Load {ido_name} (filter: {filter_str}) [Status: {resp.status_code}] ---")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items") or []
        print(f"Records found: {len(items)}")
        if not items:
            print(f"  Raw response keys: {list(data.keys())}")
            # Print first 500 chars of response for debugging
            raw = json.dumps(data)[:500]
            print(f"  Raw response: {raw}")
        for item in items:
            print(f"  {json.dumps(item, indent=4)}")
        return data
    else:
        print(f"Error: {resp.text[:500]}")
        return None


def prop(name, value):
    return {"IsNull": False, "Modified": True, "Name": name, "Value": value}


def test_insert(headers, ido_name, properties_list, description=""):
    url = f"{IDO_URL()}/update/{ido_name}"
    h = {**headers, "X-Infor-MongooseConfig": SITE, "Content-Type": "application/json"}
    payload = {
        "IDOName": ido_name,
        "RefreshAfterSave": True,
        "Changes": [{"Action": 1, "Properties": properties_list}]
    }
    print(f"\n{'='*60}")
    print(f"TEST INSERT: {ido_name} - {description}")
    print(f"{'='*60}")
    for p in properties_list:
        print(f"  {p['Name']}: {p['Value']}")
    resp = requests.post(url, headers=h, json=payload)
    print(f"\nStatus: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        success = data.get("Success", False)
        message = data.get("Message", "")
        print(f"Success: {success}")
        if message:
            print(f"Message: {message}")
        if success:
            items = data.get("Items", [])
            if items:
                # Print ALL returned properties to see what the system populated
                print(f"Created record (all fields):")
                for key, val in items[0].items():
                    if val and val != "0" and val != "0.00000000" and not key.startswith("_"):
                        print(f"    {key}: {val}")
                print(f"  _ItemId: {items[0].get('_ItemId', 'N/A')}")
        return data
    else:
        print(f"HTTP Error: {resp.text[:1000]}")
        return None


def main():
    headers = get_auth_headers()

    # ---- 1: Discover valid ProductCodes ----
    print("=" * 60)
    print("1. DISCOVER VALID PRODUCT CODES")
    print("=" * 60)
    # SLProductCodes IDO should have the valid codes
    load_ido(headers, "SLProductCodes", "1=1", "ProductCode,Description", 50)

    # ---- 2: Look at ALL properties of existing standard jobs ----
    print("\n\n" + "=" * 60)
    print("2. EXISTING STANDARD JOB - ALL PROPERTIES")
    print("=" * 60)
    # Get full detail of job 1 (FA-10000)
    load_ido(headers, "SLJobs",
             "Type = 'S' AND Job = '         1'",
             "Job,Suffix,Item,Type,Stat,QtyReleased,Whse,Description,UM,OrdType,ProdMix,StartDate,EffectDate,RootJob,RootSuf,SchedDriver,LowLevel",
             1)

    # ---- 3: Try SLJobs insert with explicit Job number ----
    print("\n\n" + "=" * 60)
    print("3. TEST SLJobs INSERT WITH EXPLICIT JOB NUMBER")
    print("=" * 60)

    # Try with an explicit high job number to avoid conflicts
    test_insert(headers, "SLJobs", [
        prop("Job", "     99901"),
        prop("Item", "BOMTEST-001"),
        prop("Suffix", "0"),
        prop("Type", "S"),
        prop("Stat", "F"),
        prop("QtyReleased", "1.00"),
        prop("Whse", "MAIN"),
    ], "Explicit Job number 99901")

    # ---- 4: Try without Job number but with more fields ----
    print("\n\n" + "=" * 60)
    print("4. TEST SLJobs INSERT - NO JOB NUMBER, MORE FIELDS")
    print("=" * 60)

    test_insert(headers, "SLJobs", [
        prop("Item", "BOMTEST-001"),
        prop("Suffix", "0"),
        prop("Type", "S"),
        prop("Stat", "F"),
        prop("QtyReleased", "1.00"),
        prop("Whse", "MAIN"),
        prop("Description", "Test Standard Job"),
        prop("LowLevel", "0"),
    ], "No Job number, added Description + LowLevel")

    # ---- 5: Item insert with PMTCode=P and a valid ProductCode ----
    print("\n\n" + "=" * 60)
    print("5. TEST ITEM INSERT - PMTCode=P WITH VALID PRODUCTCODE")
    print("=" * 60)
    # Will use the first valid ProductCode found in step 1
    # For now try FG-100 which we know works from earlier tests
    test_insert(headers, "SLItems", [
        prop("Item", "BOMTEST-003"),
        prop("Description", "BOM Test Item - Purchased with FG-100"),
        prop("UM", "EA"),
        prop("MatlType", "M"),
        prop("PMTCode", "P"),
        prop("ProductCode", "FG-100"),
        prop("AbcCode", "B"),
        prop("CostType", "A"),
        prop("CostMethod", "S"),
        prop("Stat", "A"),
    ], "PMTCode=P with ProductCode=FG-100")

    print("\n\n### ROUND 2 DISCOVERY COMPLETE ###")


if __name__ == "__main__":
    main()
