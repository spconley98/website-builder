---
type: session-log
contributors: [sean]
agent: codex
status: active
created: 2026-06-09
updated: 2026-06-09
topic: scoring-signals
tags: [sessions]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session - Scoring Signals + Report Refresh - 2026-06-09 22:38

**Contributor:** Sean
**Agent:** Codex

## Summary

Implemented the `AGENTS.md` §1 deterministic scoring signals in the live `leadpipe` scaffold.
Google Places Details now captures phone/hours/recent-review/staleness facts for newly found leads,
and Lead Prioritizer writes a deterministic 0-100 `lead_score` from those facts plus photo count.
Profile and shared prioritized reports now show a score column.

## What changed

- Added acquisition fact fields to `LeadCreate` / `Lead`:
  `phone_present`, `recent_review_count`, `hours_present`, `staleness_flags`.
- Added `lead_score` to `LeadPrioritization` / `Lead`.
- Expanded Google Places Details field mask and derived staleness flags:
  `missing_phone`, `missing_hours`, `no_recent_reviews`.
- Added `score_from_signals()` in `lead_prioritizer`:
  photo count remains primary; phone/hours/recent reviews add confidence; staleness flags are soft
  penalties only.
- Updated Website Intelligence prompt context to include `lead_score`.
- Updated profile/shared prioritized reports to display and sort by score.
- Added a report-only legacy fallback (`photo_rating * 15`) so older prioritized records display a
  score until re-prioritized with richer Places facts.
- Regenerated Sean, Matt, and shared reports.

## Commands run

- `uv run pytest tests/ -q` -> 50 passed
- `uv run leadpipe vault validate` -> 36 notes OK
- `uv run leadpipe vault heartbeat` -> 36 notes scanned, 0 broken links, 0 warnings
- `uv run leadpipe report --profile sean` -> regenerated Sean + shared reports
- `uv run leadpipe report --profile matt` -> regenerated Matt + shared reports
- `git commit -m "[1][scoring] Add deterministic lead scoring signals"` -> `69efc64`
- `py -m notebooklm source add ./MEMORY.md --notebook bd83690f-e997-46c5-b054-6ff3139e11d6 --title "[Sean] MEMORY.md - 2026-06-09 2238 - scoring-signals"` -> source `770a10a8-9851-4c5e-9450-f4c42c2489dc`
- `node C:/Users/mysis/.claude/memory-mcp/indexer.mjs` -> succeeded after sandbox escalation; wrote 317 chunks

## Files changed

- `src/leadpipe/models.py`
- `src/leadpipe/sources/google_places.py`
- `src/leadpipe/agents/lead_finder.py`
- `src/leadpipe/agents/lead_prioritizer.py`
- `src/leadpipe/agents/website_intelligence.py`
- `src/leadpipe/reports.py`
- `tests/test_agents.py`
- `tests/test_google_places.py`
- `tests/test_reports.py`
- `tests/test_store.py`
- Generated reports under `reports/`
- `MEMORY.md`
- `_HOT.md` after wrap-up regeneration

## Decisions

- Existing prioritized records are not rewritten in-place just to backfill score facts.
  Reports display a conservative legacy score fallback until those records are naturally
  re-prioritized.
- Staleness signals remain ranking inputs only. No lead is excluded because phone, hours, or recent
  review data is missing.

## Next recommended steps

1. Push the latest `main` commits when ready.
2. Review the 49 Northern CA trade leads and run Website Intelligence on the strongest prioritized
   candidates.
3. Decide the fate of the stray React/Vite scaffold on `matt-wip-2026-06-09`.
4. Investigate the `Spark Electricians` prioritizer timeout if it remains relevant.

## Blockers / risks

- No current blockers.
- Existing stored leads only get the richer Places facts on a future re-find/re-prioritize cycle.
- NotebookLM shared brain is accepted/onboarded for Matt per current `MEMORY.md`.
