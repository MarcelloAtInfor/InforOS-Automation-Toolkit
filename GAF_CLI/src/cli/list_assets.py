#!/usr/bin/env python3
"""
List GenAI assets with filtering options.

CLI-04: list_assets.py - list tools/agents with filtering options.

Usage:
    python -m src.cli.list_assets
    python -m src.cli.list_assets --prefix GAF
    python -m src.cli.list_assets --type API
    python -m src.cli.list_assets --prefix GAF --type TOOLKIT
    python -m src.cli.list_assets --json

Exit codes:
    0: Success
    1: Error (API failure, config error)
"""

import argparse
import json
import logging
import sys
from typing import List, Dict, Any

from src.infor_os.genai_client import GenAIClient
from src.shared.logging import configure_logging


def filter_assets(
    assets: List[Dict[str, Any]],
    prefix: str = None,
    asset_type: str = None
) -> List[Dict[str, Any]]:
    """Filter assets by prefix and/or type."""
    result = assets

    if prefix:
        result = [a for a in result if a.get("name", "").startswith(prefix)]

    if asset_type:
        result = [a for a in result if a.get("type") == asset_type]

    return result


def format_asset_line(asset: Dict[str, Any]) -> str:
    """Format single asset for human-readable output."""
    name = asset.get("name", "unknown")
    asset_type = asset.get("type", "?")
    guid = asset.get("guid", "no-guid")[:8]  # Truncate GUID for readability
    return f"  {name} ({asset_type}) [{guid}...]"


def main():
    parser = argparse.ArgumentParser(
        description="List GenAI assets (tools and agents)",
        epilog="Example: python -m src.cli.list_assets --prefix GAF"
    )

    parser.add_argument(
        "--prefix",
        help="Filter by name prefix (e.g., 'GAF' for Factory tools)"
    )

    parser.add_argument(
        "--type",
        choices=["API", "TOOLKIT", "FUNCTION"],
        help="Filter by asset type"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    configure_logging(level)

    try:
        # Initialize client
        client = GenAIClient()

        # List all assets
        assets = client.list_tools()

        # Apply filters
        filtered = filter_assets(assets, args.prefix, args.type)

        # Output
        if args.output_json:
            print(json.dumps(filtered, indent=2))
        else:
            print(f"Found {len(filtered)} asset(s):")
            for asset in filtered:
                print(format_asset_line(asset))

        sys.exit(0)

    except FileNotFoundError as e:
        logging.error(f"Configuration file not found: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error listing assets: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
