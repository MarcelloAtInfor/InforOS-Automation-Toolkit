"""Main rendering pipeline: WorkflowSpec -> WorkflowBuilder -> JSON dict.

The renderer orchestrates the full transformation from a compact JSON
workflow spec into a complete ION workflow definition by:
1. Auto-creating internal variables from flow analysis
2. Building variables, views, and trees via WorkflowBuilder
3. Rendering each flow step via preset functions
4. Returning the assembled workflow dict
"""
from __future__ import annotations

import json
from pathlib import Path

from src.workflow_builder.builder import WorkflowBuilder
from src.workflow_builder.models import (
    WorkflowVariable,
    WorkflowView,
    ViewParameter,
)
from src.config.tenant import TenantConfig
from shared.tenant import get_drillback_logical_id, get_drillback_view_set

from .schema import (
    WorkflowSpec,
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
from .presets import render_step


def _collect_variable_refs(steps: list[StepType]) -> list[str]:
    """Scan flow steps recursively and collect all referenced variable names.

    Returns variable names in discovery order (first occurrence).
    """
    seen: set[str] = set()
    refs: list[str] = []

    def _add(name: str | None) -> None:
        if name and name not in seen:
            seen.add(name)
            refs.append(name)

    def _scan(steps: list[StepType]) -> None:
        for step in steps:
            if isinstance(step, ApprovalTaskStep):
                _add(step.button_variable)
                for p in step.params:
                    _add(p.variable)
            elif isinstance(step, NotificationStep):
                for p in step.params:
                    _add(p.variable)
            elif isinstance(step, AssignmentStep):
                for a in step.assignments:
                    _add(a.variable)
            elif isinstance(step, IdoBranchStep):
                _add(step.condition.variable)
                _add(step.true_assignment.variable)
                _add(step.true_assignment.from_variable)
                _add(step.false_assignment.variable)
                _add(step.false_assignment.from_variable)
            elif isinstance(step, IdoLoadStep):
                _add(step.filter_var)
                _add(step.config_var)
                _add(step.ido_var)
                _add(step.properties_var)
                for var_name in step.outputs:
                    _add(var_name)
            elif isinstance(step, IdoUpdateStep):
                _add(step.item_id_var)
                _add(step.config_var)
                _add(step.ido_var)
                for change in step.changes:
                    _add(change.value_var)
                for var_name in step.outputs:
                    _add(var_name)
            elif isinstance(step, SubworkflowStep):
                _scan(step.steps)
            elif isinstance(step, ParallelStep):
                for branch in step.branches:
                    _scan(branch)
            elif isinstance(step, ConditionStep):
                _add(step.condition.variable)
                _scan(step.true_steps)
                _scan(step.false_steps)
            # WaitStep has no variable references

    _scan(steps)
    return refs


def _infer_variable_types(spec: WorkflowSpec) -> dict[str, str]:
    """Build a map of variable name -> inferred data type from flow assignments.

    Looks at ido_branch steps where a target variable is assigned from a source
    variable with a known type (e.g. UpdatePropertyValue <- Discount[DECIMAL]).
    """
    declared_types = {v.name: v.type for v in spec.variables}
    inferred: dict[str, str] = {}

    def _scan(steps):
        for step in steps:
            if isinstance(step, IdoBranchStep):
                for assignment in (step.true_assignment, step.false_assignment):
                    src_type = declared_types.get(assignment.from_variable)
                    if src_type and assignment.variable not in declared_types:
                        inferred[assignment.variable] = src_type
            elif isinstance(step, SubworkflowStep):
                _scan(step.steps)
            elif isinstance(step, ParallelStep):
                for branch in step.branches:
                    _scan(branch)
            elif isinstance(step, ConditionStep):
                _scan(step.true_steps)
                _scan(step.false_steps)

    _scan(spec.flow)
    return inferred


def auto_create_variables(spec: WorkflowSpec) -> list[WorkflowVariable]:
    """Create internal variables for names referenced in flow but not declared.

    Returns a list of WorkflowVariable objects for auto-created variables.
    Infers data types from ido_branch assignments when possible.
    """
    explicit_names = {v.name for v in spec.variables}
    all_refs = _collect_variable_refs(spec.flow)
    type_map = _infer_variable_types(spec)

    # Default initial values for non-STRING types (ION rejects empty string for these)
    _TYPE_DEFAULTS = {"DECIMAL": "0", "INTEGER": "0", "BOOLEAN": "false"}

    auto_vars = []
    for name in all_refs:
        if name not in explicit_names:
            data_type = type_map.get(name, "STRING")
            initial = _TYPE_DEFAULTS.get(data_type)
            auto_vars.append(WorkflowVariable(name, data_type=data_type,
                                              initial_value=initial))

    return auto_vars


def render(spec: WorkflowSpec, tenant: TenantConfig) -> dict:
    """Main rendering pipeline: spec + tenant -> ION workflow dict."""
    builder = WorkflowBuilder(spec.name, spec.description)

    # 1. Add auto-created internal variables
    for var in auto_create_variables(spec):
        builder.add_variable(var)

    # 2. Add explicit variables from spec
    for var_spec in spec.variables:
        builder.add_variable(
            WorkflowVariable(
                name=var_spec.name,
                data_type=var_spec.type,
                workflow_input=var_spec.input,
                workflow_output=var_spec.output,
                initial_value=var_spec.initial_value,
            )
        )

    # 3. Add views (auto-inject LogicalId and viewSetName from tenant config when empty)
    for view_spec in spec.views:
        view_set = view_spec.view_set or get_drillback_view_set()
        params = []
        for param_name, param_value in view_spec.params.items():
            if param_value.startswith("$"):
                params.append(ViewParameter(param_name, variable=param_value[1:]))
            elif param_name == "LogicalId" and not param_value:
                params.append(ViewParameter(param_name, value=get_drillback_logical_id()))
            else:
                params.append(ViewParameter(param_name, value=param_value))
        builder.add_view(
            WorkflowView(view_spec.name, view_set, view_spec.view, params)
        )

    # 4. Add trees
    for tree_spec in spec.trees:
        builder.add_tree(tree_spec.to_dict())

    # 5. Render flow steps with auto-sequencing
    for i, step in enumerate(spec.flow):
        seq = i + 1
        flowpart = render_step(step, seq, tenant)
        builder.add_flowpart(flowpart)

    return builder.build()


def load_spec(json_path: str | Path) -> WorkflowSpec:
    """Load a workflow spec from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return WorkflowSpec.from_dict(data)
