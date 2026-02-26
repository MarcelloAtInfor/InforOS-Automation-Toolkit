"""Data models for AES (Application Event System) configuration.

Each dataclass maps to a SyteLine IDO and provides:
  - to_insert_properties() -> list[dict] for IDO update API Changes[].Properties
  - from_ido_record(record) classmethod -> parse from IDO load response

Boolean fields use "1"/"0" strings (SyteLine convention).
"""
from __future__ import annotations

from dataclasses import dataclass, field


def _bool_str(value: bool) -> str:
    """Convert Python bool to SyteLine '1'/'0' string."""
    return "1" if value else "0"


def _parse_bool(value) -> bool:
    """Parse SyteLine boolean value to Python bool."""
    return str(value).strip().lower() in ("1", "true", "yes")


def _prop(name: str, value, modified: bool = True) -> dict:
    """Build a single IDO property dict for update API."""
    is_null = value is None or (isinstance(value, str) and value == "")
    return {
        "Name": name,
        "Value": "" if is_null else str(value),
        "Modified": modified,
        "IsNull": is_null,
    }


@dataclass
class EventAction:
    """An action within an AES event handler.

    Maps to the EventActions IDO.
    Keys: EventHandlerRowPointer + EvrEventName + RowPointer
    """

    sequence: int
    action_type: str
    parameters: str = ""
    description: str = ""
    row_pointer: str | None = None
    event_handler_row_pointer: str | None = None
    event_name: str | None = None

    def to_insert_properties(self) -> list[dict]:
        """Build Properties array for IDO insert (Action=1)."""
        props = [
            _prop("Sequence", self.sequence),
            _prop("ActionType", self.action_type),
        ]
        if self.parameters:
            props.append(_prop("Parameters", self.parameters))
        if self.description:
            props.append(_prop("Description", self.description))
        if self.event_handler_row_pointer:
            props.append(
                _prop("EventHandlerRowPointer", self.event_handler_row_pointer)
            )
        if self.event_name:
            props.append(_prop("EvrEventName", self.event_name))
        return props

    @classmethod
    def from_ido_record(cls, record: dict) -> EventAction:
        """Parse an EventAction from an IDO load response record."""
        return cls(
            sequence=int(record.get("Sequence", 0)),
            action_type=record.get("ActionType", ""),
            parameters=record.get("Parameters", "") or "",
            description=record.get("Description", "") or "",
            row_pointer=record.get("RowPointer"),
            event_handler_row_pointer=record.get("EventHandlerRowPointer"),
            event_name=record.get("EvrEventName")
                or record.get("EventName"),
        )

    def to_dict(self) -> dict:
        """Serializable dict for export/reference."""
        d = {
            "sequence": self.sequence,
            "actionType": self.action_type,
        }
        if self.parameters:
            d["parameters"] = self.parameters
        if self.description:
            d["description"] = self.description
        if self.row_pointer:
            d["rowPointer"] = self.row_pointer
        if self.event_handler_row_pointer:
            d["eventHandlerRowPointer"] = self.event_handler_row_pointer
        if self.event_name:
            d["eventName"] = self.event_name
        return d


@dataclass
class EventHandler:
    """An AES event handler configuration.

    Maps to the EventHandlers IDO.
    Keys: EventName + Sequence
    """

    event_name: str
    sequence: int
    description: str = ""
    ido_collections: str = ""
    synchronous: bool = False
    suspend: bool = False
    active: bool = True
    transactional: bool = True
    ignore_failure: bool = False
    overridable: bool = True
    triggering_property: str = ""
    applies_to_initiators: str = ""
    access_as: str = ""
    actions: list[EventAction] = field(default_factory=list)
    row_pointer: str | None = None

    def to_insert_properties(self) -> list[dict]:
        """Build Properties array for IDO insert (Action=1)."""
        return [
            _prop("EventName", self.event_name),
            _prop("Sequence", self.sequence),
            _prop("Description", self.description),
            _prop("IDOCollections", self.ido_collections),
            _prop("Synchronous", _bool_str(self.synchronous)),
            _prop("Suspend", _bool_str(self.suspend)),
            _prop("Active", _bool_str(self.active)),
            _prop("Transactional", _bool_str(self.transactional)),
            _prop("IgnoreFailure", _bool_str(self.ignore_failure)),
            _prop("Overridable", _bool_str(self.overridable)),
            _prop("TriggeringProperty", self.triggering_property, modified=bool(self.triggering_property)),
            _prop("AppliesToInitiators", self.applies_to_initiators, modified=bool(self.applies_to_initiators)),
            _prop("AccessAs", self.access_as, modified=bool(self.access_as)),
        ]

    @classmethod
    def from_ido_record(cls, record: dict) -> EventHandler:
        """Parse an EventHandler from an IDO load response record."""
        return cls(
            event_name=record.get("EventName", ""),
            sequence=int(record.get("Sequence", 0)),
            description=record.get("Description", "") or "",
            ido_collections=record.get("IDOCollections", "")
                or record.get("AppliesToObjects", "") or "",
            synchronous=_parse_bool(record.get("Synchronous", 0)),
            suspend=_parse_bool(record.get("Suspend", 0)),
            active=_parse_bool(record.get("Active", 0)),
            transactional=_parse_bool(record.get("Transactional", 0)),
            ignore_failure=_parse_bool(record.get("IgnoreFailure", 0)),
            overridable=_parse_bool(record.get("Overridable", 0)),
            triggering_property=record.get("TriggeringProperty", "") or "",
            applies_to_initiators=record.get("AppliesToInitiators", "") or "",
            access_as=record.get("AccessAs", "") or "",
            row_pointer=record.get("RowPointer"),
        )

    def to_dict(self) -> dict:
        """Serializable dict for export/reference."""
        d = {
            "eventName": self.event_name,
            "sequence": self.sequence,
            "description": self.description,
            "idoCollections": self.ido_collections,
            "synchronous": self.synchronous,
            "suspend": self.suspend,
            "active": self.active,
            "transactional": self.transactional,
            "ignoreFailure": self.ignore_failure,
            "overridable": self.overridable,
        }
        if self.triggering_property:
            d["triggeringProperty"] = self.triggering_property
        if self.applies_to_initiators:
            d["appliesToInitiators"] = self.applies_to_initiators
        if self.access_as:
            d["accessAs"] = self.access_as
        if self.row_pointer:
            d["rowPointer"] = self.row_pointer
        if self.actions:
            d["actions"] = [a.to_dict() for a in self.actions]
        return d
