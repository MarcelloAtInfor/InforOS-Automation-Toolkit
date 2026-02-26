#!/usr/bin/env python3
"""
Phase 0 Discovery: ItwhseJob linkage and Work Center catalog.

Discovers how standard jobs link to items via SLItemwhses, and catalogs
all available work centers from SLWcs.

Steps:
  1. Discover SLItemwhses IDO metadata (all properties)
  2. Query FA-10000's warehouse record to see Job field
  3. Discover SLWcs IDO metadata
  4. Query all work centers (SLWcs)
  5. Test linkage: create test item + standard job, check if ItwhseJob auto-populates
  6. If NOT auto-populated: attempt to set Job field on SLItemwhses

Usage:
    python discover_itwhse_wcs.py                    # Discovery only (steps 1-4)
    python discover_itwhse_wcs.py --test-linkage      # Also run steps 5-6
    python discover_itwhse_wcs.py --json              # JSON output

Requires: access_token.txt in same directory (run shared.auth to generate)
"""

import argparse
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
    """Get authenticated headers with site config."""
    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = SITE
    return headers


def get_ido_info(headers, ido_name):
    """Query IDO metadata and return structured property info."""
    url = f"{IDO_URL()}/info/{ido_name}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    data = resp.json()
    return data, None


def ido_load(headers, ido_name, properties, filter_str, record_cap=100):
    """Query IDO records. Properties can be None to return all fields."""
    url = f"{IDO_URL()}/load/{ido_name}"
    params = {"recordCap": record_cap}
    if properties:
        params["properties"] = properties
    if filter_str:
        params["filter"] = filter_str
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    data = resp.json()
    items = data.get("Items") or []
    return items, None


def _prop(name, value):
    """Create a property entry for IDO insert/update payloads."""
    return {"IsNull": False, "Modified": True, "Name": name, "Value": str(value)}


def ido_insert(headers, ido_name, changes_dict):
    """Insert a record into an IDO. changes_dict is {Name: Value}."""
    url = f"{IDO_URL()}/update/{ido_name}"
    props_list = [_prop(k, v) for k, v in changes_dict.items()]
    payload = {
        "IDOName": ido_name,
        "RefreshAfterSave": True,
        "Changes": [{"Action": 1, "Properties": props_list}]
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        return resp.status_code, data
    return resp.status_code, resp.text[:500]


def ido_update(headers, ido_name, changes_dict, filter_str, key_fields=None):
    """Update a record in an IDO (requires loading first to get _ItemId).
    key_fields: dict of key field names->values to include as non-modified props.
    """
    # First load the record to get _ItemId
    url = f"{IDO_URL()}/load/{ido_name}"
    params = {"filter": filter_str, "recordCap": 1}
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return resp.status_code, f"Load failed: {resp.text[:300]}"
    data = resp.json()
    items = data.get("Items") or []
    if not items:
        return 404, "No record found to update"

    item_id = items[0].get("_ItemId", "")
    if not item_id:
        return 500, "No _ItemId in record"

    # Build update payload
    url = f"{IDO_URL()}/update/{ido_name}"
    props_list = [_prop(k, v) for k, v in changes_dict.items()]
    # Add key fields as non-modified (required by some IDOs)
    if key_fields:
        for k, v in key_fields.items():
            props_list.append({"IsNull": False, "Modified": False, "Name": k, "Value": str(v)})
    props_list.append({"IsNull": False, "Modified": False, "Name": "_ItemId", "Value": item_id})
    payload = {
        "IDOName": ido_name,
        "RefreshAfterSave": True,
        "Changes": [{"Action": 2, "Properties": props_list}]
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        return resp.status_code, resp.json()
    return resp.status_code, resp.text[:500]


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def step1_itwhses_metadata(headers):
    """Step 1: Discover SLItemwhses IDO metadata."""
    print_section("STEP 1: SLItemwhses IDO Metadata")

    data, err = get_ido_info(headers, "SLItemwhses")
    if err:
        print(f"  ERROR: {err}")
        return None

    props = data.get("Properties") or []
    if not props:
        success = data.get("Success", True)
        msg = data.get("Message", "")
        print(f"  WARNING: No properties returned. Success={success}, Message='{msg}'")
        return None
    print(f"  Total properties: {len(props)}")

    # Find job-related properties
    job_props = []
    print(f"\n  --- Job-related properties ---")
    for p in props:
        name = p.get("Name", "")
        if "job" in name.lower() or "jtwhse" in name.lower():
            prop_type = p.get("Type", "")
            read_only = p.get("ReadOnly", False)
            req_insert = p.get("RequiredForInsert", False)
            default = p.get("DefaultValue", "")
            print(f"    {name}: Type={prop_type}, ReadOnly={read_only}, ReqInsert={req_insert}, Default='{default}'")
            job_props.append(p)

    # Also show key writable properties
    print(f"\n  --- Key writable properties ---")
    for p in props:
        name = p.get("Name", "")
        read_only = p.get("ReadOnly", False)
        req_insert = p.get("RequiredForInsert", False)
        if not read_only and not name.startswith("_"):
            prop_type = p.get("Type", "")
            default = p.get("DefaultValue", "")
            marker = " [REQ]" if req_insert else ""
            print(f"    {name}: Type={prop_type}, Default='{default}'{marker}")

    return {"properties": props, "job_properties": job_props}


def step2_fa10000_warehouse(headers):
    """Step 2: Query FA-10000's warehouse record to see Job field."""
    print_section("STEP 2: FA-10000 Warehouse Record (SLItemwhses)")

    # Query without properties param (returns all fields)
    items, err = ido_load(
        headers, "SLItemwhses",
        None,  # Return all fields
        "Item = 'FA-10000'"
    )
    if err:
        print(f"  ERROR: {err}")
        return None

    if not items:
        print("  No warehouse record found for FA-10000")
        print("  Trying broader query...")
        items, err = ido_load(headers, "SLItemwhses", None, "Item LIKE 'FA-%'", record_cap=5)
        if err:
            print(f"  ERROR: {err}")
            return None

    items = items or []
    print(f"  Records found: {len(items)}")
    for item in items:
        # Show key fields
        print(f"    Item={item.get('Item')}, Whse={item.get('Whse')}")
        print(f"    Job='{item.get('Job', '')}', ItwhJob='{item.get('ItwhJob', '')}'")
        print(f"    ItwhSuffix='{item.get('ItwhSuffix', '')}'")
        print(f"    PMTCode='{item.get('PMTCode', '')}'")
        print()

    return items


def step3_wcs_metadata(headers):
    """Step 3: Discover SLWcs IDO metadata."""
    print_section("STEP 3: SLWcs IDO Metadata")

    data, err = get_ido_info(headers, "SLWcs")
    if err:
        print(f"  ERROR: {err}")
        return None

    props = data.get("Properties", [])
    print(f"  Total properties: {len(props)}")

    print(f"\n  --- Key properties (writable, non-internal) ---")
    for p in props:
        name = p.get("Name", "")
        read_only = p.get("ReadOnly", False)
        if not read_only and not name.startswith("_"):
            prop_type = p.get("Type", "")
            default = p.get("DefaultValue", "")
            req_insert = p.get("RequiredForInsert", False)
            marker = " [REQ]" if req_insert else ""
            print(f"    {name}: Type={prop_type}, Default='{default}'{marker}")

    return data


def step4_all_work_centers(headers):
    """Step 4: Query all available work centers."""
    print_section("STEP 4: All Work Centers (SLWcs)")

    items, err = ido_load(
        headers, "SLWcs",
        None,  # Return all fields
        None,  # No filter - get all WCs
        record_cap=200
    )
    if err:
        print(f"  ERROR: {err}")
        return None

    items = items or []
    print(f"  Total work centers: {len(items)}")
    print(f"\n  {'Code':<12} {'Description':<40} {'Dept':<10}")
    print(f"  {'-'*12} {'-'*40} {'-'*10}")
    for wc in sorted(items, key=lambda x: x.get("Wc", "")):
        code = wc.get("Wc", "").strip()
        desc = wc.get("Description", "").strip()
        dept = wc.get("Dept", "").strip()
        print(f"  {code:<12} {desc:<40} {dept:<10}")

    return items


def step5_test_linkage(headers):
    """Step 5: Create test item + standard job, check ItwhseJob auto-population."""
    print_section("STEP 5: Test ItwhseJob Linkage")

    test_item = "TEST-BOM-001"
    test_job = "     95001"  # 5 spaces + 95001

    # 5a: Create test item (PMTCode='M' = Manufactured)
    print(f"\n  5a: Creating test item '{test_item}' (PMTCode='M')...")
    status, resp = ido_insert(headers, "SLItems", {
        "Item": test_item,
        "Description": "BOM Linkage Test Item",
        "UM": "EA",
        "PMTCode": "M",
        "ProductCode": "FG-100",
        "CostType": "A",
        "CostMethod": "S",
        "MatlType": "M",
        "Stat": "A"
    })
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"    Success: {success}")
        if msg:
            print(f"    Message: {msg}")
        if not success and "already exists" not in msg.lower():
            print(f"    Item creation failed, aborting linkage test")
            return None
        if "already exists" in msg.lower():
            print(f"    (Continuing with existing item)")
    else:
        print(f"    HTTP {status}: {resp}")
        return None

    # 5b: Check SLItemwhses BEFORE creating job
    print(f"\n  5b: Checking SLItemwhses for '{test_item}' BEFORE job creation...")
    items_before, err = ido_load(
        headers, "SLItemwhses",
        None,  # Return all fields
        f"Item = '{test_item}'"
    )
    if err:
        print(f"    ERROR: {err}")
    else:
        print(f"    Records: {len(items_before or [])}")
        for item in (items_before or []):
            print(f"    Item={item.get('Item')}, Whse={item.get('Whse')}")
            print(f"    Job='{item.get('Job', '')}', ItwhJob='{item.get('ItwhJob', '')}'")

    # 5c: Create standard job for the test item
    print(f"\n  5c: Creating standard job '{test_job.strip()}' for '{test_item}'...")
    status, resp = ido_insert(headers, "SLJobs", {
        "Job": test_job,
        "Suffix": "0",
        "Item": test_item,
        "Type": "S",
        "Stat": "F",
        "QtyReleased": "1.00",
        "Whse": "MAIN"
    })
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"    Success: {success}")
        if msg:
            print(f"    Message: {msg}")
    else:
        print(f"    HTTP {status}: {resp}")

    # 5d: Add a routing operation (required for BOM to display)
    print(f"\n  5d: Adding routing operation (OperNum=10, Wc=FA-400)...")
    status, resp = ido_insert(headers, "SLJobRoutes", {
        "Job": test_job,
        "Suffix": "0",
        "OperNum": "10",
        "Wc": "FA-400"
    })
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"    Success: {success}")
        if msg:
            print(f"    Message: {msg}")
    else:
        print(f"    HTTP {status}: {resp}")

    # 5e: Check SLItemwhses AFTER creating job
    print(f"\n  5e: Checking SLItemwhses for '{test_item}' AFTER job creation...")
    items_after, err = ido_load(
        headers, "SLItemwhses",
        None,  # Return all fields
        f"Item = '{test_item}'"
    )
    if err:
        print(f"    ERROR: {err}")
    else:
        print(f"    Records: {len(items_after or [])}")
        for item in (items_after or []):
            print(f"    Item={item.get('Item')}, Whse={item.get('Whse')}")
            print(f"    Job='{item.get('Job', '')}', ItwhJob='{item.get('ItwhJob', '')}'")

    # 5f: Determine if auto-populated
    auto_populated = False
    if items_after:
        job_ro = items_after[0].get("Job") or ""
        itwh_job = items_after[0].get("ItwhJob") or ""
        job_ro = str(job_ro).strip() if job_ro else ""
        itwh_job = str(itwh_job).strip() if itwh_job else ""
        if job_ro and job_ro != "None":
            auto_populated = True
            print(f"\n  RESULT: Job (read-only) AUTO-POPULATED with '{job_ro}'")
        if itwh_job and itwh_job != "None":
            auto_populated = True
            print(f"\n  RESULT: ItwhJob (writable) AUTO-POPULATED with '{itwh_job}'")
        if not auto_populated:
            print(f"\n  RESULT: Neither Job nor ItwhJob auto-populated after job creation")
            print(f"    Job='{job_ro}', ItwhJob='{itwh_job}'")

    return {
        "test_item": test_item,
        "test_job": test_job.strip(),
        "before": items_before,
        "after": items_after,
        "auto_populated": auto_populated
    }


def step6_manual_linkage(headers, test_item="TEST-BOM-001", test_job="     95001"):
    """Step 6: If Job not auto-populated, try to set it manually on SLItemwhses."""
    print_section("STEP 6: Manual ItwhseJob Linkage Attempt")

    print(f"  Attempting to update SLItemwhses.ItwhJob for '{test_item}' to '{test_job.strip()}'...")

    status, resp = ido_update(
        headers, "SLItemwhses",
        {"ItwhJob": test_job},
        f"Item = '{test_item}' AND Whse = 'MAIN'",
        key_fields={"Item": test_item, "Whse": "MAIN"}
    )
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"    Success: {success}")
        if msg:
            print(f"    Message: {msg}")
        if not success:
            print(f"\n  RESULT: Manual linkage FAILED (API returned Success=False)")
            return False
    elif status == 404:
        print(f"    No SLItemwhses record found for '{test_item}'")
        print(f"\n  RESULT: Manual linkage FAILED (no warehouse record)")
        return False
    else:
        print(f"    HTTP {status}: {resp}")
        print(f"\n  RESULT: Manual linkage FAILED")
        return False

    # Verify
    print(f"\n  Verifying after manual update...")
    items, err = ido_load(
        headers, "SLItemwhses",
        None,  # Return all fields
        f"Item = '{test_item}' AND Whse = 'MAIN'"
    )
    if items:
        for item in items:
            job_ro = item.get("Job", "").strip()
            itwh_job = item.get("ItwhJob", "").strip()
            print(f"    Item={item.get('Item')}, Whse={item.get('Whse')}")
            print(f"    Job='{job_ro}', ItwhJob='{itwh_job}'")
            if itwh_job and itwh_job != "None":
                print(f"\n  RESULT: Manual linkage SUCCEEDED (ItwhJob='{itwh_job}')")
                return True

    print(f"\n  RESULT: Manual linkage had no effect")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Phase 0 Discovery: ItwhseJob linkage and Work Center catalog",
        epilog="Example: python discover_itwhse_wcs.py --test-linkage"
    )
    parser.add_argument(
        "--test-linkage",
        action="store_true",
        help="Run linkage test (steps 5-6): creates TEST-BOM-001 item and job"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output results as JSON"
    )
    args = parser.parse_args()

    headers = get_headers()

    results = {}

    # Steps 1-4: Discovery (always run)
    results["step1_itwhses_meta"] = step1_itwhses_metadata(headers)
    results["step2_fa10000"] = step2_fa10000_warehouse(headers)
    results["step3_wcs_meta"] = step3_wcs_metadata(headers)
    results["step4_work_centers"] = step4_all_work_centers(headers)

    # Steps 5-6: Linkage test (only with --test-linkage)
    if args.test_linkage:
        linkage_result = step5_test_linkage(headers)
        results["step5_linkage_test"] = linkage_result

        if linkage_result and not linkage_result.get("auto_populated"):
            manual_result = step6_manual_linkage(headers)
            results["step6_manual_linkage"] = manual_result
        else:
            print(f"\n  Skipping Step 6: Job was auto-populated (or step 5 failed)")

    # Summary
    print_section("SUMMARY")
    print(f"  Steps 1-4 (Discovery): Complete")
    if args.test_linkage:
        if results.get("step5_linkage_test"):
            lt = results["step5_linkage_test"]
            print(f"  Step 5 (Linkage Test): {'AUTO-POPULATED' if lt.get('auto_populated') else 'NOT auto-populated'}")
            if not lt.get("auto_populated") and "step6_manual_linkage" in results:
                print(f"  Step 6 (Manual Linkage): {'SUCCEEDED' if results['step6_manual_linkage'] else 'FAILED'}")
    else:
        print(f"  Steps 5-6 (Linkage Test): Skipped (use --test-linkage to run)")

    print(f"\n  NEXT: User should validate TEST-BOM-001 in SyteLine UI")
    print(f"         Check: Current Operations form, BOM tree expansion")

    if args.output_json:
        # Serialize what we can
        json_results = {
            "step2_fa10000": results.get("step2_fa10000"),
            "step4_work_centers": results.get("step4_work_centers"),
        }
        if args.test_linkage and results.get("step5_linkage_test"):
            json_results["step5_linkage_test"] = results["step5_linkage_test"]
        print(f"\n--- JSON OUTPUT ---")
        print(json.dumps(json_results, indent=2, default=str))


if __name__ == "__main__":
    main()
