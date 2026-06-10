---
type: session-log
contributors: [sean]
agent: claude
status: active
created: 2026-06-09
updated: 2026-06-09
topic: firecrawl-credit-pause-guard
tags: [sessions]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session — Firecrawl credit-pause guard cherry-pick (2026-06-09 23:30)

**Contributor:** Sean · **Agent:** Claude Sonnet 4.6

## What changed
Reviewed `origin/matt-wip-2026-06-09` diff against `main` for `src/leadpipe/sources/firecrawl.py` and
`tests/test_agents.py` (per MEMORY.md backlog item). Found:
- `firecrawl.py` `get_credit_usage()` — additive, low-risk (as flagged).
- `tests/test_agents.py` — Matt's branch **deleted** 5 existing tests (`_matches_target`,
  `_parse_photo_count_response`, `website_intelligence`, llm-config-fallback) and replaced with
  2 new credit-pause tests that depend on a pause feature not present on `main`.

Did NOT cherry-pick wholesale. Instead, built the feature properly on `main`:
- `src/leadpipe/sources/firecrawl.py` — ported `get_credit_usage()` (hits Firecrawl
  `/v2/team/credit-usage`, returns `None` on any failure so callers don't block on "can't tell").
- `src/leadpipe/config.py` — new `Settings.firecrawl_pause_credits_pct` (env
  `FIRECRAWL_PAUSE_CREDITS_PCT`, default `5.0`).
- `src/leadpipe/agents/lead_prioritizer.py` — new `_credit_pause_error()`; `run()` now checks
  remaining/plan credit % up front and returns immediately with a clear error if below threshold
  (account-wide credits, shared Sean/Matt — pauses everyone's Firecrawl-backed prioritization).
- `tests/test_agents.py` — added Matt's 2 pause tests (`test_prioritizer_pauses_when_credits_low`,
  `test_prioritizer_does_not_pause_when_credits_healthy`) **alongside** all 5 existing tests, none
  removed.
- `.env.example` — documented `FIRECRAWL_PAUSE_CREDITS_PCT`; also dropped the stale
  "Sean's RTX 3090" comment (consistent with this session's earlier AGENTS.md §1 hardware-ref removal).

## Commands run
- `uv run pytest tests/ -q` → 41 passed (was 39)
- `uv run leadpipe vault validate` → 29 notes OK
- `uv run leadpipe vault heartbeat` → 0 broken links, 0 warnings

## Files changed
- `src/leadpipe/sources/firecrawl.py`
- `src/leadpipe/config.py`
- `src/leadpipe/agents/lead_prioritizer.py`
- `tests/test_agents.py`
- `.env.example`

## Decisions
- Account-wide credit pause (not per-profile) — Firecrawl credits are shared between Sean and Matt.
- Default pause threshold 5% remaining — conservative, doesn't change current behavior until credits
  are nearly exhausted; tunable per-collaborator via `.env`.
- `matt-wip-2026-06-09` branch: this was the one outstanding cherry-pick item from that branch's
  triage. The stray React/Vite scaffold on that branch is still unaddressed (delete vs separate repo
  — still open per MEMORY.md backlog).

## Next recommended steps
1. Decide fate of stray React/Vite scaffold on `matt-wip-2026-06-09` (delete vs separate repo).
2. Implement the §1 scoring signals (`phone_present`, `recent_review_count`, `hours_present`,
   `staleness_flags`) spec'd in the previous session.
3. Continue real hunt tuning (`config/targets.sean.yaml` / `config/targets.matt.yaml`).

## Blockers/risks
None.
