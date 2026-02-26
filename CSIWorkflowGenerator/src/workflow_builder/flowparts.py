"""Factory functions for ION workflow flowpart types.

Each function produces a dict matching the exact JSON structure expected
by the ION Process Model API for that flowpart type.
"""
from __future__ import annotations

import json

from .models import (
    ActionButton,
    Assignment,
    DistributionItem,
    DueDate,
    TaskParameter,
)


def usertask(
    name: str,
    seq: int,
    task_type: str,
    message: str,
    distribution: list[DistributionItem],
    parameters: list[TaskParameter],
    action_buttons: list[ActionButton] | None = None,
    action_button_variable: str | None = None,
    priority: str = "Medium",
    due_date: DueDate | None = None,
    propagate_notes: bool = False,
) -> dict:
    """Build a usertask flowpart.

    Args:
        name: Task name.
        seq: Sequence number within the flow.
        task_type: "USER_TASK" or "NOTIFICATION".
        message: Task message (can include [VarName] placeholders).
        distribution: Users/roles to receive the task.
        parameters: Variables/views displayed in the task form.
        action_buttons: Custom action buttons (USER_TASK with CustomActions).
        action_button_variable: Variable to store the selected action value.
        priority: "High", "Medium", or "Low".
        due_date: Due date configuration (USER_TASK only).
        propagate_notes: Whether to carry notes forward.
    """
    is_custom = action_buttons is not None and len(action_buttons) > 0

    d: dict = {
        "_type": "usertask",
        "sequenceNumber": seq,
        "name": name,
    }

    if action_button_variable is not None:
        d["actionButtonVariable"] = action_button_variable

    d["parallel"] = False
    d["priority"] = priority
    d["taskMessage"] = message
    d["taskActionType"] = "CustomActions" if is_custom else "StandardAction"
    d["userTaskType"] = task_type
    d["maxEscalationLevel"] = 1
    d["distributionComplexity"] = "Simple"
    d["propagateNotes"] = propagate_notes

    if due_date is not None:
        d["dueDateJson"] = due_date.to_json_string()

    d["parameters"] = [p.to_dict() for p in parameters]
    d["workflowDistributionItems"] = [di.to_dict() for di in distribution]
    d["taskMessages"] = []
    d["actionButtons"] = [b.to_dict() for b in action_buttons] if action_buttons else []
    d["workflowDecisionTables"] = []
    d["userTaskEscalations"] = []

    if due_date is not None:
        d["dueDate"] = due_date.to_dict()

    return d


def assignment(
    name: str,
    seq: int,
    assignments: list[Assignment],
) -> dict:
    """Build an assignment flowpart.

    Produces both serializedAssignments (JSON string) and
    listOfAllAssignments (list) in sync.
    """
    serialized = json.dumps(
        [a.to_serialized_dict() for a in assignments],
        separators=(",", ":"),
    )

    return {
        "_type": "assignment",
        "sequenceNumber": seq,
        "name": name,
        "assignmentType": "NoAssignment",
        "serializedAssignments": serialized,
        "listOfAllAssignments": [a.to_dict() for a in assignments],
    }


def ionapi_flowpart(
    name: str,
    seq: int,
    ionapi_dict: dict,
    description: str | None = None,
    timeout: int = 600,
    retry_time: int = 600,
    ignore_errors: bool = False,
) -> dict:
    """Build an ionapi flowpart by wrapping ionapi.py output.

    Args:
        name: Flowpart name (e.g. "Get Record").
        seq: Sequence number.
        ionapi_dict: Result from build_ido_load() or build_ido_update().
        description: Optional description text.
        timeout: API call timeout in seconds.
        retry_time: Retry interval in seconds.
        ignore_errors: Whether to continue on API errors.
    """
    d: dict = {
        "_type": "ionapi",
        "sequenceNumber": seq,
        "name": name,
    }
    if description is not None:
        d["description"] = description
    d["timeOut"] = timeout
    d["retryTime"] = retry_time
    d["ignoreErrors"] = ignore_errors
    d.update(ionapi_dict)
    return d


def ifthenelse(
    seq: int,
    condition_xml: str,
    true_branch: list[dict],
    false_branch: list[dict],
) -> dict:
    """Build an ifthenelse flowpart.

    Args:
        seq: Sequence number.
        condition_xml: XML condition string from conditions.build_condition().
        true_branch: List of flowpart dicts for the true path.
        false_branch: List of flowpart dicts for the false path.
    """
    return {
        "_type": "ifthenelse",
        "sequenceNumber": seq,
        "trueBranch": sequential_flow(true_branch),
        "falseBranch": sequential_flow(false_branch),
        "conditionAsString": condition_xml,
    }


def subworkflow(
    name: str,
    seq: int,
    flowparts: list[dict],
    state: int = 1,
) -> dict:
    """Build a subworkflow flowpart.

    Args:
        name: Subworkflow name.
        seq: Sequence number.
        flowparts: List of flowpart dicts within the subworkflow.
        state: Subworkflow state (1 = active).
    """
    return {
        "_type": "subworkflow",
        "sequenceNumber": seq,
        "subFlow": sequential_flow(flowparts),
        "state": state,
        "name": name,
    }


def parallel(
    seq: int,
    join_type: str,
    branches: list[list[dict]],
) -> dict:
    """Build a parallel flowpart.

    Args:
        seq: Sequence number.
        join_type: "ONE_IN" (first branch wins) or "ALL_IN" (all must complete).
        branches: List of branch flowpart lists.
    """
    return {
        "_type": "parallel",
        "sequenceNumber": seq,
        "joinType": join_type,
        "sequentialFlows": [
            sequential_flow(branch, seq=i + 1)
            for i, branch in enumerate(branches)
        ],
    }


def wait(
    name: str,
    seq: int,
    duration: int,
    unit: str = "DAYS",
) -> dict:
    """Build a wait flowpart.

    Args:
        name: Wait step name.
        seq: Sequence number.
        duration: Numeric duration value.
        unit: Time unit (DAYS, HOURS, MINUTES).
    """
    return {
        "_type": "wait",
        "sequenceNumber": seq,
        "name": name,
        "duration": duration,
        "waitUnit": unit,
    }


def sequential_flow(flowparts: list[dict], seq: int = 0) -> dict:
    """Wrap a list of flowparts into a sequentialFlow structure.

    Args:
        flowparts: List of flowpart dicts.
        seq: Sequence number for the flow container (usually 0).
    """
    return {
        "sequenceNumber": seq,
        "flowParts": flowparts,
    }
