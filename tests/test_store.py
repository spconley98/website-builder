"""Tests for the riskiest contract in the scaffold (per three-brain/Codex
adversarial review): dedup, fact/judgment separation, and status monotonicity.
If these break, agents built on top will silently corrupt the lead database.
"""
from __future__ import annotations

from datetime import date

import pytest

from leadpipe.models import Lead, LeadCreate, LeadPrioritization, LeadStatus
from leadpipe.store import LeadStore


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
