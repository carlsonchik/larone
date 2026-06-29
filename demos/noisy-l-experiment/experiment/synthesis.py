"""Weighted synthesis helpers for LAR-1 experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Recommendation = Literal["hold", "deploy"]

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


@dataclass
class AgentOutput:
    name: str
    recommendation: Recommendation
    summary: str
    lar1: dict[str, Any] | None = None


def synthesis_weight(output: AgentOutput, *, use_lar1: bool) -> float:
    """Trust weight for one delegate output."""
    if not use_lar1:
        return 1.0

    lar = output.lar1
    if not lar:
        return 0.5

    l_val = float(lar.get("L", 0.5))
    c_val = COGNITION_WEIGHT.get(str(lar.get("C", "inf")), 0.5)
    v_val = VERIFICATION_FACTOR.get(str(lar.get("V", "unverified")), 0.7)
    return l_val * c_val * v_val


def weighted_decision(
    outputs: list[AgentOutput],
    *,
    use_lar1: bool,
) -> tuple[Recommendation, dict[str, float]]:
    """
    Synthesize a hold/deploy decision from delegate outputs.

    - no_lar1: majority vote (equal weights)
    - lar1: winner-take-all — follow the single highest-weight delegate
      (models synthesizers that over-trust one high-confidence source)
    """
    weights: dict[str, float] = {
        out.name: synthesis_weight(out, use_lar1=use_lar1) for out in outputs
    }

    if not use_lar1:
        hold_mass = sum(w for o in outputs if o.recommendation == "hold" for w in [weights[o.name]])
        deploy_mass = sum(w for o in outputs if o.recommendation == "deploy" for w in [weights[o.name]])
        decision: Recommendation = "hold" if hold_mass >= deploy_mass else "deploy"
        return decision, weights

    winner = max(outputs, key=lambda o: weights[o.name])
    return winner.recommendation, weights


def quality_score(decision: Recommendation, ground_truth: Recommendation) -> float:
    return 1.0 if decision == ground_truth else 0.0
