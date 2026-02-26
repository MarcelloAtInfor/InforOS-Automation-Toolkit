#!/usr/bin/env python3
"""
Discover required fields and valid values for BOMGenerator IDOs.
Queries /info/ endpoints and attempts test inserts to validate tool specs.
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


def get_ido_info(headers, ido_name):
    """Query IDO metadata to discover all properties and their attributes."""
    url = f"{IDO_URL()}/info/{ido_name}"
    headers["X-Infor-MongooseConfig"] = SITE
    resp = requests.get(url, headers=headers)
    print(f"\n{'='*60}")
    print(f"IDO INFO: {ido_name} (Status: {resp.status_code})")
    print(f"{'='*60}")
    if resp.status_code == 200:
        data = resp.json()
        # Print property details
        props = data.get("Properties", [])
        print(f"Total properties: {len(props)}")
        print(f"\n--- Properties with RequiredForInsert or RequiredForUpdate ---")
        for p in props:
            name = p.get("Name", "")
            req_insert = p.get("RequiredForInsert", False)
            req_update = p.get("RequiredForUpdate", False)
            read_only = p.get("ReadOnly", False)
            prop_type = p.get("Type", "")
            default = p.get("DefaultValue", "")
            if req_insert or req_update:
                print(f"  {name}: Type={prop_type}, ReqInsert={req_insert}, ReqUpdate={req_update}, ReadOnly={read_only}, Default='{default}'")

        print(f"\n--- All writable properties (ReadOnly=False) ---")
        for p in props:
            name = p.get("Name", "")
            read_only = p.get("ReadOnly", False)
            prop_type = p.get("Type", "")
            default = p.get("DefaultValue", "")
            req_insert = p.get("RequiredForInsert", False)
            if not read_only and not name.startswith("_"):
                marker = " [REQ]" if req_insert else ""
                print(f"  {name}: Type={prop_type}, Default='{default}'{marker}")
        return data
    else:
        print(f"Error: {resp.text[:500]}")
        return None


def load_ido(headers, ido_name, filter_str, properties, record_cap=5):
    """Query IDO records to see real data patterns."""
    url = f"{IDO_URL()}/load/{ido_name}"
    headers["X-Infor-MongooseConfig"] = SITE
    params = {
        "properties": properties,
        "filter": filter_str,
        "recordCap": record_cap
    }
    resp = requests.get(url, headers=headers, params=params)
    print(f"\n--- Load {ido_name} (filter: {filter_str}) ---")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items", [])
        print(f"Records found: {len(items)}")
        for item in items[:3]:
            print(f"  {json.dumps(item, indent=4)}")
        return data
    else:
        print(f"Error {resp.status_code}: {resp.text[:500]}")
        return None


def test_insert(headers, ido_name, properties_list, description=""):
    """Attempt a test insert and report the result."""
    url = f"{IDO_URL()}/update/{ido_name}"
    headers["X-Infor-MongooseConfig"] = SITE
    headers["Content-Type"] = "application/json"

    payload = {
        "IDOName": ido_name,
        "RefreshAfterSave": True,
        "Changes": [
            {
                "Action": 1,
                "Properties": properties_list
            }
        ]
    }

    print(f"\n{'='*60}")
    print(f"TEST INSERT: {ido_name} - {description}")
    print(f"{'='*60}")
    print(f"Payload properties:")
    for p in properties_list:
        print(f"  {p['Name']}: {p['Value']}")

    resp = requests.post(url, headers=headers, json=payload)
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
                print(f"Created record:")
                print(f"  {json.dumps(items[0], indent=4)}")
        return data
    else:
        print(f"HTTP Error: {resp.text[:1000]}")
        return None


def prop(name, value):
    """Helper to create a property dict."""
    return {"IsNull": False, "Modified": True, "Name": name, "Value": value}


def main():
    headers = get_auth_headers()

    print("=" * 60)
    print("BOMGenerator IDO Field Discovery")
    print("=" * 60)

    # ---- Phase 1: IDO Metadata Discovery ----
    print("\n\n### PHASE 1: IDO Metadata Discovery ###\n")

    # Discover SLItems metadata
    items_info = get_ido_info(headers, "SLItems")

    # Discover SLJobs metadata
    jobs_info = get_ido_info(headers, "SLJobs")

    # Discover SLJobRoutes metadata
    routes_info = get_ido_info(headers, "SLJobRoutes")

    # Discover SLJobmatls metadata
    matls_info = get_ido_info(headers, "SLJobmatls")

    # ---- Phase 2: Look at existing data patterns ----
    print("\n\n### PHASE 2: Existing Data Patterns ###\n")

    # Look at existing items for PMTCode values
    load_ido(headers, "SLItems", "PMTCode = 'M'", "Item,Description,UM,PMTCode,MatlType,ProductCode", 3)
    load_ido(headers, "SLItems", "PMTCode = 'P'", "Item,Description,UM,PMTCode,MatlType,ProductCode", 3)
    load_ido(headers, "SLItems", "PMTCode = 'T'", "Item,Description,UM,PMTCode,MatlType,ProductCode", 3)

    # Look at existing standard jobs
    load_ido(headers, "SLJobs", "Type = 'S'", "Job,Suffix,Item,Type,Stat,QtyReleased,Whse", 3)

    # ---- Phase 3: Test Inserts ----
    print("\n\n### PHASE 3: Test Inserts ###\n")

    # Test 1: Item insert with PMTCode='M' (manufactured)
    test_insert(headers, "SLItems", [
        prop("Item", "BOMTEST-001"),
        prop("Description", "BOM Generator Test Item - Manufactured"),
        prop("UM", "EA"),
        prop("MatlType", "M"),
        prop("PMTCode", "M"),
        prop("ProductCode", "FG-100"),
        prop("AbcCode", "B"),
        prop("CostType", "A"),
        prop("CostMethod", "S"),
        prop("Stat", "A"),
    ], "Item with PMTCode=M (manufactured)")

    # Test 2: Item insert with PMTCode='P' (purchased)
    test_insert(headers, "SLItems", [
        prop("Item", "BOMTEST-002"),
        prop("Description", "BOM Generator Test Item - Purchased"),
        prop("UM", "EA"),
        prop("MatlType", "M"),
        prop("PMTCode", "P"),
        prop("ProductCode", "RM-100"),
        prop("AbcCode", "B"),
        prop("CostType", "A"),
        prop("CostMethod", "S"),
        prop("Stat", "A"),
    ], "Item with PMTCode=P (purchased)")

    # Test 3: Standard Job insert (current spec - may be missing fields)
    test_insert(headers, "SLJobs", [
        prop("Item", "BOMTEST-001"),
        prop("Suffix", "0"),
        prop("Type", "S"),
        prop("Stat", "F"),
        prop("QtyReleased", "1.00"),
        prop("Whse", "MAIN"),
    ], "Standard Job with current spec fields")

    # Test 4: Standard Job insert with additional fields from metadata
    # (will add more fields based on what /info/ reveals)

    print("\n\n### DISCOVERY COMPLETE ###")
    print("Review the output above to identify:")
    print("1. Required fields for each IDO")
    print("2. Valid PMTCode values")
    print("3. Missing fields for SLJobs insert")


if __name__ == "__main__":
    main()
