"""
Start an RPA_Invoice_Notification workflow instance for testing.

Usage:
    python start_rpa_notification_workflow.py                     # Start with test data (SUCCESS)
    python start_rpa_notification_workflow.py --failure           # Start with FAILURE test data
    python start_rpa_notification_workflow.py --custom            # Start with custom values

Prerequisites:
    - Generate token first: python -m shared.auth ION/scripts
    - Create and activate workflow: python create_rpa_notification_workflow.py --activate
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path for shared module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from shared.auth import get_auth_headers
from shared.config import get_base_url
from shared.tenant import get_users

# Configuration
WORKFLOW_NAME = "RPA_Invoice_Notification"
LOGICAL_ID = "lid://infor.rpa.claudecode"
USER_IDENTITY = get_users().get('user1', {}).get('guid', '<USER_GUID>')

# API endpoint (ION Process Application Service)
ION_APP_URL = get_base_url('IONSERVICES/process/application')
START_URL = f"{ION_APP_URL}/v1/workflow/start"


def get_test_data_success() -> dict:
    """Get test data for SUCCESS scenario."""
    return {
        "RecipientUserId": USER_IDENTITY,
        "ProcessingStatus": "SUCCESS",
        "ErrorMessage": "N/A",  # ION requires non-empty values
        "FileName": "TestInvoice_PrecisionTools.pdf",
        "VendorNumber": "DEMO001",
        "VendorName": "Precision Tools Inc.",
        "PONumber": "DP00009000",
        "ItemsCreated": "WIDGET-A, BOLT-M8, GEAR-10",
        "ItemCount": "3"
    }


def get_test_data_failure() -> dict:
    """Get test data for FAILURE scenario."""
    return {
        "RecipientUserId": USER_IDENTITY,
        "ProcessingStatus": "FAILURE",
        "ErrorMessage": "GenAI Agent failed to process invoice: Vendor lookup failed - no matching vendor found for 'Unknown Supplier Co.'",
        "FileName": "FailedInvoice_Unknown.pdf",
        "VendorNumber": "N/A",  # ION requires non-empty values
        "VendorName": "N/A",
        "PONumber": "N/A",
        "ItemsCreated": "N/A",
        "ItemCount": "0"
    }


def build_created_assets_structure(test_data: dict) -> dict:
    """
    Build the CreatedAssets tree structure for the workflow.

    The tree has 3 nodes: VendorInfo, POInfo, ItemsInfo
    Each node contains fields that map to workflow variables.
    """
    return {
        "name": "CreatedAssets",
        "subStructures": [
            {
                "name": "VendorInfo",
                "fields": [
                    {"name": "VendorNumber", "value": test_data["VendorNumber"], "dataType": "STRING"},
                    {"name": "VendorName", "value": test_data["VendorName"], "dataType": "STRING"}
                ]
            },
            {
                "name": "POInfo",
                "fields": [
                    {"name": "PONumber", "value": test_data["PONumber"], "dataType": "STRING"}
                ]
            },
            {
                "name": "ItemsInfo",
                "fields": [
                    {"name": "ItemCount", "value": test_data["ItemCount"], "dataType": "STRING"},
                    {"name": "ItemsCreated", "value": test_data["ItemsCreated"], "dataType": "STRING"}
                ]
            }
        ]
    }


def start_workflow(test_data: dict) -> dict:
    """Start a workflow instance with the given test data."""
    headers = get_auth_headers()

    # Build instance name with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    instance_name = f"RPA_Test_{timestamp}"

    # Build input variables with dataType (CRITICAL for ION API)
    input_variables = [
        {"name": key, "value": value, "dataType": "STRING"}
        for key, value in test_data.items()
    ]

    # Build the CreatedAssets structure for tree display
    created_assets = build_created_assets_structure(test_data)

    payload = {
        "workflowName": WORKFLOW_NAME,
        "instanceName": instance_name,
        "inputVariables": input_variables,
        "inputStructures": [created_assets]
    }

    params = {"logicalId": LOGICAL_ID}

    print(f"Starting workflow: {WORKFLOW_NAME}")
    print(f"Instance name: {instance_name}")
    print(f"URL: {START_URL}")
    print(f"\nTest Data:")
    for key, value in test_data.items():
        display_value = value if len(str(value)) < 50 else f"{value[:47]}..."
        print(f"  {key}: {display_value}")

    response = requests.post(START_URL, headers=headers, json=payload, params=params)

    print(f"\nStatus: {response.status_code}")
    if response.text:
        print(f"Response: {response.text}")

    response.raise_for_status()
    return response.json() if response.text else {"status": "started", "instance": instance_name}


if __name__ == "__main__":
    print("=" * 60)
    print("RPA Invoice Notification Workflow Test Starter")
    print("=" * 60)

    if "--failure" in sys.argv:
        # Test with FAILURE data
        print("\nStarting workflow with FAILURE test data...")
        print("-" * 40)
        test_data = get_test_data_failure()

    elif "--custom" in sys.argv:
        # Interactive custom values
        print("\nEnter custom values (press Enter for defaults):")
        print("-" * 40)

        defaults = get_test_data_success()
        test_data = {}

        for key, default_value in defaults.items():
            user_input = input(f"  {key} [{default_value}]: ").strip()
            test_data[key] = user_input if user_input else default_value

    else:
        # Test with SUCCESS data
        print("\nStarting workflow with SUCCESS test data...")
        print("-" * 40)
        test_data = get_test_data_success()

    try:
        result = start_workflow(test_data)
        print(f"\nSuccess! Workflow instance started.")
        print(f"Check your Pulse inbox for the notification.")
        print(f"\nVerification steps:")
        print(f"  1. Open Infor OS Pulse inbox")
        print(f"  2. Look for notification: 'RPA Invoice Processing {test_data['ProcessingStatus']}: {test_data['FileName']}'")
        print(f"  3. Verify Created Assets tree shows vendor/PO/items info")
        print(f"  4. Test drillback links for PO and Vendor (if SUCCESS)")

    except requests.exceptions.HTTPError as e:
        error_text = str(e)
        if "404" in error_text:
            print(f"\nError: Workflow '{WORKFLOW_NAME}' not found or not active.")
            print("Make sure to run: python create_rpa_notification_workflow.py --activate")
        elif "400" in error_text:
            print(f"\nError 400 - Bad Request. Check the workflow definition.")
            print("Try deleting and recreating: python create_rpa_notification_workflow.py --delete")
        else:
            print(f"\nError: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response body: {e.response.text}")
