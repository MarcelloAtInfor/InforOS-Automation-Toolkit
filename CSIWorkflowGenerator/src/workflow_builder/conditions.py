"""XML condition string builder for ifthenelse flowparts.

ION workflows use XML-encoded condition strings for branching logic.

Simple condition example:
    <?xml version="1.0" encoding="UTF-8"?>
    <Condition version="1.0">
      <UsedSubcondition>IsApproved</UsedSubcondition>
      <Subconditions>
        <Subcondition>
          <Name>IsApproved</Name>
          <Type>AttributeValueComparison</Type>
          <AttributeName>ApproveReject</AttributeName>
          <ComparisonOperator>Equal</ComparisonOperator>
          <Value>Approved</Value>
        </Subcondition>
      </Subconditions>
    </Condition>

Compound condition example (AND/OR):
    <?xml version="1.0" encoding="UTF-8"?>
    <Condition version="1.0">
      <UsedSubcondition>BothApproved</UsedSubcondition>
      <Subconditions>
        <Subcondition>
          <Name>EngApproved</Name>
          <Type>AttributeValueComparison</Type>
          ...
        </Subcondition>
        <Subcondition>
          <Name>QualApproved</Name>
          <Type>AttributeValueComparison</Type>
          ...
        </Subcondition>
        <Subcondition>
          <Name>BothApproved</Name>
          <Type>CombinedCondition</Type>
          <Conditions>EngApproved,QualApproved</Conditions>
          <ANDOR>AND</ANDOR>
        </Subcondition>
      </Subconditions>
    </Condition>
"""
from __future__ import annotations

from xml.sax.saxutils import escape

VALID_OPERATORS = {
    "Equal",
    "NotEqual",
    "GreaterThan",
    "LessThan",
    "GreaterOrEqual",
    "LessOrEqual",
}


def _xml_text(value: str) -> str:
    """Escape text for safe inclusion in XML element bodies."""
    return escape(str(value))


def build_condition(
    name: str,
    variable: str,
    operator: str,
    value: str,
) -> str:
    """Build an XML condition string for an ifthenelse flowpart.

    Args:
        name: Subcondition name (e.g. "IsApproved").
        variable: Workflow variable to compare (e.g. "ApproveReject").
        operator: Comparison operator (Equal, NotEqual, GreaterThan, etc.).
        value: Literal value to compare against.

    Returns:
        XML condition string matching ION workflow format.
    """
    if operator not in VALID_OPERATORS:
        raise ValueError(
            f"Invalid operator '{operator}'. Must be one of: {sorted(VALID_OPERATORS)}"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Condition version="1.0">'
        f"<UsedSubcondition>{_xml_text(name)}</UsedSubcondition>"
        "<Subconditions>"
        "<Subcondition>"
        f"<Name>{_xml_text(name)}</Name>"
        "<Type>AttributeValueComparison</Type>"
        f"<AttributeName>{_xml_text(variable)}</AttributeName>"
        f"<ComparisonOperator>{_xml_text(operator)}</ComparisonOperator>"
        f"<Value>{_xml_text(value)}</Value>"
        "</Subcondition>"
        "</Subconditions>"
        "</Condition>"
    )


VALID_LOGIC_OPERATORS = {"AND", "OR"}


def build_compound_condition(
    name: str,
    logic: str,
    conditions: list,
) -> str:
    """Build a compound XML condition with AND/OR logic.

    Generates a CombinedCondition subcondition that references multiple
    AttributeValueComparison subconditions by name.

    Args:
        name: Name for the compound subcondition (e.g. "BothApproved").
        logic: Boolean operator — "AND" or "OR".
        conditions: List of sub-condition specs, each having
            name, variable, operator, value attributes.

    Returns:
        XML condition string with compound logic.
    """
    if logic not in VALID_LOGIC_OPERATORS:
        raise ValueError(
            f"Invalid logic '{logic}'. Must be one of: {sorted(VALID_LOGIC_OPERATORS)}"
        )
    if len(conditions) < 2:
        raise ValueError("Compound condition requires at least 2 sub-conditions")

    # Build individual subcondition XML fragments
    subcondition_xml = ""
    cond_names = []
    for cond in conditions:
        if cond.operator not in VALID_OPERATORS:
            raise ValueError(
                f"Invalid operator '{cond.operator}' in sub-condition '{cond.name}'. "
                f"Must be one of: {sorted(VALID_OPERATORS)}"
            )
        subcondition_xml += (
            "<Subcondition>"
            f"<Name>{_xml_text(cond.name)}</Name>"
            "<Type>AttributeValueComparison</Type>"
            f"<AttributeName>{_xml_text(cond.variable)}</AttributeName>"
            f"<ComparisonOperator>{_xml_text(cond.operator)}</ComparisonOperator>"
            f"<Value>{_xml_text(cond.value)}</Value>"
            "</Subcondition>"
        )
        cond_names.append(cond.name)

    # Build the CombinedCondition subcondition (comma-separated name list)
    compound_xml = (
        "<Subcondition>"
        f"<Name>{_xml_text(name)}</Name>"
        "<Type>CombinedCondition</Type>"
        f"<Conditions>{_xml_text(','.join(cond_names))}</Conditions>"
        f"<ANDOR>{_xml_text(logic)}</ANDOR>"
        "</Subcondition>"
    )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Condition version="1.0">'
        f"<UsedSubcondition>{_xml_text(name)}</UsedSubcondition>"
        "<Subconditions>"
        f"{subcondition_xml}"
        f"{compound_xml}"
        "</Subconditions>"
        "</Condition>"
    )
