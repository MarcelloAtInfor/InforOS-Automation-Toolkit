#!/usr/bin/env python3
"""
Round 3: Find valid ProductCodes and test routing/material inserts
against the job we created (99901).
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


def load_ido(headers, ido_name, filter_str, properties, record_cap=20, order_by=None):
    url = f"{IDO_URL()}/load/{ido_name}"
    h = {**headers, "X-Infor-MongooseConfig": SITE}
    params = {"properties": properties, "filter": filter_str, "recordCap": record_cap}
    if order_by:
        params["orderBy"] = order_by
    resp = requests.get(url, headers=h, params=params)
    print(f"\n--- Load {ido_name} (filter: {filter_str}) [Status: {resp.status_code}] ---")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items") or []
        msg = data.get("Message", "")
        print(f"Records found: {len(items)}")
        if msg:
            print(f"Message: {msg}")
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
            items = data.get("Items") or []
            if items:
                print(f"Created record (non-null/non-zero fields):")
                for key, val in items[0].items():
                    if val is not None and val != "" and val != "0" and val != "0.00000000" and not key.startswith("_"):
                        print(f"    {key}: {val}")
                print(f"  _ItemId: {items[0].get('_ItemId', 'N/A')}")
        return data
    else:
        print(f"HTTP Error: {resp.text[:1000]}")
        return None


def main():
    headers = get_auth_headers()

    # ---- 1: Find valid ProductCodes from existing items ----
    print("=" * 60)
    print("1. DISCOVER VALID PRODUCT CODES (from SLItems DISTINCT values)")
    print("=" * 60)

    # Try to find a product codes collection
    for ido_name in ["SLProductCd", "SLProdcds", "SLProdcodes"]:
        url = f"{IDO_URL()}/load/{ido_name}"
        h = {**headers, "X-Infor-MongooseConfig": SITE}
        resp = requests.get(url, headers=h, params={"properties": "ProductCode,Description", "recordCap": 5})
        if resp.status_code == 200:
            data = resp.json()
            success = data.get("Success", False)
            items = data.get("Items") or []
            print(f"  Tried {ido_name}: Success={success}, Items={len(items)}")
            if items:
                for item in items:
                    print(f"    {json.dumps(item)}")
        else:
            print(f"  Tried {ido_name}: HTTP {resp.status_code}")

    # Query distinct ProductCode values from existing items
    print("\n--- Distinct ProductCode values from SLItems ---")
    # Get a variety of items to see what ProductCodes exist
    load_ido(headers, "SLItems",
             "ProductCode <> ''",
             "ProductCode",
             50)

    # ---- 2: Check the job we created (99901) ----
    print("\n\n" + "=" * 60)
    print("2. VERIFY CREATED JOB 99901")
    print("=" * 60)
    load_ido(headers, "SLJobs",
             "Job = '     99901'",
             "Job,Suffix,Item,Type,Stat,QtyReleased,Whse,Description",
             1)

    # ---- 3: Test routing insert on job 99901 ----
    print("\n\n" + "=" * 60)
    print("3. TEST ROUTING INSERT ON JOB 99901")
    print("=" * 60)
    test_insert(headers, "SLJobRoutes", [
        prop("Job", "     99901"),
        prop("Suffix", "0"),
        prop("OperNum", "10"),
        prop("Wc", "FA-400"),
        prop("SetupHrsT", "0.50"),
        prop("RunHrsTLbr", "0.25"),
        prop("RunHrsTMch", "0.00"),
    ], "Routing oper 10 on job 99901")

    # ---- 4: Test material insert on job 99901 ----
    print("\n\n" + "=" * 60)
    print("4. TEST MATERIAL INSERT ON JOB 99901")
    print("=" * 60)
    # Use BOMTEST-003 as the child material (created earlier with PMTCode=P)
    test_insert(headers, "SLJobmatls", [
        prop("Job", "     99901"),
        prop("Suffix", "0"),
        prop("OperNum", "10"),
        prop("Sequence", "1"),
        prop("Item", "BOMTEST-003"),
        prop("Description", "BOM Test Item - Purchased with FG-100"),
        prop("MatlQtyConv", "2.00"),
        prop("UM", "EA"),
        prop("MatlType", "M"),
        prop("Units", "U"),
        prop("RefType", "I"),
        prop("AltGroup", "1"),
        prop("ScrapFact", "0.00"),
    ], "Material BOMTEST-003 on job 99901 oper 10")

    print("\n\n### ROUND 3 DISCOVERY COMPLETE ###")


if __name__ == "__main__":
    main()
