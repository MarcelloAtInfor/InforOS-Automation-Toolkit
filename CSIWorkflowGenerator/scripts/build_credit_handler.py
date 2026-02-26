"""Reconstruct the ue_CreditLimitWorkflow_API handler using the AES builder.

Validates the AES builder by producing a handler that matches the reference
structure exported from the live SyteLine system.

Usage:
    python scripts/build_credit_handler.py              # Build + compare
    python scripts/build_credit_handler.py --diff       # Show detailed diff
    python scripts/build_credit_handler.py --deploy     # Deploy (deactivates old handler first)
    python scripts/build_credit_handler.py --delete     # Delete clone (reactivates old handler)
    python scripts/build_credit_handler.py --name X     # Override handler name
    python scripts/build_credit_handler.py --sequence N # Override sequence number

Deploy safety:
    --deploy automatically deactivates the original ue_CreditLimitWorkflow_API
    handler (seq=31) before creating the clone, preventing double-firing.
    --delete automatically reactivates the original after removing the clone.
"""
import json
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # repo root (shared/)
sys.path.insert(0, str(Path(__file__).parent.parent))          # project root (src/)

from src.aes_builder import (
    AESBuilder,
    EventHandler,
    EventAction,
    # Action type constants
    ACTION_FINISH,
    ACTION_NOTIFY,
    ACTION_SET_VALUES,
    ACTION_LOAD_COLLECTION,
    ACTION_INVOKE_METHOD,
    # Base expressions
    prop,
    var,
    event_param,
    return_var,
    substitute,
    round_expr,
    configname,
    username,
    curdatetime,
    # Compound patterns
    finish_with_result,
    not_condition,
    property_modified,
    # Parameter builders
    setpropvalues_params,
    load_collection_params,
    invoke_method_params,
    notify_params,
    build_ion_workflow_start_params,
)

# Paths
REFERENCE_PATH = Path(__file__).parent.parent / "reference" / "AES_ue_CreditLimitWorkflow_API.json"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_PATH = OUTPUT_DIR / "ue_CreditLimitWorkflow_Clone.json"

# Defaults
DEFAULT_NAME = "ue_CreditLimitWorkflow_Clone"
DEFAULT_SEQUENCE = 100

# Original handler identity (for safe activation toggle)
OLD_HANDLER_EVENT = "IdoOnItemUpdate"
OLD_HANDLER_SEQ = 31
OLD_HANDLER_NAME = "ue_CreditLimitWorkflow_API"


def load_reference() -> dict:
    """Load the reference handler JSON."""
    with open(REFERENCE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_handler(name: str = DEFAULT_NAME, sequence: int = DEFAULT_SEQUENCE) -> EventHandler:
    """Build the credit limit handler with all 7 actions.

    Mirrors the live ue_CreditLimitWorkflow_API handler exactly.
    """

    # Action 10: Finish - skip if CreditLimit not modified
    action_10 = EventAction(
        sequence=10,
        action_type=ACTION_FINISH,
        parameters=finish_with_result(
            not_condition(property_modified("CreditLimit")),
            "Credit Limit is not modified",
        ),
        description="Finish - Credit Limit is not modifired.",
    )

    # Action 20: LoadCollection - get old credit limit via IDO query
    action_20 = EventAction(
        sequence=20,
        action_type=ACTION_LOAD_COLLECTION,
        parameters=load_collection_params(
            "SLCustomers",
            "CreditLimit, RowPointer",
            substitute("RowPointer = '{0}'", prop("RowPointer")),
            {"OldCreditLimit": "CreditLimit"},
        ),
        description="Get old credit limit",
    )

    # Action 25: SetValues - build ION workflow start JSON payload
    from shared.tenant import get_logical_id
    action_25 = EventAction(
        sequence=25,
        action_type=ACTION_SET_VALUES,
        parameters=build_ion_workflow_start_params(
            "CS_Credit_Approval_API",
            get_logical_id(),
            {
                "CustName": ("STRING", prop("Name")),
                "CustNum": ("STRING", prop("CustNum")),
                "MGConfig": ("STRING", configname()),
                "NewCreditLimit": ("STRING", prop("CreditLimit")),
                "OldCreditLimit": ("STRING", round_expr(event_param("OldCreditLimit"), 2)),
                "RowPointer": ("STRING", prop("RowPointer")),
            },
        ),
        description="Set API PARMS",
    )

    # Action 30: InvokeMethod - call ION API to start workflow
    action_30 = EventAction(
        sequence=30,
        action_type=ACTION_INVOKE_METHOD,
        parameters=invoke_method_params(
            "IONAPIMethods",
            "InvokeIONAPIMethod2",
            [
                '"False"', '"0"', '"IONSERVICES"', '"POST"',
                '"/process/application/v1/workflow/start"',
                var("PARM"), '"application/json"', '"10000"', '"False"',
                return_var("httpResponseCode"), return_var("response"),
                return_var("responseHeaders"), return_var("infobar"),
            ],
        ),
        description="Start Workflow API",
    )

    # Action 35: Notify - debug email with parameters (optional/diagnostic)
    # NOTE: Replace <USER_EMAIL> with your email to enable debug notifications
    action_35 = EventAction(
        sequence=35,
        action_type=ACTION_NOTIFY,
        parameters=notify_params(
            to='"<USER_EMAIL>"',
            subject='"Start Workflow Params"',
            body=substitute("{0}", var("PARM")),
            save_message=False,
        ),
    )

    # Action 40: SetValues - set InWorkflow=1 AND rollback CreditLimit to old value
    action_40 = EventAction(
        sequence=40,
        action_type=ACTION_SET_VALUES,
        parameters=setpropvalues_params({
            "InWorkflow": '"1"',
            "CreditLimit": event_param("OldCreditLimit"),
        }),
        description="Lock Record & set credit limit back",
    )

    # Action 50: InvokeMethod - log note in SLObjectNotes
    action_50 = EventAction(
        sequence=50,
        action_type=ACTION_INVOKE_METHOD,
        parameters=invoke_method_params(
            "SLObjectNotes",
            "CreateRemoteNoteSp",
            [
                '"customer"',
                prop("RowPointer"),
                '"Approval Workflow Submitted"',
                substitute(
                    "Credit Limit approval workflow was submitted by {0}, at {1}.",
                    username(),
                    curdatetime(),
                ),
                '"1"',
                return_var("infobar"),
            ],
        ),
        description="Log in Notes Workflow Start",
    )

    return EventHandler(
        event_name="IdoOnItemUpdate",
        sequence=sequence,
        description=name,
        ido_collections="SLCustomers",
        synchronous=True,
        suspend=False,
        active=True,
        transactional=False,
        ignore_failure=False,
        overridable=True,
        applies_to_initiators="Form.Customers",
        access_as="ue_",
        actions=[action_10, action_20, action_25, action_30, action_35, action_40, action_50],
    )


def compare_handlers(reference: dict, generated: dict) -> list[str]:
    """Compare reference and generated handler dicts.

    Skips server-assigned fields (rowPointer, eventHandlerRowPointer, eventName)
    and intentionally-different fields (handler sequence, description).

    Returns list of difference descriptions (empty = perfect match).
    """
    diffs = []

    # --- Handler-level comparison ---
    # Skip: rowPointer (server-assigned), sequence and description (intentionally different)
    skip_handler = {"rowPointer", "sequence", "description", "actions"}
    for key in sorted(set(reference.keys()) | set(generated.keys())):
        if key in skip_handler:
            continue
        ref_val = reference.get(key)
        gen_val = generated.get(key)
        if ref_val != gen_val:
            diffs.append(f"HANDLER.{key}: ref={ref_val!r} gen={gen_val!r}")

    # Check for extra/missing handler keys (excluding skipped)
    ref_keys = set(reference.keys()) - skip_handler
    gen_keys = set(generated.keys()) - skip_handler
    for k in ref_keys - gen_keys:
        diffs.append(f"MISSING handler field: {k}")
    for k in gen_keys - ref_keys:
        diffs.append(f"EXTRA handler field: {k}")

    # --- Action-level comparison ---
    ref_actions = sorted(reference.get("actions", []), key=lambda a: a["sequence"])
    gen_actions = sorted(generated.get("actions", []), key=lambda a: a["sequence"])

    if len(ref_actions) != len(gen_actions):
        diffs.append(f"ACTION COUNT: ref={len(ref_actions)} gen={len(gen_actions)}")

    # Skip on actions: rowPointer, eventHandlerRowPointer, eventName
    skip_action = {"rowPointer", "eventHandlerRowPointer", "eventName"}

    for i in range(min(len(ref_actions), len(gen_actions))):
        ref_a = ref_actions[i]
        gen_a = gen_actions[i]
        seq = ref_a.get("sequence", "?")

        for key in sorted(set(ref_a.keys()) | set(gen_a.keys())):
            if key in skip_action:
                continue
            ref_val = ref_a.get(key)
            gen_val = gen_a.get(key)

            # Normalize: strip trailing whitespace on parameters
            if key == "parameters" and isinstance(ref_val, str) and isinstance(gen_val, str):
                ref_val = ref_val.rstrip()
                gen_val = gen_val.rstrip()

            if ref_val != gen_val:
                if key == "parameters":
                    # Show a more detailed diff for parameters
                    diffs.append(f"ACTION {seq}.{key} DIFFERS:")
                    diffs.append(f"  REF: {ref_val!r}")
                    diffs.append(f"  GEN: {gen_val!r}")
                else:
                    diffs.append(f"ACTION {seq}.{key}: ref={ref_val!r} gen={gen_val!r}")

        # Check for extra/missing action keys
        ref_akeys = set(ref_a.keys()) - skip_action
        gen_akeys = set(gen_a.keys()) - skip_action
        for k in ref_akeys - gen_akeys:
            diffs.append(f"MISSING action {seq} field: {k}")
        for k in gen_akeys - ref_akeys:
            diffs.append(f"EXTRA action {seq} field: {k}")

    return diffs


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Build and validate AES credit limit handler")
    parser.add_argument("--diff", action="store_true", help="Show detailed diff output")
    parser.add_argument("--deploy", action="store_true",
                        help="Deploy handler (deactivates old handler first)")
    parser.add_argument("--delete", action="store_true",
                        help="Delete clone handler (reactivates old handler)")
    parser.add_argument("--name", default=DEFAULT_NAME, help="Handler description/name")
    parser.add_argument("--sequence", type=int, default=DEFAULT_SEQUENCE,
                        help="Handler sequence number (system may auto-assign)")
    args = parser.parse_args()

    print("=" * 60)
    print("AES Credit Limit Handler Builder")
    print("=" * 60)

    builder = AESBuilder()

    # --- Delete mode: remove clone + reactivate original ---
    if args.delete:
        print(f"\n--- Cleanup ---")

        # Find the clone by description
        print(f"Looking for clone handler: {args.name}")
        clone_handlers = builder.load_handlers(
            event_name=OLD_HANDLER_EVENT,
            description_filter=args.name,
        )
        if not clone_handlers:
            print(f"[WARN] No handler found with description '{args.name}'")
            print(f"  Trying by sequence={args.sequence} instead...")
            try:
                builder.delete_handler(OLD_HANDLER_EVENT, args.sequence)
            except ValueError as e:
                print(f"  [ERROR] {e}")
                return 1
        else:
            clone = clone_handlers[0]
            print(f"  Found: seq={clone.sequence}, active={clone.active}")
            builder.delete_handler(OLD_HANDLER_EVENT, clone.sequence)

        # Reactivate original handler
        print(f"\nReactivating original handler: {OLD_HANDLER_NAME} (seq={OLD_HANDLER_SEQ})")
        try:
            builder.set_handler_active(OLD_HANDLER_EVENT, OLD_HANDLER_SEQ, active=True)
        except ValueError as e:
            print(f"  [WARN] Could not reactivate original: {e}")
            print(f"  You may need to reactivate {OLD_HANDLER_NAME} manually.")

        print("\nCleanup complete.")
        return 0

    # --- Build handler ---
    print(f"\nBuilding handler: {args.name} (requested sequence={args.sequence})")
    handler = build_handler(name=args.name, sequence=args.sequence)

    # Export to dict and save
    generated = handler.to_dict()
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(generated, f, indent=2, ensure_ascii=False)
    print(f"Written to: {OUTPUT_PATH}")

    # Load reference and compare
    print(f"\nLoading reference: {REFERENCE_PATH}")
    reference = load_reference()

    print("\n--- Structural Comparison ---")
    diffs = compare_handlers(reference, generated)

    if not diffs:
        print("[OK] Generated handler matches reference structure exactly!")
    else:
        print(f"[!!] Found {len(diffs)} difference(s):")
        for d in diffs:
            print(f"  - {d}")

    if args.diff:
        print("\n--- Full JSON Diff ---")
        import difflib

        # Normalize for diff: remove server-assigned fields from reference
        ref_norm = {k: v for k, v in reference.items() if k != "rowPointer"}
        ref_norm["actions"] = [
            {k: v for k, v in a.items() if k not in ("rowPointer", "eventHandlerRowPointer", "eventName")}
            for a in sorted(reference.get("actions", []), key=lambda a: a["sequence"])
        ]
        gen_norm = {k: v for k, v in generated.items() if k != "rowPointer"}
        gen_norm["actions"] = sorted(generated.get("actions", []), key=lambda a: a["sequence"])

        ref_lines = json.dumps(ref_norm, indent=2, ensure_ascii=False).splitlines(keepends=True)
        gen_lines = json.dumps(gen_norm, indent=2, ensure_ascii=False).splitlines(keepends=True)
        diff = difflib.unified_diff(ref_lines, gen_lines, fromfile="reference", tofile="generated")
        diff_text = "".join(diff)
        if diff_text:
            print(diff_text)
        else:
            print("(no differences in normalized output)")

    # Summary
    print(f"\nHandler: {handler.description} (event={handler.event_name}, seq={handler.sequence})")
    print(f"Actions: {len(handler.actions)}")
    for a in handler.actions:
        desc = f" - {a.description}" if a.description else ""
        print(f"  [{a.sequence}] type={a.action_type}{desc}")

    # --- Deploy mode ---
    if args.deploy:
        if diffs:
            print("\n[WARN] Deploying despite differences!")

        # Step 1: Deactivate original handler
        print(f"\n--- Deploy ---")
        print(f"Step 1: Deactivating original handler: {OLD_HANDLER_NAME} (seq={OLD_HANDLER_SEQ})")
        try:
            builder.set_handler_active(OLD_HANDLER_EVENT, OLD_HANDLER_SEQ, active=False)
        except ValueError as e:
            print(f"  [ERROR] Could not deactivate original: {e}")
            print(f"  Aborting deploy to prevent double-firing.")
            return 1

        # Step 2: Create clone handler
        print(f"\nStep 2: Creating clone handler: {args.name}")
        try:
            builder.create(handler)
        except Exception as e:
            print(f"\n  [ERROR] Create failed: {e}")
            print(f"  Reactivating original handler...")
            builder.set_handler_active(OLD_HANDLER_EVENT, OLD_HANDLER_SEQ, active=True)
            return 1

        # Step 3: Verify what the system actually created
        print(f"\nStep 3: Verifying created handler...")
        actual = builder.verify_created_handler(handler)
        if actual:
            print(f"  Stored as: seq={actual.sequence}, active={actual.active}, "
                  f"desc={actual.description}")
            if actual.sequence != args.sequence:
                print(f"  [NOTE] System assigned sequence={actual.sequence} "
                      f"(requested {args.sequence})")
                print(f"  Use --sequence {actual.sequence} with --delete for cleanup")
        else:
            print(f"  [WARN] Could not read back handler. "
                  f"Use query_aes.py to confirm.")

        print("\nDeployment complete.")
        print(f"\nTo clean up and restore original handler:")
        seq = actual.sequence if actual else args.sequence
        print(f"  python scripts/build_credit_handler.py --delete --sequence {seq}")

    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
