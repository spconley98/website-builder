---
type: project
contributors: [sean, matt]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: agent-onboarding-eli5-end
tags: [onboarding, sean, matt, agents]
related: ["[[AGENTS]]", "[[_HOT]]", "[[MEMORY]]", "[[SYNC_GUIDE]]", "[[AGENT_PROMPT_GUIDE (Start Session)]]"]
---

# New Agent Prompt Guide (End Session) (ELI5)

> For Matt (and Sean too). Explains why every session needs a "save game" step before you close
> the chat, and gives a copy-paste block to do it right. Pair with
> [[AGENT_PROMPT_GUIDE (Start Session)]].

---

## Why does this even matter?

When you close a chat, **everything in that agent's head disappears**. If you just close the
window:
- the next agent (even a few hours later) has no idea what changed
- `_HOT.md` (the "fridge sticky note") goes stale — it'll lie to the next agent
- your work might sit uncommitted on your machine, invisible to Sean/Matt and to GitHub
- if Matt or Sean starts a session before you wrap up, their agent could step on your changes

**The fix:** one command — `wrap up` — that saves the "game state" so the next session (yours,
Matt's, or Sean's) picks up exactly where you left off.

---

## What "wrap up" actually does (in plain English)

Saying `wrap up` (or `/context-transfer`) tells the agent to run the **`context-transfer`**
skill, which does all of this automatically:

| Step | Think of it as... | Why it matters |
|---|---|---|
| Run the test suite (`uv run pytest tests/ -q`) | "Did I break anything?" check | Catches broken code before it gets saved as "current state." |
| Write a session log under `docs/session-logs/<you>/...` | Today's diary entry | Detailed record of what you did and why — future-you or Matt can read this. |
| Regenerate `_HOT.md` (`leadpipe vault hot`) | Re-write the fridge sticky note | Keeps the 30-second summary accurate for the next cold start. |
| Run `leadpipe vault heartbeat` | Check the vault for broken links/typos | Catches broken `[[wikilinks]]` and stale notes before they confuse the next agent. |
| Update `MEMORY.md` (only if the protocol allows) | Update the full diary | Only the right "owner" updates shared state — see `AGENTS.md` §5 authority model. |
| Mirror `MEMORY.md` to NotebookLM brain | Sync the shared cloud copy | Matt and Sean share one NotebookLM brain — keeps it matching the repo. |
| Commit (and push, if you confirm) | Save game | Makes your work visible to GitHub, Matt, and Sean. |

You don't need to remember any of these individually — `wrap up` triggers all of them in order.

---

## The copy-paste prompt — use this at the end of EVERY session

Paste this as your message when you're done working, **before closing the chat**:

```
wrap up

Follow AGENTS.md §8 session protocol + the context-transfer skill:
- run the test suite (uv run pytest tests/ -q)
- write my session log under docs/session-logs/<my-name>/
- regenerate _HOT.md (leadpipe vault hot) and run leadpipe vault heartbeat
- update MEMORY.md only if the authority model in AGENTS.md §5 allows it
- mirror MEMORY.md to the NotebookLM brain, tagged with my name
- show me the git diff/status, then commit (ask before pushing)
```

If something is mid-flight (tests failing, half-done feature) — say so before "wrap up" so the
agent records it as a known blocker instead of pretending things are finished.

---

## What if I'm out of time and didn't finish?

Still say `wrap up`. An honest "this is half-done, here's where I stopped, here's the blocker"
session log is **way more useful** than silence. The next agent (or you tomorrow) needs to know
the true state — not a guess.

---

## The one rule that matters most

**Never skip `wrap up`, even for a 5-minute session.** A skipped wrap-up means `_HOT.md` and
`MEMORY.md` are now wrong, and the next cold-start prompt (see
[[AGENT_PROMPT_GUIDE (Start Session)]]) will hand the next agent stale info. Garbage in →
garbage out.

---

## TL;DR for Matt

1. Finish your work (or hit your stopping point — done or not).
2. Say **`wrap up`** (paste the block above if you want the full checklist spelled out).
3. Review what the agent committed (git diff/status) before it pushes.
4. Close the chat. Next session starts clean via
   [[AGENT_PROMPT_GUIDE (Start Session)]].
