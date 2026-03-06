"""IDO metadata discovery using IdoCollections/IdoProperties/IdoTables."""
from __future__ import annotations

import argparse
import sys

from common import build_result, emit_result
from query_ido import execute_query


def _run_mode(mode: str, keyword: str | None, collection_name: str | None) -> dict:
    """Run selected lookup mode via query-ido core."""
    if mode == "collections":
        if not keyword:
            return build_result(
                status="error",
                command="ido-lookup",
                message="Missing required --keyword for collections mode.",
                errors=["Example: --mode collections --keyword Vendor"],
            )
        return execute_query(
            ido_name="IdoCollections",
            properties="CollectionName",
            filter_str=f"CollectionName LIKE '%{keyword}%'",
            orderby="CollectionName ASC",
            record_cap=200,
        )

    if mode == "properties":
        if not collection_name:
            return build_result(
                status="error",
                command="ido-lookup",
                message="Missing required --collection-name for properties mode.",
                errors=["Example: --mode properties --collection-name SLPOs"],
            )
        return execute_query(
            ido_name="IdoProperties",
            properties="PropertyName,PropertyDataType,ColumnName,ColumnTableAlias,ColumnTableName",
            filter_str=f"CollectionName = '{collection_name}'",
            orderby="PropertyName ASC",
            record_cap=2000,
        )

    if mode == "tables":
        if not collection_name:
            return build_result(
                status="error",
                command="ido-lookup",
                message="Missing required --collection-name for tables mode.",
                errors=["Example: --mode tables --collection-name SLPOs"],
            )
        return execute_query(
            ido_name="IdoTables",
            properties="TableName,TableType,JoinType",
            filter_str=f"CollectionName = '{collection_name}'",
            orderby="TableName ASC",
            record_cap=200,
        )

    return build_result(
        status="error",
        command="ido-lookup",
        message=f"Unsupported mode: {mode}",
        errors=["Valid modes: collections, properties, tables"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Lookup IDO metadata")
    parser.add_argument("--mode", choices=["collections", "properties", "tables"], required=False)
    parser.add_argument("--keyword")
    parser.add_argument("--collection-name")
    parser.add_argument("--output-mode", choices=["json", "table"], default="json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="ido-lookup",
                message="Dry-run only.",
                data={"args": vars(args)},
            ),
            output_mode=args.output_mode,
        )
        return 0

    if not args.mode:
        emit_result(
            build_result(
                status="error",
                command="ido-lookup",
                message="Missing required --mode.",
                errors=["Valid modes: collections, properties, tables"],
            ),
            output_mode=args.output_mode,
        )
        return 2

    result = _run_mode(args.mode, args.keyword, args.collection_name)
    result["command"] = "ido-lookup"

    if args.output_mode == "table" and result.get("status") == "ok":
        rows = result.get("data", {}).get("rows", [])
        emit_result({"data": rows}, output_mode="table")
    else:
        emit_result(result, output_mode="json")
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
