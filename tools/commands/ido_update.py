"""Create/update/delete records via SyteLine IDO update endpoint."""
from __future__ import annotations

import argparse
import json
import sys

import requests

from common import build_result, emit_result, ensure_repo_import_path, load_json_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Update IDO records")
    parser.add_argument("--ido-name")
    parser.add_argument("--action", type=int, choices=[1, 2, 4])
    parser.add_argument("--payload-file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="ido-update",
                message="Dry-run only.",
                data={"args": vars(args)},
            )
        )
        return 0

    if not args.ido_name or not args.payload_file:
        emit_result(
            build_result(
                status="error",
                command="ido-update",
                message="Missing required arguments.",
                errors=["Provide --ido-name and --payload-file."],
            )
        )
        return 2

    if args.action == 3:
        emit_result(
            build_result(
                status="error",
                command="ido-update",
                message="Action 3 is unsupported.",
                errors=["Use Action 4 for delete."],
            )
        )
        return 2

    try:
        payload = load_json_file(args.payload_file)
    except Exception as exc:
        emit_result(
            build_result(
                status="error",
                command="ido-update",
                message="Invalid payload file.",
                errors=[str(exc)],
            )
        )
        return 1

    # Optional guard: enforce supplied --action if provided.
    if args.action is not None:
        try:
            changes = payload.get("Changes", [])
            if changes:
                changes[0]["Action"] = args.action
        except Exception:
            pass

    ensure_repo_import_path()
    from shared.auth import get_auth_headers
    from shared.config import IDO_URL, get_mongoose_config

    headers = get_auth_headers()
    headers["X-Infor-MongooseConfig"] = get_mongoose_config()

    url = f"{IDO_URL()}/update/{args.ido_name}"
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
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
                command="ido-update",
                message=f"IDO update failed: {exc}",
                data={"url": url, "ido_name": args.ido_name},
                errors=[detail] if detail else [],
            )
        )
        return 1

    emit_result(
        build_result(
            status="ok",
            command="ido-update",
            message="IDO update succeeded.",
            data={"ido_name": args.ido_name, "response": resp.json()},
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
