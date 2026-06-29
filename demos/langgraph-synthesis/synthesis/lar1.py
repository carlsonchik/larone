"""Attach and read LAR-1 metadata on LangChain messages."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, BaseMessage

LAR1_KEY = "lar-1"

# Cognition weights for synthesizer (higher = more trust)
COGNITION_WEIGHT: dict[str, float] = {
    "obs": 1.0,
    "det": 0.95,
    "inf": 0.75,
    "rev": 0.6,
    "mem": 0.5,
    "hyp": 0.35,
}

VERIFICATION_FACTOR: dict[str, float] = {
    "verified_tool": 1.0,
    "verified_human": 1.0,
    "verified_crossref": 0.9,
    "unverified": 0.7,
}


def attach_lar1(message: AIMessage, fields: dict[str, Any]) -> AIMessage:
    """Merge LAR-1 fields into message additional_kwargs."""
    kwargs = dict(message.additional_kwargs)
    kwargs[LAR1_KEY] = fields
    return AIMessage(content=message.content, additional_kwargs=kwargs)


def read_lar1(message: BaseMessage) -> dict[str, Any] | None:
    """Read LAR-1 block from message metadata."""
    if not hasattr(message, "additional_kwargs"):
        return None
    block = message.additional_kwargs.get(LAR1_KEY)
    return block if isinstance(block, dict) else None


def synthesis_weight(message: BaseMessage, use_lar1: bool) -> float:
    """
    Compute trust weight for synthesizer.
    Baseline mode: equal weight (1.0).
    LAR-1 mode: combine L, C, and V.
    """
    if not use_lar1:
        return 1.0

    lar = read_lar1(message)
    if not lar:
        return 0.5

    l_val = float(lar.get("L", 0.5))
    c_val = COGNITION_WEIGHT.get(str(lar.get("C", "inf")), 0.5)
    v_val = VERIFICATION_FACTOR.get(str(lar.get("V", "unverified")), 0.7)

    return l_val * c_val * v_val
