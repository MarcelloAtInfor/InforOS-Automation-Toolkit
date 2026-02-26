"""
Minimal test to understand PoReceivePopulateTtRcvSp parameter signature.
"""
import requests
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site


def test_invoke_with_params(params: list):
    """Test the invoke call with given parameters."""
    headers = get_auth_headers()
    headers['X-Infor-MongooseConfig'] = get_site()

    url = f"{IDO_URL()}/invoke/SLPoItems?method=PoReceivePopulateTtRcvSp"

    print(f"Testing with {len(params)} parameters:")
    print(f"  Params: {json.dumps(params[:10])}...")

    response = requests.post(url, headers=headers, json=params)

    print(f"  Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        success = data.get('Success', False)
        msg = data.get('Message', '')
        print(f"  Success: {success}")
        if msg:
            print(f"  Message: {msg}")
    else:
        print(f"  Error: {response.text[:300]}")

    print()
    return response


if __name__ == '__main__':
    print("Testing PoReceivePopulateTtRcvSp parameter signature")
    print("=" * 60)

    # Test 1: Empty array
    print("\nTest 1: Empty array")
    test_invoke_with_params([])

    # Test 2: Single numeric string
    print("\nTest 2: Single parameter [1]")
    test_invoke_with_params(["1"])

    # Test 3: Few parameters
    print("\nTest 3: 5 parameters")
    test_invoke_with_params(["1", "PO20261009", "1", "0", "0"])

    # Test 4: Numeric-first approach (maybe Seq, PoLine, PoRelease are all numeric?)
    print("\nTest 4: All numeric-style")
    test_invoke_with_params(["1", "0", "1", "0", "0"])
