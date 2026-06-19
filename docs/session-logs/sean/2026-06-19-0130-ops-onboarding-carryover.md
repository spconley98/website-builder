---
type: session-log
contributors: [sean]
agent: claude
status: active
created: 2026-06-19
updated: 2026-06-19
topic: ops-onboarding-carryover
tags: [sessions, onboarding, tooling]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session — ops/onboarding carry-over from website-final-build (Sean/Claude, 2026-06-19)

## What Sean asked
Catch up, access the NotebookLM brain, audit the sister repo `website-final-build`'s entire framework,
decide what tools/frameworks/ideas to carry over to **this** repo (`website-builder`/leadpipe), make an
implementation proposal, stress-test it via three-brain, then build.

## What was decided + done
- **Audit:** read both repos' constitutions + the `website-final-build-brain` NotebookLM brain. Verdict:
  the sister repo's design/build skills are **out of scope here** (AGENTS.md §4 forbids them in the
  lead-pipeline repo); Agent OS / Hermes / graphify are global or already present; only the
  **ops/onboarding layer** was worth porting.
- **Stress-test:** routed the proposal to **Codex** (route confirmed back up — the logged `service_tier`
  blocker was killed by the codex-cli 0.128→**0.139** bump; live `codex exec` succeeded). Verdict
  **FIX-FIRST**, 8 findings — all folded in. Review filed at
  `three-brain-out/2026-06-19-carryover-proposal/` (input + codex-review + ledger row).
- **Sean's calls:** "rename + ban bare name" (stay in-repo) · "build all 3 parts".

## Shipped (Python-native, mirrors the sister repo's Node tooling)
1. **Skill rename** `context-transfer` → **`wb-context-transfer`** (`git mv` + `name:` field + every
   *active* invocation: AGENTS.md §4/§8, CLAUDE.md, GEMINI.md, _HOME.md, Start/End guides, SYNC_GUIDE,
   ONBOARDING_MATT, ARCHITECTURE). Historical session logs + reference-library left untouched. Closes the
   long-standing skill-collision blocker; bare `/context-transfer` documented as banned.
2. **`leadpipe vault catch-up`** — executable cold-start briefing. A *non-authoritative printer* over the
   generated `_HOT.md` (+ live local git + top `past_mistakes.md` gotchas) — never re-derives from
   MEMORY.md (Codex #1). Warns if `_HOT.md` stale. Local/read-only by default; `--sync-check` compares
   existing origin refs (no network), `--fetch` refreshes first (Codex #6).
3. **`wb-catch-up`** thin skill wrapper — delegates entirely to the CLI (Codex #8) so Codex/Gemini get
   the identical briefing.
4. **State fixes:** flipped the Codex-route-DOWN + skill-collision blockers to RESOLVED in MEMORY.md;
   edited MEMORY.md then regenerated `_HOT.md` (never hand-edited, Codex #2).

## Commands run + results
- `uv run pytest tests/ -q` → **63 passed** (+4 new catch-up tests).
- `uv run leadpipe vault validate` → **48 notes OK**; `heartbeat` → **0 broken links**.
- `uv run leadpipe vault catch-up [--sync-check]` → verified output (digest + git ahead/behind + gotchas).
- `codex exec` adversarial review → FIX-FIRST.

## Files changed
`src/leadpipe/vault.py` (+catch-up cmd, git/gotcha helpers), `tests/test_vault.py` (+4 tests),
`.claude/skills/wb-context-transfer/` (renamed), `.claude/skills/wb-catch-up/` (new), AGENTS.md,
CLAUDE.md, GEMINI.md, _HOME.md, _HOT.md, MEMORY.md, ARCHITECTURE.md, ONBOARDING_MATT.md, SYNC_GUIDE.md,
both AGENT_PROMPT_GUIDE docs, `three-brain-out/`.

## Next
- Run a real `leadpipe find` on the small-town `config/targets.sean.yaml`, then prioritize.
- Optional: move the global AAS `context-transfer` skill into the AAS repo (root-cause fix for the
  collision; left as a logged option per Sean's "rename + ban" decision).
- SQLite + asyncio remain the next larger engine upgrades.

## Blockers
None new. Codex route restored. NotebookLM auth may need `py -m notebooklm login` if the cookie expired.
