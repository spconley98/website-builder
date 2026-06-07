"""Tests for the agent contract and the deterministic rating function.

The rating thresholds are explicitly "tune later" (ARCHITECTURE.md) — this
test pins the CURRENT behavior so a future tuning change is a deliberate,
visible diff here, not a silent drift.
"""
from __future__ import annotations

from leadpipe.agents.base import AgentResult
from leadpipe.agents.lead_prioritizer import rate_from_count


def test_rate_from_count_thresholds():
    assert rate_from_count(0) == 0
    assert rate_from_count(1) == 1
    assert rate_from_count(4) == 1
    assert rate_from_count(5) == 2
    assert rate_from_count(14) == 2
    assert rate_from_count(15) == 3
    assert rate_from_count(29) == 3
    assert rate_from_count(30) == 4
    assert rate_from_count(59) == 4
    assert rate_from_count(60) == 5
    assert rate_from_count(1000) == 5


def test_agent_result_summary_reports_errors():
    result = AgentResult("lead_finder", processed=10, created_or_updated=8, skipped=2, errors=["a", "b"])
    summary = result.summary()
    assert "processed 10" in summary
    assert "wrote 8" in summary
    assert "skipped 2" in summary
    assert "2 error(s)" in summary


def test_agent_result_summary_omits_errors_when_clean():
    result = AgentResult("lead_finder", processed=5, created_or_updated=5, skipped=0, errors=[])
    assert "error" not in result.summary()
