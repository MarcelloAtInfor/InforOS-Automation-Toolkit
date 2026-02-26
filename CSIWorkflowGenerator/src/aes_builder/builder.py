"""AES Configuration Builder — query, create, delete event handlers via IDO API.

Combines discovery (querying existing handlers) and mutation (creating/deleting)
in one class. Uses shared/auth.py and shared/config.py for authentication
and URL construction.

Usage:
    from src.aes_builder.builder import AESBuilder

    builder = AESBuilder()
    handler = builder.load_handler_with_actions("IdoOnItemUpdate", "ue_CreditLimit%")
    print(builder.export_handler(handler))
"""
from __future__ import annotations

import json

from shared.auth import get_auth_headers
from shared.config import IDO_URL
from shared.tenant import get_site
from src.http_client import get as http_get, post as http_post, raise_for_status_with_detail

from .models import EventAction, EventHandler

# IDO properties to fetch for each entity
_HANDLER_PROPS = (
    "EventName,Sequence,Description,IDOCollections,Synchronous,Suspend,"
    "Active,Transactional,IgnoreFailure,Overridable,TriggeringProperty,"
    "AppliesToInitiators,AccessAs,RowPointer"
)
_ACTION_PROPS = (
    "Sequence,ActionType,Parameters,Description,"
    "EventHandlerRowPointer,EvrEventName,RowPointer,"
    "EventName,EventHandlerSequence"
)


class AESBuilder:
    """Query and manage AES event handlers via the SyteLine IDO API."""

    def __init__(self, site: str | None = None):
        self.site = site or get_site()

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

    def _ido_insert(self, ido_name: str, properties: list[dict]) -> dict:
        """Insert a record into an IDO. Returns full API response."""
        url = f"{IDO_URL()}/update/{ido_name}"
        payload = {
            "IDOName": ido_name,
            "RefreshAfterSave": True,
            "Changes": [
                {
                    "Action": 1,  # Insert
                    "Properties": properties,
                }
            ],
        }
        resp = http_post(url, headers=self._headers(), json=payload)
        raise_for_status_with_detail(resp)
        data = resp.json()
        if not data.get("Success", True):
            msg = data.get("Message", "unknown error")
            raise RuntimeError(f"IDO insert failed for {ido_name}: {msg}")
        return data

    def _ido_update(self, ido_name: str, properties: list[dict]) -> dict:
        """Update a record in an IDO. Returns full API response.

        Properties must include key fields (Modified=False) for record
        identification and modified fields (Modified=True) for changes.
        """
        url = f"{IDO_URL()}/update/{ido_name}"
        payload = {
            "IDOName": ido_name,
            "RefreshAfterSave": True,
            "Changes": [
                {
                    "Action": 2,  # Update
                    "Properties": properties,
                }
            ],
        }
        resp = http_post(url, headers=self._headers(), json=payload)
        raise_for_status_with_detail(resp)
        data = resp.json()
        if not data.get("Success", True):
            msg = data.get("Message", "unknown error")
            raise RuntimeError(f"IDO update failed for {ido_name}: {msg}")
        return data

    def _ido_delete(
        self,
        ido_name: str,
        properties: list[dict],
        item_id: str | None = None,
    ) -> dict:
        """Delete a record from an IDO. Returns full API response.

        Args:
            ido_name: IDO name.
            properties: Key properties for record identification.
            item_id: Optional _ItemId for precise record targeting.
                Required for multi-table IDOs (e.g. EventActions) where
                property-based deletes hit SQL column ambiguity.
        """
        url = f"{IDO_URL()}/update/{ido_name}"
        change: dict = {
            "Action": 4,  # Delete (NOT 3 — Action=3 is a no-op)
            "Properties": properties,
        }
        if item_id:
            change["ItemId"] = item_id
        payload = {
            "IDOName": ido_name,
            "RefreshAfterSave": False,
            "Changes": [change],
        }
        resp = http_post(url, headers=self._headers(), json=payload)
        raise_for_status_with_detail(resp)
        data = resp.json()
        if not data.get("Success", True):
            msg = data.get("Message", "unknown error")
            raise RuntimeError(f"IDO delete failed for {ido_name}: {msg}")
        return data

    # ---- Query methods ----

    def load_handlers(
        self,
        event_name: str | None = None,
        description_filter: str | None = None,
        ido_filter: str | None = None,
    ) -> list[EventHandler]:
        """Load event handlers matching optional filters.

        Args:
            event_name: Exact event name (e.g. "IdoOnItemUpdate").
            description_filter: LIKE pattern for Description field.
            ido_filter: LIKE pattern for IDOCollections field.

        Returns:
            List of EventHandler instances (without actions populated).
        """
        filters = []
        if event_name:
            filters.append(f"EventName = '{event_name}'")
        if description_filter:
            if "%" in description_filter:
                filters.append(f"Description LIKE '{description_filter}'")
            else:
                filters.append(f"Description = '{description_filter}'")
        if ido_filter:
            if "%" in ido_filter:
                filters.append(f"IDOCollections LIKE '{ido_filter}'")
            else:
                filters.append(f"IDOCollections = '{ido_filter}'")

        filter_str = " AND ".join(filters) if filters else None
        items = self._ido_load("EventHandlers", _HANDLER_PROPS, filter_str)
        return [EventHandler.from_ido_record(item) for item in items]

    def load_actions(
        self,
        event_handler_row_pointer: str | None = None,
        event_name: str | None = None,
        handler_sequence: int | None = None,
    ) -> list[EventAction]:
        """Load event actions, optionally filtered by parent handler.

        Args:
            event_handler_row_pointer: Filter by parent handler RowPointer.
            event_name: Filter by event name.
            handler_sequence: Filter by handler sequence number.

        Returns:
            List of EventAction instances sorted by sequence.
        """
        filters = []
        if event_handler_row_pointer:
            filters.append(
                f"EventHandlerRowPointer = '{event_handler_row_pointer}'"
            )
        if event_name:
            filters.append(f"EventName = '{event_name}'")
        if handler_sequence is not None:
            filters.append(f"EventHandlerSequence = '{handler_sequence}'")

        filter_str = " AND ".join(filters) if filters else None
        items = self._ido_load("EventActions", _ACTION_PROPS, filter_str)
        actions = [EventAction.from_ido_record(item) for item in items]
        return sorted(actions, key=lambda a: a.sequence)

    def load_handler_with_actions(
        self,
        event_name: str,
        description: str,
    ) -> EventHandler:
        """Load a single handler by event name + description, with actions.

        Args:
            event_name: Event name (e.g. "IdoOnItemUpdate").
            description: Handler description (exact or LIKE pattern).

        Returns:
            EventHandler with actions populated.

        Raises:
            ValueError: If no matching handler found.
        """
        handlers = self.load_handlers(
            event_name=event_name,
            description_filter=description,
        )
        if not handlers:
            raise ValueError(
                f"No handler found: event={event_name}, desc={description}"
            )

        handler = handlers[0]
        if handler.row_pointer:
            handler.actions = self.load_actions(
                event_handler_row_pointer=handler.row_pointer
            )
        else:
            # Fall back to event name + sequence filter
            handler.actions = self.load_actions(
                event_name=handler.event_name,
                handler_sequence=handler.sequence,
            )
        return handler

    def export_handler(self, handler: EventHandler) -> dict:
        """Export handler + actions as a JSON-serializable reference dict."""
        return handler.to_dict()

    # ---- Create methods ----

    def create(self, handler: EventHandler) -> EventHandler:
        """Create an event handler with its actions.

        Two-step process:
        1. Insert handler record -> extract RowPointer from response
        2. Insert each action with parent RowPointer linkage

        Args:
            handler: EventHandler with actions to create.

        Returns:
            EventHandler with row_pointer populated from server response.
        """
        # Step 1: Insert handler
        handler_props = handler.to_insert_properties()
        resp = self._ido_insert("EventHandlers", handler_props)
        row_pointer = self._extract_row_pointer(resp)

        # Fallback: if response didn't include RowPointer, query for it
        if not row_pointer:
            print(f"  Response did not include RowPointer — querying...")
            found = self.load_handlers(
                event_name=handler.event_name,
                description_filter=handler.description,
            )
            if found:
                row_pointer = found[0].row_pointer
                handler.sequence = found[0].sequence  # may differ from requested

        handler.row_pointer = row_pointer

        print(f"  Handler created: {handler.description} "
              f"(event={handler.event_name}, seq={handler.sequence})")
        if row_pointer:
            print(f"  RowPointer: {row_pointer}")

        # Step 2: Insert actions with parent linkage
        for action in handler.actions:
            action.event_handler_row_pointer = row_pointer
            action.event_name = handler.event_name
            action_props = action.to_insert_properties()
            action_resp = self._ido_insert("EventActions", action_props)
            action_rp = self._extract_row_pointer(action_resp)
            if action_rp:
                action.row_pointer = action_rp
            print(f"    Action {action.sequence}: {action.action_type} created")

        return handler

    def verify_created_handler(self, handler: EventHandler) -> EventHandler | None:
        """Re-read a handler after creation to confirm actual field values.

        The system may auto-assign sequence numbers. This method reads
        back the handler by RowPointer to confirm what was actually stored.

        Returns:
            The handler as stored by the server, or None if not found.
        """
        if not handler.row_pointer:
            return None
        filter_str = f"RowPointer = '{handler.row_pointer}'"
        items = self._ido_load("EventHandlers", _HANDLER_PROPS, filter_str)
        if not items:
            return None
        return EventHandler.from_ido_record(items[0])

    # ---- Update methods ----

    def set_handler_active(
        self,
        event_name: str,
        sequence: int,
        active: bool,
    ) -> None:
        """Toggle the Active flag on an existing handler.

        Args:
            event_name: Event name (e.g. "IdoOnItemUpdate").
            sequence: Handler sequence number.
            active: True to activate, False to deactivate.

        Raises:
            ValueError: If no matching handler found.
        """
        # Find handler by exact event+sequence filter
        filter_str = f"EventName = '{event_name}' AND Sequence = '{sequence}'"
        items = self._ido_load("EventHandlers", _HANDLER_PROPS, filter_str)
        target = EventHandler.from_ido_record(items[0]) if items else None

        if target is None:
            raise ValueError(
                f"No handler found: event={event_name}, sequence={sequence}"
            )

        if not target.row_pointer:
            raise ValueError("Handler has no RowPointer — cannot update")

        self._ido_update("EventHandlers", [
            {"Name": "EventName", "Value": event_name,
             "Modified": False, "IsNull": False},
            {"Name": "Sequence", "Value": str(sequence),
             "Modified": False, "IsNull": False},
            {"Name": "RowPointer", "Value": target.row_pointer,
             "Modified": False, "IsNull": False},
            {"Name": "Active", "Value": "1" if active else "0",
             "Modified": True, "IsNull": False},
        ])
        status = "activated" if active else "deactivated"
        print(f"  Handler {status}: {target.description} "
              f"(event={event_name}, seq={sequence})")

    def _extract_row_pointer(self, response: dict) -> str | None:
        """Extract RowPointer from an IDO insert response.

        Tries multiple response patterns since exact format depends on
        IDO configuration. Logs full response if extraction fails.
        """
        # Pattern 1: Changes[0].Properties array with RowPointer
        changes = response.get("Changes") or []
        if changes:
            props = changes[0].get("Properties") or []
            for p in props:
                if p.get("Name") == "RowPointer" and p.get("Value"):
                    return p["Value"]

        # Pattern 2: Items[0].RowPointer (RefreshAfterSave response)
        items = response.get("Items") or []
        if items:
            rp = items[0].get("RowPointer")
            if rp:
                return rp

        # Pattern 3: Top-level RowPointer
        if response.get("RowPointer"):
            return response["RowPointer"]

        # Extraction failed — log for debugging
        print(f"  WARNING: Could not extract RowPointer from response.")
        print(f"  Response keys: {list(response.keys())}")
        print(f"  Full response: {json.dumps(response, indent=2)[:2000]}")
        return None

    # ---- Delete methods ----

    def _load_action_item_ids(
        self, event_handler_row_pointer: str
    ) -> dict[str, str]:
        """Load _ItemId for each action under a handler.

        EventActions is a multi-table IDO (EventAction + EventHandler +
        EventRevision). Property-based deletes hit SQL column ambiguity,
        so _ItemId is required for reliable deletion.

        Returns:
            Dict mapping action RowPointer -> _ItemId.
        """
        items = self._ido_load(
            "EventActions",
            "RowPointer,_ItemId",
            f"EventHandlerRowPointer = '{event_handler_row_pointer}'",
        )
        return {
            item["RowPointer"]: item["_ItemId"]
            for item in items
            if item.get("RowPointer") and item.get("_ItemId")
        }

    def delete_action(
        self,
        action_row_pointer: str,
        item_id: str,
    ) -> None:
        """Delete a single event action by RowPointer + _ItemId.

        Args:
            action_row_pointer: RowPointer of the action to delete.
            item_id: _ItemId from IDO load (required for multi-table delete).
        """
        self._ido_delete(
            "EventActions",
            [{"Name": "RowPointer", "Value": action_row_pointer,
              "Modified": False, "IsNull": False}],
            item_id=item_id,
        )

    def delete_handler(
        self,
        event_name: str,
        sequence: int,
    ) -> None:
        """Delete an event handler and its actions by event name + sequence.

        Actions are deleted first (child records), then the handler.

        Args:
            event_name: Event name (e.g. "IdoOnItemUpdate").
            sequence: Handler sequence number.
        """
        # Load handler by exact event+sequence filter
        filter_str = f"EventName = '{event_name}' AND Sequence = '{sequence}'"
        items = self._ido_load("EventHandlers", _HANDLER_PROPS, filter_str)
        target = EventHandler.from_ido_record(items[0]) if items else None

        if target is None:
            raise ValueError(
                f"No handler found: event={event_name}, sequence={sequence}"
            )

        if not target.row_pointer:
            raise ValueError(
                f"Handler has no RowPointer — cannot delete"
            )

        # Delete actions first (need _ItemId for multi-table IDO)
        actions = self.load_actions(
            event_handler_row_pointer=target.row_pointer
        )
        item_ids = self._load_action_item_ids(target.row_pointer)
        for action in actions:
            if action.row_pointer and action.row_pointer in item_ids:
                self.delete_action(
                    action.row_pointer, item_ids[action.row_pointer]
                )
                print(f"    Deleted action {action.sequence}: "
                      f"{action.action_type}")

        # Delete handler
        self._ido_delete("EventHandlers", [
            {"Name": "EventName", "Value": event_name,
             "Modified": False, "IsNull": False},
            {"Name": "Sequence", "Value": str(sequence),
             "Modified": False, "IsNull": False},
            {"Name": "RowPointer", "Value": target.row_pointer,
             "Modified": False, "IsNull": False},
        ])
        print(f"  Deleted handler: {target.description} "
              f"(event={event_name}, seq={sequence})")
