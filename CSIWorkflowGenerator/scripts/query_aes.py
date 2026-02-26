"""Discover and export existing AES event handlers.

Usage:
    python scripts/query_aes.py                                    # List IdoOnItemUpdate handlers
    python scripts/query_aes.py --handler ue_CreditLimit           # Search by description
    python scripts/query_aes.py --handler ue_CreditLimit --export  # Export to reference/
    python scripts/query_aes.py --ido SLCustomers                  # Filter by IDO
    python scripts/query_aes.py --all                              # All handlers (all events)
    python scripts/query_aes.py --event IdoOnItemInsert            # Specific event type

Requires: IONAPI_FILE env var or .ionapi in cwd
"""
import argparse
import json
import sys
from pathlib import Path

# Add repo root for shared/, project root for src/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.aes_builder.builder import AESBuilder


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_handler_summary(handler, index=None):
    """Print a compact handler summary."""
    prefix = f"  [{index}] " if index is not None else "  "
    active = "ACTIVE" if handler.active else "INACTIVE"
    suspend = " [SUSPEND]" if handler.suspend else ""
    sync = " [SYNC]" if handler.synchronous else ""
    print(
        f"{prefix}{handler.description or '(no description)'} "
        f"-- {handler.event_name} seq={handler.sequence} "
        f"ido={handler.ido_collections or '(none)'} "
        f"{active}{suspend}{sync}"
    )
    if handler.triggering_property:
        print(f"      TriggeringProperty: {handler.triggering_property}")
    if handler.applies_to_initiators:
        print(f"      AppliesToInitiators: {handler.applies_to_initiators}")
    if handler.access_as:
        print(f"      AccessAs: {handler.access_as}")


def print_action_detail(action):
    """Print action details."""
    print(f"    Action {action.sequence}: {action.action_type}")
    if action.description:
        print(f"      Description: {action.description}")
    if action.parameters:
        # Break long parameter strings for readability
        params = action.parameters
        if len(params) > 100:
            # Try to break at semicolons or known keywords
            parts = []
            current = ""
            for char in params:
                current += char
                if char == ")" and len(current) > 40:
                    parts.append(current)
                    current = ""
            if current:
                parts.append(current)
            if len(parts) > 1:
                print(f"      Parameters:")
                for part in parts:
                    print(f"        {part}")
            else:
                print(f"      Parameters: {params}")
        else:
            print(f"      Parameters: {params}")


def export_handler(handler, output_dir):
    """Export a handler to a JSON reference file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Build filename from description
    desc = handler.description or f"{handler.event_name}_{handler.sequence}"
    # Sanitize filename
    safe_name = "".join(
        c if c.isalnum() or c in ("_", "-") else "_" for c in desc
    )
    filename = f"AES_{safe_name}.json"
    filepath = output_dir / filename

    ref = handler.to_dict()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ref, f, indent=2, ensure_ascii=False)
    print(f"\n  Exported to: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Discover and export AES event handlers"
    )
    parser.add_argument(
        "--handler", "-H",
        help="Filter by handler description (supports %% wildcards)",
    )
    parser.add_argument(
        "--ido", "-I",
        help="Filter by IDO collection name (supports %% wildcards)",
    )
    parser.add_argument(
        "--event", "-E",
        default="IdoOnItemUpdate",
        help="Event name to query (default: IdoOnItemUpdate)",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Show all handlers (no event filter)",
    )
    parser.add_argument(
        "--export", action="store_true",
        help="Export matching handler(s) to reference/ as JSON",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON instead of formatted text",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  AES Handler Discovery")
    print("=" * 60)

    builder = AESBuilder()

    # Determine filters
    event_name = None if args.all else args.event
    description_filter = args.handler
    ido_filter = args.ido

    # Add wildcard if not present for handler search
    if description_filter and "%" not in description_filter:
        description_filter = f"%{description_filter}%"

    filters_desc = []
    if event_name:
        filters_desc.append(f"event={event_name}")
    if description_filter:
        filters_desc.append(f"description LIKE '{description_filter}'")
    if ido_filter:
        filters_desc.append(f"ido={ido_filter}")
    print(f"\n  Filters: {', '.join(filters_desc) if filters_desc else '(none)'}")

    # Load handlers
    print_section("Handlers")
    handlers = builder.load_handlers(
        event_name=event_name,
        description_filter=description_filter,
        ido_filter=ido_filter,
    )

    if not handlers:
        print("  No handlers found matching filters.")
        return 0

    print(f"  Found {len(handlers)} handler(s):\n")
    for i, handler in enumerate(handlers, 1):
        print_handler_summary(handler, i)

    # Load actions for each handler
    print_section("Handler Details (with Actions)")
    for handler in handlers:
        print(f"\n  --- {handler.description or '(no description)'} ---")
        print(f"  Event: {handler.event_name}")
        print(f"  Sequence: {handler.sequence}")
        print(f"  IDO: {handler.ido_collections or '(none)'}")
        print(f"  Active: {handler.active}")
        print(f"  Suspend: {handler.suspend}")
        print(f"  Synchronous: {handler.synchronous}")
        print(f"  Transactional: {handler.transactional}")
        print(f"  Overridable: {handler.overridable}")
        if handler.triggering_property:
            print(f"  TriggeringProperty: {handler.triggering_property}")
        if handler.row_pointer:
            print(f"  RowPointer: {handler.row_pointer}")

        # Load actions
        if handler.row_pointer:
            actions = builder.load_actions(
                event_handler_row_pointer=handler.row_pointer
            )
        else:
            actions = builder.load_actions(
                event_name=handler.event_name,
                handler_sequence=handler.sequence,
            )

        handler.actions = actions
        if actions:
            print(f"\n  Actions ({len(actions)}):")
            for action in actions:
                print_action_detail(action)
        else:
            print("\n  No actions found.")

    # JSON output
    if args.json:
        print_section("JSON Output")
        output = [builder.export_handler(h) for h in handlers]
        print(json.dumps(output, indent=2, ensure_ascii=False))

    # Export
    if args.export:
        print_section("Export")
        ref_dir = Path(__file__).parent.parent / "reference"
        for handler in handlers:
            export_handler(handler, ref_dir)

    # Summary
    print_section("Summary")
    print(f"  Handlers found: {len(handlers)}")
    total_actions = sum(len(h.actions) for h in handlers)
    print(f"  Total actions: {total_actions}")
    for h in handlers:
        print(f"    {h.description}: {len(h.actions)} actions")

    return 0


if __name__ == "__main__":
    sys.exit(main())
