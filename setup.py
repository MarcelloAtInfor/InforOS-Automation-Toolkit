#!/usr/bin/env python3
"""
Interactive setup script for Infor OS Automation Toolkit.

Guides the user through creating a tenant_config.json file:
  1. Locate and validate .ionapi credentials
  2. Test API connectivity
  3. Discover available SyteLine sites
  4. Add approver users (resolve email -> IFS GUID)
  5. Extract service account from an exported ION workflow
  6. Configure logical ID
  7. Write tenant_config.json

Usage:
    python setup.py
"""
import json
import os
import sys
from pathlib import Path

# Ensure shared/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_header(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def _print_step(n, total, desc):
    print(f"\n--- Step {n}/{total}: {desc} ---\n")


def _ask(prompt, default=None):
    """Prompt user for input with optional default."""
    if default:
        raw = input(f"{prompt} [{default}]: ").strip()
        return raw if raw else default
    while True:
        raw = input(f"{prompt}: ").strip()
        if raw:
            return raw
        print("  (input required)")


def _ask_yes_no(prompt, default=True):
    """Prompt user for yes/no."""
    suffix = "[Y/n]" if default else "[y/N]"
    raw = input(f"{prompt} {suffix}: ").strip().lower()
    if not raw:
        return default
    return raw in ('y', 'yes')


TOTAL_STEPS = 7


# ---------------------------------------------------------------------------
# Step 1: Locate .ionapi credentials
# ---------------------------------------------------------------------------

def step_locate_ionapi():
    _print_step(1, TOTAL_STEPS, "Locate .ionapi credentials")

    # Check env var first
    env_path = os.environ.get('IONAPI_FILE')
    if env_path and Path(env_path).exists():
        print(f"  Found via IONAPI_FILE env var: {env_path}")
        if _ask_yes_no("  Use this file?"):
            return Path(env_path)

    # Check CWD
    cwd_path = Path.cwd() / '.ionapi'
    if cwd_path.exists():
        print(f"  Found .ionapi in current directory: {cwd_path}")
        if _ask_yes_no("  Use this file?"):
            return cwd_path

    # Ask user
    print("  No .ionapi file found automatically.")
    print("  You can get one from Infor OS Portal:")
    print("    API Gateway > Authorized Apps > Backend Service")
    print("    > Create Service Account > Download Credentials\n")
    while True:
        path_str = _ask("  Enter path to your .ionapi file")
        p = Path(path_str).expanduser().resolve()
        if p.exists():
            return p
        print(f"  File not found: {p}")


# ---------------------------------------------------------------------------
# Step 2: Validate connectivity
# ---------------------------------------------------------------------------

def step_validate_connectivity(ionapi_path):
    _print_step(2, TOTAL_STEPS, "Validate API connectivity")

    # Temporarily set env var so shared.auth can find it
    os.environ['IONAPI_FILE'] = str(ionapi_path)

    from shared.auth import get_credentials, request_token
    from shared.config import get_tenant_id, get_base_url

    print(f"  Loading credentials from: {ionapi_path}")
    creds = get_credentials()
    print(f"  Tenant ID: {creds['ti']}")
    print(f"  ION API URL: {creds.get('iu', '(not set)')}")

    print("\n  Requesting OAuth token...")
    try:
        token = request_token()
        print("\n  Connectivity OK!")
        return creds, token
    except Exception as e:
        print(f"\n  ERROR: Could not obtain token: {e}")
        print("  Check your .ionapi file and network connectivity.")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Step 3: Discover SyteLine sites
# ---------------------------------------------------------------------------

def step_discover_sites(token):
    _print_step(3, TOTAL_STEPS, "Discover SyteLine sites")

    import requests
    from shared.config import IDO_URL, get_mongoose_config

    # Use default mongoose config for initial connection
    default_config = get_mongoose_config()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'X-Infor-MongooseConfig': default_config,
    }

    print(f"  Querying SLSites IDO (using config: {default_config})...")
    try:
        url = f"{IDO_URL()}/load/SLSites"
        params = {"properties": "Site,SiteGroup,SiteDesc", "recordCap": 100}
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        items = resp.json().get("Items", [])
    except Exception as e:
        print(f"  WARNING: Could not auto-discover sites: {e}")
        print("  You can enter your site manually.\n")
        items = []

    if items:
        print(f"  Found {len(items)} site(s):\n")
        for i, item in enumerate(items, 1):
            props = {p['Name']: p.get('Value', '') for p in item.get('Properties', [])}
            site = props.get('Site', '?')
            desc = props.get('SiteDesc', '')
            print(f"    {i}. {site} — {desc}")

        print()
        choice = _ask("  Enter site number or type site name manually", "1")
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            idx = int(choice) - 1
            props = {p['Name']: p.get('Value', '') for p in items[idx].get('Properties', [])}
            site = props.get('Site', '')
        else:
            site = choice
    else:
        # Suggest the default mongoose config as a starting point
        site = _ask("  Enter your SyteLine site identifier", default_config)

    # The MongooseConfig value used in API headers is typically the full site string
    # (e.g. "TENANTID_DEM_DALS"). Confirm with user.
    print(f"\n  Selected site: {site}")
    print("  Note: This is the value used in the X-Infor-MongooseConfig header.")
    print("  It is typically your tenant ID + suffix (e.g. TENANTID_DEM_DALS).")
    site = _ask("  Confirm or edit site value", site)
    return site


# ---------------------------------------------------------------------------
# Step 4: Add approver users
# ---------------------------------------------------------------------------

def step_add_users(token, base_url):
    _print_step(4, TOTAL_STEPS, "Add approver users (optional)")

    import requests

    users = {}
    print("  Add users who will appear in workflow approvals/notifications.")
    print("  Enter email addresses to resolve their IFS user GUIDs.")
    print("  Press Enter with no email when done.\n")

    ifs_url = f"{base_url}/ifsservice/usermgt/v2/users/search/identity2byemail"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    while True:
        email = input("  Email (blank to finish): ").strip()
        if not email:
            break

        # Resolve email to GUID via IFS API
        print(f"    Resolving {email}...")
        try:
            resp = requests.post(
                ifs_url,
                headers=headers,
                json={"email": email},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            user_list = data.get("response", {}).get("userlist", [])
            if user_list:
                guid = user_list[0].get("id", "")
                display_name = user_list[0].get("displayName", "")
                if not display_name:
                    # Try other common fields
                    display_name = user_list[0].get("firstName", "") + " " + user_list[0].get("lastName", "")
                    display_name = display_name.strip()
                print(f"    Found: {display_name} ({guid})")
            else:
                print(f"    WARNING: No user found for {email}")
                guid = _ask("    Enter GUID manually (or 'skip' to skip)", "skip")
                if guid == "skip":
                    continue
                display_name = _ask("    Enter display name")
        except Exception as e:
            print(f"    WARNING: IFS API error: {e}")
            guid = _ask("    Enter GUID manually (or 'skip' to skip)", "skip")
            if guid == "skip":
                continue
            display_name = _ask("    Enter display name")

        # Generate a user key from the name
        suggested_key = display_name.split()[0].lower() if display_name else email.split("@")[0]
        key = _ask(f"    User key for config", suggested_key)

        if not display_name:
            display_name = _ask("    Display name")

        users[key] = {
            "guid": guid,
            "name": display_name,
            "email": email,
        }
        print(f"    Added: {key} -> {display_name}\n")

    if not users:
        print("  No users added. You can edit tenant_config.json later.")

    return users


# ---------------------------------------------------------------------------
# Step 5: Extract service account from ION workflow export
# ---------------------------------------------------------------------------

def step_service_account():
    _print_step(5, TOTAL_STEPS, "Extract service account token")

    print("  The service account token is an encrypted string embedded in")
    print("  ION workflow definitions. To extract it:")
    print("    1. Open ION Desk > Connect > Workflows")
    print("    2. Export any active workflow as JSON")
    print("    3. Provide the path to the exported JSON file\n")

    while True:
        choice = _ask("  Enter path to exported workflow JSON (or 'skip' to skip)", "skip")
        if choice == "skip":
            print("  Skipped. You'll need to add service_account to tenant_config.json manually.")
            return "<YOUR_SERVICE_ACCOUNT>"

        p = Path(choice).expanduser().resolve()
        if not p.exists():
            print(f"  File not found: {p}")
            continue

        try:
            # Use the same extraction logic as CSIWorkflowGenerator
            with open(p, 'r', encoding='utf-8') as f:
                ref = json.load(f)

            def _find_sa(flowparts):
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

            sa = _find_sa(ref.get("sequentialFlow", {}).get("flowParts", []))
            if sa:
                print(f"  Found service account token ({len(sa)} chars)")
                print(f"  Preview: {sa[:40]}...")
                return sa
            else:
                print("  WARNING: No serviceAccount found in this workflow.")
                print("  The workflow must contain at least one ION API activity.\n")
        except json.JSONDecodeError:
            print("  ERROR: File is not valid JSON.\n")
        except Exception as e:
            print(f"  ERROR: {e}\n")


# ---------------------------------------------------------------------------
# Step 6: Configure logical ID
# ---------------------------------------------------------------------------

def step_logical_id(site):
    _print_step(6, TOTAL_STEPS, "Configure ION logical ID")

    # Derive a sensible default suffix from the site name
    # e.g. "TENANTID_DEM_DALS" -> "dals"
    parts = site.lower().split("_")
    default_suffix = parts[-1] if parts else "default"

    print("  The ION logical ID identifies your SyteLine instance in workflows.")
    print(f"  Format: lid://infor.syteline.csi/<suffix>\n")

    suffix = _ask("  Enter logical ID suffix", default_suffix)
    logical_id = f"lid://infor.syteline.csi/{suffix}"
    print(f"  Logical ID: {logical_id}")
    return logical_id


# ---------------------------------------------------------------------------
# Step 7: Write tenant_config.json
# ---------------------------------------------------------------------------

def step_write_config(site, logical_id, service_account, users):
    _print_step(7, TOTAL_STEPS, "Write tenant_config.json")

    config = {
        "site": site,
        "logical_id": logical_id,
        "service_account": service_account,
        "users": users,
    }

    out_path = Path(__file__).resolve().parent / "tenant_config.json"
    print(f"  Writing to: {out_path}\n")
    print(json.dumps(config, indent=2))

    if out_path.exists():
        print(f"\n  WARNING: {out_path.name} already exists.")
        if not _ask_yes_no("  Overwrite?"):
            alt = _ask("  Enter alternative filename", "tenant_config_new.json")
            out_path = out_path.parent / alt

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    print(f"\n  Config written to: {out_path}")
    print("  This file is gitignored and will NOT be committed.")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    _print_header("Infor OS Automation Toolkit — Setup")
    print("This script will create your tenant_config.json file.")
    print("You'll need:")
    print("  - A .ionapi credentials file (from Infor OS Portal)")
    print("  - (Optional) An exported ION workflow JSON for service account")
    print("  - (Optional) Email addresses of workflow approvers")

    # Step 1: Locate credentials
    ionapi_path = step_locate_ionapi()

    # Step 2: Validate connectivity
    creds, token = step_validate_connectivity(ionapi_path)

    # Step 3: Discover sites
    site = step_discover_sites(token)

    # Step 4: Add users
    from shared.config import get_base_url
    base_url = get_base_url()
    users = step_add_users(token, base_url)

    # Step 5: Service account
    service_account = step_service_account()

    # Step 6: Logical ID
    logical_id = step_logical_id(site)

    # Step 7: Write config
    config_path = step_write_config(site, logical_id, service_account, users)

    _print_header("Setup Complete!")
    print(f"  Config file: {config_path}")
    print(f"  Credentials: {ionapi_path}")
    print()
    print("  Next steps:")
    print("    - Review tenant_config.json and edit if needed")
    print("    - Try running a project (see each project's README)")
    print("    - Run 'python -c \"from shared.tenant import get_site; print(get_site())\"' to verify")
    print()


if __name__ == '__main__':
    main()
