---
type: moc
contributors: [sean]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: home-index
tags: [moc, index]
related: ["[[AGENTS]]", "[[MEMORY]]", "[[_HOT]]"]
---

# 🏠 website-builder — Home

> Master navigation index for **Sean**, **Matt**, and any agent. Open in Obsidian; use Graph view to see
> how it all connects.

**Project in one line:** a local-AI pipeline that finds local businesses with no website, prioritizes them
by available photos, so we can build + sell them websites.

## 🧭 Cold-start read-path (AGENTS.md §5)
1. [[AGENTS]] — rules / safety (authority on protocol)
2. [[_HOT]] — generated current-state digest (active tasks + blockers; falls back to [[MEMORY]] when stale)
3. [[_HOME]] — this index
4. `docs/_working-context/<proj>.md` — current focus (e.g. [[leadpipe]])
5. [[past_mistakes]] — gotchas to not repeat
6. [[MEMORY]] — canonical deep state

## 🗺️ Maps of Content
- [[Project-MOC]] — canon, design, control surfaces
- [[Sessions-MOC]] — per-contributor session handoffs
- [[Research-MOC]] — working research + derived NotebookLM insight guides
- [[Reference-MOC]] — source/reference library (ideas only, NOT the scaffold)

## 📊 Dashboards (Bases)
- `docs/_bases/` — Sessions, Reference Library, Research, Pending Approvals (open with the Bases core plugin).

## 👥 People
- **Sean** — owner, sole approver
- **Matt** — collaborator (onboarding/sync status lives in [[MEMORY]])
- **[[SYNC_GUIDE]]** — copy-paste before/after-session checklist for Sean & Matt (plain English)
- **[[AGENT_PROMPT_GUIDE (Matt - Getting Up To Date)]]** — ELI5: git sync words + copy-paste prompt to pull latest before working
- **[[AGENT_PROMPT_GUIDE (Start Session)]]** — ELI5: what AGENTS.md/_HOT/MEMORY are + copy-paste cold-start prompt for new agent chats
- **[[AGENT_PROMPT_GUIDE (End Session)]]** — ELI5: why/how to "wrap up" + copy-paste end-of-session prompt

## 🗂️ Areas
- **Project canon** — `docs/project/` (ARCHITECTURE, [[SELL_METHODOLOGY]], onboarding, visuals)
- **Reference library** — `docs/_reference-library/` — *source material + generated tiers; ideas only, NOT the scaffold*
- **Research** — `docs/research/` — *working notes and synthesized guidance; not canonical state*
- **Skills** — `.claude/skills/` — `wb-context-transfer`, `reference-visualizer`
- **Session logs** — `docs/session-logs/sean/` and `docs/session-logs/matt/`
- **Lead data** — `data/sean/` and `data/matt/` profile stores
- **Reports** — `reports/` generated Sean/Matt/shared lead and Website Brief views

## 🧠 Shared brain
- **NotebookLM** — `website-builder-brain` (shared; mirrors `MEMORY.md` only). Attach your name when you add.
- **This Obsidian vault** — the primary brain (you're in it).

---
*Maintained by `leadpipe vault` + `wb-context-transfer`. `[[wikilinks]]` resolve to repo-root + docs notes in Obsidian.*
