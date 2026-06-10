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


def test_prioritizer_pauses_when_credits_low(tmp_path, monkeypatch):
    from unittest.mock import MagicMock
    from leadpipe.agents import lead_prioritizer
    from leadpipe.store import LeadStore
    from leadpipe.config import Target
    from leadpipe.models import LeadCreate
    from datetime import date

    # Create a store and some "found" leads
    store = LeadStore(tmp_path / "leads.jsonl")
    for i in range(3):
        store.create(LeadCreate(
            place_id=f"p{i}",
            name=f"Pizza {i}",
            industry="restaurants",
            location="Austin, TX",
            has_website=False,
            found_date=date(2026, 1, 1),
        ))

    # Mock settings to set pause threshold to 70.0%
    monkeypatch.setenv("FIRECRAWL_PAUSE_CREDITS_PCT", "70.0")

    # Mock firecrawl.get_credit_usage to simulate credits at 65% remaining
    get_usage_mock = MagicMock(return_value={"remainingCredits": 650, "planCredits": 1000})
    monkeypatch.setattr(lead_prioritizer.firecrawl, "get_credit_usage", get_usage_mock)

    # Run the prioritizer
    target = Target(area="Austin, TX", radius="5km", industries=["restaurants"])
    res = lead_prioritizer.run(store, target)

    # It should immediately pause before processing any leads
    assert res.processed == 0
    assert res.created_or_updated == 0
    assert len(res.errors) == 1
    assert "dropped below" in res.errors[0]


def test_prioritizer_does_not_pause_when_credits_healthy(tmp_path, monkeypatch):
    from unittest.mock import MagicMock
    from leadpipe.agents import lead_prioritizer
    from leadpipe.store import LeadStore
    from leadpipe.config import Target
    from leadpipe.models import LeadCreate
    from datetime import date

    # Create a store and a lead
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(LeadCreate(
        place_id="p1",
        name="Pizza Joint",
        industry="restaurants",
        location="Austin, TX",
        has_website=False,
        found_date=date(2026, 1, 1),
    ))

    # Mock settings to set pause threshold to 70.0%
    monkeypatch.setenv("FIRECRAWL_PAUSE_CREDITS_PCT", "70.0")

    # Mock firecrawl.get_credit_usage to simulate credits at 80% remaining
    get_usage_mock = MagicMock(return_value={"remainingCredits": 800, "planCredits": 1000})
    monkeypatch.setattr(lead_prioritizer.firecrawl, "get_credit_usage", get_usage_mock)

    # Mock scrape and LLM estimate to return valid rating
    monkeypatch.setattr(lead_prioritizer.firecrawl, "scrape", lambda url: "some markdown")
    monkeypatch.setattr(lead_prioritizer, "_estimate_photo_count", lambda md: (10, "good"))

    # Run the prioritizer
    target = Target(area="Austin, TX", radius="5km", industries=["restaurants"])
    res = lead_prioritizer.run(store, target)

    # It should process the lead normally
    assert res.processed == 1
    assert res.created_or_updated == 1
    assert len(res.errors) == 0

