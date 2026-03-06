"""Query records from a SyteLine IDO collection."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import requests

from common import build_result, emit_result, ensure_repo_import_path


def _normalize_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize IDO response items into flat row dicts."""
    rows: list[dict[str, Any]] = []
    for item in items:
        row: dict[str, Any] = {}

        # Common metadata fields sometimes returned outside Properties array.
        for key in ("ItemID", "_ItemId", "RowPointer"):
            if key in item:
                row[key] = item.get(key)

        props = item.get("Properties")
        if isinstance(props, list):
            for prop in props:
                name = prop.get("Name")
                if name:
                    row[name] = prop.get("Value")
        else:
            # Some endpoints may already return flattened objects.
            for key, value in item.items():
                if key not in {"Properties"}:
                    row[key] = value

        rows.append(row)
    return rows


def execute_query(
    *,
    ido_name: str,
    properties: str | None = None,
    filter_str: str | None = None,
    orderby: str | None = None,
    record_cap: int = 100,
) -> dict[str, Any]:
    """Execute an IDO load query and return standard response envelope."""
    ensure_repo_import_path()
    from shared.auth import get_auth_headers
    from shared.config import IDO_URL, get_mongoose_config

    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = get_mongoose_config()

    params: dict[str, Any] = {"recordCap": record_cap}
    quirks: list[str] = []

    ido_lower = ido_name.lower()
    if ido_lower == "slitemwhses":
        # Known IDO quirk: properties causes empty results.
        if properties:
            quirks.append(
                "SLItemwhses ignores/returns empty with properties; omitted properties automatically."
            )
        properties = None
    if ido_lower == "sljrtresourcegroups" and not properties:
        return build_result(
            status="error",
            command="query-ido",
            message="SLJrtResourceGroups requires explicit properties.",
            errors=[
                "Provide --properties (example: Job,Suffix,OperNum,Rgid,_ItemId)."
            ],
        )

    if ido_lower == "slwcs" and properties:
        allowed = {"wc", "wcdescription", "deptdescription"}
        requested = {p.strip().lower() for p in properties.split(",") if p.strip()}
        if not requested.issubset(allowed):
            return build_result(
                status="error",
                command="query-ido",
                message="SLWcs property set is restricted for reliability.",
                errors=[
                    "Use only: Wc,WcDescription,DeptDescription."
                ],
            )

    if properties:
        params["properties"] = properties
    if filter_str:
        params["filter"] = filter_str
    if orderby:
        params["orderby"] = orderby

    url = f"{IDO_URL()}/load/{ido_name}"
    resp = requests.get(url, headers=headers, params=params, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        detail = ""
        try:
            detail = json.dumps(resp.json(), ensure_ascii=False)
        except Exception:
            detail = resp.text[:500]
        return build_result(
            status="error",
            command="query-ido",
            message=f"IDO query failed: {exc}",
            errors=[detail] if detail else [],
            data={"url": url, "params": params},
        )

    payload = resp.json()
    items = payload.get("Items", []) if isinstance(payload, dict) else []
    rows = _normalize_rows(items) if isinstance(items, list) else []

    return build_result(
        status="ok",
        command="query-ido",
        message=f"Query succeeded for {ido_name}.",
        data={
            "ido_name": ido_name,
            "params": params,
            "count": len(rows),
            "more_rows_exist": bool(payload.get("MoreRowsExist", False)),
            "rows": rows,
            "quirks_applied": quirks,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Query IDO records")
    parser.add_argument("--ido-name", help="Case-sensitive IDO name (e.g., SLItems)")
    parser.add_argument("--properties")
    parser.add_argument("--filter")
    parser.add_argument("--orderby")
    parser.add_argument("--record-cap", type=int, default=100)
    parser.add_argument("--output-mode", choices=["json", "table"], default="json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="query-ido",
                message="Dry-run only.",
                data={"args": vars(args)},
            ),
            output_mode=args.output_mode,
        )
        return 0

    if not args.ido_name:
        emit_result(
            build_result(
                status="error",
                command="query-ido",
                message="Missing required argument --ido-name.",
                errors=["Provide a case-sensitive IDO name."],
            ),
            output_mode=args.output_mode,
        )
        return 2

    result = execute_query(
        ido_name=args.ido_name,
        properties=args.properties,
        filter_str=args.filter,
        orderby=args.orderby,
        record_cap=args.record_cap,
    )

    if args.output_mode == "table" and result.get("status") == "ok":
        rows = result.get("data", {}).get("rows", [])
        emit_result({"data": rows}, output_mode="table")
    else:
        emit_result(result, output_mode="json")
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
