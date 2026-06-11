---
type: session-log
contributors: [sean]
agent: claude
status: active
created: 2026-06-10
updated: 2026-06-10
topic: nateherk-tiered-llm-sales
tags: [sessions, llm, sales]
related: ["[[MEMORY]]", "[[SELL_METHODOLOGY]]", "[[ARCHITECTURE]]"]
---

# Session — Nate Herk integration: tiered LLM (A1) + sell methodology (C1)

**Contributor:** Sean · **Agent:** Claude Opus 4.8 · **Branch:** `nateherk-tiered-llm-sales`
**Timestamp:** 2026-06-10 23:33

## What happened
Digested all 10 **Reports** in the NotebookLM `NATE HERK GUIDE` notebook (`191dfe34`),
cross-referenced against the project, and produced a 9-item recommendation catalog
(plan file `access-notebook-lm-and-prancy-ember.md`). Sean selected two to implement:
**A1 (tiered LLM)** and **C1 (sales methodology)**. Both shipped.

Key cross-reference finding: project already implements ~60% of Nate's ideas (Karpathy
LLM Wiki, CLI>MCP, applied-learning log, hot cache, three-brain, vault linting,
patch-don't-rewrite, exclusion guardrails) and last session already rejected his
numerology (`/compact`@60%, 95% number). Recommendations avoided re-litigating those.

## Changes
**A1 — tiered/two-pass local LLM** (fixes a real stuck lead):
- `config.py` + `.env.example`: `LLM_MODEL_DEEP=gemma4:31b`, `LLM_DEEP_TIMEOUT=180`.
- `llm.generate()`: optional `model`/`timeout` params (additive, back-compat).
- `agents/lead_prioritizer.py::_estimate_photo_count` + `agents/website_intelligence.py::
  _generate_intelligence`: fast model first → on any `LLMError` (timeout or unparseable)
  escalate the SAME prompt to the deep model + 180s, then degrade (skip / fallback).
  Recovers the previously-stuck "Spark Electricians" path instead of skipping.

**C1 — sales methodology**:
- New `docs/project/SELL_METHODOLOGY.md` (Nate framework → "you're already found,
  inquiries leak to competitors" value story; 3 leverage tests as lead qualification;
  leverage-billed posture; future sell-repo notes). Linked from `_HOME.md`.
- `agents/website_intelligence.py`: `_INTELLIGENCE_SYSTEM` + `_fallback_intelligence` now
  ROI/leverage-anchored. 5-field wire format (BRIEF/ANGLE/PAGES/CONTENT/VISUAL) unchanged
  → parser + tests unaffected.

## Commands run + results
- `uv run pytest tests/ -q` → **59 passed** (was 56; +3 new: 2 escalation, 1 leverage cue).
- `uv run leadpipe vault validate` → 42 notes OK (incl. new SELL_METHODOLOGY).
- `uv run leadpipe vault heartbeat` → 0 broken links, 0 warnings.
- `ollama list` → `gemma4:31b` confirmed installed (deep tier is real).
- **three-brain cross-challenge** via Gemini (Codex route still down): 6 findings → 2 false
  positives disproven by tests (missing-import, non-LLMError parsers), 3 accepted-minor
  (broad LLMError catch, load_settings re-read, deep-timeout skip), **1 valid fix applied**
  (unified prioritizer deep-retry to reuse the same `prompt` — kills instruction drift).
  Re-ran tests after fix → still 59.

## Files changed
`config.py`, `.env.example`, `llm.py`, `agents/lead_prioritizer.py`,
`agents/website_intelligence.py`, `tests/test_agents.py`,
`docs/project/SELL_METHODOLOGY.md` (new), `_HOME.md`.

## Decisions
- Escalate on ANY `LLMError` (not just timeout) for simplicity; a connection error fails
  fast again, acceptable cost. `llm_model` stays the fast/default model (back-compat).
- C1 lands as positioning doc + brief-prompt voice only; outreach/CRM/pricing/site-build
  remain out of leadpipe scope (future separate sell repo).

## Next recommended steps
- Live-verify A1: re-prioritize "Spark Electricians" with Ollama up + Firecrawl credits —
  should escalate to deep on the 60s timeout and move `found → prioritized`.
- Decide whether to PR `nateherk-tiered-llm-sales` → `main`.
- Remaining catalog if wanted: A2 verification gate · A3 parallelize (async) · A4
  idea-mining briefs · B1 audit/hunt skills · B2 index+log · B3 tighten past_mistakes ·
  C2 "pain" leverage signal in lead_score.

## Blockers / risks
- **Codex three-brain route still DOWN** (`~/.codex/config.toml` `service_tier` invalid for
  codex-cli 0.128). Used Gemini as adversarial brain. Fix pending Sean.
- **Skill collision**: invoking `context-transfer` resolved to the GLOBAL AAS-WEBSITE skill
  (`~/.claude/skills/context-transfer`) instead of this project's. The AAS skill is a
  project-specific skill wrongly living in global skills → pollutes every repo. Recommend
  moving it into the AAS repo's `.claude/skills/`. This session followed the correct
  website-builder project skill manually.
