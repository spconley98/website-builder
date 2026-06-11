---
type: session-log
contributors: [sean]
agent: codex
status: active
created: 2026-06-10
updated: 2026-06-10
topic: obsidian-cleanup
tags: [sessions, cleanup, obsidian]
related: ["[[MEMORY]]", "[[AGENTS]]", "[[_HOME]]", "[[Research-MOC]]", "[[Reference-MOC]]", "[[Sessions-MOC]]"]
---

# Session Log — Obsidian Cleanup

## Summary

Sean asked for a deep project-code and Obsidian-flow audit, especially around duplicate-looking research
sections, then approved the conservative cleanup path. Codex implemented navigation/labeling cleanup and
a tiny low-risk `reports.py` dedupe without changing project rules, lead data, store semantics, Firecrawl
guards, or agent stage contracts.

## What changed

- Updated `_HOME.md` so the home index distinguishes canonical project docs, source/reference material,
  derived research, generated reports, and profile stores.
- Updated `docs/_moc/Research-MOC.md`, `docs/_moc/Reference-MOC.md`, and
  `docs/_moc/Sessions-MOC.md` to expose newer session logs, raw-only reference material, and the
  research/reference boundary more clearly.
- Clarified `docs/research/README.md` and
  `docs/research/notebooklm-insights/00_INSIGHTS_INDEX.md`: NotebookLM insight guides are derived
  research aids, not canonical truth.
- Updated `reports/README.md` to list Website Brief reports and remind agents/users that Website Briefs
  need human review before outreach.
- Refactored `src/leadpipe/reports.py` to share repeated link-formatting and category-sort helpers.
  Regenerated reports for Sean and Matt; generated report content did not churn.
- Confirmed `.aiexclude` and `.geminiignore` are tracked and cache folders remain ignored. Left
  `three-brain-out/` and the untracked `.tmp_nateherk/` folder untouched.

## Commands run

```powershell
uv run leadpipe report --profile sean
uv run leadpipe report --profile matt
uv run leadpipe vault validate
uv run leadpipe vault heartbeat
uv run pytest tests/ -q
```

Results:
- Reports regenerated successfully.
- `vault validate`: 40 notes OK.
- `vault heartbeat`: 40 notes scanned, 0 broken links, 0 warnings.
- `pytest`: 56 passed. The sandboxed pytest command hit uv cache permission error
  (`AppData\Local\uv\cache\sdists-v9\.git`: Access denied), then passed when rerun with approved
  escalation.

## Decisions

- Keep cleanup conservative: preserve research/reference/history, but label roles and navigation paths
  clearly.
- Keep `docs/_reference-library/` as source/reference material and `docs/research/` as working or
  derived research. `AGENTS.md` remains protocol authority; `MEMORY.md` remains state authority.
- Do not start SQLite or async/pooling work as part of this cleanup.

## Next recommended steps

- Review and commit/push this cleanup after NotebookLM + local memory sync complete.
- Continue with the already-planned SQLite migration as the next larger technical upgrade.
- Human-review `reports/Sean - Website Briefs.md` before any sales outreach.
- Decide the fate of the stray React/Vite scaffold on `matt-wip-2026-06-09` when ready.

## Risks / blockers

- Codex three-brain route remains documented as down from the prior token-economy session; use Gemini
  for adversarial review until Codex service-tier config is repaired.
- `.tmp_nateherk/` is untracked local material and was intentionally not touched or staged.
