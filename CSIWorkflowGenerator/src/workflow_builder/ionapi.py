"""ION API call builder for ionapi flowparts.

Builds the dual-encoded ionapi structure:
- ionApiMethod: compact dict (nulls omitted)
- method: JSON string of verbose dict (nulls included)

Both carry identical data but use different null-handling conventions.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class ApiInput:
    """An input parameter for an ION API call."""

    name: str
    description: str = ""
    swagger_datatype: str = "string"
    swagger_format: str | None = None
    required: bool = False
    type: str = "QUERY"
    wf_variable_name: str | None = None
    literal_value: str | None = None

    def to_compact_dict(self) -> dict:
        """For ionApiMethod (omit null fields)."""
        d: dict = {}
        if self.wf_variable_name is not None:
            d["wfVariableName"] = self.wf_variable_name
        if self.literal_value is not None:
            d["literalValue"] = self.literal_value
        d["name"] = self.name
        d["description"] = self.description
        d["swaggerDatatype"] = self.swagger_datatype
        if self.swagger_format is not None:
            d["swaggerFormat"] = self.swagger_format
        d["required"] = self.required
        d["type"] = self.type
        return d

    def to_verbose_dict(self) -> dict:
        """For method JSON string (include all fields, nulls explicit)."""
        return {
            "wfVariableName": self.wf_variable_name,
            "literalValue": self.literal_value,
            "name": self.name,
            "description": self.description,
            "swaggerDatatype": self.swagger_datatype,
            "swaggerFormat": self.swagger_format,
            "required": self.required,
            "type": self.type,
        }


@dataclass
class ApiOutput:
    """An output extraction from an ION API response."""

    wf_variable_name: str
    path: str
    type: str = "BODY"
    optional: bool = False

    def to_dict(self) -> dict:
        return {
            "wfVariableName": self.wf_variable_name,
            "type": self.type,
            "path": self.path,
            "optional": self.optional,
        }


@dataclass
class ApiInputBody:
    """The request body configuration for an ION API call."""

    name: str | None = None
    description: str | None = None
    required: bool = False
    available_input_content_types: list[str] = field(default_factory=list)
    input_content_type: str | None = None
    body: str = " "
    ignore: bool = True
    variable_names_from_body: list[str] = field(default_factory=list)
    structure_names_from_body: list[str] = field(default_factory=list)

    def to_compact_dict(self) -> dict:
        """For ionApiMethod (omit null fields)."""
        d: dict = {}
        if self.name is not None:
            d["name"] = self.name
        if self.description is not None:
            d["description"] = self.description
        d["required"] = self.required
        d["availableInputContentTypes"] = self.available_input_content_types
        if self.input_content_type is not None:
            d["inputContentType"] = self.input_content_type
        d["body"] = self.body
        d["ignore"] = self.ignore
        d["structureNamesFromBody"] = self.structure_names_from_body
        d["variableNamesFromBody"] = self.variable_names_from_body
        return d

    def to_verbose_dict(self) -> dict:
        """For method JSON string (include all fields)."""
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "availableInputContentTypes": self.available_input_content_types,
            "inputContentType": self.input_content_type,
            "body": self.body,
            "ignore": self.ignore,
            "variableNamesFromBody": self.variable_names_from_body,
            "structureNamesFromBody": self.structure_names_from_body,
        }


def _build_ionapi_method(
    product_logical_id: str,
    operation_proxy_path: str,
    operation_rest_path: str,
    product_name: str,
    summary: str,
    http_method: str,
    inputs: list[ApiInput],
    outputs: list[ApiOutput],
    input_body: ApiInputBody | None = None,
) -> tuple[dict, str]:
    """Build both ionApiMethod (compact) and method (JSON string).

    Args:
        input_body: Request body config. None produces null in verbose
            and omits from compact.

    Returns:
        (ionApiMethod_dict, method_json_string)
    """
    operation_path = f"{operation_proxy_path}{operation_rest_path}"

    base = {
        "productLogicalId": product_logical_id,
        "operationProxyPath": operation_proxy_path,
        "operationRestPath": operation_rest_path,
        "productName": product_name,
        "operationPath": operation_path,
        "summary": summary,
        "httpMethod": http_method,
        "availableOutputContentTypes": ["JSON"],
        "outputContentType": "JSON",
    }

    compact = dict(base)
    compact["input"] = [inp.to_compact_dict() for inp in inputs]
    compact["output"] = [out.to_dict() for out in outputs]
    if input_body is not None:
        compact["inputBody"] = input_body.to_compact_dict()

    verbose = dict(base)
    verbose["input"] = [inp.to_verbose_dict() for inp in inputs]
    verbose["output"] = [out.to_dict() for out in outputs]
    verbose["inputBody"] = input_body.to_verbose_dict() if input_body is not None else None

    method_str = json.dumps(verbose, separators=(",", ":"))

    return compact, method_str


# --- Standard SyteLine IDO API input definitions ---

_SYTELINE_PRODUCT = "infor.syteline"
_SYTELINE_NAME = "Infor SyteLine"
_IDO_PROXY_PATH = "CSI/IDORequestService/ido"


def _auth_header(literal_value: str | None = None) -> ApiInput:
    return ApiInput(
        name="Authorization",
        description=(
            "Token obtained through a call to SecurityToken, or if using the "
            "service through ION API, a valid OAuth 2.0 Bearer token "
            "(filled in automatically by Swagger UI)."
        ),
        swagger_datatype="string",
        required=False,
        type="HEADER",
        literal_value=literal_value,
    )


def _config_header(config_var: str) -> ApiInput:
    return ApiInput(
        name="X-Infor-MongooseConfig",
        description=(
            "Mongoose configuration to log into; required when using the "
            "service through ION API, not needed otherwise."
        ),
        swagger_datatype="string",
        required=False,
        type="HEADER",
        wf_variable_name=config_var,
    )


# Standard load endpoint optional parameters
_LOAD_OPTIONAL_INPUTS = [
    ApiInput(name="orderBy", description="SQL ORDER BY value", type="QUERY"),
    ApiInput(
        name="recordCap",
        description="Sets row cap: -1 = default in Mongoose; 0 = unlimited.",
        swagger_datatype="integer",
        type="QUERY",
    ),
    ApiInput(
        name="distinct",
        description="SQL DISTINCT keyword",
        swagger_datatype="boolean",
        type="QUERY",
    ),
    ApiInput(
        name="clm",
        description="Custom Load Method name",
        type="QUERY",
    ),
    ApiInput(
        name="clmParam",
        description="Comma-separated Custom Load Method parameters",
        swagger_datatype="array(null)",
        type="QUERY",
    ),
    ApiInput(
        name="loadType",
        description="Load type, one of FIRST | NEXT | PREVIOUS | LAST",
        type="QUERY",
    ),
    ApiInput(
        name="bookmark",
        description="Designate bookmark ID",
        type="QUERY",
    ),
    ApiInput(
        name="pqc",
        description="Post Query Command name",
        type="QUERY",
    ),
    ApiInput(
        name="readOnly",
        description="Read Only flag; if set to 'true', no ItemId is returned with query",
        swagger_datatype="boolean",
        type="QUERY",
    ),
]


def build_ido_load(
    ido_name: str | None = None,
    ido_var: str | None = None,
    properties: str | None = None,
    properties_var: str | None = None,
    filter_var: str = "",
    config_var: str = "MGConfig",
    output_mappings: list[ApiOutput] | None = None,
    service_account: str = "",
    auth_literal_value: str | None = None,
) -> dict:
    """Build an ionapi flowpart dict for IDO load (GET /load/{ido}).

    Args:
        ido_name: Literal IDO collection name (e.g. "SLCustomers").
        ido_var: Workflow variable name bound to the ido parameter.
        properties: Literal comma-separated property list.
        properties_var: Workflow variable name bound to properties.
        filter_var: Workflow variable name bound to the filter parameter.
        config_var: Workflow variable name for X-Infor-MongooseConfig.
        output_mappings: List of ApiOutput defining response extractions.
        service_account: Encrypted service account token.
        auth_literal_value: Literal value for Authorization header (None or "").

    Returns:
        Dict with method, ionApiMethod, serviceAccount, isCustom keys.
    """
    if output_mappings is None:
        output_mappings = []

    # IDO name: literal or variable-bound
    ido_input = ApiInput(
        name="ido",
        description="IDO name",
        swagger_datatype="string",
        required=True,
        type="PATH",
        literal_value=ido_name if ido_var is None else None,
        wf_variable_name=ido_var,
    )

    # Properties: literal or variable-bound
    props_input = ApiInput(
        name="properties",
        description=(
            "A comma-delimited property list. "
            "Provide\ufffd*\ufffd to include all, except subcollection properties."
        ),
        swagger_datatype="array(string)",
        required=True,
        type="QUERY",
        literal_value=properties if properties_var is None else None,
        wf_variable_name=properties_var,
    )

    inputs = [
        _auth_header(literal_value=auth_literal_value),
        _config_header(config_var),
        ido_input,
        props_input,
        ApiInput(
            name="filter",
            description="SQL filter string",
            type="QUERY",
            wf_variable_name=filter_var,
        ),
        *_LOAD_OPTIONAL_INPUTS,
    ]

    # Variable-bound mode uses null inputBody; literal mode uses empty inputBody
    use_variable_bound = ido_var is not None
    input_body = None if use_variable_bound else ApiInputBody()

    compact, method_str = _build_ionapi_method(
        product_logical_id=_SYTELINE_PRODUCT,
        operation_proxy_path=_IDO_PROXY_PATH,
        operation_rest_path="/load/{ido}",
        product_name=_SYTELINE_NAME,
        summary="LoadCollection",
        http_method="GET",
        inputs=inputs,
        outputs=output_mappings,
        input_body=input_body,
    )

    return {
        "method": method_str,
        "serviceAccount": service_account,
        "isCustom": True,
        "ionApiMethod": compact,
    }


def build_ido_update(
    ido_name: str | None = None,
    ido_var: str | None = None,
    changes_body: str = "",
    variable_names_from_body: list[str] | None = None,
    config_var: str = "MGConfig",
    output_mappings: list[ApiOutput] | None = None,
    service_account: str = "",
) -> dict:
    """Build an ionapi flowpart dict for IDO update (POST /update/{ido}).

    Args:
        ido_name: Literal IDO collection name (e.g. "SLCustomers").
        ido_var: Workflow variable name bound to the ido parameter.
        changes_body: JSON string for the request body (with $value() placeholders).
        variable_names_from_body: Variable names referenced in the body via $value().
        config_var: Workflow variable name for X-Infor-MongooseConfig.
        output_mappings: List of ApiOutput defining response extractions.
        service_account: Encrypted service account token.

    Returns:
        Dict with method, ionApiMethod, serviceAccount, isCustom keys.
    """
    if variable_names_from_body is None:
        variable_names_from_body = []
    if output_mappings is None:
        output_mappings = []

    # IDO name: literal or variable-bound
    ido_input = ApiInput(
        name="ido",
        description="IDO name",
        swagger_datatype="string",
        required=True,
        type="PATH",
        literal_value=ido_name if ido_var is None else None,
        wf_variable_name=ido_var,
    )

    inputs = [
        _auth_header(),
        _config_header(config_var),
        ido_input,
        ApiInput(
            name="refresh",
            description="Refresh after update flag",
            swagger_datatype="boolean",
            type="QUERY",
            literal_value="true",
        ),
    ]

    input_body = ApiInputBody(
        name="body",
        description="IDOUpdateItem structure",
        required=True,
        available_input_content_types=["JSON"],
        input_content_type="JSON",
        body=changes_body,
        ignore=False,
        variable_names_from_body=variable_names_from_body,
    )

    compact, method_str = _build_ionapi_method(
        product_logical_id=_SYTELINE_PRODUCT,
        operation_proxy_path=_IDO_PROXY_PATH,
        operation_rest_path="/update/{ido}",
        product_name=_SYTELINE_NAME,
        summary="UpdateCollection",
        http_method="POST",
        inputs=inputs,
        outputs=output_mappings,
        input_body=input_body,
    )

    return {
        "method": method_str,
        "serviceAccount": service_account,
        "isCustom": True,
        "ionApiMethod": compact,
    }
