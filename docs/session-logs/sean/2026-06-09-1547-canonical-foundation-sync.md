---
type: session-log
contributors: [sean]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: canonical-foundation-sync
tags: [sessions]
---

# Canonical Foundation Sync - 2026-06-09 1547

## Contributor

Sean

## Agent

Codex

## Summary

Current `main` remains the canonical foundation for Sean and Matt. `origin/onboarding-matt` was not
merged or cherry-picked; it was preserved as an artifact source only.

## What changed

- Fixed Markdown table escaping in `src/leadpipe/reports.py` so lead text containing `|` stays inside a
  single table cell.
- Added a report regression test using `Mecanico a Domicilio | Mobile Mechanic`.
- Regenerated Matt and shared reports through `leadpipe report` so the existing dirty shared report diff
  was resolved by generation, not hand editing.
- Added `docs/research/matt/2026-06-09-branch-sync-audit.md`.
- Added `docs/research/matt/2026-06-09-proposed-targets-from-onboarding-matt.md`.
- Updated `MEMORY.md` with the canonical sync decision and next-agent handoff.

## Verification

- `uv run pytest tests/ -q` -> 26 passed.
- `uv run leadpipe report --profile sean` -> regenerated Sean + shared reports.
- `uv run leadpipe report --profile matt` -> regenerated Matt + shared reports.
- `reports/Shared - Prioritized Leads.md` now renders `Mecanico a Domicilio \| Mobile Mechanic`.
- `data/matt/leads.jsonl` remains 166 records.
- `data/sean/leads.jsonl` remains 28 records.
- Matt statuses remain 98 `found`, 68 `prioritized`.
- `Compare-Object` between `origin/onboarding-matt:data/leads.jsonl` and current
  `data/matt/leads.jsonl` returned 0 differences.
- `git diff --name-status main..origin/onboarding-matt` was inspected and not applied.

## Decisions

- Do not merge `origin/onboarding-matt` wholesale.
- Keep `config/targets.matt.yaml` empty until Sean/Matt choose a smaller first Matt run list.
- Convert Matt's broad branch targets into research notes only.
- Defer optional code imports from Matt's branch; rebuild useful hardening later on current `main`.
- Keep Firecrawl-backed stages behind explicit `--use-firecrawl`; do not add interactive prompts.

## NotebookLM / Obsidian

- NotebookLM brain: `website-builder-brain`
  (`bd83690f-e997-46c5-b054-6ff3139e11d6`).
- Upload title used for this context transfer:
  `[Sean] MEMORY.md - 2026-06-09 1547 - canonical-foundation-sync`.
- Uploaded source ID: `a5c65bf7-7251-4ca8-98b5-5486e1a99e31`.
- Note: `source add --title` initially created a plain `MEMORY.md` source; it was immediately renamed
  with `py -m notebooklm source rename` and verified in `source list --json`.
- Matt NotebookLM access is listed as accepted in current shared memory.
- Obsidian vault remains the project folder at `C:\Users\mysis\website-builder`; Matt still works from
  the same repo structure once synced to canonical `main`.

## Next recommended steps

1. Commit and push canonical `main`.
2. On Matt's machine, preserve any dirty work on a Matt WIP branch, then fast-forward to `origin/main`.
3. Matt runs `uv sync --group dev` and `uv run pytest tests/ -q`.
4. Sean/Matt choose a small first Matt target list before editing `config/targets.matt.yaml`.
