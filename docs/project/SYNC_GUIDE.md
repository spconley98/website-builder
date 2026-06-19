---
type: project
contributors: [sean, matt]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: sync-protocol
tags: [onboarding, sync, sean, matt]
related: ["[[AGENTS]]", "[[MEMORY]]", "[[ONBOARDING_MATT]]"]
---

# Sean ↔ Matt — Working Together Safely

Two people, three AI agents (Claude, Codex, Gemini), one repo. This page is the **before/after every
session** checklist so neither of you overwrites the other's work. Copy-paste the block for your name.

## Why this matters (plain English)

You're both editing the same shared folder from different computers. If you start working on an old
copy, your AI can make changes that conflict with — or silently undo — what the other person already
did. The commands below check "is my copy current?" before touching anything, and "did I just leave
a mess?" before you walk away. Skipping this is how work gets lost or duplicated.

---

## Before you start working — check you're up to date

Run this first, every session, before asking your AI to change anything:

```powershell
git status --short --branch
git fetch origin
git log --oneline HEAD..origin/main
git log --oneline origin/main..HEAD
```

**What you're looking at:**
- First line tells you if you have uncommitted changes (your own unsaved work).
- `HEAD..origin/main` = commits the *other person* made that you don't have yet.
- `origin/main..HEAD` = commits *you* made that aren't pushed yet.

**If you have no local changes and you're behind:**
```powershell
git pull --ff-only
uv sync --group dev
uv run pytest tests/ -q
```

**If you have local changes (uncommitted work):** don't pull yet. Tell your agent to save your work
first (new branch or commit), THEN pull. Never `git reset --hard` or `git checkout .` to "make pulling
easier" — that deletes your work. See `AGENTS.md` §7 "Stale working-copy protocol" for the full version.

---

## After you finish working — wrap up cleanly

```
/wb-context-transfer
```
(say `/wb-context-transfer`, **not** the bare `/context-transfer` — that fires a different
project's global skill)

This single command tells your agent to: run the test suite, write a dated note about what you did
under `docs/session-logs/<your-name>/`, update the shared `MEMORY.md` if you're allowed to, sync the
shared NotebookLM brain, and commit + push everything. **Do this every session, even short ones** — it's
the only thing that keeps both of your AIs (and Codex) on the same page about what changed and why.

---

## Quick copy-paste — Sean

```powershell
git status --short --branch
git fetch origin
git log --oneline HEAD..origin/main
git pull --ff-only
uv sync --group dev
uv run pytest tests/ -q
```
...do your work, then say: `wrap up`

## Quick copy-paste — Matt

```powershell
git status --short --branch
git fetch origin
git log --oneline HEAD..origin/main
git pull --ff-only
uv sync --group dev
uv run pytest tests/ -q
uv run leadpipe check --google
```
...do your work, then say: `wrap up`

---

## If something looks wrong

- **Tests fail after pulling** → tell your agent the exact error, don't try to "fix" it by force-pushing
  or resetting. Read `past_mistakes.md` first — it might already be documented.
- **Your agent says the branch has uncommitted changes from before** → don't discard them. Have the
  agent save them on a new branch (e.g. `<yourname>-wip-YYYY-MM-DD`) first, then proceed.
- **Confused about current project state** → read `_HOT.md` (30-second summary), then `MEMORY.md`
  (full state). Both are kept current by the wrap-up step above.

---

## The one rule that matters most

**Never let your agent overwrite the other person's uncommitted work to make a pull "go smoothly."**
Every git operation that could discard work (`reset --hard`, `checkout .`, `clean -f`, force-push)
needs your explicit yes — your agent should ask first.
