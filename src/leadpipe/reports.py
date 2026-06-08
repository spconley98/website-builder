"""Renders the human-facing clickable Markdown views FROM the store
(ARCHITECTURE.md §4/§9). These files are GENERATED — never hand-edited, never
the source of truth. Re-run `leadpipe report` anytime to refresh them.
"""
from __future__ import annotations

from pathlib import Path

from .models import Lead, LeadStatus
from .store import ALLOWED_PROFILES, DEFAULT_PROFILE, LeadStore, normalize_profile

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"

SHARED_ALL_PATH = REPORTS_DIR / "Shared - AI Leads.md"
SHARED_PRIORITIZED_PATH = REPORTS_DIR / "Shared - Prioritized Leads.md"

_STARS = {0: "—", 1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}


def _profile_label(profile: str) -> str:
    return normalize_profile(profile).title()


def profile_report_paths(profile: str) -> tuple[Path, Path]:
    label = _profile_label(profile)
    return REPORTS_DIR / f"{label} - AI Leads.md", REPORTS_DIR / f"{label} - Prioritized Leads.md"


def _active(leads: list[Lead]) -> list[Lead]:
    return [l for l in leads if l.status not in {LeadStatus.INVALID, LeadStatus.ARCHIVED}]


def _all_leads_table(leads: list[Lead]) -> str:
    leads = _active(leads)
    if not leads:
        return "_No leads yet — run `leadpipe find` to populate this list._\n"
    rows = ["| Business | Industry | Location | Status | Maps |", "|---|---|---|---|---|"]
    for l in sorted(leads, key=lambda x: (x.industry, x.name)):
        maps = f"[map]({l.google_maps_url})" if l.google_maps_url else "—"
        rows.append(f"| {l.name} | {l.industry} | {l.location} | {l.status.value} | {maps} |")
    return "\n".join(rows) + "\n"


def _prioritized_table(leads: list[Lead]) -> str:
    rated = [l for l in _active(leads) if l.photo_rating is not None]
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


def render_all_leads(leads: list[Lead], *, source_label: str = "data/<profile>/leads.jsonl") -> str:
    return (
        "# AI Leads\n\n"
        f"> Generated from `{source_label}` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Every business Lead Finder found with **no website**.\n\n"
        f"{_all_leads_table(leads)}"
    )


def render_prioritized(leads: list[Lead], *, source_label: str = "data/<profile>/leads.jsonl") -> str:
    return (
        "# Prioritized Leads\n\n"
        f"> Generated from `{source_label}` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Sorted by photo availability — higher ⭐ means more existing material to build a site from.\n"
        "> Click the link numbers to open the Yelp/Google listing and save photos.\n\n"
        f"{_prioritized_table(leads)}"
    )


def _merge_shared(profile_leads: dict[str, list[Lead]]) -> list[tuple[Lead, list[str]]]:
    merged: dict[str, tuple[Lead, list[str]]] = {}
    for profile, leads in profile_leads.items():
        for lead in _active(leads):
            existing = merged.get(lead.place_id)
            if existing is None:
                merged[lead.place_id] = (lead, [_profile_label(profile)])
                continue
            current, owners = existing
            best = lead if _lead_sort_rank(lead) > _lead_sort_rank(current) else current
            if _profile_label(profile) not in owners:
                owners.append(_profile_label(profile))
            merged[lead.place_id] = (best, sorted(owners))
    return list(merged.values())


def _lead_sort_rank(lead: Lead) -> tuple[int, int]:
    return (lead.status.rank, lead.photo_rating or -1)


def _shared_all_table(rows_with_owners: list[tuple[Lead, list[str]]]) -> str:
    if not rows_with_owners:
        return "_No shared leads yet — run a profile find command to populate this list._\n"
    rows = ["| Owners | Business | Industry | Location | Status | Maps |", "|---|---|---|---|---|---|"]
    for lead, owners in sorted(rows_with_owners, key=lambda x: (x[0].industry, x[0].name)):
        maps = f"[map]({lead.google_maps_url})" if lead.google_maps_url else "—"
        rows.append(
            f"| {', '.join(owners)} | {lead.name} | {lead.industry} | {lead.location} | {lead.status.value} | {maps} |"
        )
    return "\n".join(rows) + "\n"


def _shared_prioritized_table(rows_with_owners: list[tuple[Lead, list[str]]]) -> str:
    rated = [(lead, owners) for lead, owners in rows_with_owners if lead.photo_rating is not None]
    if not rated:
        return "_No shared prioritized leads yet — run `leadpipe prioritize` for a profile first._\n"
    rows = [
        "| ⭐ | Owners | Business | Industry | Location | Photos | Links | Why |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for lead, owners in sorted(rated, key=lambda x: (-(x[0].photo_rating or 0), x[0].name)):
        stars = _STARS.get(lead.photo_rating or 0, "—")
        links = " · ".join(f"[{i+1}]({u})" for i, u in enumerate(lead.photo_links)) or "—"
        why = lead.rating_reason or "—"
        rows.append(
            f"| {stars} | {', '.join(owners)} | {lead.name} | {lead.industry} | {lead.location} | "
            f"{lead.photo_count or 0} | {links} | {why} |"
        )
    return "\n".join(rows) + "\n"


def render_shared_all(profile_leads: dict[str, list[Lead]]) -> str:
    return (
        "# Shared AI Leads\n\n"
        "> Generated from profile stores under `data/<profile>/leads.jsonl` — do not hand-edit.\n"
        "> Archived/invalid leads are hidden by default; owners show who found the same place.\n\n"
        f"{_shared_all_table(_merge_shared(profile_leads))}"
    )


def render_shared_prioritized(profile_leads: dict[str, list[Lead]]) -> str:
    return (
        "# Shared Prioritized Leads\n\n"
        "> Generated from profile stores under `data/<profile>/leads.jsonl` — do not hand-edit.\n"
        "> Deduped by `place_id`; higher ⭐ means more existing material to build a site from.\n\n"
        f"{_shared_prioritized_table(_merge_shared(profile_leads))}"
    )


def write_reports(store: LeadStore, *, profile: str | None = None) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    leads = list(store.load().values())
    profile = normalize_profile(profile or DEFAULT_PROFILE)
    all_path, prioritized_path = profile_report_paths(profile)
    source_label = f"data/{profile}/leads.jsonl"
    all_path.write_text(render_all_leads(leads, source_label=source_label), encoding="utf-8")
    prioritized_path.write_text(render_prioritized(leads, source_label=source_label), encoding="utf-8")
    return all_path, prioritized_path


def write_shared_reports(profiles: list[str] | None = None) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    profiles = profiles or sorted(ALLOWED_PROFILES)
    profile_leads = {profile: list(LeadStore.for_profile(profile).load().values()) for profile in profiles}
    SHARED_ALL_PATH.write_text(render_shared_all(profile_leads), encoding="utf-8")
    SHARED_PRIORITIZED_PATH.write_text(render_shared_prioritized(profile_leads), encoding="utf-8")
    return SHARED_ALL_PATH, SHARED_PRIORITIZED_PATH
