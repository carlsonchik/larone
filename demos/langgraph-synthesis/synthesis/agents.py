"""Three agent stubs with LAR-1 metadata."""

from __future__ import annotations

from langchain_core.messages import AIMessage

from synthesis.lar1 import attach_lar1


def researcher(topic: str) -> AIMessage:
    """Gathers observations — high confidence direct evidence."""
    content = (
        f"[Researcher] Found 3 peer-reviewed sources on '{topic}'. "
        "Primary finding: adoption grows 40% YoY in agent tooling."
    )
    return attach_lar1(
        AIMessage(content=content),
        {
            "T": "now",
            "S": "here",
            "C": "obs",
            "E": "direct",
            "L": 0.85,
            "V": "verified_tool",
        },
    )


def critic(topic: str) -> AIMessage:
    """Reviews claims — lower confidence, revision stance."""
    content = (
        f"[Critic] The 40% figure on '{topic}' may conflate MCP and A2A adoption. "
        "Recommend citing primary surveys only."
    )
    return attach_lar1(
        AIMessage(content=content),
        {
            "T": "now",
            "S": "meta",
            "C": "rev",
            "E": "derived",
            "L": 0.62,
            "V": "unverified",
        },
    )


def researcher_hypothesis(topic: str) -> AIMessage:
    """Low-confidence hypothesis for contrast in baseline demo."""
    content = (
        f"[Researcher] Speculative: '{topic}' could reach 90% market share by 2028."
    )
    return attach_lar1(
        AIMessage(content=content),
        {
            "T": "future",
            "S": "there",
            "C": "hyp",
            "E": "reported",
            "L": 0.25,
            "V": "unverified",
        },
    )


def synthesizer(inputs: list[AIMessage], use_lar1: bool) -> AIMessage:
    """
    Merge agent outputs.
    With LAR-1: weight by L, C, V via synthesis_weight().
    Without: equal weighting.
    """
    from synthesis.lar1 import attach_lar1, synthesis_weight

    if not inputs:
        return AIMessage(content="[Synthesizer] No inputs.")

    weighted_lines: list[str] = []
    total_w = 0.0

    for msg in inputs:
        w = synthesis_weight(msg, use_lar1=use_lar1)
        total_w += w
        prefix = f"(w={w:.2f})" if use_lar1 else "(equal)"
        weighted_lines.append(f"{prefix} {msg.content}")

    if use_lar1:
        summary = (
            "[Synthesizer/LAR-1] Weighted merge favors observations over hypotheses. "
            f"Total weight mass: {total_w:.2f}\n"
            + "\n".join(weighted_lines)
        )
        lar = {"T": "now", "C": "inf", "E": "aggregated", "L": 0.78, "V": "unverified"}
    else:
        summary = (
            "[Synthesizer/Baseline] Equal merge — speculative claims treated same as facts.\n"
            + "\n".join(weighted_lines)
        )
        lar = {"T": "now", "C": "inf", "L": 0.5, "V": "unverified"}

    return attach_lar1(AIMessage(content=summary), lar)
