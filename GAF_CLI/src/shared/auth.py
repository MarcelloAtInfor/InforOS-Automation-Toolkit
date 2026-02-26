"""
OAuth token management with caching.

Provides TokenManager for acquiring and caching OAuth access tokens
from Infor OS token endpoint using client credentials flow.
"""

from datetime import datetime, timedelta
from typing import Optional

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from src.shared.config import Config


class TokenManager:
    """
    Manages OAuth token acquisition and caching.

    Uses password grant type (resource owner password credentials) to obtain
    access tokens from Infor OS using service account keys (SAAK/SASK).
    Tokens are cached and reused until near expiry (60s safety margin).
    """

    def __init__(self, config: Config):
        """
        Initialize TokenManager with configuration.

        Args:
            config: Configuration instance containing OAuth credentials
        """
        self._config = config
        self._token: Optional[dict] = None
        self._token_expires_at: Optional[datetime] = None

    def _fetch_token(self) -> dict:
        """
        Fetch new OAuth token from token endpoint.

        Uses service account keys (SAAK as username, SASK as password)
        with the password grant type required by Infor OS.

        Returns:
            Token dictionary containing access_token, token_type, expires_in

        Raises:
            OAuth2Error: If token acquisition fails
        """
        client = LegacyApplicationClient(client_id=self._config.client_id)
        oauth = OAuth2Session(client=client)

        token = oauth.fetch_token(
            token_url=self._config.token_url,
            username=self._config.saak,
            password=self._config.sask,
            client_id=self._config.client_id,
            client_secret=self._config.client_secret,
            timeout=(5, 10)  # 5s connect, 10s read
        )

        return token

    def get_valid_token(self) -> str:
        """
        Get valid access token, fetching new one if needed.

        Returns cached token if available and not expired.
        Otherwise fetches new token and caches it.

        Returns:
            Access token string

        Raises:
            OAuth2Error: If token acquisition fails
        """
        now = datetime.utcnow()

        # Return cached token if valid
        if self._token and self._token_expires_at and now < self._token_expires_at:
            return self._token['access_token']

        # Fetch new token
        self._token = self._fetch_token()

        # Cache with 60s safety margin before actual expiry
        expires_in = self._token.get('expires_in', 3600)
        self._token_expires_at = now + timedelta(seconds=expires_in - 60)

        return self._token['access_token']
