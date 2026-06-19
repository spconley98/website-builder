# Proposal: carry ops/onboarding tooling from website-final-build → website-builder (leadpipe)

## Repo facts
- website-builder = Python/uv lead pipeline. Cold-start today = documented 6-file read-path
  (AGENTS.md→_HOT.md→_HOME.md→working-context→past_mistakes.md→MEMORY.md) + CLI
  `leadpipe vault validate|heartbeat|hot`. `vault hot` regenerates _HOT.md (a ~500-word digest of
  MEMORY.md, stamped generated/stale_after) from MEMORY.md + latest session log.
- OPEN blocker (in _HOT.md + MEMORY.md): invoking skill `context-transfer` resolves to a GLOBAL
  AAS-WEBSITE skill (~/.claude/skills/context-transfer) that fires the WRONG project's NotebookLM
  brain. Project skill lives at .claude/skills/context-transfer. Other project skill:
  reference-visualizer (no known global twin).
- Sister repo website-final-build (Astro/Node) ALREADY fixed the identical collision by renaming
  context-transfer → wfb-context-transfer, and built `npm run catch-up` (tools/catch-up.mjs):
  a deterministic <30-line cold-start briefing — Codex-hardened into a repo-native core + thin
  Claude skill wrapper so Codex/Gemini get the same briefing.
- AGENTS.md §4 of website-builder FORBIDS design/genmedia/build skills here (clone-site,
  frontend-design, ui-ux-pro-max, AstroWind, SiteConfig, skeletons, Stripe/Resend, etc.). Agent OS
  + Hermes + graphify are global / already present.

## Proposal (3 parts, ops/onboarding ONLY — zero pipeline/agent code touched)
1. Rename project skill context-transfer → wb-context-transfer. Update AGENTS.md §4/§8, _HOME.md,
   and flip the _HOT.md/MEMORY.md blocker entry to resolved. Leave reference-visualizer alone.
2. Add `leadpipe vault catch-up` — a new Typer subcommand beside the existing vault hot/heartbeat/
   validate. Prints: phase, resume point (top In-Progress), last session log, blockers, git state,
   ≤3 past_mistakes gotchas, suggested next. Reuses the parsers `vault hot` already uses to read
   MEMORY.md. Read-only + local by default. Repo-native (Python) so Codex/Gemini get it too, with
   a thin wb-catch-up Claude skill wrapper + one Start-Session guide doc.
3. Fold an opt-in `--sync-check` into catch-up that runs git ahead/behind (git fetch + rev-list)
   to automate AGENTS.md §7 manual stale-working-copy protocol.

## Stress-test asks
Find: failure modes, wrong assumptions, scope creep, DUPLICATION with existing `leadpipe vault hot`/
_HOT.md (do we now have two competing "current state" surfaces? does catch-up violate the §5
authority model that says _HOT.md is the only generated digest?), and anything that makes onboarding
WORSE not better (e.g. another stale surface, another thing to maintain, --sync-check doing network
I/O on every cold-start). Is renaming the skill enough, or does the global AAS skill need to move?
Should catch-up just BE `vault hot` plus a print, or a separate command? Be adversarial. Prove parts wrong.
