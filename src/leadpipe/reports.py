"""Renders the human-facing clickable Markdown views FROM the store
(ARCHITECTURE.md §4/§9). These files are GENERATED — never hand-edited, never
the source of truth. Re-run `leadpipe report` anytime to refresh them.
"""
from __future__ import annotations

from pathlib import Path

from .industries import industry_group, load_industry_categories
from .models import Lead, LeadStatus
from .store import ALLOWED_PROFILES, DEFAULT_PROFILE, LeadStore, normalize_profile

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"

SHARED_ALL_PATH = REPORTS_DIR / "Shared - AI Leads.md"
SHARED_PRIORITIZED_PATH = REPORTS_DIR / "Shared - Prioritized Leads.md"
SHARED_WEBSITE_BRIEFS_PATH = REPORTS_DIR / "Shared - Website Briefs.md"

_STARS = {0: "—", 1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}


def _report_frontmatter(topic: str, contributors: tuple[str, ...], tags: list[str]) -> str:
    """Schema-valid frontmatter (AGENTS.md §5) so generated reports show up in Obsidian Bases.
    No dates on purpose — reports are regenerated from data, so a date would churn every run."""
    return (
        "---\n"
        "type: report\n"
        f"contributors: [{', '.join(contributors)}]\n"
        "status: active\n"
        f"topic: {topic}\n"
        f"tags: [{', '.join(tags)}]\n"
        "---\n\n"
    )


def _cell(value: object) -> str:
    text = "—" if value is None else str(value)
    return text.replace("\r", " ").replace("\n", " ").replace("|", "\\|")


def _profile_label(profile: str) -> str:
    return normalize_profile(profile).title()


def profile_report_paths(profile: str) -> tuple[Path, Path]:
    label = _profile_label(profile)
    return REPORTS_DIR / f"{label} - AI Leads.md", REPORTS_DIR / f"{label} - Prioritized Leads.md"


def profile_website_briefs_path(profile: str) -> Path:
    return REPORTS_DIR / f"{_profile_label(profile)} - Website Briefs.md"


def _active(leads: list[Lead]) -> list[Lead]:
    return [l for l in leads if l.status not in {LeadStatus.INVALID, LeadStatus.ARCHIVED}]


def _score_value(lead: Lead) -> int | None:
    if lead.lead_score is not None:
        return lead.lead_score
    if lead.photo_rating is not None:
        return lead.photo_rating * 15
    return None


def _score_sort_key(lead: Lead) -> tuple[int, int, str]:
    score = _score_value(lead)
    return (-(score if score is not None else -1), -(lead.photo_rating or 0), lead.name)


_ALL_LEADS_HEADER = ["| Business | Industry | Location | Status | Maps |", "|---|---|---|---|---|"]


def _all_leads_row(l: Lead) -> str:
    maps = f"[map]({l.google_maps_url})" if l.google_maps_url else "—"
    return f"| {_cell(l.name)} | {_cell(l.industry)} | {_cell(l.location)} | {_cell(l.status.value)} | {maps} |"


def _all_leads_table(leads: list[Lead]) -> str:
    leads = _active(leads)
    if not leads:
        return "_No leads yet — run `leadpipe find` to populate this list._\n"
    rows = list(_ALL_LEADS_HEADER)
    for l in sorted(leads, key=lambda x: (x.industry, x.name)):
        rows.append(_all_leads_row(l))
    return "\n".join(rows) + "\n"


def _grouped_leads_sections(leads: list[Lead]) -> str:
    leads = _active(leads)
    if not leads:
        return "_No leads yet — run `leadpipe find` to populate this list._\n"
    categories, other_label = load_industry_categories()
    groups: dict[str, list[Lead]] = {}
    for l in leads:
        groups.setdefault(industry_group(l.industry, categories, other_label), []).append(l)

    def _sort_key(label: str) -> tuple[int, str]:
        return (1, label) if label == other_label else (0, label)

    sections = []
    for label in sorted(groups, key=_sort_key):
        members = sorted(groups[label], key=lambda x: (x.industry, x.name))
        rows = list(_ALL_LEADS_HEADER) + [_all_leads_row(l) for l in members]
        sections.append(
            f"<details>\n<summary>{label} ({len(members)})</summary>\n\n" + "\n".join(rows) + "\n\n</details>\n"
        )
    return "\n".join(sections)


def _prioritized_table(leads: list[Lead]) -> str:
    rated = [l for l in _active(leads) if l.photo_rating is not None]
    if not rated:
        return "_No prioritized leads yet — run `leadpipe prioritize` after finding leads._\n"
    rows = [
        "| Score | ⭐ | Business | Industry | Location | Photos | Links | Why |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for l in sorted(rated, key=_score_sort_key):
        stars = _STARS.get(l.photo_rating or 0, "—")
        links = " · ".join(f"[{i+1}]({u})" for i, u in enumerate(l.photo_links)) or "—"
        why = l.rating_reason or "—"
        rows.append(
            f"| {_cell(_score_value(l))} | {_cell(stars)} | {_cell(l.name)} | {_cell(l.industry)} | {_cell(l.location)} | "
            f"{_cell(l.photo_count or 0)} | {links} | {_cell(why)} |"
        )
    return "\n".join(rows) + "\n"


def _website_briefs_table(leads: list[Lead]) -> str:
    briefed = [l for l in _active(leads) if l.site_brief]
    if not briefed:
        return "_No website briefs yet — run `leadpipe intelligence --use-firecrawl` after prioritizing leads._\n"
    rows = [
        "| Business | Industry | Brief | Selling angle | Pages | Visual notes | Sources |",
        "|---|---|---|---|---|---|---|",
    ]
    for l in sorted(
        briefed,
        key=_score_sort_key,
    ):
        pages = ", ".join(l.suggested_pages) or "—"
        sources = " · ".join(f"[{i+1}]({u})" for i, u in enumerate(l.intelligence_sources)) or "—"
        rows.append(
            f"| {_cell(l.name)} | {_cell(l.industry)} | {_cell(l.site_brief or '—')} | "
            f"{_cell(l.selling_angle or '—')} | {_cell(pages)} | {_cell(l.visual_notes or '—')} | "
            f"{sources} |"
        )
    return "\n".join(rows) + "\n"


def render_all_leads(
    leads: list[Lead], *, source_label: str = "data/<profile>/leads.jsonl", contributors: tuple[str, ...] = ("sean",)
) -> str:
    return (
        _report_frontmatter("ai-leads", contributors, ["report", "leads"])
        + "# AI Leads\n\n"
        f"> Generated from `{source_label}` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Every business Lead Finder found with **no website**.\n\n"
        "## By Category\n\n"
        f"{_grouped_leads_sections(leads)}\n"
        "## Full List\n\n"
        f"{_all_leads_table(leads)}"
    )


def render_prioritized(
    leads: list[Lead], *, source_label: str = "data/<profile>/leads.jsonl", contributors: tuple[str, ...] = ("sean",)
) -> str:
    return (
        _report_frontmatter("prioritized-leads", contributors, ["report", "leads", "prioritized"])
        + "# Prioritized Leads\n\n"
        f"> Generated from `{source_label}` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Sorted by photo availability — higher ⭐ means more existing material to build a site from.\n"
        "> Click the link numbers to open the Yelp/Google listing and save photos.\n\n"
        f"{_prioritized_table(leads)}"
    )


def render_website_briefs(
    leads: list[Lead], *, source_label: str = "data/<profile>/leads.jsonl", contributors: tuple[str, ...] = ("sean",)
) -> str:
    return (
        _report_frontmatter("website-briefs", contributors, ["report", "briefs"])
        + "# Website Briefs\n\n"
        f"> Generated from `{source_label}` — do not hand-edit, regenerate with `leadpipe report`.\n"
        "> Build/sales intelligence for prioritized leads. This is judgment, not lifecycle status.\n\n"
        f"{_website_briefs_table(leads)}"
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


def _lead_sort_rank(lead: Lead) -> tuple[int, int, int]:
    return (lead.status.rank, _score_value(lead) or -1, lead.photo_rating or -1)


_SHARED_ALL_HEADER = ["| Owners | Business | Industry | Location | Status | Maps |", "|---|---|---|---|---|---|"]


def _shared_all_row(lead: Lead, owners: list[str]) -> str:
    maps = f"[map]({lead.google_maps_url})" if lead.google_maps_url else "—"
    return (
        f"| {_cell(', '.join(owners))} | {_cell(lead.name)} | {_cell(lead.industry)} | "
        f"{_cell(lead.location)} | {_cell(lead.status.value)} | {maps} |"
    )


def _shared_all_table(rows_with_owners: list[tuple[Lead, list[str]]]) -> str:
    if not rows_with_owners:
        return "_No shared leads yet — run a profile find command to populate this list._\n"
    rows = list(_SHARED_ALL_HEADER)
    for lead, owners in sorted(rows_with_owners, key=lambda x: (x[0].industry, x[0].name)):
        rows.append(_shared_all_row(lead, owners))
    return "\n".join(rows) + "\n"


def _grouped_shared_sections(rows_with_owners: list[tuple[Lead, list[str]]]) -> str:
    if not rows_with_owners:
        return "_No shared leads yet — run a profile find command to populate this list._\n"
    categories, other_label = load_industry_categories()
    groups: dict[str, list[tuple[Lead, list[str]]]] = {}
    for lead, owners in rows_with_owners:
        groups.setdefault(industry_group(lead.industry, categories, other_label), []).append((lead, owners))

    def _sort_key(label: str) -> tuple[int, str]:
        return (1, label) if label == other_label else (0, label)

    sections = []
    for label in sorted(groups, key=_sort_key):
        members = sorted(groups[label], key=lambda x: (x[0].industry, x[0].name))
        rows = list(_SHARED_ALL_HEADER) + [_shared_all_row(lead, owners) for lead, owners in members]
        sections.append(
            f"<details>\n<summary>{label} ({len(members)})</summary>\n\n" + "\n".join(rows) + "\n\n</details>\n"
        )
    return "\n".join(sections)


def _shared_prioritized_table(rows_with_owners: list[tuple[Lead, list[str]]]) -> str:
    rated = [(lead, owners) for lead, owners in rows_with_owners if lead.photo_rating is not None]
    if not rated:
        return "_No shared prioritized leads yet — run `leadpipe prioritize` for a profile first._\n"
    rows = [
        "| Score | ⭐ | Owners | Business | Industry | Location | Photos | Links | Why |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for lead, owners in sorted(
        rated,
        key=lambda x: _score_sort_key(x[0]),
    ):
        stars = _STARS.get(lead.photo_rating or 0, "—")
        links = " · ".join(f"[{i+1}]({u})" for i, u in enumerate(lead.photo_links)) or "—"
        why = lead.rating_reason or "—"
        rows.append(
            f"| {_cell(_score_value(lead))} | {_cell(stars)} | {_cell(', '.join(owners))} | "
            f"{_cell(lead.name)} | {_cell(lead.industry)} | "
            f"{_cell(lead.location)} | {_cell(lead.photo_count or 0)} | {links} | {_cell(why)} |"
        )
    return "\n".join(rows) + "\n"


def _shared_website_briefs_table(rows_with_owners: list[tuple[Lead, list[str]]]) -> str:
    briefed = [(lead, owners) for lead, owners in rows_with_owners if lead.site_brief]
    if not briefed:
        return "_No shared website briefs yet — run `leadpipe intelligence --use-firecrawl` for a profile first._\n"
    rows = [
        "| Owners | Business | Industry | Brief | Selling angle | Pages | Visual notes | Sources |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for lead, owners in sorted(
        briefed,
        key=lambda x: _score_sort_key(x[0]),
    ):
        pages = ", ".join(lead.suggested_pages) or "—"
        sources = " · ".join(f"[{i+1}]({u})" for i, u in enumerate(lead.intelligence_sources)) or "—"
        rows.append(
            f"| {_cell(', '.join(owners))} | {_cell(lead.name)} | {_cell(lead.industry)} | "
            f"{_cell(lead.site_brief or '—')} | {_cell(lead.selling_angle or '—')} | {_cell(pages)} | "
            f"{_cell(lead.visual_notes or '—')} | {sources} |"
        )
    return "\n".join(rows) + "\n"


def render_shared_all(profile_leads: dict[str, list[Lead]]) -> str:
    merged = _merge_shared(profile_leads)
    return (
        _report_frontmatter("shared-ai-leads", ("sean", "matt"), ["report", "leads", "shared"])
        + "# Shared AI Leads\n\n"
        "> Generated from profile stores under `data/<profile>/leads.jsonl` — do not hand-edit.\n"
        "> Archived/invalid leads are hidden by default; owners show who found the same place.\n\n"
        "## By Category\n\n"
        f"{_grouped_shared_sections(merged)}\n"
        "## Full List\n\n"
        f"{_shared_all_table(merged)}"
    )


def render_shared_prioritized(profile_leads: dict[str, list[Lead]]) -> str:
    return (
        _report_frontmatter("shared-prioritized-leads", ("sean", "matt"), ["report", "leads", "prioritized", "shared"])
        + "# Shared Prioritized Leads\n\n"
        "> Generated from profile stores under `data/<profile>/leads.jsonl` — do not hand-edit.\n"
        "> Deduped by `place_id`; higher ⭐ means more existing material to build a site from.\n\n"
        f"{_shared_prioritized_table(_merge_shared(profile_leads))}"
    )


def render_shared_website_briefs(profile_leads: dict[str, list[Lead]]) -> str:
    return (
        _report_frontmatter("shared-website-briefs", ("sean", "matt"), ["report", "briefs", "shared"])
        + "# Shared Website Briefs\n\n"
        "> Generated from profile stores under `data/<profile>/leads.jsonl` — do not hand-edit.\n"
        "> Deduped by `place_id`; each row is build/sales intelligence from the best available profile record.\n\n"
        f"{_shared_website_briefs_table(_merge_shared(profile_leads))}"
    )


def write_reports(store: LeadStore, *, profile: str | None = None) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    leads = list(store.load().values())
    profile = normalize_profile(profile or DEFAULT_PROFILE)
    all_path, prioritized_path = profile_report_paths(profile)
    source_label = f"data/{profile}/leads.jsonl"
    all_path.write_text(render_all_leads(leads, source_label=source_label, contributors=(profile,)), encoding="utf-8")
    prioritized_path.write_text(
        render_prioritized(leads, source_label=source_label, contributors=(profile,)), encoding="utf-8"
    )
    return all_path, prioritized_path


def write_website_briefs(store: LeadStore, *, profile: str | None = None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    leads = list(store.load().values())
    profile = normalize_profile(profile or DEFAULT_PROFILE)
    path = profile_website_briefs_path(profile)
    source_label = f"data/{profile}/leads.jsonl"
    path.write_text(render_website_briefs(leads, source_label=source_label, contributors=(profile,)), encoding="utf-8")
    return path


def write_shared_reports(profiles: list[str] | None = None) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    profiles = profiles or sorted(ALLOWED_PROFILES)
    profile_leads = {profile: list(LeadStore.for_profile(profile).load().values()) for profile in profiles}
    SHARED_ALL_PATH.write_text(render_shared_all(profile_leads), encoding="utf-8")
    SHARED_PRIORITIZED_PATH.write_text(render_shared_prioritized(profile_leads), encoding="utf-8")
    return SHARED_ALL_PATH, SHARED_PRIORITIZED_PATH


def write_shared_website_briefs(profiles: list[str] | None = None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    profiles = profiles or sorted(ALLOWED_PROFILES)
    profile_leads = {profile: list(LeadStore.for_profile(profile).load().values()) for profile in profiles}
    SHARED_WEBSITE_BRIEFS_PATH.write_text(render_shared_website_briefs(profile_leads), encoding="utf-8")
    return SHARED_WEBSITE_BRIEFS_PATH
