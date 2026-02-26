#!/usr/bin/env python3
"""
Update an existing asset in Infor OS GenAI from JSON spec file.

CLI-03: update_asset.py - update asset from JSON spec file.

The spec file MUST include the 'guid' field of the existing asset.
This performs a full replacement - all fields must be provided.

Usage:
    python -m src.cli.update_asset specs/tools/MyTool_v1.json
    python -m src.cli.update_asset specs/tools/MyTool_v1.json --json

Exit codes:
    0: Success
    1: Error (validation failure, API error, missing GUID)
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from src.infor_os.genai_client import GenAIClient
from src.shared.validation import validate_spec
from src.shared.logging import configure_logging


def load_spec(spec_path: Path) -> dict:
    """Load and parse JSON spec file."""
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    with spec_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Update an existing asset in Infor OS GenAI",
        epilog="Example: python -m src.cli.update_asset specs/tools/GAF_GenAI_ListAssets_Tool_v1.json"
    )

    parser.add_argument(
        "spec_file",
        type=Path,
        help="Path to asset spec JSON file (must include 'guid' field)"
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
        help="Output result as JSON"
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip spec validation (not recommended)"
    )

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    configure_logging(level)

    try:
        # Load spec
        spec = load_spec(args.spec_file)
        logging.info(f"Loaded spec: {spec.get('name', 'unknown')}")

        # Validate GUID presence
        if "guid" not in spec:
            print("Error: Spec must include 'guid' field for update.", file=sys.stderr)
            print("  Use publish_tool.py or publish_agent.py for new assets.", file=sys.stderr)
            sys.exit(1)

        # Validate spec (unless skipped)
        if not args.skip_validation:
            errors = validate_spec(spec)
            if errors:
                print("Validation failed:", file=sys.stderr)
                for err in errors:
                    print(f"  - {err['field']}: {err['message']}", file=sys.stderr)
                sys.exit(1)

        # Update asset
        client = GenAIClient()
        result = client.update_tool(spec)

        # Output
        if args.output_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Updated asset: {result.get('name', 'unknown')}")
            print(f"  GUID: {result.get('guid', 'no-guid')}")
            print(f"  Type: {result.get('type', 'unknown')}")

        sys.exit(0)

    except FileNotFoundError as e:
        logging.error(str(e))
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in spec file: {e}")
        sys.exit(1)
    except ValueError as e:
        # From update_tool GUID validation
        logging.error(str(e))
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error updating asset: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
