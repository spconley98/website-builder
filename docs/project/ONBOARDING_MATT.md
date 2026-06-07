# Onboarding — Matt

> ## 🚫 READ FIRST — do NOT build anything yet
> This project is **pre-scaffold**. Your only job right now is **environment setup** (the checklist
> below). **Do not write app code, create the project structure, or start agents** until **Sean
> approves** the scaffold. The architecture is approved but Sean drives the build start. If unsure,
> ask Sean — when in doubt, default to "not yet."

Welcome. This gets your machine ready so you and Sean can build together. Assumes you've **linked up a
few skills already**. Work top to bottom.

---

## What this project is (60 seconds)
A **local-AI lead pipeline**: it finds local businesses with **no website**, rates them by how much
photo material exists online (Yelp/Google), and outputs clickable lead lists. We then build + sell
those businesses a website. Local AI (Ollama) does the research grunt-work. Full detail:
[`ARCHITECTURE.md`](./ARCHITECTURE.md). The constitution every agent follows: [`../../AGENTS.md`](../../AGENTS.md).

---

## Step 1 — Accept your invites
- [ ] **GitHub** — accept the collaborator invite to `spconley98/website-builder` (check email /
      https://github.com/spconley98/website-builder/invitations). Gives you write access.
- [ ] **NotebookLM** — accept the share for the **`website-builder-brain`** notebook (Sean sent it to
      `mpitto214@gmail.com`).

## Step 2 — Install the apps
- [ ] **Git** + **GitHub CLI** (`gh`) — clone + auth (`gh auth login`).
- [ ] **Python 3.12+** and **`uv`** (our package manager) — https://docs.astral.sh/uv/
- [ ] **Ollama** — https://ollama.com — this runs the **local AI** on your machine. You need your own
      GPU for real speed (Sean runs an RTX 3090). Don't pull a specific model yet — **Sean picks the
      model**; you'll `ollama pull <that-model>` once decided.
- [ ] **Obsidian** — https://obsidian.md — then **Open folder as vault** → select your cloned
      `website-builder` folder. This is our shared visual brain. Start at **`_HOME.md`**.
- [ ] **VS Code** (or your editor) with the Claude Code / Codex / Gemini extension you use.

## Step 3 — Clone + look around
```bash
gh repo clone spconley98/website-builder
cd website-builder
```
- [ ] Read **`AGENTS.md`** (the constitution — every agent reads this first).
- [ ] Read **`MEMORY.md`** (current state).
- [ ] Skim **`docs/project/ARCHITECTURE.md`** (the plan) and the visuals in `docs/project/visuals/`.

## Step 4 — Your API keys (you get your OWN — do not share/commit)
We each use our **own** keys. They live in a local `.env` (gitignored — never committed).
- [ ] **Google Places API key** — Google Cloud Console → enable Places API → create key. (Cheap /
      free-tier. This is how we find businesses + detect "no website.")
- [ ] **Firecrawl key** — https://firecrawl.dev — for web enrichment. (Note: the shared usage has hit
      credit limits before; your own key avoids collisions.)
- [ ] Copy the template: `cp .mcp.json.example .mcp.json` → paste **your** Firecrawl key.
- [ ] **Restart** Claude Code after creating `.mcp.json` — MCP tools only load on restart (mid-session
      they won't appear; use the Firecrawl REST API directly if you need it before restarting).

## Step 5 — Skills
- [ ] Project skills travel in the repo (`.claude/skills/`) — `git pull` and you have
      `context-transfer` + `reference-visualizer`. Nothing to install for those.
- [ ] For more skills, see `docs/_reference-library/(Raw Text) Master_Skills_Catalog.md` — it lists
      what to pull from Anthropic / VoltAgent repos with copy-paste install commands. **Don't add
      project tooling/skills mid-build without Sean's ok.**

---

## Shared-resource rule — attach your name
The **NotebookLM brain is the one shared resource** (everything else = your own keys/machine). **When
your agent adds anything to the brain** (a source, a note, a generated artifact), **attach your name** —
title sources like `[Matt] <doc>` and note that Matt contributed. This keeps our shared brain's
provenance clear (same per-contributor rule the `context-transfer` skill uses for `MEMORY.md`).

---

## Your "ready" checklist
You're set up when: invites accepted ✓, apps installed ✓, repo cloned ✓, `.env` + `.mcp.json` created
with your keys ✓, you've read `AGENTS.md` + `ARCHITECTURE.md` ✓. Then ping Sean — and **wait for his
go-ahead** before building anything past this setup.
