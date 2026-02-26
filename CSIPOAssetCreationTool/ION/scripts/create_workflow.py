"""
Create and activate an ION Workflow via REST API.

Usage:
    python create_workflow.py                 # Create test workflow
    python create_workflow.py --activate      # Create and activate
    python create_workflow.py --delete        # Delete test workflow

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
from shared.tenant import get_users

# Configuration
WORKFLOW_NAME = "ClaudeCode_Test_Workflow"
USER_IDENTITY = get_users().get('user1', {}).get('guid', '<USER_GUID>')

# API endpoint (ION Process Model Service)
ION_MODEL_URL = get_base_url('IONSERVICES/process/model')
WORKFLOW_URL = f"{ION_MODEL_URL}/v1/workflows"


def build_test_workflow() -> dict:
    """
    Build a simple test workflow with a UserTask notification.

    Based on actual workflow structure from DocumentApprovalWorkflow.
    Key findings:
    - _type values are lowercase (usertask, ifthenelse, ionapi, scripting)
    - Variables use workflowInput: true instead of direction: "INPUT"
    - UserTask uses userTaskType, taskMessage, and workflowDistributionItems
    """
    workflow = {
        "name": WORKFLOW_NAME,
        "description": "Test workflow created via Claude Code REST API. Sends a notification with a custom message.",
        "variables": [
            {
                "name": "InputMessage",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            },
            {
                "name": "SenderName",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            }
        ],
        "views": [],
        "trees": [],
        "sequentialFlow": {
            "sequenceNumber": 0,
            "flowParts": [
                {
                    "_type": "usertask",
                    "sequenceNumber": 1,
                    "name": "SendNotification",
                    "parallel": False,
                    "priority": "Medium",
                    "taskMessage": "Message from [SenderName]: [InputMessage]",
                    "taskActionType": "StandardAction",
                    "userTaskType": "NOTIFICATION",
                    "maxEscalationLevel": 1,
                    "distributionComplexity": "Simple",
                    "propagateNotes": False,
                    "parameters": [
                        {
                            "variable": "InputMessage",
                            "label": "Message",
                            "readOnly": True,
                            "sequenceNumber": 0,
                            "completionProperty": "NOT_APPLICABLE",
                            "labels": []
                        },
                        {
                            "variable": "SenderName",
                            "label": "Sender",
                            "readOnly": True,
                            "sequenceNumber": 1,
                            "completionProperty": "NOT_APPLICABLE",
                            "labels": []
                        }
                    ],
                    "workflowDistributionItems": [
                        {
                            "name": USER_IDENTITY,
                            "distributionType": "USER",
                            "description": "Test User",
                            "sendEmail": False
                        }
                    ],
                    "taskMessages": [],
                    "actionButtons": [],
                    "workflowDecisionTables": [],
                    "userTaskEscalations": []
                }
            ]
        }
    }

    return workflow


def create_workflow(workflow_def: dict) -> dict:
    """Create a new workflow via API."""
    headers = get_auth_headers()

    print(f"Creating workflow: {workflow_def['name']}")
    print(f"URL: {WORKFLOW_URL}")

    response = requests.post(WORKFLOW_URL, headers=headers, json=workflow_def)

    print(f"Status: {response.status_code}")

    if response.status_code == 409:
        print("Workflow already exists. Use --delete first to recreate.")
        return None

    if response.text:
        print(f"Response: {response.text[:500]}")

    response.raise_for_status()
    return response.json() if response.text else {"status": "created"}


def activate_workflow(name: str) -> dict:
    """Activate a workflow."""
    headers = get_auth_headers()

    url = f"{WORKFLOW_URL}/{name}/activate"
    print(f"\nActivating workflow: {name}")
    print(f"URL: {url}")

    response = requests.put(url, headers=headers)

    print(f"Status: {response.status_code}")
    if response.text:
        print(f"Response: {response.text[:500]}")

    response.raise_for_status()
    return response.json() if response.text else {"status": "activated"}


def deactivate_workflow(name: str) -> dict:
    """Deactivate a workflow."""
    headers = get_auth_headers()

    url = f"{WORKFLOW_URL}/{name}/deactivate"
    print(f"\nDeactivating workflow: {name}")

    response = requests.put(url, headers=headers)

    print(f"Status: {response.status_code}")
    if response.text:
        print(f"Response: {response.text[:500]}")

    response.raise_for_status()
    return response.json() if response.text else {"status": "deactivated"}


def delete_workflow(name: str) -> dict:
    """Delete a workflow."""
    headers = get_auth_headers()

    url = f"{WORKFLOW_URL}/{name}"
    print(f"Deleting workflow: {name}")
    print(f"URL: {url}")

    # Try to deactivate first (may fail if already inactive)
    try:
        deactivate_workflow(name)
    except requests.exceptions.HTTPError:
        print("  (Workflow was not active)")

    response = requests.delete(url, headers=headers)

    print(f"Status: {response.status_code}")
    if response.text:
        print(f"Response: {response.text[:500]}")

    response.raise_for_status()
    return {"status": "deleted"}


def get_workflow(name: str) -> dict:
    """Get a workflow definition."""
    headers = get_auth_headers()

    url = f"{WORKFLOW_URL}/{name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("=" * 60)
    print("ION Workflow Creation via REST API")
    print("=" * 60)

    if "--delete" in sys.argv:
        # Delete the test workflow
        try:
            delete_workflow(WORKFLOW_NAME)
            print("\nWorkflow deleted successfully.")
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                print("\nWorkflow does not exist.")
            else:
                raise

    elif "--activate" in sys.argv:
        # Create and activate
        workflow_def = build_test_workflow()

        print("\nWorkflow Definition:")
        print(json.dumps(workflow_def, indent=2))

        result = create_workflow(workflow_def)
        if result:
            print(f"\nWorkflow created: {result}")
            activate_workflow(WORKFLOW_NAME)
            print("\nWorkflow is now ACTIVE and ready to receive instances.")

    elif "--status" in sys.argv:
        # Check if workflow exists
        workflow = get_workflow(WORKFLOW_NAME)
        if workflow:
            print(f"\nWorkflow exists:")
            print(f"  Name: {workflow.get('name')}")
            print(f"  Status: {workflow.get('status', 'unknown')}")
            print(f"  Description: {workflow.get('description', 'N/A')}")
        else:
            print(f"\nWorkflow '{WORKFLOW_NAME}' does not exist.")

    else:
        # Just create (don't activate)
        workflow_def = build_test_workflow()

        print("\nWorkflow Definition:")
        print(json.dumps(workflow_def, indent=2))

        result = create_workflow(workflow_def)
        if result:
            print(f"\nWorkflow created: {result}")
            print("\nTo activate, run: python create_workflow.py --activate")
            print("To delete, run: python create_workflow.py --delete")
