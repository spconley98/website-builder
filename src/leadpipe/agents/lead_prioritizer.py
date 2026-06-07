"""Lead Prioritizer — rates leads by how much photo material exists online
(ARCHITECTURE.md §3). More existing photos = faster/easier site to build.

Division of labor: Firecrawl fetches the Yelp/Google listing pages (facts —
what's actually on the page); the LLM reasons over that scraped content to
estimate a photo count and write a one-line justification. The numeric
1-5 rating itself is a deterministic threshold function (`rate_from_count`)
— NOT an LLM guess — so re-runs are stable and the thresholds are tunable
in one place (Codex review: "thresholds, tune later").

Degradation (important — Sean's Firecrawl account is out of credits today):
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
from ..config import Target
from ..models import LeadPrioritization
from ..sources import firecrawl
from ..store import LeadStore
from .base import AgentResult

NAME = "lead_prioritizer"

_COUNT_SYSTEM = (
    "You are reviewing scraped business-listing page content to estimate how "
    "many distinct photos of the business's actual work/products are shown or "
    "referenced. Respond in EXACTLY this format, nothing else:\n"
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
    response = llm.generate(
        f"Page content (truncated):\n{scraped_markdown[:6000]}\n\nEstimate:",
        system=_COUNT_SYSTEM,
        temperature=0.0,
    )
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


def run(store: LeadStore, target: Target) -> AgentResult:
    processed = created_or_updated = skipped = 0
    errors: list[str] = []

    # Prioritizer works the existing FOUND queue — it doesn't search Places
    # again. `target` scopes WHICH found leads to work (by area/industry),
    # consistent with how `find` is invoked.
    candidates = [
        l
        for l in store.by_status("found")
        if l.location.startswith(target.area.split(",")[0]) and l.industry in target.industries
        or not target.industries  # empty industries list = "all in this area"
    ]

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
            # Expected degradation path (e.g. Firecrawl out of credits) — skip,
            # don't fabricate a rating. Re-running later will retry these.
            skipped += 1
            errors.append(f"{lead.place_id} ({lead.name!r}): {e}")
        except Exception as e:
            skipped += 1
            errors.append(f"{lead.place_id} ({lead.name!r}): unexpected error — {e}")

    return AgentResult(NAME, processed, created_or_updated, skipped, errors)
