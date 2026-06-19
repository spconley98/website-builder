---
type: project
contributors: [sean, matt]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: agent-onboarding-eli5-start
tags: [onboarding, sean, matt, agents]
related: ["[[AGENTS]]", "[[_HOT]]", "[[MEMORY]]", "[[SYNC_GUIDE]]", "[[ONBOARDING_MATT]]", "[[AGENT_PROMPT_GUIDE (End Session)]]"]
---

# New Agent Prompt Guide (Start Session) (ELI5)

> For Matt (and Sean too). Explains why every new chat needs a "wake-up" prompt, what each file
> does, and gives a copy-paste block to start every session. Pair with
> [[AGENT_PROMPT_GUIDE (End Session)]] for wrap-up. **Matt: run
> [[AGENT_PROMPT_GUIDE (Matt - Getting Up To Date)]] first to sync your repo.**

---

## Why does this even matter?

Every time you open a **new chat** with Claude/Codex/Gemini, that agent has **zero memory** of
anything from before. Brand new brain. It doesn't know:
- what this project is
- what we already built
- what's broken
- what you're working on right now

If you just say "hey, fix the lead scorer" — the agent might re-do work that's already done,
break something that was just fixed, or guess wrong about the project and go off in a weird
direction.

**The fix:** this repo has a small set of files that act like a "save file" for the project.
A new agent reads them first (takes seconds), and now it "remembers" everything important —
without you having to explain the whole project every single time.

---

## The files, explained like you're 5

| File | Think of it as... | Why it matters |
|---|---|---|
| **`AGENTS.md`** | The rulebook / constitution | Tells the agent the rules: who's allowed to do what, how we name commits, how we organize files, what NOT to do. Doesn't change much. |
| **`_HOT.md`** | A sticky note on the fridge | Auto-generated 30-second summary: "here's what's going on RIGHT NOW, here's what's blocked." Gets regenerated automatically when someone wraps up. |
| **`_HOME.md`** | The map / table of contents | Links to everything else. If the agent gets lost, this points the way. |
| **`MEMORY.md`** | The full diary | The complete, detailed history of decisions and current state. `_HOT.md` is the summary of THIS file. If they disagree, `MEMORY.md` wins. |
| **`past_mistakes.md`** | "Don't touch the stove again" list | Bugs/gotchas we already hit once. Stops the agent from repeating the same mistake. |
| **Latest session log** (`docs/session-logs/<you>/...`) | Yesterday's notes-to-self | The most recent detailed write-up of what was done and why — more detail than `_HOT.md` gives. |

**The order matters** because each file is small and gets you "more detail, but slower" — like
zooming in on a map. Read the cheap/fast ones first; only dig into `MEMORY.md` or session logs
if you need the full story.

---

## What is "context" and why do agents "drop" it?

Every agent has a limited amount of "working memory" per chat (called the **context window**).
Long sessions, big files, lots of back-and-forth — eventually it fills up and older parts of the
conversation get summarized or forgotten ("token drop").

**Reading the small files above FIRST** means: even if the agent later forgets earlier parts of
a long chat, the *important* stuff (what this project is, current priorities, rules) was loaded
early and is more likely to stick around or get re-summarized correctly. It's cheap insurance.

---

## The one-command shortcut (preferred)

Before the copy-paste block below, the fastest catch-up is one command — it prints the `_HOT.md`
digest + your live git state + the top gotchas in a single briefing:

```powershell
uv run leadpipe vault catch-up                # local-only, instant
uv run leadpipe vault catch-up --sync-check   # also compare against origin (uses existing refs)
uv run leadpipe vault catch-up --fetch        # refresh remote refs first, then compare (network)
```

The copy-paste prompt below is the fuller fallback (it has the agent read each file and reason
about it) — use it when you want the agent oriented, not just yourself.

## The copy-paste prompt — use this at the start of EVERY session

Paste this as your **first message** in a brand-new chat (Claude, Codex, or Gemini — works for
all three since they all point at `AGENTS.md`):

```
Cold start. Read in this order, following AGENTS.md §5 cold-start read-path:
1. AGENTS.md
2. _HOT.md
3. _HOME.md
4. docs/_working-context/leadpipe.md
5. past_mistakes.md
6. MEMORY.md

Then check git status (am I behind origin/main? any uncommitted work from
last session?), check for any pending approvals, and give me a short
summary of: current phase, my active tasks, and any blockers — before we
start new work.
```

**That's it.** This single block:
- Loads the rules (`AGENTS.md`)
- Loads "what's happening right now" (`_HOT.md`, `MEMORY.md`)
- Loads "don't repeat this mistake" (`past_mistakes.md`)
- Checks if your local copy is stale (the [[SYNC_GUIDE]] check)
- Gives you a summary back, so YOU also know where things stand — not just the agent

---

## At the end of every session

Just say:

```
/wb-context-transfer
```

This runs the `wb-context-transfer` skill: writes a session log, updates `_HOT.md`/`MEMORY.md` if
allowed, syncs the shared NotebookLM brain, and commits. **This is what makes the cold-start
prompt above actually useful next time** — if nobody wraps up, `_HOT.md` goes stale and the next
agent starts more blind.

---

## TL;DR for Matt

1. New chat → paste the **cold start** block above → read the summary the agent gives you.
2. Do your work.
3. Say **`wrap up`** before you close the chat.
4. If confused mid-session → `[[SYNC_GUIDE]]` (sync checklist) or just ask the agent to
   "re-read `_HOT.md` and `MEMORY.md`".

That's the whole loop. Every agent, every session, same loop — that's how Claude, Codex, and
Gemini all stay in sync on the same project without stepping on each other.
