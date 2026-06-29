"""Serialize and deserialize LAR-1 data."""

from __future__ import annotations

import json

from lar1.enums import FIELD_ORDER, PREFIX, Lar1Fields
from lar1.validate import validate, validate_envelope


def serialize(data: Lar1Fields) -> str:
    return json.dumps({"LAR-1": data}, separators=(",", ":"))


def deserialize(json_str: str) -> dict[str, Lar1Fields]:
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON") from exc
    if not validate_envelope(parsed):
        raise ValueError("Invalid LAR-1 envelope")
    return parsed


def deserialize_fields(json_str: str) -> Lar1Fields:
    return deserialize(json_str)["LAR-1"]


def _format_value(key: str, value: object) -> str:
    if key == "L" and isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def compact(data: Lar1Fields) -> str:
    parts: list[str] = []
    for key in FIELD_ORDER:
        if key in data:
            parts.append(f"{key}={_format_value(key, data[key])}")
    if not parts:
        raise ValueError("Cannot compact empty LAR-1 object")
    return PREFIX + ",".join(parts)
