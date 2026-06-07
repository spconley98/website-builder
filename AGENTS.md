# AGENTS.md — website-builder Constitution

> **This is the canonical front door for every agent (Claude Code, OpenAI Codex, Gemini) and every
> human working on this project.** Read this first, then read `MEMORY.md` for current state.
> `CLAUDE.md` and `GEMINI.md` are thin pointers back to this file — update THIS file, not those.

---

## 0. Status & the one hard rule

**Phase:** pre-scaffold. Project conventions, skills, memory, and reference material are established —
but the actual application scaffolding (framework, app structure, tooling) has **not** been built yet.

> 🚫 **HARD RULE — do NOT build project scaffolding yet.** The scaffold will be designed in a dedicated
> session where Sean provides full project context and we run `/grill-me` to pressure-test the
> structure against the reference library. Until that session produces an approved scaffold, do not
> create app folders, pick a framework, or generate boilerplate. If asked to "start building," confirm
> the grill-me scaffolding session has happened first.

This document is an **evolving rough draft** — it will gain detail (especially the project vision) over
time. Keep it current.

---

## 1. What this project is

`website-builder` — a **local-AI lead pipeline**: finds local businesses with **no website**,
prioritizes them by available online photos (Yelp/Google), outputs clickable lead lists so Sean + Matt
can build + sell them websites. Local AI (Ollama/RTX 3090) does the research grunt-work. Website
*building* itself is a separate future repo. **Full architecture: [`docs/project/ARCHITECTURE.md`](./docs/project/ARCHITECTURE.md).**
Treat the reference library as inspiration, not the spec.

---

## 2. Contributors & roles

| Person | Role | Identities |
|---|---|---|
| **Sean** | Owner, sole approver | GitHub `spconley98`, spconley98@gmail.com |
| **Matt** | Collaborator | GitHub `mp214gitty` = NotebookLM `mpitto214@gmail.com` = "Matt" |

- **Only Sean approves** pending items (see reference-visualizer queue, §4).
- Default work attribution is **Sean** unless the conversation names Matt.
- **Pending onboarding for Matt** (track until confirmed): GitHub collaborator invite (write access),
  NotebookLM `website-builder-brain` share, and installing **Obsidian** to use the project vault.

---

## 3. Operating principles (Karpathy)

Apply on every task:
1. **Data first** — define data structures before logic.
2. **Surgical changes** — modify only what was explicitly requested; don't touch unrelated code.
3. **Simplicity first** — minimal logic, no speculative abstractions.
4. **Goal-driven** — measure every change against the project's North Star.
5. **Per-task rhythm** — explore → plan → code → commit. Never skip a step.

---

## 4. Repo conventions

### Reference library — `docs/_reference-library/`
**Reference ONLY. NOT the project scaffold.** A curated library of ideas/tools/frameworks Sean gathered
(AI Build Bible, Custom SDKs Bible, Comprehensive_* guides, Master Skills Catalog). Listing a tool here
is **not** a decision to use it. Each doc has three tiers:
- `(Raw Text) <name>.md` — source text
- `(Mind Map) <name>/<name>.md` — NotebookLM mind map as nested bullets (Obsidian Markmap-friendly)
- `(Visualization) <name>/<name>.png` — NotebookLM infographic

### Skills (`.claude/skills/`)
- **`reference-visualizer`** — when a new doc is added to the reference library, it **proactively
  offers** (asks first, never auto-generates) to build the `(Mind Map)` + `(Visualization)` tiers.
  Response branches: **Yes** → generate · **No** → skip · **Unsure** (e.g. Matt) → log to
  `docs/_reference-library/_PENDING_APPROVALS.md` for **Sean's** approval. Only Sean processes the queue.
- **`context-transfer`** — session wrap-up: health check, update `MEMORY.md` (with **per-contributor
  attribution**), upload to the NotebookLM brain, commit. Run it at the end of a work session.
- Full menu of available + recommended skills: `docs/_reference-library/(Raw Text) Master_Skills_Catalog.md`.

---

## 5. Memory & knowledge

- **`MEMORY.md` (repo root)** — the **portable, multi-agent state file**. Every agent reads it on start
  and updates it on end. This is the shared source of truth for project state (Codex/Gemini included).
- **Claude private memory** — Claude Code also keeps notes under
  `.claude/projects/.../memory/`. That is Claude-specific and **not** a substitute for root `MEMORY.md`.
- **NotebookLM brain** — `website-builder-brain`, ID `bd83690f-e997-46c5-b054-6ff3139e11d6`. Holds
  reference sources + generated mind-maps/infographics. Shared with Matt. **It is the one shared
  resource** (all API keys are per-person). 🏷️ **When any agent adds to the brain** (source, note,
  artifact), **attach the contributor's name** — title sources `[<Name>] <doc>` and attribute the
  contribution. Keeps shared-brain provenance clear (same per-contributor rule as `context-transfer`).
- **Obsidian vault** — opens on the project folder; visual map of structure/themes. Matt must install
  Obsidian to use it.

---

## 6. Tooling / MCP

- **Firecrawl MCP** — configured in local `.mcp.json` (gitignored). New collaborators copy
  `.mcp.json.example` → `.mcp.json` and add their own key.
  - MCP tools (`mcp__firecrawl__*`) load **only on a session restart** — not mid-session.
  - **Mid-session fallback:** hit the REST API directly —
    `POST https://api.firecrawl.dev/v1/search` `{"query":"...","limit":N}` /
    `POST https://api.firecrawl.dev/v1/scrape` `{"url":"...","formats":["markdown"]}`,
    header `Authorization: Bearer <key>`.
  - ⚠️ Account is currently **out of credits** — scrapes return "Insufficient credits" until topped up.
- **NotebookLM CLI** — `py -m notebooklm ...` (auth at `C:\Users\mysis\.notebooklm\storage_state.json`).

---

## 7. Git & secrets

- Repo: https://github.com/spconley98/website-builder (public, shared with Matt).
- Branch off `main` for work; don't commit straight to `main` without reason.
- Commit format: `[PHASE][AREA] Description` (e.g. `[0][setup] Add multi-agent constitution`).
- 🔒 **NEVER commit** `.mcp.json`, `.env*`, `*.key`, or `storage_state.json` — already in `.gitignore`.

---

## 8. Session protocol

**Start:** read `AGENTS.md` (this file) → `MEMORY.md` → check for pending approvals/onboarding.

**End — MANDATORY for every contributor (Sean AND Matt), every session:** run the `context-transfer`
skill ("wrap up" / "/context-transfer"). It updates `MEMORY.md` with a summary **tagged with
contributor name + timestamp**, syncs the NotebookLM brain (remember the `[<Name>]` attribution rule
in §5), reflects in Obsidian, and commits. Skipping it means the next session starts blind — do it
every time, even short sessions.
