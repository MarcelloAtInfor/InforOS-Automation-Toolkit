"""
Test the UpdateOrderLineDates_Agent_v2 via Chat API
"""
import json
import requests
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CHAT_URL

# Chat API endpoint
chat_url = f"{GENAI_CHAT_URL()}/api/v1/chat/sync"

# Agent logical ID
logical_id = "lid://infor.syteline.update-orderline-dates-v2"

headers = get_auth_headers()
headers['x-infor-logicalidprefix'] = logical_id

# Test prompt
request_body = {
    "prompt": "Update the order line due dates for this week",
    "session": None
}

print("Testing UpdateOrderLineDates_Agent_v2")
print("=" * 60)
print(f"POST {chat_url}")
print(f"Logical ID: {logical_id}")
print(f"Prompt: {request_body['prompt']}\n")

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
    response_file = Path(__file__).parent / "orderline_agent_test_response.json"
    with open(response_file, 'w') as f:
        json.dump(chat_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

else:
    print(f"[ERROR] Agent execution failed")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
