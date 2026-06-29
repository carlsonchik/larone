"""Validate LAR-1 fields."""

from __future__ import annotations

from typing import Any

from lar1.enums import ENUMS, Lar1Fields


def _is_likelihood(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1


def validate(data: Lar1Fields | Any) -> bool:
    if not isinstance(data, dict) or not data:
        return False

    for key, value in data.items():
        if key in ENUMS:
            if value not in ENUMS[key]:
                return False
        elif key == "L":
            if not _is_likelihood(value):
                return False
        else:
            return False

    return True


def validate_envelope(envelope: Any) -> bool:
    if not isinstance(envelope, dict) or "LAR-1" not in envelope:
        return False
    return validate(envelope["LAR-1"])
