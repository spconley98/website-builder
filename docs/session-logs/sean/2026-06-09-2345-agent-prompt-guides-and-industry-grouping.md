---
type: session-log
contributors: [sean]
agent: claude
status: active
created: 2026-06-09
updated: 2026-06-09
topic: agent-prompt-guides-and-industry-grouping
tags: [sessions]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Sean Session Log — 2026-06-09 23:45 — Agent Prompt Guides + Industry Grouping

## What changed

1. **New ELI5 onboarding guides for Matt** (Obsidian, `docs/project/`):
   - `AGENT_PROMPT_GUIDE (Matt - Getting Up To Date).md` — explains git sync words
     (origin/main/HEAD/fetch/pull --ff-only) + copy-paste sync prompt.
   - `AGENT_PROMPT_GUIDE (Start Session).md` — explains AGENTS.md/_HOT/_HOME/MEMORY/
     past_mistakes + copy-paste cold-start prompt.
   - `AGENT_PROMPT_GUIDE (End Session).md` — explains what `wrap up` does step-by-step +
     copy-paste end-of-session prompt.
   - All three cross-linked, linked from `_HOME.md`. Committed + pushed (`53e1916`).

2. **Industry-category grouping for "AI Leads" reports** (pure reporting change, no new agent):
   - New `config/industry_categories.yaml` — broad category (Trades, Food & Beverage, Other)
     to keyword-match list against `Lead.industry`.
   - New `src/leadpipe/industries.py` — `load_industry_categories()` + `industry_group()`.
   - `src/leadpipe/reports.py` — `render_all_leads()` and `render_shared_all()` now have a
     "## By Category" section (collapsible `<details>` per category) above the unchanged
     "## Full List" master table.
   - New `tests/test_industries.py` (4 tests) + 2 new tests in `tests/test_reports.py`;
     updated 1 existing assertion (count expectation changed from 1→2 since the lead now
     appears in both the grouped section and the full list — expected).
   - 47/47 tests pass. Committed (`94ccef9`), **not yet pushed**.

## Commands run

```
uv run pytest tests/ -q          # 47 passed
uv run leadpipe vault validate   # 34 notes OK
uv run leadpipe vault heartbeat  # 0 broken links
uv run leadpipe report --profile sean   # regenerated all 6 reports (verification only)
```

## Decisions made

- Taxonomy lives in editable YAML config (`config/industry_categories.yaml`), not hardcoded —
  Matt/Sean can add new categories/keywords without touching code.
- Grouping covers "AI Leads" reports only (not Prioritized/Website Briefs) per Sean's choice.
- Layout: single-level `<details>` per broad category, full flat master table kept unchanged
  below — not nested two-level.

## Files changed (this session, committed)

- `_HOME.md`
- `docs/project/AGENT_PROMPT_GUIDE (Start Session).md` (new)
- `docs/project/AGENT_PROMPT_GUIDE (End Session).md` (new)
- `docs/project/AGENT_PROMPT_GUIDE (Matt - Getting Up To Date).md` (new)
- `config/industry_categories.yaml` (new)
- `src/leadpipe/industries.py` (new)
- `src/leadpipe/reports.py`
- `tests/test_industries.py` (new)
- `tests/test_reports.py`

## Left uncommitted (pre-existing, not touched/not mine to resolve)

- `config/targets.sean.yaml` (modified before this session)
- `data/sean/leads.jsonl` (modified before this session)
- Regenerated report files under `reports/` from the verification `leadpipe report --profile
  sean` run (reflect the above pre-existing data changes mixed with the new grouping —
  regenerate again after those data changes are resolved/committed).

## Next recommended steps

- Sean: decide on `config/targets.sean.yaml` / `data/sean/leads.jsonl` pending changes, then
  re-run `leadpipe report` and commit refreshed reports.
- Sean: push commit `94ccef9` (industry grouping) once ready.
- Open from `_HOT.md`: §1 scoring signals (`phone_present`, `recent_review_count`,
  `hours_present`, `staleness_flags`) still not implemented; React/Vite stray scaffold fate
  still open.
- Grow `config/industry_categories.yaml` as new industries appear from hunts (currently only
  Trades + Food & Beverage seeded).

## Blockers

None.
