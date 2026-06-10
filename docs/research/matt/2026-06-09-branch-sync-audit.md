---
type: research
contributors: [sean]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: branch-sync-audit
tags: [research, audit]
---

# Matt Branch Sync Audit - 2026-06-09

## Decision

Use current `main` as the canonical foundation for Sean and Matt. Do not merge or cherry-pick
`origin/onboarding-matt` wholesale.

## Evidence

- Current local `main` was ahead of `origin/main` by 2 commits at the start of this cleanup.
- `origin/onboarding-matt:data/leads.jsonl` has 166 records.
- Current `data/matt/leads.jsonl` has 166 records.
- `Compare-Object` between those two lead files returned 0 differences.
- Current Matt lead statuses are 98 `found` and 68 `prioritized`.
- Current `data/sean/leads.jsonl` has 28 records and was not migrated or rewritten for this audit.
- One shared place exists between Sean and Matt profile stores: Fresh Brew Cafe
  (`ChIJOcFA7FDRRIYRyVPmm9uPTSE`).

## Branch Risk

`git diff --stat main..origin/onboarding-matt` shows the branch would remove or rewrite current
foundation files if merged directly, including protocol docs, profile target configs, Agent 3 website
intelligence, reports, tests, and session logs. Treat the branch as historical evidence and an artifact
source only.

## Result

No second Matt lead migration is needed unless new commits appear on Matt's branch. Matt should move to
current `main` after Sean pushes the canonical cleanup commit, preserving any local dirty work on a Matt
WIP branch before pulling.
