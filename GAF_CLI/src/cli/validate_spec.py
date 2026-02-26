#!/usr/bin/env python3
"""
Validate tool/agent spec from JSON or YAML file.

CLI-XX: validate_spec.py - validate tool/agent spec from JSON or YAML file.

Usage:
    python -m src.cli.validate_spec specs/tools/MyTool_v1.json
    python -m src.cli.validate_spec specs/tools/MyTool_v1.yaml
    python -m src.cli.validate_spec specs/tools/MyTool_v1.json --json
    python -m src.cli.validate_spec specs/tools/MyTool_v1.json -v

Exit codes:
    0: Success (spec is valid)
    1: Validation failure
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Try to import yaml, but make it optional
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from src.shared.validation import validate_spec
from src.shared.logging import configure_logging


def load_spec(spec_path: Path) -> dict:
    """
    Load and parse spec file (JSON or YAML).

    Args:
        spec_path: Path to spec file

    Returns:
        Parsed spec dict

    Raises:
        FileNotFoundError: If spec file doesn't exist
        ValueError: If file extension is not supported or PyYAML is not installed
        json.JSONDecodeError: If JSON is malformed
        yaml.YAMLError: If YAML is malformed
    """
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    # Detect format from extension
    extension = spec_path.suffix.lower()

    if extension == '.json':
        with spec_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    elif extension in ['.yaml', '.yml']:
        if not YAML_AVAILABLE:
            raise ValueError(
                "YAML support requires PyYAML. Install with: pip install pyyaml"
            )
        with spec_path.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(
            f"Unsupported file extension: {extension}. "
            "Supported formats: .json, .yaml, .yml"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Validate a tool or agent spec file",
        epilog="Example: python -m src.cli.validate_spec specs/tools/GAF_GenAI_ListAssets_Tool_v1.json"
    )

    parser.add_argument(
        "spec_file",
        type=Path,
        help="Path to spec file (JSON or YAML)"
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

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    configure_logging(level)

    try:
        # Load spec
        spec = load_spec(args.spec_file)
        logging.info(f"Loaded spec: {spec.get('name', 'unknown')}")

        # Validate spec
        errors = validate_spec(spec)

        if errors:
            # Validation failed
            if args.output_json:
                result = {
                    "valid": False,
                    "errors": errors
                }
                print(json.dumps(result, indent=2))
            else:
                print("Validation failed:", file=sys.stderr)
                for err in errors:
                    print(f"  - {err['field']}: {err['message']}", file=sys.stderr)
            sys.exit(1)
        else:
            # Validation passed
            if args.output_json:
                result = {
                    "valid": True,
                    "name": spec.get('name', 'unknown'),
                    "type": spec.get('type', 'unknown')
                }
                print(json.dumps(result, indent=2))
            else:
                print(f"VALID: {spec.get('name', 'unknown')}")
                print(f"  Type: {spec.get('type', 'unknown')}")
            sys.exit(0)

    except FileNotFoundError as e:
        logging.error(str(e))
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in spec file: {e}")
        print(f"Error: Invalid JSON in spec file: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        logging.error(str(e))
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error validating spec: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
