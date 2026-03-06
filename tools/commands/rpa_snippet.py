"""Scaffold entrypoint for rpa-snippet command."""
from __future__ import annotations

import argparse
import sys

from common import run_planned_stub


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold: generate RPA snippets")
    parser.add_argument("--snippet-type")
    parser.add_argument("--context")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run_planned_stub("rpa-snippet", vars(args))


if __name__ == "__main__":
    sys.exit(main())

