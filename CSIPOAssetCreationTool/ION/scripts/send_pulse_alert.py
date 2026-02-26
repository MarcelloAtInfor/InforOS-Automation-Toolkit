"""
Test script to send a Pulse Alert via ION Process Application API.

Usage:
    python send_pulse_alert.py

Prerequisites:
    - Generate token first: python -m shared.auth ION/scripts
"""
import sys
from pathlib import Path

# Add parent to path for shared module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
from shared.auth import get_auth_headers
from shared.config import get_base_url
from shared.tenant import get_users

# Configuration
# LogicalId format requires exactly 2 dots: lid://infor.product.instance
LOGICAL_ID = "lid://infor.rpa.claudecode"
USER_IDENTITY = get_users().get('user1', {}).get('guid', '<USER_GUID>')

# API endpoint (ION Process Application Service)
ION_PROCESS_URL = get_base_url('IONSERVICES/process/application')
ALERT_URL = f"{ION_PROCESS_URL}/v1/pulse/alert/create"


def send_alert(message: str, category: str = "Test", details: dict = None):
    """Send a Pulse alert to the configured user."""
    headers = get_auth_headers()

    payload = {
        "message": message,
        "distribution": [
            {
                "identifier": USER_IDENTITY,
                "type": "USER",
                "sendMail": False
            }
        ],
        "category": category
    }

    if details:
        payload["details"] = details

    params = {"logicalId": LOGICAL_ID}

    print(f"Sending alert to: {ALERT_URL}")
    print(f"LogicalId: {LOGICAL_ID}")
    print(f"Message: {message}")

    response = requests.post(ALERT_URL, headers=headers, json=payload, params=params)

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")

    response.raise_for_status()
    return response.json()


def send_fake_invoice_alert():
    """Send a rich fake invoice alert with lots of properties."""

    message = "URGENT: Invoice requires approval - Acme Corporation $47,832.50"
    category = "AP Invoice"

    # Build a detailed tree structure with fake invoice data
    details = {
        "name": "Invoice Details",
        "properties": [
            {"name": "Invoice Number", "value": "INV-2026-00847", "dataType": "STRING"},
            {"name": "Invoice Date", "value": "2026-01-29", "dataType": "STRING"},
            {"name": "Due Date", "value": "2026-02-28", "dataType": "STRING"},
            {"name": "Total Amount", "value": "47832.50", "dataType": "DECIMAL"},
            {"name": "Currency", "value": "USD", "dataType": "STRING"},
            {"name": "Status", "value": "Pending Approval", "dataType": "STRING"}
        ],
        "subLevels": [
            {
                "name": "Vendor Information",
                "properties": [
                    {"name": "Vendor ID", "value": "V-10042", "dataType": "STRING"},
                    {"name": "Vendor Name", "value": "Acme Corporation", "dataType": "STRING"},
                    {"name": "Contact", "value": "John Smith", "dataType": "STRING"},
                    {"name": "Email", "value": "john.smith@acmecorp.fake", "dataType": "STRING"},
                    {"name": "Phone", "value": "+1 (555) 123-4567", "dataType": "STRING"},
                    {"name": "Payment Terms", "value": "Net 30", "dataType": "STRING"}
                ]
            },
            {
                "name": "Purchase Order",
                "properties": [
                    {"name": "PO Number", "value": "PO-2026-003421", "dataType": "STRING"},
                    {"name": "PO Date", "value": "2026-01-15", "dataType": "STRING"},
                    {"name": "Buyer", "value": "Sarah Johnson", "dataType": "STRING"},
                    {"name": "Department", "value": "Manufacturing", "dataType": "STRING"}
                ]
            },
            {
                "name": "Line Items",
                "subLevels": [
                    {
                        "name": "Line 1",
                        "properties": [
                            {"name": "Item", "value": "Industrial Widget A-500", "dataType": "STRING"},
                            {"name": "Quantity", "value": "250", "dataType": "INTEGER"},
                            {"name": "Unit Price", "value": "125.00", "dataType": "DECIMAL"},
                            {"name": "Extended", "value": "31250.00", "dataType": "DECIMAL"}
                        ]
                    },
                    {
                        "name": "Line 2",
                        "properties": [
                            {"name": "Item", "value": "Precision Gear Set B-200", "dataType": "STRING"},
                            {"name": "Quantity", "value": "75", "dataType": "INTEGER"},
                            {"name": "Unit Price", "value": "198.50", "dataType": "DECIMAL"},
                            {"name": "Extended", "value": "14887.50", "dataType": "DECIMAL"}
                        ]
                    },
                    {
                        "name": "Line 3",
                        "properties": [
                            {"name": "Item", "value": "Shipping & Handling", "dataType": "STRING"},
                            {"name": "Quantity", "value": "1", "dataType": "INTEGER"},
                            {"name": "Unit Price", "value": "1695.00", "dataType": "DECIMAL"},
                            {"name": "Extended", "value": "1695.00", "dataType": "DECIMAL"}
                        ]
                    }
                ]
            },
            {
                "name": "Approval Chain",
                "properties": [
                    {"name": "Requested By", "value": "Mike Wilson", "dataType": "STRING"},
                    {"name": "Current Approver", "value": "YOU", "dataType": "STRING"},
                    {"name": "Next Approver", "value": "Finance Director", "dataType": "STRING"},
                    {"name": "Approval Threshold", "value": "50000.00", "dataType": "DECIMAL"},
                    {"name": "Days Until Due", "value": "30", "dataType": "INTEGER"}
                ]
            }
        ]
    }

    return send_alert(message, category, details)


if __name__ == "__main__":
    print("=" * 60)
    print("Sending FAKE Invoice Alert with Rich Details")
    print("=" * 60)
    result = send_fake_invoice_alert()
    print(f"\nAlert created with ID: {result.get('id')}")
