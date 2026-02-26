#!/usr/bin/env python3
"""
Verify BOM Generator Agent results by querying SyteLine IDO APIs directly.

Accepts an item code (the top-level BOM item) and walks the full BOM tree:
  Items -> Standard Jobs -> Routing Operations -> Materials

Usage:
    python verify_bom.py CH-10000
    python verify_bom.py CH-10000 --deep
    python verify_bom.py CH-10000 --json

Exit codes:
    0: All checks passed
    1: One or more checks failed
"""

import argparse
import json
import sys
from pathlib import Path

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site

SITE = get_site()

# Try importing requests
try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def ido_load(headers, ido, filter_str, properties=None, record_cap=100):
    """Query an IDO collection and return Items list.

    properties: comma-separated property names, or None to return all fields.
                SLItemwhses MUST omit properties (returns 0 records otherwise).
                SLJrtResourceGroups MUST specify properties (returns 0 otherwise).
    """
    url = f"{IDO_URL()}/load/{ido}"
    params = {
        "filter": filter_str,
        "recordCap": record_cap
    }
    if properties:
        params["properties"] = properties
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:200]}"
    data = resp.json()
    return data.get("Items", []), None


def check_item(headers, item_code):
    """Check if an item exists in SLItems."""
    items, err = ido_load(
        headers, "SLItems",
        f"Item = '{item_code}'",
        properties="Item,Description,UM,MatlType,PMTCode,Stat"
    )
    if err:
        return None, err
    if not items:
        return None, f"Item '{item_code}' not found"
    return items[0], None


def find_standard_job(headers, item_code):
    """Find the standard job (Type='S') for an item."""
    jobs, err = ido_load(
        headers, "SLJobs",
        f"Type = 'S' AND Item = '{item_code}'",
        properties="Job,Suffix,Item,Type,Stat,QtyReleased,Whse"
    )
    if err:
        return None, err
    if not jobs:
        return None, f"No standard job found for item '{item_code}'"
    return jobs[0], None


def get_routing(headers, job_number):
    """Get routing operations for a job."""
    routes, err = ido_load(
        headers, "SLJobRoutes",
        f"Job = '{job_number}' AND Suffix = 0",
        properties="Job,Suffix,OperNum,Wc,SetupHrsT,RunHrsTLbr,RunHrsTMch"
    )
    if err:
        return None, err
    return routes, None


def check_itwh_job(headers, item_code, expected_job):
    """Check that SLItemwhses.ItwhJob is set and matches the standard job.

    CRITICAL: SLItemwhses MUST be queried with properties=None (IDO quirk —
    specifying properties returns 0 records). Pattern proven in discover_itwhse_wcs.py.
    """
    items, err = ido_load(
        headers, "SLItemwhses",
        f"Item = '{item_code}'"
        # properties=None — intentionally omitted for SLItemwhses quirk
    )
    if err:
        return None, f"ItwhJob query error - {err}"
    if not items:
        return None, f"No SLItemwhses record for item '{item_code}'"

    itwh_job = (items[0].get("ItwhJob") or "").strip()
    expected = expected_job.strip()
    if not itwh_job:
        return None, f"ItwhJob is EMPTY for item '{item_code}' (expected '{expected}')"
    if itwh_job != expected:
        return None, f"ItwhJob mismatch for '{item_code}': got '{itwh_job}', expected '{expected}'"

    return itwh_job, None


def check_resource_groups(headers, job_number, routes):
    """Check that each routing operation has a resource group record in SLJrtResourceGroups.

    CRITICAL: SLJrtResourceGroups MUST specify properties param (INVERSE quirk —
    omitting properties returns 0 records). Batched: one API call per job.
    """
    rg_records, err = ido_load(
        headers, "SLJrtResourceGroups",
        f"Job = '{job_number}' AND Suffix = 0",
        properties="Job,Suffix,OperNum,Rgid,QtyResources,Sequence"
    )
    if err:
        return None, f"ResourceGroup query error - {err}"

    # Index RG records by OperNum for lookup
    rg_by_oper = {}
    for rg in (rg_records or []):
        oper = rg.get("OperNum", "")
        rg_by_oper[oper] = rg

    results = []
    for route in routes:
        oper_num = route.get("OperNum", "?")
        rg = rg_by_oper.get(oper_num)
        if not rg:
            results.append((oper_num, None, f"No resource group for Op{oper_num}"))
        else:
            rgid = rg.get("Rgid", "").strip()
            if not rgid:
                results.append((oper_num, None, f"Rgid is EMPTY for Op{oper_num}"))
            else:
                results.append((oper_num, rgid, None))

    return results, None


def check_setuprgid(headers, job_number, routes):
    """Check that each routing operation has Setuprgid set in SLJrtSchs.

    Batched: one API call per job. Records auto-created when routing ops are inserted.
    """
    schs, err = ido_load(
        headers, "SLJrtSchs",
        f"Job = '{job_number}' AND Suffix = 0",
        properties="Job,Suffix,OperNum,Setuprgid,SchedDrv"
    )
    if err:
        return None, f"JrtSchs query error - {err}"

    # Index by OperNum
    sch_by_oper = {}
    for s in (schs or []):
        oper = s.get("OperNum", "")
        sch_by_oper[oper] = s

    results = []
    for route in routes:
        oper_num = route.get("OperNum", "?")
        sch = sch_by_oper.get(oper_num)
        if not sch:
            results.append((oper_num, None, None, f"No JrtSchs record for Op{oper_num}"))
        else:
            setuprgid = sch.get("Setuprgid", "").strip()
            sched_drv = sch.get("SchedDrv", "").strip()
            if not setuprgid:
                results.append((oper_num, None, sched_drv, f"Setuprgid is EMPTY for Op{oper_num}"))
            else:
                results.append((oper_num, setuprgid, sched_drv, None))

    return results, None


def get_materials(headers, job_number):
    """Get BOM materials for a job."""
    matls, err = ido_load(
        headers, "SLJobmatls",
        f"Job = '{job_number}' AND Suffix = 0",
        properties="Job,Suffix,OperNum,Sequence,Item,Description,MatlQtyConv,UM,MatlType,RefType,AltGroup"
    )
    if err:
        return None, err
    return matls, None


def verify_bom_tree(headers, item_code, depth=0, deep=False, results=None):
    """
    Recursively verify a BOM tree starting from an item code.

    Returns a results dict with pass/fail counts and details.
    """
    if results is None:
        results = {"passed": 0, "failed": 0, "warnings": 0, "details": [], "tree": {}}

    indent = "  " * depth
    node = {"item": item_code, "children": []}

    # 1. Check item exists
    item, err = check_item(headers, item_code)
    if err:
        results["failed"] += 1
        results["details"].append(f"{indent}FAIL: {err}")
        node["status"] = "MISSING"
        return node, results

    desc = item.get("Description", "")
    results["passed"] += 1
    results["details"].append(f"{indent}OK: Item '{item_code}' - {desc}")
    node["description"] = desc
    node["status"] = "OK"

    # 2. Check for standard job
    job, err = find_standard_job(headers, item_code)
    if err:
        # Not an error for leaf items - they don't need jobs
        if depth > 0:
            results["details"].append(f"{indent}  INFO: No standard job (leaf/purchased item)")
            node["job"] = None
        else:
            results["failed"] += 1
            results["details"].append(f"{indent}  FAIL: {err}")
            node["job"] = "MISSING"
        return node, results

    job_number = job.get("Job", "")
    job_stat = job.get("Stat", "")
    results["passed"] += 1
    results["details"].append(f"{indent}  OK: Standard Job '{job_number.strip()}' (Stat={job_stat})")
    node["job"] = job_number.strip()

    # 3. Check ItwhJob linkage (makes BOM visible in SyteLine UI)
    itwh_job, err = check_itwh_job(headers, item_code, job_number)
    if err:
        results["failed"] += 1
        results["details"].append(f"{indent}  FAIL: {err}")
        node["itwh_job"] = "MISSING"
    else:
        results["passed"] += 1
        results["details"].append(f"{indent}  OK: ItwhJob = '{itwh_job}'")
        node["itwh_job"] = itwh_job

    # 4. Check routing operations
    routes, err = get_routing(headers, job_number)
    if err:
        results["failed"] += 1
        results["details"].append(f"{indent}  FAIL: Routing query error - {err}")
    elif not routes:
        results["failed"] += 1
        results["details"].append(f"{indent}  FAIL: No routing operations found")
    else:
        results["passed"] += 1
        route_summary = ", ".join(
            f"Op{r.get('OperNum', '?')}({r.get('Wc', '?')})" for r in routes
        )
        results["details"].append(f"{indent}  OK: {len(routes)} routing ops: {route_summary}")
        node["routing"] = [
            {"oper": r.get("OperNum"), "wc": r.get("Wc")} for r in routes
        ]

        # 5. Check resource groups per operation
        rg_results, rg_err = check_resource_groups(headers, job_number, routes)
        if rg_err:
            results["failed"] += 1
            results["details"].append(f"{indent}  FAIL: {rg_err}")
        else:
            for oper_num, rgid, rg_error in rg_results:
                if rg_error:
                    results["failed"] += 1
                    results["details"].append(f"{indent}    FAIL: {rg_error}")
                else:
                    results["passed"] += 1
                    results["details"].append(f"{indent}    OK: Op{oper_num} ResourceGroup = '{rgid}'")

        # 6. Check Setuprgid per operation
        sch_results, sch_err = check_setuprgid(headers, job_number, routes)
        if sch_err:
            results["failed"] += 1
            results["details"].append(f"{indent}  FAIL: {sch_err}")
        else:
            for oper_num, setuprgid, sched_drv, sch_error in sch_results:
                if sch_error:
                    results["failed"] += 1
                    results["details"].append(f"{indent}    FAIL: {sch_error}")
                else:
                    results["passed"] += 1
                    results["details"].append(
                        f"{indent}    OK: Op{oper_num} Setuprgid = '{setuprgid}' (SchedDrv={sched_drv})"
                    )

    # 7. Check materials (BOM children)
    matls, err = get_materials(headers, job_number)
    if err:
        results["failed"] += 1
        results["details"].append(f"{indent}  FAIL: Materials query error - {err}")
    elif not matls:
        results["warnings"] += 1
        results["details"].append(f"{indent}  WARN: No materials found (empty BOM?)")
    else:
        results["passed"] += 1
        results["details"].append(f"{indent}  OK: {len(matls)} materials:")
        node["materials"] = []

        for m in matls:
            child_item = m.get("Item", "?")
            child_desc = m.get("Description", "")
            qty = m.get("MatlQtyConv", "?")
            ref_type = m.get("RefType", "?")
            um = m.get("UM", "?")

            ref_label = {"J": "Sub-assy", "I": "Inventory", "P": "Phantom"}.get(ref_type, ref_type)
            results["details"].append(
                f"{indent}    - {child_item}: {child_desc} (Qty={qty} {um}, {ref_label})"
            )

            child_node = {"item": child_item, "qty": qty, "ref_type": ref_type}
            node["materials"].append(child_node)

            # Recurse into sub-assemblies if deep mode
            if deep and ref_type == "J":
                results["details"].append(f"{indent}    Verifying sub-assembly '{child_item}'...")
                sub_node, results = verify_bom_tree(
                    headers, child_item, depth + 2, deep, results
                )
                child_node["sub_tree"] = sub_node

    return node, results


def main():
    parser = argparse.ArgumentParser(
        description="Verify BOM Generator results by querying SyteLine IDO APIs directly",
        epilog="Example: python verify_bom.py CH-10000 --deep"
    )

    parser.add_argument(
        "item",
        help="Top-level item code to verify (e.g., CH-10000)"
    )

    parser.add_argument(
        "--deep",
        action="store_true",
        help="Recursively verify sub-assembly BOMs"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output results as JSON"
    )

    parser.add_argument(
        "--site",
        default=SITE,
        help=f"SyteLine site config (default: {SITE})"
    )

    args = parser.parse_args()

    # Auth
    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = args.site

    print(f"Verifying BOM for: {args.item}")
    print(f"Site: {args.site}")
    print(f"Mode: {'Deep (recursive)' if args.deep else 'Shallow (top-level only)'}")
    print("=" * 60)

    tree, results = verify_bom_tree(headers, args.item, deep=args.deep)

    if args.output_json:
        output = {
            "item": args.item,
            "site": args.site,
            "deep": args.deep,
            "passed": results["passed"],
            "failed": results["failed"],
            "warnings": results["warnings"],
            "tree": tree
        }
        print(json.dumps(output, indent=2))
    else:
        # Print detail lines
        for line in results["details"]:
            print(line)

        # Summary
        print("\n" + "=" * 60)
        total = results["passed"] + results["failed"]
        print(f"Results: {results['passed']}/{total} checks passed", end="")
        if results["warnings"]:
            print(f", {results['warnings']} warnings", end="")
        print()

        if results["failed"] > 0:
            print("STATUS: FAIL")
        else:
            print("STATUS: PASS")

    sys.exit(1 if results["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
