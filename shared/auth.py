"""
Centralized authentication utilities for Infor ION API.
Used by: CSIPOAssetCreationTool, BOMGenerator

Credential resolution order:
  1. IONAPI_FILE env var -> path to .ionapi file
  2. .ionapi in current working directory
  3. If none found -> FileNotFoundError with instructions

Token workflow:
  get_auth_headers() auto-fetches and caches OAuth tokens.
  No need to pre-generate access_token.txt files.

Usage:
    from shared.auth import get_auth_headers
    headers = get_auth_headers()
"""
import json
import os
import time
import requests
from pathlib import Path

# Required fields in .ionapi credential file
_REQUIRED_FIELDS = {'ti', 'ci', 'cs', 'pu', 'ot', 'saak', 'sask'}

# Module-level token cache
_token_cache = {
    'access_token': None,
    'expires_at': 0.0,  # epoch timestamp
}

# Safety margin: refresh token 60 seconds before actual expiry
_EXPIRY_MARGIN_SECONDS = 60


def _resolve_ionapi_path():
    """
    Resolve the path to the .ionapi credentials file.

    Resolution order:
      1. IONAPI_FILE environment variable
      2. .ionapi in current working directory
      3. FileNotFoundError with setup instructions

    Returns:
        Path to the .ionapi file

    Raises:
        FileNotFoundError: If no credential file can be found
    """
    # 1. IONAPI_FILE env var
    env_path = os.environ.get('IONAPI_FILE')
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p
        raise FileNotFoundError(
            f"IONAPI_FILE points to '{env_path}' but file does not exist."
        )

    # 2. .ionapi in current working directory
    cwd_path = Path.cwd() / '.ionapi'
    if cwd_path.exists():
        return cwd_path

    # 3. Nothing found
    raise FileNotFoundError(
        "No .ionapi credential file found. Set up credentials using one of:\n"
        "  1. Set IONAPI_FILE env var to the path of your .ionapi file\n"
        "  2. Place a .ionapi file in your working directory\n"
    )


def _validate_credentials(data, source_path):
    """
    Validate that loaded credentials are well-formed.

    Args:
        data: Parsed JSON data
        source_path: Path the data was loaded from (for error messages)

    Returns:
        Validated credentials dict

    Raises:
        ValueError: If credentials are invalid or missing required fields
    """
    if not isinstance(data, dict):
        raise ValueError(
            f"Credential file '{source_path}' must contain a JSON object, "
            f"got {type(data).__name__}"
        )

    missing = _REQUIRED_FIELDS - set(data.keys())
    if missing:
        raise ValueError(
            f"Credential file '{source_path}' is missing required fields: "
            f"{', '.join(sorted(missing))}"
        )

    return data


def get_credentials():
    """
    Load and validate credentials from the resolved .ionapi file.

    Returns:
        Dict with credential fields (ti, ci, cs, pu, ot, saak, sask, iu, etc.)

    Raises:
        FileNotFoundError: If no credential file found
        ValueError: If file is not valid JSON or missing required fields
    """
    ionapi_path = _resolve_ionapi_path()

    try:
        with open(ionapi_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Credential file '{ionapi_path}' is not valid JSON: {e}"
        )

    return _validate_credentials(data, ionapi_path)


def get_token_url(creds=None):
    """Construct OAuth token URL from credentials."""
    if creds is None:
        creds = get_credentials()
    return f"{creds['pu']}{creds['ot']}"


def request_token(save_path=None):
    """
    Request new OAuth token using password grant.

    Uses service account access key (saak) and secret key (sask)
    with password grant type (NOT client_credentials).

    Also populates the in-memory token cache so subsequent calls to
    get_auth_headers() reuse this token until it expires.

    Args:
        save_path: Optional path to save token file. If None, token is not saved.

    Returns:
        access_token string

    Raises:
        requests.HTTPError: If token request fails
    """
    creds = get_credentials()
    token_url = get_token_url(creds)

    data = {
        'grant_type': 'password',
        'username': creds['saak'],
        'password': creds['sask'],
        'client_id': creds['ci'],
        'client_secret': creds['cs']
    }

    print(f"Requesting token from: {token_url}")
    print("Using password grant type with service account credentials")

    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()

    token_data = response.json()
    access_token = token_data['access_token']
    expires_in = token_data.get('expires_in', 3600)

    # Populate module-level cache
    _token_cache['access_token'] = access_token
    _token_cache['expires_at'] = time.time() + expires_in - _EXPIRY_MARGIN_SECONDS

    print(f"\n[SUCCESS] Token obtained successfully!")
    print(f"Expires in: {expires_in} seconds ({expires_in/3600:.1f} hours)")
    print(f"\nAccess Token (first 50 chars):")
    print(access_token[:50] + "...")

    if save_path:
        save_path = Path(save_path)
        with open(save_path, 'w') as f:
            f.write(access_token)
        print(f"\n[SUCCESS] Token saved to: {save_path}")

    return access_token


def _get_cached_token():
    """
    Return cached token if still valid, else None.

    Token is considered expired if current time >= expires_at
    (which already includes the 60-second safety margin).
    """
    if _token_cache['access_token'] and time.time() < _token_cache['expires_at']:
        return _token_cache['access_token']
    return None


def get_auth_headers(token=None, **_kwargs):
    """
    Get standard authorization headers for API calls.

    Resolution order:
      1. Explicit token= parameter (if provided)
      2. In-memory cached token (if still valid)
      3. Auto-fetch new token via OAuth

    Args:
        token: Token string (if already loaded). Usually omitted —
               the function auto-fetches and caches tokens.

    Returns:
        Dict with Authorization and Content-Type headers
    """
    if token is None:
        # Try in-memory cache
        token = _get_cached_token()

    if token is None:
        # Auto-fetch via OAuth
        token = request_token()

    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


# Allow running as script for token generation
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        # Save to specified directory
        save_dir = Path(sys.argv[1])
        if not save_dir.is_absolute():
            # Make relative to repo root
            save_dir = Path(__file__).parent.parent / save_dir
        save_path = save_dir / "access_token.txt"
    else:
        # Default: save to shared/ directory
        save_path = Path(__file__).parent / "access_token.txt"

    request_token(save_path)
