"""Data models for ION workflow components.

Each dataclass has a to_dict() method producing the exact JSON structure
expected by the ION Process Model API.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class WorkflowVariable:
    """A workflow variable definition."""

    name: str
    data_type: str = "STRING"
    workflow_input: bool = False
    workflow_output: bool = False
    use_value: bool = False
    initial_value: str | None = None

    def to_dict(self) -> dict:
        d = {
            "name": self.name,
            "dataType": self.data_type,
            "workflowInput": self.workflow_input,
            "workflowOutput": self.workflow_output,
            "useValue": self.use_value,
        }
        if self.initial_value is not None:
            d["initialValue"] = self.initial_value
        return d


@dataclass
class ViewParameter:
    """A parameter for a drillback view."""

    name: str
    value: str | None = None
    variable: str | None = None

    def to_dict(self) -> dict:
        d: dict = {}
        if self.variable is not None:
            d["variable"] = self.variable
        d["name"] = self.name
        if self.value is not None:
            d["value"] = self.value
        return d


@dataclass
class WorkflowView:
    """A drillback view definition."""

    name: str
    view_set_name: str
    view_name: str
    parameters: list[ViewParameter] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "viewSetName": self.view_set_name,
            "viewName": self.view_name,
            "viewParameters": [p.to_dict() for p in self.parameters],
        }


@dataclass
class DistributionItem:
    """A user/role to distribute a task to."""

    name: str
    distribution_type: str = "USER"
    description: str = ""
    send_email: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "distributionType": self.distribution_type,
            "description": self.description,
            "sendEmail": self.send_email,
        }


@dataclass
class ActionButton:
    """A custom action button on a user task."""

    label: str
    value: str
    sequence_number: int = 0

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
            "sequenceNumber": self.sequence_number,
            "actionButtonLabels": [],
        }


@dataclass
class TaskParameter:
    """A parameter displayed in a user task form."""

    label: str
    sequence_number: int = 0
    read_only: bool = True
    variable: str | None = None
    view: str | None = None
    tree: str | None = None
    completion_property: str = "NOT_APPLICABLE"

    def to_dict(self) -> dict:
        d: dict = {}
        if self.variable is not None:
            d["variable"] = self.variable
        if self.view is not None:
            d["view"] = self.view
        if self.tree is not None:
            d["tree"] = self.tree
        d["label"] = self.label
        d["readOnly"] = self.read_only
        d["sequenceNumber"] = self.sequence_number
        d["completionProperty"] = self.completion_property
        d["labels"] = []
        return d


@dataclass
class Assignment:
    """A variable assignment within an assignment flowpart."""

    variable_name: str
    expression: str
    assignment_type: str = "VALUE_ASSIGNMENT"

    def to_dict(self) -> dict:
        """Compact dict for listOfAllAssignments."""
        return {
            "assignmentType": self.assignment_type,
            "expression": self.expression,
            "variableName": self.variable_name,
        }

    def to_serialized_dict(self) -> dict:
        """Verbose dict for serializedAssignments JSON string (includes null fields)."""
        return {
            "assignmentType": self.assignment_type,
            "expression": self.expression,
            "treePath": None,
            "variableName": self.variable_name,
            "personFullName": None,
        }


@dataclass
class DueDate:
    """Due date configuration for a user task."""

    type: str = "SINCE_CREATION_VALUE"
    since_value: int = 1
    since_time_unit: str = "HOURS"
    variable_name: str | None = None

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "sinceValue": self.since_value,
            "sinceTimeUnit": self.since_time_unit,
        }

    def to_json_string(self) -> str:
        """Produce the dueDateJson string representation."""
        return json.dumps({
            "type": self.type,
            "variableName": self.variable_name,
            "sinceValue": self.since_value,
            "sinceTimeUnit": self.since_time_unit,
        }, separators=(",", ":"))
