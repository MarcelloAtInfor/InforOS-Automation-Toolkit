"""
Automated end-to-end test harness for the BOM Generator Agent.

Uses GAF_CLI's GenAIClient async chat pattern (POST /chat + polling) to
drive multi-turn BOM creation without the 240s gateway timeout that
plagued chat_sync. Automatically sends "continue" at each checkpoint.

Prompts are auto-generated with unique item codes and dynamic job numbers
via generate_prompt.py.

Usage:
    python test_bom_agent.py --case simple -v
    python test_bom_agent.py --case moderate --verify
    python test_bom_agent.py --prompt "Create a BOM for a wooden table"
    python test_bom_agent.py --all -v
    python test_bom_agent.py --case simple --json
"""

import argparse
import json
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# GAF_CLI import
# ---------------------------------------------------------------------------
GAF_CLI_DIR = Path(__file__).resolve().parent.parent.parent / "GAF_CLI"
sys.path.insert(0, str(GAF_CLI_DIR))

from src.infor_os.genai_client import GenAIClient  # noqa: E402

# ---------------------------------------------------------------------------
# Prompt generator import
# ---------------------------------------------------------------------------
from generate_prompt import (  # noqa: E402
    generate_for_case,
    lookup_next_job_number,
    format_job_number,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AGENT_NAME = "GAF_SyteLine_BomGenerator_Agent_v1"

SENTINEL_COMPLETE = "<<COMPLETE>>"
SENTINEL_CHECKPOINT = "<<CHECKPOINT>>"

SENTINEL_INSTRUCTIONS = (
    "\n\nAt each checkpoint end with <<CHECKPOINT>> "
    "and when fully complete end with <<COMPLETE>>."
)

CASE_NAMES = ["simple", "moderate", "complex"]

# ---------------------------------------------------------------------------
# Sentinel-based response classification
# ---------------------------------------------------------------------------

def classify_response(content: str) -> str:
    """Classify agent response as 'final', 'checkpoint', or 'unknown'."""
    if SENTINEL_COMPLETE in content:
        return "final"
    elif SENTINEL_CHECKPOINT in content:
        return "checkpoint"
    else:
        return "unknown"


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def ensure_log_dir(log_dir: Path) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def write_chunk_to_log(log_file: Path, chunk_num: int, elapsed: float,
                       state: str, prompt_sent: str, content: str):
    """Append one chunk's details to the log file."""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*70}\n")
        f.write(f"CHUNK {chunk_num} | State: {state} | Elapsed: {elapsed:.1f}s\n")
        f.write(f"{'='*70}\n")
        f.write(f"PROMPT SENT: {prompt_sent[:200]}{'...' if len(prompt_sent) > 200 else ''}\n")
        f.write(f"{'-'*70}\n")
        f.write(f"RESPONSE:\n{content}\n")


# ---------------------------------------------------------------------------
# Core test runner (async chat pattern)
# ---------------------------------------------------------------------------

def run_test(client: GenAIClient, prompt: str, *,
             max_chunks: int = 20,
             poll_interval: int = 10,
             max_polls: int = 60,
             agent: str = AGENT_NAME,
             verbose: bool = False,
             log_file: Path = None) -> dict:
    """
    Run a multi-turn BOM generation test using async chat + polling.

    Returns dict with:
        success: bool
        chunks: list of chunk info dicts
        session_id: str or None
        error: str or None (if failed)
        total_elapsed: float
    """
    session_id = uuid.uuid4().hex  # dashless hex for async pattern

    # Only add sentinel instructions if not already present
    if SENTINEL_COMPLETE not in prompt:
        current_prompt = prompt + SENTINEL_INSTRUCTIONS
    else:
        current_prompt = prompt

    chunks = []
    msg_count = 0  # track total messages seen so far
    total_start = time.time()

    for chunk_num in range(1, max_chunks + 1):
        if verbose:
            label = "Initial prompt" if chunk_num == 1 else "continue"
            print(f"  [{chunk_num}] Sending: {label}...", flush=True)

        chunk_start = time.time()

        # --- Submit async ---
        try:
            client.chat(
                prompt=current_prompt,
                tools=[agent],
                session=session_id,
            )
        except Exception as e:
            elapsed = time.time() - chunk_start
            error_msg = str(e)

            if "401" in error_msg or "403" in error_msg:
                error_type = "AUTH_ERROR"
            else:
                error_type = "SUBMIT_ERROR"

            chunk_info = {
                "chunk_num": chunk_num,
                "elapsed": elapsed,
                "state": "error",
                "error_type": error_type,
                "error_msg": error_msg,
                "content": "",
                "has_errors": True,
            }
            chunks.append(chunk_info)

            if verbose:
                print(f"    ERROR ({error_type}) [{elapsed:.1f}s]")

            if log_file:
                write_chunk_to_log(log_file, chunk_num, elapsed, f"error:{error_type}",
                                   current_prompt if chunk_num == 1 else "continue",
                                   f"ERROR: {error_msg}")

            return {
                "success": False,
                "chunks": chunks,
                "session_id": session_id,
                "error": error_type,
                "error_msg": error_msg,
                "total_elapsed": time.time() - total_start,
            }

        # Account for the User message we just sent
        msg_count += 1

        # --- Poll for LLM response ---
        def on_poll(attempt, elapsed, count, expected):
            if verbose:
                if count < 0:
                    print(f"      Poll {attempt} ({elapsed:.0f}s): ERROR", flush=True)
                elif attempt <= 3 or attempt % 6 == 0:
                    print(f"      Poll {attempt} ({elapsed:.0f}s): {count} msgs (expecting > {expected})", flush=True)

        content, msg_count, poll_elapsed = client.poll_for_response(
            session_id=session_id,
            expected_count=msg_count,
            poll_interval=poll_interval,
            max_polls=max_polls,
            on_poll=on_poll,
        )

        elapsed = time.time() - chunk_start

        if content is None:
            # Polling timeout
            chunk_info = {
                "chunk_num": chunk_num,
                "elapsed": elapsed,
                "state": "error",
                "error_type": "POLL_TIMEOUT",
                "error_msg": f"No LLM response after {poll_elapsed:.0f}s polling",
                "content": "",
                "has_errors": True,
            }
            chunks.append(chunk_info)

            if verbose:
                print(f"    TIMEOUT — no response after {poll_elapsed:.0f}s")

            if log_file:
                write_chunk_to_log(log_file, chunk_num, elapsed, "error:POLL_TIMEOUT",
                                   current_prompt if chunk_num == 1 else "continue",
                                   f"TIMEOUT: No LLM response after {poll_elapsed:.0f}s")

            return {
                "success": False,
                "chunks": chunks,
                "session_id": session_id,
                "error": "POLL_TIMEOUT",
                "error_msg": f"No LLM response after {poll_elapsed:.0f}s polling",
                "total_elapsed": time.time() - total_start,
            }

        # --- Classify response ---
        has_debug_errors = "---DEBUG---" in content
        state = classify_response(content)

        chunk_info = {
            "chunk_num": chunk_num,
            "elapsed": elapsed,
            "state": state,
            "content": content,
            "has_errors": has_debug_errors,
        }
        chunks.append(chunk_info)

        if verbose:
            status = state.upper()
            err_flag = " [ERRORS]" if has_debug_errors else ""
            print(f"    {status}{err_flag} [{elapsed:.1f}s]")

        if log_file:
            write_chunk_to_log(log_file, chunk_num, elapsed, state,
                               current_prompt if chunk_num == 1 else "continue",
                               content)

        if state == "unknown" and verbose:
            print(f"    WARNING: No sentinel found in chunk {chunk_num}")
            if has_debug_errors:
                print(f"    WARNING: Agent reported errors (---DEBUG--- block)")

        if state == "final":
            total_elapsed = time.time() - total_start
            return {
                "success": True,
                "chunks": chunks,
                "session_id": session_id,
                "error": None,
                "total_elapsed": total_elapsed,
            }

        # For both checkpoint and unknown, send "continue"
        current_prompt = "continue"

    # Max chunks exceeded
    total_elapsed = time.time() - total_start
    return {
        "success": False,
        "chunks": chunks,
        "session_id": session_id,
        "error": "MAX_CHUNKS_EXCEEDED",
        "total_elapsed": total_elapsed,
    }


# ---------------------------------------------------------------------------
# Result display
# ---------------------------------------------------------------------------

def print_summary(case_name: str, result: dict, gen_info: dict = None):
    """Print a human-readable test summary."""
    status = "PASS" if result["success"] else "FAIL"
    print(f"\n{'='*60}")
    print(f"Test: {case_name} | {status}")
    print(f"{'='*60}")
    if gen_info:
        print(f"  Item code: {gen_info.get('item_code', '(custom)')}")
        print(f"  Job range: {gen_info.get('job_range', '(custom)')}")
    print(f"  Chunks: {len(result['chunks'])}")
    print(f"  Total time: {result['total_elapsed']:.1f}s")
    if result.get("error"):
        print(f"  Error: {result['error']}")

    error_chunks = [c for c in result["chunks"] if c.get("has_errors")]
    if error_chunks:
        print(f"  Chunks with errors: {[c['chunk_num'] for c in error_chunks]}")

    unknown_chunks = [c for c in result["chunks"] if c["state"] == "unknown"]
    if unknown_chunks:
        print(f"  Chunks without sentinel: {[c['chunk_num'] for c in unknown_chunks]}")

    print(f"\n  Chunk timing:")
    for c in result["chunks"]:
        flag = ""
        if c.get("has_errors"):
            flag = " [ERRORS]"
        elif c["state"] == "unknown":
            flag = " [NO SENTINEL]"
        print(f"    Chunk {c['chunk_num']}: {c['elapsed']:.1f}s ({c['state']}){flag}")

    # Show final response excerpt if successful
    if result["success"]:
        final = result["chunks"][-1]["content"]
        if "BOM Generation Complete" in final:
            start = final.find("## BOM Generation Complete")
            excerpt = final[start:start + 500] if start >= 0 else final[:500]
            print(f"\n  Final response excerpt:\n    {excerpt[:500]}...")

    # Show verify command
    if gen_info and gen_info.get("verify_cmd"):
        print(f"\n  Verify: {gen_info['verify_cmd']}")


def results_to_json(results: dict) -> str:
    """Convert results to JSON, stripping large content fields."""
    slim = {}
    for case_name, (result, gen_info) in results.items():
        slim[case_name] = {
            "success": result["success"],
            "total_elapsed": round(result["total_elapsed"], 1),
            "num_chunks": len(result["chunks"]),
            "error": result.get("error"),
            "item_code": gen_info.get("item_code"),
            "job_range": gen_info.get("job_range"),
            "chunks": [
                {
                    "chunk_num": c["chunk_num"],
                    "elapsed": round(c["elapsed"], 1),
                    "state": c["state"],
                    "has_errors": c.get("has_errors", False),
                    "content_length": len(c.get("content", "")),
                }
                for c in result["chunks"]
            ],
        }
    return json.dumps(slim, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Automated end-to-end test for BOM Generator Agent"
    )
    parser.add_argument("--case", choices=CASE_NAMES,
                        help="Built-in test case name")
    parser.add_argument("--prompt", type=str,
                        help="Custom prompt (overrides --case)")
    parser.add_argument("--all", action="store_true",
                        help="Run all built-in test cases")
    parser.add_argument("--verify", action="store_true",
                        help="Run verify_bom.py after completion (not yet implemented)")
    parser.add_argument("--max-chunks", type=int, default=20,
                        help="Max chunks before giving up (default: 20)")
    parser.add_argument("--poll-interval", type=int, default=10,
                        help="Seconds between polls (default: 10)")
    parser.add_argument("--max-polls", type=int, default=60,
                        help="Max poll attempts per chunk (default: 60)")
    parser.add_argument("--agent", type=str, default=AGENT_NAME,
                        help="Agent name override")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose console output")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")
    parser.add_argument("--log-dir", type=str, default="test_logs",
                        help="Directory for log files (default: test_logs/)")

    args = parser.parse_args()

    # Determine which tests to run
    if args.all:
        cases_to_run = list(CASE_NAMES)
    elif args.prompt:
        cases_to_run = ["custom"]
    elif args.case:
        cases_to_run = [args.case]
    else:
        parser.error("Specify --case, --prompt, or --all")

    # Generate prompts with unique item codes and job number ranges
    generated = {}
    if args.prompt:
        generated["custom"] = {
            "prompt": args.prompt,
            "item_code": "(custom)",
            "job_range": "(custom)",
            "verify_cmd": "",
        }
    else:
        next_job = lookup_next_job_number()
        if args.verbose:
            if next_job is not None:
                print(f"Next available job: {format_job_number(next_job)}")
            else:
                print("Job number lookup failed -- using sequence-based fallback")
            print()

        for case_name in cases_to_run:
            gen = generate_for_case(case_name, next_job_override=next_job)
            generated[case_name] = gen
            if next_job is not None:
                next_job += gen["job_reserve"]

    # Setup
    log_dir = ensure_log_dir(
        Path(__file__).parent / args.log_dir
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    client = GenAIClient()

    if args.verbose:
        print(f"Agent: {args.agent}")
        print(f"Max chunks: {args.max_chunks}")
        print(f"Poll: {args.poll_interval}s interval, {args.max_polls} max attempts")
        print(f"Log dir: {log_dir}")
        print()

    # Run tests
    results = {}
    for case_name in cases_to_run:
        gen = generated[case_name]
        prompt = gen["prompt"]
        log_file = log_dir / f"test_{timestamp}_{case_name}.log"

        # Write header to log
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"BOM Generator Agent Test (async)\n")
            f.write(f"Case: {case_name}\n")
            f.write(f"Agent: {args.agent}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Item code: {gen.get('item_code', '(custom)')}\n")
            f.write(f"Job range: {gen.get('job_range', '(custom)')}\n")
            f.write(f"Poll: {args.poll_interval}s interval, {args.max_polls} max\n")
            f.write(f"Prompt:\n{prompt}\n")

        if args.verbose:
            print(f"Running test: {case_name}")
            print(f"  Item code: {gen.get('item_code', '(custom)')}")
            print(f"  Job range: {gen.get('job_range', '(custom)')}")
            print(f"  Prompt: {prompt[:120]}...")

        result = run_test(
            client, prompt,
            max_chunks=args.max_chunks,
            poll_interval=args.poll_interval,
            max_polls=args.max_polls,
            agent=args.agent,
            verbose=args.verbose,
            log_file=log_file,
        )
        results[case_name] = (result, gen)

        if not args.json:
            print_summary(case_name, result, gen)

    # Output
    if args.json:
        print(results_to_json(results))

    # Exit code: 0 if all passed, 1 if any failed
    all_passed = all(r[0]["success"] for r in results.values())
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
