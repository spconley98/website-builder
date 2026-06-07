# MEMORY.md — website-builder (shared project state)

> Portable, multi-agent state file. **Read on session start, update on session end.** This is the
> shared source of truth for project state across Claude / Codex / Gemini. Constitution lives in
> [`AGENTS.md`](./AGENTS.md).

**Last updated:** 2026-06-07T13:40:00-05:00 · **Last agent:** Gemini (Antigravity) — Matt onboarding verification and model pull
**Phase:** pre-scaffold (architecture APPROVED, app not yet built)

---

## 👤 Contributors
- **Sean** — owner, sole approver. Set up the repo, skills, reference library, NotebookLM brain, MCP.
- **Matt** (mp214gitty / mpitto214@gmail.com) — collaborator. Onboarding complete (invites accepted, local apps/MCP/env set up).

## ✅ What exists now
- GitHub repo (public, shared) + `.gitignore` + `.mcp.json.example`.
- Multi-agent constitution: `AGENTS.md` (canonical), `CLAUDE.md` + `GEMINI.md` (pointers), this file.
- Skills: `context-transfer` (session wrap-up, per-contributor attribution),
  `reference-visualizer` (proactive mind-map/visualization with ask-first + Sean-only pending approvals).
- Reference library `docs/_reference-library/` — 7 docs, each in 3 tiers (Raw Text / Mind Map /
  Visualization). Reference only, NOT the scaffold.
- NotebookLM brain `website-builder-brain` (`bd83690f-e997-46c5-b054-6ff3139e11d6`).
- Firecrawl MCP wired in local `.mcp.json` (key valid, account out of credits; loads on restart).
- Local Ollama model (`qwen2.5:7b`) pulled for Matt's GPU.
- Programmatic NotebookLM CLI (`notebooklm-py`) and Playwright Chromium browser installed for Matt.

## 🔨 In progress
- Nothing actively mid-edit.

## 🚫 Blocked / waiting
- Firecrawl scraping — account out of credits.
- Google Places API (Matt) — key returns `LegacyApiNotActivatedMapError`. Matt needs to enable the legacy "Places API" in his Google Cloud Console.

## ✅ Architecture (approved 2026-06-07 via /grill-me)
Local-AI **lead pipeline** (Python). Lead Finder → Lead Prioritizer → future agents. Google Places API
acquires + detects "no website"; Ollama LLM reasons; Firecrawl enriches. Master `leads.jsonl` (dedup by
place_id) + generated clickable Markdown reports. Typer CLI. Full detail + approved scaffold tree:
[`docs/project/ARCHITECTURE.md`](./docs/project/ARCHITECTURE.md).

## ➡️ Next (do NOT pre-empt — needs Sean's go-ahead)
1. **Build the approved scaffold** (tree in ARCHITECTURE §5) — files/stubs/CLI/schema/config.
2. ~~Sean picks the Ollama model~~ ✅ **Done — `gemma4-fast`** (RTX 3090; secondary: `nomic-embed-text`
   for embedding-based dedup later). **Matt picks his OWN model based on his own GPU** — don't assume
   he mirrors Sean's. `LLM_MODEL` is config-driven (one-line `.env` change either way).
3. ~~Sean + Matt get their own keys~~ ✅ **Both done** — Sean's Google Places key secured locally
   (`.env`, gitignored); Matt's Google Places + Firecrawl keys configured on his end too (Places key verified but blocked on legacy activation).
4. Implement Lead Finder, then Lead Prioritizer.

## 📋 REQUIRED — every session, every contributor
Run the **`context-transfer`** skill at the END of every session (say "wrap up" / "/context-transfer").
It updates this file with a summary + **who did what + timestamp**, syncs the NotebookLM brain, and
syncs Obsidian. **This applies to Matt too — first thing to know after his first `git pull`.**

## Context for next agent
Read `AGENTS.md` → this file → `docs/project/ARCHITECTURE.md`. Matt's onboarding is complete (git pull verified, Ollama model `qwen2.5:7b` pulled, Google key tested). The legacy Google Places API needs to be enabled for Matt's key to work. Scaffold is the next build step but **must wait for Sean's approval** to start. Matt onboarding: `docs/project/ONBOARDING_MATT.md`.
