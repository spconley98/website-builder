"""Google Places API (New) — the FACTS layer.

ARCHITECTURE.md §5: "does this business have a website?" must be a hard fact,
not an LLM guess. This module is the only place that fact comes from. The LLM
never decides has_website — it only reasons about what these calls return.

Uses Places API (New) — Text Search to enumerate candidates in an area, then
Place Details for the `websiteUri` field (the actual signal we filter on).
Docs: https://developers.google.com/maps/documentation/places/web-service/op-overview
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import httpx

from ..config import load_settings

_BASE = "https://places.googleapis.com/v1"
_SEARCH_FIELDS = "places.id,places.displayName,places.formattedAddress,places.googleMapsUri"
_DETAILS_FIELDS = (
    "id,websiteUri,googleMapsUri,nationalPhoneNumber,internationalPhoneNumber,"
    "regularOpeningHours,userRatingCount,reviews"
)

DEFAULT_TIMEOUT = 30.0
DEFAULT_RESULT_LIMIT = 20


class PlacesError(RuntimeError):
    """Raised for any Places-API failure, with enough context to debug it."""


def _client(api_key: str) -> httpx.Client:
    return httpx.Client(
        base_url=_BASE,
        timeout=DEFAULT_TIMEOUT,
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": api_key},
    )


def search_businesses(
    area: str,
    industry: str,
    *,
    api_key: str | None = None,
    limit: int = DEFAULT_RESULT_LIMIT,
) -> list[dict]:
    """Text-search Places for `<industry> in <area>`. Returns raw candidate dicts
    with id/name/address/maps_url — NOT yet filtered by website presence (that
    requires a details call per place, done in `enrich_with_website`)."""
    settings = load_settings()
    key = api_key or settings.google_places_api_key
    if not key:
        raise PlacesError(
            "GOOGLE_PLACES_API_KEY is not set. Copy .env.example to .env and add your key "
            "(see docs/project/ONBOARDING_MATT.md)."
        )

    query = f"{industry} in {area}"
    limit = max(1, min(limit, DEFAULT_RESULT_LIMIT))
    try:
        with _client(key) as client:
            resp = client.post(
                "/places:searchText",
                headers={"X-Goog-FieldMask": _SEARCH_FIELDS},
                json={"textQuery": query, "pageSize": limit},
            )
            resp.raise_for_status()
    except httpx.TimeoutException as e:
        raise PlacesError(f"Places search timed out after {DEFAULT_TIMEOUT}s for {query!r}") from e
    except httpx.HTTPStatusError as e:
        raise PlacesError(
            f"Places search failed for {query!r}: HTTP {e.response.status_code} — {e.response.text}"
        ) from e

    places = resp.json().get("places", [])[:limit]
    return [
        {
            "place_id": p["id"],
            "name": p.get("displayName", {}).get("text", "Unknown"),
            "location": p.get("formattedAddress", area),
            "google_maps_url": p.get("googleMapsUri"),
        }
        for p in places
    ]


def fetch_place_details(place_id: str, *, api_key: str | None = None) -> dict:
    """Place Details lookup — returns deterministic acquisition facts from
    Google. `websiteUri` remains the hard no-website filter; the other signals
    are soft ranking inputs for the Prioritizer."""
    settings = load_settings()
    key = api_key or settings.google_places_api_key
    if not key:
        raise PlacesError("GOOGLE_PLACES_API_KEY is not set.")

    try:
        with _client(key) as client:
            resp = client.get(
                f"/places/{place_id}",
                headers={"X-Goog-FieldMask": _DETAILS_FIELDS},
            )
            resp.raise_for_status()
    except httpx.TimeoutException as e:
        raise PlacesError(f"Places details timed out for {place_id}") from e
    except httpx.HTTPStatusError as e:
        raise PlacesError(
            f"Places details failed for {place_id}: HTTP {e.response.status_code} — {e.response.text}"
        ) from e

    return resp.json()


def fetch_website(place_id: str, *, api_key: str | None = None) -> str | None:
    """Place Details lookup — returns the `websiteUri` if Google has one on file,
    else None. THIS is the deterministic "has website" signal (no LLM involved)."""
    return fetch_place_details(place_id, api_key=api_key).get("websiteUri")


def _recent_review_count(details: dict, *, today: date | None = None, days: int = 180) -> int:
    """Count recent Google review timestamps from the limited review sample
    returned by Places Details. Missing/unparseable review dates count as 0."""
    today = today or date.today()
    cutoff = today - timedelta(days=days)
    count = 0
    for review in details.get("reviews") or []:
        raw = review.get("publishTime")
        if not raw:
            continue
        try:
            published = datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc).date()
        except ValueError:
            continue
        if published >= cutoff:
            count += 1
    return count


def _hours_present(details: dict) -> bool:
    hours = details.get("regularOpeningHours") or {}
    return bool(hours.get("periods") or hours.get("weekdayDescriptions"))


def _staleness_flags(*, phone_present: bool, hours_present: bool, recent_review_count: int) -> list[str]:
    flags: list[str] = []
    if not phone_present:
        flags.append("missing_phone")
    if not hours_present:
        flags.append("missing_hours")
    if recent_review_count <= 0:
        flags.append("no_recent_reviews")
    return flags


def find_leads_without_website(
    area: str,
    industry: str,
    *,
    limit: int = DEFAULT_RESULT_LIMIT,
) -> list[dict]:
    """The full acquisition step Lead Finder calls: search, then check each
    candidate's website field. Returns only candidates with NO website —
    these are the only ones that should ever reach the store.

    Each returned dict has everything `LeadCreate` needs except `industry`
    (the agent knows that — it's the search parameter) and `found_date`.
    """
    candidates = search_businesses(area, industry, limit=limit)
    leads_without_site = []
    for c in candidates:
        details = fetch_place_details(c["place_id"])
        if details.get("websiteUri") is None:
            phone_present = bool(details.get("nationalPhoneNumber") or details.get("internationalPhoneNumber"))
            hours_present = _hours_present(details)
            recent_review_count = _recent_review_count(details)
            leads_without_site.append(
                {
                    **c,
                    "google_maps_url": details.get("googleMapsUri") or c.get("google_maps_url"),
                    "has_website": False,
                    "found_date": date.today(),
                    "phone_present": phone_present,
                    "recent_review_count": recent_review_count,
                    "hours_present": hours_present,
                    "staleness_flags": _staleness_flags(
                        phone_present=phone_present,
                        hours_present=hours_present,
                        recent_review_count=recent_review_count,
                    ),
                }
            )
    return leads_without_site
