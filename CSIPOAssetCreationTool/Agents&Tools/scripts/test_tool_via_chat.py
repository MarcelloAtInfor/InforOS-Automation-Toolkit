"""
Test a tool via the Chat API
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

headers = get_auth_headers()

# Test prompt
test_prompt = "Search for customers with name containing 'Test'"

# Request body
chat_request = {
    "prompt": test_prompt,
    "session": None,
    "tools": ["CustomerSearch_Tool"],  # Specify our new tool
    "toolInfo": {
        "CustomerSearch_Tool": {
            "stub": False  # Use real API, not stub
        }
    }
}

print("Testing CustomerSearch_Tool via Chat API")
print("=" * 60)
print(f"POST {chat_url}")
print(f"\nPrompt: {test_prompt}")
print(f"Tool: CustomerSearch_Tool\n")

response = requests.post(chat_url, headers=headers, json=chat_request)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    chat_response = response.json()
    print("[SUCCESS] Chat completed!\n")

    print(f"Session ID: {chat_response.get('session')}")
    print(f"Message ID: {chat_response.get('id')}")
    print(f"\nResponse Content:")
    print("-" * 60)
    print(chat_response.get('content', 'No content'))

    # Save full response
    response_file = Path(__file__).parent / "chat_test_response.json"
    with open(response_file, 'w') as f:
        json.dump(chat_response, f, indent=2)

    print(f"\n{'-' * 60}")
    print(f"[SUCCESS] Full response saved to: {response_file}")

    # Check for links or follow-ups
    links = chat_response.get('links')
    followups = chat_response.get('followups')

    if links:
        print(f"\nLinks provided: {len(links)}")
    if followups:
        print(f"Follow-up suggestions: {len(followups)}")

else:
    print(f"[ERROR] Chat request failed")
    print(f"Response: {response.text}")

print("\n" + "=" * 60)
