"""The thin runner — orders agents over targets (ARCHITECTURE.md §3).

Deliberately dumb: no state machine, no retries, no scheduling. It loops
targets, calls each agent's run() in sequence, and collects results. Adding
agent #3 is one line in STAGES below — that's the whole point of the
"lightweight file-based pipeline, standard contract" choice over a framework.
"""
from __future__ import annotations

from dataclasses import dataclass

from .agents import lead_finder, lead_prioritizer
from .agents.base import AgentResult
from .config import Settings, Target
from .store import LeadStore

# Pipeline order. To add a stage: write agents/<name>.py with a `run(store, target)`
# function returning AgentResult, then append it here.
STAGES = {
    "find": lead_finder,
    "prioritize": lead_prioritizer,
}


@dataclass
class RunReport:
    results: list[AgentResult]

    def summary(self) -> str:
        return "\n".join(r.summary() for r in self.results)


def run_stage(stage: str, store: LeadStore, targets: list[Target], *, limit: int | None = None) -> RunReport:
    """Run a single named stage across every target."""
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r} — choices: {', '.join(STAGES)}")
    module = STAGES[stage]
    if stage == "find" and limit is not None:
        results = [module.run(store, target, limit=limit) for target in targets]
    else:
        results = [module.run(store, target) for target in targets]
    return RunReport(results)


def run_all(store: LeadStore, targets: list[Target], *, limit: int | None = None) -> RunReport:
    """Run every stage, in pipeline order, across every target."""
    results: list[AgentResult] = []
    for name, module in STAGES.items():
        if name == "find" and limit is not None:
            results.extend(module.run(store, target, limit=limit) for target in targets)
        else:
            results.extend(module.run(store, target) for target in targets)
    return RunReport(results)


def resolve_targets(settings: Settings, *, area: str | None, industry: str | None, radius: str | None) -> list[Target]:
    """CLI-flag override vs config-file batch list (ARCHITECTURE.md §8):
    explicit --area/--industry wins for a one-off; otherwise use targets.yaml."""
    if area:
        return [Target(area=area, radius=radius or "5km", industries=[industry] if industry else [])]
    return settings.targets
