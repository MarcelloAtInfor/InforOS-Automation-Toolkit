"""Top-level WorkflowBuilder that assembles components into complete ION workflow JSON."""
from __future__ import annotations

import json

from .models import WorkflowVariable, WorkflowView
from .flowparts import sequential_flow


class WorkflowBuilder:
    """Fluent builder for ION workflow definitions.

    Usage:
        wf = (WorkflowBuilder("MyWorkflow", "Description")
              .add_variable(WorkflowVariable("Var1", workflow_input=True))
              .add_view(WorkflowView(...))
              .add_flowpart(usertask(...))
              .add_flowpart(assignment(...)))

        workflow_json = wf.to_json()
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.variables: list[WorkflowVariable] = []
        self.views: list[WorkflowView] = []
        self.trees: list[dict] = []
        self.flow_parts: list[dict] = []

    def add_variable(self, var: WorkflowVariable) -> WorkflowBuilder:
        self.variables.append(var)
        return self

    def add_view(self, view: WorkflowView) -> WorkflowBuilder:
        self.views.append(view)
        return self

    def add_tree(self, tree: dict) -> WorkflowBuilder:
        self.trees.append(tree)
        return self

    def add_flowpart(self, flowpart: dict) -> WorkflowBuilder:
        self.flow_parts.append(flowpart)
        return self

    def build(self) -> dict:
        """Assemble complete workflow JSON dict."""
        return {
            "name": self.name,
            "description": self.description,
            "variables": [v.to_dict() for v in self.variables],
            "views": [v.to_dict() for v in self.views],
            "trees": self.trees,
            "sequentialFlow": sequential_flow(self.flow_parts),
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to formatted JSON string."""
        return json.dumps(self.build(), indent=indent, ensure_ascii=False)
