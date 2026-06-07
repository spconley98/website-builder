# MEMORY.md — website-builder (shared project state)

> Portable, multi-agent state file. **Read on session start, update on session end.** This is the
> shared source of truth for project state across Claude / Codex / Gemini. Constitution lives in
> [`AGENTS.md`](./AGENTS.md).

**Last updated:** 2026-06-07 · **Last agent:** Claude Sonnet 4.6 — architecture via /grill-me
**Phase:** pre-scaffold (architecture APPROVED, app not yet built)

---

## 👤 Contributors
- **Sean** — owner, sole approver. Set up the repo, skills, reference library, NotebookLM brain, MCP.
- **Matt** (mp214gitty / mpitto214@gmail.com) — collaborator. **Pending:** accept GitHub invite,
  accept NotebookLM share, install Obsidian.

## ✅ What exists now
- GitHub repo (public, shared) + `.gitignore` + `.mcp.json.example`.
- Multi-agent constitution: `AGENTS.md` (canonical), `CLAUDE.md` + `GEMINI.md` (pointers), this file.
- Skills: `context-transfer` (session wrap-up, per-contributor attribution),
  `reference-visualizer` (proactive mind-map/visualization with ask-first + Sean-only pending approvals).
- Reference library `docs/_reference-library/` — 7 docs, each in 3 tiers (Raw Text / Mind Map /
  Visualization). Reference only, NOT the scaffold.
- NotebookLM brain `website-builder-brain` (`bd83690f-e997-46c5-b054-6ff3139e11d6`).
- Firecrawl MCP wired in local `.mcp.json` (key valid, account out of credits; loads on restart).

## 🔨 In progress
- Nothing actively mid-edit.

## 🚫 Blocked / waiting
- Firecrawl scraping — account out of credits.
- Matt — onboarding acceptances pending.

## ✅ Architecture (approved 2026-06-07 via /grill-me)
Local-AI **lead pipeline** (Python). Lead Finder → Lead Prioritizer → future agents. Google Places API
acquires + detects "no website"; Ollama LLM reasons; Firecrawl enriches. Master `leads.jsonl` (dedup by
place_id) + generated clickable Markdown reports. Typer CLI. Full detail + approved scaffold tree:
[`docs/project/ARCHITECTURE.md`](./docs/project/ARCHITECTURE.md).

## ➡️ Next (do NOT pre-empt — needs Sean's go-ahead)
1. **Build the approved scaffold** (tree in ARCHITECTURE §5) — files/stubs/CLI/schema/config.
2. Sean picks the **Ollama model**.
3. Sean + Matt get their **own** Google Places + Firecrawl keys.
4. Implement Lead Finder, then Lead Prioritizer.

## Context for next agent
Read `AGENTS.md` → this file → `docs/project/ARCHITECTURE.md`. Architecture is locked; scaffold is the
next build step but **must wait for Sean's approval** to start. Matt onboarding: `docs/project/ONBOARDING_MATT.md`.
