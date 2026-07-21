"""Validate LAR-1 fields."""

from __future__ import annotations

from typing import Any

from lar1.enums import ENUMS, Lar1Fields

OPTIONAL_STRING_KEYS = frozenset({"R_label", "R_strategy", "provenance_key"})
OPTIONAL_INT_KEYS = frozenset({"R_raw", "R_scale"})


def _is_likelihood(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


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
        elif key == "R":
            if not _is_likelihood(value):
                return False
        elif key in OPTIONAL_INT_KEYS:
            if not _is_positive_int(value):
                return False
        elif key in OPTIONAL_STRING_KEYS:
            if not isinstance(value, str):
                return False
        else:
            return False

    return True


def validate_envelope(envelope: Any) -> bool:
    if not isinstance(envelope, dict) or "LAR-1" not in envelope:
        return False
    return validate(envelope["LAR-1"])