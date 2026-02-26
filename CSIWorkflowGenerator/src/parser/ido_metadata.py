"""Live IDO metadata client for validating IDO names and properties.

Queries SyteLine IdoCollections and IdoProperties system IDOs to verify
that IDO names and property names referenced in a workflow spec actually
exist. Follows the AESBuilder pattern from src/aes_builder/builder.py.

Usage:
    from src.parser.ido_metadata import IdoMetadataClient

    client = IdoMetadataClient()
    assert client.ido_exists("SLCustomers")
    props = client.get_properties("SLCustomers")
    assert "CreditLimit" in props
"""
from __future__ import annotations

import difflib

from shared.auth import get_auth_headers
from shared.config import IDO_URL
from src.http_client import get as http_get, raise_for_status_with_detail

from shared.tenant import get_site


class IdoMetadataClient:
    """Query SyteLine IDO metadata for validation."""

    def __init__(self, site: str | None = None):
        site = site or get_site()
        self.site = site
        self._ido_cache: dict[str, bool] = {}
        self._prop_cache: dict[str, set[str]] = {}
        self._all_ido_names: list[str] | None = None

    def _headers(self) -> dict:
        """Get authenticated headers with site config."""
        headers = get_auth_headers()
        headers["X-Infor-MongooseConfig"] = self.site
        return headers

    def _ido_load(
        self,
        ido_name: str,
        properties: str,
        filter_str: str | None = None,
        record_cap: int = 100,
    ) -> list[dict]:
        """Load records from an IDO. Returns list of item dicts."""
        url = f"{IDO_URL()}/load/{ido_name}"
        params: dict = {"properties": properties, "recordCap": record_cap}
        if filter_str:
            params["filter"] = filter_str
        resp = http_get(url, headers=self._headers(), params=params)
        raise_for_status_with_detail(resp)
        data = resp.json()
        if not data.get("Success", True):
            msg = data.get("Message", "unknown error")
            raise RuntimeError(f"IDO load failed for {ido_name}: {msg}")
        return data.get("Items") or []

    def ido_exists(self, name: str) -> bool:
        """Check if an IDO collection exists in SyteLine (cached)."""
        if name in self._ido_cache:
            return self._ido_cache[name]

        items = self._ido_load(
            "IdoCollections",
            "CollectionName",
            f"CollectionName = '{name}'",
            record_cap=1,
        )
        exists = len(items) > 0
        self._ido_cache[name] = exists
        return exists

    def get_properties(self, ido_name: str) -> set[str]:
        """Get all property names for an IDO collection (cached)."""
        if ido_name in self._prop_cache:
            return self._prop_cache[ido_name]

        items = self._ido_load(
            "IdoProperties",
            "PropertyName",
            f"CollectionName = '{ido_name}'",
            record_cap=500,
        )
        props = {item["PropertyName"] for item in items if item.get("PropertyName")}
        self._prop_cache[ido_name] = props
        return props

    def property_exists(self, ido_name: str, prop_name: str) -> bool:
        """Check if a property exists on an IDO collection."""
        return prop_name in self.get_properties(ido_name)

    def find_case_match(self, ido_name: str, prop_name: str) -> str | None:
        """Find the correctly-cased property name (case-insensitive lookup).

        Returns the correct casing if found, None if no match at all.
        """
        props = self.get_properties(ido_name)
        lower_map = {p.lower(): p for p in props}
        return lower_map.get(prop_name.lower())

    def suggest_ido(self, name: str, n: int = 3) -> list[str]:
        """Suggest similar IDO names using fuzzy matching against SL% IDOs."""
        if self._all_ido_names is None:
            items = self._ido_load(
                "IdoCollections",
                "CollectionName",
                "CollectionName LIKE 'SL%'",
                record_cap=1000,
            )
            self._all_ido_names = [
                item["CollectionName"]
                for item in items
                if item.get("CollectionName")
            ]
        return difflib.get_close_matches(name, self._all_ido_names, n=n, cutoff=0.5)

    def suggest_property(
        self, ido_name: str, prop_name: str, n: int = 3
    ) -> list[str]:
        """Suggest similar property names using fuzzy matching."""
        props = self.get_properties(ido_name)
        return difflib.get_close_matches(prop_name, props, n=n, cutoff=0.5)
