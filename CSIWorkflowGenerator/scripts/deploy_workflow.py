"""Deploy ION workflows via the Process Model REST API.

Usage:
    python scripts/deploy_workflow.py output/CS_Credit_Approval_Clone.json              # Create only
    python scripts/deploy_workflow.py output/CS_Credit_Approval_Clone.json --activate   # Create + activate
    python scripts/deploy_workflow.py --delete WorkflowName                              # Delete
    python scripts/deploy_workflow.py --status WorkflowName                              # Check status
    python scripts/deploy_workflow.py --get WorkflowName                                 # Download JSON
"""
import json
import sys
from pathlib import Path

# Add repo root to path for shared module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from shared.auth import get_auth_headers
from shared.config import get_base_url
from src.http_client import (
    get as http_get,
    post as http_post,
    put as http_put,
    delete as http_delete,
    raise_for_status_with_detail,
)

# ION Process Model Service endpoint
ION_MODEL_URL = get_base_url("IONSERVICES/process/model")
WORKFLOW_URL = f"{ION_MODEL_URL}/v1/workflows"


def create_workflow(workflow_def: dict) -> dict | None:
    """Create a new workflow via API."""
    headers = get_auth_headers()
    name = workflow_def.get("name", "unknown")

    print(f"Creating workflow: {name}")
    print(f"URL: {WORKFLOW_URL}")

    resp = http_post(WORKFLOW_URL, headers=headers, json=workflow_def)
    print(f"Status: {resp.status_code}")

    if resp.status_code == 409 or (
        resp.status_code == 400 and "already exists" in (resp.text or "")
    ):
        print("Workflow already exists. Use --update to delete and recreate.")
        return None

    if resp.text:
        print(f"Response: {resp.text[:500]}")

    raise_for_status_with_detail(resp)
    return resp.json() if resp.text else {"status": "created"}


def activate_workflow(name: str) -> dict:
    """Activate a workflow."""
    headers = get_auth_headers()
    url = f"{WORKFLOW_URL}/{name}/activate"

    print(f"Activating workflow: {name}")
    resp = http_put(url, headers=headers)
    print(f"Status: {resp.status_code}")

    if resp.text:
        print(f"Response: {resp.text[:500]}")

    raise_for_status_with_detail(resp)
    return resp.json() if resp.text else {"status": "activated"}


def deactivate_workflow(name: str) -> dict:
    """Deactivate a workflow."""
    headers = get_auth_headers()
    url = f"{WORKFLOW_URL}/{name}/deactivate"

    print(f"Deactivating workflow: {name}")
    resp = http_put(url, headers=headers)
    print(f"Status: {resp.status_code}")

    raise_for_status_with_detail(resp)
    return resp.json() if resp.text else {"status": "deactivated"}


def delete_workflow(name: str) -> dict:
    """Deactivate (if needed) and delete a workflow."""
    headers = get_auth_headers()

    # Try deactivate first (may fail if already inactive)
    try:
        deactivate_workflow(name)
    except requests.exceptions.HTTPError:
        print("  (Workflow was not active)")

    url = f"{WORKFLOW_URL}/{name}"
    print(f"Deleting workflow: {name}")
    resp = http_delete(url, headers=headers)
    print(f"Status: {resp.status_code}")

    if resp.text:
        print(f"Response: {resp.text[:500]}")

    raise_for_status_with_detail(resp)
    return {"status": "deleted"}


def get_workflow(name: str) -> dict | None:
    """Get a workflow definition."""
    headers = get_auth_headers()
    url = f"{WORKFLOW_URL}/{name}"

    resp = http_get(url, headers=headers)

    if resp.status_code == 404:
        return None

    raise_for_status_with_detail(resp)
    return resp.json()


def print_usage():
    print("Usage:")
    print("  python scripts/deploy_workflow.py <file.json>              # Create")
    print("  python scripts/deploy_workflow.py <file.json> --activate   # Create + activate")
    print("  python scripts/deploy_workflow.py --delete <name>          # Delete")
    print("  python scripts/deploy_workflow.py --status <name>          # Check status")
    print("  python scripts/deploy_workflow.py --get <name>             # Download JSON")


def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        return 1

    print("=" * 60)
    print("ION Workflow Deployment")
    print("=" * 60)

    if "--delete" in args:
        args.remove("--delete")
        if not args:
            print("Error: workflow name required for --delete")
            return 1
        name = args[0]
        try:
            delete_workflow(name)
            print(f"\nWorkflow '{name}' deleted.")
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                print(f"\nWorkflow '{name}' does not exist.")
            else:
                raise
        return 0

    if "--status" in args:
        args.remove("--status")
        if not args:
            print("Error: workflow name required for --status")
            return 1
        name = args[0]
        wf = get_workflow(name)
        if wf:
            print(f"\nWorkflow: {wf.get('name')}")
            print(f"Description: {wf.get('description', 'N/A')}")
            print(f"Last Updated: {wf.get('lastUpdatedOn', 'N/A')}")
            print(f"Last Updated By: {wf.get('lastUpdatedBy', 'N/A')}")
            print(f"Archived: {wf.get('archived', 'N/A')}")
        else:
            print(f"\nWorkflow '{name}' does not exist.")
        return 0

    if "--get" in args:
        args.remove("--get")
        if not args:
            print("Error: workflow name required for --get")
            return 1
        name = args[0]
        wf = get_workflow(name)
        if wf:
            output_path = Path(f"output/{name}.json")
            output_path.parent.mkdir(exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(wf, f, indent=2, ensure_ascii=False)
            print(f"\nDownloaded to: {output_path}")
        else:
            print(f"\nWorkflow '{name}' does not exist.")
        return 0

    # Default: create from file
    do_activate = "--activate" in args
    if do_activate:
        args.remove("--activate")

    if not args:
        print("Error: workflow JSON file required")
        return 1

    json_path = Path(args[0])
    if not json_path.exists():
        print(f"Error: file not found: {json_path}")
        return 1

    with open(json_path, "r", encoding="utf-8") as f:
        workflow_def = json.load(f)

    name = workflow_def.get("name", "unknown")
    print(f"\nFile: {json_path}")
    print(f"Workflow: {name}")
    print(f"Variables: {len(workflow_def.get('variables', []))}")
    print(f"FlowParts: {len(workflow_def.get('sequentialFlow', {}).get('flowParts', []))}")
    print()

    result = create_workflow(workflow_def)
    if result is None:
        return 1

    print(f"\nWorkflow created successfully.")

    if do_activate:
        print()
        activate_workflow(name)
        print(f"\nWorkflow '{name}' is now ACTIVE.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
