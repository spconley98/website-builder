---
name: context-transfer
description: >
  website-builder session wrapup skill. Verifies build health (if applicable), updates
  contributor-owned context-transfer notes, optionally updates MEMORY.md when allowed by
  AGENTS.md, optionally uploads to NotebookLM project brain, and commits all changes. Trigger
  when user says "wrap up", "end session", "context transfer", "close session",
  "/context-transfer", or "update memory".
---

# Context Transfer — website-builder Session Wrapup

Closes out a work session cleanly so the next agent (or future you) has full context.

---

## Step 1: Health Check

This is a **Python/uv** project (`pyproject.toml`) — **not** npm. Run the test suite and the vault
checks; report results before continuing and fix failures before proceeding.

```powershell
uv run pytest tests/ -q          # riskiest-contract tests — should be all green
uv run leadpipe vault validate   # frontmatter schema on the allowlisted notes
uv run leadpipe vault heartbeat  # broken [[wikilinks]] / orphans / stale notes (report-only)
```

---

## Step 2: Contributor Context Transfer

Create or update a contributor-owned session handoff:

```text
docs/session-logs/sean/YYYY-MM-DD-HHMM-<short-topic>.md
docs/session-logs/matt/YYYY-MM-DD-HHMM-<short-topic>.md
```

Default contributor is **Sean** unless the conversation explicitly names Matt or another contributor.

Include:
- contributor name
- timestamp
- agent/tool used
- what changed
- commands run and results
- files changed
- decisions made
- next recommended steps
- blockers or risks

This file is the default place for every context transfer. Matt's agent must not rewrite shared
`MEMORY.md`, `AGENTS.md`, scaffold docs, or code as part of context transfer unless Sean explicitly
asks for that exact change.

---

## Step 2b: MEMORY.md Update

Update `MEMORY.md` (project root) with:

- **Last Updated:** current datetime (ISO 8601)
- **Last Agent:** model name + task area (e.g., "Claude Sonnet 4.6 — Phase 1 content")
- **Phase:** current phase
- **✅ Completed:** move anything finished from In Progress → Completed — tag each item with the contributor who did it (e.g., "Sean — navbar layout", "mp214gitty — pricing copy")
- **🔨 In Progress:** what was being worked on when session ended — tag with contributor
- **🚫 Blocked:** any blockers discovered this session
- **👤 Contributors this session:** list each person + the section/area they worked on. Default to **Sean** if no other contributor is mentioned in the conversation; name others explicitly when the user references them (e.g., mp214gitty)
- **Context for Next Agent:** 2-3 sentence handoff — what's done, what's next, any gotchas
- **Active Design Decisions:** update if any decisions were made or changed
- **Known Issues & Tooling:** update if any new issues found or fixed

Rules:
- Sean-owned sessions may update `MEMORY.md` directly when the session changes project state.
- Matt-owned sessions should append detailed context to `docs/session-logs/matt/` and leave
  `MEMORY.md` untouched unless Sean explicitly approves a shared-memory update.
- If Matt's agent believes `MEMORY.md` is stale, it should create a proposed memory update in the
  Matt context-transfer note instead of rewriting the shared file.

---

## Step 2c: Regenerate the brain spine (repo-native — works for Sean AND Matt)

After `MEMORY.md` is updated, regenerate the generated onboarding layer and check vault health. These are
pure Python (`leadpipe vault`, AGENTS.md §6) — **no Obsidian plugins or Claude skills required**, so Matt's
Gemini runs them identically:

```powershell
uv run leadpipe vault hot         # regenerate _HOT.md from the just-updated MEMORY.md
uv run leadpipe vault heartbeat   # broken [[wikilinks]] / stale / missing-frontmatter (fix broken links)
uv run leadpipe vault validate    # frontmatter schema on the allowlisted notes
```

Never hand-edit `_HOT.md` — it is regenerated here. Commit the refreshed `_HOT.md` in Step 4.

---

## Step 3: Upload to NotebookLM

Upload updated `MEMORY.md` to the website-builder Project Brain notebook. Source titles must include
the contributor, timestamp, and topic so repeated uploads remain auditable.

**Mirror `MEMORY.md` only** — do NOT upload `_HOT.md` or any other generated digest. A second
"current state" source in the brain is exactly the duplicate/stale problem already repaired once
(AGENTS.md §5: NotebookLM mirrors `MEMORY.md` only).

**Notebook:** website-builder-brain
**ID:** `bd83690f-e997-46c5-b054-6ff3139e11d6`
**URL:** https://notebooklm.google.com/notebook/bd83690f-e997-46c5-b054-6ff3139e11d6
**Shared with:** mpitto214@gmail.com (mp214gitty) — see `MEMORY.md` for current share/acceptance status (don't hardcode it here)

In session summary, note current acceptance status of the shared notebook invite (pending / accepted) so next agent knows whether the collaborator has full access yet.

Run via CLI, replacing the contributor/topic values for the session:
```powershell
py -m notebooklm source add ./MEMORY.md --notebook bd83690f-e997-46c5-b054-6ff3139e11d6 --title "[Sean] MEMORY.md - YYYY-MM-DD HHMM - short-topic"
```

For Matt-owned context transfers, use `[Matt] MEMORY.md - YYYY-MM-DD HHMM - short-topic`. If
authorship is unclear during a repair/audit, use `[Unknown] MEMORY.md - YYYY-MM-DD HHMM -
needs-review` instead of guessing. Never upload a plain `MEMORY.md` title.

If CLI unavailable or fails, instruct user to manually re-upload `MEMORY.md` to the notebook and note it in session output.

---

## Step 3a: Obsidian vault note

Sean created an **Obsidian vault** pointed directly at this project folder
(`C:\Users\mysis\website-builder`). It serves as:
- scaffolding/structure reference for future agents
- shared layout/theme tracker for both contributors
- visual map of the project that raw files / Antigravity can't provide

**Matt** (mp214gitty / mpitto214@gmail.com) needs to **download Obsidian** and open this
folder as a vault to use it. Note current status (vault exists, Matt onboarded or not yet)
in the session summary.

---

## Step 3b: Reindex local semantic memory

Re-embed the markdown memory so the `memory` MCP server (`search_memory`) can recall
this session's notes next time. Runs locally via Ollama (`nomic-embed-text`) — free, offline.

```powershell
node C:/Users/mysis/.claude/memory-mcp/indexer.mjs
```

If Ollama isn't running, start it (`ollama serve`) or note that reindex was skipped.
The index lives at `C:/Users/mysis/.claude/memory-mcp/index.json` (not committed).

---

## Step 4: Commit

Stage and commit all changes with format:

```
[PHASE][AREA] Session wrapup — <1-line summary of what was accomplished>
```

Example:
```
[1][blueprint] Session wrapup — locked brand tokens, updated content-map placeholders
```

Only commit files that changed this session. Never commit `.env`, secrets, or `node_modules`.

---

## Step 5: Report

Output a clean session summary:

```
SESSION COMPLETE
───────────────
✅ Build: passing (or: skipped — no build tooling)
✅ MEMORY.md: updated
✅ NotebookLM: synced (or: skipped — not configured)
✅ Committed: [commit hash]

NEXT SESSION SHOULD:
- [top priority item]
- [second priority]
```
