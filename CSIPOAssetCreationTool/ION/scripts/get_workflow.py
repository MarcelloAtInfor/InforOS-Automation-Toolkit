"""
Download ION Workflow definitions via REST API.

Usage:
    python get_workflow.py                    # Download all reference workflows
    python get_workflow.py WorkflowName       # Download specific workflow

Prerequisites:
    - Generate token first: python -m shared.auth ION/scripts
"""
import sys
import json
from pathlib import Path

# Add parent to path for shared module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from shared.auth import get_auth_headers
from shared.config import get_base_url

# Reference workflows to download
REFERENCE_WORKFLOWS = [
    "CS_Credit_Approval_API",
    "DocumentApprovalWorkflow",
    "CSI_Item_similarity",
    "Send_Presentation",
    "CustomerOrderDiscountWorkflow"
]

# API endpoint (ION Process Model Service)
ION_MODEL_URL = get_base_url('IONSERVICES/process/model')
WORKFLOW_URL = f"{ION_MODEL_URL}/v1/workflows"

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "workflow_definitions"


def get_workflow(name: str) -> dict:
    """Download a workflow definition by name."""
    headers = get_auth_headers()

    url = f"{WORKFLOW_URL}/{name}"
    print(f"Fetching: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        print(f"  Workflow not found: {name}")
        return None

    response.raise_for_status()
    return response.json()


def save_workflow(name: str, definition: dict):
    """Save workflow definition to JSON file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filepath = OUTPUT_DIR / f"{name}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(definition, f, indent=2, ensure_ascii=False)

    print(f"  Saved to: {filepath}")


def list_workflows() -> list:
    """List all available workflows."""
    headers = get_auth_headers()

    url = WORKFLOW_URL
    print(f"Listing workflows from: {url}")

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def download_reference_workflows():
    """Download all reference workflows."""
    print("=" * 60)
    print("Downloading Reference Workflow Definitions")
    print("=" * 60)

    successful = 0
    failed = 0

    for name in REFERENCE_WORKFLOWS:
        print(f"\n[{REFERENCE_WORKFLOWS.index(name) + 1}/{len(REFERENCE_WORKFLOWS)}] {name}")

        try:
            definition = get_workflow(name)
            if definition:
                save_workflow(name, definition)
                successful += 1
            else:
                failed += 1
        except requests.exceptions.HTTPError as e:
            print(f"  Error: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Complete: {successful} downloaded, {failed} failed")
    print("=" * 60)


def download_single_workflow(name: str):
    """Download a specific workflow by name."""
    print(f"Downloading workflow: {name}")

    try:
        definition = get_workflow(name)
        if definition:
            save_workflow(name, definition)
            print("\nSuccess!")
        else:
            print("\nWorkflow not found.")
    except requests.exceptions.HTTPError as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Download specific workflow
        workflow_name = sys.argv[1]
        download_single_workflow(workflow_name)
    else:
        # Download all reference workflows
        download_reference_workflows()
