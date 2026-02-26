"""
Test authentication with Infor GenAI API using different methods
"""
import json
import requests
from pathlib import Path
import base64
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_credentials
from shared.config import GENAI_CORE_URL

# Load credentials
creds = get_credentials()

print("Testing Infor GenAI API Authentication\n")
print("=" * 60)

# Method 1: Try using Service Account Access Key directly
print("\nMethod 1: Using Service Account Access Key as Bearer token")
print("-" * 60)

tools_url = f"{GENAI_CORE_URL()}/api/v1/tools"

headers = {
    'Authorization': f"Bearer {creds['saak']}"
}

print(f"GET {tools_url}")
response = requests.get(tools_url, headers=headers)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("[SUCCESS] Service Account Key works!")
    tools = response.json()
    print(f"Found {len(tools)} tools")
    if tools:
        print(f"\nFirst tool: {tools[0].get('name', 'N/A')}")
else:
    print(f"Response: {response.text[:200]}")

# Method 2: Try Basic Auth with service account keys
print("\n\nMethod 2: Using Basic Auth with Service Account Keys")
print("-" * 60)

auth_string = f"{creds['saak']}:{creds['sask']}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    'Authorization': f"Basic {encoded_auth}"
}

print(f"GET {tools_url}")
response = requests.get(tools_url, headers=headers)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("[SUCCESS] Basic Auth works!")
    tools = response.json()
    print(f"Found {len(tools)} tools")
else:
    print(f"Response: {response.text[:200]}")

# Method 3: Try OAuth with password grant (would need username/password)
print("\n\nMethod 3: OAuth Password Grant")
print("-" * 60)
print("Skipping - requires user credentials (username/password)")

print("\n" + "=" * 60)
print("\nSummary: Check which method returned Status Code 200")
