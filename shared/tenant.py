"""
Centralized tenant configuration for Infor SyteLine projects.

Provides site, logical ID, service account, and user registry
loaded from a single tenant_config.json file shared by all projects.

Config resolution order:
  1. TENANT_CONFIG env var -> path to tenant_config.json
  2. tenant_config.json in repository root
  3. FileNotFoundError with setup instructions

Usage:
    from shared.tenant import get_site, get_logical_id, get_users
    site = get_site()
    lid = get_logical_id()
    users = get_users()
"""
import json
import os
from pathlib import Path

# Cache loaded config to avoid repeated file reads
_config_cache = None

# Repository root (shared/ is one level below root)
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _resolve_config_path():
    """
    Resolve the path to the tenant_config.json file.

    Resolution order:
      1. TENANT_CONFIG environment variable
      2. tenant_config.json in repository root
      3. FileNotFoundError with setup instructions

    Returns:
        Path to the tenant_config.json file

    Raises:
        FileNotFoundError: If no config file can be found
    """
    # 1. TENANT_CONFIG env var
    env_path = os.environ.get('TENANT_CONFIG')
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p
        raise FileNotFoundError(
            f"TENANT_CONFIG points to '{env_path}' but file does not exist."
        )

    # 2. tenant_config.json in repo root
    root_path = _REPO_ROOT / 'tenant_config.json'
    if root_path.exists():
        return root_path

    # 3. Nothing found
    raise FileNotFoundError(
        "No tenant_config.json found. Run setup to create one:\n"
        "  python setup.py\n"
        "\n"
        "Or set the TENANT_CONFIG env var to point to your config file.\n"
        "See tenant_config.example.json for the expected format."
    )


def _validate_config(data, source_path):
    """
    Validate that loaded tenant config is well-formed.

    Args:
        data: Parsed JSON data
        source_path: Path the data was loaded from (for error messages)

    Returns:
        Validated config dict

    Raises:
        ValueError: If config is invalid or missing required fields
    """
    if not isinstance(data, dict):
        raise ValueError(
            f"Config file '{source_path}' must contain a JSON object, "
            f"got {type(data).__name__}"
        )

    required = {'site', 'logical_id', 'service_account'}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(
            f"Config file '{source_path}' is missing required fields: "
            f"{', '.join(sorted(missing))}"
        )

    # Validate users section if present
    users = data.get('users', {})
    if not isinstance(users, dict):
        raise ValueError(
            f"Config file '{source_path}': 'users' must be a JSON object"
        )
    for key, user in users.items():
        if not isinstance(user, dict):
            raise ValueError(
                f"Config file '{source_path}': user '{key}' must be a JSON object"
            )
        user_required = {'guid', 'name'}
        user_missing = user_required - set(user.keys())
        if user_missing:
            raise ValueError(
                f"Config file '{source_path}': user '{key}' missing fields: "
                f"{', '.join(sorted(user_missing))}"
            )

    return data


def get_tenant_config():
    """
    Load and validate tenant configuration.

    Returns:
        Dict with keys: site, logical_id, service_account, users

    Raises:
        FileNotFoundError: If no config file found
        ValueError: If config is invalid
    """
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    config_path = _resolve_config_path()

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Config file '{config_path}' is not valid JSON: {e}"
        )

    _config_cache = _validate_config(data, config_path)
    return _config_cache


def get_site():
    """Get the SyteLine site identifier (used in X-Infor-MongooseConfig header)."""
    return get_tenant_config()['site']


def get_logical_id():
    """Get the ION logical ID (e.g. 'lid://infor.syteline.csi/dals')."""
    return get_tenant_config()['logical_id']


def get_service_account():
    """Get the encrypted service account token for ION workflow deployment."""
    return get_tenant_config()['service_account']


def get_users():
    """
    Get the user registry from tenant config.

    Returns:
        Dict of user_key -> {guid, name, email (optional)}
    """
    return get_tenant_config().get('users', {})


def clear_cache():
    """Clear the cached config (useful for testing or after config changes)."""
    global _config_cache
    _config_cache = None
