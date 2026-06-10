---
type: project
contributors: [matt, sean]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: matt-sync-eli5
tags: [onboarding, matt, sync, git]
related: ["[[AGENTS]]", "[[SYNC_GUIDE]]", "[[AGENT_PROMPT_GUIDE (Start Session)]]", "[[AGENT_PROMPT_GUIDE (End Session)]]"]
---

# Matt — Getting Up To Date (ELI5)

> For Matt. Explains, like you're 5, why you must "sync" before working, what each git command
> does, and what to paste so your agent does it for you. Run this **before**
> [[AGENT_PROMPT_GUIDE (Start Session)]] cold-start prompt — or just paste both together.

---

## Why does this matter?

Sean works on this same repo too. While you were away, Sean (or his agent) may have:
- changed `AGENTS.md` (the rulebook)
- updated `MEMORY.md` / `_HOT.md` (current state)
- added/changed code

If you start working on your **old copy** without updating first, two bad things can happen:
1. Your agent follows **old rules** — it doesn't know about new decisions.
2. When you try to push your work later, it can **conflict** with Sean's changes — messy to fix,
   and risky (someone's work can get lost if handled wrong).

**The fix:** "sync" = check what's new, pull it down, THEN start working.

---

## The git words, explained like you're 5

| Word/command | What it means in plain English |
|---|---|
| **`origin`** | The shared copy on GitHub — the "master" version everyone pushes to / pulls from. |
| **`main`** | The main/shared branch — the "official" version of the project. |
| **`HEAD`** | "Where I am right now" on my local copy. |
| **`git fetch origin`** | "Go check GitHub for new stuff, but don't change my files yet." Just looks. |
| **`git status --short --branch`** | "Show me: am I ahead, behind, or have I got unsaved changes?" |
| **`git log --oneline HEAD..origin/main`** | "List the commits Sean made that I DON'T have yet." |
| **`git log --oneline origin/main..HEAD`** | "List the commits I made that I haven't pushed yet." |
| **`git pull --ff-only`** | "Download Sean's new commits and add them to my copy — but ONLY if it's a clean add with no conflicts." Safe. |
| **uncommitted changes** | Work you did that hasn't been "saved" into git history yet. **Never get deleted to make a pull easier** — that's how work gets lost. |

---

## The copy-paste prompt — run this FIRST, every session

Paste this as your first message (before or together with the
[[AGENT_PROMPT_GUIDE (Start Session)]] cold-start prompt):

```
Sync check before we start. Follow AGENTS.md §7 "Stale working-copy
protocol" and SYNC_GUIDE:

1. Run: git status --short --branch
2. Run: git fetch origin
3. Run: git log --oneline HEAD..origin/main   (what Sean has that I don't)
4. Run: git log --oneline origin/main..HEAD   (what I have that's unpushed)

Then:
- If I have NO uncommitted changes and I'm behind: run
  `git pull --ff-only`, then `uv sync --group dev`, then
  `uv run pytest tests/ -q`. Tell me if anything fails.
- If I HAVE uncommitted changes: do NOT pull yet. Tell me what files
  changed, and save my work first (new branch or WIP commit) before
  pulling. Never use reset --hard, checkout ., or clean -f without
  asking me first.
- After syncing, re-read AGENTS.md and MEMORY.md if they changed —
  rules may have been updated.
```

---

## What the agent will tell you back

- **"You're up to date"** → great, move on to the cold-start prompt
  ([[AGENT_PROMPT_GUIDE (Start Session)]]).
- **"You're behind, no local changes, pulled clean"** → also great, just re-read updated
  `AGENTS.md`/`MEMORY.md` if they changed, then continue.
- **"You have uncommitted changes AND you're behind"** → agent should pause, save your work
  safely (e.g. branch `matt-wip-YYYY-MM-DD`), THEN pull. Don't let it discard anything.
- **"Tests failed after pulling"** → tell the agent the exact error. Check
  [[past_mistakes]] first — might be a known issue with a known fix.

---

## The one rule that matters most

**Never let an agent discard your unsaved work to "make the pull easier."** Anything that says
`reset --hard`, `checkout .`, `clean -f`, or force-push needs your explicit "yes" first — every
time, no exceptions.

---

## TL;DR for Matt

1. New session → paste the **sync check** prompt above first.
2. If behind + no local changes → agent pulls + tests, tell you results.
3. If you have local changes → agent saves them safely first, THEN pulls.
4. Then run the [[AGENT_PROMPT_GUIDE (Start Session)]] cold-start prompt.
5. Work.
6. [[AGENT_PROMPT_GUIDE (End Session)]] — `wrap up` before closing.
