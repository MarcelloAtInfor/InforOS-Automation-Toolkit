"""
Logging configuration with credential redaction.

Provides structured logging that automatically redacts sensitive information
like Bearer tokens, client secrets, and passwords.
"""

import logging
import re
import sys
from typing import Optional


class CredentialRedactionFilter(logging.Filter):
    """
    Logging filter that redacts sensitive credentials from log messages.

    Redacts:
    - Bearer tokens: "Bearer <token>" -> "Bearer ***REDACTED***"
    - JSON secret fields: "cs": "secret" -> "cs": "***REDACTED***"
    - Password parameters: password=value -> password=***REDACTED***
    """

    # Redaction patterns
    PATTERNS = [
        # Bearer tokens
        (re.compile(r'Bearer\s+[A-Za-z0-9._-]+'), 'Bearer ***REDACTED***'),

        # JSON client_secret, cs, sask fields (handles various quote styles and spacing)
        (re.compile(r'(["\']?(?:client_secret|cs|sask)["\']?\s*:\s*["\'])[^"\']+(["\'])'),
         r'\1***REDACTED***\2'),

        # Password parameters (URL params, form data, etc.)
        (re.compile(r'(password=)[^&\s]+'), r'\1***REDACTED***'),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Redact sensitive information from log record.

        Args:
            record: Log record to filter

        Returns:
            True (always - we redact but don't filter out records)
        """
        # Redact the message string
        if isinstance(record.msg, str):
            record.msg = self._redact(record.msg)

        # Redact formatted message if args are present
        if record.args:
            try:
                # Format message with args, then redact
                formatted = record.msg % record.args
                redacted = self._redact(formatted)
                # Clear args and set msg to redacted formatted message
                record.msg = redacted
                record.args = None
            except (TypeError, ValueError):
                # If formatting fails, just redact the original message
                pass

        return True

    def _redact(self, text: str) -> str:
        """
        Apply all redaction patterns to text.

        Args:
            text: Text to redact

        Returns:
            Redacted text
        """
        for pattern, replacement in self.PATTERNS:
            text = pattern.sub(replacement, text)
        return text


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging with credential redaction.

    Creates a StreamHandler to stdout with CredentialRedactionFilter applied.
    Sets a standard format for log messages.

    Args:
        level: Logging level (default: INFO)

    Returns:
        Logger instance for the calling module
    """
    # Create handler with stdout
    handler = logging.StreamHandler(sys.stdout)

    # Add credential redaction filter
    handler.addFilter(CredentialRedactionFilter())

    # Set format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True  # Override any existing configuration
    )

    # Return logger for calling module
    return logging.getLogger(__name__)
