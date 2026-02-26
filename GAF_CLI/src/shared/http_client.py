"""
HTTP client with retry strategy.

Provides configured HTTP session with exponential backoff retry logic
for resilient API communication.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_http_session(timeout=(5, 10)):
    """
    Create HTTP session with exponential backoff retry strategy.

    Configures session with:
    - Max 5 retry attempts with exponential backoff
    - Retry on status codes: 429, 500, 502, 503, 504
    - Safe methods only (HEAD, GET, OPTIONS) retried by default
    - Connection pooling (10 connections per host)
    - Default timeout applied to all requests

    Args:
        timeout: Default timeout tuple (connect_timeout, read_timeout).
                Default: (5, 10) - 5s connect, 10s read.

    Returns:
        Configured requests.Session instance

    Example:
        session = create_http_session()
        response = session.get("https://api.example.com/resource")
    """
    # Create retry strategy with exponential backoff
    retry_strategy = Retry(
        total=5,  # Max 5 retry attempts
        backoff_factor=1,  # Delays: 0s, 2s, 4s, 8s, 16s
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        allowed_methods=["HEAD", "GET", "OPTIONS"],  # Safe methods only
        raise_on_status=False  # Let caller handle status codes
    )

    # Create HTTP adapter with retry strategy and connection pooling
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10
    )

    # Create session and mount adapter
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # Wrap request method to apply default timeout
    original_request = session.request

    def request_with_timeout(method, url, **kwargs):
        """Wrapper that applies default timeout if not specified."""
        kwargs.setdefault('timeout', timeout)
        return original_request(method, url, **kwargs)

    session.request = request_with_timeout

    return session
