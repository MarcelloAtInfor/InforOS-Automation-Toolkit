"""Preset factory functions: spec step -> Phase 1 flowpart dict.

Each function translates a high-level spec step into the corresponding
Phase 1 builder call(s), producing the exact flowpart dict structure
expected by the ION Process Model API.
"""
from __future__ import annotations

import json

from src.workflow_builder.models import (
    ActionButton,
    Assignment,
    DistributionItem,
    DueDate,
    TaskParameter,
)
from src.workflow_builder.flowparts import (
    usertask,
    assignment,
    ionapi_flowpart,
    ifthenelse,
    subworkflow,
    parallel,
    wait,
)
from src.workflow_builder.conditions import build_condition, build_compound_condition
from src.workflow_builder.ionapi import ApiOutput, build_ido_load, build_ido_update

from .schema import (
    ApprovalTaskStep,
    NotificationStep,
    AssignmentStep,
    IdoBranchStep,
    IdoLoadStep,
    IdoUpdateStep,
    SubworkflowStep,
    ParallelStep,
    WaitStep,
    ConditionStep,
    StepType,
)
from src.config.tenant import TenantConfig


def render_approval_task(
    step: ApprovalTaskStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render an approval task spec into a usertask flowpart dict."""
    distribution = tenant.resolve_distribution(
        step.distribution, send_email=step.send_email
    )
    params = [
        TaskParameter(
            label=p.label,
            sequence_number=i,
            read_only=p.read_only,
            variable=p.variable,
            view=p.view,
            tree=p.tree,
        )
        for i, p in enumerate(step.params)
    ]
    buttons = [
        ActionButton(b.label, b.value, sequence_number=i)
        for i, b in enumerate(step.buttons)
    ]
    due = (
        DueDate(since_value=step.due_date.value, since_time_unit=step.due_date.unit)
        if step.due_date
        else None
    )

    return usertask(
        name=step.name,
        seq=seq,
        task_type="USER_TASK",
        message=step.message,
        distribution=distribution,
        parameters=params,
        action_buttons=buttons,
        action_button_variable=step.button_variable,
        priority=step.priority,
        due_date=due,
        propagate_notes=step.propagate_notes,
    )


def render_notification(
    step: NotificationStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render a notification spec into a usertask flowpart dict."""
    distribution = tenant.resolve_distribution(
        step.distribution, send_email=step.send_email
    )
    params = [
        TaskParameter(
            label=p.label,
            sequence_number=i,
            variable=p.variable,
            view=p.view,
            tree=p.tree,
        )
        for i, p in enumerate(step.params)
    ]

    return usertask(
        name=step.name,
        seq=seq,
        task_type="NOTIFICATION",
        message=step.message,
        distribution=distribution,
        parameters=params,
        propagate_notes=step.propagate_notes,
    )


def render_assignment_step(step: AssignmentStep, seq: int) -> dict:
    """Render an assignment spec into an assignment flowpart dict."""
    assignments = [
        Assignment(
            variable_name=a.variable,
            expression=a.expression,
            assignment_type=a.assignment_type,
        )
        for a in step.assignments
    ]
    return assignment(name=step.name, seq=seq, assignments=assignments)


def render_ido_branch(step: IdoBranchStep, seq: int) -> dict:
    """Render an ido_branch spec into an ifthenelse flowpart dict."""
    condition_xml = _build_condition_xml(step.condition)

    true_assign = assignment(
        name=step.true_assignment.name,
        seq=1,
        assignments=[
            Assignment(
                variable_name=step.true_assignment.variable,
                expression=step.true_assignment.from_variable,
                assignment_type="VARIABLE_ASSIGNMENT",
            )
        ],
    )

    false_assign = assignment(
        name=step.false_assignment.name,
        seq=1,
        assignments=[
            Assignment(
                variable_name=step.false_assignment.variable,
                expression=step.false_assignment.from_variable,
                assignment_type="VARIABLE_ASSIGNMENT",
            )
        ],
    )

    return ifthenelse(
        seq=seq,
        condition_xml=condition_xml,
        true_branch=[true_assign],
        false_branch=[false_assign],
    )


def render_ido_load(
    step: IdoLoadStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render an ido_load spec into an ionapi flowpart dict."""
    output_mappings = [
        ApiOutput(wf_variable_name=var_name, path=json_path)
        for var_name, json_path in step.outputs.items()
    ]

    api_dict = build_ido_load(
        ido_name=step.ido,
        ido_var=step.ido_var,
        properties=step.properties,
        properties_var=step.properties_var,
        filter_var=step.filter_var,
        config_var=step.config_var,
        output_mappings=output_mappings,
        service_account=tenant.service_account,
        auth_literal_value=step.auth_literal,
    )

    return ionapi_flowpart(
        step.name, seq=seq, ionapi_dict=api_dict, description=step.description,
    )


def render_ido_update(
    step: IdoUpdateStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render an ido_update spec into an ionapi flowpart dict."""
    # Build property changes and collect variable names for $value() placeholders
    variable_names: list[str] = []
    properties: list[dict] = []

    for change in step.changes:
        if change.value_var:
            val = f"$value({change.value_var})"
            if change.value_var not in variable_names:
                variable_names.append(change.value_var)
        else:
            val = change.value
        properties.append({
            "IsNull": False,
            "Modified": True,
            "Name": change.property,
            "Value": val,
        })

    # Determine IDO name for body
    if step.ido_var:
        ido_body_name = f"$value({step.ido_var})"
        if step.ido_var not in variable_names:
            variable_names.append(step.ido_var)
    else:
        ido_body_name = step.ido

    # item_id_var goes after property/ido variables
    if step.item_id_var and step.item_id_var not in variable_names:
        variable_names.append(step.item_id_var)

    # Build the update body JSON
    body = {
        "IDOName": ido_body_name,
        "RefreshAfterSave": True,
        "Changes": [
            {
                "Action": 2,
                "ItemId": f"$value({step.item_id_var})",
                "Properties": properties,
            }
        ],
    }
    changes_body = json.dumps(body, indent=2)

    output_mappings = [
        ApiOutput(wf_variable_name=var_name, path=json_path)
        for var_name, json_path in step.outputs.items()
    ]

    api_dict = build_ido_update(
        ido_name=step.ido if step.ido_var is None else None,
        ido_var=step.ido_var,
        changes_body=changes_body,
        variable_names_from_body=variable_names,
        config_var=step.config_var,
        output_mappings=output_mappings,
        service_account=tenant.service_account,
    )

    return ionapi_flowpart(
        step.name, seq=seq, ionapi_dict=api_dict, description=step.description,
    )


def render_subworkflow_step(
    step: SubworkflowStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render a subworkflow spec into a subworkflow flowpart dict."""
    flowparts = []
    for i, child_step in enumerate(step.steps):
        child_seq = i + 1
        flowparts.append(render_step(child_step, child_seq, tenant))
    return subworkflow(name=step.name, seq=seq, flowparts=flowparts)


def render_parallel_step(
    step: ParallelStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render a parallel spec into a parallel flowpart dict."""
    rendered_branches = []
    for branch_steps in step.branches:
        branch_flowparts = []
        for i, child_step in enumerate(branch_steps):
            child_seq = i + 1
            branch_flowparts.append(render_step(child_step, child_seq, tenant))
        rendered_branches.append(branch_flowparts)
    return parallel(seq=seq, join_type=step.join_type, branches=rendered_branches)


def render_wait_step(step: WaitStep, seq: int) -> dict:
    """Render a wait spec into a wait flowpart dict."""
    return wait(name=step.name, seq=seq, duration=step.duration, unit=step.unit)


def _build_condition_xml(condition) -> str:
    """Build XML for a simple or compound condition."""
    if condition.is_compound:
        return build_compound_condition(
            name=condition.name,
            logic=condition.logic,
            conditions=condition.conditions,
        )
    return build_condition(
        name=condition.name,
        variable=condition.variable,
        operator=condition.operator,
        value=condition.value,
    )


def render_condition_step(
    step: ConditionStep, seq: int, tenant: TenantConfig
) -> dict:
    """Render a condition spec into an ifthenelse flowpart dict."""
    condition_xml = _build_condition_xml(step.condition)

    true_flowparts = []
    for i, child_step in enumerate(step.true_steps):
        true_flowparts.append(render_step(child_step, i + 1, tenant))

    false_flowparts = []
    for i, child_step in enumerate(step.false_steps):
        false_flowparts.append(render_step(child_step, i + 1, tenant))

    return ifthenelse(
        seq=seq,
        condition_xml=condition_xml,
        true_branch=true_flowparts,
        false_branch=false_flowparts,
    )


def render_step(step: StepType, seq: int, tenant: TenantConfig) -> dict:
    """Dispatch a step spec to the appropriate render function."""
    if isinstance(step, ApprovalTaskStep):
        return render_approval_task(step, seq, tenant)
    elif isinstance(step, NotificationStep):
        return render_notification(step, seq, tenant)
    elif isinstance(step, AssignmentStep):
        return render_assignment_step(step, seq)
    elif isinstance(step, IdoBranchStep):
        return render_ido_branch(step, seq)
    elif isinstance(step, IdoLoadStep):
        return render_ido_load(step, seq, tenant)
    elif isinstance(step, IdoUpdateStep):
        return render_ido_update(step, seq, tenant)
    elif isinstance(step, SubworkflowStep):
        return render_subworkflow_step(step, seq, tenant)
    elif isinstance(step, ParallelStep):
        return render_parallel_step(step, seq, tenant)
    elif isinstance(step, WaitStep):
        return render_wait_step(step, seq)
    elif isinstance(step, ConditionStep):
        return render_condition_step(step, seq, tenant)
    else:
        raise ValueError(f"Unknown step type: {type(step)}")
