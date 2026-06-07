"""The agent contract every pipeline stage implements (ARCHITECTURE.md §3).

Deliberately minimal — "lightweight file-based pipeline, standard run()
contract" was the grill-validated choice over an agent framework. Each agent:
  - takes a LeadStore (the filesystem handoff) and a Target (what to hunt)
  - returns an AgentResult summarizing what it did
  - is independently runnable and independently testable

Adding agent #3 means: write a module implementing this Protocol, register it
in pipeline.py. Nothing else changes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..config import Target
from ..store import LeadStore


@dataclass
class AgentResult:
    agent: str
    processed: int
    created_or_updated: int
    skipped: int
    errors: list[str]

    def summary(self) -> str:
        line = f"{self.agent}: processed {self.processed}, wrote {self.created_or_updated}, skipped {self.skipped}"
        if self.errors:
            line += f", {len(self.errors)} error(s)"
        return line


class Agent(Protocol):
    name: str

    def run(self, store: LeadStore, target: Target) -> AgentResult:
        """Do the agent's job for one target (one area + one industry list),
        writing through the store's stage-scoped methods, and report what happened.
        Must not raise on a single bad record — collect it in AgentResult.errors
        and continue; a bad business shouldn't sink a whole run.
        """
        ...
