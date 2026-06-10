"""Tests for the repo-native vault maintenance commands (src/leadpipe/vault.py).

These exercise the pure helpers on temp/sample data so they are deterministic
regardless of the real vault's backfill state.
"""
from __future__ import annotations

from datetime import date

from leadpipe.vault import (
    HOT_STALE_DAYS,
    check_note,
    extract_wikilinks,
    is_resolvable,
    parse_frontmatter,
    render_hot,
    validate_frontmatter,
)

GOOD = {
    "type": "session-log",
    "contributors": ["sean"],
    "agent": "claude",
    "status": "active",
    "created": date(2026, 6, 9),
    "updated": date(2026, 6, 9),
    "topic": "x",
    "tags": ["sessions"],
    "related": ["[[MEMORY]]"],
}


def test_validate_accepts_good_frontmatter():
    assert validate_frontmatter(dict(GOOD)) == []


def test_validate_flags_missing_required():
    errors = validate_frontmatter({"type": "research"})
    assert any("contributors" in e for e in errors)
    assert any("status" in e for e in errors)


def test_validate_flags_non_list_contributors():
    bad = dict(GOOD, contributors="sean")  # scalar, not a list
    errors = validate_frontmatter(bad)
    assert any("contributors must be a list" in e for e in errors)


def test_validate_flags_bad_enums_and_date():
    bad = dict(GOOD, type="bogus", status="open", created="06/09/2026")
    errors = validate_frontmatter(bad)
    assert any("type" in e for e in errors)
    assert any("status" in e for e in errors)
    assert any("created" in e for e in errors)


def test_validate_flags_unknown_contributor():
    bad = dict(GOOD, contributors=["sean", "dave"])
    assert any("dave" in e for e in validate_frontmatter(bad))


def test_parse_frontmatter_missing_block():
    data, err = parse_frontmatter("# No frontmatter here\n")
    assert data is None and "no YAML frontmatter" in err


def test_parse_frontmatter_handles_crlf():
    data, err = parse_frontmatter("---\r\ntype: project\r\ncontributors: [sean]\r\nstatus: active\r\n---\r\n\r\nbody")
    assert err is None
    assert data["type"] == "project"


def test_check_note_roundtrip(tmp_path):
    good = tmp_path / "good.md"
    good.write_text("---\ntype: research\ncontributors: [sean]\nstatus: active\n---\n\n# Body\n", encoding="utf-8")
    assert check_note(good).ok

    bad = tmp_path / "bad.md"
    bad.write_text("# No frontmatter\n", encoding="utf-8")
    assert not check_note(bad).ok


def test_extract_wikilinks_strips_alias_and_heading():
    links = extract_wikilinks("see [[MEMORY]] and [[AGENTS|the rules]] and [[Note#section]] and ![[img.png]]")
    assert links == ["MEMORY", "AGENTS", "Note", "img.png"]


def test_extract_wikilinks_ignores_code_spans_and_blocks():
    text = "real [[MEMORY]] but inline `[[wikilinks]]` and\n```\n[[AGENTS]] in a fence\n```\ndone"
    assert extract_wikilinks(text) == ["MEMORY"]


def test_is_resolvable_matches_basename_path_and_skips_assets():
    basenames = {"memory", "agents"}
    relpaths = {"memory", "agents", "docs/_moc/sessions-moc"}
    assert is_resolvable("MEMORY", basenames, relpaths)
    assert is_resolvable("docs/_moc/Sessions-MOC", basenames, relpaths)
    assert not is_resolvable("Nonexistent", basenames, relpaths)
    assert is_resolvable("diagram.png", basenames, relpaths)  # asset embed — out of scope


def test_render_hot_digests_memory_and_validates():
    memory = (
        "# MEMORY.md\n"
        "**Phase:** test phase operational\n\n"
        "## In progress\n- Sean — doing X\n- Sean — doing Y\n\n"
        "## Blocked / waiting\n- None currently.\n\n"
        "## Next\n1. First next thing\n2. Second next thing\n\n"
        "## Context for next agent\nHandoff sentence for the next agent.\n"
    )
    out = render_hot(memory, None, date(2026, 6, 9))

    # digest content present
    assert "test phase operational" in out
    assert "doing X" in out
    assert "First next thing" in out
    assert "Handoff sentence" in out
    # stale_after is today + HOT_STALE_DAYS
    assert f"stale_after: {date(2026, 6, 9 + HOT_STALE_DAYS)}" in out
    # the generated _HOT.md must itself pass the schema
    data, err = parse_frontmatter(out)
    assert err is None
    assert validate_frontmatter(data) == []
    assert data["type"] == "context"
