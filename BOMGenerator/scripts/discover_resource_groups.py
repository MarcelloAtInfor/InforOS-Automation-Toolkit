#!/usr/bin/env python3
"""
Resource Group Discovery: Investigate SLJrtResourceGroups on routing operations.

Determines whether resource groups need explicit API inserts after creating
routing operations, or if there's another mechanism.

Steps:
  1. Discover SLJrtResourceGroups IDO metadata (all properties)
  2. Query FA-10000's resource groups (Job 342 - known good BOM)
  3. Query TEST-BOM-001's resource groups (Job 95001 - API-created, no resource groups expected)
  4. (--test-insert) Attempt to insert a resource group for TEST-BOM-001 OperNum=10

Usage:
    python discover_resource_groups.py                  # Discovery only (steps 1-3)
    python discover_resource_groups.py --test-insert     # Also run step 4
    python discover_resource_groups.py --json            # JSON output

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
        return None, f"HTTP {resp.status_code}: {resp.text[:500]}"
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
        return None, f"HTTP {resp.status_code}: {resp.text[:500]}"
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


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def step1_resource_group_metadata(headers):
    """Step 1: Discover SLJrtResourceGroups IDO metadata."""
    print_section("STEP 1: SLJrtResourceGroups IDO Metadata")

    data, err = get_ido_info(headers, "SLJrtResourceGroups")
    if err:
        print(f"  ERROR: {err}")
        # Try alternate names
        for alt_name in ["SLJobRouteResourceGroups", "SLJobrtResourceGroups", "SLJrtrgs"]:
            print(f"  Trying alternate IDO name: {alt_name}...")
            data, err2 = get_ido_info(headers, alt_name)
            if not err2:
                print(f"  FOUND as '{alt_name}'!")
                break
        if err and not data:
            print(f"  No alternate names worked. Last error: {err}")
            return None

    props = data.get("Properties") or []
    if not props:
        success = data.get("Success", True)
        msg = data.get("Message", "")
        print(f"  WARNING: No properties returned. Success={success}, Message='{msg}'")
        print(f"  Full response keys: {list(data.keys())}")
        print(f"  Full response (first 1000 chars): {json.dumps(data, indent=2)[:1000]}")
        return data

    print(f"  Total properties: {len(props)}")

    # Categorize properties
    key_props = []
    writable_props = []
    readonly_props = []

    for p in props:
        name = p.get("Name", "")
        if name.startswith("_"):
            continue
        read_only = p.get("ReadOnly", False)
        req_insert = p.get("RequiredForInsert", False)
        prop_type = p.get("Type", "")
        default = p.get("DefaultValue", "")

        if req_insert:
            key_props.append(p)
        elif not read_only:
            writable_props.append(p)
        else:
            readonly_props.append(p)

    print(f"\n  --- Required for Insert ({len(key_props)}) ---")
    for p in key_props:
        name = p.get("Name", "")
        prop_type = p.get("Type", "")
        default = p.get("DefaultValue", "")
        print(f"    {name}: Type={prop_type}, Default='{default}' [REQUIRED]")

    print(f"\n  --- Writable ({len(writable_props)}) ---")
    for p in writable_props:
        name = p.get("Name", "")
        prop_type = p.get("Type", "")
        default = p.get("DefaultValue", "")
        print(f"    {name}: Type={prop_type}, Default='{default}'")

    print(f"\n  --- Read-Only ({len(readonly_props)}) ---")
    for p in readonly_props:
        name = p.get("Name", "")
        prop_type = p.get("Type", "")
        print(f"    {name}: Type={prop_type}")

    return {
        "total_properties": len(props),
        "required": [p.get("Name") for p in key_props],
        "writable": [p.get("Name") for p in writable_props],
        "readonly": [p.get("Name") for p in readonly_props],
        "all_properties": props
    }


def step2_fa10000_resource_groups(headers):
    """Step 2: Query FA-10000's resource groups (known good BOM, Job 342)."""
    print_section("STEP 2: FA-10000 Resource Groups (Job 342 - Known Good)")

    fa_job = "       342"  # 7 spaces + 342 (10 chars)

    # First try loading SLJrtResourceGroups directly
    print(f"  2a: Querying SLJrtResourceGroups for Job='342'...")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        f"Job = '{fa_job}'"
    )
    if err:
        print(f"  ERROR: {err}")
        # Try without padded job number
        print(f"  Trying filter with trimmed job number...")
        items, err2 = ido_load(
            headers, "SLJrtResourceGroups",
            None,
            "Job LIKE '%342'"
        )
        if err2:
            print(f"  ERROR: {err2}")
        else:
            print(f"  Records found (LIKE filter): {len(items or [])}")
    else:
        print(f"  Records found: {len(items or [])}")

    if items:
        print(f"\n  Resource group records for FA-10000 (Job 342):")
        for i, item in enumerate(items):
            print(f"\n  --- Record {i+1} ---")
            # Print all non-null, non-empty, non-internal fields
            for key, val in sorted(item.items()):
                if key.startswith("_"):
                    continue
                if val is not None and str(val).strip() and str(val).strip() != "None":
                    print(f"    {key} = '{val}'")
    else:
        print(f"  No resource group records found for Job 342")

    # Also query the routing operations for context
    print(f"\n  2b: Querying SLJobRoutes for Job='342' (for context)...")
    routes, err = ido_load(
        headers, "SLJobRoutes",
        None,
        f"Job = '{fa_job}'"
    )
    if err:
        print(f"  ERROR: {err}")
        routes, err2 = ido_load(
            headers, "SLJobRoutes",
            None,
            "Job LIKE '%342'"
        )
        if err2:
            print(f"  ERROR: {err2}")
        else:
            routes = routes or []
    else:
        routes = routes or []

    if routes:
        print(f"  Routing operations found: {len(routes)}")
        for r in routes:
            oper = r.get("OperNum", "")
            wc = r.get("Wc", "")
            desc = r.get("WcDescription", "") or r.get("Description", "")
            print(f"    OperNum={oper}, Wc='{wc}', Desc='{desc}'")

    return {"resource_groups": items, "routes": routes}


def step3_test_bom_resource_groups(headers):
    """Step 3: Query TEST-BOM-001's resource groups (Job 95001 - API-created)."""
    print_section("STEP 3: TEST-BOM-001 Resource Groups (Job 95001 - API-Created)")

    test_job = "     95001"  # 5 spaces + 95001

    print(f"  3a: Querying SLJrtResourceGroups for Job='95001'...")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        f"Job = '{test_job}'"
    )
    if err:
        print(f"  ERROR: {err}")
        items, err2 = ido_load(
            headers, "SLJrtResourceGroups",
            None,
            "Job LIKE '%95001'"
        )
        if err2:
            print(f"  ERROR: {err2}")
        else:
            print(f"  Records found (LIKE filter): {len(items or [])}")
    else:
        print(f"  Records found: {len(items or [])}")

    if items:
        print(f"\n  Resource group records for TEST-BOM-001 (Job 95001):")
        for i, item in enumerate(items):
            print(f"\n  --- Record {i+1} ---")
            for key, val in sorted(item.items()):
                if key.startswith("_"):
                    continue
                if val is not None and str(val).strip() and str(val).strip() != "None":
                    print(f"    {key} = '{val}'")
    else:
        print(f"  No resource group records found (confirms API routing insert doesn't auto-create them)")

    return items


def step4_test_insert(headers):
    """Step 4: Attempt to insert a resource group for TEST-BOM-001 OperNum=10."""
    print_section("STEP 4: Test Resource Group Insert (Job 95001, OperNum=10)")

    test_job = "     95001"

    # We need to know the required fields from step 1.
    # Based on typical IDO patterns, try with minimal fields first.
    print(f"  4a: Attempting minimal insert (Job, Suffix, OperNum)...")
    status, resp = ido_insert(headers, "SLJrtResourceGroups", {
        "Job": test_job,
        "Suffix": "0",
        "OperNum": "10"
    })
    print(f"    HTTP {status}")
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"    Success: {success}")
        if msg:
            print(f"    Message: {msg}")
        if success:
            # Show the created record
            changes = resp.get("Changes", [])
            if changes:
                print(f"    Created record properties:")
                for prop in changes[0].get("Properties", []):
                    name = prop.get("Name", "")
                    value = prop.get("Value", "")
                    if name.startswith("_"):
                        continue
                    if value and str(value).strip() and str(value).strip() != "None":
                        print(f"      {name} = '{value}'")
            return {"success": True, "response": resp}
    else:
        print(f"    Response: {resp}")

    # If minimal insert failed, try with more fields
    print(f"\n  4b: Attempting insert with ResourceGroup and Wc...")
    status, resp = ido_insert(headers, "SLJrtResourceGroups", {
        "Job": test_job,
        "Suffix": "0",
        "OperNum": "10",
        "ResourceGroup": "FA-400",
        "Wc": "FA-400"
    })
    print(f"    HTTP {status}")
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"    Success: {success}")
        if msg:
            print(f"    Message: {msg}")
        if success:
            changes = resp.get("Changes", [])
            if changes:
                print(f"    Created record properties:")
                for prop in changes[0].get("Properties", []):
                    name = prop.get("Name", "")
                    value = prop.get("Value", "")
                    if name.startswith("_"):
                        continue
                    if value and str(value).strip() and str(value).strip() != "None":
                        print(f"      {name} = '{value}'")
            return {"success": True, "response": resp}
    else:
        print(f"    Response: {resp}")

    # Verify if anything was created
    print(f"\n  4c: Verifying resource groups after insert attempts...")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        f"Job = '{test_job}'"
    )
    if err:
        print(f"    ERROR: {err}")
    else:
        print(f"    Records found: {len(items or [])}")
        if items:
            for i, item in enumerate(items):
                print(f"\n    --- Record {i+1} ---")
                for key, val in sorted(item.items()):
                    if key.startswith("_"):
                        continue
                    if val is not None and str(val).strip() and str(val).strip() != "None":
                        print(f"      {key} = '{val}'")

    return {"success": False, "items_after": items}


def main():
    parser = argparse.ArgumentParser(
        description="Resource Group Discovery: Investigate SLJrtResourceGroups",
        epilog="Example: python discover_resource_groups.py --test-insert"
    )
    parser.add_argument(
        "--test-insert",
        action="store_true",
        help="Attempt to insert a resource group for TEST-BOM-001 (step 4)"
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

    # Steps 1-3: Discovery (always run)
    results["step1_metadata"] = step1_resource_group_metadata(headers)
    results["step2_fa10000"] = step2_fa10000_resource_groups(headers)
    results["step3_test_bom"] = step3_test_bom_resource_groups(headers)

    # Step 4: Test insert (only with --test-insert)
    if args.test_insert:
        results["step4_insert"] = step4_test_insert(headers)

    # Summary
    print_section("SUMMARY")
    meta = results.get("step1_metadata")
    if meta and isinstance(meta, dict) and "total_properties" in meta:
        print(f"  Step 1: IDO has {meta['total_properties']} properties")
        print(f"    Required: {meta.get('required', [])}")
        print(f"    Writable: {meta.get('writable', [])}")
    else:
        print(f"  Step 1: IDO metadata query failed or unexpected format")

    fa_rg = results.get("step2_fa10000", {})
    if isinstance(fa_rg, dict):
        rg_items = fa_rg.get("resource_groups") or []
        routes = fa_rg.get("routes") or []
        print(f"  Step 2: FA-10000 has {len(rg_items)} resource group records, {len(routes)} routing operations")
    else:
        print(f"  Step 2: FA-10000 query completed")

    test_rg = results.get("step3_test_bom")
    print(f"  Step 3: TEST-BOM-001 has {len(test_rg or [])} resource group records")

    if args.test_insert:
        insert_result = results.get("step4_insert", {})
        if isinstance(insert_result, dict):
            print(f"  Step 4: Insert {'SUCCEEDED' if insert_result.get('success') else 'FAILED'}")
    else:
        print(f"  Step 4: Skipped (use --test-insert to attempt)")

    print(f"\n  KEY QUESTION: Do we need to explicitly insert resource groups after routing creation?")
    if isinstance(fa_rg, dict):
        rg_items = fa_rg.get("resource_groups") or []
        if rg_items:
            print(f"    FA-10000 HAS resource group records -> YES, they need to exist")
        else:
            print(f"    FA-10000 has NO resource group records -> MAYBE not needed")

    if args.output_json:
        print(f"\n--- JSON OUTPUT ---")
        # Serialize what we can
        json_safe = {}
        for k, v in results.items():
            try:
                json.dumps(v)
                json_safe[k] = v
            except (TypeError, ValueError):
                json_safe[k] = str(v)
        print(json.dumps(json_safe, indent=2, default=str))


if __name__ == "__main__":
    main()
