"""Tests for noisy-L experiment invariants."""

from experiment.scenarios import SCENARIOS
from experiment.synthesis import weighted_decision, quality_score


def test_accurate_lar1_beats_noisy_on_deploy_scenario():
    scenario = next(s for s in SCENARIOS if s.id == "deploy-config")
    accurate = scenario.build_outputs("accurate_lar1")
    noisy = scenario.build_outputs("noisy_lar1")
    none = scenario.build_outputs("no_lar1")

    d_acc, _ = weighted_decision(accurate, use_lar1=True)
    d_noisy, w_noisy = weighted_decision(noisy, use_lar1=True)
    d_none, _ = weighted_decision(none, use_lar1=False)

    assert quality_score(d_acc, "hold") == 1.0
    assert d_noisy == "deploy"
    assert quality_score(d_noisy, "hold") == 0.0
    assert d_none == "hold"
    assert w_noisy["optimist"] > w_noisy["load-tester"]


def test_all_scenarios_have_three_delegates():
    for scenario in SCENARIOS:
        for condition in ("no_lar1", "accurate_lar1", "noisy_lar1"):
            assert len(scenario.build_outputs(condition)) == 3
