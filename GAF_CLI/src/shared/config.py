"""
Configuration loading from .ionapi files.

Provides secure parsing and validation of ION API credentials.
"""

import json
import os
from pathlib import Path
from typing import Optional


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""
    pass


class Config:
    """
    Loads and validates .ionapi configuration file.

    The .ionapi file must contain:
    - ti: Tenant ID
    - ci: Client ID
    - cs: Client Secret
    - iu: ION API URL
    - pu: PU URL
    - ot: OAuth Token URL
    """

    # Maximum allowed file size (1MB)
    MAX_FILE_SIZE = 1024 * 1024

    # Required fields in .ionapi file
    REQUIRED_FIELDS = {'ti', 'ci', 'cs', 'iu', 'pu', 'ot', 'saak', 'sask'}

    def __init__(self, ionapi_path: Optional[str] = None):
        """
        Initialize Config by loading .ionapi file.

        Args:
            ionapi_path: Path to .ionapi file. If None, uses IONAPI_FILE env var
                        or defaults to '.ionapi' in current directory.

        Raises:
            ConfigurationError: If file is missing, invalid, or contains errors.
        """
        if ionapi_path is None:
            ionapi_path = os.getenv('IONAPI_FILE', '.ionapi')

        self._path = Path(ionapi_path)
        self._data = self._load_and_validate()

    def _load_and_validate(self) -> dict:
        """Load and validate .ionapi file."""

        # Check file exists
        if not self._path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {self._path}"
            )

        # Security check: reject files > 1MB
        file_size = self._path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            raise ConfigurationError(
                f"Configuration file too large: {file_size} bytes "
                f"(max: {self.MAX_FILE_SIZE})"
            )

        # Load and parse JSON
        try:
            content = self._path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            raise ConfigurationError(
                f"Invalid file encoding in {self._path}: {e}"
            )

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in {self._path} at line {e.lineno}, "
                f"column {e.colno}: {e.msg}"
            )

        # Validate required fields
        if not isinstance(data, dict):
            raise ConfigurationError(
                f"Configuration must be a JSON object, got {type(data).__name__}"
            )

        missing_fields = self.REQUIRED_FIELDS - set(data.keys())
        if missing_fields:
            fields_list = ', '.join(sorted(missing_fields))
            raise ConfigurationError(
                f"Missing required fields in {self._path}: {fields_list}"
            )

        return data

    @property
    def tenant_id(self) -> str:
        """Tenant ID (ti)."""
        return self._data['ti']

    @property
    def client_id(self) -> str:
        """Client ID (ci)."""
        return self._data['ci']

    @property
    def client_secret(self) -> str:
        """Client Secret (cs)."""
        return self._data['cs']

    @property
    def token_url(self) -> str:
        """
        OAuth token URL constructed from PU URL (pu) and token endpoint (ot).

        Returns:
            Full token URL in format: {pu}{ot}
        """
        pu = self._data['pu'].rstrip('/')
        ot = self._data['ot']
        return f"{pu}/{ot}"

    @property
    def genai_base_url(self) -> str:
        """
        GenAI base URL constructed from ION API URL (iu) and tenant ID (ti).

        Returns:
            Base URL in format: {iu}/{ti}/
        """
        iu = self._data['iu'].rstrip('/')
        ti = self._data['ti']
        return f"{iu}/{ti}/"

    @property
    def ionapi_url(self) -> str:
        """ION API URL (iu)."""
        return self._data['iu']

    @property
    def pu_url(self) -> str:
        """PU URL (pu)."""
        return self._data['pu']

    @property
    def saak(self) -> str:
        """Service Account Access Key (saak)."""
        return self._data['saak']

    @property
    def sask(self) -> str:
        """Service Account Secret Key (sask)."""
        return self._data['sask']
