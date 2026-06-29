"""Parse LAR-1 compact strings."""

from __future__ import annotations

from lar1.enums import ENUMS, PREFIX, VALID_KEYS, Lar1Fields
from lar1.errors import Lar1ParseError


def _assert_enum(key: str, value: str) -> str:
    allowed = ENUMS[key]
    if value not in allowed:
        raise Lar1ParseError("INVALID_ENUM", f"Invalid {key}={value}")
    return value


def _parse_likelihood(raw: str) -> float:
    try:
        n = float(raw)
    except ValueError:
        raise Lar1ParseError("INVALID_LIKELIHOOD", f"Invalid L={raw}") from None
    if n < 0 or n > 1:
        raise Lar1ParseError("INVALID_LIKELIHOOD", f"L out of range: {n}")
    return n


def parse(compact: str) -> Lar1Fields:
    """Parse compact string into inner LAR-1 fields."""
    trimmed = compact.strip()
    if trimmed == "":
        raise Lar1ParseError("EMPTY_INPUT")
    if not trimmed.startswith(PREFIX):
        raise Lar1ParseError("MISSING_PREFIX")

    body = trimmed[len(PREFIX) :]
    if body == "":
        raise Lar1ParseError("NO_PAIRS")

    pairs = body.split(",")
    if not pairs or (len(pairs) == 1 and pairs[0] == ""):
        raise Lar1ParseError("NO_PAIRS")

    seen: set[str] = set()
    data: Lar1Fields = {}

    for pair in pairs:
        if "=" not in pair:
            raise Lar1ParseError("MALFORMED_PAIR", f"Missing '=': {pair}")
        key, _, value = pair.partition("=")
        key = key.strip()
        value = value.strip()

        if key not in VALID_KEYS:
            raise Lar1ParseError("UNKNOWN_KEY", f"Unknown key: {key}")
        if key in seen:
            raise Lar1ParseError("DUPLICATE_KEY", f"Duplicate key: {key}")
        seen.add(key)

        if key == "L":
            data["L"] = _parse_likelihood(value)
        elif key in ENUMS:
            data[key] = _assert_enum(key, value)  # type: ignore[literal-required]

    return data


def parse_envelope(compact: str) -> dict[str, Lar1Fields]:
    return {"LAR-1": parse(compact)}
