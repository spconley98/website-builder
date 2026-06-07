# MEMORY.md — website-builder (shared project state)

> Portable, multi-agent state file. **Read on session start, update on session end.** This is the
> shared source of truth for project state across Claude / Codex / Gemini. Constitution lives in
> [`AGENTS.md`](./AGENTS.md).

**Last updated:** 2026-06-07T15:10:00-05:00 · **Last agent:** Gemini (Antigravity) — Matt onboarding & Places API verified, scaffold merged
**Phase:** scaffold BUILT and working — `leadpipe` CLI runs end-to-end on real data

---

## 👤 Contributors
- **Sean** — owner, sole approver. Set up the repo, skills, reference library, NotebookLM brain, MCP.
- **Matt** (mp214gitty / mpitto214@gmail.com) — collaborator. Onboarding complete (invites accepted, local apps/MCP/env set up).

## ✅ What exists now
- GitHub repo (public, shared) + `.gitignore` + `.mcp.json.example` + `.env.example`.
- Multi-agent constitution: `AGENTS.md` (canonical), `CLAUDE.md` + `GEMINI.md` (pointers), this file.
- Skills: `context-transfer`, `reference-visualizer`.
- Reference library `docs/_reference-library/` — 7 docs, 3 tiers each. Reference only, NOT the scaffold.
- NotebookLM brain `website-builder-brain` (`bd83690f-e997-46c5-b054-6ff3139e11d6`) + project visuals
  + status explainer video (in progress) + Matt morning-briefing script.
- **`leadpipe` — the lead pipeline scaffold, BUILT AND VALIDATED LIVE** (`src/leadpipe/`):
  - `config`/`models`/`store`/`llm` core, `sources/` (google_places, firecrawl), `agents/`
    (lead_finder, lead_prioritizer), `pipeline`, `reports`, Typer `cli` (`find`/`prioritize`/`run`/`report`)
  - 11 passing tests covering the riskiest contracts (dedup, fact/judgment separation, status monotonicity, atomic writes)
  - **Cross-challenged via `three-brain`→Codex** before agents were built on top — caught real
    foundational issues (status regression, enrichment-overwrites-facts) which were fixed pre-emptively
  - **Validated on REAL data**: `leadpipe find --area "Round Rock, TX" --industry "coffee shops"` found
    20 candidates, correctly identified the 1 with no website ("Fresh Brew Cafe"), wrote it to the store,
    rendered the clickable report — full pipeline works end-to-end
  - **Found + fixed a real infra bug**: broken IPv6 routing on Sean's network made every Google/Firecrawl
    HTTPS call hang ~85s; patched IPv4-only DNS resolution in `config.py` → 0.05s. Documented inline.
- Local Ollama model (`qwen2.5:7b`) pulled for Matt's GPU.
- Programmatic NotebookLM CLI (`notebooklm-py`) and Playwright Chromium browser installed for Matt.

## 🔨 In progress
- Status/pipeline explainer video still rendering in NotebookLM (background).

## 🚫 Blocked / waiting
- Firecrawl scraping — account out of credits (code handles this gracefully — Prioritizer skips
  and logs rather than crashing or faking a rating).

## ✅ Architecture (approved 2026-06-07 via /grill-me) — NOW BUILT
Local-AI **lead pipeline** (Python/uv). Lead Finder → Lead Prioritizer → future agents. Google Places
API acquires + detects "no website" (FACT layer); Ollama LLM reasons (classify/rate, JUDGMENT layer);
Firecrawl enriches. Master `leads.jsonl` (dedup by place_id, monotonic status) + generated clickable
Markdown reports. Typer CLI. Full detail: [`docs/project/ARCHITECTURE.md`](./docs/project/ARCHITECTURE.md).

## ➡️ Next
1. ~~Build the scaffold~~ ✅ **DONE — working end-to-end on real data.**
2. ~~Sean picks the Ollama model~~ ✅ **`gemma4-fast`** (Matt picks his own per his GPU — **`qwen2.5:7b` pulled and configured**).
3. ~~Both get keys~~ ✅ **Done** — Sean's Places key live and validated; Matt's original Places API key verified working on Places API (New).
4. **Run real hunts** — fill out `config/targets.yaml` with real areas/industries, run `leadpipe run`.
5. **Top up Firecrawl credits** to unlock Lead Prioritizer's photo-rating step.
6. Build agent #3+ (outreach, etc.) — same pattern: `agents/<name>.py` + one line in `pipeline.STAGES`.

## 📋 REQUIRED — every session, every contributor
Run the **`context-transfer`** skill at the END of every session (say "wrap up" / "/context-transfer").
It updates this file with a summary + **who did what + timestamp**, syncs the NotebookLM brain, and
syncs Obsidian. **This applies to Matt too — first thing to know after his first `git pull`.**

## 🛠️ How to pick this up cold (any agent — Claude, Codex, Gemini)

Read order: `AGENTS.md` (constitution/rules) → this file (state) →
`docs/project/ARCHITECTURE.md` (full design + the approved scaffold tree, §5).

The scaffold is **DONE and working** — this is a real Python project now, not just docs:

```powershell
cd website-builder
uv sync --group dev          # install deps (uv is the package manager — see pyproject.toml)
uv run pytest tests/ -q      # health check — should show 11 passed
uv run leadpipe --help       # see the CLI: find / prioritize / run / report
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
- Firecrawl account is out of credits — `lead_prioritizer` degrades gracefully (skips +
  logs, never fakes a rating). This is expected, not a bug, until credits are topped up.

## Context for next agent
Architecture is locked AND BUILT. The pipeline runs end-to-end on real data (see "What exists
now" above for the live validation result). Matt's onboarding is complete (git pull verified, Ollama model `qwen2.5:7b` pulled, Google key tested and verified working against Places API (New)). Remaining work is in §"Next": real hunts, Firecrawl credits, future agents. Matt onboarding: `docs/project/ONBOARDING_MATT.md`. No approval gate remains on the scaffold — that gate (AGENTS.md §0) was for the *initial* build, which is complete.
