"""Tenant configuration for workflow generation.

Contains site, service account, and user registry.
Loads values from the central tenant_config.json via shared.tenant.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from src.workflow_builder.models import DistributionItem

# Ensure repo root is on sys.path so shared/ is importable
_REPO_ROOT = str(Path(__file__).resolve().parent.parent.parent.parent)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


@dataclass
class UserEntry:
    """A user in the tenant registry."""

    guid: str
    description: str
    send_email: bool = False


@dataclass
class TenantConfig:
    """Tenant configuration for workflow rendering."""

    site: str
    logical_id: str
    service_account: str
    users: dict[str, UserEntry] = field(default_factory=dict)

    def resolve_distribution(
        self, users: str | list[str], send_email: bool = False
    ) -> list[DistributionItem]:
        """Resolve user key(s) to DistributionItem list.

        Args:
            users: A single user key (e.g. "user1") or list of user keys.
            send_email: If True, overrides all users to send_email=True.
                If False (default), uses each user's default send_email setting.
        """
        if isinstance(users, str):
            users = [users]

        items = []
        for user_key in users:
            if user_key not in self.users:
                raise ValueError(f"Unknown user '{user_key}' in tenant config")
            user = self.users[user_key]
            items.append(
                DistributionItem(
                    name=user.guid,
                    description=user.description,
                    send_email=send_email or user.send_email,
                )
            )
        return items


def extract_service_account_from_dict(workflow: dict) -> str | None:
    """Extract encrypted serviceAccount token from a workflow dict.

    Checks top-level ``serviceAccount`` first (API response format),
    then searches recursively through ionapi flowparts.

    Returns:
        The token string, or None if not found.
    """
    # 1. Top-level field (present in API GET responses)
    top = workflow.get("serviceAccount")
    if top:
        return top

    # 2. Recursive search through flowparts
    def _find_sa(flowparts: list[dict]) -> str | None:
        for fp in flowparts:
            if fp.get("_type") == "ionapi" and "serviceAccount" in fp:
                return fp["serviceAccount"]
            if fp.get("_type") == "subworkflow":
                found = _find_sa(fp.get("subFlow", {}).get("flowParts", []))
                if found:
                    return found
            if fp.get("_type") == "ifthenelse":
                for branch_key in ("trueBranch", "falseBranch"):
                    branch = fp.get(branch_key, {})
                    found = _find_sa(branch.get("flowParts", []))
                    if found:
                        return found
            if fp.get("_type") == "parallel":
                for seq_flow in fp.get("sequentialFlows", []):
                    found = _find_sa(seq_flow.get("flowParts", []))
                    if found:
                        return found
        return None

    return _find_sa(workflow.get("sequentialFlow", {}).get("flowParts", []))


def extract_service_account(reference_path: str | Path) -> str:
    """Extract encrypted serviceAccount token from a reference workflow JSON file.

    Utility function — used by setup.py and for manual extraction.
    Normal config loading uses shared.tenant.get_service_account() instead.
    """
    with open(reference_path, "r", encoding="utf-8") as f:
        ref = json.load(f)

    sa = extract_service_account_from_dict(ref)
    if sa is None:
        raise ValueError(f"No serviceAccount found in {reference_path}")
    return sa


def load_default() -> TenantConfig:
    """Load tenant configuration from central tenant_config.json.

    Reads site, logical_id, service_account, and users from the shared
    config file (see shared/tenant.py for resolution order).
    """
    from shared.tenant import get_tenant_config

    config = get_tenant_config()

    # Build UserEntry objects from config users dict
    users: dict[str, UserEntry] = {}
    for key, user_data in config.get("users", {}).items():
        users[key] = UserEntry(
            guid=user_data["guid"],
            description=user_data["name"],
        )

    return TenantConfig(
        site=config["site"],
        logical_id=config["logical_id"],
        service_account=config["service_account"],
        users=users,
    )
