"""Tests for Google Places acquisition facts used by lead scoring."""
from __future__ import annotations

from leadpipe.sources import google_places


def test_find_leads_adds_scoring_facts(monkeypatch):
    monkeypatch.setattr(
        google_places,
        "search_businesses",
        lambda area, industry, limit=20: [
            {
                "place_id": "p1",
                "name": "Fresh Brew Cafe",
                "location": "Round Rock, TX",
                "google_maps_url": "https://maps.example/search",
            }
        ],
    )
    monkeypatch.setattr(
        google_places,
        "fetch_place_details",
        lambda place_id: {
            "id": place_id,
            "googleMapsUri": "https://maps.example/details",
            "nationalPhoneNumber": "(512) 555-0100",
            "regularOpeningHours": {"weekdayDescriptions": ["Monday: 8 AM-5 PM"]},
            "reviews": [
                {"publishTime": "2026-06-01T12:00:00Z"},
                {"publishTime": "2024-01-01T12:00:00Z"},
            ],
        },
    )

    leads = google_places.find_leads_without_website("Round Rock, TX", "coffee shops")

    assert len(leads) == 1
    assert leads[0]["google_maps_url"] == "https://maps.example/details"
    assert leads[0]["phone_present"] is True
    assert leads[0]["hours_present"] is True
    assert leads[0]["recent_review_count"] == 1
    assert leads[0]["staleness_flags"] == []


def test_find_leads_staleness_flags_are_soft_signals(monkeypatch):
    monkeypatch.setattr(
        google_places,
        "search_businesses",
        lambda area, industry, limit=20: [{"place_id": "p1", "name": "Acme Plumbing", "location": area}],
    )
    monkeypatch.setattr(google_places, "fetch_place_details", lambda place_id: {"id": place_id})

    leads = google_places.find_leads_without_website("Austin, TX", "plumbing")

    assert len(leads) == 1
    assert leads[0]["staleness_flags"] == ["missing_phone", "missing_hours", "no_recent_reviews"]
