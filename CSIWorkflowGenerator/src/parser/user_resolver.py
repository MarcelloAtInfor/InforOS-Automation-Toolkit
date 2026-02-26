"""User resolution and validation against tenant config.

Functions for resolving user references, listing available
users, and validating distribution references.
"""
from __future__ import annotations

import difflib
from dataclasses import dataclass, field

from src.config.tenant import TenantConfig


@dataclass
class UserInfo:
    """Information about a tenant user."""

    key: str
    guid: str
    description: str


@dataclass
class DistributionResult:
    """Result of validating a distribution reference."""

    valid: bool
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def suggest_users(text: str, tenant: TenantConfig, n: int = 3) -> list[str]:
    """Suggest similar user keys using fuzzy matching."""
    return difflib.get_close_matches(
        text, tenant.users.keys(), n=n, cutoff=0.4
    )


def list_users(tenant: TenantConfig) -> list[UserInfo]:
    """List all users in the tenant registry."""
    return [
        UserInfo(key=key, guid=user.guid, description=user.description)
        for key, user in tenant.users.items()
    ]


def validate_distribution(
    distribution: str | list[str], tenant: TenantConfig
) -> DistributionResult:
    """Validate a distribution reference against tenant config.

    Accepts a single user key or list of user keys.
    Returns a DistributionResult with validation details and suggestions.
    """
    if isinstance(distribution, str):
        user_keys = [distribution]
    else:
        user_keys = distribution

    issues = []
    suggestions = []
    for user_key in user_keys:
        if user_key not in tenant.users:
            issue = f"User '{user_key}' not found in tenant config"
            issues.append(issue)
            user_suggestions = suggest_users(user_key, tenant)
            suggestions.extend(user_suggestions)

    return DistributionResult(
        valid=not issues,
        issues=issues,
        suggestions=suggestions,
    )
