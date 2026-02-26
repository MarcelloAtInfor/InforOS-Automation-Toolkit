"""
Test the CustomerSearch_Agent via Chat API
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

# Agent logical ID prefix
logical_id_prefix = "lid://infor.syteline.customer-search"

headers = get_auth_headers()
headers['x-infor-logicalidprefix'] = logical_id_prefix  # This tells the API which agent to use

# Test prompt
test_prompt = "Search for customers with name containing 'Corp'"

# Request body
chat_request = {
    "prompt": test_prompt,
    "session": None  # Start new session
}

print("Testing CustomerSearch_Agent via Chat API")
print("=" * 60)
print(f"POST {chat_url}")
print(f"Logical ID: {logical_id_prefix}")
print(f"\nPrompt: {test_prompt}\n")

response = requests.post(chat_url, headers=headers, json=chat_request, timeout=60)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    chat_response = response.json()
    print("[SUCCESS] Chat completed!\n")

    print(f"Session ID: {chat_response.get('session')}")
    print(f"Message ID: {chat_response.get('id')}")

    content = chat_response.get('content', 'No content')
    print(f"\nAgent Response:")
    print("=" * 60)
    print(content)
    print("=" * 60)

    # Save full response
    response_file = Path(__file__).parent / "agent_chat_test_response.json"
    with open(response_file, 'w') as f:
        json.dump(chat_response, f, indent=2)

    print(f"\n[SUCCESS] Full response saved to: {response_file}")

    # Check for links or follow-ups
    links = chat_response.get('links')
    followups = chat_response.get('followups')
    screen_nav = chat_response.get('screen_navigation')

    if links:
        print(f"\nLinks: {len(links)} link(s) provided")
    if followups:
        print(f"Follow-ups: {len(followups)} suggestion(s)")
        for i, followup in enumerate(followups[:3], 1):
            print(f"  {i}. {followup}")
    if screen_nav:
        print(f"Screen Navigation: {screen_nav}")

elif response.status_code == 404:
    print(f"[ERROR] Logical ID not found")
    print(f"The agent with logical ID '{logical_id_prefix}' may not exist or is not accessible.")
    print(f"\nTry checking:")
    print(f"  - Is the agent enabled?")
    print(f"  - Is the logical ID correct?")
    print(f"  - Does the agent have the CustomerSearch_Tool assigned?")

else:
    print(f"[ERROR] Chat request failed")
    try:
        error_data = response.json()
        print(f"Error: {json.dumps(error_data, indent=2)}")
    except:
        print(f"Response: {response.text}")

print("\n" + "=" * 60)
