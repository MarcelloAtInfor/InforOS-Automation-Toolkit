"""Dataclasses for workflow spec structure.

A WorkflowSpec is the compact JSON representation of a workflow that gets
rendered into full ION workflow JSON via the presets and renderer modules.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# --- Supporting types ---


@dataclass
class VariableSpec:
    """A workflow variable declaration."""

    name: str
    type: str = "STRING"
    input: bool = False
    output: bool = False
    initial_value: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> VariableSpec:
        return cls(
            name=d["name"],
            type=d.get("type", "STRING"),
            input=d.get("input", False),
            output=d.get("output", False),
            initial_value=d.get("initial_value"),
        )


@dataclass
class ViewSpec:
    """A drillback view declaration."""

    name: str
    view_set: str
    view: str
    params: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> ViewSpec:
        return cls(
            name=d["name"],
            view_set=d["view_set"],
            view=d["view"],
            params=d.get("params", {}),
        )


@dataclass
class ButtonSpec:
    """An action button on an approval task."""

    label: str
    value: str

    @classmethod
    def from_dict(cls, d: dict) -> ButtonSpec:
        return cls(label=d["label"], value=d["value"])


@dataclass
class ParamSpec:
    """A parameter displayed in a user task form."""

    label: str
    variable: str | None = None
    view: str | None = None
    tree: str | None = None
    read_only: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> ParamSpec:
        return cls(
            label=d["label"],
            variable=d.get("variable"),
            view=d.get("view"),
            tree=d.get("tree"),
            read_only=d.get("read_only", True),
        )


@dataclass
class DueDateSpec:
    """Due date configuration."""

    value: int = 1
    unit: str = "HOURS"

    @classmethod
    def from_dict(cls, d: dict) -> DueDateSpec:
        return cls(value=d.get("value", 1), unit=d.get("unit", "HOURS"))


@dataclass
class ConditionSpec:
    """A condition for branching.

    Simple condition: name + variable + operator + value.
    Compound condition: name + logic (AND/OR) + conditions (list of simple ConditionSpec).
    """

    name: str
    variable: str = ""
    operator: str = ""
    value: str = ""
    logic: str | None = None
    conditions: list[ConditionSpec] | None = None

    @property
    def is_compound(self) -> bool:
        return self.logic is not None and self.conditions is not None

    @classmethod
    def from_dict(cls, d: dict) -> ConditionSpec:
        sub_conditions = None
        if "conditions" in d:
            sub_conditions = [ConditionSpec.from_dict(c) for c in d["conditions"]]
        return cls(
            name=d["name"],
            variable=d.get("variable", ""),
            operator=d.get("operator", ""),
            value=d.get("value", ""),
            logic=d.get("logic"),
            conditions=sub_conditions,
        )


@dataclass
class BranchAssignmentSpec:
    """A variable assignment in one branch of an ido_branch."""

    name: str
    variable: str
    from_variable: str

    @classmethod
    def from_dict(cls, d: dict) -> BranchAssignmentSpec:
        return cls(
            name=d["name"],
            variable=d["variable"],
            from_variable=d["from_variable"],
        )


@dataclass
class AssignmentEntrySpec:
    """A single variable assignment."""

    variable: str
    expression: str
    assignment_type: str = "VALUE_ASSIGNMENT"

    @classmethod
    def from_dict(cls, d: dict) -> AssignmentEntrySpec:
        return cls(
            variable=d["variable"],
            expression=d["expression"],
            assignment_type=d.get("assignment_type", "VALUE_ASSIGNMENT"),
        )


@dataclass
class ChangeSpec:
    """A property change in an IDO update."""

    property: str
    value_var: str | None = None
    value: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> ChangeSpec:
        return cls(
            property=d["property"],
            value_var=d.get("value_var"),
            value=d.get("value"),
        )


# --- Tree spec types ---


@dataclass
class TreeFieldSpec:
    """A leaf field in a tree definition."""

    name: str
    label: str
    sequence: int = 0
    data_type: str = "STRING"

    @classmethod
    def from_dict(cls, d: dict) -> TreeFieldSpec:
        return cls(
            name=d["name"],
            label=d["label"],
            sequence=d.get("sequence", 0),
            data_type=d.get("data_type", "STRING"),
        )

    def to_dict(self) -> dict:
        return {
            "_type": "field",
            "name": self.name,
            "label": self.label,
            "sequence": self.sequence,
            "treeLabels": [],
            "dataType": self.data_type,
        }


@dataclass
class TreeNodeSpec:
    """A branch node in a tree definition (contains children)."""

    name: str
    label: str
    sequence: int = 0
    children: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> TreeNodeSpec:
        children = [_tree_child_from_dict(c) for c in d.get("children", [])]
        return cls(
            name=d["name"],
            label=d["label"],
            sequence=d.get("sequence", 0),
            children=children,
        )

    def to_dict(self) -> dict:
        return {
            "_type": "node",
            "name": self.name,
            "label": self.label,
            "sequence": self.sequence,
            "treeLabels": [],
            "treeElementChildren": [c.to_dict() for c in self.children],
        }


@dataclass
class TreeSpec:
    """A tree definition for hierarchical data display in tasks."""

    name: str
    label: str
    children: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> TreeSpec:
        children = [_tree_child_from_dict(c) for c in d.get("children", [])]
        return cls(
            name=d["name"],
            label=d["label"],
            children=children,
        )

    def to_dict(self) -> dict:
        return {
            "_type": "tree",
            "name": self.name,
            "label": self.label,
            "sequence": 0,
            "treeLabels": [],
            "treeElementChildren": [c.to_dict() for c in self.children],
        }


def _tree_child_from_dict(d: dict) -> TreeFieldSpec | TreeNodeSpec:
    """Parse a tree child dict into field or node."""
    if d.get("type") == "node" or "children" in d:
        return TreeNodeSpec.from_dict(d)
    return TreeFieldSpec.from_dict(d)


# --- Flow step types ---


@dataclass
class ApprovalTaskStep:
    """An approval user task with action buttons."""

    type: str
    name: str
    message: str
    distribution: str | list[str]
    params: list[ParamSpec]
    buttons: list[ButtonSpec]
    button_variable: str
    send_email: bool = False
    priority: str = "Medium"
    due_date: DueDateSpec | None = None
    propagate_notes: bool = False


@dataclass
class NotificationStep:
    """A notification task (no action buttons)."""

    type: str
    name: str
    message: str
    distribution: str | list[str]
    params: list[ParamSpec]
    send_email: bool = False
    propagate_notes: bool = False


@dataclass
class AssignmentStep:
    """A variable assignment step."""

    type: str
    name: str
    assignments: list[AssignmentEntrySpec]


@dataclass
class IdoBranchStep:
    """An if/then/else with two variable assignments."""

    type: str
    condition: ConditionSpec
    true_assignment: BranchAssignmentSpec
    false_assignment: BranchAssignmentSpec


@dataclass
class IdoLoadStep:
    """An IDO load (GET) API call."""

    type: str
    name: str
    ido: str | None = None
    ido_var: str | None = None
    properties: str | None = None
    properties_var: str | None = None
    filter_var: str = ""
    outputs: dict[str, str] = field(default_factory=dict)
    config_var: str = "MGConfig"
    description: str | None = None
    auth_literal: str | None = None


@dataclass
class IdoUpdateStep:
    """An IDO update (POST) API call."""

    type: str
    name: str
    ido: str | None = None
    ido_var: str | None = None
    changes: list[ChangeSpec] = field(default_factory=list)
    item_id_var: str = ""
    outputs: dict[str, str] = field(default_factory=dict)
    config_var: str = "MGConfig"
    description: str | None = None


@dataclass
class SubworkflowStep:
    """A subworkflow containing child steps."""

    type: str
    name: str
    steps: list  # list of step objects (any type)


@dataclass
class ParallelStep:
    """A parallel flowpart with multiple branches."""

    type: str
    join_type: str  # "ONE_IN" or "ALL_IN"
    branches: list  # list of lists of step objects


@dataclass
class WaitStep:
    """A wait/timer flowpart."""

    type: str
    name: str
    duration: int
    unit: str = "DAYS"


@dataclass
class ConditionStep:
    """A generic if/then/else with arbitrary step branches."""

    type: str
    condition: ConditionSpec
    true_steps: list  # list of step objects for true branch
    false_steps: list  # list of step objects for false branch


# Union type for all step types
StepType = (
    ApprovalTaskStep
    | NotificationStep
    | AssignmentStep
    | IdoBranchStep
    | IdoLoadStep
    | IdoUpdateStep
    | SubworkflowStep
    | ParallelStep
    | WaitStep
    | ConditionStep
)


def step_from_dict(d: dict) -> StepType:
    """Parse a step dict into the appropriate dataclass."""
    t = d.get("type")
    if not t:
        raise ValueError(f"Step missing 'type' field: {d}")

    if t == "approval_task":
        return ApprovalTaskStep(
            type=t,
            name=d["name"],
            message=d["message"],
            distribution=d["distribution"],
            params=[ParamSpec.from_dict(p) for p in d.get("params", [])],
            buttons=[ButtonSpec.from_dict(b) for b in d.get("buttons", [])],
            button_variable=d["button_variable"],
            send_email=d.get("send_email", False),
            priority=d.get("priority", "Medium"),
            due_date=DueDateSpec.from_dict(d["due_date"]) if "due_date" in d else None,
            propagate_notes=d.get("propagate_notes", False),
        )
    elif t == "notification":
        return NotificationStep(
            type=t,
            name=d["name"],
            message=d["message"],
            distribution=d["distribution"],
            params=[ParamSpec.from_dict(p) for p in d.get("params", [])],
            send_email=d.get("send_email", False),
            propagate_notes=d.get("propagate_notes", False),
        )
    elif t == "assignment":
        return AssignmentStep(
            type=t,
            name=d["name"],
            assignments=[AssignmentEntrySpec.from_dict(a) for a in d["assignments"]],
        )
    elif t == "ido_branch":
        return IdoBranchStep(
            type=t,
            condition=ConditionSpec.from_dict(d["condition"]),
            true_assignment=BranchAssignmentSpec.from_dict(d["true_assignment"]),
            false_assignment=BranchAssignmentSpec.from_dict(d["false_assignment"]),
        )
    elif t == "ido_load":
        return IdoLoadStep(
            type=t,
            name=d["name"],
            ido=d.get("ido"),
            ido_var=d.get("ido_var"),
            properties=d.get("properties"),
            properties_var=d.get("properties_var"),
            filter_var=d.get("filter_var", ""),
            outputs=d.get("outputs", {}),
            config_var=d.get("config_var", "MGConfig"),
            description=d.get("description"),
            auth_literal=d.get("auth_literal"),
        )
    elif t == "ido_update":
        return IdoUpdateStep(
            type=t,
            name=d["name"],
            ido=d.get("ido"),
            ido_var=d.get("ido_var"),
            changes=[ChangeSpec.from_dict(c) for c in d.get("changes", [])],
            item_id_var=d.get("item_id_var", ""),
            outputs=d.get("outputs", {}),
            config_var=d.get("config_var", "MGConfig"),
            description=d.get("description"),
        )
    elif t == "subworkflow":
        return SubworkflowStep(
            type=t,
            name=d["name"],
            steps=[step_from_dict(s) for s in d["steps"]],
        )
    elif t == "parallel":
        branches = [
            [step_from_dict(s) for s in branch]
            for branch in d["branches"]
        ]
        return ParallelStep(
            type=t,
            join_type=d["join_type"],
            branches=branches,
        )
    elif t == "wait":
        return WaitStep(
            type=t,
            name=d["name"],
            duration=d["duration"],
            unit=d.get("unit", "DAYS"),
        )
    elif t == "condition":
        return ConditionStep(
            type=t,
            condition=ConditionSpec.from_dict(d["condition"]),
            true_steps=[step_from_dict(s) for s in d["true_steps"]],
            false_steps=[step_from_dict(s) for s in d["false_steps"]],
        )
    else:
        raise ValueError(f"Unknown step type: {t}")


# --- AES trigger spec ---


@dataclass
class AesTriggerSpec:
    """AES event handler trigger configuration.

    Declares how a workflow should be triggered from a SyteLine AES event,
    enabling automatic generation of the 7-action ION API handler pattern.
    """

    event: str                              # "IdoOnItemUpdate"
    ido: str                                # "SLCustomers"
    monitored_field: str                    # "CreditLimit"
    workflow_inputs: dict[str, str]         # {"CustNum": "CustNum", "MGConfig": "CONFIGNAME()"}
    applies_to_initiators: str = ""         # "Form.Customers"
    access_as: str = "ue_"
    handler_sequence: int = 200
    handler_description: str | None = None  # defaults to "ue_{workflow_name}"
    guard_condition: str | None = None      # optional extra condition beyond PROPERTYMODIFIED
    notify_email: str | None = None         # optional debug email (action 35)
    notes_ido: str | None = None            # optional notes logging IDO (action 50)
    notes_object_type: str | None = None    # e.g. "customer"

    @classmethod
    def from_dict(cls, d: dict) -> AesTriggerSpec:
        return cls(
            event=d["event"],
            ido=d["ido"],
            monitored_field=d["monitored_field"],
            workflow_inputs=d["workflow_inputs"],
            applies_to_initiators=d.get("applies_to_initiators", ""),
            access_as=d.get("access_as", "ue_"),
            handler_sequence=d.get("handler_sequence", 200),
            handler_description=d.get("handler_description"),
            guard_condition=d.get("guard_condition"),
            notify_email=d.get("notify_email"),
            notes_ido=d.get("notes_ido"),
            notes_object_type=d.get("notes_object_type"),
        )


# --- Top-level spec ---


@dataclass
class WorkflowSpec:
    """Complete workflow specification parsed from JSON."""

    name: str
    description: str
    variables: list[VariableSpec]
    views: list[ViewSpec]
    trees: list[TreeSpec]
    flow: list[StepType]
    aes_trigger: AesTriggerSpec | None = None

    @classmethod
    def from_dict(cls, d: dict) -> WorkflowSpec:
        aes_trigger = None
        if "aes_trigger" in d:
            aes_trigger = AesTriggerSpec.from_dict(d["aes_trigger"])
        return cls(
            name=d["name"],
            description=d.get("description", ""),
            variables=[VariableSpec.from_dict(v) for v in d.get("variables", [])],
            views=[ViewSpec.from_dict(v) for v in d.get("views", [])],
            trees=[TreeSpec.from_dict(t) for t in d.get("trees", [])],
            flow=[step_from_dict(s) for s in d.get("flow", [])],
            aes_trigger=aes_trigger,
        )
