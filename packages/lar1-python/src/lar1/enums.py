"""LAR-1 v0.4 field enums — includes R-register harness control primitives."""

from __future__ import annotations

from typing import Final, Literal, TypedDict

TemporalFrame = Literal["now", "past", "recall", "future"]
SpatialFrame = Literal["here", "there", "meta"]
CognitionStance = Literal["obs", "hyp", "mem", "det", "inf", "rev"]
EvidenceGrounding = Literal["direct", "derived", "aggregated", "reported"]
VerificationStatus = Literal[
    "unverified", "verified_human", "verified_tool", "verified_crossref"
]

# R-Register (Harness Control Primitives)
RRegisterRouting = Literal["passive", "moderate", "aggressive", "contextual"]
RRegisterTool = Literal["passthrough", "structured", "validated"]
RRegisterScale = Literal["single", "chain", "parallel", "graph", "adaptive"]
RRegisterMemory = Literal["none", "ephemeral", "persistent", "semantic", "relational"]
RRegisterStrategy = Literal["deterministic", "temperature", "top_p", "beam", "adaptive"]
RRegisterPlausibility = Literal["none", "confidence", "consistency", "crossref"]

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
    # Semantic overlay
    T: TemporalFrame
    S: SpatialFrame
    C: CognitionStance
    E: EvidenceGrounding
    L: float
    V: VerificationStatus
    # R-Register (harness control)
    R: RRegisterRouting
    R_raw: RRegisterTool
    R_scale: RRegisterScale
    R_label: RRegisterMemory
    R_strategy: RRegisterStrategy
    R_plausibility: RRegisterPlausibility


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
    "R": ("passive", "moderate", "aggressive", "contextual"),
    "R_raw": ("passthrough", "structured", "validated"),
    "R_scale": ("single", "chain", "parallel", "graph", "adaptive"),
    "R_label": ("none", "ephemeral", "persistent", "semantic", "relational"),
    "R_strategy": ("deterministic", "temperature", "top_p", "beam", "adaptive"),
    "R_plausibility": ("none", "confidence", "consistency", "crossref"),
}

VALID_KEYS: Final[frozenset[str]] = frozenset({
    "T", "S", "C", "E", "L", "V",
    "R", "R_raw", "R_scale", "R_label", "R_strategy", "R_plausibility",
})
FIELD_ORDER: Final[tuple[str, ...]] = (
    "T", "S", "C", "E", "L", "V",
    "R", "R_raw", "R_scale", "R_label", "R_strategy", "R_plausibility",
)
PREFIX: Final[str] = "LAR:"