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
from leadpipe.agents.scraped_content import compact_scraped_content
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


def test_compact_scraped_content_preserves_head_middle_and_tail():
    markdown = (
        "START useful listing identity\n"
        + ("filler\n" * 600)
        + "Photo gallery shows finished projects\n"
        + ("more filler\n" * 600)
        + "TAIL contact and hours"
    )

    compacted = compact_scraped_content(markdown, max_chars=900)

    assert len(compacted) <= 900
    assert "START useful listing identity" in compacted
    assert "Photo gallery shows finished projects" in compacted
    assert "TAIL contact and hours" in compacted
    assert "compacted for local LLM timeout guard" in compacted


def test_prioritizer_prompt_uses_compacted_scraped_content(monkeypatch):
    from leadpipe.agents import lead_prioritizer

    huge_markdown = (
        "BUSINESS HEADER\n"
        + ("plain filler\n" * 700)
        + "Photo gallery mentions service images\n"
        + ("extra filler\n" * 700)
        + "BOTTOM hours and contact"
    )
    prompts = []

    def fake_generate(prompt, **kwargs):
        prompts.append(prompt)
        return "COUNT: 4\nREASON: visible project photos"

    monkeypatch.setattr(lead_prioritizer.llm, "generate", fake_generate)

    count, reason = lead_prioritizer._estimate_photo_count(huge_markdown)

    assert count == 4
    assert reason == "visible project photos"
    assert len(prompts[0]) < len(huge_markdown)
    assert "BUSINESS HEADER" in prompts[0]
    assert "Photo gallery mentions service images" in prompts[0]
    assert "BOTTOM hours and contact" in prompts[0]


def test_website_intelligence_prompt_uses_compacted_scraped_content():
    lead = Lead(
        place_id="p1",
        name="Ready Cafe",
        industry="coffee shops",
        location="Round Rock, TX",
        has_website=False,
        found_date=date(2026, 6, 7),
        photo_rating=3,
        lead_score=50,
        photo_count=15,
        rating_reason="visible listing photos",
    )
    huge_markdown = (
        "TOP listing summary\n"
        + ("plain filler\n" * 900)
        + "Gallery has interior photos and menu images\n"
        + ("extra filler\n" * 900)
        + "BOTTOM phone and hours"
    )

    prompt = website_intelligence._build_prompt(lead, huge_markdown)

    assert len(prompt) < len(huge_markdown)
    assert "TOP listing summary" in prompt
    assert "Gallery has interior photos and menu images" in prompt
    assert "BOTTOM phone and hours" in prompt


def test_website_intelligence_parser_accepts_markdown_labels():
    parsed = website_intelligence._parse_response(
        "**BRIEF:** Build a service website.\n"
        "**ANGLE:** Convert listing views.\n"
        "**PAGES:** Home, Services, Contact\n"
        "**CONTENT:** Verify hours.\n"
        "**VISUAL:** Use listing photos."
    )

    assert parsed["site_brief"] == "Build a service website."
    assert parsed["suggested_pages"] == ["Home", "Services", "Contact"]


def test_website_intelligence_falls_back_after_unparseable_repair(monkeypatch):
    lead = Lead(
        place_id="p1",
        name="Ready Cafe",
        industry="coffee shops",
        location="Round Rock, TX",
        has_website=False,
        found_date=date(2026, 6, 7),
    )
    monkeypatch.setattr(website_intelligence.llm, "generate", lambda *args, **kwargs: "not structured")

    parsed = website_intelligence._generate_intelligence(lead, "listing content")

    assert parsed["site_brief"].startswith("A simple credibility website for Ready Cafe")
    assert parsed["suggested_pages"] == ["Home", "Services", "Gallery", "Contact"]


def test_estimate_photo_count_escalates_to_deep_model_on_failure(monkeypatch):
    """A1 tiering: when the fast model fails (timeout/garbage), the retry must use the
    deep model + deep timeout — this is what recovers the previously-stuck lead."""
    from leadpipe.agents import lead_prioritizer

    calls = []

    def fake_generate(prompt, **kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise lead_prioritizer.llm.LLMError("fast model timed out after 60.0s")
        return "COUNT: 8\nREASON: visible work photos"

    monkeypatch.setattr(lead_prioritizer.llm, "generate", fake_generate)

    count, reason = lead_prioritizer._estimate_photo_count("some scraped markdown")
    settings = load_settings()

    assert count == 8
    assert len(calls) == 2
    assert calls[0].get("model") in (None, settings.llm_model)  # fast/default first
    assert calls[1]["model"] == settings.llm_model_deep
    assert calls[1]["timeout"] == settings.llm_deep_timeout


def test_website_intelligence_escalates_to_deep_model_before_fallback(monkeypatch):
    """A1 tiering for Agent 3: fast failure escalates to the deep model, which can then
    succeed instead of dropping straight to the conservative fallback."""
    lead = Lead(
        place_id="p1",
        name="Ready Cafe",
        industry="coffee shops",
        location="Round Rock, TX",
        has_website=False,
        found_date=date(2026, 6, 7),
    )
    calls = []

    def fake_generate(prompt, **kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise website_intelligence.llm.LLMError("fast model timed out")
        return (
            "BRIEF: Build a service site.\nANGLE: Convert listing views.\n"
            "PAGES: Home, Contact\nCONTENT: Gather reviews.\nVISUAL: Use listing photos."
        )

    monkeypatch.setattr(website_intelligence.llm, "generate", fake_generate)

    parsed = website_intelligence._generate_intelligence(lead, "listing content")
    settings = load_settings()

    assert parsed["site_brief"] == "Build a service site."
    assert len(calls) == 2
    assert calls[1]["model"] == settings.llm_model_deep
    assert calls[1]["timeout"] == settings.llm_deep_timeout


def test_intelligence_system_prompt_carries_leverage_frame():
    """C1: the brief's selling voice must be ROI/leverage-anchored, not generic."""
    system = website_intelligence._INTELLIGENCE_SYSTEM.lower()
    assert "listing view" in system
    assert "roi" in system or "leverage" in system
    fallback = website_intelligence._fallback_intelligence(
        Lead(
            place_id="p1",
            name="Ready Cafe",
            industry="coffee shops",
            location="Round Rock, TX",
            has_website=False,
            found_date=date(2026, 6, 7),
        )
    )
    assert "leak" in fallback["selling_angle"].lower()


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


def test_website_intelligence_skips_existing_briefs(tmp_path, monkeypatch):
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(
        LeadCreate(
            place_id="p1",
            name="Ready Cafe",
            industry="coffee shops",
            location="Round Rock, TX",
            has_website=False,
            found_date=date(2026, 6, 7),
            google_maps_url="https://maps.example/p1",
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
    store.apply_website_intelligence(
        website_intelligence.LeadWebsiteIntelligence(
            place_id="p1",
            site_brief="Existing brief.",
            selling_angle="Existing angle.",
            suggested_pages=["Home"],
            content_notes="Existing notes.",
            visual_notes="Existing visual notes.",
            intelligence_sources=["https://listing.example/ready"],
            intelligence_date=date(2026, 6, 9),
        )
    )
    monkeypatch.setattr(website_intelligence.firecrawl, "scrape", lambda url: (_ for _ in ()).throw(AssertionError))

    result = website_intelligence.run(
        store,
        Target(area="Round Rock, TX", radius="5km", industries=["coffee shops"]),
    )

    assert result.processed == 0
    assert store.load()["p1"].site_brief == "Existing brief."
