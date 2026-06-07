# Onboarding — Matt

> ## READ FIRST — current status
> The initial scaffold is built and validated live. This repo now contains the working `leadpipe`
> Python CLI in `src/leadpipe/`. Your setup goal is to get local tools, keys, and model config ready
> so you can run the same pipeline and contribute future agents safely.

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
      GPU for real speed (Sean runs an RTX 3090). Model choice lives in your local `.env`, so you can
      use a model that fits your hardware once Sean settles the current routing plan.
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
- [ ] Run `uv sync --group dev`.
- [ ] Run `uv run pytest tests/ -q` and expect the core scaffold tests to pass.
- [ ] Run `uv run leadpipe --help` to confirm the CLI is available.

### Before every work session — sync safely
Before your agent edits anything, have it check whether your local copy is stale:

```powershell
git status --short --branch
git fetch origin
git log --oneline HEAD..origin/main
git log --oneline origin/main..HEAD
```

If you have no local edits and you are behind, run:

```powershell
git pull --ff-only
uv sync --group dev
uv run pytest tests/ -q
```

If you do have local edits, your agent should preserve them first on a Matt branch or Matt-attributed
WIP commit, then reconcile with `origin/main`. It should never reset, overwrite, or delete your local
work just to make a pull succeed. After any pull/rebase/merge, re-read `AGENTS.md` + `MEMORY.md`
because Sean may have updated the project rules.

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
      `context-transfer` + `reference-visualizer`. Nothing to install for those — **for Claude Code.**
- [ ] **You use Gemini — it needs separate one-time setup** (Gemini doesn't read `.claude/skills/`
      or `.mcp.json` natively). Run these once, pointing at YOUR clone path + YOUR OWN Firecrawl key:
      ```powershell
      gemini skills link "<your-clone-path>\.claude\skills\context-transfer" --scope workspace --consent
      gemini skills link "<your-clone-path>\.claude\skills\reference-visualizer" --scope workspace --consent
      gemini mcp add firecrawl npx -y firecrawl-mcp -e "FIRECRAWL_API_KEY=<your-own-key>" --scope user
      ```
      Verify: `gemini skills list` shows both; `gemini mcp list` shows `firecrawl ... Connected`.
      Full detail: `GEMINI.md`.
- [ ] For more skills, see `docs/_reference-library/(Raw Text) Master_Skills_Catalog.md` — it lists
      what to pull from Anthropic / VoltAgent repos with copy-paste install commands. Keep new
      project tooling deliberate and aligned with `AGENTS.md`.

---

## Shared-resource rule — attach your name
The **NotebookLM brain is the one shared resource** (everything else = your own keys/machine). **When
your agent adds anything to the brain** (a source, a note, a generated artifact), **attach your name** —
title sources like `[Matt] <doc>` and note that Matt contributed. This keeps our shared brain's
provenance clear (same per-contributor rule the `context-transfer` skill uses for `MEMORY.md`).

---

## ⚠️ THE ONE HABIT TO LOCK IN — run `context-transfer` at the END of every session

This is **mandatory for both of us, every single session** — say "wrap up" or "/context-transfer"
to your agent before you close out. It:
1. Updates `MEMORY.md` with a session summary **tagged with your name + a timestamp**.
2. Syncs the shared NotebookLM brain (with the `[Matt]` attribution from the rule above).
3. Reflects in the Obsidian vault.
4. Commits everything.

**Why it matters:** with two of us and three different AI agents in play, this is the *only* thing
keeping everyone — you, me, Claude, Codex, Gemini — on the same page about who did what and when.
Skip it and the next session (yours, mine, or an agent's) starts blind. Even a 10-minute session —
run it. No exceptions.

---

## Your "ready" checklist
You're set up when: invites accepted ✓, apps installed ✓, repo cloned ✓, `.env` + `.mcp.json` created
with your keys ✓, you've read `AGENTS.md` + `MEMORY.md` + `ARCHITECTURE.md` ✓, tests pass ✓, and
`uv run leadpipe --help` works ✓. Then coordinate with Sean on target hunts or the next agent.
