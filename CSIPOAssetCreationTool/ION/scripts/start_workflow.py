"""
Start an ION Workflow instance via REST API.

Usage:
    python start_workflow.py                              # Start with defaults
    python start_workflow.py "Custom message here"        # Start with custom message
    python start_workflow.py --list                       # List active workflows

Prerequisites:
    - Generate token first: python -m shared.auth ION/scripts
    - Create and activate workflow: python create_workflow.py --activate
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path for shared module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from shared.auth import get_auth_headers
from shared.config import get_base_url

# Configuration
WORKFLOW_NAME = "ClaudeCode_Test_Workflow"
LOGICAL_ID = "lid://infor.rpa.claudecode"

# API endpoint (ION Process Application Service)
ION_APP_URL = get_base_url('IONSERVICES/process/application')
START_URL = f"{ION_APP_URL}/v1/workflow/start"
INTERFACE_URL = f"{ION_APP_URL}/v1/workflow/interface"


def start_workflow(message: str = None, sender: str = "Claude Code") -> dict:
    """Start a workflow instance."""
    headers = get_auth_headers()

    if message is None:
        message = f"Hello from Claude Code! Timestamp: {datetime.now().isoformat()}"

    # Build instance name with timestamp
    instance_name = f"CC_Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    payload = {
        "workflowName": WORKFLOW_NAME,
        "instanceName": instance_name,
        "inputVariables": [
            {"name": "InputMessage", "value": message, "dataType": "STRING"},
            {"name": "SenderName", "value": sender, "dataType": "STRING"}
        ]
    }

    params = {"logicalId": LOGICAL_ID}

    print(f"Starting workflow: {WORKFLOW_NAME}")
    print(f"Instance name: {instance_name}")
    print(f"URL: {START_URL}")
    print(f"Message: {message}")
    print(f"Sender: {sender}")

    response = requests.post(START_URL, headers=headers, json=payload, params=params)

    print(f"\nStatus: {response.status_code}")
    if response.text:
        print(f"Response: {response.text}")

    response.raise_for_status()
    return response.json() if response.text else {"status": "started", "instance": instance_name}


def list_active_workflows() -> list:
    """List active workflows that can receive instances."""
    headers = get_auth_headers()

    print(f"Listing active workflows from: {INTERFACE_URL}")

    response = requests.get(INTERFACE_URL, headers=headers)

    print(f"Status: {response.status_code}")

    response.raise_for_status()
    return response.json()


def start_any_workflow(workflow_name: str, variables: dict = None) -> dict:
    """Start any workflow by name with optional variables."""
    headers = get_auth_headers()

    instance_name = f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    payload = {
        "workflowName": workflow_name,
        "instanceName": instance_name
    }

    if variables:
        payload["inputVariables"] = [
            {"name": k, "value": v} for k, v in variables.items()
        ]

    params = {"logicalId": LOGICAL_ID}

    print(f"Starting workflow: {workflow_name}")
    print(f"Instance name: {instance_name}")

    response = requests.post(START_URL, headers=headers, json=payload, params=params)

    print(f"Status: {response.status_code}")
    if response.text:
        print(f"Response: {response.text}")

    response.raise_for_status()
    return response.json() if response.text else {"status": "started"}


if __name__ == "__main__":
    print("=" * 60)
    print("ION Workflow Instance Starter")
    print("=" * 60)

    if "--list" in sys.argv:
        # List active workflows
        print("\nActive Workflows:")
        print("-" * 40)

        try:
            workflows = list_active_workflows()
            if isinstance(workflows, list):
                for wf in workflows:
                    if isinstance(wf, dict):
                        print(f"  - {wf.get('name', wf)}")
                    else:
                        print(f"  - {wf}")
            else:
                print(workflows)
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")

    elif "--workflow" in sys.argv:
        # Start a specific workflow
        idx = sys.argv.index("--workflow")
        if idx + 1 < len(sys.argv):
            wf_name = sys.argv[idx + 1]
            print(f"\nStarting workflow: {wf_name}")
            try:
                result = start_any_workflow(wf_name)
                print(f"\nResult: {result}")
            except requests.exceptions.HTTPError as e:
                print(f"\nError: {e}")
        else:
            print("Usage: python start_workflow.py --workflow WorkflowName")

    else:
        # Start the test workflow
        message = None
        if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
            message = sys.argv[1]

        print(f"\nStarting test workflow: {WORKFLOW_NAME}")
        print("-" * 40)

        try:
            result = start_workflow(message=message)
            print(f"\nSuccess! Instance started.")
            print(f"Check your Pulse inbox for the notification.")
        except requests.exceptions.HTTPError as e:
            error_text = str(e)
            if "404" in error_text:
                print(f"\nError: Workflow '{WORKFLOW_NAME}' not found or not active.")
                print("Make sure to run: python create_workflow.py --activate")
            else:
                print(f"\nError: {e}")
