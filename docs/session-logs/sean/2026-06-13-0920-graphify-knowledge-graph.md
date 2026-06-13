---
type: session-log
contributors: [sean]
status: active
created: 2026-06-13
updated: 2026-06-13
topic: graphify-knowledge-graph
tags: [sessions, graphify, knowledge-graph, agents-md, efficiency]
---

# Session — graphify knowledge graph + doc↔code bridges (Sean/Claude, 2026-06-13)

## What happened
Built a persistent knowledge graph of the whole repo with `/graphify`, then fixed a
real structural finding and wired the graph into the agent onboarding path.

### 1. Graph build
- `/graphify` on repo root: **142 files** (32 code AST + 101 docs + 9 image
  visualizations) → **789 nodes / 1437 edges / 41 communities**. 1 sensitive file
  skipped. ~628k input tokens (8 semantic subagents, no Gemini key so Claude
  subagents did extraction). Benchmark: ~10.8x token reduction per query.
- Outputs in `graphify-out/`: `graph.json`, `GRAPH_REPORT.md`, `graph.html`.
- God nodes: `LeadStore` (50 edges), `load_settings()`, `Lead`, `LeadStatus`,
  `AgentResult`, `Target`.

### 2. Finding: knowledge base was 16 disconnected islands
The graph fragmented into 16 connected components — a 361-node **code** island vs.
scattered **doc/strategy** islands. `Sell Methodology` (doc) and the
`website_intelligence.py` code meant to embody it shared **zero edges** despite
citing each other in source. Cause: the doc-chunk extractor can't emit the code's
AST node-ids, so cross-layer edges never formed.

### 3. Fix: curated doc↔code bridges
- `graphify-out/bridges.json` — **17 curated edges**, each grounded in a citation
  that already exists in source (EXTRACTED) or a strong concept==code link
  (INFERRED). Cut islands 16 → 12.
- `graphify-out/apply_bridges.py` — idempotent re-stitch; re-run after any rebuild
  (rebuild overwrites `graph.json`). Skips missing endpoints, prints component delta.
- `website_intelligence.py` module docstring now names `SELL_METHODOLOGY.md`,
  `ARCHITECTURE.md §3`, and the `[[tiered-llm]]` A1 pattern (docstring only, no
  logic change).

### 4. Wired graph into agent cold-start path
- `AGENTS.md` §5: new **"Knowledge graph (graphify) — query before you grep"**
  subsection — documents `graphify query`, `GRAPH_REPORT.md` as the map, and the
  re-run-`apply_bridges.py`-after-rebuild rule. Source wins on disagreement.
- Committed `graph.json` + `GRAPH_REPORT.md` + `graph.html` so a fresh clone has
  instant graph context with no rebuild.
- `graphify-out/.gitignore` keeps machine-local interpreter paths + extraction
  cache out of the repo; only shareable artifacts tracked.

### 5. Proved the manual-refresh upkeep path
- Ran `graphify --update` (recommended over an auto-rebuild hook): re-extracted
  only the 2 changed files (`AGENTS.md`, `website_intelligence.py`) — **49k tokens**
  vs a full rebuild. Correctly excluded the committed `graphify-out/` artifacts.
- Re-ran `apply_bridges.py` (idempotent, 17 intact). Graph now **799 nodes / 1480
  edges / 39 communities**; components **12 → 10**.

## Health
- `uv run pytest tests/ -q` → **59 passed**.

## Git
Branch `nateherk-tiered-llm-sales`, **PR #4 → main** opened. Commits this session:
`fe56491` bridges + docstring · `50b0fb8` AGENTS.md wiring + artifacts ·
`d41f298` incremental refresh.

## Next
- Refresh the graph after meaningful source drift: `/graphify --update` →
  `python graphify-out/apply_bridges.py` → commit `graph.json`/`GRAPH_REPORT.md`/`graph.html`.
- Still open from prior sessions: run `leadpipe find` on the new small-town targets;
  fix Codex `service_tier` to restore three-brain Codex routes.
