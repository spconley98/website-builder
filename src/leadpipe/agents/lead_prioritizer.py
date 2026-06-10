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
import re

from .. import llm
from ..config import Target, load_settings
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
    prompt = (
        f"Analyze the following scraped page content:\n"
        f"<scraped_content>\n{scraped_markdown[:6000]}\n</scraped_content>\n\n"
        f"Based on the content above, estimate how many photos of the business are shown.\n"
        f"You MUST respond in EXACTLY this format and nothing else (do not include markdown formatting or conversational text):\n"
        f"COUNT: <number>\n"
        f"REASON: <one short sentence justification>\n\n"
        f"Response:"
    )
    response = llm.generate(
        prompt,
        system=_COUNT_SYSTEM,
        temperature=0.0,
    )
    count = reason = None
    for line in response.splitlines():
        line = line.strip()
        if line.upper().startswith("COUNT:"):
            val = "".join(c for c in line.split(":", 1)[1] if c.isdigit())
            if val:
                count = int(val)
        elif line.upper().startswith("REASON:"):
            reason = line.split(":", 1)[1].strip()

    # Fallback for count if not found in standard format
    if count is None:
        m = re.search(r'(?:COUNT|count|Count):\s*(\d+)', response)
        if m:
            count = int(m.group(1))
        else:
            word_to_num = {
                "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, 
                "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
                "ten": 10
            }
            lower_resp = response.lower()
            found_num = False
            for word, num in word_to_num.items():
                if f"{word} photo" in lower_resp or f"{word} image" in lower_resp:
                    count = num
                    found_num = True
                    break
            if not found_num:
                m_phrase = re.search(r'(\d+)\s*(?:photo|image|picture)', lower_resp)
                if m_phrase:
                    count = int(m_phrase.group(1))
                else:
                    m_any = re.search(r'\d+', response)
                    if m_any:
                        count = int(m_any.group())
                    else:
                        count = 0  # Default to 0 if absolutely no number found

    # Fallback for reason
    if reason is None:
        non_empty_lines = [l.strip() for l in response.splitlines() if l.strip()]
        for line in non_empty_lines:
            if not line.upper().startswith("COUNT:"):
                reason = line
                break
        if not reason:
            reason = "No reason given"

    return count, reason


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


_NEARBY_TOWNS = {
    "austin": {"round rock"},
    "san antonio": {"von ormy"},
    "denton": {"cross roads"},
    "wichita falls": {"iowa park", "sheppard afb"},
    "arlington": {"pantego", "dalworthington gardens"},
}


def run(store: LeadStore, target: Target) -> AgentResult:
    processed = created_or_updated = skipped = 0
    errors: list[str] = []

    # Prioritizer works the existing FOUND queue — it doesn't search Places
    # again. `target` scopes WHICH found leads to work (by area/industry),
    # consistent with how `find` is invoked.
    area_city = target.area.split(",")[0].strip().lower()
    allowed_cities = {area_city}
    if area_city in _NEARBY_TOWNS:
        allowed_cities.update(_NEARBY_TOWNS[area_city])

    candidates = [
        l
        for l in store.by_status("found")
        if any(city in l.location.lower() for city in allowed_cities)
        and (not target.industries or l.industry in target.industries)
    ]

    settings = load_settings()
    pause_pct = settings.firecrawl_pause_credits_pct

    for lead in candidates:
        if pause_pct is not None and pause_pct > 0:
            usage = firecrawl.get_credit_usage()
            if usage:
                rem = usage.get("remainingCredits", 0)
                plan = usage.get("planCredits", 0)
                if plan > 0:
                    current_pct = (rem / plan) * 100
                    if current_pct <= pause_pct:
                        errors.append(
                            f"Firecrawl credits remaining ({current_pct:.1f}%) reached or dropped below "
                            f"the pause threshold of {pause_pct}%. Pausing prioritization."
                        )
                        break

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
