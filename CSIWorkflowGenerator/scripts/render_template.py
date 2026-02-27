"""Render a workflow spec JSON into ION workflow JSON.

Usage:
    python scripts/render_template.py workflow_specs/credit_approval.json
    python scripts/render_template.py workflow_specs/credit_approval.json --diff reference/CS_Credit_Approval_API.json
    python scripts/render_template.py workflow_specs/credit_approval.json --deploy
    python scripts/render_template.py workflow_specs/credit_approval.json --deploy --activate
    python scripts/render_template.py workflow_specs/credit_approval.json --name CS_Credit_Approval_v2
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

OUTPUT_DIR = PROJECT_ROOT / "output"


# --- Structural comparison with normalization ---

# Keys to skip at the top level (metadata that won't match between template and reference)
SKIP_KEYS = {
    "name", "description",
    "lastUpdatedBy", "lastUpdatedOn", "tenant",
    "activationDate", "archived", "sendToDataLake",
}

# Keys to skip at any depth (tenant-specific values that differ between references)
SKIP_KEYS_GLOBAL = {
    "serviceAccount",
}

# Array keys that should be sorted before comparison, with their sort keys
SORT_RULES = {
    "flowParts": "sequenceNumber",
    "variables": "name",
    "parameters": "sequenceNumber",
    "workflowDistributionItems": "name",
    "actionButtons": "sequenceNumber",
    "viewParameters": "name",
    "sequentialFlows": "sequenceNumber",
    "treeElementChildren": "sequence",
}

# String-list array keys that should be sorted (order-independent)
SORT_STRING_LISTS = {
    "variableNamesFromBody",
    "structureNamesFromBody",
}


def _sort_key(item: object, key: str) -> object:
    """Extract sort key from an item, with fallback for non-dict items."""
    if isinstance(item, dict):
        return item.get(key, "")
    return ""


def normalize(obj: object) -> object:
    """Recursively normalize a structure for order-independent comparison.

    Sorts known arrays by their natural keys so that element ordering
    differences don't produce false positives.
    """
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key in SORT_RULES and isinstance(value, list):
                sort_key = SORT_RULES[key]
                result[key] = sorted(
                    [normalize(v) for v in value],
                    key=lambda x, k=sort_key: _sort_key(x, k),
                )
            elif key in SORT_STRING_LISTS and isinstance(value, list):
                result[key] = sorted(value)
            else:
                result[key] = normalize(value)
        return result
    elif isinstance(obj, list):
        return [normalize(v) for v in obj]
    return obj


def deep_compare(ref: object, gen: object, path: str = "") -> list[str]:
    """Recursively compare two normalized structures, returning differences.

    Skips metadata fields and parses JSON-encoded strings for comparison.
    """
    diffs = []

    if isinstance(ref, dict) and isinstance(gen, dict):
        all_keys = set(ref.keys()) | set(gen.keys())
        for key in sorted(all_keys):
            if not path and key in SKIP_KEYS:
                continue
            if key in SKIP_KEYS_GLOBAL:
                continue
            full_path = f"{path}.{key}" if path else key
            if key not in ref:
                diffs.append(f"EXTRA in generated: {full_path}")
            elif key not in gen:
                diffs.append(f"MISSING in generated: {full_path}")
            elif key in ("method", "serializedAssignments", "dueDateJson"):
                # Compare as parsed JSON (key order independent)
                try:
                    ref_parsed = json.loads(ref[key])
                    gen_parsed = json.loads(gen[key])
                    ref_norm = normalize(ref_parsed)
                    gen_norm = normalize(gen_parsed)
                    diffs.extend(deep_compare(ref_norm, gen_norm, f"{full_path}(parsed)"))
                except (json.JSONDecodeError, TypeError):
                    if ref[key] != gen[key]:
                        diffs.append(f"DIFF {full_path}: strings differ")
            else:
                diffs.extend(deep_compare(ref[key], gen[key], full_path))
    elif isinstance(ref, list) and isinstance(gen, list):
        if len(ref) != len(gen):
            diffs.append(f"LENGTH {path}: ref={len(ref)} gen={len(gen)}")
        for i in range(min(len(ref), len(gen))):
            diffs.extend(deep_compare(ref[i], gen[i], f"{path}[{i}]"))
    else:
        if ref != gen:
            diffs.append(f"DIFF {path}: ref={ref!r} gen={gen!r}")

    return diffs


def compare_workflows(reference: dict, generated: dict) -> list[str]:
    """Compare two workflow dicts structurally after normalization."""
    ref_norm = normalize(reference)
    gen_norm = normalize(generated)
    return deep_compare(ref_norm, gen_norm)


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python scripts/render_template.py <spec.json> [options]")
        print("  --diff <reference.json>   Compare against reference")
        print("  --deploy                  Deploy via API")
        print("  --activate                Activate after deploy")
        print("  --name <name>             Override workflow name")
        return 1

    # Parse arguments
    spec_path = None
    diff_path = None
    do_deploy = False
    do_activate = False
    override_name = None

    i = 0
    while i < len(args):
        if args[i] == "--diff" and i + 1 < len(args):
            diff_path = args[i + 1]
            i += 2
        elif args[i] == "--deploy":
            do_deploy = True
            i += 1
        elif args[i] == "--activate":
            do_activate = True
            i += 1
        elif args[i] == "--name" and i + 1 < len(args):
            override_name = args[i + 1]
            i += 2
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
    print("Workflow Template Renderer")
    print("=" * 60)

    # Load spec
    print(f"\nSpec: {spec_file}")
    spec = load_spec(spec_file)

    if override_name:
        spec.name = override_name

    print(f"Workflow: {spec.name}")
    print(f"Description: {spec.description}")
    print(f"Variables (explicit): {len(spec.variables)}")
    print(f"Views: {len(spec.views)}")
    print(f"Flow steps: {len(spec.flow)}")

    # Load tenant config
    tenant = load_default()
    print(f"\nTenant site: {tenant.site}")
    print(f"Service account: {tenant.service_account[:40]}...")

    # Render
    print("\nRendering...")
    result = render(spec, tenant)

    # Write output
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{spec.name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Written to: {output_path}")

    # Summary
    print(f"\nVariables (total): {len(result['variables'])}")
    print(f"Views: {len(result['views'])}")
    print(f"Trees: {len(result['trees'])}")
    print(f"Top-level flowparts: {len(result['sequentialFlow']['flowParts'])}")

    # Diff against reference
    if diff_path:
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
            return 1

    # Deploy
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
