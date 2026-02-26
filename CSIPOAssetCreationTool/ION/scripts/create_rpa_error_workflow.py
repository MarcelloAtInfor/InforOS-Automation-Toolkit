"""
Create and activate the RPA_Error_Notification ION Workflow.

This workflow sends a notification when an RPA workflow encounters an unhandled exception.
It includes exception details, stack trace, and context information. Higher priority than
normal invoice notifications.

Usage:
    python create_rpa_error_workflow.py                 # Create workflow
    python create_rpa_error_workflow.py --activate      # Create and activate
    python create_rpa_error_workflow.py --delete        # Delete workflow
    python create_rpa_error_workflow.py --status        # Check workflow status

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
WORKFLOW_NAME = "RPA_Error_Notification"
USER_IDENTITY = get_users().get('user1', {}).get('guid', '<USER_GUID>')

# API endpoint (ION Process Model Service)
ION_MODEL_URL = get_base_url('IONSERVICES/process/model')
WORKFLOW_URL = f"{ION_MODEL_URL}/v1/workflows"


def build_rpa_error_workflow() -> dict:
    """
    Build the RPA Error Notification workflow.

    Features:
    - 6 input variables for error details
    - No drillback views (no SyteLine assets to link to)
    - Tree structure for exception and context info
    - High priority notification task
    """
    workflow = {
        "name": WORKFLOW_NAME,
        "description": "RPA Critical Error Notification - Sends notification when RPA workflow encounters an unhandled exception.",

        # Workflow Variables (all inputs from RPA)
        "variables": [
            {
                "name": "RecipientUserId",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            },
            {
                "name": "ProcessingStatus",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            },
            {
                "name": "FileName",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            },
            {
                "name": "ExceptionMessage",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            },
            {
                "name": "StackTrace",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            },
            {
                "name": "Timestamp",
                "dataType": "STRING",
                "workflowInput": True,
                "workflowOutput": False,
                "useValue": False
            }
        ],

        # No drillback views - there's no vendor/PO to link to for errors
        "views": [],

        # Tree Structure for Error Details
        "trees": [
            {
                "_type": "tree",
                "name": "ErrorDetails",
                "label": "Error Details",
                "sequence": 0,
                "treeLabels": [],
                "treeElementChildren": [
                    {
                        "_type": "node",
                        "name": "ExceptionInfo",
                        "label": "Exception",
                        "sequence": 0,
                        "treeLabels": [],
                        "treeElementChildren": [
                            {
                                "_type": "field",
                                "name": "ExceptionMessage",
                                "label": "Message",
                                "sequence": 0,
                                "treeLabels": [],
                                "dataType": "STRING"
                            },
                            {
                                "_type": "field",
                                "name": "StackTrace",
                                "label": "Stack Trace",
                                "sequence": 1,
                                "treeLabels": [],
                                "dataType": "STRING"
                            }
                        ]
                    },
                    {
                        "_type": "node",
                        "name": "ContextInfo",
                        "label": "Context",
                        "sequence": 1,
                        "treeLabels": [],
                        "treeElementChildren": [
                            {
                                "_type": "field",
                                "name": "FileName",
                                "label": "File Being Processed",
                                "sequence": 0,
                                "treeLabels": [],
                                "dataType": "STRING"
                            },
                            {
                                "_type": "field",
                                "name": "Timestamp",
                                "label": "Error Time",
                                "sequence": 1,
                                "treeLabels": [],
                                "dataType": "STRING"
                            }
                        ]
                    }
                ]
            }
        ],

        # Sequential Flow with High Priority Notification Task
        "sequentialFlow": {
            "sequenceNumber": 0,
            "flowParts": [
                {
                    "_type": "usertask",
                    "sequenceNumber": 1,
                    "name": "SendErrorNotification",
                    "parallel": False,
                    "priority": "High",  # Higher priority than normal notifications
                    "taskMessage": "RPA CRITICAL ERROR: [FileName]",
                    "taskActionType": "StandardAction",
                    "userTaskType": "NOTIFICATION",
                    "maxEscalationLevel": 1,
                    "distributionComplexity": "Simple",
                    "propagateNotes": False,
                    "parameters": [
                        {
                            "variable": "ProcessingStatus",
                            "label": "Status",
                            "readOnly": True,
                            "sequenceNumber": 0,
                            "completionProperty": "NOT_APPLICABLE",
                            "labels": []
                        },
                        {
                            "variable": "FileName",
                            "label": "File Being Processed",
                            "readOnly": True,
                            "sequenceNumber": 1,
                            "completionProperty": "NOT_APPLICABLE",
                            "labels": []
                        },
                        {
                            "variable": "ExceptionMessage",
                            "label": "Exception",
                            "readOnly": True,
                            "sequenceNumber": 2,
                            "completionProperty": "NOT_APPLICABLE",
                            "labels": []
                        },
                        {
                            "tree": "ErrorDetails",
                            "label": "Error Details",
                            "readOnly": True,
                            "sequenceNumber": 3,
                            "completionProperty": "NOT_APPLICABLE",
                            "labels": []
                        }
                    ],
                    "workflowDistributionItems": [
                        {
                            "name": USER_IDENTITY,
                            "distributionType": "USER",
                            "description": "RPA Error Notification Recipient",
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


def save_workflow_definition(workflow: dict, filename: str = None):
    """Save workflow definition to JSON file."""
    if filename is None:
        filename = f"{workflow['name']}.json"

    output_dir = Path(__file__).parent.parent / "workflow_definitions"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\nWorkflow definition saved to: {output_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("RPA Error Notification Workflow Creator")
    print("=" * 60)

    if "--delete" in sys.argv:
        # Delete the workflow
        try:
            delete_workflow(WORKFLOW_NAME)
            print("\nWorkflow deleted successfully.")
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                print("\nWorkflow does not exist.")
            else:
                raise

    elif "--status" in sys.argv:
        # Check if workflow exists
        workflow = get_workflow(WORKFLOW_NAME)
        if workflow:
            print(f"\nWorkflow exists:")
            print(f"  Name: {workflow.get('name')}")
            print(f"  Status: {workflow.get('status', 'unknown')}")
            print(f"  Description: {workflow.get('description', 'N/A')}")
            print(f"  Variables: {len(workflow.get('variables', []))}")
            print(f"  Views: {len(workflow.get('views', []))}")
            print(f"  Trees: {len(workflow.get('trees', []))}")
            if workflow.get('activationDate'):
                print(f"  Activated: {workflow.get('activationDate')}")
        else:
            print(f"\nWorkflow '{WORKFLOW_NAME}' does not exist.")

    elif "--activate" in sys.argv:
        # Create and activate
        workflow_def = build_rpa_error_workflow()

        print("\nWorkflow Definition Summary:")
        print(f"  Name: {workflow_def['name']}")
        print(f"  Variables: {len(workflow_def['variables'])}")
        print(f"  Views: {len(workflow_def['views'])}")
        print(f"  Trees: {len(workflow_def['trees'])}")
        print(f"  Flow Parts: {len(workflow_def['sequentialFlow']['flowParts'])}")

        result = create_workflow(workflow_def)
        if result:
            print(f"\nWorkflow created: {result}")

            # Save the definition
            save_workflow_definition(workflow_def)

            # Activate
            activate_workflow(WORKFLOW_NAME)
            print("\nWorkflow is now ACTIVE and ready to receive instances.")
            print("\nTo test, you can trigger an RPA error or use the ION API directly.")

    elif "--save-only" in sys.argv:
        # Just save the definition without creating
        workflow_def = build_rpa_error_workflow()
        save_workflow_definition(workflow_def)
        print("\nDefinition saved. Use --activate to create and activate.")

    else:
        # Just create (don't activate)
        workflow_def = build_rpa_error_workflow()

        print("\nWorkflow Definition:")
        print(json.dumps(workflow_def, indent=2))

        result = create_workflow(workflow_def)
        if result:
            print(f"\nWorkflow created: {result}")
            save_workflow_definition(workflow_def)
            print("\nTo activate, run: python create_rpa_error_workflow.py --activate")
            print("To delete, run: python create_rpa_error_workflow.py --delete")
