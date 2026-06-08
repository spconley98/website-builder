"""Tests for the riskiest contract in the scaffold (per three-brain/Codex
adversarial review): dedup, fact/judgment separation, and status monotonicity.
If these break, agents built on top will silently corrupt the lead database.
"""
from __future__ import annotations

from datetime import date

import pytest

from leadpipe.models import Lead, LeadCreate, LeadPrioritization, LeadStatus, LeadWebsiteIntelligence
from leadpipe.store import LeadStore, normalize_profile


def _create(place_id="p1", name="Joe's Pizza", has_website=False) -> LeadCreate:
    return LeadCreate(
        place_id=place_id,
        name=name,
        industry="restaurants",
        location="Austin, TX",
        has_website=has_website,
        found_date=date(2026, 1, 1),
    )


def _prioritization(place_id="p1", rating=3, count=12) -> LeadPrioritization:
    return LeadPrioritization(
        place_id=place_id,
        photo_rating=rating,
        photo_count=count,
        photo_links=["https://yelp.com/biz/joes-pizza"],
        photo_sources=["yelp"],
        rating_reason="found a dozen food photos",
        prioritized_date=date(2026, 1, 2),
    )


def _website_intelligence(place_id="p1") -> LeadWebsiteIntelligence:
    return LeadWebsiteIntelligence(
        place_id=place_id,
        site_brief="A compact restaurant site with menu, photos, and contact info.",
        selling_angle="Make it easier for hungry nearby customers to choose them.",
        suggested_pages=["Home", "Menu", "Gallery", "Contact"],
        content_notes="Gather current menu, hours, and best dishes.",
        visual_notes="Use warm food photos from the listing.",
        intelligence_sources=["https://yelp.com/biz/joes-pizza"],
        intelligence_date=date(2026, 1, 3),
    )


def test_create_dedupes_by_place_id(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(_create(name="Joe's Pizza"))
    store.create(_create(name="Joe's Pizza & Pasta"))  # re-found, name changed

    leads = store.load()
    assert len(leads) == 1, "same place_id must not create a second record"
    assert leads["p1"].name == "Joe's Pizza & Pasta", "re-running Finder refreshes facts"


def test_create_refuses_leads_with_website():
    store = LeadStore.__new__(LeadStore)  # avoid touching disk for a pure validation check
    with pytest.raises(ValueError, match="has_website=True"):
        store.create(_create(has_website=True))


def test_prioritization_cannot_overwrite_acquisition_facts(tmp_path):
    """The core Codex finding: enrichment must never clobber Places-acquired facts."""
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(_create(name="Joe's Pizza", place_id="p1"))
    store.apply_prioritization(_prioritization(place_id="p1"))

    lead = store.load()["p1"]
    assert lead.name == "Joe's Pizza"
    assert lead.industry == "restaurants"
    assert lead.location == "Austin, TX"
    assert lead.has_website is False
    assert lead.photo_rating == 3
    assert lead.photo_count == 12


def test_prioritization_advances_status_but_never_regresses(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(_create(place_id="p1"))
    assert store.load()["p1"].status == LeadStatus.FOUND

    store.apply_prioritization(_prioritization(place_id="p1"))
    assert store.load()["p1"].status == LeadStatus.PRIORITIZED

    # mark it further along manually...
    store.set_status("p1", LeadStatus.SOLD)
    assert store.load()["p1"].status == LeadStatus.SOLD

    # ...then re-prioritizing (e.g. a re-run) must NOT drag it back to "prioritized"
    store.apply_prioritization(_prioritization(place_id="p1", rating=5, count=40))
    lead = store.load()["p1"]
    assert lead.status == LeadStatus.SOLD, "status must be monotonic — never regress"
    assert lead.photo_rating == 5, "judgment fields still update on re-run"


def test_set_status_refuses_to_move_backwards(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(_create(place_id="p1"))
    store.set_status("p1", LeadStatus.CONTACTED)

    with pytest.raises(ValueError, match="backwards"):
        store.set_status("p1", LeadStatus.FOUND)


def test_apply_prioritization_requires_existing_lead(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    with pytest.raises(KeyError):
        store.apply_prioritization(_prioritization(place_id="ghost"))


def test_website_intelligence_cannot_overwrite_facts_or_status(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    store.create(_create(name="Joe's Pizza", place_id="p1"))
    store.apply_prioritization(_prioritization(place_id="p1"))

    before = store.load()["p1"]
    store.apply_website_intelligence(_website_intelligence(place_id="p1"))

    lead = store.load()["p1"]
    assert lead.name == before.name
    assert lead.industry == before.industry
    assert lead.location == before.location
    assert lead.has_website is False
    assert lead.status == LeadStatus.PRIORITIZED
    assert lead.photo_rating == 3
    assert lead.site_brief.startswith("A compact restaurant site")


def test_apply_website_intelligence_requires_existing_lead(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    with pytest.raises(KeyError):
        store.apply_website_intelligence(_website_intelligence(place_id="ghost"))


def test_corrupt_line_raises_with_location(tmp_path):
    path = tmp_path / "leads.jsonl"
    path.write_text("not json\n", encoding="utf-8")
    store = LeadStore(path)
    with pytest.raises(ValueError, match=r"leads\.jsonl:1: corrupt"):
        store.load()


def test_save_is_atomic_and_survives_reload(tmp_path):
    store = LeadStore(tmp_path / "leads.jsonl")
    for i in range(5):
        store.create(_create(place_id=f"p{i}", name=f"Biz {i}"))

    reloaded = LeadStore(tmp_path / "leads.jsonl").load()
    assert len(reloaded) == 5
    assert {l.place_id for l in reloaded.values()} == {f"p{i}" for i in range(5)}


def test_profiles_are_limited_to_known_owners():
    assert normalize_profile("Sean") == "sean"
    assert normalize_profile(" matt ") == "matt"

    with pytest.raises(ValueError, match="unknown profile"):
        normalize_profile("shared")
