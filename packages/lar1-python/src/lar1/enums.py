"""LAR-1 v0.4 field enums."""

from __future__ import annotations

from typing import Final, Literal, TypedDict

TemporalFrame = Literal["now", "past", "recall", "future"]
SpatialFrame = Literal["here", "there", "meta"]
CognitionStance = Literal["obs", "hyp", "mem", "det", "inf", "rev"]
EvidenceGrounding = Literal["direct", "derived", "aggregated", "reported"]
VerificationStatus = Literal[
    "unverified", "verified_human", "verified_tool", "verified_crossref"
]

Lar1ErrorCode = Literal[
    "EMPTY_INPUT",
    "MISSING_PREFIX",
    "NO_PAIRS",
    "UNKNOWN_KEY",
    "INVALID_ENUM",
    "INVALID_LIKELIHOOD",
    "DUPLICATE_KEY",
    "MALFORMED_PAIR",
    "EMPTY_OBJECT",
]


class Lar1Fields(TypedDict, total=False):
    T: TemporalFrame
    S: SpatialFrame
    C: CognitionStance
    E: EvidenceGrounding
    L: float
    V: VerificationStatus
    # v0.4 fields
    R: float
    R_raw: int
    R_scale: int
    R_label: str
    R_strategy: str
    provenance_key: str


Lar1Envelope = TypedDict("Lar1Envelope", {"LAR-1": Lar1Fields})


ENUMS: Final[dict[str, tuple[str, ...]]] = {
    "T": ("now", "past", "recall", "future"),
    "S": ("here", "there", "meta"),
    "C": ("obs", "hyp", "mem", "det", "inf", "rev"),
    "E": ("direct", "derived", "aggregated", "reported"),
    "V": (
        "unverified",
        "verified_human",
        "verified_tool",
        "verified_crossref",
    ),
}

VALID_KEYS: Final[frozenset[str]] = frozenset({
    "T", "S", "C", "E", "L", "V",
    "R", "R_raw", "R_scale", "R_label", "R_strategy",
    "provenance_key",
})
FIELD_ORDER: Final[tuple[str, ...]] = (
    "T", "S", "C", "E", "L", "V",
    "R", "R_raw", "R_scale", "R_label", "R_strategy",
    "provenance_key",
)
PREFIX: Final[str] = "LAR:"