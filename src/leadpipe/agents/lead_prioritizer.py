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

import re
from datetime import date

from .. import llm
from ..config import Target, load_settings
from ..models import LeadPrioritization
from ..sources import firecrawl
from ..store import LeadStore
from .base import AgentResult
from .scraped_content import compact_scraped_content

NAME = "lead_prioritizer"
PHOTO_PROMPT_CONTENT_LIMIT = 6000

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


def score_from_signals(
    *,
    photo_count: int,
    phone_present: bool | None,
    recent_review_count: int | None,
    hours_present: bool | None,
    staleness_flags: list[str] | None,
) -> int:
    """Deterministic lead score from buildability + reachability signals.
    Unknown legacy facts are neutral; known stale signals are soft penalties."""
    score = rate_from_count(photo_count) * 15
    if phone_present is True:
        score += 10
    if hours_present is True:
        score += 5
    if recent_review_count is not None:
        score += min(recent_review_count, 5) * 2
    if staleness_flags:
        score -= min(len(staleness_flags) * 5, 20)
    return max(0, min(100, score))


def _estimate_photo_count(scraped_markdown: str) -> tuple[int, str]:
    """LLM reasoning step over scraped page content. Raises LLMError on failure
    or on an unparseable response — caller decides how to degrade.

    Tiered (Nate Herk model tiering): the fast model handles the common case; if it
    times out OR returns an unparseable response, escalate the retry to the deep
    model + longer timeout (config.llm_model_deep / llm_deep_timeout). This recovers
    hard leads that the fast model can't handle in 60s instead of skipping them
    (e.g. the previously-stuck "Spark Electricians")."""
    compacted = compact_scraped_content(scraped_markdown, max_chars=PHOTO_PROMPT_CONTENT_LIMIT)
    prompt = (
        "Return only the two-line photo estimate for this scraped listing content.\n\n"
        f"SCRAPED_CONTENT:\n{compacted}\n\n"
        "Your response must be exactly:\n"
        "COUNT: <integer>\n"
        "REASON: <one short sentence>"
    )
    try:
        response = llm.generate(prompt, system=_COUNT_SYSTEM, temperature=0.0)
        return _parse_photo_count_response(response)
    except llm.LLMError:
        # Escalate the SAME prompt to the deep tier — reusing `prompt` (not a reworded
        # inline copy) keeps the extraction instructions in one place. Note: we escalate
        # on any LLMError; a connection error just fails fast again, which is acceptable.
        settings = load_settings()
        repair = llm.generate(
            prompt,
            system=_COUNT_SYSTEM,
            temperature=0.0,
            model=settings.llm_model_deep,
            timeout=settings.llm_deep_timeout,
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


# Industry-family matching: the Finder LLM-normalizes stored labels
# ("plumbers" search -> "plumbing" / "plumbing services" on the lead), so an
# exact `lead.industry in target.industries` silently ranked ZERO leads for
# `run` / `prioritize --industry X`. Matching is deterministic stem-token
# intersection — no LLM in the scoping path, so re-runs stay stable.
#
# Filler tokens carry business *form* or generic marketing modifiers, not
# trade ("plumbing services" must not match "cleaning services" via
# "services"; "24 hour plumbing" must not match "24 hour locksmith" via
# "hour"). Suffix stripping unifies the trade families actually seen in
# stores: plumbers/plumbing -> plumb, electricians/electrician/electrical
# -> electric, landscaping/landscapers -> landscap. Known accepted
# over-match (Codex-reviewed): same-stem retail/supply labels ("electrical
# supply" under "electricians", "landscaping supplies" under "landscapers")
# — those leads came from that same search, so scoping them in mirrors what
# the search itself returned.
_FILLER_TOKENS = {
    "service", "services", "supply", "supplies", "contractor", "contractors",
    "shop", "shops", "store", "stores", "company", "companies", "co", "llc", "inc",
    # generic modifiers (Codex finding: any-token intersection over-matched)
    "hour", "hours", "emergency", "commercial", "residential", "industrial",
    "local", "mobile", "professional", "certified", "licensed", "affordable",
}
# Longest-first so "ers" wins over "er"/"s"; a stripped stem must keep >= 4
# chars ("metal" never becomes "met").
_STEM_SUFFIXES = ("ians", "ian", "ing", "ers", "ors", "er", "or", "al", "es", "s")


def _stem(token: str) -> str:
    for suffix in _STEM_SUFFIXES:
        if token.endswith(suffix) and len(token) - len(suffix) >= 4:
            token = token[: -len(suffix)]
            break
    # Terminal-e normalization (Codex finding): "landscape" must meet
    # "landscaping" at "landscap", "tree" must meet "trees" at "tre",
    # "appliance" must meet "appliances" at "applianc".
    if token.endswith("e") and len(token) >= 5:
        token = token[:-1]
    return token


def _industry_stems(label: str) -> set[str]:
    """Non-filler trade stems for a label. Drops 1-char fragments (the "s" in
    "men's" bridged EVERY possessive pair — Codex finding) and pure numbers
    ("24" in "24 hour plumbing")."""
    tokens = re.findall(r"[a-z0-9]+", label.lower())
    return {
        _stem(t)
        for t in tokens
        if len(t) > 1 and not t.isdigit() and t not in _FILLER_TOKENS
    }


def _industry_matches(lead_industry: str, target_industries: list[str]) -> bool:
    """True when the lead's (LLM-normalized) industry label belongs to the same
    trade family as any requested target industry."""
    if not target_industries:
        return True
    lead_label = (lead_industry or "").strip().lower()
    lead_stems = _industry_stems(lead_label)
    for wanted in target_industries:
        wanted_label = wanted.strip().lower()
        if lead_label == wanted_label:
            return True
        wanted_stems = _industry_stems(wanted_label)
        # Both sides need a non-filler stem — an all-filler label (e.g. bare
        # "services") only ever matches exactly, never by family.
        if lead_stems and wanted_stems and lead_stems & wanted_stems:
            return True
    return False


def _matches_target(lead, target: Target) -> bool:
    """Scope found leads to the requested target. Google Places addresses start
    with street numbers, so match the city/area anywhere in the formatted address.
    Industries match by family (see _industry_matches), not exact string."""
    area_name = target.area.split(",", 1)[0].strip().lower()
    location = lead.location.lower()
    in_area = area_name in location if area_name else True
    return in_area and _industry_matches(lead.industry, target.industries)


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
                lead_score=score_from_signals(
                    photo_count=total_count,
                    phone_present=lead.phone_present,
                    recent_review_count=lead.recent_review_count,
                    hours_present=lead.hours_present,
                    staleness_flags=lead.staleness_flags,
                ),
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
