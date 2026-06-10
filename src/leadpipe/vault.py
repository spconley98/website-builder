"""Repo-native Obsidian vault maintenance (AGENTS.md §5/§6).

Tool-agnostic on purpose: pure Python/uv with no Obsidian or Claude-skill
dependency, so Sean (Claude) AND Matt (Gemini) run the mandatory wrap-up loop
identically (post three-brain/Codex review — the mandatory loop must not depend
on per-person plugins/skills). Three commands:

    leadpipe vault validate    # frontmatter schema on the allowlisted notes
    leadpipe vault heartbeat   # broken [[wikilinks]] / orphans / stale (report-only)
    leadpipe vault hot         # regenerate _HOT.md from MEMORY.md (deterministic)

Authority rule (Codex): the vault must never hold a "current truth" that competes
with MEMORY.md. `_HOT.md` is a GENERATED digest — stamped generated/stale_after,
never hand-edited — and an agent falls back to MEMORY.md once it is stale.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

import typer
import yaml
from rich.console import Console

ROOT = Path(__file__).resolve().parents[2]
console = Console()

HOT_STALE_DAYS = 5

# --- Frontmatter schema (mirrors AGENTS.md §5) ------------------------------
TYPE_VALUES = {"session-log", "research", "reference", "moc", "project", "report", "context"}
STATUS_VALUES = {"active", "draft", "archived", "superseded"}
AGENT_VALUES = {"claude", "codex", "gemini"}
CONTRIBUTOR_VALUES = {"sean", "matt"}
REQUIRED_KEYS = ("type", "contributors", "status")
LIST_KEYS = ("contributors", "tags", "related")
DATE_KEYS = ("created", "updated", "stale_after")
# `generated` is an ISO datetime (not a plain date) so it is intentionally not in DATE_KEYS.
KNOWN_KEYS = {
    "type", "contributors", "agent", "status", "created", "updated",
    "topic", "tags", "related", "generated", "stale_after",
}

# Notes that MUST carry frontmatter. Codex flagged "backfill all hand-written" as unsafe — generated
# / reference artifacts (reports/, data/, _reference-library raw + mind maps, notebooklm-insights) are
# intentionally excluded so a bulk pass never rewrites source-reference material.
ALLOWLIST_GLOBS = (
    "_HOME.md", "_HOT.md", "past_mistakes.md", "MEMORY.md", "AGENTS.md",
    "docs/project/**/*.md",
    "docs/session-logs/**/*.md",
    "docs/research/sean/**/*.md",
    "docs/research/matt/**/*.md",
    "docs/_moc/**/*.md",
    "docs/_working-context/**/*.md",
)

# Directories never scanned for the note index (not vault content).
_IGNORE_PARTS = {".git", ".obsidian", "node_modules", ".venv", "__pycache__", ".pytest_cache"}
_ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".canvas", ".mp3", ".wav", ".m4a"}

WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
_PHASE_RE = re.compile(r"^\*\*Phase:\*\*\s*(.+)$", re.MULTILINE)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


# --- Frontmatter parsing / validation ---------------------------------------
def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    """Return (data, error). data is the YAML mapping; error is a human string when the
    block is missing/unterminated/not-a-mapping/invalid-YAML."""
    norm = _normalize(text)
    if not norm.startswith("---\n"):
        return None, "no YAML frontmatter block (must start with ---)"
    end = norm.find("\n---", 4)
    if end == -1:
        return None, "frontmatter not terminated with a closing ---"
    try:
        data = yaml.safe_load(norm[4:end])
    except yaml.YAMLError as e:
        return None, f"invalid YAML in frontmatter: {e}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a key/value mapping"
    return data, None


def _is_date(value: object) -> bool:
    if isinstance(value, (date, datetime)):
        return True
    if isinstance(value, str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return False


def validate_frontmatter(data: dict) -> list[str]:
    """Schema errors for a parsed frontmatter mapping (empty list == valid)."""
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if "type" in data and data["type"] not in TYPE_VALUES:
        errors.append(f"type {data['type']!r} not in {sorted(TYPE_VALUES)}")
    if "status" in data and data["status"] not in STATUS_VALUES:
        errors.append(f"status {data['status']!r} not in {sorted(STATUS_VALUES)}")
    if "agent" in data and data["agent"] not in AGENT_VALUES:
        errors.append(f"agent {data['agent']!r} not in {sorted(AGENT_VALUES)}")
    for key in LIST_KEYS:
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be a list (got {type(data[key]).__name__}) — Obsidian types properties globally by name")
    if isinstance(data.get("contributors"), list):
        for c in data["contributors"]:
            if c not in CONTRIBUTOR_VALUES:
                errors.append(f"unknown contributor {c!r} (expected one of {sorted(CONTRIBUTOR_VALUES)})")
    for key in DATE_KEYS:
        if key in data and not _is_date(data[key]):
            errors.append(f"{key} must be a YYYY-MM-DD date (got {data[key]!r})")
    return errors


@dataclass
class NoteIssue:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def check_note(path: Path) -> NoteIssue:
    issue = NoteIssue(path=path)
    data, err = parse_frontmatter(path.read_text(encoding="utf-8"))
    if err:
        issue.errors.append(err)
        return issue
    assert data is not None
    issue.errors.extend(validate_frontmatter(data))
    for key in data:
        if key not in KNOWN_KEYS:
            issue.warnings.append(f"unknown frontmatter key: {key}")
    return issue


def allowlisted_notes() -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for pattern in ALLOWLIST_GLOBS:
        for p in sorted(ROOT.glob(pattern)):
            if p.is_file() and p.suffix == ".md" and p not in seen:
                seen.add(p)
                out.append(p)
    return out


# --- Wikilink resolution ----------------------------------------------------
def extract_wikilinks(text: str) -> list[str]:
    """Bare link targets from [[Target]], [[Target|alias]], [[Target#heading]] (and ![[...]] embeds)."""
    out: list[str] = []
    for raw in WIKILINK_RE.findall(_normalize(text)):
        target = raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()
        if target:
            out.append(target)
    return out


def is_resolvable(target: str, basenames: set[str], relpaths: set[str]) -> bool:
    suffix = Path(target).suffix.lower()
    if suffix and suffix != ".md":
        return True  # attachment / non-note embed — out of scope for note-link checking
    tnorm = target.lower().removesuffix(".md")
    return tnorm in basenames or tnorm in relpaths or Path(tnorm).name in basenames


def _note_index() -> tuple[set[str], set[str]]:
    basenames: set[str] = set()
    relpaths: set[str] = set()
    for p in ROOT.rglob("*.md"):
        if _IGNORE_PARTS & set(p.relative_to(ROOT).parts):
            continue
        basenames.add(p.stem.lower())
        relpaths.add(p.relative_to(ROOT).as_posix().lower().removesuffix(".md"))
    return basenames, relpaths


# --- _HOT.md generation -----------------------------------------------------
def _section(md: str, header_contains: str) -> str:
    out: list[str] = []
    capturing = False
    for line in md.split("\n"):
        if line.startswith("## "):
            if capturing:
                break
            capturing = header_contains.lower() in line.lower()
            continue
        if capturing:
            out.append(line)
    return "\n".join(out).strip()


def _top_lines(text: str, n: int) -> str:
    lines = [l for l in text.split("\n") if l.strip()]
    return "\n".join(lines[:n]) if lines else "_none recorded_"


def _phase(md: str) -> str:
    m = _PHASE_RE.search(md)
    return m.group(1).strip() if m else "_unknown_"


def latest_session_log() -> Path | None:
    logs = [p for p in ROOT.glob("docs/session-logs/**/*.md") if re.match(r"\d{4}-\d{2}-\d{2}", p.name)]
    if logs:
        return max(logs, key=lambda p: p.name)
    logs = [p for p in ROOT.glob("docs/session-logs/**/*.md") if p.is_file()]
    return max(logs, key=lambda p: p.stat().st_mtime) if logs else None


def _first_heading(path: Path) -> str:
    for line in _normalize(path.read_text(encoding="utf-8")).split("\n"):
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return path.stem


def render_hot(memory_md: str, session_log: Path | None, today: date) -> str:
    """Deterministic _HOT.md body from MEMORY.md (the single source of truth) + latest session log."""
    memory_md = _normalize(memory_md)
    stale_after = today + timedelta(days=HOT_STALE_DAYS)
    session_line = "_none_"
    if session_log is not None:
        session_line = f"`{_rel(session_log)}` — {_first_heading(session_log)}"
    frontmatter = (
        "---\n"
        "type: context\n"
        "contributors: [sean]\n"
        "status: active\n"
        f"created: {today.isoformat()}\n"
        f"updated: {today.isoformat()}\n"
        "topic: hot-cache\n"
        f"generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"stale_after: {stale_after.isoformat()}\n"
        "tags: [hot, onboarding]\n"
        'related: ["[[MEMORY]]", "[[AGENTS]]"]\n'
        "---\n\n"
    )
    body = (
        "> **GENERATED by `leadpipe vault hot` — do not hand-edit.** Non-authoritative digest of "
        "`MEMORY.md`. If `stale_after` has passed, treat this as stale and read `MEMORY.md` directly.\n\n"
        "# Right now\n\n"
        f"**Phase:** {_phase(memory_md)}\n\n"
        "## Active tasks\n"
        f"{_top_lines(_section(memory_md, 'in progress'), 8)}\n\n"
        "## Next\n"
        f"{_top_lines(_section(memory_md, 'next'), 6)}\n\n"
        "## Blockers\n"
        f"{_section(memory_md, 'blocked') or '_none_'}\n\n"
        "## Handoff\n"
        f"{_section(memory_md, 'context for next agent') or '_see MEMORY.md_'}\n\n"
        "## Latest session\n"
        f"{session_line}\n"
    )
    return frontmatter + body


# --- Typer sub-app ----------------------------------------------------------
app = typer.Typer(help="Obsidian vault maintenance: validate / heartbeat / hot (pure Python, no plugins).")


@app.command()
def validate() -> None:
    """Assert every allowlisted note matches the §5 frontmatter schema (non-zero exit on violations)."""
    notes = allowlisted_notes()
    failed = 0
    for note in notes:
        issue = check_note(note)
        if issue.errors:
            failed += 1
            console.print(f"[red]✗[/red] {_rel(note)}")
            for e in issue.errors:
                console.print(f"    [red]{e}[/red]")
        for w in issue.warnings:
            console.print(f"    [yellow]warn[/yellow] {_rel(note)}: {w}")
    if failed:
        console.print(f"[red]vault validate: {failed}/{len(notes)} note(s) failed the schema.[/red]")
        raise typer.Exit(code=1)
    console.print(f"[green]vault validate: {len(notes)} note(s) OK.[/green]")


@app.command()
def heartbeat(
    stale_days: int = typer.Option(45, help="Warn when an 'updated' date is older than this many days."),
) -> None:
    """Report broken [[wikilinks]] / missing frontmatter / stale notes. Exits non-zero only on broken links."""
    basenames, relpaths = _note_index()
    notes = allowlisted_notes()
    broken = 0
    warnings = 0
    today = date.today()
    for note in notes:
        text = note.read_text(encoding="utf-8")
        for target in extract_wikilinks(text):
            if not is_resolvable(target, basenames, relpaths):
                broken += 1
                console.print(f"[red]broken link[/red] {_rel(note)} -> [[{target}]]")
        data, err = parse_frontmatter(text)
        if err:
            warnings += 1
            console.print(f"[yellow]no/invalid frontmatter[/yellow] {_rel(note)}: {err}")
            continue
        updated = data.get("updated") if data else None
        if _is_date(updated):
            u = updated if isinstance(updated, date) and not isinstance(updated, datetime) else (
                updated.date() if isinstance(updated, datetime) else datetime.strptime(str(updated), "%Y-%m-%d").date()
            )
            if (today - u).days > stale_days:
                warnings += 1
                console.print(f"[yellow]stale[/yellow] {_rel(note)}: updated {u} (> {stale_days}d)")
    console.print(f"[dim]heartbeat: {len(notes)} note(s) scanned, {broken} broken link(s), {warnings} warning(s).[/dim]")
    if broken:
        raise typer.Exit(code=1)
    console.print("[green]vault heartbeat: no broken links.[/green]")


@app.command()
def hot() -> None:
    """Regenerate _HOT.md from MEMORY.md + latest session log (deterministic; never hand-edit _HOT.md)."""
    memory = (ROOT / "MEMORY.md").read_text(encoding="utf-8")
    today = date.today()
    (ROOT / "_HOT.md").write_text(render_hot(memory, latest_session_log(), today), encoding="utf-8")
    console.print(
        f"[green]vault hot: wrote _HOT.md[/green] (stale_after {today + timedelta(days=HOT_STALE_DAYS)})."
    )
