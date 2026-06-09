"""Tests for profile-owned and shared Obsidian reports."""
from __future__ import annotations

from datetime import date

from leadpipe.models import Lead, LeadStatus
from leadpipe.reports import (
    render_shared_all,
    render_shared_prioritized,
    render_shared_website_briefs,
    render_website_briefs,
)


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


def _briefed_lead(place_id: str, *, name: str = "Fresh Brew Cafe") -> Lead:
    lead = _lead(place_id, name=name, status=LeadStatus.PRIORITIZED, rating=3)
    return lead.model_copy(
        update={
            "site_brief": "A compact cafe site with menu, gallery, and visit info.",
            "selling_angle": "Convert map traffic into in-store visits.",
            "suggested_pages": ["Home", "Menu", "Gallery", "Contact"],
            "content_notes": "Gather current hours and menu.",
            "visual_notes": "Use bright coffee and pastry photos.",
            "intelligence_sources": ["https://maps.google.com/fresh"],
            "intelligence_date": date(2026, 6, 8),
        }
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


def test_shared_prioritized_escapes_pipe_characters_in_table_cells():
    lead = _lead(
        "p1",
        name="Mecanico a Domicilio | Mobile Mechanic",
        status=LeadStatus.PRIORITIZED,
        rating=1,
    )

    rendered = render_shared_prioritized({"matt": [lead]})

    assert "Mecanico a Domicilio \\| Mobile Mechanic" in rendered
    assert "Mecanico a Domicilio | Mobile Mechanic" not in rendered


def test_profile_website_briefs_render_empty_and_briefed_states():
    empty = render_website_briefs([])
    rendered = render_website_briefs([_briefed_lead("p1")])

    assert "No website briefs yet" in empty
    assert "A compact cafe site" in rendered
    assert "Home, Menu, Gallery, Contact" in rendered


def test_shared_website_briefs_dedupes_and_shows_owners():
    sean = _briefed_lead("p1")
    matt = _lead("p1", status=LeadStatus.PRIORITIZED, rating=1)

    rendered = render_shared_website_briefs({"sean": [sean], "matt": [matt]})

    assert rendered.count("Fresh Brew Cafe") == 1
    assert "Matt, Sean" in rendered
    assert "Convert map traffic" in rendered
