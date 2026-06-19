---
type: project
contributors: [sean]
status: active
created: 2026-06-07
updated: 2026-06-09
topic: project-state
tags: [canon, state]
---

# MEMORY.md — website-builder (shared project state)

> Portable, multi-agent state file. **Read on session start, update on session end.** This is the
> shared source of truth for project state across Claude / Codex / Gemini. Constitution lives in
> [`AGENTS.md`](./AGENTS.md).

**Last updated:** 2026-06-19T00:40:00-07:00 · **Last Agent:** Claude Opus 4.8 — cold-start read + read-only wrapup (Sean); no state change, verified 59/59 + vault clean, committed Bases-plugin churn
**Phase:** operational with active safety/ops hardening. This session added a persistent **graphify**
knowledge graph of the whole repo (committed under `graphify-out/`, wired into the AGENTS.md cold-start
read-path) + 17 curated doc↔code bridges. Branch `nateherk-tiered-llm-sales` (PR #4 → main) still carries
Nate Herk tiered-LLM/sales-methodology work plus existing lead/report diffs; SQLite + `asyncio` remain the
next larger engine upgrades.

---

## 👤 Contributors
- **Sean** — owner, sole approver. Set up the repo, skills, reference library, NotebookLM brain, MCP.
- **Matt** (mp214gitty / mpitto214@gmail.com) — collaborator. Onboarding complete (invites accepted, local apps/MCP/env set up).

## ✅ What exists now
- **Graphify knowledge graph + doc↔code bridges — Sean/Claude, 2026-06-13**: Built a persistent
  knowledge graph of the whole repo via `/graphify` (142 files → 789 nodes/1437 edges/41 communities;
  ~10.8x token reduction/query). Finding: the graph was **16 disconnected islands** — a 361-node code
  island vs. scattered doc/strategy islands; `Sell Methodology` and the `website_intelligence.py` code
  that embodies it shared zero edges. Fixed with `graphify-out/bridges.json` (17 curated doc↔code edges,
  each grounded in an existing source citation or strong concept==code link) + idempotent
  `graphify-out/apply_bridges.py` (re-run after any rebuild — rebuild overwrites `graph.json`). Wired the
  graph into the agent onboarding path: **AGENTS.md §5 "Knowledge graph (graphify) — query before you
  grep"**, and committed `graph.json`/`GRAPH_REPORT.md`/`graph.html` so fresh clones get instant context
  (machine-local dotfiles + cache gitignored). `website_intelligence.py` module docstring now cites
  `SELL_METHODOLOGY.md`/`ARCHITECTURE.md §3`/tiered-LLM A1. Proved the manual-refresh upkeep path:
  `graphify --update` re-extracted only the 2 changed files (49k tokens) → graph now 799 nodes/1480
  edges/39 communities, components 16→10. Chose manual refresh over an auto-rebuild commit hook (recurring
  token cost). **59/59 tests pass.** PR #4 → main. Session log:
  `docs/session-logs/sean/2026-06-13-0920-graphify-knowledge-graph.md`.
- **CA Nursery Leads Hunt — Sean/Gemini, 2026-06-10**: Ran a targeted hunt for "plant nursery" and "garden center" across several California cities (Sacramento, Fresno, San Jose, Los Angeles, San Diego, Bakersfield, Stockton). Acquired 20 new leads without websites in the `found` state. Verified health with `leadpipe check --google` before the hunt and `pytest` after. Changes to `data/sean/leads.jsonl` and generated reports were committed directly to the `nateherk-tiered-llm-sales` branch. Session log: `docs/session-logs/sean/2026-06-10-2358-ca-nursery-leads.md`. Next: run `prioritize` on these leads.
- **Small-town retarget — Sean/Claude, 2026-06-11**: Sean noticed hunts only hit big
  CA cities and believes smaller towns have more no-website opportunity (less
  tech-savvy, less competition). `config/targets.sean.yaml` fully retargeted from 5
  big cities (Sacramento, San Jose, Oakland, Fresno, Santa Rosa) to 12 small CA towns
  (Placerville, Grass Valley, Auburn, Yuba City, Turlock, Manteca, Porterville,
  Hanford, Petaluma, Ukiah, Sonora, Jackson), same 5 trades + 8km radius. New
  `config/ca_small_towns.yaml` (not read by code) is a reference menu of ~30 more
  small CA towns by county for future targets or one-off `--area`/county hunts.
  No code change needed — `Target.area` is free-text into Places Text Search and the
  CLI `--area` override already supports any town/county. 59/59 tests pass, vault
  validate (44 notes) + heartbeat (0 broken links) clean. Session log:
  `docs/session-logs/sean/2026-06-11-0000-small-town-retarget.md`. **Next: run a real
  `leadpipe find` (no Firecrawl) on the new targets to validate geocoding/results.**
- **Lead-source/platform expansion research — Sean/Codex, 2026-06-10**: Researched additional avenues for
  large lead databases and no-website verification. Direction: keep Google Places as the high-confidence
  paid verifier, but do not use paid APIs as the bulk database engine. Best low-cost/free expansion lanes
  are OpenStreetMap/Overpass for small polite queries, Overture Maps Places for larger bulk seeding, and
  public/license/permit datasets for vertical-specific lead seeds. Yelp/Foursquare are useful as secondary
  validation/enrichment sources, not free bulk sources. Apify/Bright Data/Clay/Apollo/n8n are useful reference
  ecosystems but generally paid. For the sister website-building project, public business photos may be used
  for research/mockups, but final publishing should require owner permission and asset provenance; avoid
  customer-uploaded review photos unless rights are clear. Session log:
  `docs/session-logs/sean/2026-06-10-2356-lead-source-research.md`.
- **Nate Herk integration: tiered LLM (A1) + sell methodology (C1) — Sean/Claude, 2026-06-10**:
  Digested all 10 **Reports** in the NotebookLM `NATE HERK GUIDE` notebook (`191dfe34`), cross-referenced
  against the project (found ~60% of Nate's ideas already implemented; numerology already rejected last
  session), and produced a 9-item recommendation catalog (plan
  `access-notebook-lm-and-prancy-ember.md`). Sean shipped two on branch `nateherk-tiered-llm-sales`:
  **A1 tiered/two-pass local LLM** — `config.py`/`.env.example` add `LLM_MODEL_DEEP=gemma4:31b` +
  `LLM_DEEP_TIMEOUT=180`; `llm.generate()` gains optional `model`/`timeout`; `lead_prioritizer` +
  `website_intelligence` escalate the same prompt to the deep tier on any `LLMError` (timeout/unparseable)
  before degrading — recovers the previously-stuck "Spark Electricians" timeout path.
  **C1 sales methodology** — new `docs/project/SELL_METHODOLOGY.md` (Nate framework → no-website-lead
  value story + leverage qualification tests + future sell-repo positioning; linked from `_HOME.md`) and
  leverage/ROI-anchored `_INTELLIGENCE_SYSTEM` + fallback (5-field wire format unchanged). **59/59 tests**
  (+3 new). Gemini three-brain cross-challenge (Codex route still down): 2 false positives disproven by
  tests, 1 valid drift fix applied. Session log:
  `docs/session-logs/sean/2026-06-10-2333-nateherk-tiered-llm-sales.md`.
- **Conservative Obsidian + report cleanup — Sean/Codex, 2026-06-10**: Refreshed `_HOME.md`,
  `Research-MOC`, `Reference-MOC`, and `Sessions-MOC` so agents/users can distinguish canonical state,
  derived NotebookLM research, reference source material, session logs, and generated reports more
  quickly. Clarified `docs/research/README.md`, `docs/research/notebooklm-insights/00_INSIGHTS_INDEX.md`,
  and `reports/README.md` (including Website Brief reports + human-review warning). `reports.py` now
  shares small helpers for repeated link/category rendering while preserving report output; regenerating
  Sean/Matt reports produced no report-content churn. `uv run leadpipe vault validate`,
  `uv run leadpipe vault heartbeat`, and `uv run pytest tests/ -q` pass (56/56).
- **Token & context economy — research + 2 adopted standards — Sean/Claude, 2026-06-10**: Deep-dived
  the `NATE HERK GUIDE` NotebookLM notebook + scraped official Claude Code best-practices, a
  context-window deep-dive, and the Antigravity technical review (Firecrawl). Stress-tested 15 draft
  conclusions via `three-brain` — **Codex route was down** (`~/.codex/config.toml` `service_tier =
  default` invalid for codex-cli 0.128; account rejects `flex`/`fast`), so routed **Gemini** as the
  adversarial brain. Outcome: repo already does most input-token tricks; killed the influencer numerology
  (120k cap, /compact-at-60%, 95% gate) and flagged "ditch MCP/35x" as dated (lazy tool loading).
  **Two genuinely-missing levers adopted as canon in `AGENTS.md` §6.x**: (1) patch-don't-rewrite
  (output tokens are the bottleneck), (2) exclusion guardrails — new git-tracked `.geminiignore` +
  `.aiexclude` exclude `uv.lock` + `data/**/*.jsonl` from agent context (git-tracked ≠ AI-excluded).
  Full playbook (reference-only): `docs/_reference-library/(Raw Text) Token_and_Context_Economy.md`.
  56/56 tests pass. Session log: `docs/session-logs/sean/2026-06-10-2249-token-economy-standards.md`.
- **Today Path implementation — Sean/Codex, 2026-06-10**: NotebookLM CLI context was corrected to the
  canonical `website-builder-brain` (`bd83690f-e997-46c5-b054-6ff3139e11d6`), the stray local Matt
  morning-brief artifact under `docs/project/` was removed after confirming the canonical brain already
  had `[Sean] Matt Morning Brief - 06/10/2026`, and the previous local `main` commit (`5fdc6c8`) was
  pushed to `origin/main`. `AGENTS.md` now includes Hunt Operations (hunt rhythm, territory coordination,
  post-hunt sync, and Website Brief review before outreach), and `past_mistakes.md` documents that
  NotebookLM active context can drift.
- **Prompt compaction + Website Intelligence hardening** — oversized scraped markdown is now compacted
  before Ollama prompts, preserving head, relevant middle snippets, and tail content instead of blindly
  truncating the top. Website Intelligence now tolerates Markdown-style labels, skips leads that already
  have briefs to avoid repeated Firecrawl spend, and writes a conservative fact-only fallback brief if
  Ollama ignores the required schema twice. Tests cover the new behavior; current suite is 56/56 passing.
- **Lead data trust refresh** — legacy prioritized records now have persisted deterministic `lead_score`
  values instead of relying on report-only fallback (Sean 26/26, Matt 68/68). Sean's configured Northern
  CA target leads now have Website Briefs for 25 prioritized CA leads; Fresh Brew Cafe remains unbriefed
  because it is outside the current Sean target config. Reports regenerated.
- **Project Analysis & Pressure Test completed** — Spawned multiple sub-agents to analyze the project's efficiency, review the constitution, and conduct competitive market research. Findings are saved in `docs/session-logs/sean/2026-06-09-2359-efficiency-market-analysis.md`. Identified O(N²) JSONL read/write bottleneck, synchronous I/O blocks, and recommended SQLite, `asyncio`, and `tenacity`.
- **AI Leads reports grouped by industry category** — `config/industry_categories.yaml`
  (broad category → keyword match, e.g. "Trades" ← plumb/electric/hvac/roof/handyman/landscap;
  "Food & Beverage" ← coffee/cafe/restaurant/bakery/bar/brewery; falls back to "Other") +
  `src/leadpipe/industries.py` (`load_industry_categories`, `industry_group`).
  `render_all_leads`/`render_shared_all` now render a "## By Category" section of collapsible
  `<details>` blocks per category above the unchanged "## Full List" master table. Pure
  reporting change, no new agent. 47/47 tests pass (4 new in `tests/test_industries.py`, 2 new
  in `tests/test_reports.py`). Grow the YAML as new industries appear from hunts.
- **Deterministic §1 scoring signals implemented** — Google Places Details now captures
  `phone_present`, `recent_review_count`, `hours_present`, and `staleness_flags` as acquisition
  facts on newly found leads. Lead Prioritizer writes a bounded 0-100 `lead_score` from photo count
  plus those soft reachability/staleness signals. Prioritized reports display score columns and use
  a legacy photo-rating fallback for older records until they are re-prioritized with the richer
  Places facts. 50/50 tests pass.
- **ELI5 onboarding guides for Matt** (`docs/project/`, linked from `_HOME.md`):
  `AGENT_PROMPT_GUIDE (Matt - Getting Up To Date).md` (git sync + copy-paste prompt),
  `AGENT_PROMPT_GUIDE (Start Session).md` (cold-start prompt + what AGENTS.md/_HOT/MEMORY are),
  `AGENT_PROMPT_GUIDE (End Session).md` (wrap-up prompt + what context-transfer does). Pushed
  (`53e1916`).
- **Obsidian agent-brain — MERGED to `main`** (`e289f49`, was branch `obsidian-agent-brain`, PR #2) —
  the vault is now the primary brain with an Authority model (`AGENTS.md` §5), a cold-start read-path
  (`_HOT.md` → `_HOME.md` MOCs → `docs/_working-context/` → `past_mistakes.md` → `MEMORY.md`), schema
  frontmatter on every note, four `docs/_bases/` dashboards, and a repo-native
  `uv run leadpipe vault validate|heartbeat|hot` maintenance engine (no plugins — Matt/Gemini run the
  mandatory loop too). Built from `/grill-me` + the NotebookLM "Obsidian best practices" notebook
  (49 sources) + a three-brain/Codex adversarial review. 39 tests green on both Sean's and Matt's machines.
- **Reciprocal three-brain routing for Codex/Gemini** — `AGENTS.md` §5 "Reciprocal routing" subsection:
  when Codex or Gemini drives, 2x-stuck / self-review / risk-path edits hand off to Claude (or Gemini
  for media/whole-repo scans), mirroring Claude's `~/.claude/commands/three-brain.md`. Codex CLI reads
  `AGENTS.md` natively.
- **Matt's WIP preserved on `matt-wip-2026-06-09`** (not merged) — 16 modified Python files (triaged:
  `config.py`/`cli.py` changes are HIGH risk, revert profile-isolation, do NOT cherry-pick;
  `firecrawl.py` `get_credit_usage()` + 2 credit-guard tests are low-risk/additive, future candidate),
  a stray React/Vite scaffold (unknown origin, stays on that branch only), and his own
  `.claude/skills/three-brain/` (independently installed, separate from the AGENTS.md routing rules
  above). See `docs/research/matt/2026-06-09-wip-branch-diff-summary.md`.
- **Matt confirmed on `28f144e`** — pulled clean (39/39), read AGENTS.md §5 reciprocal routing,
  internalized it as his operating rules. He compared his `.claude/skills/three-brain/` against §5:
  consistent, not stale — skill = full Claude-side detail (parallel consensus, media pipelines,
  startup self-check), §5 = lightweight repo-level mirror for Matt/Gemini/Codex pointing back to it.
  Nothing to change.
- GitHub repo (public, shared) + `.gitignore` + `.mcp.json.example` + `.env.example`.
- Multi-agent constitution: `AGENTS.md` (canonical), `CLAUDE.md` + `GEMINI.md` (pointers), this file.
- Skills: `context-transfer`, `reference-visualizer`.
- Reference library `docs/_reference-library/` — 8 raw docs total; 7 have the full 3-tier treatment.
  New raw reference added this session: `(Raw Text) Local_AI_Agents_for_Leadpipe.md`.
- NotebookLM brain `website-builder-brain` (`bd83690f-e997-46c5-b054-6ff3139e11d6`) + project visuals
  + generated reference/research summaries. Existing duplicate `MEMORY.md` uploads have been renamed
  with contributor/timestamp/topic provenance.
- Obsidian-facing folder indexes exist for `config/`, `data/`, `reports/`, `docs/research/`, and
  `docs/session-logs/`.
- **`leadpipe` — the lead pipeline scaffold, BUILT AND VALIDATED LIVE** (`src/leadpipe/`):
  - `config`/`models`/`store`/`llm` core, `sources/` (google_places, firecrawl), `agents/`
    (lead_finder, lead_prioritizer, website_intelligence), `pipeline`, `reports`, Typer `cli`
    (`check`/`find`/`prioritize`/`run`/`intelligence`/`report`)
  - 26 passing tests covering the riskiest contracts (dedup, fact/judgment separation, status monotonicity, atomic writes,
    local-model config fallback, Prioritizer target scoping, photo-count parse handling, Firecrawl guardrails,
    Website Intelligence queue discipline, Website Brief report rendering, and Markdown report escaping)
  - **Cross-challenged via `three-brain`→Codex** before agents were built on top — caught real
    foundational issues (status regression, enrichment-overwrites-facts) which were fixed pre-emptively
  - **Validated on REAL data**: `leadpipe find --area "Round Rock, TX" --industry "coffee shops"` found
    20 candidates, correctly identified the 1 with no website ("Fresh Brew Cafe"), wrote it to the store,
    rendered the clickable report — full pipeline works end-to-end
  - **Validated again on REAL data with local model + Firecrawl active**: `leadpipe check --google`
    passed; `leadpipe find --area "Round Rock, TX" --industry "coffee shops"` wrote Fresh Brew Cafe;
    `leadpipe prioritize --area "Round Rock, TX" --industry "coffee shops"` processed 1/wrote 1 and
    marked it `prioritized` with a 1-star photo rating from the Google Maps listing.
  - **Surgically imported Matt's work**: Extracted 166 leads from Matt's stale `onboarding-matt` branch
    into `data/matt/leads.jsonl`. Verified his branch was out of sync (pre-scaffold docs) and 
    preserved local `AGENTS.md` / `src/` to prevent regression.
  - **Obsidian framework cleanup**: Removed the legacy `data/leads.jsonl`, renamed reports to
    `Sean - ...`, `Matt - ...`, and `Shared - ...`, moved all session logs to `docs/session-logs/`,
    renamed duplicate README notes, removed redundant `.gitkeep` placeholders, and removed the Matt
    morning briefing artifacts.
  - **Found + fixed a real infra bug**: broken IPv6 routing on Sean's network made every Google/Firecrawl
    HTTPS call hang ~85s; patched IPv4-only DNS resolution in `config.py` → 0.05s. Documented inline.
  - **Request-only Firecrawl guardrails added**: `prioritize`, `run`, and `intelligence` now refuse to spend
    Firecrawl credits unless `--use-firecrawl` is passed explicitly.
  - **Agent 3 built**: Website Intelligence enriches prioritized active leads with build/sales briefs while
    preserving facts, photo judgment, and lifecycle status. Reports now include `Sean - Website Briefs.md`,
    `Matt - Website Briefs.md`, and `Shared - Website Briefs.md`.
  - **Canonical foundation sync prepared**: Current `main` remains the foundation for Sean + Matt; Matt's
    stale `origin/onboarding-matt` branch is preserved as historical evidence only. Verified Matt's branch
    lead file already matches `data/matt/leads.jsonl` exactly (166 records: 98 `found`, 68 `prioritized`),
    added Matt branch audit/proposed-target research notes, fixed Markdown table escaping for lead names/text
    containing `|`, regenerated reports, and kept `config/targets.matt.yaml` empty pending a small chosen run.

## ✅ What exists now (cont.)
- **First Northern CA trade hunt — Sean, 2026-06-09/10**: `config/targets.sean.yaml` repointed
  from TX placeholders to 5 Northern CA areas (Sacramento, San Jose, Oakland, Fresno, Santa Rosa,
  8km radius), 5 industries each (HVAC contractors, plumbers, electricians, handyman,
  landscaping). `leadpipe find` (no Firecrawl needed) found 49 new no-website leads (Sacramento 9,
  San Jose 10, Oakland 15, Fresno 8, Santa Rosa 7). `leadpipe prioritize --use-firecrawl` rated
  25/26 candidates; one persistent failure ("Spark Electricians",
  `ChIJiePmHvA1joARvbNVvZcwFJY`) — Ollama `gemma4-fast` times out after 60s on its scraped content,
  even on retry, lead stays `found`. Reports regenerated. Session log:
  `docs/session-logs/sean/2026-06-09-lead-hunt-norcal-trades.md`.

## 🔨 In progress
- Sean — run `leadpipe check --google` + `leadpipe find` (no Firecrawl) on the new
  small-town targets in `config/targets.sean.yaml`, then regenerate reports.
- Sean — decide fate of stray React/Vite scaffold on `matt-wip-2026-06-09` (delete vs separate repo) —
  last open item from that branch's triage; `get_credit_usage()` + pause guard now done on `main`.
- Sean — reviewing Matt's imported leads in `data/matt/leads.jsonl`.
- Sean — review the 25 generated Northern CA Website Briefs in `reports/Sean - Website Briefs.md`
  before using them for sales outreach; fallback-generated briefs are conservative and still need human
  review.
- Sean — investigate/retry the remaining `found` Sean leads when useful, including "Spark Electricians";
  prompt compaction is now in place, but that lead was not re-prioritized during this session.
- Sean — plan SQLite migration and async/pooling work as separate larger engine upgrades.
- Sean — evaluate a free/open bulk-seeding spike after the current branch/data diffs are settled:
  likely `leadpipe seed-osm` first, then Overture Maps Places or public permit/license datasets.
- Sean — fix Codex `service_tier` config to restore three-brain Codex routes (see Blocked).
- Sean — optionally generate `(Mind Map)` + `(Visualization)` tiers for the new token-economy
  reference doc via `reference-visualizer`.

## 🚫 Blocked / waiting
- **Codex three-brain route DOWN** — `~/.codex/config.toml` has `service_tier = default`, invalid for
  codex-cli 0.128 (expects `fast`/`flex`; OpenAI account rejects both with "Unsupported service_tier").
  Codex review/rescue routes unavailable until the config is fixed; use Gemini as the adversarial brain
  meanwhile. Fix = set a valid/supported `service_tier` (or remove the line) in `~/.codex/config.toml`.
- NotebookLM auth was refreshed after the 2026-06-07 Agent 3 context transfer and `MEMORY.md` was
  uploaded successfully.
- **Skill collision** — invoking `context-transfer` resolves to the GLOBAL AAS-WEBSITE skill
  (`~/.claude/skills/context-transfer`: npm/tsc + AAS notebook) instead of this project's
  `.claude/skills/context-transfer`. The AAS skill is project-specific but lives in global skills, so it
  shadows every repo. Fix = move it into the AAS repo's `.claude/skills/`. Workaround: run the
  website-builder project skill manually (done this session).

## ✅ Architecture (approved 2026-06-07 via /grill-me) — NOW BUILT
Local-AI **lead pipeline** (Python/uv). Lead Finder → Lead Prioritizer → future agents. Google Places
API acquires + detects "no website" (FACT layer); Ollama LLM reasons (classify/rate, JUDGMENT layer);
Firecrawl enriches. Master `leads.jsonl` (dedup by place_id, monotonic status) + generated clickable
Markdown reports. Typer CLI. Full detail: [`docs/project/ARCHITECTURE.md`](./docs/project/ARCHITECTURE.md).

## ➡️ Next
1. ~~Build the scaffold~~ ✅ **DONE — working end-to-end on real data.**
2. ~~Sean picks the Ollama model~~ ✅ **`gemma4-fast`** as the default runtime model (Matt picks his own per his GPU).
3. ~~Both get keys~~ ✅ **Done** — Sean's Places key live and validated; enable "Places API (New)"
   specifically if Matt hits a 403 (a real gotcha Sean hit — see `lead_finder` PlacesError messages).
4. **Run real hunts** — tune `config/targets.sean.yaml` or `config/targets.matt.yaml` with better
   areas/industries, then run `leadpipe run --profile sean --use-firecrawl` or profile-specific one-offs.
5. ~~Top up Firecrawl credits~~ ✅ **Done** — Firecrawl key is active in `.mcp.json` and copied into local `.env`;
   Prioritizer now works on Fresh Brew Cafe.
6. ~~Design budget-safe scheduled operation~~ ✅ **Superseded by request-only operation** — no scheduler;
   Firecrawl-backed commands require explicit `--use-firecrawl`.
7. ~~Implement Sean/Matt profile protocol~~ ✅ **Done**:
   `data/sean/leads.jsonl`, `data/matt/leads.jsonl`, generated `Sean - ...`, `Matt - ...`, and
   `Shared - ...` reports, automatic shared sync/dedup by `place_id`, and soft-delete/archive rather
   than hard delete.
8. **Use contributor context-transfer folders going forward**:
   Sean handoffs in `docs/session-logs/sean/`; Matt handoffs in `docs/session-logs/matt/`.
   Matt's agent should propose shared-memory changes there instead of rewriting `MEMORY.md` directly.
9. **Review Matt imported leads** — especially before prioritizing or using them for outreach.
10. ~~Build agent #3~~ ✅ **Done — Website Intelligence**. Next: run it on prioritized leads with
    `leadpipe intelligence --profile sean --use-firecrawl`.
11. ~~Implement §1 scoring signals~~ ✅ **Done** — Places-backed facts now include
    `phone_present`, `recent_review_count`, `hours_present`, and `staleness_flags`; Prioritizer writes
    deterministic `lead_score`; reports display score columns.
12. **Sync Matt onto canonical `main`** — after Sean pushes, Matt/Matt's agent should run
    `git status --short --branch`, `git fetch origin`, preserve any dirty work on a Matt WIP branch if
    needed, then fast-forward `main`, run `uv sync --group dev`, and run `uv run pytest tests/ -q`.

## 📋 REQUIRED — every session, every contributor
Run the **`context-transfer`** skill at the END of every session (say "wrap up" / "/context-transfer").
It writes a contributor-owned handoff under `docs/session-logs/<sean|matt>/`, updates this file
only when protocol allows, syncs the NotebookLM brain, and syncs Obsidian. **This applies to Matt too
— first thing to know after his first `git pull`.**

## 🛠️ How to pick this up cold (any agent — Claude, Codex, Gemini)

Read order: `AGENTS.md` (constitution/rules) → this file (state) →
`docs/project/ARCHITECTURE.md` (full design + the approved scaffold tree, §5).

The scaffold is **DONE and working** — this is a real Python project now, not just docs:

```powershell
cd website-builder
uv sync --group dev          # install deps (uv is the package manager — see pyproject.toml)
uv run pytest tests/ -q      # health check — should show 25 passed
uv run leadpipe --help       # see the CLI: check / find / prioritize / run / intelligence / report
uv run leadpipe check --google  # verify Google Places + local Ollama before hunts
uv run leadpipe find --area "Austin, TX" --industry restaurants   # try it on real data
```

Code lives in `src/leadpipe/`. Each module has a docstring explaining its role AND any
hardening that came from the `three-brain`→Codex adversarial review (search for
"post three-brain/Codex review" — those comments explain WHY the code looks the way it
does; don't "simplify" them away without re-reading the reasoning).

**Known gotchas already solved — don't rediscover these:**
- `config.py::_force_ipv4_dns()` — broken IPv6 on Sean's network made every Google/Firecrawl
  call hang ~85s; this patch fixes it to ~0.05s. If Matt or anyone hits mysterious slow API
  calls, this is probably why — the patch should already cover it, but verify it's present.
- Google Cloud requires **"Places API (New)"** specifically enabled (not the legacy "Places
  API") — a 403 `SERVICE_DISABLED` error means that toggle is off. `PlacesError` messages
  include the exact enable-URL.
- Firecrawl is credit-backed — `lead_prioritizer` and `website_intelligence` use it and can spend credits.
  They now require explicit `--use-firecrawl`; Finder uses Google Places + Ollama, not Firecrawl.
- `leadpipe check` verifies local setup. Current Sean machine: `gemma4-fast` works via Ollama at
  `http://localhost:11434/v1`; installed local models include `gemma4-fast`, `gemma4:31b`,
  `qwen2.5-coder:14b`, and `nomic-embed-text`.

## Context for next agent
Architecture is locked and built. This session added a committed **graphify knowledge graph** under
`graphify-out/` and wired it into the AGENTS.md §5 cold-start read-path — **query it (`graphify query
"<q>"`) before grepping the repo cold (~10x cheaper context); read `graphify-out/GRAPH_REPORT.md` for the
map.** After any graph rebuild (`/graphify --update`), re-run `python graphify-out/apply_bridges.py` to
re-apply the 17 doc↔code bridges. Prior lead-pipeline work still open: run `leadpipe find` on the new
small-town `config/targets.sean.yaml`, then prioritize. Worktree on `nateherk-tiered-llm-sales` (PR #4).

## 👤 Contributors this session
- **Sean** — asked to graphify the repo, then to bridge the doc↔code islands and point new agents at the
  graph for efficiency.
- **Claude (Opus 4.8)** — built the graph, added curated bridges + `apply_bridges.py`, wired graphify into
  AGENTS.md §5, committed the graph artifacts, ran the incremental refresh, and ran context transfer.

## Active design decisions
- Default local runtime model is **`gemma4-fast`**.
- Keep Hermes/CrewAI/LangGraph/PydanticAI out of the production runtime for now; continue with the
  lightweight `leadpipe` agent-stage pattern.
- Operation is request-only, not 24/7 scheduled. Firecrawl-heavy stages (`prioritize`, `run`, and
  `intelligence`) require explicit `--use-firecrawl`.
- Hunt operations now require the AGENTS.md Hunt Operations rhythm: check git/profile/targets, run
  `leadpipe check`, use `find` first, spend Firecrawl only on explicit request, regenerate reports after
  data changes, and review Website Briefs before outreach.
- Collaboration protocol: Sean and Matt agents should write separate stores; shared visibility comes
  from generated Obsidian reports. Leads may auto-update and auto-archive/soft-delete; no autonomous
  hard delete from shared history.
- Automation safety: no Firecrawl-backed scraping unless explicitly prompted by CLI guard flag; Finder
  defaults to 20 Google Places candidates per industry/request.
- Large database strategy: use free/open data for bulk lead seeding first (OpenStreetMap/Overpass,
  Overture Maps Places, public registries/permits/licenses), then use paid APIs only for deduped,
  shortlisted verification/enrichment batches. Do not treat "missing website in one source" as a hard
  no-website fact until verified.
- Sister website-build asset rule: scraped/public photos are acceptable for research and private drafts;
  final client websites should only publish images marked `approved` or `client_provided`, with source and
  permission provenance tracked.
- Lead scoring: `lead_score` is deterministic and bounded 0-100. Photo availability remains the main
  buildability signal; phone/hours/recent reviews add reachability confidence; staleness flags are soft
  penalties only, never hard excludes.
- Matt stale-copy protocol: when Matt or Matt's agent notices his local repo is behind `origin/main`,
  pause feature work, inspect status/fetch/log divergence, pull fast-forward if clean, or preserve
  Matt's local edits on a Matt branch/WIP commit before reconciling. Never reset or overwrite Matt's
  local work just to pull.
- Selective import protocol: if Sean wants only Matt's context transfer and agent research, fetch and
  inspect Matt's branch but import only `docs/session-logs/matt/`, `docs/research/matt/`,
  `data/matt/`, and approved Matt report outputs. Shared memory, protocol, code, tests, config,
  scaffold docs, and agent tooling require Sean review before import.
- Framework cleanup rule: no new `data/leads.jsonl`, no `(report)` / `(Sean)` style report names, no
  new `docs/context-transfers/` or `docs/project/sessions/` logs. Use profile stores, human-readable
  report names, and `docs/session-logs/<contributor>/`.
- Information architecture cleanup is conservative: keep historical research/reference/session material,
  but label it clearly. `docs/_reference-library/` is source/reference material; `docs/research/` is
  working or derived research; `AGENTS.md`/`MEMORY.md` remain the authorities.
- NotebookLM shared-brain sync initially failed on 2026-06-07 due expired local auth, then succeeded
  after re-authentication. Latest uploaded `MEMORY.md` source ID:
  `d1f9e159-031e-42f8-a1e0-0ced5c395a63` (`[Sean] MEMORY.md - 2026-06-10 2235 - today-path-implementation`).
  Local semantic memory reindex also succeeded.
- NotebookLM source-title rule: all future shared-brain uploads must include contributor, timestamp,
  and topic. Context-transfer `MEMORY.md` uploads must use `[<Name>] MEMORY.md - YYYY-MM-DD HHMM -
  <topic>`; use `[Unknown] ... needs-review` only when provenance cannot be proven.
- Canonical sync decision: `origin/onboarding-matt` is not a merge target. Useful Matt ideas should be
  rebuilt later on current `main`; optional hardening candidates include robust LLM parser fallback and
  configurable `nearby_areas`. Do not add interactive Firecrawl prompts, and keep Firecrawl-backed stages
  behind explicit `--use-firecrawl`.
