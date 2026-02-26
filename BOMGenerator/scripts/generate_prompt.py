#!/usr/bin/env python3
"""
Generate unique, ready-to-use test prompts for the BOM Generator Agent.

Each invocation produces a prompt with:
- Unique item prefix (from local sequence counter)
- Dynamic job number range (from SLHighKeys API lookup)
- Sentinel tokens for automated test harness

Usage:
    python generate_prompt.py                          # Random template
    python generate_prompt.py --template chair         # Specific template
    python generate_prompt.py --desc "custom thing"    # Custom description
    python generate_prompt.py --list                   # Show all templates
    python generate_prompt.py --dry-run                # Preview without incrementing
    python generate_prompt.py | clip                   # Copy to clipboard (Windows)
"""

import argparse
import random
import sys
from pathlib import Path

# Repo root for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.auth import get_auth_headers  # noqa: E402
from shared.config import IDO_URL  # noqa: E402
from shared.tenant import get_site  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SITE = get_site()
SEQUENCE_FILE = Path(__file__).parent / ".test_sequence"
BOM_PREFIX = "BOM"
BOM_PREFIX_LEN = 3
JOB_NUM_DIGITS = 7  # BOM + 7 digits = 10 chars total

# ---------------------------------------------------------------------------
# Template library
# ---------------------------------------------------------------------------
TEMPLATES = {
    "birdhouse": {
        "description": "wooden birdhouse with 2 sub-assemblies (body panel assembly and roof assembly), 6 wall/floor/roof panels, screws, and a perch",
        "item_prefix": "BH",
        "complexity": "simple",
        "job_reserve": 5,
    },
    "stool": {
        "description": "4-legged wooden stool with round seat",
        "item_prefix": "ST",
        "complexity": "simple",
        "job_reserve": 5,
    },
    "chair": {
        "description": "wooden chair with seat, backrest, and 4 legs",
        "item_prefix": "CH",
        "complexity": "moderate",
        "job_reserve": 10,
    },
    "desk-lamp": {
        "description": "desk lamp with weighted base, adjustable arm, and shade",
        "item_prefix": "DL",
        "complexity": "moderate",
        "job_reserve": 10,
    },
    "bookshelf": {
        "description": "3-shelf bookshelf with side panels and back panel",
        "item_prefix": "BS",
        "complexity": "moderate",
        "job_reserve": 10,
    },
    "workbench": {
        "description": "steel workbench with a drawer sub-assembly",
        "item_prefix": "WB",
        "complexity": "complex",
        "levels": 2,
        "job_reserve": 20,
    },
    "bicycle": {
        "description": "mountain bike with wheel and drivetrain sub-assemblies",
        "item_prefix": "MB",
        "complexity": "complex",
        "levels": 2,
        "job_reserve": 20,
    },
    "go-kart": {
        "description": "go-kart with 3 levels of hierarchy: a chassis sub-assembly (which itself contains a rear axle assembly sub-sub-assembly with axle shaft, rear wheels, and brake disc), an engine sub-assembly, and a steering sub-assembly. The chassis-to-rear-axle nesting makes this a true 3-level BOM",
        "item_prefix": "GK",
        "complexity": "complex",
        "levels": 3,
        "job_reserve": 20,
    },
}

# Map test harness case names to templates
CASE_MAP = {
    "simple": "birdhouse",
    "moderate": "chair",
    "complex": "bicycle",
}

COMPLEXITY_DEFAULTS = {"simple": 5, "moderate": 10, "complex": 20}


# ---------------------------------------------------------------------------
# Sequence management
# ---------------------------------------------------------------------------
def read_sequence():
    """Read current sequence number from file. Returns 0 if not found."""
    if SEQUENCE_FILE.exists():
        try:
            return int(SEQUENCE_FILE.read_text().strip())
        except (ValueError, OSError):
            return 0
    return 0


def write_sequence(seq):
    """Write sequence number to file."""
    SEQUENCE_FILE.write_text(str(seq))


def next_sequence(dry_run=False):
    """Get next sequence number, optionally incrementing the file."""
    current = read_sequence()
    next_val = current + 1
    if not dry_run:
        write_sequence(next_val)
    return next_val


def seq_to_prefix(seq):
    """Convert sequence number to unique prefix: 1->T01, 2->T02, etc."""
    return f"T{seq:02d}"


# ---------------------------------------------------------------------------
# SLHighKeys job number lookup
# ---------------------------------------------------------------------------
def lookup_next_job_number():
    """
    Query SLHighKeys for the next available BOM job number.

    Returns the numeric portion (e.g., 2 if last was BOM0000001),
    or None if the lookup fails (auth expired, network error, etc.).
    """
    try:
        import requests
        headers = get_auth_headers()
        headers["X-Infor-MongooseConfig"] = SITE
        url = f"{IDO_URL()}/load/SLHighKeys"
        params = {
            "filter": f"Prefix='{BOM_PREFIX}'",
            "properties": "HighKey",
        }
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        if resp.status_code != 200:
            return None
        items = resp.json().get("Items", [])
        if not items:
            return 1  # No BOM prefix entry yet, start at 1
        high_key = items[0].get("HighKey", "").strip()
        numeric_part = high_key[BOM_PREFIX_LEN:]
        return int(numeric_part) + 1
    except Exception:
        return None


def format_job_number(n):
    """Format a job number: 1 -> BOM0000001."""
    return f"{BOM_PREFIX}{n:0{JOB_NUM_DIGITS}d}"


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------
def build_prompt(description, item_prefix, seq_prefix, next_job, job_reserve,
                 complexity, levels=None):
    """Build the full prompt string with naming rules and sentinels."""
    top_level_code = f"{item_prefix}-{seq_prefix}000"
    job_start = format_job_number(next_job)
    job_end = format_job_number(next_job + job_reserve - 1)

    level_hint = ""
    if levels and levels > 1:
        level_hint = f"{levels}-level "

    return (
        f"Create a {level_hint}BOM for a {description}. "
        f"Use item code {top_level_code} for the top-level item, "
        f"SA-{seq_prefix}- prefix for any sub-assemblies, "
        f"and {seq_prefix}- prefix for components. "
        f"Use job numbers {job_start} through {job_end} sequentially. "
        f"Warehouse: MAIN. "
        f"Announce your estimated chunk count before starting. "
        f"Surface all tool errors with full ---DEBUG--- information. "
        f"At each checkpoint end with <<CHECKPOINT>> "
        f"and when fully complete end with <<COMPLETE>>."
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generate(template_name=None, description=None, complexity=None,
             dry_run=False, next_job_override=None):
    """
    Generate a unique test prompt.

    Args:
        template_name:    Name of a built-in template (e.g., "chair")
        description:      Custom description (overrides template)
        complexity:       Complexity for custom descriptions (simple/moderate/complex)
        dry_run:          If True, don't increment the sequence counter
        next_job_override: Pre-allocated starting job number (for batch generation)

    Returns:
        dict with keys: prompt, item_code, template, complexity, seq, seq_prefix,
                        job_start, job_reserve, job_range, verify_cmd
    """
    levels = None
    if description:
        item_prefix = "CU"
        job_reserve = COMPLEXITY_DEFAULTS.get(complexity or "moderate", 10)
        tmpl_name = "custom"
    elif template_name:
        tmpl = TEMPLATES[template_name]
        description = tmpl["description"]
        item_prefix = tmpl["item_prefix"]
        job_reserve = tmpl["job_reserve"]
        complexity = tmpl["complexity"]
        levels = tmpl.get("levels")
        tmpl_name = template_name
    else:
        # Random template
        tmpl_name = random.choice(list(TEMPLATES.keys()))
        tmpl = TEMPLATES[tmpl_name]
        description = tmpl["description"]
        item_prefix = tmpl["item_prefix"]
        job_reserve = tmpl["job_reserve"]
        complexity = tmpl["complexity"]
        levels = tmpl.get("levels")

    seq = next_sequence(dry_run=dry_run)
    seq_prefix = seq_to_prefix(seq)

    if next_job_override is not None:
        next_job = next_job_override
    else:
        next_job = lookup_next_job_number()
        if next_job is None:
            next_job = seq * 100  # Fallback: non-overlapping sequence-based range

    prompt = build_prompt(description, item_prefix, seq_prefix,
                          next_job, job_reserve, complexity, levels)
    top_level_code = f"{item_prefix}-{seq_prefix}000"

    return {
        "prompt": prompt,
        "item_code": top_level_code,
        "template": tmpl_name,
        "complexity": complexity or "moderate",
        "seq": seq,
        "seq_prefix": seq_prefix,
        "job_start": next_job,
        "job_reserve": job_reserve,
        "job_range": (f"{format_job_number(next_job)} - "
                      f"{format_job_number(next_job + job_reserve - 1)}"),
        "verify_cmd": f"python verify_bom.py {top_level_code} --deep",
    }


def generate_for_case(case_name, dry_run=False, next_job_override=None):
    """Generate a prompt for a test harness case (simple/moderate/complex)."""
    template_name = CASE_MAP.get(case_name, case_name)
    if template_name in TEMPLATES:
        return generate(template_name=template_name, dry_run=dry_run,
                        next_job_override=next_job_override)
    return generate(description=case_name, dry_run=dry_run,
                    next_job_override=next_job_override)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def list_templates():
    """Print the template library."""
    print(f"{'Name':<12} {'Prefix':<8} {'Complexity':<16} {'Jobs':<6} Description")
    print("-" * 85)
    for name, tmpl in TEMPLATES.items():
        lvl = tmpl.get("levels", 1)
        cplx = tmpl["complexity"]
        if lvl > 1:
            cplx += f" ({lvl}-lvl)"
        print(f"{name:<12} {tmpl['item_prefix']:<8} {cplx:<16} "
              f"{tmpl['job_reserve']:<6} {tmpl['description']}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate unique test prompts for BOM Generator Agent",
        epilog="Example: python generate_prompt.py --template chair | clip",
    )
    parser.add_argument("--template", "-t", choices=list(TEMPLATES.keys()),
                        help="Use a specific template")
    parser.add_argument("--desc", "-d", type=str,
                        help="Custom BOM description (overrides --template)")
    parser.add_argument("--complexity", "-c",
                        choices=["simple", "moderate", "complex"],
                        default="moderate",
                        help="Complexity for custom descriptions (default: moderate)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all available templates")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview prompt without incrementing sequence")

    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    result = generate(
        template_name=args.template,
        description=args.desc,
        complexity=args.complexity,
        dry_run=args.dry_run,
    )

    # Prompt to stdout (pipe-friendly), metadata to stderr
    print(result["prompt"])

    print(file=sys.stderr)
    print(f"Template:   {result['template']}", file=sys.stderr)
    print(f"Complexity: {result['complexity']}", file=sys.stderr)
    print(f"Sequence:   {result['seq']} ({result['seq_prefix']})", file=sys.stderr)
    print(f"Item code:  {result['item_code']}", file=sys.stderr)
    print(f"Job range:  {result['job_range']}", file=sys.stderr)
    if args.dry_run:
        print("(dry run -- sequence NOT incremented)", file=sys.stderr)
    print(file=sys.stderr)
    print(f"After test completes, verify with:", file=sys.stderr)
    print(f"  {result['verify_cmd']}", file=sys.stderr)


if __name__ == "__main__":
    main()
