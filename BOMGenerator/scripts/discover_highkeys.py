#!/usr/bin/env python3
"""
Phase 0 Discovery: Explore SLHighKeys IDO for job number tracking.

Queries:
1. All properties available on SLHighKeys
2. All job-related entries (TableColumnName LIKE 'job%')
3. Entries with 'BOM' prefix (if any exist)
4. Full unfiltered sample to see all prefixes and formats

Usage:
    python discover_highkeys.py
"""

import json
import sys
from pathlib import Path

# Add repo root to path for shared imports
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


def ido_query(headers, ido, filter_str="", properties="", record_cap=200):
    """Query an IDO collection and return raw response."""
    url = f"{IDO_URL()}/load/{ido}"
    params = {"recordCap": record_cap}
    if filter_str:
        params["filter"] = filter_str
    if properties:
        params["properties"] = properties
    resp = requests.get(url, headers=headers, params=params)
    return resp


def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_items(items, max_items=30):
    """Print items as formatted JSON rows."""
    if not items:
        print("  (no records)")
        return
    for i, item in enumerate(items[:max_items]):
        print(f"  [{i+1}] {json.dumps(item, indent=None)}")
    if len(items) > max_items:
        print(f"  ... and {len(items) - max_items} more records")


def main():
    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = SITE

    # ---------------------------------------------------------------
    # Query 1: Unfiltered SLHighKeys (no properties filter -- see all columns)
    # ---------------------------------------------------------------
    print_section("Query 1: SLHighKeys - Unfiltered sample (all properties)")
    resp = ido_query(headers, "SLHighKeys", record_cap=20)
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items", [])
        print(f"  Records returned: {len(items)}")
        if items:
            print(f"  Properties available: {list(items[0].keys())}")
        print_items(items)
    else:
        print(f"  Error: {resp.text[:500]}")

    # ---------------------------------------------------------------
    # Query 2: Job-related entries
    # ---------------------------------------------------------------
    print_section("Query 2: SLHighKeys - Job-related entries (TableColumnName LIKE 'job%')")
    resp = ido_query(headers, "SLHighKeys", filter_str="TableColumnName LIKE 'job%'")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items", [])
        print(f"  Records returned: {len(items)}")
        print_items(items)
    else:
        print(f"  Error: {resp.text[:500]}")

    # ---------------------------------------------------------------
    # Query 3: Entries with BOM prefix
    # ---------------------------------------------------------------
    print_section("Query 3: SLHighKeys - BOM prefix entries (Prefix='BOM')")
    resp = ido_query(headers, "SLHighKeys", filter_str="Prefix = 'BOM'")
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items", [])
        print(f"  Records returned: {len(items)}")
        print_items(items)
    else:
        print(f"  Error: {resp.text[:500]}")

    # ---------------------------------------------------------------
    # Query 4: All distinct prefixes in use
    # ---------------------------------------------------------------
    print_section("Query 4: SLHighKeys - All entries (see all prefixes)")
    resp = ido_query(headers, "SLHighKeys", record_cap=500)
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items", [])
        print(f"  Total records: {len(items)}")

        # Summarize by prefix
        prefixes = {}
        for item in items:
            prefix = item.get("Prefix", "(none)")
            table_col = item.get("TableColumnName", "?")
            last_val = item.get("LastValue", "?")
            if prefix not in prefixes:
                prefixes[prefix] = []
            prefixes[prefix].append(f"{table_col}={last_val}")

        print(f"\n  Prefixes found ({len(prefixes)}):")
        for prefix, entries in sorted(prefixes.items(), key=lambda x: x[0] or ""):
            print(f"    '{prefix}': {entries[:5]}{'...' if len(entries) > 5 else ''}")
    else:
        print(f"  Error: {resp.text[:500]}")

    # ---------------------------------------------------------------
    # Query 5: IDO metadata - what properties does SLHighKeys have?
    # ---------------------------------------------------------------
    print_section("Query 5: IdoProperties for SLHighKeys")
    resp = ido_query(
        headers, "IdoProperties",
        filter_str="CollectionName = 'SLHighKeys'",
        properties="PropertyName,ColumnName,TableAlias,ReadOnly,DataType",
        record_cap=100
    )
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items") or []
        print(f"  Properties count: {len(items)}")
        print_items(items, max_items=50)
    else:
        print(f"  Error: {resp.text[:500]}")

    # ---------------------------------------------------------------
    # Query 6: IdoTables for SLHighKeys (find primary table)
    # ---------------------------------------------------------------
    print_section("Query 6: IdoTables for SLHighKeys")
    resp = ido_query(
        headers, "IdoTables",
        filter_str="CollectionName = 'SLHighKeys'",
        properties="TableName,TableAlias,TableType",
        record_cap=20
    )
    print(f"  HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("Items") or []
        print(f"  Tables count: {len(items)}")
        print_items(items)
    else:
        print(f"  Error: {resp.text[:500]}")

    print(f"\n{'='*70}")
    print("  Discovery complete. Review results above.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
