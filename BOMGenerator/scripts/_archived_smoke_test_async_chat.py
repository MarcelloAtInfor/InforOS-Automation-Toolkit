#!/usr/bin/env python3
"""
Smoke test: async chat submit + message polling for full BOM generation.

Tests the async pattern end-to-end:
1. POST /api/v1/chat (async, fire-and-forget) to submit BOM prompt
2. GET /api/v1/sessions/{id}/messages to poll for responses
3. Detect <<CHECKPOINT>> sentinels and send "continue"
4. Repeat until <<COMPLETE>> or max chunks reached

Usage:
    python smoke_test_async_chat.py
"""

import sys
import time
import uuid
from pathlib import Path

# GAF_CLI for auth
GAF_CLI_DIR = Path(__file__).resolve().parent.parent.parent / "GAF_CLI"
sys.path.insert(0, str(GAF_CLI_DIR))

from src.infor_os.genai_client import GenAIClient  # noqa: E402
from generate_prompt import generate_for_case  # noqa: E402

AGENT_NAME = "GAF_SyteLine_BomGenerator_Agent_v1"
POLL_INTERVAL = 10   # seconds between polls
MAX_POLLS_PER_CHUNK = 60  # 60 * 10s = 10 min max wait per chunk
MAX_CHUNKS = 20

SENTINEL_COMPLETE = "<<COMPLETE>>"
SENTINEL_CHECKPOINT = "<<CHECKPOINT>>"


def submit_async(client, base, session_id, prompt):
    """POST /api/v1/chat (async). Returns (status, elapsed, body, resolved_session_id)."""
    url = f"{base}/chat"
    payload = {
        "prompt": prompt,
        "tools": [AGENT_NAME],
        "session": session_id,
    }
    t0 = time.time()
    resp = client._request("POST", url, json=payload, timeout=30)
    elapsed = time.time() - t0
    body = resp.json()

    # Extract platform-assigned session ID if present in response
    resolved_id = session_id
    if isinstance(body, dict):
        for key in ("session", "sessionId", "session_id", "id"):
            if key in body and body[key]:
                resolved_id = str(body[key]).replace("-", "")
                break

    return resp.status_code, elapsed, body, resolved_id


def poll_for_new_message(client, base, session_id, expected_count):
    """
    Poll GET /sessions/{id}/messages until message count exceeds expected_count.

    Returns (new_llm_content, new_total_count, poll_elapsed) or (None, count, elapsed) on timeout.
    """
    url = f"{base}/sessions/{session_id}/messages"
    t0 = time.time()

    for attempt in range(1, MAX_POLLS_PER_CHUNK + 1):
        time.sleep(POLL_INTERVAL)
        try:
            resp = client._request("GET", url, timeout=15)
            data = resp.json()
        except Exception as e:
            elapsed = time.time() - t0
            print(f"      Poll {attempt} ({elapsed:.0f}s): ERROR - {e}")
            continue

        # Handle both paginated (items/count) and direct list responses
        if isinstance(data, list):
            items = data
            count = len(data)
        elif isinstance(data, dict):
            items = data.get("items", data.get("messages", []))
            count = data.get("count", data.get("totalCount", len(items)))
        else:
            items = []
            count = 0

        elapsed = time.time() - t0

        # Debug: log every poll on first chunk to diagnose issues
        if attempt <= 3 or attempt % 6 == 0:
            print(f"      Poll {attempt} ({elapsed:.0f}s): {count} msgs (expecting > {expected_count})")

        if count > expected_count:
            # Find the newest LLM message (items are newest-first from API)
            llm_messages = [m for m in items if m.get("sender") == "LLM"]
            if llm_messages:
                newest = llm_messages[0]
                content = newest.get("content", "")
                print(f"      Poll {attempt} ({elapsed:.0f}s): {count} msgs — LLM responded ({len(content)} chars)")
                return content, count, elapsed

    elapsed = time.time() - t0
    return None, expected_count, elapsed


def main():
    client = GenAIClient()
    base = client.chatsvc_base

    # Generate a real BOM prompt
    gen = generate_for_case("simple")
    prompt = gen["prompt"]

    # Platform uses dashless hex GUIDs (e.g., b85ab817c305447782967cf6e009f1cb)
    # uuid.uuid4().hex gives dashless directly
    session_id = uuid.uuid4().hex

    print("=" * 70)
    print("ASYNC BOM SMOKE TEST")
    print("=" * 70)
    print(f"Session:   {session_id}")
    print(f"Chat base: {base}")
    print(f"Item code: {gen['item_code']}")
    print(f"Job range: {gen['job_range']}")
    print(f"Prompt:    {prompt[:120]}...")
    print()

    total_start = time.time()
    msg_count = 0  # track total messages seen so far

    for chunk_num in range(1, MAX_CHUNKS + 1):
        current_prompt = prompt if chunk_num == 1 else "continue"
        label = "Initial BOM prompt" if chunk_num == 1 else "continue"

        # --- Submit ---
        print(f"[Chunk {chunk_num}] Submitting: {label}")
        status, submit_time, body, resolved_id = submit_async(client, base, session_id, current_prompt)
        print(f"  POST /chat: {status} ({submit_time:.2f}s)")
        print(f"  Response body: {body}")

        # Update session_id if platform returned a different one
        if resolved_id != session_id:
            print(f"  Session ID resolved: {session_id} -> {resolved_id}")
            session_id = resolved_id

        # After submit, expect 1 new User message + eventually 1 new LLM message
        msg_count += 1  # the User message we just sent

        # NOTE: With POST /chat (async), messages are NOT stored immediately.
        # Both User + LLM messages appear together once the agent finishes
        # processing (~2-3 min for chunk 1). 0 messages during this period is normal.

        # --- Poll for LLM response ---
        print(f"  Polling for LLM response...")
        content, msg_count, poll_time = poll_for_new_message(
            client, base, session_id, msg_count
        )

        if content is None:
            print(f"  TIMEOUT — no LLM response after {poll_time:.0f}s")
            print(f"\nFAILED at chunk {chunk_num}")
            return 1

        # --- Classify response ---
        total_elapsed = time.time() - total_start

        if SENTINEL_COMPLETE in content:
            print(f"  <<COMPLETE>> detected!")
            print(f"\n{'=' * 70}")
            print(f"SUCCESS — {chunk_num} chunks, {total_elapsed:.0f}s total")
            print(f"{'=' * 70}")
            # Print final summary excerpt
            if "## BOM Generation" in content:
                start = content.find("## BOM Generation")
                print(content[start:start + 800])
            print(f"\nVerify: {gen['verify_cmd']}")
            return 0
        elif SENTINEL_CHECKPOINT in content:
            print(f"  <<CHECKPOINT>> — chunk {chunk_num} done ({poll_time:.0f}s wait, {total_elapsed:.0f}s total)")
            # Show checkpoint summary (first 300 chars)
            if "## Chunk" in content:
                start = content.find("## Chunk")
                print(f"  {content[start:start + 200]}...")
        else:
            print(f"  WARNING: No sentinel found ({poll_time:.0f}s wait)")
            print(f"  Response preview: {content[:300]}...")
            # Continue anyway — agent might just have missed the sentinel

    total_elapsed = time.time() - total_start
    print(f"\nFAILED — max chunks ({MAX_CHUNKS}) exceeded after {total_elapsed:.0f}s")
    return 1


if __name__ == "__main__":
    sys.exit(main())
