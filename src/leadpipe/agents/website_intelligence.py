"""Website Intelligence — turns prioritized leads into build/sales briefs.

This is Agent 3. It works only after Lead Prioritizer has found usable listing
evidence, then uses Firecrawl-acquired page content plus local LLM reasoning to
produce a compact website brief. It does not change lifecycle status: this is
build intelligence, not outreach/contact progress.

See docs/project/SELL_METHODOLOGY.md for the ANGLE/CONTENT selling frame baked
into `_INTELLIGENCE_SYSTEM` (the Nate Herk-derived C1 leverage positioning), and
ARCHITECTURE.md §3 for where this agent sits in the pipeline. The fast-then-deep
model escalation here is the A1 tiered-LLM pattern (see [[tiered-llm]] in MEMORY).
"""
from __future__ import annotations

from datetime import date

from .. import llm
from ..config import Target, load_settings
from ..models import LeadStatus, LeadWebsiteIntelligence
from ..sources import firecrawl
from ..store import LeadStore
from .base import AgentResult
from .lead_prioritizer import _matches_target
from .scraped_content import compact_scraped_content

NAME = "website_intelligence"
INTELLIGENCE_PROMPT_CONTENT_LIMIT = 8000

_INTELLIGENCE_SYSTEM = (
    "You write concise website-build briefs for local-business sales. Use only "
    "the provided lead record and scraped listing content. Do not invent facts. "
    "If something is unclear, say so briefly.\n"
    "SELLING FRAME (see docs/project/SELL_METHODOLOGY.md): this business already gets "
    "discovery views on its Google listing but owns no website, so inquiries leak to "
    "competitors. The ANGLE must be a concrete ROI/leverage point — converting existing "
    "listing views into direct owned-channel inquiries and credibility — not a generic "
    "'you need a website'. The CONTENT note should capture proof/trust material (reviews, "
    "service area, credentials) that turns a viewer into a lead.\n"
    "Respond in EXACTLY this format:\n"
    "BRIEF: <one sentence describing what site this business likely needs>\n"
    "ANGLE: <one concise ROI/leverage selling angle>\n"
    "PAGES: <comma-separated page names>\n"
    "CONTENT: <one short note about proof/trust copy to gather>\n"
    "VISUAL: <one short note about photos/design direction>"
)


def _listing_urls(lead) -> list[str]:
    urls: list[str] = []
    urls.extend(lead.photo_links)
    if lead.google_maps_url:
        urls.append(lead.google_maps_url)
    if lead.yelp_url:
        urls.append(lead.yelp_url)
    return list(dict.fromkeys(urls))


def _build_prompt(lead, scraped_content: str) -> str:
    compacted = compact_scraped_content(scraped_content, max_chars=INTELLIGENCE_PROMPT_CONTENT_LIMIT)
    return (
        "Create the website intelligence brief for this lead.\n\n"
        f"Business: {lead.name}\n"
        f"Industry: {lead.industry}\n"
        f"Location: {lead.location}\n"
        f"Lead score: {lead.lead_score if lead.lead_score is not None else 'unknown'}\n"
        f"Photo rating: {lead.photo_rating}\n"
        f"Photo count: {lead.photo_count}\n"
        f"Prioritizer reason: {lead.rating_reason or 'unknown'}\n\n"
        f"SCRAPED_LISTING_CONTENT:\n{compacted}\n\n"
        "Return exactly:\n"
        "BRIEF: <one sentence>\n"
        "ANGLE: <one concise selling angle>\n"
        "PAGES: <comma-separated page names>\n"
        "CONTENT: <one short note>\n"
        "VISUAL: <one short note>"
    )


def _parse_response(response: str) -> dict[str, object]:
    fields: dict[str, str] = {}
    for line in response.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().strip("*`# ").upper()
        if key in {"BRIEF", "ANGLE", "PAGES", "CONTENT", "VISUAL"}:
            fields[key] = value.strip().strip("*` ")
    missing = {"BRIEF", "ANGLE", "PAGES", "CONTENT", "VISUAL"} - set(fields)
    if missing:
        raise llm.LLMError(f"could not parse website intelligence fields: {', '.join(sorted(missing))}")
    pages = [p.strip() for p in fields["PAGES"].split(",") if p.strip()]
    return {
        "site_brief": fields["BRIEF"],
        "selling_angle": fields["ANGLE"],
        "suggested_pages": pages,
        "content_notes": fields["CONTENT"],
        "visual_notes": fields["VISUAL"],
    }


def _fallback_intelligence(lead) -> dict[str, object]:
    """Conservative fallback when the LLM ignores the required wire format."""
    industry = lead.industry or "local business"
    location = lead.location or "its service area"
    return {
        "site_brief": f"A simple credibility website for {lead.name}, a {industry} lead in {location}.",
        "selling_angle": (
            "Capture the inquiries already leaking from listing views — an owned site "
            "converts existing discovery traffic into direct, credible leads."
        ),
        "suggested_pages": ["Home", "Services", "Gallery", "Contact"],
        "content_notes": "Gather proof/trust copy — reviews, credentials, service area, hours — and verify before outreach.",
        "visual_notes": "Use only verified listing photos or owner-provided images.",
    }


def _generate_intelligence(lead, scraped_content: str) -> dict[str, object]:
    """Tiered (Nate Herk model tiering): fast model first; if it times out or returns
    an unparseable brief, escalate the retry to the deep model + longer timeout before
    falling back to the conservative canned brief."""
    try:
        response = llm.generate(
            _build_prompt(lead, scraped_content),
            system=_INTELLIGENCE_SYSTEM,
            temperature=0.2,
        )
        return _parse_response(response)
    except llm.LLMError:
        settings = load_settings()
        try:
            repair = llm.generate(
                _build_prompt(lead, scraped_content),
                system=_INTELLIGENCE_SYSTEM,
                temperature=0.0,
                model=settings.llm_model_deep,
                timeout=settings.llm_deep_timeout,
            )
            return _parse_response(repair)
        except llm.LLMError:
            return _fallback_intelligence(lead)


def run(store: LeadStore, target: Target) -> AgentResult:
    processed = created_or_updated = skipped = 0
    errors: list[str] = []

    candidates = [
        l
        for l in store.by_status(LeadStatus.PRIORITIZED)
        if l.photo_rating is not None and not l.site_brief and _matches_target(l, target)
    ]

    for lead in candidates:
        processed += 1
        try:
            urls = _listing_urls(lead)
            if not urls:
                skipped += 1
                errors.append(f"{lead.place_id} ({lead.name!r}): no listing URL to research")
                continue

            scraped_chunks: list[str] = []
            sources: list[str] = []
            for url in urls[:3]:
                scraped_chunks.append(firecrawl.scrape(url))
                sources.append(url)

            parsed = _generate_intelligence(lead, "\n\n---\n\n".join(scraped_chunks))
            update = LeadWebsiteIntelligence(
                place_id=lead.place_id,
                intelligence_sources=sources,
                intelligence_date=date.today(),
                **parsed,
            )
            store.apply_website_intelligence(update)
            created_or_updated += 1

        except (firecrawl.FirecrawlError, llm.LLMError) as e:
            skipped += 1
            errors.append(f"{lead.place_id} ({lead.name!r}): {e}")
        except Exception as e:
            skipped += 1
            errors.append(f"{lead.place_id} ({lead.name!r}): unexpected error — {e}")

    return AgentResult(NAME, processed, created_or_updated, skipped, errors)
