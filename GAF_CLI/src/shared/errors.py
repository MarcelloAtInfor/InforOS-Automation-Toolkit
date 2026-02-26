"""
Structured error response helpers for Factory Tools and CLI scripts.

Provides consistent error formats that can be consumed programmatically
by the Factory Agent and other automation tools.
"""

from typing import Any, Dict, List


class ToolError:
    """
    Factory class for structured error responses.

    All methods return dicts with consistent keys:
        - error: Error type code (e.g., NOT_FOUND, VALIDATION_FAILED)
        - message: Human-readable error message

    Additional context fields vary by error type.

    Usage:
        response = ToolError.not_found('Tool', 'abc123')
        # Returns: {'error': 'NOT_FOUND', 'message': 'Tool not found: abc123', ...}
    """

    @staticmethod
    def not_found(resource_type: str, identifier: str) -> Dict[str, Any]:
        """
        Create a NOT_FOUND error response.

        Args:
            resource_type: Type of resource (e.g., 'Tool', 'Agent').
            identifier: The identifier that was not found (GUID or name).

        Returns:
            Dict with error='NOT_FOUND', message, and identifier.
        """
        return {
            "error": "NOT_FOUND",
            "message": f"{resource_type} not found: {identifier}",
            "identifier": identifier
        }

    @staticmethod
    def validation_failed(errors: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Create a VALIDATION_FAILED error response.

        Args:
            errors: List of validation error dicts with 'field' and 'message'.

        Returns:
            Dict with error='VALIDATION_FAILED', message, and details array.
        """
        return {
            "error": "VALIDATION_FAILED",
            "message": "Spec validation failed",
            "details": errors
        }

    @staticmethod
    def conflict(name: str, existing_guid: str) -> Dict[str, Any]:
        """
        Create a CONFLICT error response for duplicate assets.

        Args:
            name: Name of the asset that already exists.
            existing_guid: GUID of the existing asset.

        Returns:
            Dict with error='CONFLICT', message, name, and existing_guid.
        """
        return {
            "error": "CONFLICT",
            "message": f"Asset already exists: {name}",
            "name": name,
            "existing_guid": existing_guid
        }

    @staticmethod
    def api_error(message: str, status_code: int) -> Dict[str, Any]:
        """
        Create an API_ERROR response for failed API requests.

        Args:
            message: Error message describing the failure.
            status_code: HTTP status code from the API response.

        Returns:
            Dict with error='API_ERROR', message, and status_code.
        """
        return {
            "error": "API_ERROR",
            "message": message,
            "status_code": status_code
        }

    @staticmethod
    def internal_error(message: str) -> Dict[str, Any]:
        """
        Create an INTERNAL_ERROR response for unexpected failures.

        Args:
            message: Error message describing the internal failure.

        Returns:
            Dict with error='INTERNAL_ERROR' and message.
        """
        return {
            "error": "INTERNAL_ERROR",
            "message": message
        }
