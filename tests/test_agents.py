"""Tests for the agent contract and the deterministic rating function.

The rating thresholds are explicitly "tune later" (ARCHITECTURE.md) — this
test pins the CURRENT behavior so a future tuning change is a deliberate,
visible diff here, not a silent drift.
"""
from __future__ import annotations

from datetime import date

from leadpipe.agents.base import AgentResult
from leadpipe.agents import website_intelligence
from leadpipe.agents.lead_prioritizer import (
    _matches_target,
    _parse_photo_count_response,
    rate_from_count,
    score_from_signals,
)
from leadpipe.config import load_settings
from leadpipe.config import Target
from leadpipe.models import Lead, LeadCreate, LeadPrioritization, LeadStatus
from leadpipe.store import LeadStore


def test_prioritizer_pauses_when_credits_low(tmp_path, monkeypatch):
    from unittest.mock import MagicMock

    from leadpipe.agents import lead_prioritizer

    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(
        LeadCreate(
            place_id="p1",
            name="Pizza Joint",
            industry="restaurants",
            location="Austin, TX",
            has_website=False,
            found_date=date(2026, 1, 1),
        )
    )

    monkeypatch.setenv("FIRECRAWL_PAUSE_CREDITS_PCT", "70.0")
    monkeypatch.setattr(
        lead_prioritizer.firecrawl,
        "get_credit_usage",
        MagicMock(return_value={"remainingCredits": 650, "planCredits": 1000}),
    )

    target = Target(area="Austin, TX", radius="5km", industries=["restaurants"])
    res = lead_prioritizer.run(store, target)

    assert res.processed == 0
    assert res.created_or_updated == 0
    assert len(res.errors) == 1
    assert "dropped below" in res.errors[0]


def test_prioritizer_does_not_pause_when_credits_healthy(tmp_path, monkeypatch):
    from unittest.mock import MagicMock

    from leadpipe.agents import lead_prioritizer

    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(
        LeadCreate(
            place_id="p1",
            name="Pizza Joint",
            industry="restaurants",
            location="Austin, TX",
            has_website=False,
            found_date=date(2026, 1, 1),
            google_maps_url="https://maps.example/p1",
        )
    )

    monkeypatch.setenv("FIRECRAWL_PAUSE_CREDITS_PCT", "70.0")
    monkeypatch.setattr(
        lead_prioritizer.firecrawl,
        "get_credit_usage",
        MagicMock(return_value={"remainingCredits": 800, "planCredits": 1000}),
    )
    monkeypatch.setattr(lead_prioritizer.firecrawl, "scrape", lambda url: "some markdown")
    monkeypatch.setattr(lead_prioritizer, "_estimate_photo_count", lambda md: (10, "good"))

    target = Target(area="Austin, TX", radius="5km", industries=["restaurants"])
    res = lead_prioritizer.run(store, target)

    assert res.processed == 1
    assert res.created_or_updated == 1
    assert len(res.errors) == 0


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


def test_score_from_signals_uses_soft_penalties():
    strong = score_from_signals(
        photo_count=30,
        phone_present=True,
        recent_review_count=3,
        hours_present=True,
        staleness_flags=[],
    )
    stale = score_from_signals(
        photo_count=30,
        phone_present=False,
        recent_review_count=0,
        hours_present=False,
        staleness_flags=["missing_phone", "missing_hours", "no_recent_reviews"],
    )
    legacy_unknown = score_from_signals(
        photo_count=30,
        phone_present=None,
        recent_review_count=None,
        hours_present=None,
        staleness_flags=[],
    )

    assert strong == 81
    assert stale == 45
    assert legacy_unknown == 60


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


def test_blank_llm_env_values_fall_back_to_defaults(tmp_path, monkeypatch):
    targets = tmp_path / "targets.yaml"
    targets.write_text("targets: []\n", encoding="utf-8")
    monkeypatch.setenv("LLM_MODEL", "")
    monkeypatch.setenv("LLM_BASE_URL", "   ")

    settings = load_settings(targets)

    assert settings.llm_model == "gemma4-fast"
    assert settings.llm_base_url == "http://localhost:11434/v1"


def test_prioritizer_target_match_accepts_formatted_street_address():
    lead = Lead(
        place_id="p1",
        name="Fresh Brew Cafe",
        industry="coffee shops",
        location="250 University Blvd, Round Rock, TX 78665, USA",
        has_website=False,
        found_date=date(2026, 6, 7),
    )
    target = Target(area="Round Rock, TX", radius="5km", industries=["coffee shops"])

    assert _matches_target(lead, target)


def test_prioritizer_empty_industries_still_scopes_to_area():
    lead = Lead(
        place_id="p1",
        name="Fresh Brew Cafe",
        industry="coffee shops",
        location="250 University Blvd, Round Rock, TX 78665, USA",
        has_website=False,
        found_date=date(2026, 6, 7),
    )
    round_rock_all = Target(area="Round Rock, TX", radius="5km", industries=[])
    austin_all = Target(area="Austin, TX", radius="5km", industries=[])

    assert _matches_target(lead, round_rock_all)
    assert not _matches_target(lead, austin_all)


def test_parse_photo_count_response():
    count, reason = _parse_photo_count_response("COUNT: 12\nREASON: visible menu and cafe photos")

    assert count == 12
    assert reason == "visible menu and cafe photos"


def test_website_intelligence_only_processes_prioritized_active_leads(tmp_path, monkeypatch):
    store = LeadStore(tmp_path / "leads.jsonl")
    for place_id, name in [("p1", "Ready Cafe"), ("p2", "Found Cafe"), ("p3", "Archived Cafe")]:
        store.create(
            LeadCreate(
                place_id=place_id,
                name=name,
                industry="coffee shops",
                location="Round Rock, TX",
                has_website=False,
                found_date=date(2026, 6, 7),
                google_maps_url=f"https://maps.example/{place_id}",
            )
        )
    store.apply_prioritization(
        LeadPrioritization(
            place_id="p1",
            photo_rating=3,
            lead_score=50,
            photo_count=15,
            photo_links=["https://listing.example/ready"],
            photo_sources=["google_maps"],
            rating_reason="visible listing photos",
            prioritized_date=date(2026, 6, 8),
        )
    )
    store.apply_prioritization(
        LeadPrioritization(
            place_id="p3",
            photo_rating=4,
            lead_score=65,
            photo_count=30,
            photo_links=["https://listing.example/archived"],
            photo_sources=["google_maps"],
            rating_reason="many listing photos",
            prioritized_date=date(2026, 6, 8),
        )
    )
    store.set_status("p3", LeadStatus.ARCHIVED)

    scraped_urls = []
    monkeypatch.setattr(website_intelligence.firecrawl, "scrape", lambda url: scraped_urls.append(url) or "photos")
    monkeypatch.setattr(
        website_intelligence.llm,
        "generate",
        lambda *args, **kwargs: (
            "BRIEF: Build a simple cafe site.\n"
            "ANGLE: Turn map viewers into visitors.\n"
            "PAGES: Home, Menu, Gallery, Contact\n"
            "CONTENT: Gather menu and hours.\n"
            "VISUAL: Use warm drink photos."
        ),
    )

    result = website_intelligence.run(
        store,
        Target(area="Round Rock, TX", radius="5km", industries=["coffee shops"]),
    )

    leads = store.load()
    assert result.processed == 1
    assert result.created_or_updated == 1
    assert scraped_urls == ["https://listing.example/ready", "https://maps.example/p1"]
    assert leads["p1"].site_brief == "Build a simple cafe site."
    assert leads["p2"].site_brief is None
    assert leads["p3"].site_brief is None
