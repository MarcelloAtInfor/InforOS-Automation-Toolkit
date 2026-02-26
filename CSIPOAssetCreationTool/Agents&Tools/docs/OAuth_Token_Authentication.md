# Infor ION API - OAuth Token Authentication Guide

## Problem
When calling Infor ION API endpoints, you need a valid OAuth 2.0 access token. Tokens expire after 2 hours (7200 seconds), requiring periodic renewal.

## Solution

### Using the .ionapi Credentials File

The `.ionapi` credentials file contains all necessary authentication information:

```json
{
  "ti": "TENANT_ID",
  "cn": "Connection Name",
  "ci": "client_id",
  "cs": "client_secret",
  "iu": "https://ionapi-url",
  "pu": "https://sso-url/TENANT_ID/as/",
  "ot": "token.oauth2",
  "saak": "service_account_access_key",
  "sask": "service_account_secret_key"
}
```

### Key Fields

- **saak**: Service Account Access Key (use as username)
- **sask**: Service Account Secret Key (use as password)
- **ci**: Client ID
- **cs**: Client Secret
- **pu**: SSO base URL
- **ot**: Token endpoint path

### Correct Authentication Method

**Use PASSWORD grant type** (not client_credentials):

```python
import json
import requests
from pathlib import Path

# Load credentials
creds_path = Path("path/to/your-credentials.ionapi")
with open(creds_path, 'r') as f:
    creds = json.load(f)

# Build token URL
token_url = f"{creds['pu']}{creds['ot']}"
# Example: https://mingle-sso.inforcloudsuite.com:443/TENANT/as/token.oauth2

# Request token using password grant
data = {
    'grant_type': 'password',
    'username': creds['saak'],  # Service Account Access Key
    'password': creds['sask'],  # Service Account Secret Key
    'client_id': creds['ci'],
    'client_secret': creds['cs']
}

response = requests.post(token_url, data=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    expires_in = token_data['expires_in']  # Usually 7200 (2 hours)

    # Save token for use
    with open('access_token.txt', 'w') as f:
        f.write(access_token)
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Common Mistakes

❌ **Wrong**: Using `client_credentials` grant type
```python
data = {
    'grant_type': 'client_credentials',  # This will fail!
    'client_id': creds['ci'],
    'client_secret': creds['cs']
}
# Error: "Unsupported grant type client_credentials. Expected one of password"
```

✅ **Correct**: Using `password` grant type with service account credentials
```python
data = {
    'grant_type': 'password',
    'username': creds['saak'],  # Service account key
    'password': creds['sask'],  # Service account secret
    'client_id': creds['ci'],
    'client_secret': creds['cs']
}
```

### Using the Token

Once you have the token, include it in API requests:

```python
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'X-Infor-MongooseConfig': 'TENANT_DALS'  # For IDO requests
}

response = requests.get(api_url, headers=headers)
```

### Token Expiration

- Tokens expire after **2 hours** (7200 seconds)
- **Always check the response** for 401 Unauthorized errors
- **Regenerate the token** when it expires
- Consider storing token expiration time to proactively refresh

### Quick Reference Script

Location: `scripts/get_token_password_grant.py`

Usage:
```bash
cd scripts
python get_token_password_grant.py
```

This will:
1. Read credentials from your `.ionapi` file
2. Request a new token using password grant
3. Save token to `scripts/access_token.txt`
4. Display expiration time (2 hours)

### Troubleshooting

**401 Unauthorized**: Token expired - regenerate token

**400 Bad Request - Unsupported grant type**: Using client_credentials instead of password grant

**Invalid credentials**: Check that saak/sask values are correct in .ionapi file

**Connection refused**: Verify pu (SSO URL) is correct

### Security Notes

- Never commit access tokens to version control
- Keep `.ionapi` credentials files secure
- Tokens are bearer tokens - anyone with the token has full access
- Regenerate tokens regularly (automatically expires after 2 hours)
- Use `.gitignore` to exclude: `*.ionapi`, `access_token.txt`

## Summary

**The key insight**: Infor ION API service accounts require **password** grant type using the `saak` (username) and `sask` (password) fields from the `.ionapi` file, NOT the client_credentials grant type typically used for service-to-service authentication.

This authentication pattern is specific to Infor's implementation and differs from standard OAuth 2.0 client credentials flow.
