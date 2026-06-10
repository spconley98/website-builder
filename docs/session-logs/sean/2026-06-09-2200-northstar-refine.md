---
type: session-log
contributors: [sean]
agent: claude
status: active
created: 2026-06-09
updated: 2026-06-09
topic: northstar-skillset-refine
tags: [sessions]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session — North Star refinement + skill-set scoping (2026-06-09 22:00)

**Contributor:** Sean · **Agent:** Claude Sonnet 4.6

## What changed
- `AGENTS.md` §4: added "Skill set for this project" — narrowed to lead-pipeline-relevant skills
  (vercel:*, run/verify/code-review/simplify/security-review, context-transfer, three-brain,
  grill-me, caveman:*, claude-api, website-intelligence). Design/genmedia skills explicitly out of
  scope for this project.
- `AGENTS.md` §1: refined North Star. New framing:
  - Source: Google Places API only (no Yelp/directories/social — locked).
  - Scope: no-website-only (no outdated-site/SEO tiers — locked).
  - Added explicit deterministic scoring signals: `photo_count`, `phone_present`,
    `recent_review_count`, `hours_present`, `staleness_flags` (soft penalties, never hard excludes).
  - Output reframed as a **qualified-leads feeder for a future separate website-build/sell repo** —
    leadpipe itself stays out of build/templates/pricing/CRM/outreach.
  - Removed stale "Ollama/RTX 3090" hardware reference (Matt picks his own GPU per existing decision).

## Process
- Pulled 10 sources via Firecrawl (search + 3 deep scrapes: Outscraper, Grape Leads, Targetron) on
  "find businesses without websites" lead-gen space — validated the model against competitors,
  surfaced quality signals (active phone, recent reviews = owner-managed/reachable) and bad-lead
  filters (stale/seasonal/intentionally offline).
- Asked Sean 3 scoping questions (lead-type scope, source scope, end-state framing) — all locked
  to conservative/current options except end-state, which Sean chose to extend (feeder framing).
- Cross-challenged the proposed refinement via `three-brain` → Codex adversarial review. Codex
  verdict: scoring addition worth it but keep it a thin deterministic ranking layer (not a "lead
  quality engine"); soft-penalty staleness flags not hard excludes; feeder framing OK if AGENTS.md
  stays bounded (no build/pricing/CRM/outreach scope creep).

## Commands run
- `uv run pytest tests/ -q` → 39 passed
- `uv run leadpipe vault validate` → 27 notes OK
- `uv run leadpipe vault heartbeat` → 0 broken links, 0 warnings

## Files changed
- `AGENTS.md` (§1, §4)
- `docs/research/notebooklm-insights/Master_Skills_Catalog_Guide.md`,
  `docs/research/notebooklm-insights/Project_Structuring_Guide.md` (pre-existing modified, not
  touched this session — left as-is)

## Decisions
- Locked: no-website-only, Google Places only.
- New: leadpipe = feeder for future separate website-build/sell repo (constitution language only,
  no new code/scope).
- Scoring signals named in §1 are aspirational/spec language — **not yet implemented in
  `src/leadpipe/`**. Next coding session should implement `phone_present`, `recent_review_count`,
  `hours_present`, `staleness_flags` in the Prioritizer per Codex's deterministic-signal list.

## Next recommended steps
1. Implement the new scoring signals in `lead_prioritizer` (deterministic, explainable per Codex).
2. Continue tuning real hunt targets (`config/targets.sean.yaml`).
3. Review Matt's imported leads / `matt-wip-2026-06-09` per existing MEMORY.md backlog.

## Blockers/risks
- None. `.claude/settings.json` appeared as untracked (caveman plugin statusline config, not yet
  set up) — not part of this session's work, left untouched.
