"""
Update GenAI tools and agent to use dynamic site configuration.

Replaces hardcoded X-Infor-MongooseConfig: <YOUR_SITE>
with <site> placeholder for multi-tenant support.

Phase 1: Updates VendorSearch_Tool_v2 as proof of concept
Phase 2: Updates remaining 6 tools
Phase 3: Updates InvoiceAutomation_Agent_v2
"""
import json
import requests
from pathlib import Path
import sys
import re

# Add repo root to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.auth import get_auth_headers
from shared.config import GENAI_CORE_URL

# Tool GUIDs (from log.md)
TOOL_GUIDS = {
    "VendorSearch_Tool_v2": "b7be3168-6771-4114-abe4-8c43530419ad",
    "VendorInsert_Tool_v2": "76ad5987-6071-45b8-a059-a649ded28ecb",
    "ItemSearch_Tool_v2": "f2abd732-2cdd-4238-afda-ab929d65be7b",
    "ItemInsert_Tool_v2": "2762bfa4-f36b-4bb9-9228-310030487cee",
    "PoSearch_Tool_v2": "bdb42c90-7a2f-40ca-951b-64f1c5f5f3af",
    "PoInsert_Tool_v2": "4ed7b512-6fec-4c20-b69d-3b9598c69ecf",
    "PoLineInsert_Tool_v2": "901ce71a-5e5f-4802-9142-5b4a98ab1945",
}

AGENT_GUID = "75a786f6-9926-45ef-bd3c-fd60f469a505"  # InvoiceAutomation_Agent_v2

# Site parameter instruction to add to tools
SITE_PARAM_INSTRUCTION = """

SITE PARAMETER (REQUIRED):
- The <site> placeholder must be filled with the site value from the agent's input
- Format: [TENANT]_DALS (e.g., "<YOUR_SITE>")"""


def get_headers():
    """Get auth headers for API calls."""
    return get_auth_headers()


def fetch_tool(guid: str, headers: dict) -> dict:
    """Fetch a tool definition by GUID."""
    url = f"{GENAI_CORE_URL()}/api/v1/tools/{guid}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"ERROR fetching tool {guid}: {response.status_code}")
        print(response.text)
        return None


def update_tool(tool: dict, headers: dict) -> bool:
    """Update a tool definition via PUT."""
    url = f"{GENAI_CORE_URL()}/api/v1/tools"
    response = requests.put(url, headers=headers, json=tool)
    if response.status_code == 200:
        return True
    else:
        print(f"ERROR updating tool {tool['name']}: {response.status_code}")
        print(response.text)
        return False


def update_api_docs_site(api_docs: str) -> str:
    """Replace hardcoded site with <site> placeholder in api_docs."""
    # Replace hardcoded site value with placeholder
    # Pattern matches "X-Infor-MongooseConfig: <YOUR_SITE>"
    updated = re.sub(
        r'X-Infor-MongooseConfig:\s*<YOUR_SITE>',
        'X-Infor-MongooseConfig: <site>',
        api_docs
    )
    return updated


def update_tool_instructions(instructions: str) -> str:
    """Add site parameter instruction if not already present."""
    if "SITE PARAMETER" in instructions:
        return instructions  # Already has site instruction
    return instructions + SITE_PARAM_INSTRUCTION


def process_tool(name: str, guid: str, headers: dict) -> bool:
    """Fetch, update, and save a single tool."""
    print(f"\n{'='*60}")
    print(f"Processing: {name}")
    print(f"GUID: {guid}")

    # Fetch current definition
    tool = fetch_tool(guid, headers)
    if not tool:
        return False

    # Show current api_docs (first 200 chars)
    current_api_docs = tool.get('data', {}).get('api_docs', '')
    print(f"\nCurrent api_docs (first 200 chars):")
    print(f"  {current_api_docs[:200]}...")

    # Update api_docs
    new_api_docs = update_api_docs_site(current_api_docs)
    tool['data']['api_docs'] = new_api_docs

    # Update instructions
    current_instructions = tool.get('instructions', '')
    new_instructions = update_tool_instructions(current_instructions)
    tool['instructions'] = new_instructions

    # Show changes
    print(f"\nUpdated api_docs (first 200 chars):")
    print(f"  {new_api_docs[:200]}...")

    if "SITE PARAMETER" in new_instructions and "SITE PARAMETER" not in current_instructions:
        print(f"\nAdded SITE PARAMETER instruction to tool instructions")

    # Update via API
    if update_tool(tool, headers):
        print(f"\n[SUCCESS] {name} updated successfully")

        # Save updated definition to file
        output_file = Path(__file__).parent / "v2_definitions" / f"tool_detail_{name}_dynamic_site.json"
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(tool, f, indent=2)
        print(f"Saved to: {output_file}")
        return True
    else:
        print(f"\n[FAILED] {name} update failed")
        return False


def update_agent_workflow(headers: dict) -> bool:
    """Update InvoiceAutomation_Agent_v2 with site input handling."""
    print(f"\n{'='*60}")
    print("Processing: InvoiceAutomation_Agent_v2")
    print(f"GUID: {AGENT_GUID}")

    # Fetch current definition
    agent = fetch_tool(AGENT_GUID, headers)
    if not agent:
        return False

    workflow = agent.get('data', {}).get('workflow', '')

    # Check if already updated
    if '"site":' in workflow and 'SITE CONFIGURATION' in workflow:
        print("\nAgent already has site configuration. Skipping.")
        return True

    # Define the site configuration section
    site_config = """SITE CONFIGURATION (CRITICAL):
- Extract the "site" value from input at START of processing
- Pass this value to ALL tool calls as the <site> placeholder
- If site is NOT provided in input: STOP and ask user to provide the site value before proceeding
- Default site for testing: "<YOUR_SITE>"

"""

    # Update INPUT FORMAT example to include site
    old_input_example = '''{
  "vendor": {'''

    new_input_example = '''{
  "site": "<YOUR_SITE>",
  "vendor": {'''

    # Apply updates to workflow
    updated_workflow = workflow

    # Add site configuration after "INPUT FORMAT:" section header
    if "INPUT FORMAT:" in updated_workflow and "SITE CONFIGURATION" not in updated_workflow:
        updated_workflow = updated_workflow.replace(
            "INPUT FORMAT:\nYou will receive",
            f"{site_config}INPUT FORMAT:\nYou will receive"
        )

    # Update the example JSON to include site
    if old_input_example in updated_workflow:
        updated_workflow = updated_workflow.replace(old_input_example, new_input_example)

    # Update RESPONSE FORMAT to use JSON structure matching RPA expectations
    old_response_start = "6. RESPONSE FORMAT (CRITICAL - USE EXACT FORMAT):"
    new_response_section = """6. RESPONSE FORMAT (CRITICAL - JSON FOR RPA):
   The RPA integration requires a JSON response. Your response MUST be valid JSON matching this structure:

   {
     "status": "success|partial|failed",
     "vendor": {
       "vendorNumber": "[VendNum value]",
       "name": "[Vendor name]",
       "created": true|false
     },
     "items": {
       "created": [count],
       "details": [
         {"itemCode": "[ITEMCODE]", "description": "[Description]", "created": true|false}
       ]
     },
     "purchaseOrder": {
       "poNumber": "[10-char PoNum]",
       "status": "Open",
       "linesCreated": [count]
     },
     "aiModelUpdates": {
       "vendorSimilarity": "Triggered|Not needed|Failed",
       "itemSimilarity": "Triggered|Not needed|Failed"
     },
     "errors": [],
     "notes": "Optional notes about processing"
   }

   STATUS VALUES:
   - "success": All operations completed successfully
   - "partial": Some operations failed (e.g., vendor created but items failed)
   - "failed": Critical failure, unable to complete processing

   IMPORTANT: Return ONLY the JSON object. No markdown formatting, no extra text."""

    if old_response_start in updated_workflow:
        # Find and replace the entire response format section
        # This is more complex, so we'll do a targeted replacement
        response_idx = updated_workflow.find(old_response_start)
        if response_idx != -1:
            # Find where "ERROR HANDLING:" starts (next section)
            error_idx = updated_workflow.find("ERROR HANDLING:", response_idx)
            if error_idx != -1:
                # Replace everything between these two sections
                before = updated_workflow[:response_idx]
                after = updated_workflow[error_idx:]
                updated_workflow = before + new_response_section + "\n\n" + after

    agent['data']['workflow'] = updated_workflow

    # Update via API
    if update_tool(agent, headers):
        print(f"\n[SUCCESS] InvoiceAutomation_Agent_v2 updated successfully")

        # Save updated definition to file
        output_file = Path(__file__).parent / "v2_definitions" / "tool_detail_InvoiceAutomation_Agent_v2_dynamic_site.json"
        with open(output_file, 'w') as f:
            json.dump(agent, f, indent=2)
        print(f"Saved to: {output_file}")
        return True
    else:
        print(f"\n[FAILED] InvoiceAutomation_Agent_v2 update failed")
        return False


def main():
    """Main execution."""
    print("=" * 60)
    print("Dynamic Site Configuration Update")
    print("=" * 60)

    # Parse command line args
    phase = "all"
    if len(sys.argv) > 1:
        phase = sys.argv[1]

    headers = get_headers()
    results = {"success": [], "failed": []}

    if phase in ["1", "phase1", "poc"]:
        # Phase 1: Proof of Concept - VendorSearch_Tool_v2 only
        print("\n[Phase 1] Proof of Concept - VendorSearch_Tool_v2 only")
        name = "VendorSearch_Tool_v2"
        guid = TOOL_GUIDS[name]
        if process_tool(name, guid, headers):
            results["success"].append(name)
        else:
            results["failed"].append(name)

    elif phase in ["2", "phase2", "tools"]:
        # Phase 2: All remaining tools
        print("\n[Phase 2] Remaining 6 tools")
        for name, guid in TOOL_GUIDS.items():
            if name == "VendorSearch_Tool_v2":
                continue  # Skip, already done in Phase 1
            if process_tool(name, guid, headers):
                results["success"].append(name)
            else:
                results["failed"].append(name)

    elif phase in ["3", "phase3", "agent"]:
        # Phase 3: Agent update
        print("\n[Phase 3] Agent update")
        if update_agent_workflow(headers):
            results["success"].append("InvoiceAutomation_Agent_v2")
        else:
            results["failed"].append("InvoiceAutomation_Agent_v2")

    else:
        # All phases
        print("\n[All Phases] Updating all 7 tools + agent")

        # Update all tools
        for name, guid in TOOL_GUIDS.items():
            if process_tool(name, guid, headers):
                results["success"].append(name)
            else:
                results["failed"].append(name)

        # Update agent
        if update_agent_workflow(headers):
            results["success"].append("InvoiceAutomation_Agent_v2")
        else:
            results["failed"].append("InvoiceAutomation_Agent_v2")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Success: {len(results['success'])}")
    for name in results["success"]:
        print(f"  [OK] {name}")

    if results["failed"]:
        print(f"\nFailed: {len(results['failed'])}")
        for name in results["failed"]:
            print(f"  [X] {name}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
