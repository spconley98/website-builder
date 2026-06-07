"""Renders the human-facing clickable Markdown views FROM the store
(ARCHITECTURE.md §4/§9). These files are GENERATED — never hand-edited, never
the source of truth. Re-run `leadpipe report` anytime to refresh them.
"""
from __future__ import annotations

from pathlib import Path

from .models import Lead
from .store import LeadStore

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"

ALL_LEADS_PATH = REPORTS_DIR / "(report) AI-Leads.md"
PRIORITIZED_PATH = REPORTS_DIR / "(report) Prioritized-Leads.md"

_STARS = {0: "—", 1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}


def _all_leads_table(leads: list[Lead]) -> str:
    if not leads:
        return "_No leads yet — run `leadpipe find` to populate this list._\n"
    rows = ["| Business | Industry | Location | Status | Maps |", "|---|---|---|---|---|"]
    for l in sorted(leads, key=lambda x: (x.industry, x.name)):
        maps = f"[map]({l.google_maps_url})" if l.google_maps_url else "—"
        rows.append(f"| {l.name} | {l.industry} | {l.location} | {l.status.value} | {maps} |")
    return "\n".join(rows) + "\n"


def _prioritized_table(leads: list[Lead]) -> str:
    rated = [l for l in leads if l.photo_rating is not None]
    if not rated:
        return "_No prioritized leads yet — run `leadpipe prioritize` after finding leads._\n"
    rows = [
        "| ⭐ | Business | Industry | Location | Photos | Links | Why |",
        "|---|---|---|---|---|---|---|",
    ]
    for l in sorted(rated, key=lambda x: (-(x.photo_rating or 0), x.name)):
        stars = _STARS.get(l.photo_rating or 0, "—")
        links = " · ".join(f"[{i+1}]({u})" for i, u in enumerate(l.photo_links)) or "—"
        why = l.rating_reason or "—"
        rows.append(
            f"| {stars} | {l.name} | {l.industry} | {l.location} | {l.photo_count or 0} | {links} | {why} |"
        )
    return "\n".join(rows) + "\n"


def render_all_leads(leads: list[Lead]) -> str:
    return (
        "# AI Leads\n\n"
        "> Generated from `data/leads.jsonl` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Every business Lead Finder found with **no website**.\n\n"
        f"{_all_leads_table(leads)}"
    )


def render_prioritized(leads: list[Lead]) -> str:
    return (
        "# Prioritized Leads\n\n"
        "> Generated from `data/leads.jsonl` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Sorted by photo availability — higher ⭐ means more existing material to build a site from.\n"
        "> Click the link numbers to open the Yelp/Google listing and save photos.\n\n"
        f"{_prioritized_table(leads)}"
    )


def write_reports(store: LeadStore) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    leads = list(store.load().values())
    ALL_LEADS_PATH.write_text(render_all_leads(leads), encoding="utf-8")
    PRIORITIZED_PATH.write_text(render_prioritized(leads), encoding="utf-8")
    return ALL_LEADS_PATH, PRIORITIZED_PATH
