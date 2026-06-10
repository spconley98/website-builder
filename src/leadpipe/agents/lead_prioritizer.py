"""Lead Prioritizer — rates leads by how much photo material exists online
(ARCHITECTURE.md §3). More existing photos = faster/easier site to build.

Division of labor: Firecrawl fetches the Yelp/Google listing pages (facts —
what's actually on the page); the LLM reasons over that scraped content to
estimate a photo count and write a one-line justification. The numeric
1-5 rating itself is a deterministic threshold function (`rate_from_count`)
— NOT an LLM guess — so re-runs are stable and the thresholds are tunable
in one place (Codex review: "thresholds, tune later").

Degradation:
  - FirecrawlError -> skip this lead, record the error. We do NOT write a
    photo_rating of 0 in this case: 0 means "reviewed, nothing usable found",
    which is a different fact than "couldn't review it". Skipping preserves
    that distinction so a later re-run (once credits are restored) still picks
    these up as un-prioritized.
  - LLMError -> same: skip and record. No judgment without the reasoning step.
"""
from __future__ import annotations

from datetime import date

from .. import llm
from ..config import Target, load_settings
from ..models import LeadPrioritization
from ..sources import firecrawl
from ..store import LeadStore
from .base import AgentResult

NAME = "lead_prioritizer"

_COUNT_SYSTEM = (
    "You are a strict data-extraction function. You are NOT answering a user "
    "question about directions, prices, travel, or the business. Review scraped "
    "business-listing page content and estimate how many distinct photos of the "
    "business's actual work/products are shown or referenced. If the page content "
    "does not contain clear photo evidence, use COUNT: 0. Respond in EXACTLY this "
    "format, nothing else:\n"
    "COUNT: <integer>\n"
    "REASON: <one short sentence>"
)


def rate_from_count(photo_count: int) -> int:
    """Deterministic 1-5 (or 0) rating from a photo count. Pure + tunable —
    the only place these thresholds live (Codex: 'tune later')."""
    if photo_count <= 0:
        return 0
    if photo_count < 5:
        return 1
    if photo_count < 15:
        return 2
    if photo_count < 30:
        return 3
    if photo_count < 60:
        return 4
    return 5


def _estimate_photo_count(scraped_markdown: str) -> tuple[int, str]:
    """LLM reasoning step over scraped page content. Raises LLMError on failure
    or on an unparseable response — caller decides how to degrade."""
    prompt = (
        "Return only the two-line photo estimate for this scraped listing content.\n\n"
        f"SCRAPED_CONTENT:\n{scraped_markdown[:6000]}\n\n"
        "Your response must be exactly:\n"
        "COUNT: <integer>\n"
        "REASON: <one short sentence>"
    )
    response = llm.generate(
        prompt,
        system=_COUNT_SYSTEM,
        temperature=0.0,
    )
    try:
        return _parse_photo_count_response(response)
    except llm.LLMError:
        repair = llm.generate(
            "Your previous response did not follow the required format.\n\n"
            f"Previous response:\n{response}\n\n"
            "Re-read the scraped listing content below and output ONLY:\n"
            "COUNT: <integer>\n"
            "REASON: <one short sentence>\n\n"
            f"SCRAPED_CONTENT:\n{scraped_markdown[:6000]}",
            system=_COUNT_SYSTEM,
            temperature=0.0,
        )
        return _parse_photo_count_response(repair)


def _parse_photo_count_response(response: str) -> tuple[int, str]:
    """Parse the strict two-line LLM output for photo-count estimates."""
    count = reason = None
    for line in response.splitlines():
        if line.upper().startswith("COUNT:"):
            count = int("".join(ch for ch in line.split(":", 1)[1] if ch.isdigit()) or "0")
        elif line.upper().startswith("REASON:"):
            reason = line.split(":", 1)[1].strip()
    if count is None:
        raise llm.LLMError(f"could not parse photo-count estimate from response: {response!r}")
    return count, (reason or "no reason given")


def _gather_listing_urls(lead) -> list[tuple[str, str]]:
    """Returns [(source_label, url), ...] to enrich from. Prefers URLs Lead
    Finder already captured; falls back to a Firecrawl search by name+location."""
    urls: list[tuple[str, str]] = []
    if lead.google_maps_url:
        urls.append(("google_maps", lead.google_maps_url))
    if lead.yelp_url:
        urls.append(("yelp", lead.yelp_url))
    if not urls:
        for hit in firecrawl.search(f"{lead.name} {lead.location} yelp", limit=2):
            url = hit.get("url")
            if url:
                urls.append(("yelp_search", url))
    return urls


def _matches_target(lead, target: Target) -> bool:
    """Scope found leads to the requested target. Google Places addresses start
    with street numbers, so match the city/area anywhere in the formatted address."""
    area_name = target.area.split(",", 1)[0].strip().lower()
    location = lead.location.lower()
    in_area = area_name in location if area_name else True
    in_industry = not target.industries or lead.industry in target.industries
    return in_area and in_industry


def _credit_pause_error(settings) -> str | None:
    """None means proceed (or "can't tell, don't block"). A string is the
    reason to pause — Firecrawl credit usage is account-wide and shared
    across Sean/Matt, so dropping below the threshold pauses everyone's
    Firecrawl-backed prioritization until credits are topped up."""
    usage = firecrawl.get_credit_usage()
    if not usage:
        return None
    remaining = usage.get("remainingCredits")
    plan = usage.get("planCredits")
    if not remaining or not plan:
        return None
    pct_remaining = remaining / plan * 100
    if pct_remaining < settings.firecrawl_pause_credits_pct:
        return (
            f"Firecrawl credits dropped below {settings.firecrawl_pause_credits_pct}% "
            f"({pct_remaining:.1f}% remaining) — pausing prioritization until topped up"
        )
    return None


def run(store: LeadStore, target: Target) -> AgentResult:
    processed = created_or_updated = skipped = 0
    errors: list[str] = []

    settings = load_settings()
    credit_error = _credit_pause_error(settings)
    if credit_error:
        return AgentResult(NAME, processed, created_or_updated, skipped, [credit_error])

    # Prioritizer works the existing FOUND queue — it doesn't search Places
    # again. `target` scopes WHICH found leads to work (by area/industry),
    # consistent with how `find` is invoked.
    candidates = [l for l in store.by_status("found") if _matches_target(l, target)]

    for lead in candidates:
        processed += 1
        try:
            urls = _gather_listing_urls(lead)
            if not urls:
                skipped += 1
                errors.append(f"{lead.place_id} ({lead.name!r}): no listing URL to enrich from")
                continue

            total_count = 0
            sources: list[str] = []
            links: list[str] = []
            reasons: list[str] = []
            for label, url in urls:
                markdown = firecrawl.scrape(url)
                count, reason = _estimate_photo_count(markdown)
                total_count += count
                sources.append(label)
                links.append(url)
                reasons.append(f"{label}: {reason} (~{count})")

            update = LeadPrioritization(
                place_id=lead.place_id,
                photo_rating=rate_from_count(total_count),
                photo_count=total_count,
                photo_links=links,
                photo_sources=sources,
                rating_reason="; ".join(reasons),
                prioritized_date=date.today(),
            )
            store.apply_prioritization(update)
            created_or_updated += 1

        except (firecrawl.FirecrawlError, llm.LLMError) as e:
            # Expected degradation path (e.g. Firecrawl/API issues) — skip,
            # don't fabricate a rating. Re-running later will retry these.
            skipped += 1
            errors.append(f"{lead.place_id} ({lead.name!r}): {e}")
        except Exception as e:
            skipped += 1
            errors.append(f"{lead.place_id} ({lead.name!r}): unexpected error — {e}")

    return AgentResult(NAME, processed, created_or_updated, skipped, errors)
