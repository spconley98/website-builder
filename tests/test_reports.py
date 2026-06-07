"""Tests for profile-owned and shared Obsidian reports."""
from __future__ import annotations

from datetime import date

from leadpipe.models import Lead, LeadStatus
from leadpipe.reports import render_shared_all, render_shared_prioritized


def _lead(
    place_id: str,
    *,
    name: str = "Fresh Brew Cafe",
    status: LeadStatus = LeadStatus.FOUND,
    rating: int | None = None,
) -> Lead:
    return Lead(
        place_id=place_id,
        name=name,
        industry="coffee shops",
        location="250 University Blvd, Round Rock, TX 78665, USA",
        has_website=False,
        found_date=date(2026, 6, 7),
        status=status,
        photo_rating=rating,
        photo_count=1 if rating is not None else None,
        photo_links=["https://maps.google.com/fresh"] if rating is not None else [],
        photo_sources=["google_maps"] if rating is not None else [],
        rating_reason="one visible listing image" if rating is not None else None,
    )


def test_shared_report_dedupes_by_place_id_and_shows_owners():
    sean = _lead("p1", status=LeadStatus.PRIORITIZED, rating=1)
    matt = _lead("p1", status=LeadStatus.FOUND)

    rendered = render_shared_all({"sean": [sean], "matt": [matt]})

    assert rendered.count("Fresh Brew Cafe") == 1
    assert "Matt, Sean" in rendered


def test_shared_prioritized_hides_archived_leads():
    active = _lead("p1", status=LeadStatus.PRIORITIZED, rating=1)
    archived = _lead("p2", name="Old Cafe", status=LeadStatus.ARCHIVED, rating=5)

    rendered = render_shared_prioritized({"sean": [active, archived]})

    assert "Fresh Brew Cafe" in rendered
    assert "Old Cafe" not in rendered
