"""Multi-agent scenarios for the noisy-L experiment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

from experiment.synthesis import AgentOutput, Recommendation

Condition = Literal["no_lar1", "accurate_lar1", "noisy_lar1"]


@dataclass
class Scenario:
    id: str
    title: str
    ground_truth: Recommendation
    description: str
    build_outputs: Callable[[Condition], list[AgentOutput]]


def _deploy_config_scenario() -> Scenario:
    """Three delegates advise on a risky deployment (LDP-style)."""

    def build(condition: Condition) -> list[AgentOutput]:
        if condition == "no_lar1":
            return [
                AgentOutput(
                    "load-tester",
                    "hold",
                    "Load tests failed at 80% target traffic.",
                    None,
                ),
                AgentOutput(
                    "sre",
                    "hold",
                    "Error budget exhausted; rollback recommended.",
                    None,
                ),
                AgentOutput(
                    "optimist",
                    "deploy",
                    "Ship now — we can patch in prod if needed.",
                    None,
                ),
            ]

        if condition == "accurate_lar1":
            return [
                AgentOutput(
                    "load-tester",
                    "hold",
                    "Load tests failed at 80% target traffic.",
                    {
                        "T": "now",
                        "C": "obs",
                        "E": "direct",
                        "L": 0.88,
                        "V": "verified_tool",
                    },
                ),
                AgentOutput(
                    "sre",
                    "hold",
                    "Error budget exhausted; rollback recommended.",
                    {
                        "T": "now",
                        "C": "rev",
                        "E": "derived",
                        "L": 0.72,
                        "V": "verified_crossref",
                    },
                ),
                AgentOutput(
                    "optimist",
                    "deploy",
                    "Ship now — we can patch in prod if needed.",
                    {
                        "T": "future",
                        "C": "hyp",
                        "E": "reported",
                        "L": 0.22,
                        "V": "unverified",
                    },
                ),
            ]

        # noisy_lar1 — optimist lies about confidence and verification
        accurate = build("accurate_lar1")
        return [
            accurate[0],
            accurate[1],
            AgentOutput(
                "optimist",
                "deploy",
                "Ship now — we can patch in prod if needed.",
                {
                    "T": "now",
                    "C": "obs",
                    "E": "direct",
                    "L": 0.99,
                    "V": "verified_tool",
                },
            ),
        ]

    return Scenario(
        id="deploy-config",
        title="Risky production deploy",
        ground_truth="hold",
        description="Two reliable hold signals vs one reckless deploy push.",
        build_outputs=build,
    )


def _incident_triage_scenario() -> Scenario:
    def build(condition: Condition) -> list[AgentOutput]:
        if condition == "no_lar1":
            return [
                AgentOutput("logs", "hold", "Stack traces show memory leak in v2.", None),
                AgentOutput("metrics", "hold", "p99 latency doubled after release.", None),
                AgentOutput("junior", "deploy", "Likely unrelated — increase replicas.", None),
            ]

        if condition == "accurate_lar1":
            return [
                AgentOutput(
                    "logs",
                    "hold",
                    "Stack traces show memory leak in v2.",
                    {"C": "obs", "E": "direct", "L": 0.91, "V": "verified_tool"},
                ),
                AgentOutput(
                    "metrics",
                    "hold",
                    "p99 latency doubled after release.",
                    {"C": "obs", "E": "direct", "L": 0.86, "V": "verified_tool"},
                ),
                AgentOutput(
                    "junior",
                    "deploy",
                    "Likely unrelated — increase replicas.",
                    {"C": "hyp", "E": "reported", "L": 0.3, "V": "unverified"},
                ),
            ]

        accurate = build("accurate_lar1")
        return [
            accurate[0],
            accurate[1],
            AgentOutput(
                "junior",
                "deploy",
                "Likely unrelated — increase replicas.",
                {"C": "obs", "E": "direct", "L": 0.99, "V": "verified_human"},
            ),
        ]

    return Scenario(
        id="incident-triage",
        title="Incident triage under pressure",
        ground_truth="hold",
        description="Observability says hold; one delegate pushes scale-out.",
        build_outputs=build,
    )


def _schema_migration_scenario() -> Scenario:
    def build(condition: Condition) -> list[AgentOutput]:
        if condition == "no_lar1":
            return [
                AgentOutput("dba", "hold", "Migration lacks backfill validation.", None),
                AgentOutput("app", "hold", "Breaking change in API contract.", None),
                AgentOutput("pm", "deploy", "Deadline is today — ship migration.", None),
            ]

        if condition == "accurate_lar1":
            return [
                AgentOutput(
                    "dba",
                    "hold",
                    "Migration lacks backfill validation.",
                    {"C": "det", "E": "direct", "L": 0.9, "V": "verified_tool"},
                ),
                AgentOutput(
                    "app",
                    "hold",
                    "Breaking change in API contract.",
                    {"C": "inf", "E": "derived", "L": 0.77, "V": "verified_crossref"},
                ),
                AgentOutput(
                    "pm",
                    "deploy",
                    "Deadline is today — ship migration.",
                    {"C": "hyp", "E": "reported", "L": 0.35, "V": "unverified"},
                ),
            ]

        accurate = build("accurate_lar1")
        return [
            accurate[0],
            accurate[1],
            AgentOutput(
                "pm",
                "deploy",
                "Deadline is today — ship migration.",
                {"C": "inf", "E": "aggregated", "L": 0.98, "V": "verified_tool"},
            ),
        ]

    return Scenario(
        id="schema-migration",
        title="Database schema migration",
        ground_truth="hold",
        description="Engineering hold vs inflated business pressure.",
        build_outputs=build,
    )


SCENARIOS: list[Scenario] = [
    _deploy_config_scenario(),
    _incident_triage_scenario(),
    _schema_migration_scenario(),
]

CONDITIONS: list[Condition] = ["no_lar1", "accurate_lar1", "noisy_lar1"]
