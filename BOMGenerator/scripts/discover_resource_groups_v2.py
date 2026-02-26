#!/usr/bin/env python3
"""
Resource Group Discovery V2: Re-investigate SLJrtResourceGroups with systematic approach.

Previous investigation (v1) concluded "0 records system-wide" but user confirms FA-10000
(Job 342) DOES have resource group data visible in the UI's Resources grid. The v1 script:
- Only filtered by Job (may need Job + Suffix + OperNum)
- Used wrong property names in insert attempts (ResourceGroup instead of Rgid)
- May have hit an IDO quirk similar to SLItemwhses (properties param issue)

Two separate things must be populated per operation:
1. Setuprgid via SLJrtSchs (Resource Setup section) - already working
2. SLJrtResourceGroups sub-collection (Resources grid) - THIS IS THE MISSING PIECE

Steps:
  0.1 - IDO Metadata via System IDOs (IdoCollections, IdoTables, IdoProperties, /info)
  0.2 - Systematic query approaches for FA-10000 (Job 342)
  0.3 - Capture FA-10000 reference record (all property values)
  0.4 - Confirm TEST-BOM-001 (Job 95001) has no records
  0.5 - Test INSERT for TEST-BOM-001 Op 10 (--test-insert)
  0.6 - Test relationship: SLJrtResourceGroups insert vs SLJrtSchs.Setuprgid (--test-insert)
  0.7 - Summary and next steps

Usage:
    python discover_resource_groups_v2.py                  # Discovery only (steps 0.1-0.4)
    python discover_resource_groups_v2.py --test-insert    # Also run steps 0.5-0.6
    python discover_resource_groups_v2.py --json           # JSON output

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


# ────────────────────────────────────────────────────────────────
# Helper functions (reused from discover_itwhse_wcs.py patterns)
# ────────────────────────────────────────────────────────────────

def get_headers():
    """Get authenticated headers with site config."""
    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = SITE
    return headers


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


def _prop(name, value, modified=True):
    """Create a property entry for IDO insert/update payloads."""
    return {"IsNull": False, "Modified": modified, "Name": name, "Value": str(value)}


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
    """Update a record in an IDO (requires loading first to get _ItemId)."""
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

    url = f"{IDO_URL()}/update/{ido_name}"
    props_list = [_prop(k, v) for k, v in changes_dict.items()]
    if key_fields:
        for k, v in key_fields.items():
            props_list.append(_prop(k, v, modified=False))
    props_list.append(_prop("_ItemId", item_id, modified=False))
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


def print_record(item, indent=4):
    """Print all non-null, non-empty, non-internal fields of an IDO record."""
    prefix = " " * indent
    for key, val in sorted(item.items()):
        if key.startswith("_"):
            continue
        if val is not None and str(val).strip() and str(val).strip() != "None":
            print(f"{prefix}{key} = '{val}'")


# ────────────────────────────────────────────────────────────────
# Step 0.1: IDO Metadata via System IDOs
# ────────────────────────────────────────────────────────────────

def step01_ido_metadata(headers):
    """Query system IDOs for SLJrtResourceGroups metadata."""
    print_section("STEP 0.1: SLJrtResourceGroups IDO Metadata (System IDOs)")
    results = {}

    # 0.1a: IdoCollections - server assembly, extension class
    print(f"\n  --- 0.1a: IdoCollections for SLJrtResourceGroups ---")
    items, err = ido_load(
        headers, "IdoCollections",
        "CollectionName,ServerAssembly,ExtensionClassId,UserDefinedCollection",
        "CollectionName = 'SLJrtResourceGroups'"
    )
    if err:
        print(f"  ERROR: {err}")
    elif items:
        print(f"  Found {len(items)} record(s)")
        for item in items:
            print_record(item)
        results["IdoCollections"] = items
    else:
        print(f"  No IdoCollections record found for SLJrtResourceGroups")
        # Try partial match
        print(f"  Trying LIKE query...")
        items, err = ido_load(
            headers, "IdoCollections",
            "CollectionName,ServerAssembly,ExtensionClassId",
            "CollectionName LIKE 'SLJrt%'",
            record_cap=20
        )
        if items:
            print(f"  Found {len(items)} SLJrt* collections:")
            for item in items:
                print(f"    {item.get('CollectionName')}")
            results["IdoCollections_partial"] = items
        else:
            print(f"  No SLJrt* collections found")

    # 0.1b: IdoTables - primary table, joined tables
    print(f"\n  --- 0.1b: IdoTables for SLJrtResourceGroups ---")
    items, err = ido_load(
        headers, "IdoTables",
        "CollectionName,TableName,TableAlias,JoinType,TableType",
        "CollectionName = 'SLJrtResourceGroups'"
    )
    if err:
        print(f"  ERROR: {err}")
    elif items:
        print(f"  Found {len(items)} table(s)")
        for item in items:
            table_type = item.get("TableType", "")
            marker = " <-- PRIMARY (writable)" if str(table_type) == "3" else ""
            print(f"    TableName={item.get('TableName')}, Alias={item.get('TableAlias')}, "
                  f"JoinType={item.get('JoinType')}, TableType={table_type}{marker}")
        results["IdoTables"] = items
    else:
        print(f"  No IdoTables records found")

    # 0.1c: IdoProperties - ALL properties with column/table mapping
    print(f"\n  --- 0.1c: IdoProperties for SLJrtResourceGroups ---")
    items, err = ido_load(
        headers, "IdoProperties",
        "CollectionName,PropertyName,ColumnName,ColumnTableAlias,ColumnTableName,DataType,ReadOnly,RequiredForInsert",
        "CollectionName = 'SLJrtResourceGroups'",
        record_cap=200
    )
    if err:
        print(f"  ERROR: {err}")
    elif items:
        print(f"  Found {len(items)} properties")
        print(f"\n  Writable properties (ReadOnly=False):")
        writable = [p for p in items if str(p.get("ReadOnly", "")).lower() in ("false", "0", "")]
        for p in sorted(writable, key=lambda x: x.get("PropertyName", "")):
            name = p.get("PropertyName", "")
            col = p.get("ColumnName", "")
            table = p.get("ColumnTableName", "") or p.get("ColumnTableAlias", "")
            dtype = p.get("DataType", "")
            req = p.get("RequiredForInsert", "")
            req_marker = " [REQUIRED]" if str(req).lower() in ("true", "1") else ""
            print(f"    {name}: Column={col}, Table={table}, Type={dtype}{req_marker}")

        print(f"\n  Read-only properties:")
        readonly = [p for p in items if str(p.get("ReadOnly", "")).lower() in ("true", "1")]
        for p in sorted(readonly, key=lambda x: x.get("PropertyName", "")):
            name = p.get("PropertyName", "")
            col = p.get("ColumnName", "")
            table = p.get("ColumnTableName", "") or p.get("ColumnTableAlias", "")
            print(f"    {name}: Column={col}, Table={table}")

        results["IdoProperties"] = items
    else:
        print(f"  No IdoProperties records found")

    # 0.1d: /info endpoint - RequiredForInsert, DefaultValues
    print(f"\n  --- 0.1d: /info/SLJrtResourceGroups ---")
    url = f"{IDO_URL()}/info/SLJrtResourceGroups"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"  ERROR: HTTP {resp.status_code}: {resp.text[:500]}")
    else:
        data = resp.json()
        props = data.get("Properties") or []
        print(f"  Total properties from /info: {len(props)}")

        required_props = [p for p in props if p.get("RequiredForInsert")]
        writable_props = [p for p in props if not p.get("ReadOnly") and not p.get("Name", "").startswith("_")]
        readonly_props = [p for p in props if p.get("ReadOnly") and not p.get("Name", "").startswith("_")]

        print(f"\n  Required for Insert ({len(required_props)}):")
        for p in required_props:
            print(f"    {p.get('Name')}: Type={p.get('Type','')}, Default='{p.get('DefaultValue','')}'")

        print(f"\n  Writable (non-internal, {len(writable_props)}):")
        for p in writable_props:
            name = p.get("Name", "")
            if name.startswith("_"):
                continue
            default = p.get("DefaultValue", "")
            ptype = p.get("Type", "")
            print(f"    {name}: Type={ptype}, Default='{default}'")

        print(f"\n  Read-Only (non-internal, {len(readonly_props)}):")
        for p in readonly_props:
            name = p.get("Name", "")
            if name.startswith("_"):
                continue
            print(f"    {name}: Type={p.get('Type','')}")

        results["info_endpoint"] = {
            "total": len(props),
            "required": [p.get("Name") for p in required_props],
            "writable": [p.get("Name") for p in writable_props if not p.get("Name","").startswith("_")],
            "readonly": [p.get("Name") for p in readonly_props if not p.get("Name","").startswith("_")]
        }

    return results


# ────────────────────────────────────────────────────────────────
# Step 0.2: Systematic Query Approaches (FA-10000, Job 342)
# ────────────────────────────────────────────────────────────────

def step02_systematic_queries(headers):
    """Try multiple query strategies until we find records."""
    print_section("STEP 0.2: Systematic Query Approaches (FA-10000, Job 342)")
    results = {}

    fa_job_padded = "       342"  # 7 spaces + 342 (10 chars)

    # Approach 1: Filter with ALL linking keys
    print(f"\n  --- Approach 1: Full key filter (Job + Suffix + OperNum) ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,  # All properties
        f"Job = '{fa_job_padded}' AND Suffix = 0 AND OperNum = 10"
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        print(f"  Records found: {len(items or [])}")
        results["approach1_full_key"] = items

    # Approach 2: No filter at all (any records in system?)
    print(f"\n  --- Approach 2: No filter (recordCap=10, any records?) ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,  # All properties
        None,  # No filter
        record_cap=10
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        count = len(items or [])
        print(f"  Records found: {count}")
        if items:
            print(f"  First record:")
            print_record(items[0])
        results["approach2_no_filter"] = items

    # Approach 3: Omit properties param (SLItemwhses-like quirk test)
    # Note: ido_load with properties=None already does this, but let's be explicit
    print(f"\n  --- Approach 3: Job filter only, no properties param ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,  # Explicitly no properties param
        f"Job = '{fa_job_padded}'"
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        print(f"  Records found: {len(items or [])}")
        results["approach3_job_only"] = items

    # Approach 4: LIKE filter for different Job format
    print(f"\n  --- Approach 4: Job LIKE '%342%' ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        "Job LIKE '%342%'"
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        print(f"  Records found: {len(items or [])}")
        results["approach4_like"] = items

    # Approach 5: Try with explicit properties list (inverse of SLItemwhses quirk)
    print(f"\n  --- Approach 5: With explicit properties param ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        "Job,Suffix,OperNum,Rgid,QtyResources,Resactn,Sequence",
        f"Job = '{fa_job_padded}'"
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        print(f"  Records found: {len(items or [])}")
        results["approach5_explicit_props"] = items

    # Approach 6: Try different job numbers (broad search)
    print(f"\n  --- Approach 6: Broad search (all records, cap=50) ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        None,  # No filter
        record_cap=50
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        count = len(items or [])
        print(f"  Records found: {count}")
        if items:
            # Summarize unique jobs
            jobs = set()
            for item in items:
                j = item.get("Job", "").strip()
                if j and j != "None":
                    jobs.add(j)
            if jobs:
                print(f"  Unique jobs with resource groups: {sorted(jobs)}")
        results["approach6_broad"] = items

    # Determine which approach found data
    found_data = False
    for key, items in results.items():
        if items and len(items) > 0:
            found_data = True
            print(f"\n  FOUND DATA via {key}!")
            break

    if not found_data:
        print(f"\n  NO DATA found via any approach.")
        print(f"  Possible explanations:")
        print(f"    1. SLJrtResourceGroups may NOT be the IDO the UI's Resources grid uses")
        print(f"    2. The Resources grid may use a different sub-collection IDO")
        print(f"    3. Resource group data may live in a different table entirely")
        print(f"  NEXT: Check IdoTables for the primary table name, then search for other IDOs")

    return results


# ────────────────────────────────────────────────────────────────
# Step 0.3: Capture FA-10000 Reference Record
# ────────────────────────────────────────────────────────────────

def step03_capture_reference(headers, query_results):
    """If step 0.2 found data, capture all property values for FA-10000 Op 10."""
    print_section("STEP 0.3: Capture FA-10000 Reference Record")

    # Find any records from step 0.2
    found_items = None
    for key, items in query_results.items():
        if items and len(items) > 0:
            found_items = items
            break

    if found_items:
        print(f"  Found {len(found_items)} record(s). Full details:")
        for i, item in enumerate(found_items):
            print(f"\n  --- Record {i+1} ---")
            print_record(item)
        return found_items
    else:
        print(f"  No records found in step 0.2. Skipping capture.")
        print(f"  Will investigate alternative IDOs/tables in summary.")

        # Additional investigation: query the IDO table to find what table
        # the SLJrtResourceGroups IDO maps to, then look for OTHER IDOs
        # that also map to that table
        print(f"\n  --- Additional: Find alternate IDOs for the same table ---")

        # Get the primary table name from step 0.1 (if available)
        items, err = ido_load(
            headers, "IdoTables",
            "CollectionName,TableName,TableAlias,TableType",
            "CollectionName = 'SLJrtResourceGroups' AND TableType = 3"
        )
        if items:
            primary_table = items[0].get("TableName", "")
            print(f"  Primary table for SLJrtResourceGroups: '{primary_table}'")

            if primary_table:
                # Find ALL IDOs that have this table as primary
                items2, err2 = ido_load(
                    headers, "IdoTables",
                    "CollectionName,TableName,TableAlias,TableType",
                    f"TableName = '{primary_table}' AND TableType = 3",
                    record_cap=20
                )
                if items2:
                    print(f"  IDOs with '{primary_table}' as primary table:")
                    for it in items2:
                        print(f"    {it.get('CollectionName')}")

                # Also find IDOs that have this table as joined (read)
                items3, err3 = ido_load(
                    headers, "IdoTables",
                    "CollectionName,TableName,TableAlias,JoinType,TableType",
                    f"TableName = '{primary_table}'",
                    record_cap=20
                )
                if items3:
                    print(f"\n  All IDOs referencing '{primary_table}':")
                    for it in items3:
                        ttype = it.get("TableType", "")
                        marker = " <-- PRIMARY" if str(ttype) == "3" else " (joined)"
                        print(f"    {it.get('CollectionName')}: TableType={ttype}{marker}")
        else:
            print(f"  Could not find primary table for SLJrtResourceGroups")

            # Try querying the table directly via SQL-like approach
            print(f"\n  --- Searching for 'jrt_resource' in IdoTables ---")
            items4, err4 = ido_load(
                headers, "IdoTables",
                "CollectionName,TableName,TableAlias,TableType",
                "TableName LIKE '%resource%'",
                record_cap=20
            )
            if items4:
                print(f"  Tables matching 'resource':")
                for it in items4:
                    ttype = it.get("TableType", "")
                    marker = " <-- PRIMARY" if str(ttype) == "3" else ""
                    print(f"    {it.get('CollectionName')}.{it.get('TableName')} (TableType={ttype}){marker}")
            else:
                print(f"  No tables matching 'resource' found")

            # Also try 'rg' pattern
            print(f"\n  --- Searching for 'jrt_rg' or 'jobrtrg' in IdoTables ---")
            for pattern in ["jrt_rg%", "jobrtrg%", "%jrt%rg%", "%resource_group%"]:
                items5, err5 = ido_load(
                    headers, "IdoTables",
                    "CollectionName,TableName,TableAlias,TableType",
                    f"TableName LIKE '{pattern}'",
                    record_cap=10
                )
                if items5:
                    print(f"  Tables matching '{pattern}':")
                    for it in items5:
                        ttype = it.get("TableType", "")
                        marker = " <-- PRIMARY" if str(ttype) == "3" else ""
                        print(f"    {it.get('CollectionName')}.{it.get('TableName')} (TableType={ttype}){marker}")

        return None


# ────────────────────────────────────────────────────────────────
# Step 0.4: Confirm TEST-BOM-001 (Job 95001) Has No Records
# ────────────────────────────────────────────────────────────────

def step04_test_bom_check(headers):
    """Verify API-created routing doesn't auto-populate resource groups."""
    print_section("STEP 0.4: TEST-BOM-001 Resource Groups (Job 95001)")

    test_job = "     95001"

    # Try same approaches that worked for FA-10000
    print(f"  Querying SLJrtResourceGroups for Job 95001...")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        f"Job = '{test_job}'"
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        count = len(items or [])
        print(f"  Records found: {count}")
        if items:
            print(f"  UNEXPECTED: Resource groups exist for TEST-BOM-001!")
            for i, item in enumerate(items):
                print(f"\n  --- Record {i+1} ---")
                print_record(item)
        else:
            print(f"  Confirmed: No resource groups for API-created routing (as expected)")

    # Also check with no filter, broader approach
    print(f"\n  Also checking with LIKE filter...")
    items2, err2 = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        "Job LIKE '%95001'"
    )
    if err2:
        print(f"  ERROR: {err2}")
    else:
        print(f"  Records found (LIKE): {len(items2 or [])}")

    return items or items2


# ────────────────────────────────────────────────────────────────
# Step 0.5: Test INSERT for TEST-BOM-001 Op 10
# ────────────────────────────────────────────────────────────────

def step05_test_insert(headers, metadata_results):
    """Attempt to insert a resource group for TEST-BOM-001 Op 10."""
    print_section("STEP 0.5: Test INSERT (Job 95001, OperNum=10)")

    test_job = "     95001"

    # Determine correct property names from metadata (step 0.1)
    info = metadata_results.get("info_endpoint", {})
    required = info.get("required", [])
    writable = info.get("writable", [])

    print(f"  Required properties: {required}")
    print(f"  Writable properties: {writable}")

    # Attempt 1: Use the correct property names from metadata
    # Expected from plan: Rgid (not ResourceGroup), QtyResources, Resactn, Sequence
    print(f"\n  --- Attempt 1: Using metadata-derived property names ---")
    insert_dict = {
        "Job": test_job,
        "Suffix": "0",
        "OperNum": "10",
    }
    # Add Rgid if it's in writable/required
    if "Rgid" in writable or "Rgid" in required:
        insert_dict["Rgid"] = "FA-400-LRG"
    elif "ResourceGroup" in writable or "ResourceGroup" in required:
        insert_dict["ResourceGroup"] = "FA-400-LRG"
    else:
        # Try Rgid anyway (most likely based on SLWcResourceGroups pattern)
        insert_dict["Rgid"] = "FA-400-LRG"
        print(f"  NOTE: 'Rgid' not found in metadata, trying anyway")

    # Add optional fields if known
    for field in ["QtyResources", "Sequence"]:
        if field in writable or field in required:
            if field == "QtyResources":
                insert_dict[field] = "1"
            elif field == "Sequence":
                insert_dict[field] = "1"

    print(f"  Insert payload: {json.dumps(insert_dict, indent=4)}")
    status, resp = ido_insert(headers, "SLJrtResourceGroups", insert_dict)
    print(f"  HTTP {status}")

    success = False
    if status == 200 and isinstance(resp, dict):
        success = resp.get("Success", False)
        msg = resp.get("Message", "")
        print(f"  Success: {success}")
        if msg:
            print(f"  Message: {msg}")
        if success:
            changes = resp.get("Changes", [])
            if changes:
                print(f"\n  Created record properties:")
                for prop in changes[0].get("Properties", []):
                    name = prop.get("Name", "")
                    value = prop.get("Value", "")
                    if name.startswith("_"):
                        continue
                    if value and str(value).strip() and str(value).strip() != "None":
                        print(f"    {name} = '{value}'")
            return {"success": True, "response": resp}
    else:
        print(f"  Response: {resp}")

    if not success:
        # Attempt 2: Minimal insert (just keys, let defaults fill in)
        print(f"\n  --- Attempt 2: Minimal insert (Job, Suffix, OperNum only) ---")
        status, resp = ido_insert(headers, "SLJrtResourceGroups", {
            "Job": test_job,
            "Suffix": "0",
            "OperNum": "10"
        })
        print(f"  HTTP {status}")
        if status == 200 and isinstance(resp, dict):
            success = resp.get("Success", False)
            msg = resp.get("Message", "")
            print(f"  Success: {success}")
            if msg:
                print(f"  Message: {msg}")
            if success:
                print(f"  Minimal insert succeeded! Now update with Rgid...")
                # Try updating Rgid on the new record
                status2, resp2 = ido_update(
                    headers, "SLJrtResourceGroups",
                    {"Rgid": "FA-400-LRG"},
                    f"Job = '{test_job}' AND Suffix = 0 AND OperNum = 10",
                    key_fields={"Job": test_job, "Suffix": "0", "OperNum": "10"}
                )
                if status2 == 200 and isinstance(resp2, dict):
                    print(f"  Update success: {resp2.get('Success', False)}")
                    if resp2.get("Message"):
                        print(f"  Update message: {resp2.get('Message')}")
                return {"success": True, "approach": "minimal_then_update", "response": resp}
        else:
            print(f"  Response: {resp}")

    if not success:
        # Attempt 3: Try with Wc field instead of/in addition to Rgid
        print(f"\n  --- Attempt 3: With Wc field ---")
        status, resp = ido_insert(headers, "SLJrtResourceGroups", {
            "Job": test_job,
            "Suffix": "0",
            "OperNum": "10",
            "Wc": "FA-400",
            "Rgid": "FA-400-LRG",
            "QtyResources": "1",
            "Sequence": "1"
        })
        print(f"  HTTP {status}")
        if status == 200 and isinstance(resp, dict):
            success = resp.get("Success", False)
            msg = resp.get("Message", "")
            print(f"  Success: {success}")
            if msg:
                print(f"  Message: {msg}")
            if success:
                return {"success": True, "approach": "with_wc", "response": resp}
        else:
            print(f"  Response: {resp}")

    # Verify what exists after all attempts
    print(f"\n  --- Verification: Query after insert attempts ---")
    items, err = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        f"Job = '{test_job}'"
    )
    if err:
        print(f"  ERROR: {err}")
    else:
        print(f"  Records found: {len(items or [])}")
        if items:
            for i, item in enumerate(items):
                print(f"\n  --- Record {i+1} ---")
                print_record(item)

    return {"success": success, "items_after": items}


# ────────────────────────────────────────────────────────────────
# Step 0.6: Test Relationship with SLJrtSchs.Setuprgid
# ────────────────────────────────────────────────────────────────

def step06_test_relationship(headers, insert_result):
    """Check if SLJrtResourceGroups insert affects SLJrtSchs.Setuprgid (or vice versa)."""
    print_section("STEP 0.6: Relationship: SLJrtResourceGroups vs SLJrtSchs.Setuprgid")

    test_job = "     95001"

    # Check current SLJrtSchs state
    print(f"  6a: Current SLJrtSchs state for Job 95001, Op 10...")
    items, err = ido_load(
        headers, "SLJrtSchs",
        None,
        f"Job = '{test_job}' AND Suffix = 0 AND OperNum = 10"
    )
    if err:
        print(f"  ERROR: {err}")
    elif items:
        setuprgid = items[0].get("Setuprgid", "")
        print(f"  Setuprgid = '{setuprgid}'")
        # Show all resource-related fields
        for item in items:
            for key, val in sorted(item.items()):
                if key.startswith("_"):
                    continue
                if val is not None and str(val).strip() and str(val).strip() != "None":
                    if "rg" in key.lower() or "resource" in key.lower() or "setup" in key.lower():
                        print(f"    {key} = '{val}'")
    else:
        print(f"  No SLJrtSchs record found for Op 10")

    # Check current SLJrtResourceGroups state
    print(f"\n  6b: Current SLJrtResourceGroups state for Job 95001, Op 10...")
    items2, err2 = ido_load(
        headers, "SLJrtResourceGroups",
        None,
        f"Job = '{test_job}' AND Suffix = 0 AND OperNum = 10"
    )
    if err2:
        print(f"  ERROR: {err2}")
    else:
        print(f"  Records found: {len(items2 or [])}")
        if items2:
            for i, item in enumerate(items2):
                print(f"\n  --- Record {i+1} ---")
                print_record(item)

    # Check SLJobRoutes for cross-IDO visibility
    print(f"\n  6c: SLJobRoutes state for Job 95001 (resource-related fields)...")
    items3, err3 = ido_load(
        headers, "SLJobRoutes",
        None,
        f"Job = '{test_job}'"
    )
    if err3:
        print(f"  ERROR: {err3}")
    elif items3:
        for item in items3:
            oper = item.get("OperNum", "")
            wc = item.get("Wc", "")
            print(f"\n  OperNum={oper}, Wc={wc}")
            for key, val in sorted(item.items()):
                if key.startswith("_"):
                    continue
                if val is not None and str(val).strip() and str(val).strip() != "None":
                    if "rg" in key.lower() or "resource" in key.lower() or "setup" in key.lower():
                        print(f"    {key} = '{val}'")

    # Determine relationship
    print(f"\n  --- Relationship Analysis ---")
    if insert_result and insert_result.get("success"):
        print(f"  SLJrtResourceGroups insert SUCCEEDED")
        if items and items[0].get("Setuprgid"):
            print(f"  SLJrtSchs.Setuprgid is ALSO populated")
            print(f"  CONCLUSION: They may be auto-linked, or Setuprgid was set earlier")
        else:
            print(f"  SLJrtSchs.Setuprgid is NOT populated")
            print(f"  CONCLUSION: SLJrtResourceGroups and SLJrtSchs are INDEPENDENT")
            print(f"  Both must be set separately for full resource group support")
    else:
        print(f"  SLJrtResourceGroups insert FAILED or was not attempted")
        print(f"  Cannot determine relationship without successful insert")

    return {"jrt_schs": items, "jrt_resource_groups": items2, "job_routes": items3}


# ────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Resource Group Discovery V2: Re-investigate SLJrtResourceGroups",
        epilog="Example: python discover_resource_groups_v2.py --test-insert"
    )
    parser.add_argument(
        "--test-insert",
        action="store_true",
        help="Attempt to insert a resource group for TEST-BOM-001 (steps 0.5-0.6)"
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

    # Step 0.1: IDO Metadata
    results["step01_metadata"] = step01_ido_metadata(headers)

    # Step 0.2: Systematic Queries
    results["step02_queries"] = step02_systematic_queries(headers)

    # Step 0.3: Capture Reference Record
    results["step03_reference"] = step03_capture_reference(headers, results["step02_queries"])

    # Step 0.4: TEST-BOM-001 Check
    results["step04_test_bom"] = step04_test_bom_check(headers)

    # Steps 0.5-0.6: Test Insert + Relationship (only with --test-insert)
    if args.test_insert:
        results["step05_insert"] = step05_test_insert(headers, results["step01_metadata"])
        results["step06_relationship"] = step06_test_relationship(headers, results.get("step05_insert"))
    else:
        print(f"\n  Steps 0.5-0.6: Skipped (use --test-insert to run)")

    # ────────────────────────────────────────────────────────────
    # SUMMARY
    # ────────────────────────────────────────────────────────────
    print_section("SUMMARY")

    # Step 0.1 summary
    meta = results.get("step01_metadata", {})
    info = meta.get("info_endpoint", {})
    tables = meta.get("IdoTables", [])
    if info:
        print(f"  Step 0.1 - IDO Metadata:")
        print(f"    Properties: {info.get('total', '?')}")
        print(f"    Required for insert: {info.get('required', [])}")
        print(f"    Writable: {info.get('writable', [])}")
        if tables:
            for t in tables:
                tt = t.get("TableType", "")
                marker = " <-- PRIMARY" if str(tt) == "3" else ""
                print(f"    Table: {t.get('TableName')} (Type={tt}){marker}")

    # Step 0.2 summary
    queries = results.get("step02_queries", {})
    total_found = 0
    for key, items in queries.items():
        if items:
            total_found += len(items)
    print(f"\n  Step 0.2 - Systematic Queries:")
    print(f"    Total records found across all approaches: {total_found}")
    if total_found == 0:
        print(f"    STATUS: SLJrtResourceGroups still has 0 records system-wide")
        print(f"    IMPLICATION: UI Resources grid may use a DIFFERENT mechanism")
    else:
        print(f"    STATUS: Records found! SLJrtResourceGroups IS used")

    # Step 0.3 summary
    ref = results.get("step03_reference")
    if ref:
        print(f"\n  Step 0.3 - FA-10000 Reference: {len(ref)} record(s) captured")
    else:
        print(f"\n  Step 0.3 - FA-10000 Reference: No data (investigating alternatives)")

    # Step 0.4 summary
    test_items = results.get("step04_test_bom")
    print(f"\n  Step 0.4 - TEST-BOM-001: {len(test_items or [])} resource group records")

    # Steps 0.5-0.6 summary
    if args.test_insert:
        insert = results.get("step05_insert", {})
        if isinstance(insert, dict):
            print(f"\n  Step 0.5 - Insert Test: {'SUCCEEDED' if insert.get('success') else 'FAILED'}")
        print(f"  Step 0.6 - Relationship: See details above")
    else:
        print(f"\n  Steps 0.5-0.6: Skipped (use --test-insert)")

    # NEXT STEPS
    print(f"\n  {'='*50}")
    print(f"  NEXT STEPS:")
    print(f"  {'='*50}")
    if total_found == 0 and not (args.test_insert and results.get("step05_insert", {}).get("success")):
        print(f"  1. If no records found AND insert fails:")
        print(f"     - The UI 'Resources grid' may use a different IDO or mechanism")
        print(f"     - Check if Setuprgid on SLJrtSchs is sufficient (already working)")
        print(f"     - Ask user: does setting Setuprgid alone resolve the validation error?")
        print(f"  2. If insert succeeds:")
        print(f"     - User should validate in Current Operations form")
        print(f"     - Check: Resources grid populated? Validation error gone?")
    else:
        print(f"  1. User validates in SyteLine UI:")
        print(f"     - Current Operations form for TEST-BOM-001")
        print(f"     - Resources grid populated?")
        print(f"     - No validation error navigating between operations?")

    if args.output_json:
        print(f"\n--- JSON OUTPUT ---")
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
