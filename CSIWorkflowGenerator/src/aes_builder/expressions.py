"""AES expression string builders.

Factory functions producing AES parameter strings for event action
configuration. Analogous to workflow_builder/conditions.py for ION XML.

AES parameter syntax conventions:
  - UPPERCASE function names
  - Arguments in parentheses
  - String literals in double quotes
  - Variable refs: V(var), P(property), GC(const), E(param)
  - Multiple values separated by semicolons (no spaces)

Action type codes (numeric):
  1  = Notify           14 = LoadCollection
  10 = Finish           21 = InvokeMethod
  12 = SetValues        29 = SendBOD
"""

# -- Action type constants (numeric codes used by SyteLine) --

ACTION_FINISH = "10"
ACTION_NOTIFY = "1"
ACTION_SET_VALUES = "12"
ACTION_LOAD_COLLECTION = "14"
ACTION_INVOKE_METHOD = "21"
ACTION_SEND_BOD = "29"
ACTION_BRANCH = "7"
ACTION_PROMPT = "3"
ACTION_UPDATE_RECORD = "13"
ACTION_GENERATE_EVENT = "23"
ACTION_CALL_WORKFLOW = "18"
ACTION_WAIT = "8"
ACTION_SLEEP = "4"


# -- Base expression functions --


def condition(expr: str) -> str:
    """Wrap an expression as a CONDITION() parameter."""
    return f"CONDITION({expr})"


def not_condition(expr: str) -> str:
    """Wrap a negated expression as a CONDITION(NOT ...)."""
    return f"CONDITION(NOT {expr})"


def property_modified(name: str) -> str:
    """PROPERTYMODIFIED("name") -- detect field change."""
    return f'PROPERTYMODIFIED("{name}")'


def prop(name: str) -> str:
    """P("name") -- reference a property value."""
    return f'P("{name}")'


def var(name: str) -> str:
    """V(name) -- reference an event variable."""
    return f"V({name})"


def global_const(name: str) -> str:
    """GC(name) -- reference a global constant."""
    return f"GC({name})"


def event_param(name: str) -> str:
    """E(name) -- reference an event parameter."""
    return f"E({name})"


def result_expr(name: str) -> str:
    """RE(name) -- reference a result variable (for SET assignments)."""
    return f"RE({name})"


def return_var(name: str) -> str:
    """RV(name) -- reference a return variable (for IDO method outputs)."""
    return f"RV({name})"


def substitute(template: str, *args: str) -> str:
    """SUBSTITUTE("template", arg1, arg2, ...) -- string formatting.

    Args:
        template: Format string with {0}, {1}, etc. placeholders.
        args: Expression arguments to substitute.
    """
    arg_list = ", ".join(args)
    return f'SUBSTITUTE("{template}", {arg_list})'


def voting_result(seq: int) -> str:
    """VOTINGRESULT(seq) -- check prompt result from action at given sequence."""
    return f"VOTINGRESULT({seq})"


def db_function(func_name: str, *args: str) -> str:
    """DBFUNCTION("funcName", args) -- call a database function."""
    arg_list = ", ".join(args)
    return f'DBFUNCTION("{func_name}", {arg_list})'


def if_expr(bool_expr: str, true_expr: str, false_expr: str) -> str:
    """IF(bool, trueExpr, falseExpr) -- conditional expression."""
    return f"IF({bool_expr}, {true_expr}, {false_expr})"


def round_expr(value: str, decimals: int) -> str:
    """ROUND(value, decimals) -- round a numeric value."""
    return f"ROUND({value}, {decimals})"


def configname() -> str:
    """CONFIGNAME() -- current SyteLine configuration name."""
    return "CONFIGNAME()"


def username() -> str:
    """USERNAME() -- current user name."""
    return "USERNAME()"


def curdatetime() -> str:
    """CURDATETIME() -- current date/time."""
    return "CURDATETIME()"


def originator() -> str:
    """ORIGINATOR() -- originating user."""
    return "ORIGINATOR()"


# -- Common compound patterns --


def finish_unless_modified(prop_name: str) -> str:
    """CONDITION(NOT PROPERTYMODIFIED("prop")) -- skip if field not changed.

    Common first action in handlers that should only fire when a
    specific field is modified.
    """
    return not_condition(property_modified(prop_name))


def finish_with_result(condition_expr: str, result_msg: str) -> str:
    """CONDITION(expr)RESULT("msg") -- conditional finish with message.

    Used as Finish action parameters to exit early with an explanation.
    """
    return f'{condition_expr}RESULT("{result_msg}")'


def fail_if_rejected(seq: int) -> str:
    """CONDITION(VOTINGRESULT(seq) = 0) -- fail if prompt was rejected.

    Used after a Prompt action to check if the user rejected.
    """
    return condition(f"{voting_result(seq)} = 0")


# -- Parameter line builders for specific action types --


def set_variable_params(variable: str, value: str) -> str:
    """Build Parameters string for SetVariable/Set Values action type.

    Args:
        variable: Variable name to set.
        value: Expression for the value.
    """
    return f'V({variable})VALUE({value})'


def setvarvalues_params(assignments: dict[str, str]) -> str:
    """Build SETVARVALUES() parameter for SetValues (type 12) actions.

    Args:
        assignments: Mapping of variable name -> expression value.

    Example:
        setvarvalues_params({"PARM": 'SUBSTITUTE("{0}", ...)'})
        -> 'SETVARVALUES(PARM = SUBSTITUTE(...))'
    """
    parts = ", ".join(f"{k} = {v}" for k, v in assignments.items())
    return f"SETVARVALUES({parts})"


def setpropvalues_params(assignments: dict[str, str]) -> str:
    """Build SETPROPVALUES() parameter for SetValues (type 12) actions.

    Sets IDO property values on the current record.

    Args:
        assignments: Mapping of property name -> value expression.

    Example:
        setpropvalues_params({"InWorkflow": '"1"', "CreditLimit": 'E(OldCreditLimit)'})
        -> 'SETPROPVALUES("InWorkflow" = "1", "CreditLimit" = E(OldCreditLimit))'
    """
    parts = ", ".join(f'"{k}" = {v}' for k, v in assignments.items())
    return f"SETPROPVALUES({parts})"


def load_collection_params(
    ido: str,
    properties: str,
    filter_expr: str,
    set_assignments: dict[str, str],
    order_by: str | None = None,
) -> str:
    """Build parameters for LoadCollection (type 14) actions.

    Args:
        ido: IDO name to query.
        properties: Comma-separated property list.
        filter_expr: Filter expression (can use SUBSTITUTE).
        set_assignments: Mapping of RE(var) target -> IDO property source.
        order_by: Optional ORDER BY clause.

    Example:
        load_collection_params(
            "SLCustomers", "CreditLimit, RowPointer",
            'SUBSTITUTE("RowPointer = \\'{0}\\'", P("RowPointer"))',
            {"OldCreditLimit": "CreditLimit"},
        )
    """
    parts = [
        f'IDO("{ido}")',
        f'PROPERTIES("{properties}")',
        f'FILTER({filter_expr})',
    ]
    if order_by:
        parts.append(f'ORDERBY("{order_by}")')
    set_parts = ", ".join(
        f"RE({var}) = \"{prop}\"" for var, prop in set_assignments.items()
    )
    parts.append(f"SET({set_parts})")
    return "\n".join(parts) + "\n"


def invoke_method_params(
    ido: str,
    method: str,
    parms: list[str],
) -> str:
    """Build parameters for InvokeMethod (type 21) actions.

    Args:
        ido: IDO name containing the method.
        method: Method name to invoke.
        parms: List of parameter expressions (positional).

    Example:
        invoke_method_params(
            "IONAPIMethods", "InvokeIONAPIMethod2",
            ['"False"', '"0"', '"IONSERVICES"', '"POST"', ...],
        )
    """
    parms_str = ", ".join(parms)
    return f'IDO("{ido}")\nMETHOD("{method}")\nPARMS({parms_str})\n'


def call_workflow_params(
    workflow_name: str,
    inputs: dict[str, str] | None = None,
    outputs: dict[str, str] | None = None,
    suspend: bool = True,
) -> str:
    """Build Parameters string for CallWorkflow action type (type 18).

    Note: The reference Credit Approval handler uses InvokeMethod with
    IONAPIMethods instead. This function is for native AES CallWorkflow.

    Args:
        workflow_name: ION workflow name to invoke.
        inputs: Mapping of workflow input var -> AES expression providing value.
        outputs: Mapping of AES var <- workflow output var to receive value.
        suspend: Whether to suspend handler execution (SUSPEND() parameter).
    """
    parts = [f'WORKFLOW("{workflow_name}")']
    if inputs:
        for wf_var, aes_expr in inputs.items():
            parts.append(f'INPUT("{wf_var}", {aes_expr})')
    if outputs:
        for aes_var, wf_var in outputs.items():
            parts.append(f'OUTPUT("{wf_var}", V({aes_var}))')
    if suspend:
        parts.append("SUSPEND()")
    return "".join(parts)


def notify_params(
    to: str,
    subject: str,
    body: str,
    save_message: bool = True,
) -> str:
    """Build Parameters string for Notify (type 1) actions.

    Args:
        to: TO() expression (e.g. quoted email or semicolon-separated users).
        subject: SUBJECT() expression.
        body: BODY() expression.
        save_message: Whether to save the notification message.
    """
    save = "TRUE" if save_message else "FALSE"
    return f'TO({to})\nSUBJECT({subject})\nBODY({body})\nSAVEMESSAGE({save})\n'


# -- ION API workflow start helper --


def _json_escape_expr(value_expr: str, data_type: str = "STRING") -> str:
    r"""Wrap an AES value expression with REPLACE to escape double quotes.

    The ION workflow start JSON payload is double-encoded: inner JSON lives
    inside an outer JSON string.  A raw value like P("Item") returning
    "SB 2" (with embedded quotes) breaks the outer JSON.

    REPLACE escapes each " as \\\" (four literal chars: \ \ \ ").
    At the outer JSON level \\\" decodes to \" (escaped backslash + quote),
    and at the inner JSON level \" decodes to a literal " character.

    AES single-quoted strings are fully literal (no backslash escaping),
    so '\\\"' is four chars: \ \ \ "

    Numeric expressions (DECIMAL/INTEGER types, ROUND(), etc.) are returned
    unwrapped — they cannot contain double quotes, and the AES parser does
    not accept ROUND in REPLACE's first-argument token grammar.
    """
    if data_type in ("DECIMAL", "INTEGER", "BOOLEAN") or value_expr.startswith("ROUND("):
        return value_expr
    return f"""REPLACE({value_expr}, '"', '\\\\\\"')"""


def build_ion_workflow_start_params(
    workflow_name: str,
    logical_id: str,
    input_variables: dict[str, tuple[str, str]],
) -> str:
    """Build the SETVARVALUES parameter for ION workflow start via API.

    This constructs the JSON payload used by InvokeIONAPIMethod2 to call
    POST /process/application/v1/workflow/start.

    Args:
        workflow_name: ION workflow name (e.g. "CS_Credit_Approval_API").
        logical_id: Logical ID (e.g. "lid://infor.syteline.csi/dals").
        input_variables: Mapping of variable name -> (data_type, value_expression).
            value_expression is an AES expression like P("CustNum") or
            ROUND(E(OldCreditLimit), 2).

    Returns:
        Complete SETVARVALUES(...) parameter string.
    """
    # Build the JSON body template with placeholders
    var_entries = []
    placeholder_args = []
    idx = 0

    # First placeholder is the static prefix
    prefix = (
        f'[{{"Name":"logicalId","Value":"{logical_id}","Type":"query"}}, '
        f'{{"Name":"StartWorkflowJSONBody ","Value":"'
        f'{{\\"workflowName\\":\\"{workflow_name}\\",'
        f'\\"inputVariables\\":['
    )

    for i, (var_name, (data_type, value_expr)) in enumerate(input_variables.items()):
        if i > 0:
            prefix += ","
        prefix += (
            f'{{\\"name\\":\\"{var_name}\\",'
            f'\\"dataType\\":\\"{data_type}\\",'
            f'\\"value\\":\\"'
        )
        # Close the current literal segment, add placeholder for value
        placeholder_args.append(f"'{prefix}'")
        prefix = ""
        # Wrap value expressions with REPLACE to escape embedded double
        # quotes for the double-encoded JSON context (inner JSON inside
        # outer JSON string).  Numeric types and ROUND expressions skip
        # REPLACE — they can't contain quotes and ROUND is not a valid
        # token in REPLACE's first-argument grammar.
        placeholder_args.append(_json_escape_expr(value_expr, data_type))
        prefix = '\\"}'

    prefix += ']}","Type":"body"}]'
    placeholder_args.append(f"'{prefix}'")

    # Build the SUBSTITUTE template
    template_placeholders = "".join(
        f"{{{i}}}" for i in range(len(placeholder_args))
    )
    args_str = ", ".join(placeholder_args)

    return f"SETVARVALUES(PARM = SUBSTITUTE(\"{template_placeholders}\", {args_str}))\n"
