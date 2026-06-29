"""Run the noisy-L multi-agent synthesis experiment."""

from __future__ import annotations

from experiment.scenarios import CONDITIONS, SCENARIOS, Condition
from experiment.synthesis import quality_score, weighted_decision


def run_condition(condition: Condition) -> dict[str, float]:
    use_lar1 = condition != "no_lar1"
    scores: list[float] = []

    for scenario in SCENARIOS:
        outputs = scenario.build_outputs(condition)
        decision, weights = weighted_decision(outputs, use_lar1=use_lar1)
        score = quality_score(decision, scenario.ground_truth)
        scores.append(score)

        print(f"\n  [{scenario.id}] {scenario.title}")
        print(f"  {scenario.description}")
        for out in outputs:
            w = weights[out.name]
            lar = out.lar1 or {}
            l_tag = (
                f"L={lar.get('L', '-')} V={lar.get('V', '-')}"
                if lar
                else "no LAR-1"
            )
            print(
                f"    {out.name:12} -> {out.recommendation:6}  "
                f"w={w:.3f}  ({l_tag})"
            )
        mark = "OK" if score == 1.0 else "WRONG"
        print(f"  decision={decision}  expected={scenario.ground_truth}  [{mark}]")

    mean = sum(scores) / len(scores) if scores else 0.0
    return {"mean_quality": mean, "n": float(len(scores))}


def main() -> None:
    print("=" * 64)
    print("LAR-1 Noisy-L Experiment")
    print("=" * 64)
    print(
        "\nThree synthesis conditions across multi-agent scenarios.\n"
        "Ground truth: HOLD (do not take the risky action).\n"
        "Hypothesis: inflated L + fake V degrades decisions below no-LAR-1 baseline."
    )

    results: dict[str, float] = {}

    labels = {
        "no_lar1": "1. NO LAR-1 (equal weights)",
        "accurate_lar1": "2. ACCURATE LAR-1 (honest L, C, V)",
        "noisy_lar1": "3. NOISY LAR-1 (one delegate lies: L=0.99, V=verified)",
    }

    for condition in CONDITIONS:
        print("\n" + "=" * 64)
        print(labels[condition])
        print("=" * 64)
        summary = run_condition(condition)
        results[condition] = summary["mean_quality"]

    print("\n" + "=" * 64)
    print("SUMMARY — mean decision quality (1.0 = always correct)")
    print("=" * 64)
    for condition in CONDITIONS:
        q = results[condition]
        bar = "#" * int(q * 20)
        print(f"  {labels[condition]:42} {q:.2f}  {bar}")

    print("\nInterpretation:")
    if results["noisy_lar1"] < results["no_lar1"]:
        print(
            "  • Noisy LAR-1 scored LOWER than no metadata — "
            "self-reported confidence misled the synthesizer."
        )
    if results["accurate_lar1"] >= results["no_lar1"]:
        print(
            "  • Accurate LAR-1 matched or beat the equal-weight baseline — "
            "honest V and L help routing."
        )
    print(
        "  • This supports LAR-1 field V (verification): "
        "treat unverified high-L claims with discount or rejection."
    )
    print("\nReference: LDP noisy-provenance finding — arXiv:2603.08852")


if __name__ == "__main__":
    main()
