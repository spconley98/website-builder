# MEMORY.md — website-builder (shared project state)

> Portable, multi-agent state file. **Read on session start, update on session end.** This is the
> shared source of truth for project state across Claude / Codex / Gemini. Constitution lives in
> [`AGENTS.md`](./AGENTS.md).

**Last updated:** 2026-06-07T21:40:14-07:00 · **Last agent:** Codex — context transfer after manual-run guardrails + Agent 3 Website Intelligence (Sean)
**Phase:** lead generator operational — request-only Firecrawl guardrails active, Agent 3 built, profile/shared reports active

---

## 👤 Contributors
- **Sean** — owner, sole approver. Set up the repo, skills, reference library, NotebookLM brain, MCP.
- **Matt** (mp214gitty / mpitto214@gmail.com) — collaborator. Onboarding complete (invites accepted, local apps/MCP/env set up).

## ✅ What exists now
- GitHub repo (public, shared) + `.gitignore` + `.mcp.json.example` + `.env.example`.
- Multi-agent constitution: `AGENTS.md` (canonical), `CLAUDE.md` + `GEMINI.md` (pointers), this file.
- Skills: `context-transfer`, `reference-visualizer`.
- Reference library `docs/_reference-library/` — 8 raw docs total; 7 have the full 3-tier treatment.
  New raw reference added this session: `(Raw Text) Local_AI_Agents_for_Leadpipe.md`.
- NotebookLM brain `website-builder-brain` (`bd83690f-e997-46c5-b054-6ff3139e11d6`) + project visuals
  + generated reference/research summaries.
- Obsidian-facing folder indexes exist for `config/`, `data/`, `reports/`, `docs/research/`, and
  `docs/session-logs/`.
- **`leadpipe` — the lead pipeline scaffold, BUILT AND VALIDATED LIVE** (`src/leadpipe/`):
  - `config`/`models`/`store`/`llm` core, `sources/` (google_places, firecrawl), `agents/`
    (lead_finder, lead_prioritizer, website_intelligence), `pipeline`, `reports`, Typer `cli`
    (`check`/`find`/`prioritize`/`run`/`intelligence`/`report`)
  - 25 passing tests covering the riskiest contracts (dedup, fact/judgment separation, status monotonicity, atomic writes,
    local-model config fallback, Prioritizer target scoping, photo-count parse handling, Firecrawl guardrails,
    Website Intelligence queue discipline, and Website Brief report rendering)
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

## 🔨 In progress
- Sean — reviewing Matt's imported leads in `data/matt/leads.jsonl`.
- Sean — tuning real hunt targets. The first guarded Sean-config run completed but found 0 new no-website
  candidates for the current Austin/San Antonio target list.
- Sean — running Website Intelligence on prioritized leads once the desired target scope has prioritized
  candidates; one-off Round Rock/Fresh Brew remains available as a known validation lead.

## 🚫 Blocked / waiting
- NotebookLM CLI auth expired during the 2026-06-07 Agent 3 context transfer. Run
  `py -m notebooklm login`, then re-upload `MEMORY.md` to `website-builder-brain`.

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
Architecture is locked AND BUILT. Lead Finder, Lead Prioritizer, and Agent 3 Website Intelligence are
implemented with stage-scoped writes; Firecrawl-backed commands are request-only behind `--use-firecrawl`.
The first guarded Sean-config run completed but found 0 new no-website candidates, so the next agent
should tune target areas/industries or run focused one-offs before expecting new Website Briefs.
Continue using profile stores, generated human-readable reports, and session handoffs under
`docs/session-logs/<contributor>/`.

## 👤 Contributors this session
- **Sean** — chose request-only operation instead of 24/7 scheduling; approved Agent 3 as Website
  Intelligence; requested context transfer and scaffold-following wrapup.
- **Codex** — implemented Firecrawl guardrails, Agent 3 Website Intelligence, Website Brief reports,
  tests, first guarded Sean-config manual run, NotebookLM sync, and this handoff.
- **Matt / Matt's agent** — contributed imported lead/research context now isolated under Matt-owned
  files for Sean review.

## Active design decisions
- Default local runtime model is **`gemma4-fast`**.
- Keep Hermes/CrewAI/LangGraph/PydanticAI out of the production runtime for now; continue with the
  lightweight `leadpipe` agent-stage pattern.
- Operation is request-only, not 24/7 scheduled. Firecrawl-heavy stages (`prioritize`, `run`, and
  `intelligence`) require explicit `--use-firecrawl`.
- Collaboration protocol: Sean and Matt agents should write separate stores; shared visibility comes
  from generated Obsidian reports. Leads may auto-update and auto-archive/soft-delete; no autonomous
  hard delete from shared history.
- Automation safety: no Firecrawl-backed scraping unless explicitly prompted by CLI guard flag; Finder
  defaults to 20 Google Places candidates per industry/request.
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
- NotebookLM shared-brain sync failed on 2026-06-07 after the Agent 3 Website Intelligence wrapup due
  expired local NotebookLM auth. Local semantic memory reindex succeeded.
