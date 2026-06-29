"""LAR-1 semantic overlay — reference Python SDK."""

from lar1.errors import Lar1ParseError
from lar1.parse import parse, parse_envelope
from lar1.serialize import compact, deserialize, deserialize_fields, serialize

__all__ = [
    "Lar1ParseError",
    "parse",
    "parse_envelope",
    "validate",
    "validate_envelope",
    "serialize",
    "deserialize",
    "deserialize_fields",
    "compact",
]

from lar1.validate import validate, validate_envelope

__version__ = "0.3.0"
