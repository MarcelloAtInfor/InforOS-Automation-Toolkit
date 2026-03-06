"""Deploy/update/enable/disable/delete GenAI assets."""
from __future__ import annotations

import argparse
import json
import sys

import requests

from common import build_result, emit_result, ensure_repo_import_path, load_json_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy GenAI assets")
    parser.add_argument("--spec-file")
    parser.add_argument(
        "--operation",
        choices=["create", "update", "enable", "disable", "delete"],
    )
    parser.add_argument("--guid")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="deploy-genai-asset",
                message="Dry-run only.",
                data={"args": vars(args)},
            )
        )
        return 0

    if not args.operation:
        emit_result(
            build_result(
                status="error",
                command="deploy-genai-asset",
                message="Missing required --operation.",
                errors=["Valid: create, update, enable, disable, delete"],
            )
        )
        return 2

    ensure_repo_import_path()
    from shared.auth import get_auth_headers
    from shared.config import GENAI_CORE_URL

    headers = get_auth_headers()
    base = f"{GENAI_CORE_URL()}/api/v1/tools"

    try:
        if args.operation in {"create", "update"}:
            if not args.spec_file:
                raise ValueError("--spec-file is required for create/update")
            spec = load_json_file(args.spec_file)
            resp = requests.put(base, headers=headers, json=spec, timeout=60)
        elif args.operation in {"enable", "disable"}:
            guid = args.guid
            if not guid and args.spec_file:
                spec = load_json_file(args.spec_file)
                guid = spec.get("guid")
            if not guid:
                raise ValueError("--guid or --spec-file with guid is required for enable/disable")
            payload = {"guid": guid, "enabled": args.operation == "enable"}
            resp = requests.put(f"{base}/enable", headers=headers, json=payload, timeout=60)
        else:  # delete
            guid = args.guid
            if not guid and args.spec_file:
                spec = load_json_file(args.spec_file)
                guid = spec.get("guid")
            if not guid:
                raise ValueError("--guid or --spec-file with guid is required for delete")
            resp = requests.delete(f"{base}/{guid}", headers=headers, timeout=60)

        resp.raise_for_status()

    except ValueError as exc:
        emit_result(
            build_result(
                status="error",
                command="deploy-genai-asset",
                message="Argument validation failed.",
                errors=[str(exc)],
            )
        )
        return 2
    except requests.HTTPError as exc:
        detail = ""
        try:
            detail = json.dumps(resp.json(), ensure_ascii=False)  # type: ignore[name-defined]
        except Exception:
            detail = getattr(resp, "text", "")[:500] if "resp" in locals() else ""
        emit_result(
            build_result(
                status="error",
                command="deploy-genai-asset",
                message=f"Asset operation failed: {exc}",
                errors=[detail] if detail else [],
            )
        )
        return 1
    except Exception as exc:
        emit_result(
            build_result(
                status="error",
                command="deploy-genai-asset",
                message="Unexpected failure.",
                errors=[str(exc)],
            )
        )
        return 1

    body = {}
    try:
        body = resp.json()
    except Exception:
        body = {"text": resp.text[:500]}

    emit_result(
        build_result(
            status="ok",
            command="deploy-genai-asset",
            message=f"Operation '{args.operation}' succeeded.",
            data={"operation": args.operation, "response": body},
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

