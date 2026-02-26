#!/usr/bin/env python3
"""
Publish a tool to Infor OS GenAI from JSON spec file.

CLI-01: publish_tool.py - publish tool from JSON spec file.

Usage:
    python -m src.cli.publish_tool specs/tools/MyTool_v1.json
    python -m src.cli.publish_tool specs/tools/MyTool_v1.json --json
    python -m src.cli.publish_tool specs/tools/MyTool_v1.json -v

Exit codes:
    0: Success
    1: Error (validation failure, API error, file not found)
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from src.infor_os.genai_client import GenAIClient
from src.shared.validation import validate_spec, ValidationError
from src.shared.logging import configure_logging


def load_spec(spec_path: Path) -> dict:
    """Load and parse JSON spec file."""
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    with spec_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Publish a tool to Infor OS GenAI",
        epilog="Example: python -m src.cli.publish_tool specs/tools/GAF_GenAI_ListAssets_Tool_v1.json"
    )

    parser.add_argument(
        "spec_file",
        type=Path,
        help="Path to tool spec JSON file"
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

        # Validate spec (unless skipped)
        if not args.skip_validation:
            errors = validate_spec(spec)
            if errors:
                print("Validation failed:", file=sys.stderr)
                for err in errors:
                    print(f"  - {err['field']}: {err['message']}", file=sys.stderr)
                sys.exit(1)

        # Publish tool
        client = GenAIClient()
        created = client.create_tools([spec])
        result = created[0]

        # Output
        if args.output_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Published tool: {result.get('name', 'unknown')}")
            print(f"  GUID: {result.get('guid', 'no-guid')}")
            print(f"  Type: {result.get('type', 'unknown')}")

        sys.exit(0)

    except FileNotFoundError as e:
        logging.error(str(e))
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in spec file: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error publishing tool: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
