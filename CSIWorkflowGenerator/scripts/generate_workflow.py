"""Full workflow pipeline: validate + render + optional deploy.

Composes existing modules — no reimplementation.

Usage:
    python scripts/generate_workflow.py workflow_specs/credit_approval.json
    python scripts/generate_workflow.py workflow_specs/credit_approval.json --live
    python scripts/generate_workflow.py workflow_specs/credit_approval.json --diff reference/CS_Credit_Approval_API.json
    python scripts/generate_workflow.py workflow_specs/credit_approval.json --deploy --activate
    python scripts/generate_workflow.py workflow_specs/credit_approval.json --validate-only
    python scripts/generate_workflow.py workflow_specs/credit_approval.json --name CS_Credit_Approval_v3
"""
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
from src.config.tenant import load_default
from src.parser.validator import SpecValidator

OUTPUT_DIR = PROJECT_ROOT / "output"


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python scripts/generate_workflow.py <spec.json> [options]")
        print("  --live            Include live SyteLine IDO validation")
        print("  --diff <ref.json> Compare against reference workflow")
        print("  --deploy          Deploy to ION")
        print("  --activate        Activate after deploy (implies --deploy)")
        print("  --name <name>     Override workflow name")
        print("  --validate-only   Only validate, skip rendering")
        return 1

    # Parse arguments
    spec_path = None
    diff_path = None
    use_live = False
    do_deploy = False
    do_activate = False
    override_name = None
    validate_only = False

    i = 0
    while i < len(args):
        if args[i] == "--live":
            use_live = True
            i += 1
        elif args[i] == "--diff" and i + 1 < len(args):
            diff_path = args[i + 1]
            i += 2
        elif args[i] == "--deploy":
            do_deploy = True
            i += 1
        elif args[i] == "--activate":
            do_activate = True
            do_deploy = True
            i += 1
        elif args[i] == "--name" and i + 1 < len(args):
            override_name = args[i + 1]
            i += 2
        elif args[i] == "--validate-only":
            validate_only = True
            i += 1
        elif spec_path is None:
            spec_path = args[i]
            i += 1
        else:
            print(f"Unknown argument: {args[i]}")
            return 1

    if spec_path is None:
        print("Error: spec JSON file required")
        return 1

    spec_file = Path(spec_path)
    if not spec_file.exists():
        spec_file = PROJECT_ROOT / spec_path
    if not spec_file.exists():
        print(f"Error: file not found: {spec_path}")
        return 1

    print("=" * 60)
    print("Workflow Generator Pipeline")
    print("=" * 60)

    # --- Step 1: Load spec ---
    print(f"\nSpec: {spec_file}")
    try:
        spec = load_spec(spec_file)
    except Exception as e:
        print(f"\n[FAIL] Failed to parse spec: {e}")
        return 1

    if override_name:
        spec.name = override_name

    print(f"Workflow: {spec.name}")
    print(f"Variables (explicit): {len(spec.variables)}")
    print(f"Views: {len(spec.views)}")
    print(f"Trees: {len(spec.trees)}")
    print(f"Flow steps: {len(spec.flow)}")

    # --- Step 2: Load tenant ---
    tenant = load_default()
    print(f"\nTenant: {tenant.site}")

    # --- Step 3: Validate ---
    live_client = None
    if use_live:
        from src.parser.ido_metadata import IdoMetadataClient
        print("Connecting to SyteLine for live IDO validation...")
        live_client = IdoMetadataClient()

    levels = ["structural", "referential", "tenant"]
    if use_live:
        levels.append("live")
    print(f"Validation levels: {', '.join(levels)}")

    validator = SpecValidator(spec, tenant)
    report = validator.validate(live_client=live_client)

    # Print validation results
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

    if not report.is_valid:
        print("\nAborting — fix validation errors before rendering.")
        return 1

    if validate_only:
        print("\n--validate-only: skipping render/deploy.")
        return 0

    # --- Step 4: Render ---
    print(f"\n--- Rendering ---")
    result = render(spec, tenant)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{spec.name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Written to: {output_path}")

    print(f"Variables (total): {len(result['variables'])}")
    print(f"Views: {len(result['views'])}")
    print(f"Trees: {len(result['trees'])}")
    print(f"Top-level flowparts: {len(result['sequentialFlow']['flowParts'])}")

    # --- Step 5: Diff ---
    if diff_path:
        from scripts.render_template import compare_workflows

        diff_file = Path(diff_path)
        if not diff_file.exists():
            diff_file = PROJECT_ROOT / diff_path
        if not diff_file.exists():
            print(f"\nError: reference file not found: {diff_path}")
            return 1

        print(f"\n--- Structural Comparison vs {diff_file.name} ---")
        with open(diff_file, "r", encoding="utf-8") as f:
            reference = json.load(f)

        diffs = compare_workflows(reference, result)
        if not diffs:
            print("[OK] Generated workflow matches reference structure exactly!")
        else:
            print(f"[!!] Found {len(diffs)} difference(s):")
            for d in diffs:
                print(f"  - {d}")

    # --- Step 6: Deploy ---
    if do_deploy:
        from scripts.deploy_workflow import create_workflow, activate_workflow

        print(f"\n--- Deploying ---")
        create_result = create_workflow(result)
        if create_result is None:
            return 1
        print("Workflow created successfully.")

        if do_activate:
            print()
            activate_workflow(spec.name)
            print(f"Workflow '{spec.name}' is now ACTIVE.")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
