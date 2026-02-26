# shared/ — Centralized Authentication & Configuration

## Purpose

Python module providing OAuth 2.0 authentication and Infor OS service URL construction. Used by all projects in this repository (CSIPOAssetCreationTool, BOMGenerator).

**Status**: Stable. Single source of truth for authentication.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## Files

| File | Purpose |
|------|---------|
| `auth.py` | Env-var credential resolution, validation, OAuth 2.0 token generation (password grant), in-memory caching, auto-fetch |
| `config.py` | Tenant ID lookup and service URL construction (from `iu` field in credentials) |
| `__init__.py` | Public API — exports all 11 functions |

## Credential Resolution

Credentials are resolved in this order:

1. **`IONAPI_FILE` env var** → path to `.ionapi` file (recommended)
2. **`.ionapi` in current working directory**
3. **Error**: `FileNotFoundError` with setup instructions

### Setup (Recommended)

Set the `IONAPI_FILE` environment variable:

```bash
# Windows (cmd)
set IONAPI_FILE=C:\path\to\your\credentials.ionapi

# Windows (PowerShell)
$env:IONAPI_FILE = "C:\path\to\your\credentials.ionapi"

# Linux/Mac
export IONAPI_FILE=/path/to/your/credentials.ionapi
```

### Credential Validation

On load, credentials are validated for:
- Valid JSON format (parseable, is a dict)
- All 7 required fields present: `ti`, `ci`, `cs`, `pu`, `ot`, `saak`, `sask`
- Clear error messages naming any missing fields

## Public API

### From `auth.py`

| Export | Type | Purpose |
|--------|------|---------|
| `get_credentials()` | Function | Load, validate, and return ionapi JSON → dict |
| `get_token_url(creds=None)` | Function | Build OAuth token endpoint URL |
| `request_token(save_path=None)` | Function | Request OAuth token via password grant, cache in memory, optionally save to file |
| `get_auth_headers(token=None)` | Function | Build `{Authorization, Content-Type}` headers with auto-fetch |

### From `config.py`

| Export | Type | Purpose |
|--------|------|---------|
| `get_tenant_id()` | Function | Returns tenant ID from credentials |
| `get_mongoose_config()` | Function | Returns `{ti}_DALS` — SyteLine MongooseConfig header value |
| `get_base_url(service='')` | Function | Builds `{iu}/{ti}/{service}` URL from credentials |
| `GENAI_CORE_URL()` | Function | → `{base}/GENAI/coresvc` (tool/agent management) |
| `GENAI_CHAT_URL()` | Function | → `{base}/GENAI/chatsvc` (agent execution) |
| `IDP_URL()` | Function | → `{base}/COLEMANDDP/iddpuisvc` (document processing) |
| `IDO_URL()` | Function | → `{base}/CSI/IDORequestService/ido` (SyteLine data) |

## Token Management

### Auto-Fetch (New — Recommended)

`get_auth_headers()` with no arguments automatically:
1. Checks the in-memory token cache
2. If no cached token (or expired), fetches a new one via OAuth
3. Caches the token with a 60-second safety margin before expiry
4. Returns ready-to-use headers

```python
# Simplest usage — no token files, no manual steps
headers = get_auth_headers()
response = requests.get(url, headers=headers)
```

### Resolution Order in `get_auth_headers()`

1. **Explicit `token=` parameter** (if provided)
2. **In-memory cached token** (if still valid)
3. **Auto-fetch new token via OAuth** (default)

### In-Memory Cache

- Module-level cache (no class needed)
- Tokens cached until `expires_in - 60` seconds
- 60-second safety margin prevents race conditions
- Cache populated by both `request_token()` and `get_auth_headers()` auto-fetch
- Cache is per-process (resets on script restart)

## Usage Patterns

### Simple Usage (New Pattern)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from shared.auth import get_auth_headers
from shared.config import IDO_URL

# No token files needed — auto-fetches and caches
headers = get_auth_headers()
url = f"{IDO_URL()}/load/SLItems"
response = requests.get(url, headers=headers, params={"filter": "Item LIKE 'TEST%'"})
```

### Multiple API Calls (Cache Reuse)

```python
# First call fetches token and caches it
headers = get_auth_headers()
resp1 = requests.get(f"{IDO_URL()}/load/SLItems", headers=headers)

# Second call reuses cached token (no network call)
headers = get_auth_headers()
resp2 = requests.get(f"{IDO_URL()}/load/SLJobs", headers=headers)
```

### Explicit Token (When Needed)

```python
from shared.auth import request_token, get_auth_headers

# Get just the token string (e.g., for multipart uploads that need custom headers)
token = request_token()
headers = {"Authorization": f"Bearer {token}"}
```

### CLI Token Generation (Legacy — Still Supported)

```bash
# Save to specific directory
python -m shared.auth CSIPOAssetCreationTool/Agents&Tools/scripts

# Save to shared/ (default)
python -m shared.auth
```

## OAuth Flow

1. Credentials resolved via `IONAPI_FILE` env var or CWD `.ionapi`
2. Credentials validated (JSON format, 7 required fields)
3. Token requested via **password grant** (NOT client_credentials) to `{pu}{ot}`
4. Bearer token returned, valid for ~2 hours
5. Token cached in memory with 60-second safety margin
6. Token passed in `Authorization: Bearer {token}` header

## Key Discoveries

- **Grant type is `password`**, not `client_credentials` — uses `saak`/`sask` as username/password
- **Token lifetime is ~2 hours** — in-memory cache handles refresh automatically
- **Base URL from `iu` field** — `config.py` derives URLs from credentials, not hardcoded
- **No pre-generated token files needed** — `get_auth_headers()` auto-fetches

## Credential File Format

The `.ionapi` file is JSON with these fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `ti` | Yes | Tenant ID |
| `cn` | No | Connection name |
| `ci` | Yes | Client ID |
| `cs` | Yes | Client Secret |
| `pu` | Yes | OAuth provider URL base |
| `ot` | Yes | Token endpoint path |
| `saak` | Yes | Service account access key (username) |
| `sask` | Yes | Service account secret key (password) |
| `iu` | No* | ION API base URL (used by config.py for URL construction) |

*`iu` is not validated as required by auth.py but is required by config.py's `get_base_url()`.

**Security**: This file is gitignored and must never be committed. See root `.gitignore`.
