"""
Test the InvoiceAutomation_Agent_v2 via Chat API with sample invoice data
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CHAT_URL

# Load test invoice data
test_data_path = Path(__file__).parent / "test_invoice_data.json"
with open(test_data_path, 'r') as f:
    invoice_data = json.load(f)

# Chat API endpoint
chat_url = f"{GENAI_CHAT_URL()}/api/v1/chat/sync"

# Agent logical ID
logical_id = "lid://infor.syteline.invoice-automation-v2"

headers = get_auth_headers()
headers['x-infor-logicalidprefix'] = logical_id

# Create prompt with invoice data
prompt = f"""Process this invoice data:

{json.dumps(invoice_data, indent=2)}

Please create the vendor, items, purchase order, and PO lines in SyteLine."""

request_body = {
    "prompt": prompt,
    "session": None
}

print("Testing InvoiceAutomation_Agent_v2")
print("=" * 60)
print(f"POST {chat_url}")
print(f"Logical ID: {logical_id}\n")
print("Invoice Data:")
print("-" * 60)
print(json.dumps(invoice_data, indent=2))
print("-" * 60)
print()

# Make the request
response = requests.post(chat_url, headers=headers, json=request_body)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    chat_response = response.json()

    print("[SUCCESS] Agent executed!\n")

    # Extract the response
    message = chat_response.get('message', '')
    session = chat_response.get('session', '')

    print("Agent Response:")
    print("-" * 60)
    print(message)
    print("-" * 60)

    if session:
        print(f"\nSession ID: {session}")

    # Save the full response
    response_file = Path(__file__).parent / "invoice_agent_v2_test_response.json"
    with open(response_file, 'w') as f:
        json.dump(chat_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

    # Summary of what should have been created
    print("\n" + "=" * 60)
    print("EXPECTED RESULTS:")
    print("-" * 60)
    print(f"Vendor: {invoice_data['vendor']['name']}")
    print(f"Items: {len(invoice_data['lineItems'])} items")
    for item in invoice_data['lineItems']:
        print(f"  - {item['itemCode']}: {item['description']}")
    print(f"PO Number: {invoice_data['purchaseOrder']['poNumber']} (will be padded to 10 chars)")
    print(f"PO Lines: {len(invoice_data['lineItems'])} lines (created in single batch)")
    print("-" * 60)

else:
    print(f"[ERROR] Agent execution failed")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
