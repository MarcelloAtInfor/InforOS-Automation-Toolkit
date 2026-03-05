"""Build GenAI_WeeklyOrderDateUpdate workflow JSON.

Generates a simple ION workflow that:
1. Calls the GenAI chat sync API with a fixed prompt
2. Sends a notification with the agent's response

Usage:
    python scripts/build_genai_weekly.py                     # Generate JSON only
    python scripts/build_genai_weekly.py --deploy             # Generate + deploy
    python scripts/build_genai_weekly.py --deploy --activate  # Generate + deploy + activate
"""
import json
import sys
from pathlib import Path

# Path setup
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_REPO_ROOT = _PROJECT_ROOT.parent
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT))

from src.workflow_builder.ionapi import (
    ApiInput,
    ApiInputBody,
    ApiOutput,
    _build_ionapi_method,
    _is_placeholder_sa,
)
from src.workflow_builder.flowparts import ionapi_flowpart, usertask, sequential_flow
from src.workflow_builder.models import DistributionItem, TaskParameter
from src.config.tenant import load_default

OUTPUT_DIR = _PROJECT_ROOT / "output"

# --- Workflow configuration ---
WORKFLOW_NAME = "GenAI_WeeklyOrderDateUpdate"
PROMPT_TEXT = "Run weekly order date update"
DESCRIPTION = (
    "Scheduled workflow: calls GenAI chat sync API with a fixed prompt "
    "and sends a notification with the agent response."
)

# GenAI product identifiers (from swagger: GENAI/chatsvc)
GENAI_PRODUCT_ID = "infor.genai"
GENAI_PRODUCT_NAME = "Infor GenAI"
GENAI_PROXY_PATH = "GENAI/chatsvc"
GENAI_REST_PATH = "/api/v1/chat/sync"


def build_genai_chat_sync(
    prompt: str,
    response_var: str = "AgentResponse",
    service_account: str = "",
) -> dict:
    """Build an ionapi dict for GenAI chat sync POST.

    Args:
        prompt: The chat prompt text.
        response_var: Workflow variable to store the response content.
        service_account: Encrypted service account token.

    Returns:
        Dict with method, ionApiMethod, serviceAccount, isCustom keys.
    """
    inputs = [
        ApiInput(
            name="Authorization",
            description=(
                "OAuth 2.0 Bearer token (filled automatically by ION runtime)."
            ),
            swagger_datatype="string",
            required=False,
            type="HEADER",
        ),
    ]

    outputs = [
        ApiOutput(
            wf_variable_name=response_var,
            path="$.content",
            type="BODY",
            optional=False,
        ),
    ]

    # JSON body with the prompt
    body_json = json.dumps({"prompt": prompt}, separators=(",", ":"))

    input_body = ApiInputBody(
        name="body",
        description="GenAI ChatRequest payload",
        required=True,
        available_input_content_types=["JSON"],
        input_content_type="JSON",
        body=body_json,
        ignore=False,
    )

    compact, method_str = _build_ionapi_method(
        product_logical_id=GENAI_PRODUCT_ID,
        operation_proxy_path=GENAI_PROXY_PATH,
        operation_rest_path=GENAI_REST_PATH,
        product_name=GENAI_PRODUCT_NAME,
        summary="RunChatSync",
        http_method="POST",
        inputs=inputs,
        outputs=outputs,
        input_body=input_body,
    )

    result = {
        "method": method_str,
        "isCustom": True,
        "ionApiMethod": compact,
    }
    if not _is_placeholder_sa(service_account):
        result["serviceAccount"] = service_account
    return result


def build_workflow() -> dict:
    """Build the complete workflow JSON."""
    tenant = load_default()

    # --- Variables ---
    variables = [
        {
            "name": "AgentResponse",
            "dataType": "STRING",
            "workflowInput": False,
            "workflowOutput": False,
            "useValue": False,
        },
    ]

    # --- Step 1: Call GenAI chat sync API ---
    genai_call = ionapi_flowpart(
        name="Invoke GenAI Agent",
        seq=1,
        ionapi_dict=build_genai_chat_sync(
            prompt=PROMPT_TEXT,
            response_var="AgentResponse",
            service_account=tenant.service_account,
        ),
        description="POST to GenAI chat sync with weekly order update prompt",
        timeout=600,
        retry_time=60,
        ignore_errors=False,
    )

    # --- Step 2: Notification with agent response ---
    distribution = tenant.resolve_distribution("marcello")
    notification = usertask(
        name="Agent Response",
        seq=2,
        task_type="NOTIFICATION",
        message="Weekly Order Date Update completed. Agent response: [AgentResponse]",
        distribution=distribution,
        parameters=[
            TaskParameter(variable="AgentResponse", label="Agent Response", sequence_number=1),
        ],
    )

    # --- Assemble workflow ---
    workflow = {
        "name": WORKFLOW_NAME,
        "description": DESCRIPTION,
        "variables": variables,
        "views": [],
        "trees": [],
        "sequentialFlow": sequential_flow([genai_call, notification]),
    }

    return workflow


def main():
    args = sys.argv[1:]
    do_deploy = "--deploy" in args
    do_activate = "--activate" in args

    workflow = build_workflow()

    # Write JSON
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{WORKFLOW_NAME}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2)
    print(f"Generated: {output_path}")

    if do_deploy:
        from scripts.deploy_workflow import create_workflow, activate_workflow

        result = create_workflow(workflow)
        if result and do_activate:
            activate_workflow(WORKFLOW_NAME)


if __name__ == "__main__":
    main()
