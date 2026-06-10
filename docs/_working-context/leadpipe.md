---
type: context
contributors: [sean]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: leadpipe-working-context
tags: [working-context, leadpipe]
related: ["[[MEMORY]]", "[[ARCHITECTURE]]"]
---

# Working context — leadpipe

**Current focus:** the lead pipeline is built and validated; active work is the Obsidian agent-brain
upgrade (this branch) plus real hunts. One file per active project — regenerate or trim as focus shifts.

## In scope right now
- Obsidian agent-brain spine: authority model, `_HOT`/MOCs, `leadpipe vault` (this branch).
- Real hunts from `config/targets.sean.yaml` / `config/targets.matt.yaml`.
- Reviewing Matt's imported leads in `data/matt/leads.jsonl` before any outreach.

## Open questions
- Which small vetted target subset to promote from Matt's proposed-targets research.
- When to enable Bases dashboards on Matt's clone (needs the reviewed `core-plugins.json`).

## Key files
- Pipeline: `src/leadpipe/` (agents/, pipeline.py, store.py).
- Vault maintenance: `src/leadpipe/vault.py`.
- Full design in [[ARCHITECTURE]]; gotchas in [[past_mistakes]].
