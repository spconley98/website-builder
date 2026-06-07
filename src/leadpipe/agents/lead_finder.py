"""Lead Finder — finds local businesses with no website (ARCHITECTURE.md §3).

Division of labor (the architecture's central rule): Google Places supplies
the FACT (does this business have a website? — sources/google_places.py). The
LLM never decides that. What the LLM DOES do here: normalize/clean the industry
label Places returns into the canonical category we searched for — Places
sometimes returns noisy categories ("Italian restaurant", "Pizza place") when
we searched "restaurants", and a clean, consistent label makes the store
groupable and the reports readable.

If the LLM is unavailable, we degrade gracefully: fall back to the raw search
industry rather than failing the whole lead.
"""
from __future__ import annotations

from datetime import date

from .. import llm
from ..config import Target
from ..models import LeadCreate
from ..sources import google_places
from ..store import LeadStore
from .base import AgentResult

NAME = "lead_finder"

_CLASSIFY_SYSTEM = (
    "You normalize business categories for a lead-generation database. "
    "Given a business name and a raw category, respond with ONE short, clean "
    "industry label (2-3 words max, lowercase, no punctuation) that fits the "
    "search category provided. If unsure, just return the search category "
    "unchanged. Respond with the label ONLY — no explanation."
)


def _normalize_industry(name: str, search_industry: str) -> str:
    """LLM reasoning step — degrades to the raw search term on any LLM failure."""
    try:
        label = llm.generate(
            f"Business: {name!r}\nSearch category: {search_industry!r}\n"
            f"Clean industry label:",
            system=_CLASSIFY_SYSTEM,
            temperature=0.0,
        )
        return label.strip().strip('"').lower() or search_industry
    except llm.LLMError:
        return search_industry


def run(store: LeadStore, target: Target, *, limit: int = google_places.DEFAULT_RESULT_LIMIT) -> AgentResult:
    processed = created_or_updated = skipped = 0
    errors: list[str] = []

    for industry in target.industries:
        try:
            candidates = google_places.find_leads_without_website(target.area, industry, limit=limit)
        except google_places.PlacesError as e:
            errors.append(f"{target.area}/{industry}: {e}")
            continue

        for c in candidates:
            processed += 1
            try:
                clean_industry = _normalize_industry(c["name"], industry)
                lead = LeadCreate(
                    place_id=c["place_id"],
                    name=c["name"],
                    industry=clean_industry,
                    location=c["location"],
                    has_website=c["has_website"],
                    found_date=date.today(),
                    google_maps_url=c.get("google_maps_url"),
                )
                store.create(lead)
                created_or_updated += 1
            except Exception as e:  # one bad record must not sink the run
                skipped += 1
                errors.append(f"{c.get('place_id', '?')} ({c.get('name', '?')!r}): {e}")

    return AgentResult(NAME, processed, created_or_updated, skipped, errors)
