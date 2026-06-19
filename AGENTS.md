---
type: project
contributors: [sean]
status: active
created: 2026-06-07
updated: 2026-06-10
topic: constitution
tags: [canon]
---

# AGENTS.md — website-builder Constitution

> **This is the canonical front door for every agent (Claude Code, OpenAI Codex, Gemini) and every
> human working on this project.** Read this first, then read `MEMORY.md` for current state.
> `CLAUDE.md` and `GEMINI.md` are thin pointers back to this file — update THIS file, not those.

---

## 0. Status

**Phase: scaffold BUILT and validated live.** ✅ The architecture was approved via `/grill-me`
(2026-06-07) and the `leadpipe` package now exists in `src/leadpipe/` — a working Python CLI that
runs end-to-end on real data (see `MEMORY.md` "What exists now" for the live validation result:
it found a real business with no website and produced a clickable report).

**The original "don't scaffold yet" gate is LIFTED — that was for the initial build, which is done.**
Pick this project up and run with it: `MEMORY.md` has a "How to pick this up cold" section with the
exact commands (`uv sync`, `uv run pytest`, `uv run leadpipe ...`).

What's still open is normal ongoing work, not a gate: real hunts (`config/targets.sean.yaml` /
`config/targets.matt.yaml`), topping up Firecrawl credits, building further agents. None of that
requires a special approval session — just
follow the established pattern (one module in `agents/`, one line in `pipeline.STAGES`, cross-challenge
non-trivial logic via `three-brain` per §3/feedback memory before/while building).

This document is an **evolving rough draft** — it will gain detail (especially the project vision) over
time. Keep it current.

---

## 1. What this project is

`website-builder` — a **local-AI lead pipeline**: finds local businesses with **no website** via Google
Places API, scores each on buildability + reachability (`photo_count`, `phone_present`,
`recent_review_count`, `hours_present`, `staleness_flags` as soft penalties — never hard excludes), and
outputs clickable lead lists ranked by score. Output is a **qualified-leads feeder for a future separate
website-build/sell repo** — leadpipe itself does not do site building, templates, pricing, CRM, or
outreach automation. Local AI (Ollama) does the research grunt-work. Scope locked: no-website-only (no
outdated-site/SEO tiers), Google Places only (no Yelp/directories/social scraping). **Full architecture:
[`docs/project/ARCHITECTURE.md`](./docs/project/ARCHITECTURE.md).**
Treat the reference library as inspiration, not the spec.

---

## 2. Contributors & roles

| Person | Role | Identities |
|---|---|---|
| **Sean** | Owner, sole approver | GitHub `spconley98`, spconley98@gmail.com |
| **Matt** | Collaborator | GitHub `mp214gitty` = NotebookLM `mpitto214@gmail.com` = "Matt" |

- **Only Sean approves** pending items (see reference-visualizer queue, §4).
- Default work attribution is **Sean** unless the conversation names Matt.
- **Matt onboarding/sync status is mutable state — it lives in `MEMORY.md` (per the Authority model in
  §5), not here.** Don't hardcode a status in this file; read `MEMORY.md` for the current state.

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
- **`wb-context-transfer`** — session wrap-up: health check, write a contributor-owned handoff under
  `docs/session-logs/<sean|matt>/`, update `MEMORY.md` only when protocol allows, upload to the
  NotebookLM brain, commit. Run it at the end of a work session.
- Full menu of available + recommended skills: `docs/_reference-library/(Raw Text) Master_Skills_Catalog.md`.

### Skill set for this project (business lead pipeline)
This is a lead-pipeline app, not a marketing/design site — design/genmedia skills (aas-design,
aas-section-builder, aas-seo-content, frontend-design, impeccable, ui-ux-pro-max, fal-*, marketing,
ugc, storytelling, etc.) are **not relevant** and should not be invoked here. Relevant skills:
- `vercel:*` (nextjs, deploy, env-vars, vercel-storage, ai-sdk for any LLM enrichment/scoring)
- `run`, `verify`, `code-review`, `simplify`, `security-review`
- `wb-context-transfer`, `three-brain`, `grill-me`
- `caveman:*`
- `claude-api` (if calling an LLM for lead enrichment/scoring)
- `website-intelligence` (if scraping/researching lead sources)

---

## 5. Memory & knowledge — the Obsidian agent brain

The repo **is** an Obsidian vault, and that vault is the **primary** brain (source of truth + agent
working memory); NotebookLM is a downstream **mirror**. To keep a cold agent's onboarding cheap AND safe,
every "current truth" has exactly ONE owner plus a degradation rule — never create competing authorities.

### Authority model
| Concern | Source of truth | Derived / non-authoritative | Degradation rule |
|---|---|---|---|
| Rules / protocol | **`AGENTS.md`** (this file) | `CLAUDE.md` / `GEMINI.md` pointers | read first, always |
| Current state | **`MEMORY.md`** | `_HOT.md` (generated digest) | `_HOT.md` is stamped `generated` + `stale_after`; if expired, fall back to `MEMORY.md` |
| Per-project focus | latest session log | `docs/_working-context/<proj>.md` (generated) | regenerated at wrap-up |
| History | dated `docs/session-logs/**` | — | append-only |
| Cloud mirror | **`MEMORY.md` only** (NotebookLM) | — | one canonical current-state source; retire/rename stale |

Mutable state (Matt onboarding/sync status, what's in progress, blockers) lives in **`MEMORY.md`** — never
hardcode it into this file or any other "current-truth" surface.

### Cold-start read-path (AGENTS first; each file is small → seconds, few tokens)
1. `AGENTS.md` — rules / safety (authority on protocol)
2. `_HOT.md` — generated ~500-word digest: current state + active tasks + blockers `[stale_after]`
3. `_HOME.md` — navigation index → MOCs, Bases, spine docs
4. `docs/_working-context/<proj>.md` — current domain focus (generated)
5. `past_mistakes.md` — known bugs/hallucinations to not repeat
6. `MEMORY.md` — canonical deep state (authority on state)

`_HOT.md`, `docs/_working-context/*`, and `_HOME.md` are **generated/maintained by `leadpipe vault` (§6)**
— do not hand-edit `_HOT.md`. They are conveniences; if any disagrees with `MEMORY.md`, `MEMORY.md` wins.

### Knowledge graph (graphify) — query before you grep
A persistent knowledge graph of this whole repo (code + docs + research + visuals) lives in
`graphify-out/`. Use it to answer "how/where/what-connects" questions for **~10x fewer tokens** than
grepping or reading files cold:
- **`graphify query "<question>"`** — traverses the graph, returns the relevant slice + `source_location`
  citations. Try this *before* fanning out reads across the repo.
- **`graphify-out/GRAPH_REPORT.md`** — the map: god nodes (core abstractions), community labels,
  surprising connections, and the questions the graph is best at answering. Read this to orient fast.
- **`graphify-out/graph.json`** — raw graph (committed, so a fresh clone has it without rebuilding).
- **`graphify-out/bridges.json` + `apply_bridges.py`** — curated doc↔code edges that re-stitch the
  strategy docs (e.g. `SELL_METHODOLOGY.md`) to the code that embodies them (`website_intelligence.py`).
  The graph is **rebuilt** by `/graphify` (or `graphify ... --update`), which **overwrites `graph.json`** —
  so after any rebuild, re-run `python graphify-out/apply_bridges.py` to re-apply the bridges.
The graph is a convenience derived from the repo; if it disagrees with the source files, the **source wins**.

### Note metadata — frontmatter schema (enforced by `leadpipe vault validate`)
Every hand-written note carries YAML frontmatter (2-space indent; **omit** optional fields rather than
leave them blank — an empty date breaks Bases filters; single-token keys; no nested properties; no
Markdown in values, because Obsidian assigns one global type per property name):
```yaml
---
type: session-log        # session-log|research|reference|moc|project|report|context
contributors: [sean]     # LIST always (even for one)
agent: codex             # claude|codex|gemini
status: active           # active|draft|archived|superseded
created: 2026-06-09
updated: 2026-06-09
topic: short-kebab-topic
tags: [sessions]
related: ["[[MEMORY]]"]
---
```
RAG-friendly authoring (front-loaded summary, atomic 200–400 words, strict heading hierarchy) applies
**only to new research / working-context notes**. Canon (this file, `MEMORY.md`, `ARCHITECTURE.md`,
session logs, generated reports) stays as long as it needs to be.

### Other brains
- **Claude private memory** — `.claude/projects/.../memory/`. Claude-only; **not** a substitute for root `MEMORY.md`.
- **NotebookLM brain** — `website-builder-brain`, ID `bd83690f-e997-46c5-b054-6ff3139e11d6`. Mirrors
  **`MEMORY.md` only** as the single current-state source, plus reference mind-maps/infographics. Shared
  with Matt (**the one shared resource**; all API keys are per-person). 🏷️ Every upload carries
  contributor + timestamp + topic — `MEMORY.md` as `[<Name>] MEMORY.md - YYYY-MM-DD HHMM - <topic>`,
  other items as `[<Name>] <doc/topic>`; use `[Unknown] ... - needs-review` only when authorship can't be
  proven. **Do not mirror `_HOT.md`** (it's a local generated digest — mirroring it would create a second
  conflicting "current state" in the brain).

### Reciprocal routing — when Codex (or Gemini) is the active driver
Claude's `three-brain` command (`~/.claude/commands/three-brain.md`) routes Claude→Codex/Gemini. The
mirror applies when **Codex is the driver** in this repo (e.g. invoked via `codex exec` directly, or as
Matt/Sean's active agent):

- **Stuck / 2x same failure** (same test fail, same error, same edit re-tried with no progress) →
  hand off to Claude: `git diff | claude -p "rescue: <task>. Codex tried 2x and failed. Full context attached."`
  (or equivalent Claude Code CLI invocation). Announce before handing off, one line.
- **User asks Codex to "check/review/sanity-check your own output"** → same no-self-review law as
  three-brain: route to Claude for an independent pass rather than reviewing its own diff.
- **Risk-path edits** (`src/auth/**`, `src/billing/**`, `**/migrations/**`, `**/deploy/**`, `**/.env*`,
  `**/secrets/**`, `**/policy/**`, `infra/**`) → forced second-opinion from Claude before saying "done."
- **Long media / whole-repo scans** → Gemini, same as three-brain (`gemini -p "..." @file`,
  `/cc-gemini-plugin:gemini --dirs <paths> "..."`).
- Output filing + `./three-brain-out/log.md` convention applies regardless of which agent drives.

This keeps the no-self-review guarantee no matter which CLI (Claude, Codex, Gemini) is in the driver's
seat for a given session.

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
- **Obsidian vault maintenance — `leadpipe vault`** (repo-native, pure Python/uv; **no** Obsidian or
  Claude-skill dependency, so Sean AND Matt/Gemini can run the mandatory loop identically):
  - `uv run leadpipe vault validate` — assert allowlisted notes match the §5 frontmatter schema (non-zero exit on violations)
  - `uv run leadpipe vault heartbeat` — sweep for broken `[[wikilinks]]`, orphans, stale `updated`, malformed YAML (report-only, no silent edits)
  - `uv run leadpipe vault hot` — regenerate `_HOT.md` from `MEMORY.md` + latest session log (deterministic; stamps `generated`/`stale_after`)

### Obsidian plugin & vault security (non-negotiable)
- A vault's `.obsidian/` is an **executable trust boundary** — a real campaign (REF6598) hid a
  PHANTOMPULSE RAT in `.obsidian/plugins/<x>/data.json`. So **never git-track or sync `.obsidian/plugins/`,
  `.obsidian/community-plugins.json`, or workspace state** (see `.gitignore`). A reviewed `core-plugins.json`
  may stay tracked so Bases/Properties are enabled on a fresh clone.
- **Restricted Mode ON; community-plugin sync OFF.** Install only vetted, popular OSS plugins — locally,
  per person. **No shell / network / JS-executing plugins** (Shell Commands is banned). Templater is
  allowed only with "no user scripts / no system-command functions / no unreviewed templates", and is
  **never required** for repo correctness — repo health depends on `leadpipe vault`, not on any plugin.
- kepano `obsidian-skills` and all Obsidian plugins are **optional per-person UX helpers**, never a
  dependency of the mandatory session protocol (Matt runs Gemini and won't have the Claude-Code skills).

### Agent run safety
- **No autonomous scraping by default.** Local agents must not run Firecrawl-backed enrichment or
  scheduled scraping unless Sean explicitly prompts for that run or a committed schedule says so.
- **Default lead acquisition cap: 20 candidates per request.** Finder commands default to 20 Google
  Places candidates per industry; raise it only by explicit prompt/CLI flag.
- **Profiles isolate writers:** Sean agents write `data/sean/leads.jsonl`; Matt agents write
  `data/matt/leads.jsonl`. Shared Obsidian visibility comes from generated reports, not a shared
  writable store.
- **No hard deletes from automation.** Agents may mark leads `invalid`/`archived`; shared reports hide
  those by default while preserving recovery/audit history.

### Hunt operations
- **Hunt rhythm:** before any real acquisition run, check `git status --short --branch`, confirm the
  active profile/targets, run `leadpipe check` (add `--google` before a new Places hunt), then run
  `find` first. Only run Firecrawl-backed `prioritize`, `run`, or `intelligence` when Sean explicitly
  asked for that spend and the CLI includes `--use-firecrawl`.
- **Territory coordination:** active territory claims live in `MEMORY.md`, not ad hoc notes. If a task
  changes who is hunting which areas/industries, update `MEMORY.md` only during an explicit state update
  or context-transfer wrap-up. Default current territory is Sean = Northern California; Matt must choose
  targets before `config/targets.matt.yaml` is populated.
- **Post-hunt sync:** after any hunt that changes `data/<profile>/leads.jsonl`, regenerate profile and
  shared reports immediately, run tests/health checks, write the session handoff, and push or otherwise
  preserve the data/report diff before another collaborator starts a hunt. Cross-profile dedup only works
  when `data/` and `reports/` are current.
- **Website Brief review:** `leadpipe intelligence` produces draft build/sales judgment, not cleared
  outreach copy. A human (Sean by default) or a routed second LLM review must approve Website Briefs
  before they are used for sales outreach.

### Token & context economy (adopted standards)
Two rules are canon; the full (reference-only) playbook + rationale lives in
[`docs/_reference-library/(Raw Text) Token_and_Context_Economy.md`](./docs/_reference-library/(Raw%20Text)%20Token_and_Context_Economy.md).
- **Patch, don't rewrite.** Edit via minimal targeted diffs (Claude `Edit`, Gemini/Antigravity patch
  edits) — never regenerate a whole file to change a few lines. Output tokens are the costlier, slower
  bottleneck in agentic coding.
- **Exclusion guardrails.** Never read or `cat` build artifacts, `uv.lock`, or `data/**/*.jsonl` into
  context. `.geminiignore` + `.aiexclude` (both git-tracked) enforce this for Gemini/Antigravity. Claude
  Code has no read-ignore, so it's behavioral: surgical reads + grep-before-read, never slurp data dumps.
  These ignore lists are **deliberately broader than `.gitignore`** — `uv.lock` and the lead JSONLs stay
  git-tracked but must not enter a prompt (git-ignore ≠ AI-context-exclude).

---

## 7. Git & secrets

- Repo: https://github.com/spconley98/website-builder (public, shared with Matt).
- Branch off `main` for work; don't commit straight to `main` without reason.
- Commit format: `[PHASE][AREA] Description` (e.g. `[0][setup] Add multi-agent constitution`).
- 🔒 **NEVER commit** `.mcp.json`, `.env*`, `*.key`, or `storage_state.json` — already in `.gitignore`.

### Stale working-copy protocol
When Matt or Matt's agent starts work, pulls, or notices the local repo is behind `origin/main`, the
agent must pause feature work and reconcile safely before editing pipeline code.

Required checks:
1. Run `git status --short --branch`.
2. Run `git fetch origin`.
3. Compare local vs remote with `git log --oneline HEAD..origin/main` and
   `git log --oneline origin/main..HEAD`.

If Matt has no local edits and is behind, update with `git pull --ff-only`, then run `uv sync --group dev`
and `uv run pytest tests/ -q`. Re-read `AGENTS.md` + `MEMORY.md` after the pull because the rules may
have changed.

If Matt has local edits, the agent must **not overwrite, reset, or discard them**. It should identify
the files, summarize what changed, then preserve the work on a Matt branch or Matt-attributed WIP
commit before rebasing/merging remote changes. If conflicts appear, resolve them in favor of the
newer project protocol (`AGENTS.md`/`MEMORY.md`) while preserving Matt's intended feature work. Run
tests after reconciliation and regenerate reports only when the task actually touched lead data or
report logic.

### Selective import protocol for Matt work
If Sean only wants Matt's context transfer and agent research, do **not** pull or merge Matt's whole
branch into `main`. Fetch and inspect first:

```powershell
git fetch origin
git status --short --branch
git diff --name-only main..origin/<matt-branch>
```

Allowed to import from Matt automatically:
- `docs/session-logs/matt/`
- `docs/research/matt/`
- `data/matt/`
- Matt-owned generated reports, when report generation is the stated task

Requires Sean review before import/merge:
- `AGENTS.md`, `MEMORY.md`, `CLAUDE.md`, `GEMINI.md`
- `src/`, `tests/`, `config/`, `pyproject.toml`, `uv.lock`
- `.github/`, `.claude/skills/`, `.gemini/`
- `docs/project/` architecture/scaffold docs

Matt's agent should write session context to `docs/session-logs/matt/` and research to
`docs/research/matt/` by default. Matt's agent must not rewrite shared `MEMORY.md` or project
protocol files unless Sean explicitly asks for that exact change. This keeps Matt's work visible to
Sean without letting an older local framework accidentally replace current scaffold or agent rules.

### Session-log location rule
All session logs, wrap-ups, and context-transfer handoffs must live under:

```text
docs/session-logs/sean/YYYY-MM-DD-HHMM-short-topic.md
docs/session-logs/matt/YYYY-MM-DD-HHMM-short-topic.md
```

Do not create new session logs under `docs/project/`, `docs/research/`, daily-note roots, or ad hoc
folders. All new agent/human handoffs must use `docs/session-logs/<contributor>/`.

---

## 8. Session protocol

**Start:** run **`uv run leadpipe vault catch-up`** — the executable cold-start briefing (prints the
current `_HOT.md` digest + live local git state + top gotchas in one shot; add `--sync-check` to compare
against `origin`, `--fetch` to refresh remote refs first). It is a non-authoritative *printer* over the
existing generated `_HOT.md`, not a second state surface. The manual read-path in §5 (`AGENTS.md` →
`_HOT.md` → `_HOME.md` → `docs/_working-context/<proj>.md` → `past_mistakes.md` → `MEMORY.md`) is the
fallback when `uv`/Python is unavailable. Then check for pending approvals/onboarding.

**End — MANDATORY for every contributor (Sean AND Matt), every session:** run the `wb-context-transfer`
skill ("/wb-context-transfer" — **not** the bare `/context-transfer`, which resolves to a global
AAS-WEBSITE skill pointed at the wrong project brain). It runs the health check (`uv run pytest tests/ -q` — this is a
Python/uv project, not npm), writes a contributor-owned handoff under `docs/session-logs/<sean|matt>/`,
regenerates the brain spine (`uv run leadpipe vault hot` + `uv run leadpipe vault heartbeat`), updates
shared `MEMORY.md` only when allowed by the protocol above, mirrors **`MEMORY.md` only** to the NotebookLM
brain (`[<Name>] MEMORY.md - YYYY-MM-DD HHMM - <topic>` per §5), and commits. Skipping it means the next
session starts blind — do it every time, even short sessions.
