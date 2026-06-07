# website-builder — Architecture & Vision

> **Project canon.** This is the real architecture and plan (distinct from `docs/_reference-library/`,
> which is idea/reference material only). Status as of 2026-06-07: **architecture approved via
> `/grill-me`; scaffold built, tested, and validated live as the `leadpipe` Python CLI.**

---

## 1. Vision & goal

Build a **local-AI-powered lead pipeline** that finds local businesses **without a website**, researches
them, and prioritizes them — so Sean + Matt can build websites for those businesses and sell them.

The pipeline does the hard, repetitive research **locally** (Ollama on an RTX 3090 — free + private),
producing clean, prioritized lead lists. Sean/Matt then build a site (cloning from polished templates
in a *separate, future* project) and sell it to the business.

**Inspiration (context, not a blueprint):** a "lazy"/automated AI-agency strategy — instead of manual
labor, a small department of AI workers fixes local-business revenue leaks; target tight networks
(e.g. franchise owners) for word-of-mouth; use AI to pre-qualify leads instead of cold outreach. We're
adapting the *automated-workers* idea to lead generation specifically.

> This is a **rough draft that will evolve.** More agents and detail will be added over time.

---

## 2. Scope

| In scope (this repo) | Out of scope (separate future repo) |
|---|---|
| The lead-research **pipeline** | The **website-building** templates/system |
| Agents: Lead Finder, Lead Prioritizer, future agents | Actual site production + sale |
| Lead data store + clickable reports | Branding/photo transfer into templates |

Sean already has polished Next.js website projects (AAS-WEBSITE, VR-REDESIGN) to clone for the build
side — so that's a solved problem handled elsewhere. **This repo is the new, hard, valuable part.**

---

## 3. The pipeline

```
config/targets.yaml                (areas + industries to hunt)
        │
        ▼
┌──────────────────┐   Google Places API           ┌──────────────────────────┐
│  Lead Finder     │── enumerate businesses ──────▶ │ data/leads.jsonl (master)│
│  (agent)         │   detect missing `website`     │  dedup by place_id        │
└──────────────────┘   LLM: classify/summarize      │  status: found            │
        │                                           └──────────────────────────┘
        ▼
┌──────────────────┐   Firecrawl / Places photos    enrich SAME records:
│ Lead Prioritizer │── how many photos exist? ─────▶  + photo_rating (1–5)
│  (agent)         │   LLM: reason + rate            + photo_links[] (clickable
└──────────────────┘                                   Google Maps + Yelp URLs)
        │                                            status: prioritized
        ▼
   reports/ (generated, clickable Markdown views)
   ├── (report) AI-Leads.md            ← all found
   └── (report) Prioritized-Leads.md   ← ⭐-sorted, clickable photo links
        │
        ▼
   [ future agents: outreach, website-draft, etc. — TBD ]
```

**Division of labor (critical):** APIs *acquire facts* (does this business have a website? how many
photos?); the **local LLM only *reasons*** (classify industry, dedup fuzzy matches, write summaries,
assign the rating). The LLM is the cheap reasoning labor — never the search engine or the source of
"facts."

---

## 4. Architecture decisions (grill-validated 2026-06-07)

| # | Decision | Choice | Why |
|---|---|---|---|
| 1 | Scope | Lead pipeline only | Websites = separate future repo; this is the hard/new part |
| 2 | Language | **Python** | Ollama-native, agent/scraping ecosystem, 3090 workflows |
| 3 | Orchestration | **Lightweight file-based pipeline** | Simplicity-first (Karpathy); files = inspectable handoff; graduate to LangGraph only if needed |
| 4 | Data format | **JSONL source-of-truth + generated Markdown views** | Agents get reliable structure; humans get clickable files |
| 5 | Acquisition | **Google Places API** + LLM reasoning + Firecrawl enrichment | "Has website?" is a lookup, not an LLM guess |
| 6 | Local AI | **Thin `llm` module**, Ollama OpenAI endpoint, model in config, optional cloud fallback | Model choice deferred = config toggle, not rewrite |
| 7 | Isolation | **Plain processes** v1 | Sandbox earns its keep only for code-execution agents (deferred) |
| 8 | Interface | **Typer CLI** (`find`/`prioritize`/`run`) + `config/targets.yaml` | Matt-friendly; repeatable batch hunts |
| 9 | Storage | **Master `leads.jsonl` keyed by `place_id`**, dedup + status lifecycle | One place to dedup + track status; no file drift |
| 10 | Tree + git | **Approved scaffold; lead data git-tracked** | Sharing leads between Sean+Matt is the point |

**Minor defaults (changeable):**
- Package manager: **`uv`**.
- **Lead schema:** `place_id, name, industry, location, has_website, status, photo_rating,
  photo_links[], google_maps_url, yelp_url, found_date, source`.
- **Status lifecycle:** `found → prioritized → contacted → sold`.
- **Rating:** 1–5 from photo-count thresholds (tune later).
- **Photo links:** save clickable **Google Maps + Yelp business-page URLs** (what you click to view/save
  photos), not raw API photo refs.

---

## 5. Implemented scaffold

The approved scaffold now exists in the repo and is the working baseline for ongoing work:

```
website-builder/
├── pyproject.toml                  # Python project + deps (uv); defines `leadpipe` CLI
├── .env.example                    # GOOGLE_PLACES_API_KEY, FIRECRAWL_API_KEY, LLM_MODEL... (.env gitignored)
├── config/targets.yaml             # areas + industries to hunt
├── src/leadpipe/
│   ├── cli.py                      # Typer CLI: find / prioritize / run
│   ├── pipeline.py                 # thin runner — orders the agents
│   ├── config.py                   # loads .env + targets.yaml
│   ├── models.py                   # Lead schema (pydantic)
│   ├── store.py                    # leads.jsonl read/write + dedup by place_id + status
│   ├── llm.py                      # Ollama OpenAI-compatible client; model from config; cloud fallback
│   ├── sources/
│   │   ├── google_places.py        # enumerate businesses + website/photos
│   │   └── firecrawl.py            # enrichment fallback (REST)
│   ├── agents/
│   │   ├── base.py                 # Agent protocol: run(store) -> store
│   │   ├── lead_finder.py
│   │   └── lead_prioritizer.py
│   └── reports.py                  # render the two markdown views
├── data/leads.jsonl                # master store (git-tracked)
├── reports/                        # generated clickable views (git-tracked)
└── tests/                          # store dedup + agent contract
```

---

## 6. How the reference library informed this
- **Firecrawl** → enrichment fallback (§5 acquisition).
- **Claude Code Router** → the config-driven local/cloud LLM routing (§6).
- **GSD framework** → atomic-task + file-handoff philosophy (§3).
- **Vercel Sandbox** → flagged for future code-executing agents (§7).
- **Karpathy principles** → simplicity-first drove "no framework yet."
- **Net-new (not in library):** Google Places API as the acquisition layer.

---

## 7. Problems / constraints carried forward
- **Firecrawl enrichment depends on active credits/subscription** — Prioritizer handles failures
  gracefully by skipping enrichment and logging the issue rather than fabricating a rating. MCP tools
  load only on session restart; REST remains the mid-session fallback.
- **Local model routing is still a config decision** — the code uses the thin `llm` module and
  Ollama's OpenAI-compatible endpoint, so task-specific model choices can be made without rewriting
  agents.
- **Google Places API requires "Places API (New)"** — a 403 `SERVICE_DISABLED` usually means the
  legacy API was enabled instead of the new one.
- **Docs/memory must stay synchronized** — `AGENTS.md` and `MEMORY.md` are canonical; run
  `context-transfer` at session end.

---

## 8. Status & next steps
- ✅ Architecture approved via `/grill-me`.
- ✅ Scaffold built in `src/leadpipe/` and validated live on real data.
- ✅ Lead Finder and Lead Prioritizer exist behind the Typer CLI (`find`, `prioritize`, `run`,
  `report`).
- ⬜ Finalize local model choices/routing for the current machine setup.
- ⬜ Run real hunts by editing `config/targets.yaml` and using `uv run leadpipe run`.
- ⬜ Build agent #3+ by adding one module under `src/leadpipe/agents/` and registering it in
  `pipeline.STAGES`.
