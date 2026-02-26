"""Validate a workflow spec JSON file.

Usage:
    python scripts/validate_spec.py templates/credit_approval.json
    python scripts/validate_spec.py templates/credit_approval.json --tenant
    python scripts/validate_spec.py templates/credit_approval.json --live
"""
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root and repo root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT.parent))

from src.templates import load_spec
from src.config.tenant import load_default
from src.parser.validator import SpecValidator


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python scripts/validate_spec.py <spec.json> [options]")
        print("  --tenant  Include tenant config checks (distribution users)")
        print("  --live    Include live SyteLine IDO checks")
        return 1

    # Parse arguments
    spec_path = None
    use_tenant = False
    use_live = False

    i = 0
    while i < len(args):
        if args[i] == "--tenant":
            use_tenant = True
            i += 1
        elif args[i] == "--live":
            use_live = True
            use_tenant = True  # live implies tenant
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
    print("Workflow Spec Validator")
    print("=" * 60)

    # Load spec
    print(f"\nSpec: {spec_file}")
    try:
        spec = load_spec(spec_file)
    except Exception as e:
        print(f"\n[FAIL] Failed to parse spec: {e}")
        return 1

    print(f"Workflow: {spec.name}")
    print(f"Variables: {len(spec.variables)}")
    print(f"Views: {len(spec.views)}")
    print(f"Trees: {len(spec.trees)}")
    print(f"Flow steps: {len(spec.flow)}")

    # Load tenant if needed
    tenant = None
    if use_tenant:
        tenant = load_default()
        print(f"\nTenant: {tenant.site}")
        print(f"Groups: {', '.join(tenant.groups.keys())}")

    # Describe validation levels
    levels = ["structural", "referential"]
    if use_tenant:
        levels.append("tenant")
    if use_live:
        levels.append("live")
    print(f"\nValidation levels: {', '.join(levels)}")

    # Run validation
    validator = SpecValidator(spec, tenant)

    live_client = None
    if use_live:
        from src.parser.ido_metadata import IdoMetadataClient
        print("Connecting to SyteLine for live IDO validation...")
        live_client = IdoMetadataClient()

    report = validator.validate(live_client=live_client)

    # Print results
    print(f"\n{'=' * 60}")
    if report.is_valid and not report.warnings:
        print("[PASS] No issues found!")
    elif report.is_valid:
        print(f"[PASS] Valid with {len(report.warnings)} warning(s)")
    else:
        print(f"[FAIL] {report.summary()}")

    for issue in report.issues:
        icon = "!!" if issue.severity == "error" else "~~"
        print(f"\n  [{icon}] {issue.path}")
        print(f"       {issue.message}")
        if issue.suggestion:
            print(f"       -> {issue.suggestion}")

    print()
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
