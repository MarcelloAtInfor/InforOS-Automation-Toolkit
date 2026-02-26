"""
GenAI API client wrapper.

Provides high-level interface to Infor OS GenAI APIs with integrated
authentication, logging, and error handling.
"""

import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.shared.config import Config
from src.shared.auth import TokenManager
from src.shared.http_client import create_http_session
from src.shared.logging import configure_logging


class GenAIClient:
    """
    Client for interacting with Infor OS GenAI APIs.

    Integrates configuration, OAuth authentication, HTTP retry logic,
    and logging with credential redaction for secure API communication.

    Example:
        client = GenAIClient()
        tools = client.list_tools()
        tool = client.get_tool("tool-guid-here")
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize GenAI client.

        Args:
            config_path: Path to .ionapi file. If None, uses IONAPI_FILE env var
                        or defaults to '.ionapi' in current directory.
        """
        # Initialize logging with credential redaction
        self._logger = configure_logging()

        # Load configuration
        self._config = Config(config_path)
        self._logger.info(f"Loaded configuration for tenant: {self._config.tenant_id}")

        # Initialize token manager for OAuth
        self._token_manager = TokenManager(self._config)

        # Create HTTP session with retry logic
        self._session = create_http_session()

    @property
    def _auth_headers(self) -> Dict[str, str]:
        """
        Get Authorization headers with valid Bearer token.

        Returns:
            Dictionary with Authorization header
        """
        token = self._token_manager.get_valid_token()
        return {"Authorization": f"Bearer {token}"}

    @property
    def coresvc_base(self) -> str:
        """
        Get base URL for GenAI Core Service API.

        Returns:
            Core service base URL in format: {base}/GENAI/coresvc/api/v1
        """
        base = self._config.genai_base_url.rstrip('/')
        return f"{base}/GENAI/coresvc/api/v1"

    @property
    def chatsvc_base(self) -> str:
        """
        Get base URL for GenAI Chat Service API.

        Returns:
            Chat service base URL in format: {base}/GENAI/chatsvc/api/v1
        """
        base = self._config.genai_base_url.rstrip('/')
        return f"{base}/GENAI/chatsvc/api/v1"

    def _request(self, method: str, url: str, timeout: Optional[int] = None, **kwargs) -> Any:
        """
        Make authenticated HTTP request with logging.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL to request
            timeout: Optional timeout in seconds. If None, uses session default.
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object

        Raises:
            requests.HTTPError: On non-2xx status codes
        """
        # Add authentication headers
        headers = kwargs.get('headers', {})
        headers.update(self._auth_headers)
        kwargs['headers'] = headers

        # Add timeout if specified
        if timeout is not None:
            kwargs['timeout'] = timeout

        # Log request (token will be redacted by logging filter)
        self._logger.info(f"{method} {url}")
        self._logger.debug(f"Headers: {headers}")

        # Make request
        response = self._session.request(method, url, **kwargs)

        # Log response
        self._logger.info(f"Response: {response.status_code}")

        # Raise on error status
        if not response.ok:
            error_msg = f"Request failed: {response.status_code} {response.reason}"
            try:
                error_detail = response.json()
                error_msg += f" - {error_detail}"
            except Exception:
                error_msg += f" - {response.text[:200]}"

            self._logger.error(error_msg)
            response.raise_for_status()

        return response

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available GenAI tools.

        Makes GET request to /api/v1/tools endpoint.

        Returns:
            List of tool dictionaries

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.coresvc_base}/tools"
        response = self._request("GET", url)
        tools = response.json()

        self._logger.info(f"Retrieved {len(tools)} tools")
        return tools

    def get_tool(self, guid: str) -> Dict[str, Any]:
        """
        Get specific tool by GUID.

        Makes GET request to /api/v1/tools/{guid} endpoint.

        Args:
            guid: Tool GUID

        Returns:
            Tool dictionary

        Raises:
            requests.HTTPError: If API request fails or tool not found
        """
        url = f"{self.coresvc_base}/tools/{guid}"
        response = self._request("GET", url)
        tool = response.json()

        self._logger.info(f"Retrieved tool: {tool.get('name', guid)}")
        return tool

    def create_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create one or more tools.

        Makes POST request to /api/v1/tools with array of ToolRequest objects.
        API expects array even for single tool - wrap in list.

        Args:
            tools: List of tool specification dictionaries. Each must contain:
                   - name: str (GAF naming convention)
                   - instructions: str
                   - type: str ("API", "TOOLKIT", or "FUNCTION")
                   - data: dict (type-specific configuration)
                   Optional fields: description, inputs, stubResponse, namespace

        Returns:
            List of created tool dictionaries with GUIDs assigned

        Raises:
            requests.HTTPError: If API request fails (e.g., 409 conflict, 422 validation)

        Example:
            tool_spec = {"name": "GAF_GenAI_Test_Tool_v1", "type": "API", ...}
            created = client.create_tools([tool_spec])
            print(created[0]["guid"])  # New GUID assigned
        """
        url = f"{self.coresvc_base}/tools"
        response = self._request("POST", url, json=tools)
        created_tools = response.json()

        self._logger.info(f"Created {len(created_tools)} tool(s)")
        for tool in created_tools:
            self._logger.info(f"  - {tool.get('name', 'unknown')} [{tool.get('guid', 'no-guid')}]")

        return created_tools

    def update_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update (upsert) an existing tool.

        Makes PUT request to /api/v1/tools with single ToolRequest object.
        Full replacement - provide complete spec including GUID.

        IMPORTANT: Tool spec MUST include 'guid' field for update.
        Without GUID, API treats this as create (upsert behavior).

        Args:
            tool: Complete tool specification dictionary with 'guid' field.
                  All fields from original tool should be included.

        Returns:
            Updated tool dictionary

        Raises:
            requests.HTTPError: If API request fails
            ValueError: If tool spec missing 'guid' field

        Example:
            existing = client.get_tool("some-guid")
            existing["description"] = "Updated description"
            updated = client.update_tool(existing)
        """
        if "guid" not in tool:
            raise ValueError("Tool spec must include 'guid' field for update. Use create_tools() for new tools.")

        url = f"{self.coresvc_base}/tools"
        response = self._request("PUT", url, json=tool)
        updated_tool = response.json()

        self._logger.info(f"Updated tool: {updated_tool.get('name', 'unknown')} [{updated_tool.get('guid', 'no-guid')}]")
        return updated_tool

    def delete_tool(self, guid: str) -> None:
        """
        Delete specific tool by GUID.

        Makes DELETE request to /api/v1/tools/{guid} endpoint.

        Args:
            guid: Tool GUID to delete

        Raises:
            requests.HTTPError: If API request fails (404 not found, 500 server error)
        """
        url = f"{self.coresvc_base}/tools/{guid}"
        self._request("DELETE", url)
        self._logger.info(f"Deleted tool: {guid}")

    def chat_sync(
        self,
        prompt: str,
        tools: Optional[List[str]] = None,
        session: Optional[str] = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Send synchronous chat message to GenAI Chat API.

        Args:
            prompt: User message (max 5000 chars per API constraint)
            tools: List of tool names/GUIDs to use. If None/empty, uses all active tools.
            session: Session ID for multi-turn conversations. If None, API creates new session.
            timeout: Request timeout in seconds (default 300s for complex agent operations)

        Returns:
            ChatResponse dict with keys:
            - session: str (session ID for continuation)
            - id: str (message ID)
            - content: str (agent response text)
            - warnings: list (any warnings)
            - links: list (optional hyperlinks)
            - followups: list (optional suggested followups)
            - screen_navigation: dict (optional Infor OS screen nav)

        Raises:
            requests.HTTPError: If API request fails (422 for validation, 500 for server error)
        """
        url = f"{self.chatsvc_base}/chat/sync"

        payload = {"prompt": prompt}
        if tools:
            payload["tools"] = tools
        if session:
            payload["session"] = session

        self._logger.info(f"Chat request (session: {session or 'new'})")
        response = self._request("POST", url, json=payload, timeout=timeout)
        chat_response = response.json()

        self._logger.info(f"Chat response in session: {chat_response.get('session')}")
        return chat_response

    def chat(
        self,
        prompt: str,
        tools: Optional[List[str]] = None,
        session: Optional[str] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Send async chat message (fire-and-forget).

        Uses POST /chat which returns immediately. The agent processes
        the request asynchronously on the platform. Use get_session_messages()
        or poll_for_response() to retrieve the result.

        Args:
            prompt: User message
            tools: List of tool/agent names to route to
            session: Session ID (use uuid.uuid4().hex for dashless format)
            timeout: HTTP timeout in seconds (default 30s, fire-and-forget)

        Returns:
            Raw response dict (typically {"warnings": [], "message": "Message sent"})
        """
        url = f"{self.chatsvc_base}/chat"

        payload = {"prompt": prompt}
        if tools:
            payload["tools"] = tools
        if session:
            payload["session"] = session

        self._logger.info(f"Async chat submit (session: {session or 'new'})")
        response = self._request("POST", url, json=payload, timeout=timeout)
        return response.json()

    def get_session_messages(
        self,
        session_id: str,
        page: int = 1,
        size: int = 50,
        timeout: int = 15
    ) -> Dict[str, Any]:
        """
        Get messages for a chat session.

        Args:
            session_id: Session ID (dashless hex format)
            page: Page number (0-based)
            size: Page size
            timeout: HTTP timeout in seconds

        Returns:
            Normalized dict: {"items": [...], "count": int}
            Items ordered newest-first by the platform.
        """
        url = f"{self.chatsvc_base}/sessions/{session_id}/messages"
        params = {"page": page, "size": size}

        response = self._request("GET", url, params=params, timeout=timeout)
        data = response.json()

        # Normalize platform's inconsistent response formats
        if isinstance(data, list):
            return {"items": data, "count": len(data)}
        elif isinstance(data, dict):
            items = data.get("items", data.get("messages", []))
            count = data.get("count", data.get("totalCount", len(items)))
            return {"items": items, "count": count}
        else:
            return {"items": [], "count": 0}

    def poll_for_response(
        self,
        session_id: str,
        expected_count: int,
        poll_interval: int = 10,
        max_polls: int = 60,
        on_poll: Optional[Callable] = None
    ) -> Tuple[Optional[str], int, float]:
        """
        Poll session messages until a new LLM response appears.

        Polls get_session_messages() until message count exceeds
        expected_count, then returns the newest LLM message content.

        Args:
            session_id: Session ID (dashless hex)
            expected_count: Current known message count; polling waits for count > this
            poll_interval: Seconds between polls (default 10)
            max_polls: Maximum poll attempts before timeout (default 60)
            on_poll: Optional callback fn(attempt, elapsed, count, expected) for logging

        Returns:
            Tuple of (llm_content, new_count, elapsed_seconds).
            llm_content is None if polling timed out.
        """
        t0 = time.time()

        for attempt in range(1, max_polls + 1):
            time.sleep(poll_interval)

            try:
                data = self.get_session_messages(session_id)
            except Exception as e:
                elapsed = time.time() - t0
                self._logger.warning(f"Poll {attempt} error: {e}")
                if on_poll:
                    on_poll(attempt, elapsed, -1, expected_count)
                continue

            items = data.get("items", [])
            count = data.get("count", 0)
            elapsed = time.time() - t0

            if on_poll:
                on_poll(attempt, elapsed, count, expected_count)

            if count > expected_count:
                # Find newest LLM message (items are newest-first)
                llm_messages = [m for m in items if m.get("sender") == "LLM"]
                if llm_messages:
                    content = llm_messages[0].get("content", "")
                    return content, count, elapsed

        elapsed = time.time() - t0
        return None, expected_count, elapsed
