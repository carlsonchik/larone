"""LangGraph / LangChain message integration for LAR-1."""

from __future__ import annotations

from typing import Any

from lar1 import validate

LAR1_KEY = "lar-1"

# Default cognitive tags by node role name (substring match)
NODE_COGNITION: dict[str, str] = {
    "research": "obs",
    "retrieve": "obs",
    "critic": "rev",
    "review": "rev",
    "synth": "inf",
    "merge": "inf",
    "plan": "hyp",
    "memory": "mem",
}


def attach_lar1_message(message: Any, fields: dict[str, Any]) -> Any:
    """Attach LAR-1 to LangChain message additional_kwargs."""
    if not validate(fields):
        raise ValueError("Invalid LAR-1 fields")
    kwargs = dict(getattr(message, "additional_kwargs", {}) or {})
    kwargs[LAR1_KEY] = fields
    return message.model_copy(update={"additional_kwargs": kwargs})


def read_lar1_message(message: Any) -> dict[str, Any] | None:
    block = getattr(message, "additional_kwargs", {}).get(LAR1_KEY)
    if isinstance(block, dict) and validate(block):
        return block
    return None


def lar1_for_node(node_name: str, *, likelihood: float = 0.75) -> dict[str, Any]:
    """Suggest LAR-1 fields from LangGraph node name."""
    name = node_name.lower()
    cognition = "inf"
    for key, c in NODE_COGNITION.items():
        if key in name:
            cognition = c
            break
    return {
        "T": "now",
        "S": "here",
        "C": cognition,
        "E": "derived" if cognition == "inf" else "direct",
        "L": likelihood,
        "V": "unverified",
    }


def middleware_tag_node(node_name: str, message: Any) -> Any:
    """Auto-tag agent message from node name (LangGraph middleware helper)."""
    return attach_lar1_message(message, lar1_for_node(node_name))
