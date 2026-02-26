#!/usr/bin/env python3
"""
Smoke test for GenAI Agent Factory.

Verifies end-to-end workflow:
1. Invoke Factory Agent with tool request
2. Agent drafts tool specification
3. Send confirmation to create tool
4. Verify tool appears in asset list
5. Cleanup: delete created tool

Exit codes:
    0: Smoke test passed (silent)
    1: Smoke test failed (prints error)

Usage:
    python -m scripts.smoke_test
    python -m scripts.smoke_test --verbose
    python -m scripts.smoke_test --keep-assets
"""

import argparse
import logging
import sys
import time
from typing import Optional, Dict, Any

from src.infor_os.genai_client import GenAIClient
from src.shared.logging import configure_logging

FACTORY_AGENT = "GAF_GenAI_AgentFactory_Agent_v1"
TEST_TOOL_NAME = "GAF_GenAI_HelloWorld_Tool_v1"


def invoke_agent(
    client: GenAIClient,
    prompt: str,
    session: Optional[str] = None
) -> Dict[str, Any]:
    """
    Invoke Factory Agent with prompt.

    Args:
        client: GenAI client instance
        prompt: Prompt to send to agent
        session: Optional session ID for continuation

    Returns:
        Chat response dictionary with session, content, etc.
    """
    return client.chat_sync(
        prompt=prompt,
        tools=[FACTORY_AGENT],
        session=session
    )


def wait_for_asset(
    client: GenAIClient,
    asset_name: str,
    max_wait: int = 30,
    logger: Optional[logging.Logger] = None
) -> Optional[Dict[str, Any]]:
    """
    Poll for asset to appear in list with exponential backoff.

    Args:
        client: GenAI client instance
        asset_name: Name of asset to find
        max_wait: Maximum wait time in seconds
        logger: Optional logger for progress messages

    Returns:
        Asset dictionary if found, None if timeout
    """
    if logger:
        logger.info(f"Waiting for asset: {asset_name} (max {max_wait}s)")

    start_time = time.time()
    wait_interval = 0.5  # Start with 0.5s
    max_interval = 5.0   # Cap at 5s

    while (time.time() - start_time) < max_wait:
        # Check if asset exists
        assets = client.list_tools()
        for asset in assets:
            if asset.get("name") == asset_name:
                if logger:
                    logger.info(f"Asset found: {asset_name} [{asset.get('guid')}]")
                return asset

        # Wait with exponential backoff
        if logger:
            logger.debug(f"Asset not found, waiting {wait_interval}s...")
        time.sleep(wait_interval)

        # Double wait interval, capped at max_interval
        wait_interval = min(wait_interval * 2, max_interval)

    if logger:
        logger.warning(f"Asset not found after {max_wait}s timeout")
    return None


def cleanup_asset(
    client: GenAIClient,
    asset_name: str,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Find and delete asset by name.

    Args:
        client: GenAI client instance
        asset_name: Name of asset to delete
        logger: Optional logger for messages

    Returns:
        True if deleted, False if not found or error
    """
    try:
        # Find asset by name
        assets = client.list_tools()
        for asset in assets:
            if asset.get("name") == asset_name:
                guid = asset.get("guid")
                if logger:
                    logger.info(f"Deleting asset: {asset_name} [{guid}]")
                client.delete_tool(guid)
                if logger:
                    logger.info(f"Deleted asset: {asset_name}")
                return True

        if logger:
            logger.warning(f"Asset not found for cleanup: {asset_name}")
        return False

    except Exception as e:
        if logger:
            logger.error(f"Error during cleanup: {e}")
        return False


def run_smoke_test(verbose: bool = False, keep_assets: bool = False) -> None:
    """
    Run end-to-end smoke test.

    Args:
        verbose: Enable verbose logging
        keep_assets: Skip cleanup (keep created assets)

    Raises:
        Exception: On test failure
    """
    # Configure logging
    level = logging.INFO if verbose else logging.WARNING
    logger = configure_logging(level)

    client = GenAIClient()
    session_id = None
    created = False

    try:
        # Step 1: Invoke agent with tool creation request
        if verbose:
            print(f"\n[Step 1] Invoking Factory Agent...")
        logger.info("Step 1: Requesting tool creation from Factory Agent")

        prompt = (
            f"Create a simple HelloWorld tool named {TEST_TOOL_NAME} "
            "with type API that returns a greeting message"
        )
        response = invoke_agent(client, prompt)

        session_id = response.get("session")
        content = response.get("content", "")

        if verbose:
            # Encode safely for Windows console (replace unencodable chars)
            display_content = content[:200].encode('ascii', errors='replace').decode('ascii')
            print(f"Agent response: {display_content}...")

        # Check for draft indication
        if "CONFIRM" not in content.upper():
            raise Exception("Agent did not provide draft confirmation prompt")

        logger.info("Step 1 complete: Draft received")

        # Step 2: Send confirmation to create tool
        if verbose:
            print(f"\n[Step 2] Confirming tool creation...")
        logger.info("Step 2: Sending confirmation to create tool")

        response = invoke_agent(client, "CONFIRM PUBLISH", session_id)
        content = response.get("content", "")

        if verbose:
            # Encode safely for Windows console (replace unencodable chars)
            display_content = content[:200].encode('ascii', errors='replace').decode('ascii')
            print(f"Agent response: {display_content}...")

        # Check for success indication
        if "created" not in content.lower() and "success" not in content.lower():
            logger.warning("Agent response does not clearly indicate success")

        logger.info("Step 2 complete: Creation confirmed")
        created = True

        # Step 3: Verify tool appears in asset list
        if verbose:
            print(f"\n[Step 3] Verifying tool exists...")
        logger.info("Step 3: Polling for tool in asset list")

        asset = wait_for_asset(client, TEST_TOOL_NAME, max_wait=30, logger=logger)
        if not asset:
            raise Exception(f"Tool {TEST_TOOL_NAME} not found in asset list after 30s")

        if verbose:
            print(f"Tool verified: {asset.get('name')} [{asset.get('guid')[:8]}...]")
        logger.info(f"Step 3 complete: Tool verified [{asset.get('guid')}]")

        # Success
        if verbose:
            print(f"\n[SUCCESS] Smoke test passed\n")
        logger.info("Smoke test PASSED")

    finally:
        # Step 4: Cleanup (unless --keep-assets)
        if created and not keep_assets:
            if verbose:
                print(f"\n[Step 4] Cleaning up...")
            logger.info("Step 4: Cleanup")
            cleanup_asset(client, TEST_TOOL_NAME, logger)
        elif created and keep_assets:
            if verbose:
                print(f"\n[Skipped cleanup - keeping {TEST_TOOL_NAME}]\n")
            logger.info("Cleanup skipped (--keep-assets)")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run smoke test for GenAI Agent Factory",
        epilog="Exit code 0 = success (silent), 1 = failure (prints error)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show progress messages"
    )

    parser.add_argument(
        "--keep-assets",
        action="store_true",
        help="Skip cleanup (keep created assets for inspection)"
    )

    args = parser.parse_args()

    try:
        run_smoke_test(verbose=args.verbose, keep_assets=args.keep_assets)
        sys.exit(0)

    except Exception as e:
        # Print error to stderr on failure
        print(f"SMOKE TEST FAILED: {e}", file=sys.stderr)
        logging.error(f"Smoke test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
