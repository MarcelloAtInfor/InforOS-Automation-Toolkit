"""
Get OAuth 2.0 token from Infor ION API using password grant type.

This is a convenience wrapper around shared.auth.request_token().
Run this script to generate a fresh token in this directory.

Alternative: python -m shared.auth Agents&Tools/scripts
"""
from pathlib import Path
import sys

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import request_token

if __name__ == '__main__':
    save_path = Path(__file__).parent / "access_token.txt"
    request_token(save_path)
