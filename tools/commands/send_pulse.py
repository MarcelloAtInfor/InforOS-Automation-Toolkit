"""Send ION Pulse alerts/notifications/tasks."""
from __future__ import annotations

import argparse
import json
import sys

import requests

from common import build_result, emit_result, ensure_repo_import_path, load_json_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Send Pulse message")
    parser.add_argument("--pulse-type", choices=["alert", "notification", "task"])
    parser.add_argument("--payload-file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="send-pulse",
                message="Dry-run only.",
                data={"args": vars(args)},
            )
        )
        return 0

    if not args.pulse_type or not args.payload_file:
        emit_result(
            build_result(
                status="error",
                command="send-pulse",
                message="Missing required arguments.",
                errors=["Provide --pulse-type and --payload-file."],
            )
        )
        return 2

    try:
        payload = load_json_file(args.payload_file)
    except Exception as exc:
        emit_result(
            build_result(
                status="error",
                command="send-pulse",
                message="Invalid payload file.",
                errors=[str(exc)],
            )
        )
        return 1

    ensure_repo_import_path()
    from shared.auth import get_auth_headers
    from shared.config import get_base_url

    headers = get_auth_headers()
    base = get_base_url("IONSERVICES/process/application")
    url = f"{base}/v1/pulse/{args.pulse_type}/create"

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
                command="send-pulse",
                message=f"Pulse request failed: {exc}",
                data={"url": url},
                errors=[detail] if detail else [],
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
            command="send-pulse",
            message=f"Pulse {args.pulse_type} sent.",
            data={"response": body},
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
