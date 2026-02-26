"""Generate AES event handlers from workflow spec aes_trigger section.

Translates the declarative AesTriggerSpec into an EventHandler with the
proven 7-action ION API pattern (same structure as build_credit_handler.py).

Usage:
    from src.aes_builder.spec_handler import build_handler_from_spec
    handler = build_handler_from_spec(spec, tenant.logical_id)
"""
from __future__ import annotations

import re

from src.templates.schema import WorkflowSpec, AesTriggerSpec
from .models import EventHandler, EventAction
from .expressions import (
    ACTION_FINISH,
    ACTION_NOTIFY,
    ACTION_SET_VALUES,
    ACTION_LOAD_COLLECTION,
    ACTION_INVOKE_METHOD,
    prop,
    var,
    event_param,
    return_var,
    substitute,
    username,
    curdatetime,
    finish_with_result,
    not_condition,
    property_modified,
    setpropvalues_params,
    load_collection_params,
    invoke_method_params,
    notify_params,
    build_ion_workflow_start_params,
)

# Pattern to detect AES function expressions (CONFIGNAME(), ROUND(...), etc.)
_FUNCTION_RE = re.compile(r"^[A-Z_]+\(")


def _is_expression(value: str) -> bool:
    """Check if a workflow_inputs value is an AES expression vs a property name."""
    return bool(_FUNCTION_RE.match(value))


def _build_input_variables(
    workflow_inputs: dict[str, str],
    spec: WorkflowSpec,
) -> dict[str, tuple[str, str]]:
    """Convert spec workflow_inputs to the format expected by build_ion_workflow_start_params.

    Uses the spec's variable declarations to determine the correct dataType
    for each input (e.g. DECIMAL for Discount, STRING for CustNum).

    For each mapping:
    - Plain property name (e.g. "CustNum") -> (var_type, P("CustNum"))
    - Function/expression (e.g. "CONFIGNAME()") -> (var_type, "CONFIGNAME()")
    """
    # Build a lookup of variable name -> declared type
    var_types = {v.name: v.type for v in spec.variables}

    result = {}
    for wf_var, aes_value in workflow_inputs.items():
        data_type = var_types.get(wf_var, "STRING")
        if _is_expression(aes_value):
            result[wf_var] = (data_type, aes_value)
        else:
            result[wf_var] = (data_type, prop(aes_value))
    return result


def build_handler_from_spec(
    spec: WorkflowSpec,
    logical_id: str,
) -> EventHandler:
    """Build an EventHandler from a spec's aes_trigger section.

    Generates the 7-action ION API workflow trigger pattern:
      10: Finish — skip if monitored field not modified
      20: LoadCollection — get old value of monitored field
      25: SetValues — build ION workflow start JSON payload
      30: InvokeMethod — call ION API to start workflow
      35: Notify — optional debug email (only if notify_email set)
      40: SetValues — set InWorkflow=1 + rollback monitored field
      50: InvokeMethod — log to notes (only if notes_ido set)

    Args:
        spec: WorkflowSpec with aes_trigger section populated.
        logical_id: Tenant logical ID (e.g. "lid://infor.syteline.csi/dals").

    Returns:
        EventHandler ready for AESBuilder.create().

    Raises:
        ValueError: If spec.aes_trigger is None.
    """
    if spec.aes_trigger is None:
        raise ValueError("Spec has no aes_trigger section")

    trigger = spec.aes_trigger
    field_name = trigger.monitored_field
    handler_desc = trigger.handler_description or f"ue_{spec.name}"

    actions: list[EventAction] = []

    # Action 10: Finish — skip if monitored field not modified
    finish_msg = f"{field_name} is not modified"
    action_10 = EventAction(
        sequence=10,
        action_type=ACTION_FINISH,
        parameters=finish_with_result(
            not_condition(property_modified(field_name)),
            finish_msg,
        ),
        description=f"Finish - {finish_msg}.",
    )
    actions.append(action_10)

    # Action 20: LoadCollection — get old value of monitored field
    action_20 = EventAction(
        sequence=20,
        action_type=ACTION_LOAD_COLLECTION,
        parameters=load_collection_params(
            trigger.ido,
            f"{field_name}, RowPointer",
            substitute("RowPointer = '{0}'", prop("RowPointer")),
            {f"Old{field_name}": field_name},
        ),
        description=f"Get old {field_name}",
    )
    actions.append(action_20)

    # Action 25: SetValues — build ION workflow start JSON payload
    input_variables = _build_input_variables(trigger.workflow_inputs, spec)
    action_25 = EventAction(
        sequence=25,
        action_type=ACTION_SET_VALUES,
        parameters=build_ion_workflow_start_params(
            spec.name, logical_id, input_variables,
        ),
        description="Set API PARMS",
    )
    actions.append(action_25)

    # Action 30: InvokeMethod — call ION API to start workflow
    action_30 = EventAction(
        sequence=30,
        action_type=ACTION_INVOKE_METHOD,
        parameters=invoke_method_params(
            "IONAPIMethods",
            "InvokeIONAPIMethod2",
            [
                '"False"', '"0"', '"IONSERVICES"', '"POST"',
                '"/process/application/v1/workflow/start"',
                var("PARM"), '"application/json"', '"10000"', '"False"',
                return_var("httpResponseCode"), return_var("response"),
                return_var("responseHeaders"), return_var("infobar"),
            ],
        ),
        description="Start Workflow API",
    )
    actions.append(action_30)

    # Action 35: Notify — optional debug email
    if trigger.notify_email:
        action_35 = EventAction(
            sequence=35,
            action_type=ACTION_NOTIFY,
            parameters=notify_params(
                to=f'"{trigger.notify_email}"',
                subject='"Start Workflow Params"',
                body=substitute("{0}", var("PARM")),
                save_message=False,
            ),
        )
        actions.append(action_35)

    # Action 40: SetValues — set InWorkflow=1 + rollback field to old value
    action_40 = EventAction(
        sequence=40,
        action_type=ACTION_SET_VALUES,
        parameters=setpropvalues_params({
            "InWorkflow": '"1"',
            field_name: event_param(f"Old{field_name}"),
        }),
        description=f"Lock Record & set {field_name} back",
    )
    actions.append(action_40)

    # Action 50: InvokeMethod — log to notes (optional)
    if trigger.notes_ido:
        obj_type = trigger.notes_object_type or "record"
        action_50 = EventAction(
            sequence=50,
            action_type=ACTION_INVOKE_METHOD,
            parameters=invoke_method_params(
                trigger.notes_ido,
                "CreateRemoteNoteSp",
                [
                    f'"{obj_type}"',
                    prop("RowPointer"),
                    '"Approval Workflow Submitted"',
                    substitute(
                        f"{field_name} approval workflow was submitted by {{0}}, at {{1}}.",
                        username(),
                        curdatetime(),
                    ),
                    '"1"',
                    return_var("infobar"),
                ],
            ),
            description="Log in Notes Workflow Start",
        )
        actions.append(action_50)

    return EventHandler(
        event_name=trigger.event,
        sequence=trigger.handler_sequence,
        description=handler_desc,
        ido_collections=trigger.ido,
        synchronous=True,
        suspend=False,
        active=True,
        transactional=False,
        ignore_failure=False,
        overridable=True,
        applies_to_initiators=trigger.applies_to_initiators,
        access_as=trigger.access_as,
        actions=actions,
    )
