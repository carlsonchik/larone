"""Compare baseline vs LAR-1 weighted synthesis."""

from __future__ import annotations

from synthesis.graph import run_pipeline


def main() -> None:
    topic = "semantic overlays for MCP"

    print("=" * 60)
    print("BASELINE (no LAR-1 weighting)")
    print("=" * 60)
    print(run_pipeline(topic, use_lar1=False, include_hypothesis=True))
    print()

    print("=" * 60)
    print("WITH LAR-1 (L × C × V weighting)")
    print("=" * 60)
    print(run_pipeline(topic, use_lar1=True, include_hypothesis=True))
    print()

    print("Note: With LAR-1, the hypothesis (C=hyp, L=0.25) is down-ranked")
    print("relative to the observation (C=obs, L=0.85, V=verified_tool).")


if __name__ == "__main__":
    main()
