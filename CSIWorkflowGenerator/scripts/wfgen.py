"""Unified workflow generation CLI — spec to deployed system in one command.

Composes all existing modules: template system, validator, ION deployer,
and AES handler builder into a single entry point with subcommands.

Usage:
    python scripts/wfgen.py create templates/spec.json [--live] [--activate]
    python scripts/wfgen.py render templates/spec.json [--diff ref.json]
    python scripts/wfgen.py validate templates/spec.json [--live]
    python scripts/wfgen.py aes templates/spec.json [--deploy]
    python scripts/wfgen.py status WorkflowName
    python scripts/wfgen.py delete WorkflowName
    python scripts/wfgen.py extract-sa WorkflowName [--file path/to/file.json]
"""
import argparse
import json
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root and repo root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT.parent))

from src.templates import load_spec, render
from src.templates.schema import WorkflowSpec
from src.config.tenant import load_default
from src.parser.validator import SpecValidator

OUTPUT_DIR = PROJECT_ROOT / "output"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _load_and_validate(
    spec_path: str,
    use_live: bool = False,
    override_name: str | None = None,
) -> tuple[WorkflowSpec, bool]:
    """Load spec, run validation, print results.

    Returns (spec, passed) tuple. passed=False means errors found.
    """
    spec_file = Path(spec_path)
    if not spec_file.exists():
        spec_file = PROJECT_ROOT / spec_path
    if not spec_file.exists():
        print(f"Error: file not found: {spec_path}")
        sys.exit(1)

    print(f"Spec: {spec_file}")
    try:
        spec = load_spec(spec_file)
    except Exception as e:
        print(f"[FAIL] Failed to parse spec: {e}")
        sys.exit(1)

    if override_name:
        spec.name = override_name

    print(f"Workflow: {spec.name}")
    print(f"Variables: {len(spec.variables)}")
    print(f"Views: {len(spec.views)}, Trees: {len(spec.trees)}, Flow steps: {len(spec.flow)}")
    if spec.aes_trigger:
        t = spec.aes_trigger
        print(f"AES trigger: {t.event} on {t.ido}.{t.monitored_field}")

    # Validate
    tenant = load_default()
    live_client = None
    if use_live:
        from src.parser.ido_metadata import IdoMetadataClient
        print("\nConnecting to SyteLine for live IDO validation...")
        live_client = IdoMetadataClient()

    levels = ["structural", "referential", "tenant"]
    if use_live:
        levels.append("live")
    print(f"Validation levels: {', '.join(levels)}")

    validator = SpecValidator(spec, tenant)
    report = validator.validate(live_client=live_client)

    print(f"\n--- Validation ---")
    if report.is_valid and not report.warnings:
        print("[PASS] No issues found!")
    elif report.is_valid:
        print(f"[PASS] Valid with {len(report.warnings)} warning(s)")
    else:
        print(f"[FAIL] {report.summary()}")

    for issue in report.issues:
        icon = "!!" if issue.severity == "error" else "~~"
        print(f"  [{icon}] {issue.path}")
        print(f"       {issue.message}")
        if issue.suggestion:
            print(f"       -> {issue.suggestion}")

    return spec, report.is_valid


def _render_spec(spec: WorkflowSpec) -> tuple[dict, Path]:
    """Render spec to ION workflow JSON, save to output/, return (dict, path)."""
    tenant = load_default()
    result = render(spec, tenant)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{spec.name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n--- Rendered ---")
    print(f"Output: {output_path}")
    print(f"Variables: {len(result['variables'])}")
    print(f"Views: {len(result['views'])}, Trees: {len(result['trees'])}")
    print(f"Flowparts: {len(result['sequentialFlow']['flowParts'])}")

    return result, output_path


def _deploy_ion_workflow(
    workflow_def: dict, activate: bool = False, update: bool = False
) -> bool:
    """Deploy ION workflow. Returns True on success."""
    from scripts.deploy_workflow import create_workflow, activate_workflow, delete_workflow

    print(f"\n--- ION Workflow Deploy ---")
    result = create_workflow(workflow_def)

    if result is None and update:
        name = workflow_def.get("name", "unknown")
        print(f"Workflow exists — deleting and recreating (--update)")
        delete_workflow(name)
        result = create_workflow(workflow_def)

    if result is None:
        return False

    name = workflow_def.get("name", "unknown")
    if activate:
        print()
        activate_workflow(name)
        print(f"Workflow '{name}' is now ACTIVE.")
    else:
        print(f"Workflow '{name}' created (not activated).")

    return True


def _build_aes_handler(spec: WorkflowSpec) -> "EventHandler":
    """Build AES handler from spec's aes_trigger. Returns EventHandler."""
    from src.aes_builder.spec_handler import build_handler_from_spec
    from src.config.tenant import load_default

    tenant = load_default()
    handler = build_handler_from_spec(spec, tenant.logical_id)

    print(f"\n--- AES Handler Built ---")
    print(f"Handler: {handler.description}")
    print(f"Event: {handler.event_name}, Sequence: {handler.sequence}")
    print(f"IDO: {handler.ido_collections}")
    print(f"AppliesToInitiators: {handler.applies_to_initiators or '(none)'}")
    print(f"Actions: {len(handler.actions)}")
    for a in handler.actions:
        desc = f" - {a.description}" if a.description else ""
        print(f"  [{a.sequence}] type={a.action_type}{desc}")

    return handler


def _deploy_aes_handler(handler, update: bool = False) -> bool:
    """Deploy AES handler via IDO API. Returns True on success."""
    from src.aes_builder import AESBuilder

    print(f"\n--- AES Handler Deploy ---")
    builder = AESBuilder()

    try:
        builder.create(handler)
    except Exception as e:
        if update and "already exists" in str(e):
            print(f"[SKIP] AES handler already exists — keeping existing handler.")
            print(f"  (IDO API does not support handler delete/replace yet)")
        else:
            print(f"[ERROR] AES handler creation failed: {e}")
            return False

    # Verify
    actual = builder.verify_created_handler(handler)
    if actual:
        print(f"Verified: seq={actual.sequence}, active={actual.active}")
        if actual.sequence != handler.sequence:
            print(f"  [NOTE] System assigned seq={actual.sequence} (requested {handler.sequence})")
    else:
        print("[WARN] Could not verify handler — use query_aes.py to confirm.")

    return True


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------


def cmd_create(args: argparse.Namespace) -> int:
    """Full pipeline: validate + render + deploy ION + optional AES handler."""
    print("=" * 60)
    print("wfgen create — Full Pipeline")
    print("=" * 60)

    spec, valid = _load_and_validate(args.spec, args.live, args.name)
    if not valid:
        print("\nAborting — fix validation errors first.")
        return 1

    # Render
    workflow_def, output_path = _render_spec(spec)

    # Warn if ionapi flowparts exist but no service account is configured
    has_ionapi, has_sa = _check_service_account(workflow_def)
    if has_ionapi and not has_sa:
        print("\n[WARN] No service account configured — ionapi flowparts will not")
        print("  have a serviceAccount. After deployment, either:")
        print("  1. Upload the service account CSV manually in ION Desk, or")
        print("  2. Run: python scripts/wfgen.py extract-sa <ExistingWorkflowName>")
        print("     then re-deploy this workflow.\n")

    # Deploy ION workflow
    if not _deploy_ion_workflow(workflow_def, args.activate, args.update):
        return 1

    # Deploy AES handler (if spec has aes_trigger)
    if spec.aes_trigger:
        handler = _build_aes_handler(spec)
        if not _deploy_aes_handler(handler, update=args.update):
            print("\n[WARN] ION workflow was deployed but AES handler failed.")
            print("  You may need to deploy the AES handler manually or delete the workflow.")
            return 1
    else:
        print("\nNo aes_trigger section — skipping AES handler.")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Deployment complete!")
    print(f"  ION Workflow: {spec.name}")
    if spec.aes_trigger:
        desc = spec.aes_trigger.handler_description or f"ue_{spec.name}"
        print(f"  AES Handler: {desc} (seq={spec.aes_trigger.handler_sequence})")
    print(f"  Output: {output_path}")
    print(f"{'=' * 60}")

    return 0


def cmd_render(args: argparse.Namespace) -> int:
    """Validate + render to output/ (no deploy)."""
    print("=" * 60)
    print("wfgen render — Validate + Render")
    print("=" * 60)

    spec, valid = _load_and_validate(args.spec, args.live, args.name)
    if not valid:
        print("\nAborting — fix validation errors first.")
        return 1

    workflow_def, output_path = _render_spec(spec)

    # Diff
    if args.diff:
        from scripts.render_template import compare_workflows

        diff_file = Path(args.diff)
        if not diff_file.exists():
            diff_file = PROJECT_ROOT / args.diff
        if not diff_file.exists():
            print(f"\nError: reference file not found: {args.diff}")
            return 1

        print(f"\n--- Structural Comparison vs {diff_file.name} ---")
        with open(diff_file, "r", encoding="utf-8") as f:
            reference = json.load(f)

        diffs = compare_workflows(reference, workflow_def)
        if not diffs:
            print("[OK] Generated workflow matches reference structure exactly!")
        else:
            print(f"[!!] Found {len(diffs)} difference(s):")
            for d in diffs:
                print(f"  - {d}")

    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate only (no render or deploy)."""
    print("=" * 60)
    print("wfgen validate — Spec Validation")
    print("=" * 60)

    spec, valid = _load_and_validate(args.spec, args.live, args.name)
    return 0 if valid else 1


def cmd_aes(args: argparse.Namespace) -> int:
    """Build (and optionally deploy) AES handler from spec."""
    print("=" * 60)
    print("wfgen aes — AES Handler Generator")
    print("=" * 60)

    spec, valid = _load_and_validate(args.spec, args.live, args.name)
    if not valid:
        print("\nAborting — fix validation errors first.")
        return 1

    if not spec.aes_trigger:
        print("\nError: spec has no aes_trigger section.")
        return 1

    handler = _build_aes_handler(spec)

    # Save handler JSON to output/
    handler_dict = handler.to_dict()
    OUTPUT_DIR.mkdir(exist_ok=True)
    handler_path = OUTPUT_DIR / f"{handler.description}.json"
    with open(handler_path, "w", encoding="utf-8") as f:
        json.dump(handler_dict, f, indent=2, ensure_ascii=False)
    print(f"Handler JSON: {handler_path}")

    # Diff against reference
    if args.diff:
        from scripts.build_credit_handler import compare_handlers

        diff_file = Path(args.diff)
        if not diff_file.exists():
            diff_file = PROJECT_ROOT / args.diff
        if not diff_file.exists():
            print(f"\nError: reference file not found: {args.diff}")
            return 1

        print(f"\n--- AES Handler Comparison vs {diff_file.name} ---")
        with open(diff_file, "r", encoding="utf-8") as f:
            reference = json.load(f)

        diffs = compare_handlers(reference, handler_dict)
        if not diffs:
            print("[OK] Generated handler matches reference structure exactly!")
        else:
            print(f"[!!] Found {len(diffs)} difference(s):")
            for d in diffs:
                print(f"  - {d}")

    if args.deploy:
        if not _deploy_aes_handler(handler, update=getattr(args, 'update', False)):
            return 1

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Check ION workflow status."""
    print("=" * 60)
    print("wfgen status")
    print("=" * 60)

    from scripts.deploy_workflow import get_workflow

    wf = get_workflow(args.workflow_name)
    if wf:
        print(f"\nWorkflow: {wf.get('name')}")
        print(f"Description: {wf.get('description', 'N/A')}")
        print(f"Last Updated: {wf.get('lastUpdatedOn', 'N/A')}")
        print(f"Last Updated By: {wf.get('lastUpdatedBy', 'N/A')}")
        print(f"Archived: {wf.get('archived', 'N/A')}")
    else:
        print(f"\nWorkflow '{args.workflow_name}' not found.")

    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    """Delete ION workflow and optionally deactivate AES handler."""
    print("=" * 60)
    print("wfgen delete")
    print("=" * 60)

    name = args.workflow_name

    # Try to find and deactivate AES handler by description pattern
    if not args.skip_aes:
        from src.aes_builder import AESBuilder
        builder = AESBuilder()
        handler_desc = f"ue_{name}"

        print(f"\nLooking for AES handler: {handler_desc}")
        handlers = builder.load_handlers(
            description_filter=f"%{handler_desc}%",
        )
        if handlers:
            h = handlers[0]
            print(f"  Found: {h.description} (event={h.event_name}, seq={h.sequence})")
            try:
                builder.set_handler_active(h.event_name, h.sequence, active=False)
                print(f"  Deactivated AES handler.")
            except Exception as e:
                print(f"  [WARN] Could not deactivate handler: {e}")
        else:
            print(f"  No AES handler found matching '{handler_desc}'.")

    # Delete ION workflow
    from scripts.deploy_workflow import delete_workflow
    import requests

    print()
    try:
        delete_workflow(name)
        print(f"\nION workflow '{name}' deleted.")
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            print(f"\nION workflow '{name}' not found.")
        else:
            print(f"\n[ERROR] Failed to delete workflow: {e}")
            return 1

    return 0


def _check_service_account(workflow_def: dict) -> tuple[bool, bool]:
    """Check ionapi flowparts for service account status.

    Returns:
        (has_ionapi, has_sa) — whether ionapi flowparts exist and whether
        any of them include a serviceAccount key.
    """
    has_ionapi = False
    has_sa = False

    def _check(flowparts: list[dict]) -> None:
        nonlocal has_ionapi, has_sa
        for fp in flowparts:
            if fp.get("_type") == "ionapi":
                has_ionapi = True
                if "serviceAccount" in fp:
                    has_sa = True
            if fp.get("_type") == "subworkflow":
                _check(fp.get("subFlow", {}).get("flowParts", []))
            if fp.get("_type") == "ifthenelse":
                for branch_key in ("trueBranch", "falseBranch"):
                    _check(fp.get(branch_key, {}).get("flowParts", []))
            if fp.get("_type") == "parallel":
                for seq_flow in fp.get("sequentialFlows", []):
                    _check(seq_flow.get("flowParts", []))

    _check(workflow_def.get("sequentialFlow", {}).get("flowParts", []))
    return has_ionapi, has_sa


def cmd_extract_sa(args: argparse.Namespace) -> int:
    """Extract service account from an existing workflow and save to tenant_config.json."""
    print("=" * 60)
    print("wfgen extract-sa — Extract Service Account")
    print("=" * 60)

    from src.config.tenant import extract_service_account_from_dict

    # Load workflow JSON
    if args.file:
        # From local file
        p = Path(args.file)
        if not p.exists():
            p = PROJECT_ROOT / args.file
        if not p.exists():
            print(f"Error: file not found: {args.file}")
            return 1

        print(f"Source: {p}")
        try:
            with open(p, "r", encoding="utf-8") as f:
                workflow = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON: {e}")
            return 1
    else:
        # From live API
        if not args.workflow_name:
            print("Error: provide a workflow name or use --file")
            return 1

        from scripts.deploy_workflow import get_workflow

        name = args.workflow_name
        print(f"Fetching workflow: {name}")
        workflow = get_workflow(name)
        if workflow is None:
            print(f"Error: workflow '{name}' not found.")
            return 1
        print(f"Fetched: {workflow.get('name', name)}")

    # Extract service account
    sa = extract_service_account_from_dict(workflow)
    if sa is None:
        print("\nNo serviceAccount found in this workflow.")
        print("The workflow must contain at least one ION API activity with a service account attached.")
        return 1

    print(f"\nFound service account ({len(sa)} chars)")
    print(f"Preview: {sa[:50]}...")

    # Update tenant_config.json
    import os

    # Resolve config path (same logic as shared.tenant)
    config_path = None
    env_path = os.environ.get("TENANT_CONFIG")
    if env_path and Path(env_path).exists():
        config_path = Path(env_path)
    else:
        repo_root = PROJECT_ROOT.parent
        candidate = repo_root / "tenant_config.json"
        if candidate.exists():
            config_path = candidate

    if config_path is None:
        print("\nError: tenant_config.json not found.")
        print("Run 'python setup.py' first to create it.")
        return 1

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    old_sa = config.get("service_account", "")
    config["service_account"] = sa

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    # Clear cached config so subsequent commands pick up the new value
    from shared.tenant import clear_cache
    clear_cache()

    print(f"\nUpdated: {config_path}")
    if old_sa and not old_sa.startswith("<"):
        print(f"  (replaced existing {len(old_sa)}-char token)")
    else:
        print(f"  (was: {old_sa[:40] if old_sa else '(empty)'})")

    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="wfgen",
        description="Unified workflow generation CLI — spec to deployed system",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- create ---
    p_create = subparsers.add_parser("create", help="Full pipeline: validate + render + deploy")
    p_create.add_argument("spec", help="Path to spec JSON file")
    p_create.add_argument("--live", action="store_true", help="Include live IDO validation")
    p_create.add_argument("--activate", action="store_true", help="Activate workflow after creation")
    p_create.add_argument("--update", action="store_true", help="Delete and recreate if workflow already exists")
    p_create.add_argument("--name", help="Override workflow name")
    p_create.set_defaults(func=cmd_create)

    # --- render ---
    p_render = subparsers.add_parser("render", help="Validate + render to output/ (no deploy)")
    p_render.add_argument("spec", help="Path to spec JSON file")
    p_render.add_argument("--live", action="store_true", help="Include live IDO validation")
    p_render.add_argument("--diff", help="Reference JSON for structural comparison")
    p_render.add_argument("--name", help="Override workflow name")
    p_render.set_defaults(func=cmd_render)

    # --- validate ---
    p_validate = subparsers.add_parser("validate", help="Validate spec only (no render)")
    p_validate.add_argument("spec", help="Path to spec JSON file")
    p_validate.add_argument("--live", action="store_true", help="Include live IDO validation")
    p_validate.add_argument("--name", help="Override workflow name")
    p_validate.set_defaults(func=cmd_validate)

    # --- aes ---
    p_aes = subparsers.add_parser("aes", help="Build AES handler from spec's aes_trigger")
    p_aes.add_argument("spec", help="Path to spec JSON file")
    p_aes.add_argument("--live", action="store_true", help="Include live IDO validation")
    p_aes.add_argument("--deploy", action="store_true", help="Deploy handler to SyteLine")
    p_aes.add_argument("--update", action="store_true", help="Delete and recreate if handler already exists")
    p_aes.add_argument("--diff", help="Reference handler JSON for comparison")
    p_aes.add_argument("--name", help="Override workflow name")
    p_aes.set_defaults(func=cmd_aes)

    # --- status ---
    p_status = subparsers.add_parser("status", help="Check ION workflow status")
    p_status.add_argument("workflow_name", help="ION workflow name")
    p_status.set_defaults(func=cmd_status)

    # --- delete ---
    p_delete = subparsers.add_parser("delete", help="Delete ION workflow + deactivate AES handler")
    p_delete.add_argument("workflow_name", help="ION workflow name")
    p_delete.add_argument("--skip-aes", action="store_true",
                          help="Skip AES handler deactivation")
    p_delete.set_defaults(func=cmd_delete)

    # --- extract-sa ---
    p_extract = subparsers.add_parser(
        "extract-sa",
        help="Extract service account from existing workflow → tenant_config.json",
    )
    p_extract.add_argument(
        "workflow_name", nargs="?", default=None,
        help="Name of an existing ION workflow to fetch via API",
    )
    p_extract.add_argument(
        "--file", help="Path to a local workflow JSON file (instead of API fetch)",
    )
    p_extract.set_defaults(func=cmd_extract_sa)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
