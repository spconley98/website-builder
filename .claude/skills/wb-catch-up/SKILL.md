---
name: wb-catch-up
description: >
  website-builder session-START briefing. The cold-start mirror of wb-context-transfer. Trigger
  when the user says "/wb-catch-up", "catch me up", "catch up", "where did we leave off", or starts
  a fresh session. Thin wrapper — it just runs the repo-native `leadpipe vault catch-up` and reports
  the output (so Claude, Codex, and Gemini all see the same deterministic briefing).
---

# Catch Up — website-builder Session Start

Prints the cold-start briefing so a fresh session never starts blind. This skill is a **thin
wrapper with no logic of its own** (post three-brain/Codex review): the real work lives in the
repo-native `leadpipe vault catch-up`, so every agent — not just Claude — gets the identical
briefing.

## Step 1 — Run the briefing

```powershell
uv run leadpipe vault catch-up                # local-only, instant (default)
uv run leadpipe vault catch-up --sync-check   # also compare local branch vs existing origin refs (no network)
uv run leadpipe vault catch-up --fetch        # refresh remote refs first (network), then compare
```

It prints, from the generated `_HOT.md` digest + live local git + `past_mistakes.md`:
phase · first active task(s) · blockers · latest session · git state · top gotchas. It is a
**non-authoritative printer over `_HOT.md`** — it never re-derives state from `MEMORY.md`, and it
warns if `_HOT.md` is stale (then read `MEMORY.md` directly per AGENTS.md §5).

## Step 2 — Report + orient

Relay the briefing to the user, then before starting new work confirm: current phase, the user's
active task(s), and any blockers. If the briefing flags `_HOT.md` stale or the branch is **behind**
`origin`, reconcile per the AGENTS.md §7 stale-working-copy protocol **before** editing pipeline code.

## Do NOT

- Do not re-implement any parsing or "suggested next" logic here — if the briefing is wrong, fix
  `leadpipe vault catch-up` (in `src/leadpipe/vault.py`), not this skill. Keeping the wrapper trivial
  is what prevents the wrapper/core drift that caused the original skill-collision class of bug.
- Do not run the wrap-up here — that is the END-of-session `wb-context-transfer` skill.
