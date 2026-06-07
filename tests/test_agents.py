"""Tests for the agent contract and the deterministic rating function.

The rating thresholds are explicitly "tune later" (ARCHITECTURE.md) — this
test pins the CURRENT behavior so a future tuning change is a deliberate,
visible diff here, not a silent drift.
"""
from __future__ import annotations

from datetime import date

from leadpipe.agents.base import AgentResult
from leadpipe.agents.lead_prioritizer import _matches_target, _parse_photo_count_response, rate_from_count
from leadpipe.config import load_settings
from leadpipe.config import Target
from leadpipe.models import Lead


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
