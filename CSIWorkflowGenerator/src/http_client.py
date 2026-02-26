"""Resilient HTTP client with timeout, retry, and Infor error parsing."""
import time

import requests

DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, doubles each attempt
RETRYABLE_STATUS = {429, 502, 503, 504}

_session = None


def get_session() -> requests.Session:
    """Lazy-init a reusable session (connection pooling)."""
    global _session
    if _session is None:
        _session = requests.Session()
    return _session


def request(method, url, *, timeout=DEFAULT_TIMEOUT, retries=MAX_RETRIES, **kwargs):
    """Make HTTP request with timeout, retry on transient errors, and error parsing."""
    session = get_session()
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.request(method, url, timeout=timeout, **kwargs)
            if resp.status_code in RETRYABLE_STATUS and attempt < retries:
                wait = RETRY_BACKOFF * (2 ** (attempt - 1))
                print(f"  [RETRY] {resp.status_code} on {method} {url} "
                      f"— waiting {wait}s (attempt {attempt}/{retries})")
                time.sleep(wait)
                continue
            return resp
        except (requests.ConnectionError, requests.Timeout) as e:
            last_exc = e
            if attempt < retries:
                wait = RETRY_BACKOFF * (2 ** (attempt - 1))
                print(f"  [RETRY] {type(e).__name__} "
                      f"— waiting {wait}s (attempt {attempt}/{retries})")
                time.sleep(wait)
            else:
                raise
    raise last_exc  # unreachable but satisfies type checker


def raise_for_status_with_detail(resp: requests.Response):
    """Like raise_for_status() but includes JSON error body if available."""
    if resp.ok:
        return
    detail = ""
    try:
        body = resp.json()
        # Infor APIs return error info in various shapes
        detail = body.get("message") or body.get("Message") or body.get("error") or ""
        if isinstance(detail, dict):
            detail = str(detail)
    except Exception:
        pass
    msg = f"{resp.status_code} {resp.reason} for {resp.request.method} {resp.url}"
    if detail:
        msg += f"\n  Detail: {detail}"
    raise requests.HTTPError(msg, response=resp)


# Convenience wrappers
def get(url, **kwargs):
    return request("GET", url, **kwargs)


def post(url, **kwargs):
    return request("POST", url, **kwargs)


def put(url, **kwargs):
    return request("PUT", url, **kwargs)


def delete(url, **kwargs):
    return request("DELETE", url, **kwargs)
