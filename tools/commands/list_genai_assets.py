"""List GenAI assets from GenAI Core API."""
from __future__ import annotations

import argparse
import json
import sys

import requests

from common import build_result, emit_result, ensure_repo_import_path


def main() -> int:
    parser = argparse.ArgumentParser(description="List GenAI assets")
    parser.add_argument("--prefix")
    parser.add_argument("--asset-type", choices=["API_DOCS", "TOOLKIT"])
    parser.add_argument("--output-mode", choices=["json", "table"], default="json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="list-genai-assets",
                message="Dry-run only.",
                data={"args": vars(args)},
            )
        )
        return 0

    ensure_repo_import_path()
    from shared.auth import get_auth_headers
    from shared.config import GENAI_CORE_URL

    headers = get_auth_headers()
    url = f"{GENAI_CORE_URL()}/api/v1/tools"
    resp = requests.get(url, headers=headers, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        detail = ""
        try:
            detail = json.dumps(resp.json(), ensure_ascii=False)
        except Exception:
            detail = resp.text[:500]
        emit_result(
            build_result(
                status="error",
                command="list-genai-assets",
                message=f"List request failed: {exc}",
                errors=[detail] if detail else [],
            )
        )
        return 1

    assets = resp.json()
    if not isinstance(assets, list):
        assets = []

    if args.prefix:
        assets = [a for a in assets if str(a.get("name", "")).startswith(args.prefix)]
    if args.asset_type:
        assets = [a for a in assets if a.get("type") == args.asset_type]

    rows = [
        {
            "name": a.get("name"),
            "type": a.get("type"),
            "guid": a.get("guid"),
            "enabled": a.get("enabled"),
        }
        for a in assets
    ]

    if args.output_mode == "table":
        emit_result({"data": rows}, output_mode="table")
    else:
        emit_result(
            build_result(
                status="ok",
                command="list-genai-assets",
                message=f"Retrieved {len(assets)} asset(s).",
                data={"count": len(assets), "assets": rows},
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
