"""
Spec validation for GenAI Factory Tools and Agents.

Provides validation functions for naming conventions and portability
checks to ensure specs follow factory standards.

Validations are type-specific:
    - Tools (type: "API_DOCS"): api_docs, responseInstructions, whitespace, auth, example, debug
    - Agents (type: "TOOLKIT"): tools array, workflow
    - Both: naming convention, portability, required fields, type-name consistency
"""

import json
import re
from typing import Any, Dict, List, Optional, Literal


# Compiled regex patterns for performance
# Format: GAF_{Org}_{Name}_{Tool|Agent}_v{version}
NAMING_PATTERN = re.compile(r'^GAF_[A-Za-z0-9]+_[A-Za-z0-9]+_(Tool|Agent)_v\d+$')

# Hardcoded tenant patterns to detect non-portable specs
TENANT_PATTERNS = [
    re.compile(r'https://[a-zA-Z0-9-]+\.inforcloudsuite\.com'),
    re.compile(r'\.mingledev\.com'),
    re.compile(r'tenant[_-]?id["\s:]+[a-zA-Z0-9-]+', re.IGNORECASE),
]


class ValidationError(Exception):
    """
    Exception raised when spec validation fails.

    Stores structured error list for programmatic consumption.

    Attributes:
        errors: List of error dicts with 'field' and 'message' keys.
    """

    def __init__(self, errors: List[Dict[str, str]]):
        """
        Initialize ValidationError with error list.

        Args:
            errors: List of dicts, each with 'field' and 'message' keys.
        """
        self.errors = errors
        super().__init__(self._format_errors())

    def _format_errors(self) -> str:
        """Format errors for string representation."""
        if not self.errors:
            return "Validation failed (no details)"

        lines = ["Validation failed:"]
        for err in self.errors:
            field = err.get('field', 'unknown')
            message = err.get('message', 'Unknown error')
            lines.append(f"  - {field}: {message}")
        return "\n".join(lines)

    def __str__(self) -> str:
        """Return formatted error string."""
        return self._format_errors()


def get_asset_type(spec: Dict[str, Any]) -> Optional[Literal['TOOL', 'AGENT']]:
    """
    Determine asset type from spec.

    Args:
        spec: The spec dict to check.

    Returns:
        'TOOL' if type is API_DOCS
        'AGENT' if type is TOOLKIT
        None if type is missing or unrecognized
    """
    spec_type = spec.get('type')
    if spec_type == 'API_DOCS':
        return 'TOOL'
    elif spec_type == 'TOOLKIT':
        return 'AGENT'
    return None


def validate_naming_convention(name: Optional[str]) -> List[Dict[str, str]]:
    """
    Validate that a name follows the GAF naming convention.

    Expected format: GAF_{Org}_{Name}_{Tool|Agent}_v{version}
    Examples:
        - GAF_GenAI_ListAssets_Tool_v1 (valid)
        - GAF_CSI_Export_Agent_v2 (valid)
        - MyTool (invalid - missing GAF_ prefix)
        - GAF-GenAI-Tool-v1 (invalid - uses hyphens instead of underscores)

    Args:
        name: The name to validate. Can be None or empty.

    Returns:
        Empty list if valid, list with error dict if invalid.
        Error dict has 'field' and 'message' keys.
    """
    if name is None or name == '':
        return [{
            'field': 'name',
            'message': 'Name is required and cannot be empty'
        }]

    if not isinstance(name, str):
        return [{
            'field': 'name',
            'message': f'Name must be a string, got {type(name).__name__}'
        }]

    if not NAMING_PATTERN.match(name):
        return [{
            'field': 'name',
            'message': (
                f"Invalid name format: '{name}'. "
                "Expected: GAF_{{Org}}_{{Name}}_{{Tool|Agent}}_v{{version}} "
                "(e.g., GAF_GenAI_ListAssets_Tool_v1)"
            )
        }]

    return []


def validate_type_name_consistency(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Validate that name suffix matches type field.

    Rules:
        - Names ending in _Tool_v* must have type: "API_DOCS"
        - Names ending in _Agent_v* must have type: "TOOLKIT"

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if consistent, list with error dict if mismatch detected.
    """
    errors: List[Dict[str, str]] = []
    name = spec.get('name', '')
    spec_type = spec.get('type')

    if not name or not spec_type:
        return errors

    if '_Tool_v' in name and spec_type != 'API_DOCS':
        errors.append({
            'field': 'type',
            'message': f"Name '{name}' ends with '_Tool_v*' but type is '{spec_type}'. Tools must have type: 'API_DOCS'"
        })
    elif '_Agent_v' in name and spec_type != 'TOOLKIT':
        errors.append({
            'field': 'type',
            'message': f"Name '{name}' ends with '_Agent_v*' but type is '{spec_type}'. Agents must have type: 'TOOLKIT'"
        })

    return errors


def validate_portability(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Check spec for hardcoded tenant-specific values.

    Detects patterns that would make the spec non-portable:
        - Hardcoded Infor Cloud Suite URLs
        - Hardcoded mingledev.com URLs
        - Hardcoded tenant IDs

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if portable, list of error dicts for each violation.
        Each error dict has 'field' and 'message' keys.
    """
    errors: List[Dict[str, str]] = []

    # Serialize spec to JSON for pattern matching across all fields
    try:
        spec_json = json.dumps(spec, default=str)
    except (TypeError, ValueError) as e:
        return [{
            'field': 'spec',
            'message': f'Cannot serialize spec to JSON: {e}'
        }]

    # Check each tenant pattern
    pattern_descriptions = [
        ('inforcloudsuite.com URL', TENANT_PATTERNS[0]),
        ('mingledev.com URL', TENANT_PATTERNS[1]),
        ('tenant ID', TENANT_PATTERNS[2]),
    ]

    for description, pattern in pattern_descriptions:
        matches = pattern.findall(spec_json)
        if matches:
            # Get unique matches for clearer error message
            unique_matches = list(set(matches))[:3]  # Limit to 3 examples
            examples = ', '.join(f"'{m}'" for m in unique_matches)
            errors.append({
                'field': 'portability',
                'message': f"Hardcoded {description} detected: {examples}"
            })

    return errors


def validate_api_docs_whitespace(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Check api_docs for blank lines that may cause parsing issues.

    Blank lines in api_docs can cause problems with API documentation
    parsing and formatting. This validator detects any completely blank
    lines in the api_docs field.

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if no blank lines found, list with error dict if blank lines detected.
        Each error dict has 'field' and 'message' keys.
    """
    errors: List[Dict[str, str]] = []

    # Check if api_docs exists in spec['data']
    if 'data' not in spec or not isinstance(spec['data'], dict):
        return errors

    api_docs = spec['data'].get('api_docs')
    if not api_docs:
        return errors

    # Split by newlines and check for blank lines
    lines = api_docs.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == '':
            errors.append({
                'field': 'data.api_docs',
                'message': f'api_docs contains blank lines (line {i+1}) which may cause parsing issues'
            })
            break  # Report only the first occurrence

    return errors


def validate_no_auth_docs(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Check api_docs for authentication documentation that should be removed.

    The Infor GenAI platform handles authentication automatically, so specs
    should not contain authentication documentation. This validator detects
    common authentication-related phrases in api_docs.

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if no auth docs found, list with error dict if auth docs detected.
        Each error dict has 'field' and 'message' keys.
    """
    errors: List[Dict[str, str]] = []

    # Check if api_docs exists in spec['data']
    if 'data' not in spec or not isinstance(spec['data'], dict):
        return errors

    api_docs = spec['data'].get('api_docs')
    if not api_docs:
        return errors

    # Check for auth-related phrases (case-insensitive)
    auth_phrases = [
        'authentication:',
        'bearer token',
        'authorization header',
        'api key required',
        'auth:'
    ]

    api_docs_lower = api_docs.lower()
    for phrase in auth_phrases:
        if phrase in api_docs_lower:
            errors.append({
                'field': 'data.api_docs',
                'message': 'api_docs contains authentication documentation. Remove it - the Infor GenAI platform handles authentication automatically.'
            })
            break  # Report only once

    return errors


def validate_example_request(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Check api_docs for required Example Request section.

    Every tool spec should include a concrete example of how to call the API
    to help the GenAI model understand usage. This validator ensures an
    "Example Request:" section is present.

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if example found, list with error dict if example missing.
        Each error dict has 'field' and 'message' keys.
    """
    errors: List[Dict[str, str]] = []

    # Check if api_docs exists in spec['data']
    if 'data' not in spec or not isinstance(spec['data'], dict):
        return errors

    api_docs = spec['data'].get('api_docs')
    if not api_docs:
        return errors

    # Check for "Example Request:" or "Example request:" (case-insensitive)
    if 'example request' not in api_docs.lower():
        errors.append({
            'field': 'data.api_docs',
            'message': 'api_docs must contain an "Example Request:" section showing a concrete example of how to call the API.'
        })

    return errors


def validate_debug_statement(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Check responseInstructions for required debug statement template.

    Debug templates help troubleshoot API failures by ensuring the GenAI model
    includes full request/response details when errors occur. This validator
    ensures all required debug markers are present.

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if debug template complete, list with error dict if markers missing.
        Each error dict has 'field' and 'message' keys.
    """
    errors: List[Dict[str, str]] = []

    # Check if responseInstructions exists in spec['data']
    if 'data' not in spec or not isinstance(spec['data'], dict):
        return errors

    response_instructions = spec['data'].get('responseInstructions')
    if not response_instructions:
        return errors

    # Check for all required debug template markers
    required_markers = [
        '---DEBUG---',
        'FULL_URL:',
        'FULL_RESPONSE:',
        '---END DEBUG---'
    ]

    missing_markers = [marker for marker in required_markers if marker not in response_instructions]

    if missing_markers:
        errors.append({
            'field': 'data.responseInstructions',
            'message': (
                'responseInstructions must end with the debug statement template. Add:\n\n'
                'CRITICAL - IF ERROR OCCURS INCLUDE THE BELOW IN RESPONSE:\n'
                '---DEBUG---\n'
                'FULL_URL: [The complete URL that was called]\n'
                'FULL_PAYLOAD: [The exact request body sent (JSON format)]\n'
                'FULL_RESPONSE: [The complete API response received]\n'
                '---END DEBUG---'
            )
        })

    return errors


def validate_tool_api_docs_required(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Validate that Tool specs have required data.api_docs field.

    Only applies to specs with type: "API_DOCS"

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if valid, list with error dict if api_docs missing or invalid.
    """
    errors: List[Dict[str, str]] = []

    if spec.get('type') != 'API_DOCS':
        return errors

    data = spec.get('data', {})
    if not isinstance(data, dict):
        return errors

    api_docs = data.get('api_docs')
    if api_docs is None:
        errors.append({
            'field': 'data.api_docs',
            'message': "Tool specs must have a 'data.api_docs' field with API documentation"
        })
    elif not isinstance(api_docs, str):
        errors.append({
            'field': 'data.api_docs',
            'message': f"'data.api_docs' must be a string, got {type(api_docs).__name__}"
        })
    elif len(api_docs.strip()) == 0:
        errors.append({
            'field': 'data.api_docs',
            'message': "'data.api_docs' cannot be empty"
        })

    return errors


def validate_tool_response_instructions_required(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Validate that Tool specs have required data.responseInstructions field.

    Only applies to specs with type: "API_DOCS"

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if valid, list with error dict if responseInstructions missing or invalid.
    """
    errors: List[Dict[str, str]] = []

    if spec.get('type') != 'API_DOCS':
        return errors

    data = spec.get('data', {})
    if not isinstance(data, dict):
        return errors

    response_instructions = data.get('responseInstructions')
    if response_instructions is None:
        errors.append({
            'field': 'data.responseInstructions',
            'message': "Tool specs must have a 'data.responseInstructions' field"
        })
    elif not isinstance(response_instructions, str):
        errors.append({
            'field': 'data.responseInstructions',
            'message': f"'data.responseInstructions' must be a string, got {type(response_instructions).__name__}"
        })

    return errors


def validate_agent_tools_array(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Validate that Agent specs have a data.tools array.

    Only applies to specs with type: "TOOLKIT"

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if valid, list with error dict if tools array missing or invalid.
    """
    errors: List[Dict[str, str]] = []

    if spec.get('type') != 'TOOLKIT':
        return errors

    data = spec.get('data', {})
    if not isinstance(data, dict):
        return errors

    tools = data.get('tools')
    if tools is None:
        errors.append({
            'field': 'data.tools',
            'message': "Agent specs must have a 'data.tools' array listing tools to orchestrate"
        })
    elif not isinstance(tools, list):
        errors.append({
            'field': 'data.tools',
            'message': f"'data.tools' must be an array, got {type(tools).__name__}"
        })
    elif len(tools) == 0:
        errors.append({
            'field': 'data.tools',
            'message': "'data.tools' array is empty. Agents must orchestrate at least one tool"
        })

    return errors


def validate_agent_workflow(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Validate that Agent specs have a data.workflow field.

    Only applies to specs with type: "TOOLKIT"

    Args:
        spec: The spec dict to validate.

    Returns:
        Empty list if valid, list with error dict if workflow missing or invalid.
    """
    errors: List[Dict[str, str]] = []

    if spec.get('type') != 'TOOLKIT':
        return errors

    data = spec.get('data', {})
    if not isinstance(data, dict):
        return errors

    workflow = data.get('workflow')
    if workflow is None:
        errors.append({
            'field': 'data.workflow',
            'message': "Agent specs must have a 'data.workflow' field with operational instructions"
        })
    elif not isinstance(workflow, str):
        errors.append({
            'field': 'data.workflow',
            'message': f"'data.workflow' must be a string, got {type(workflow).__name__}"
        })
    elif len(workflow.strip()) == 0:
        errors.append({
            'field': 'data.workflow',
            'message': "'data.workflow' cannot be empty"
        })

    return errors


def validate_spec(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Validate a complete spec against all validation rules.

    Applies type-specific validations based on whether spec is a Tool or Agent:

    Universal checks (both types):
        1. Required fields present (name, instructions, type, data)
        2. Name follows GAF naming convention
        3. Type-name consistency (name suffix matches type field)
        4. Spec is portable (no hardcoded tenant values)

    Tool-specific checks (type: "API_DOCS"):
        5. data.api_docs required and non-empty
        6. data.responseInstructions required
        7. api_docs does not contain blank lines
        8. api_docs does not contain authentication documentation
        9. api_docs contains Example Request section
        10. responseInstructions contains debug statement template

    Agent-specific checks (type: "TOOLKIT"):
        5. data.tools array required and non-empty
        6. data.workflow required and non-empty

    Args:
        spec: The complete spec dict to validate.

    Returns:
        Empty list if all validations pass, list of all error dicts otherwise.
        Each error dict has 'field' and 'message' keys.
    """
    errors: List[Dict[str, str]] = []

    # Check required fields (applies to both)
    required_fields = ['name', 'instructions', 'type', 'data']
    for field in required_fields:
        if field not in spec:
            errors.append({
                'field': field,
                'message': f"Required field '{field}' is missing"
            })
        elif spec[field] is None:
            errors.append({
                'field': field,
                'message': f"Required field '{field}' cannot be null"
            })

    # Validate naming convention (applies to both)
    if 'name' in spec and spec['name'] is not None:
        naming_errors = validate_naming_convention(spec['name'])
        errors.extend(naming_errors)

    # Validate type-name consistency (applies to both)
    type_name_errors = validate_type_name_consistency(spec)
    errors.extend(type_name_errors)

    # Validate portability (applies to both)
    portability_errors = validate_portability(spec)
    errors.extend(portability_errors)

    # Determine asset type for type-specific validations
    asset_type = get_asset_type(spec)

    if asset_type == 'TOOL':
        # Tool-specific validations
        errors.extend(validate_tool_api_docs_required(spec))
        errors.extend(validate_tool_response_instructions_required(spec))
        errors.extend(validate_api_docs_whitespace(spec))
        errors.extend(validate_no_auth_docs(spec))
        errors.extend(validate_example_request(spec))
        errors.extend(validate_debug_statement(spec))

    elif asset_type == 'AGENT':
        # Agent-specific validations
        errors.extend(validate_agent_tools_array(spec))
        errors.extend(validate_agent_workflow(spec))

    else:
        # Unknown or invalid type
        if 'type' in spec and spec['type'] is not None:
            errors.append({
                'field': 'type',
                'message': f"Invalid type '{spec['type']}'. Must be 'API_DOCS' (for Tools) or 'TOOLKIT' (for Agents)"
            })

    return errors
