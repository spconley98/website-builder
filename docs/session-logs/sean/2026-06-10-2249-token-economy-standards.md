---
type: session-log
contributors: [sean]
agent: claude
status: active
created: 2026-06-10
updated: 2026-06-10
topic: token-economy-standards
tags: [sessions, tokens, context, agents]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session — Token & context economy research + two adopted standards

## What was done
Research → stress-test → adopt pipeline on agent token/context conservation.

1. **NotebookLM deep dive** — queried `NATE HERK GUIDE` (191dfe34) for token-conservation strategy.
   Extracted 8 clusters: 120k/12% context cap, `/compact` at 60% + targeted preserve, CLAUDE.md
   150-200 line router, CLI-over-MCP (claimed 35x), Haiku heavy-read hack, prompt-cache 1hr TTL +
   no-mid-session-model-switch, session-handoff > recompaction, Context Mode / Claude Mem plugins.
2. **Firecrawl research** — scraped official Claude Code best-practices, damiangalarza context-window
   deep-dive (hard numbers: MCP ~663 tok/tool, playwright-mcp 14.3k just to exist, skill ~200 tok at
   startup), and the remio Antigravity technical review (1M native ctx, Agent Manager swarms, artifact
   system, Canvas browser).
3. **Game plan formulated** — 15 conclusions mapped against what the repo already does.
4. **Three-brain adversarial stress test** — Codex route **unavailable** (`~/.codex/config.toml`
   `service_tier = default` invalid for codex-cli 0.128; account rejects `flex`/`fast`). Routed to
   **Gemini 2.5 Pro** instead. Saved at `three-brain-out/2026-06-10-token-economy/`.
5. **Reference doc added** — `docs/_reference-library/(Raw Text) Token_and_Context_Economy.md`
   (graded KEEP/REVISE/CUT, honest about what survived the stress test).
6. **Two missing levers implemented as native standards** (user-approved plan).

## Key finding
Repo already implements most input-token tricks (thin per-turn pointers, generated `_HOT.md`, MEMORY.md
handoff, CLI-over-MCP, single source of truth). Stress test killed the influencer numerology (120k hard
cap = cargo-cult; `/compact` at 60% = micromanagement; 95% confidence gate = misunderstands agentic
loop) and flagged "ditch MCP/35x" as DATED (advanced tool use + deferred/lazy tool loading killed the
per-turn bloat). The two genuinely-missing high-value levers:
- **Output-token economy** — patch/diff edit, never full-file rewrite (the real agentic bottleneck).
- **Exclusion guardrails** — git-tracked ≠ AI-context-excluded; `uv.lock` + `data/**/*.jsonl` get slurped.

## Files changed
- `.geminiignore` (new, tracked) — build junk + `uv.lock` + `data/**/*.jsonl` excluded from Gemini ctx.
- `.aiexclude` (new, tracked) — same content, Google AI / Antigravity convention.
- `.gitignore` — comment noting those two are intentionally tracked.
- `AGENTS.md` — new §6.x "Token & context economy" (patch-don't-rewrite + exclusion guardrails +
  pointer to reference doc); `updated:` → 2026-06-10.
- `docs/_reference-library/(Raw Text) Token_and_Context_Economy.md` (new reference).
- `three-brain-out/2026-06-10-token-economy/` (input + gemini-review + log).

## Verification
- `uv run pytest tests/ -q` → **56 passed**.
- `git check-ignore .geminiignore .aiexclude uv.lock` → all exit 1 (not ignored = tracked). `uv.lock`
  stays git-tracked but AI-excluded — the lever working as intended.

## Gotchas / open items
- **Codex three-brain route is DOWN** — `~/.codex/config.toml` `service_tier = default` invalid for
  codex-cli 0.128 (expects `fast`/`flex`; account rejects both). Review/rescue routes unavailable until
  fixed. Used Gemini as the adversarial brain this session.
- Reference doc is reference-only — only the 2 levers were promoted to AGENTS.md canon (per §4).
- Reports (`reports/*.md`) deliberately left readable (not excluded).
- Pre-existing LF→CRLF churn on `docs/_moc/*`, `ARCHITECTURE.md`, `ONBOARDING_MATT.md`,
  `_working-context/leadpipe.md` — not this session's edits, not committed.

## Next session could
- Fix Codex `service_tier` config to restore three-brain Codex routes.
- Generate the `(Mind Map)` + `(Visualization)` tiers for the new reference doc (reference-visualizer).
- SQLite migration / async-pooling engine work (still the larger open priority).
