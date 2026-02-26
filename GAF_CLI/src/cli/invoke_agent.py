#!/usr/bin/env python3
"""
Invoke a GenAI agent via Chat API.

CLI-05: invoke_agent.py - invoke agent for testing and interactive use.

Usage:
    python -m src.cli.invoke_agent "List all Factory tools"
    python -m src.cli.invoke_agent -i
    python -m src.cli.invoke_agent "Create a tool" -s <session-id>
    python -m src.cli.invoke_agent --agent GAF_SyteLine_BomGenerator_Agent_v1 "Create a chair BOM"
    python -m src.cli.invoke_agent -a GAF_SyteLine_BomGenerator_Agent_v1 -i
    python -m src.cli.invoke_agent --async "List all tools with prefix GAF_SyteLine"

Exit codes:
    0: Success
    1: Error (API error, invalid input)
"""

import argparse
import json
import logging
import sys
import uuid
from typing import List

from src.infor_os.genai_client import GenAIClient
from src.shared.logging import configure_logging

# Default agent when --agent is not specified
DEFAULT_AGENT = "GAF_GenAI_AgentFactory_Agent_v1"


def _poll_callback(attempt, elapsed, count, expected):
    """Default on_poll callback for console output."""
    if count < 0:
        print(f"  Poll {attempt} ({elapsed:.0f}s): ERROR", flush=True)
    elif attempt <= 3 or attempt % 6 == 0:
        print(f"  Poll {attempt} ({elapsed:.0f}s): {count} msgs (expecting > {expected})", flush=True)


def run_single(client: GenAIClient, prompt: str, agent: List[str],
               session: str = None, output_json: bool = False,
               use_async: bool = False, poll_interval: int = 10,
               max_polls: int = 60):
    """Single prompt invocation."""
    if not use_async:
        response = client.chat_sync(
            prompt=prompt,
            tools=agent,
            session=session
        )

        if output_json:
            print(json.dumps(response, indent=2))
        else:
            print(f"\nSession: {response.get('session')}")
            print(f"\n{response.get('content', '')}\n")

            # Show followups if available
            followups = response.get('followups')
            if followups:
                print("Suggested followups:")
                for f in followups:
                    print(f"  - {f}")
                print()
        return

    # Async mode: POST /chat + poll for response
    session_id = session or uuid.uuid4().hex
    print(f"Session: {session_id}")
    print(f"Submitting async...", flush=True)

    submit_response = client.chat(
        prompt=prompt,
        tools=agent,
        session=session_id
    )
    print(f"Submitted: {submit_response}")

    # After submit, expect 1 new User message + 1 new LLM message
    msg_count = 0  # fresh session starts at 0
    if session:
        # Existing session — query current count first
        try:
            current = client.get_session_messages(session_id)
            msg_count = current.get("count", 0)
        except Exception:
            pass
    msg_count += 1  # account for the User message we just sent

    print(f"Polling for response (interval={poll_interval}s, max={max_polls})...", flush=True)
    content, new_count, elapsed = client.poll_for_response(
        session_id=session_id,
        expected_count=msg_count,
        poll_interval=poll_interval,
        max_polls=max_polls,
        on_poll=_poll_callback
    )

    if content is None:
        print(f"\nTimeout after {elapsed:.0f}s — no response received.")
        sys.exit(1)

    if output_json:
        print(json.dumps({
            "session": session_id,
            "content": content,
            "elapsed": round(elapsed, 1),
            "message_count": new_count,
        }, indent=2))
    else:
        print(f"\nAgent ({elapsed:.1f}s):\n{content}\n")


def run_interactive(client: GenAIClient, agent: List[str],
                    use_async: bool = False, poll_interval: int = 10,
                    max_polls: int = 60):
    """Interactive chat session with session continuity."""
    session_id = uuid.uuid4().hex if use_async else str(uuid.uuid4())
    mode_label = "async" if use_async else "sync"
    print(f"Agent: {agent[0]}")
    print(f"Session: {session_id} ({mode_label})")
    print("Type 'quit' to exit\n")

    msg_count = 0  # track message count for async polling

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if prompt.lower() in ('quit', 'exit', 'q'):
            break

        if not prompt:
            continue

        try:
            if not use_async:
                response = client.chat_sync(
                    prompt=prompt,
                    tools=agent,
                    session=session_id
                )
                print(f"\nAgent: {response.get('content', '')}\n")

                followups = response.get('followups')
                if followups:
                    print("Suggestions:")
                    for f in followups:
                        print(f"  - {f}")
                    print()
            else:
                client.chat(
                    prompt=prompt,
                    tools=agent,
                    session=session_id
                )
                msg_count += 1  # User message

                print(f"  Polling...", flush=True)
                content, msg_count, elapsed = client.poll_for_response(
                    session_id=session_id,
                    expected_count=msg_count,
                    poll_interval=poll_interval,
                    max_polls=max_polls,
                    on_poll=_poll_callback
                )

                if content is None:
                    print(f"\n  Timeout after {elapsed:.0f}s\n")
                else:
                    print(f"\nAgent ({elapsed:.1f}s): {content}\n")

        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Invoke a GenAI agent via Chat API",
        epilog="Examples:\n"
               "  python -m src.cli.invoke_agent 'List all Factory tools'\n"
               "  python -m src.cli.invoke_agent -a GAF_SyteLine_BomGenerator_Agent_v1 'Create a chair BOM'\n"
               "  python -m src.cli.invoke_agent -a GAF_SyteLine_BomGenerator_Agent_v1 -i\n"
               "  python -m src.cli.invoke_agent --async 'List tools with prefix GAF_SyteLine'",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt to send to agent (omit for interactive mode)"
    )

    parser.add_argument(
        "-a", "--agent",
        default=DEFAULT_AGENT,
        help=f"Agent name to invoke (default: {DEFAULT_AGENT})"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive chat session"
    )

    parser.add_argument(
        "-s", "--session",
        help="Session ID to continue (for multi-turn, single-shot mode)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output raw JSON response"
    )

    parser.add_argument(
        "--async",
        action="store_true",
        dest="use_async",
        help="Use async chat (POST /chat + polling) instead of sync"
    )

    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds between polls in async mode (default: 10)"
    )

    parser.add_argument(
        "--max-polls",
        type=int,
        default=60,
        help="Max poll attempts in async mode (default: 60)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    configure_logging(level)

    # Validate args
    if not args.prompt and not args.interactive:
        parser.error("Either provide a prompt or use --interactive")

    # Wrap agent name in list for chat tools parameter
    agent = [args.agent]

    try:
        client = GenAIClient()

        if args.interactive:
            run_interactive(client, agent, use_async=args.use_async,
                            poll_interval=args.poll_interval,
                            max_polls=args.max_polls)
        else:
            run_single(client, args.prompt, agent, args.session,
                        args.output_json, use_async=args.use_async,
                        poll_interval=args.poll_interval,
                        max_polls=args.max_polls)

        sys.exit(0)

    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
