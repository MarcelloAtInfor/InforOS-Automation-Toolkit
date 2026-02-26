"""Workflow spec validator with layered checks.

Level 1 -- Structural (no network):
- Required fields and non-empty collections
- Valid enum values
- IDO reference completeness (ido XOR ido_var)
- Change spec completeness (value XOR value_var)

Level 2 -- Referential integrity:
- Spec-only: variable, view, and tree cross-references
- With tenant: distribution user validation

Level 3 -- Live IDO validation (Phase 4B):
- IDO names exist in SyteLine
- Property names exist and have correct casing
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from src.templates.schema import (
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
    ParamSpec,
)
from src.templates.renderer import auto_create_variables
from src.config.tenant import TenantConfig

from . import user_resolver


# --- Valid enums ---

VALID_STEP_TYPES = {
    "approval_task",
    "notification",
    "assignment",
    "ido_branch",
    "ido_load",
    "ido_update",
    "subworkflow",
    "parallel",
    "wait",
    "condition",
}

VALID_OPERATORS = {
    "Equal",
    "NotEqual",
    "GreaterThan",
    "LessThan",
    "GreaterThanOrEqual",
    "LessThanOrEqual",
}

VALID_JOIN_TYPES = {"ONE_IN", "ALL_IN"}

VALID_TIME_UNITS = {"SECONDS", "MINUTES", "HOURS", "DAYS", "WEEKS", "MONTHS"}

VALID_ASSIGNMENT_TYPES = {"VALUE_ASSIGNMENT", "EXPRESSION_ASSIGNMENT"}

VALID_LOGIC_OPERATORS = {"AND", "OR"}

VALID_VARIABLE_TYPES = {"STRING", "DECIMAL", "INTEGER", "BOOLEAN", "DATE_AND_TIME"}

BRACKET_VAR_RE = re.compile(r"\[(\w+)\]")


# --- Result types ---


@dataclass
class ValidationIssue:
    """A single validation finding."""

    level: str  # "structural", "referential", "live"
    category: str  # e.g., "required_field", "invalid_enum", "missing_variable"
    path: str  # e.g., "flow[0].buttons" or "variables[2].type"
    message: str
    severity: str = "error"  # "error" or "warning"
    suggestion: str | None = None


@dataclass
class ValidationReport:
    """Collection of validation findings."""

    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def summary(self) -> str:
        if not self.issues:
            return "No issues found."
        parts = []
        error_count = len(self.errors)
        warning_count = len(self.warnings)
        if error_count:
            parts.append(f"{error_count} error(s)")
        if warning_count:
            parts.append(f"{warning_count} warning(s)")
        return ", ".join(parts)


# --- Validator ---


class SpecValidator:
    """Validates a WorkflowSpec with layered checks."""

    def __init__(
        self, spec: WorkflowSpec, tenant: TenantConfig | None = None
    ) -> None:
        self.spec = spec
        self.tenant = tenant
        self._issues: list[ValidationIssue] = []

        # Pre-compute available variables (explicit + auto-created)
        explicit = {v.name for v in spec.variables}
        auto = {v.name for v in auto_create_variables(spec)}
        self._available_vars = explicit | auto

        # Pre-compute view and tree names
        self._view_names = {v.name for v in spec.views}
        self._tree_names = {t.name for t in spec.trees}

    def validate(self, live_client=None) -> ValidationReport:
        """Run all applicable validation levels and return report."""
        self._issues = []
        self._check_structural()
        self._check_referential()
        if self.tenant:
            self._check_tenant()
        if live_client:
            self._check_live(live_client)
        return ValidationReport(issues=list(self._issues))

    # Valid AES event names for trigger validation
    VALID_AES_EVENTS = {"IdoOnItemUpdate", "IdoOnItemInsert", "IdoOnItemDelete"}

    def _add(
        self,
        level: str,
        category: str,
        path: str,
        message: str,
        severity: str = "error",
        suggestion: str | None = None,
    ) -> None:
        self._issues.append(
            ValidationIssue(
                level=level,
                category=category,
                path=path,
                message=message,
                severity=severity,
                suggestion=suggestion,
            )
        )

    # ------------------------------------------------------------------
    # Level 1: Structural checks
    # ------------------------------------------------------------------

    def _check_structural(self) -> None:
        spec = self.spec

        # Top-level required fields
        if not spec.name:
            self._add(
                "structural", "required_field", "name",
                "Workflow name is required",
            )

        if not spec.flow:
            self._add(
                "structural", "required_field", "flow",
                "Workflow must have at least one flow step",
            )

        # AES trigger structural checks
        if spec.aes_trigger:
            self._check_aes_trigger_structural(spec.aes_trigger)

        # Variable type validation
        for i, v in enumerate(spec.variables):
            if v.type not in VALID_VARIABLE_TYPES:
                self._add(
                    "structural", "invalid_enum", f"variables[{i}].type",
                    f"Invalid variable type '{v.type}'",
                    suggestion=f"Valid types: {', '.join(sorted(VALID_VARIABLE_TYPES))}",
                )

        # Duplicate names
        self._check_duplicates(
            [v.name for v in spec.variables], "variables", "variable"
        )
        self._check_duplicates(
            [v.name for v in spec.views], "views", "view"
        )
        self._check_duplicates(
            [t.name for t in spec.trees], "trees", "tree"
        )

        # Check each flow step
        for i, step in enumerate(spec.flow):
            self._check_step_structural(step, f"flow[{i}]")

    def _check_duplicates(
        self, names: list[str], path: str, kind: str
    ) -> None:
        seen: set[str] = set()
        for name in names:
            if name in seen:
                self._add(
                    "structural", "duplicate", path,
                    f"Duplicate {kind} name: '{name}'",
                )
            seen.add(name)

    def _check_step_structural(self, step: StepType, path: str) -> None:
        if isinstance(step, ApprovalTaskStep):
            if not step.buttons:
                self._add(
                    "structural", "required_field", f"{path}.buttons",
                    "Approval task must have at least one button",
                )
            if not step.button_variable:
                self._add(
                    "structural", "required_field", f"{path}.button_variable",
                    "Approval task must specify button_variable",
                )
            if step.due_date and step.due_date.unit not in VALID_TIME_UNITS:
                self._add(
                    "structural", "invalid_enum", f"{path}.due_date.unit",
                    f"Invalid time unit '{step.due_date.unit}'",
                    suggestion=f"Valid units: {', '.join(sorted(VALID_TIME_UNITS))}",
                )

        elif isinstance(step, AssignmentStep):
            if not step.assignments:
                self._add(
                    "structural", "required_field", f"{path}.assignments",
                    "Assignment step must have at least one assignment",
                )
            for j, a in enumerate(step.assignments):
                if a.assignment_type not in VALID_ASSIGNMENT_TYPES:
                    self._add(
                        "structural", "invalid_enum",
                        f"{path}.assignments[{j}].assignment_type",
                        f"Invalid assignment type '{a.assignment_type}'",
                        suggestion=(
                            f"Valid types: {', '.join(sorted(VALID_ASSIGNMENT_TYPES))}"
                        ),
                    )

        elif isinstance(step, IdoBranchStep):
            self._check_condition_spec(step.condition, f"{path}.condition")

        elif isinstance(step, IdoLoadStep):
            if step.ido and step.ido_var:
                self._add(
                    "structural", "ido_reference", path,
                    "Cannot specify both 'ido' and 'ido_var'",
                )
            elif not step.ido and not step.ido_var:
                self._add(
                    "structural", "ido_reference", path,
                    "Must specify either 'ido' or 'ido_var'",
                )

        elif isinstance(step, IdoUpdateStep):
            if step.ido and step.ido_var:
                self._add(
                    "structural", "ido_reference", path,
                    "Cannot specify both 'ido' and 'ido_var'",
                )
            elif not step.ido and not step.ido_var:
                self._add(
                    "structural", "ido_reference", path,
                    "Must specify either 'ido' or 'ido_var'",
                )
            if not step.changes:
                self._add(
                    "structural", "required_field", f"{path}.changes",
                    "IDO update must have at least one change",
                )
            for j, c in enumerate(step.changes):
                if c.value is not None and c.value_var is not None:
                    self._add(
                        "structural", "change_reference",
                        f"{path}.changes[{j}]",
                        "Cannot specify both 'value' and 'value_var'",
                    )
                elif c.value is None and c.value_var is None:
                    self._add(
                        "structural", "change_reference",
                        f"{path}.changes[{j}]",
                        "Must specify either 'value' or 'value_var'",
                    )

        elif isinstance(step, SubworkflowStep):
            if not step.steps:
                self._add(
                    "structural", "required_field", f"{path}.steps",
                    "Subworkflow must have at least one step",
                )
            for j, s in enumerate(step.steps):
                self._check_step_structural(s, f"{path}.steps[{j}]")

        elif isinstance(step, ParallelStep):
            if step.join_type not in VALID_JOIN_TYPES:
                self._add(
                    "structural", "invalid_enum", f"{path}.join_type",
                    f"Invalid join type '{step.join_type}'",
                    suggestion=f"Valid types: {', '.join(sorted(VALID_JOIN_TYPES))}",
                )
            if not step.branches:
                self._add(
                    "structural", "required_field", f"{path}.branches",
                    "Parallel step must have at least one branch",
                )
            for j, branch in enumerate(step.branches):
                if not branch:
                    self._add(
                        "structural", "required_field",
                        f"{path}.branches[{j}]",
                        "Parallel branch must have at least one step",
                    )
                for k, s in enumerate(branch):
                    self._check_step_structural(s, f"{path}.branches[{j}][{k}]")

        elif isinstance(step, WaitStep):
            if step.duration <= 0:
                self._add(
                    "structural", "invalid_value", f"{path}.duration",
                    f"Wait duration must be positive, got {step.duration}",
                )
            if step.unit not in VALID_TIME_UNITS:
                self._add(
                    "structural", "invalid_enum", f"{path}.unit",
                    f"Invalid time unit '{step.unit}'",
                    suggestion=f"Valid units: {', '.join(sorted(VALID_TIME_UNITS))}",
                )

        elif isinstance(step, ConditionStep):
            self._check_condition_spec(step.condition, f"{path}.condition")
            for j, s in enumerate(step.true_steps):
                self._check_step_structural(s, f"{path}.true_steps[{j}]")
            for j, s in enumerate(step.false_steps):
                self._check_step_structural(s, f"{path}.false_steps[{j}]")

    def _check_condition_spec(self, condition, path: str) -> None:
        """Validate a ConditionSpec — simple or compound."""
        if condition.is_compound:
            if condition.logic not in VALID_LOGIC_OPERATORS:
                self._add(
                    "structural", "invalid_enum", f"{path}.logic",
                    f"Invalid logic operator '{condition.logic}'",
                    suggestion=f"Valid: {', '.join(sorted(VALID_LOGIC_OPERATORS))}",
                )
            if len(condition.conditions) < 2:
                self._add(
                    "structural", "required_field", f"{path}.conditions",
                    "Compound condition requires at least 2 sub-conditions",
                )
            for j, sub in enumerate(condition.conditions):
                self._check_condition_operator(
                    sub.operator, f"{path}.conditions[{j}]"
                )
        else:
            self._check_condition_operator(condition.operator, path)

    def _check_condition_operator(self, operator: str, path: str) -> None:
        if operator not in VALID_OPERATORS:
            self._add(
                "structural", "invalid_enum", f"{path}.operator",
                f"Invalid operator '{operator}'",
                suggestion=f"Valid operators: {', '.join(sorted(VALID_OPERATORS))}",
            )

    # ------------------------------------------------------------------
    # Level 2: Referential integrity (spec-only)
    # ------------------------------------------------------------------

    def _check_referential(self) -> None:
        # Check view parameter variable references
        for i, view in enumerate(self.spec.views):
            for param_name, param_value in view.params.items():
                if param_value.startswith("$"):
                    var_name = param_value[1:]
                    if var_name not in self._available_vars:
                        self._add(
                            "referential", "missing_variable",
                            f"views[{i}].params.{param_name}",
                            f"View parameter references undefined variable "
                            f"'{var_name}'",
                            suggestion=self._suggest_var(var_name),
                        )

        # Check flow steps
        for i, step in enumerate(self.spec.flow):
            self._check_step_referential(step, f"flow[{i}]")

        # AES trigger referential checks
        if self.spec.aes_trigger:
            self._check_aes_trigger_referential(self.spec.aes_trigger)

    def _check_step_referential(self, step: StepType, path: str) -> None:
        if isinstance(step, ApprovalTaskStep):
            self._check_message_vars(step.message, path)
            self._check_task_params(step.params, path)
            self._check_var_exists(
                step.button_variable, f"{path}.button_variable"
            )

        elif isinstance(step, NotificationStep):
            self._check_message_vars(step.message, path)
            self._check_task_params(step.params, path)

        elif isinstance(step, IdoBranchStep):
            self._check_var_exists(
                step.condition.variable, f"{path}.condition.variable"
            )
            self._check_var_exists(
                step.true_assignment.variable,
                f"{path}.true_assignment.variable",
            )
            self._check_var_exists(
                step.true_assignment.from_variable,
                f"{path}.true_assignment.from_variable",
            )
            self._check_var_exists(
                step.false_assignment.variable,
                f"{path}.false_assignment.variable",
            )
            self._check_var_exists(
                step.false_assignment.from_variable,
                f"{path}.false_assignment.from_variable",
            )

        elif isinstance(step, IdoLoadStep):
            self._check_var_ref(step.filter_var, f"{path}.filter_var")
            self._check_var_ref(step.config_var, f"{path}.config_var")
            self._check_var_ref(step.ido_var, f"{path}.ido_var")
            self._check_var_ref(step.properties_var, f"{path}.properties_var")

        elif isinstance(step, IdoUpdateStep):
            self._check_var_ref(step.item_id_var, f"{path}.item_id_var")
            self._check_var_ref(step.config_var, f"{path}.config_var")
            self._check_var_ref(step.ido_var, f"{path}.ido_var")
            for j, c in enumerate(step.changes):
                if c.value_var:
                    self._check_var_exists(
                        c.value_var, f"{path}.changes[{j}].value_var"
                    )

        elif isinstance(step, SubworkflowStep):
            for j, s in enumerate(step.steps):
                self._check_step_referential(s, f"{path}.steps[{j}]")

        elif isinstance(step, ParallelStep):
            for j, branch in enumerate(step.branches):
                for k, s in enumerate(branch):
                    self._check_step_referential(
                        s, f"{path}.branches[{j}][{k}]"
                    )

        elif isinstance(step, ConditionStep):
            if step.condition.is_compound:
                for j, sub in enumerate(step.condition.conditions):
                    self._check_var_exists(
                        sub.variable,
                        f"{path}.condition.conditions[{j}].variable",
                    )
            else:
                self._check_var_exists(
                    step.condition.variable, f"{path}.condition.variable"
                )
            for j, s in enumerate(step.true_steps):
                self._check_step_referential(s, f"{path}.true_steps[{j}]")
            for j, s in enumerate(step.false_steps):
                self._check_step_referential(s, f"{path}.false_steps[{j}]")

    def _check_message_vars(self, message: str, path: str) -> None:
        """Check that [BracketVars] in messages reference available variables."""
        for var_name in BRACKET_VAR_RE.findall(message):
            if var_name not in self._available_vars:
                self._add(
                    "referential", "missing_variable", f"{path}.message",
                    f"Message references undefined variable '[{var_name}]'",
                    suggestion=self._suggest_var(var_name),
                )

    def _check_task_params(
        self, params: list[ParamSpec], path: str
    ) -> None:
        """Check task parameter bindings (variable, view, tree)."""
        for j, p in enumerate(params):
            has_binding = False

            if p.variable:
                has_binding = True
                if p.variable not in self._available_vars:
                    self._add(
                        "referential", "missing_variable",
                        f"{path}.params[{j}].variable",
                        f"Task parameter references undefined variable "
                        f"'{p.variable}'",
                        suggestion=self._suggest_var(p.variable),
                    )

            if p.view:
                has_binding = True
                if p.view not in self._view_names:
                    self._add(
                        "referential", "missing_view",
                        f"{path}.params[{j}].view",
                        f"Task parameter references undefined view "
                        f"'{p.view}'",
                        suggestion=self._suggest_name(p.view, self._view_names),
                    )

            if p.tree:
                has_binding = True
                if p.tree not in self._tree_names:
                    self._add(
                        "referential", "missing_tree",
                        f"{path}.params[{j}].tree",
                        f"Task parameter references undefined tree "
                        f"'{p.tree}'",
                        suggestion=self._suggest_name(p.tree, self._tree_names),
                    )

            if not has_binding:
                self._add(
                    "referential", "missing_binding",
                    f"{path}.params[{j}]",
                    f"Task parameter '{p.label}' has no variable, view, "
                    f"or tree binding",
                    severity="warning",
                )

    def _check_var_exists(self, var_name: str | None, path: str) -> None:
        """Check that a variable reference points to an available variable."""
        if var_name and var_name not in self._available_vars:
            self._add(
                "referential", "missing_variable", path,
                f"References undefined variable '{var_name}'",
                suggestion=self._suggest_var(var_name),
            )

    def _check_var_ref(self, var_name: str | None, path: str) -> None:
        """Check optional variable reference (empty string = not specified)."""
        if var_name and var_name not in self._available_vars:
            self._add(
                "referential", "missing_variable", path,
                f"References undefined variable '{var_name}'",
                suggestion=self._suggest_var(var_name),
            )

    def _suggest_var(self, name: str) -> str | None:
        import difflib

        matches = difflib.get_close_matches(
            name, self._available_vars, n=3, cutoff=0.6
        )
        if matches:
            return f"Did you mean: {', '.join(matches)}?"
        return None

    def _suggest_name(self, name: str, valid_names: set[str]) -> str | None:
        import difflib

        matches = difflib.get_close_matches(
            name, valid_names, n=3, cutoff=0.6
        )
        if matches:
            return f"Did you mean: {', '.join(matches)}?"
        return None

    # ------------------------------------------------------------------
    # Level 2+: Tenant checks (distribution users)
    # ------------------------------------------------------------------

    def _check_tenant(self) -> None:
        for i, step in enumerate(self.spec.flow):
            self._check_step_tenant(step, f"flow[{i}]")

    def _check_step_tenant(self, step: StepType, path: str) -> None:
        if isinstance(step, (ApprovalTaskStep, NotificationStep)):
            result = user_resolver.validate_distribution(
                step.distribution, self.tenant
            )
            if not result.valid:
                for issue in result.issues:
                    suggestion = None
                    if result.suggestions:
                        suggestion = (
                            f"Similar users: {', '.join(result.suggestions)}"
                        )
                    self._add(
                        "referential", "invalid_distribution",
                        f"{path}.distribution",
                        issue,
                        suggestion=suggestion,
                    )

        elif isinstance(step, SubworkflowStep):
            for j, s in enumerate(step.steps):
                self._check_step_tenant(s, f"{path}.steps[{j}]")

        elif isinstance(step, ParallelStep):
            for j, branch in enumerate(step.branches):
                for k, s in enumerate(branch):
                    self._check_step_tenant(s, f"{path}.branches[{j}][{k}]")

        elif isinstance(step, ConditionStep):
            for j, s in enumerate(step.true_steps):
                self._check_step_tenant(s, f"{path}.true_steps[{j}]")
            for j, s in enumerate(step.false_steps):
                self._check_step_tenant(s, f"{path}.false_steps[{j}]")

    # ------------------------------------------------------------------
    # Level 3: Live IDO validation (Phase 4B stub)
    # ------------------------------------------------------------------

    def _check_live(self, client) -> None:
        """Level 3: Validate IDO names and properties against live SyteLine."""
        for i, step in enumerate(self.spec.flow):
            self._check_step_live(step, f"flow[{i}]", client)

        # AES trigger live checks
        if self.spec.aes_trigger:
            self._check_aes_trigger_live(self.spec.aes_trigger, client)

    def _check_step_live(self, step: StepType, path: str, client) -> None:
        """Recursively validate IDO references in a step against live data."""
        if isinstance(step, IdoLoadStep):
            if step.ido:
                self._validate_ido_name(step.ido, path, client)
                if step.properties:
                    for prop in step.properties.split(","):
                        prop = prop.strip()
                        if prop:
                            self._validate_property(
                                step.ido, prop, f"{path}.properties", client
                            )

        elif isinstance(step, IdoUpdateStep):
            if step.ido:
                self._validate_ido_name(step.ido, path, client)
                for j, change in enumerate(step.changes):
                    self._validate_property(
                        step.ido,
                        change.property,
                        f"{path}.changes[{j}].property",
                        client,
                    )

        elif isinstance(step, SubworkflowStep):
            for j, s in enumerate(step.steps):
                self._check_step_live(s, f"{path}.steps[{j}]", client)

        elif isinstance(step, ParallelStep):
            for j, branch in enumerate(step.branches):
                for k, s in enumerate(branch):
                    self._check_step_live(
                        s, f"{path}.branches[{j}][{k}]", client
                    )

        elif isinstance(step, ConditionStep):
            for j, s in enumerate(step.true_steps):
                self._check_step_live(s, f"{path}.true_steps[{j}]", client)
            for j, s in enumerate(step.false_steps):
                self._check_step_live(s, f"{path}.false_steps[{j}]", client)

    # ------------------------------------------------------------------
    # AES trigger validation (across levels)
    # ------------------------------------------------------------------

    def _check_aes_trigger_structural(self, trigger) -> None:
        """Level 1: Structural checks for aes_trigger section."""
        path = "aes_trigger"

        if not trigger.event:
            self._add(
                "structural", "required_field", f"{path}.event",
                "AES trigger event is required",
            )
        elif trigger.event not in self.VALID_AES_EVENTS:
            self._add(
                "structural", "invalid_enum", f"{path}.event",
                f"Invalid AES event '{trigger.event}'",
                suggestion=f"Valid events: {', '.join(sorted(self.VALID_AES_EVENTS))}",
            )

        if not trigger.ido:
            self._add(
                "structural", "required_field", f"{path}.ido",
                "AES trigger IDO is required",
            )

        if not trigger.monitored_field:
            self._add(
                "structural", "required_field", f"{path}.monitored_field",
                "AES trigger monitored_field is required",
            )

        if not trigger.workflow_inputs:
            self._add(
                "structural", "required_field", f"{path}.workflow_inputs",
                "AES trigger must have at least one workflow_inputs mapping",
            )

    def _check_aes_trigger_referential(self, trigger) -> None:
        """Level 2: Check that workflow_inputs keys match declared variables."""
        path = "aes_trigger"

        for wf_var in trigger.workflow_inputs:
            if wf_var not in self._available_vars:
                self._add(
                    "referential", "missing_variable",
                    f"{path}.workflow_inputs.{wf_var}",
                    f"Workflow input '{wf_var}' not found in declared variables",
                    suggestion=self._suggest_var(wf_var),
                )

    def _check_aes_trigger_live(self, trigger, client) -> None:
        """Level 3: Validate AES trigger IDO and monitored field against live SyteLine."""
        path = "aes_trigger"

        if trigger.ido:
            self._validate_ido_name(trigger.ido, path, client)
            if trigger.monitored_field:
                self._validate_property(
                    trigger.ido, trigger.monitored_field,
                    f"{path}.monitored_field", client,
                )

    def _validate_ido_name(self, ido_name: str, path: str, client) -> None:
        """Check that an IDO name exists in SyteLine."""
        if not client.ido_exists(ido_name):
            suggestions = client.suggest_ido(ido_name)
            suggestion = (
                f"Did you mean: {', '.join(suggestions)}?" if suggestions else None
            )
            self._add(
                "live", "invalid_ido", f"{path}.ido",
                f"IDO '{ido_name}' not found in SyteLine",
                suggestion=suggestion,
            )

    def _validate_property(
        self, ido_name: str, prop_name: str, path: str, client
    ) -> None:
        """Check that a property exists on an IDO, with case-match fallback."""
        if client.property_exists(ido_name, prop_name):
            return

        # Try case-insensitive match
        correct = client.find_case_match(ido_name, prop_name)
        if correct:
            self._add(
                "live", "case_mismatch", path,
                f"Property '{prop_name}' on '{ido_name}' has incorrect casing",
                severity="warning",
                suggestion=f"Correct casing: {correct}",
            )
            return

        # No match at all
        suggestions = client.suggest_property(ido_name, prop_name)
        suggestion = (
            f"Did you mean: {', '.join(suggestions)}?" if suggestions else None
        )
        self._add(
            "live", "invalid_property", path,
            f"Property '{prop_name}' not found on IDO '{ido_name}'",
            suggestion=suggestion,
        )
