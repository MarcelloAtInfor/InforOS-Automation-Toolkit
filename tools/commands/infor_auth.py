"""Inspect and optionally refresh Infor auth token state."""
from __future__ import annotations

import argparse
import sys

from common import build_result, emit_result, ensure_repo_import_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Auth readiness and token refresh")
    parser.add_argument("--show-source", action="store_true")
    parser.add_argument("--fetch-token", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        emit_result(
            build_result(
                status="ok",
                command="infor-auth",
                message="Dry-run only.",
                data={"args": vars(args)},
            )
        )
        return 0

    ensure_repo_import_path()
    try:
        from shared.auth import get_credentials, request_token
    except Exception as exc:
        emit_result(
            build_result(
                status="error",
                command="infor-auth",
                message="Failed to import shared auth module.",
                errors=[str(exc)],
            )
        )
        return 1

    try:
        creds = get_credentials()
    except Exception as exc:
        emit_result(
            build_result(
                status="error",
                command="infor-auth",
                message="Credential resolution failed.",
                errors=[str(exc)],
            )
        )
        return 1

    data = {
        "tenant_id": creds.get("ti"),
        "ionapi_path_hint": "resolved",
        "has_iu": bool(creds.get("iu")),
        "has_saak": bool(creds.get("saak")),
    }
    if args.show_source:
        data["iu"] = creds.get("iu")
        data["pu"] = creds.get("pu")
        data["ot"] = creds.get("ot")

    if args.fetch_token:
        try:
            token = request_token(save_path=None)
            data["token_preview"] = f"{token[:30]}..."
            data["token_length"] = len(token)
        except Exception as exc:
            emit_result(
                build_result(
                    status="error",
                    command="infor-auth",
                    message="Token request failed.",
                    data=data,
                    errors=[str(exc)],
                )
            )
            return 1

    emit_result(
        build_result(
            status="ok",
            command="infor-auth",
            message="Auth configuration is usable.",
            data=data,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
