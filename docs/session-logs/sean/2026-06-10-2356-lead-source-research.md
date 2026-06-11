---
type: session-log
contributors: [sean]
agent: codex
status: active
created: 2026-06-10
updated: 2026-06-10
topic: lead-source-research
tags: [sessions, research, leadpipe]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session Log — Lead Source Research

## Summary
Sean asked how to expand leadpipe beyond the current Google Places + Ollama workflow, especially for building a very large lead database without surprise billing. Codex used Firecrawl-backed web research and translated the findings into plain-English operating guidance.

## What Changed
- No pipeline code was changed.
- `MEMORY.md` was updated with the research decision: use free/open sources for bulk seeding, then paid APIs only for small verification/enrichment batches.
- This session log was created under the Sean-owned handoff folder.

## Research Findings
- Google Places remains the high-confidence source for verifying the hard "no website" fact, but it should not be used as the bulk database engine if cost avoidance is the goal.
- OpenStreetMap/Overpass is the best first low-cost/free spike for small polite queries.
- Overture Maps Places is a promising free bulk dataset for larger seeding, but it needs local storage/query work.
- Public registries, permits, licenses, chambers, and directories can provide vertical-specific seed lists, especially for trades and regulated businesses.
- Yelp and Foursquare are useful as second-opinion enrichment/validation sources, but are not ideal as free bulk sources.
- Apify, Bright Data, Clay, Apollo, and n8n are useful reference ecosystems; most serious usage is paid or credit-backed.
- For the sister website-building project, public photos should be used only for research/private drafts until the business owner grants permission. Final publishing should require asset provenance and `approved` or `client_provided` status.

## Commands Run
- `uv run leadpipe vault validate` — passed, 43 notes OK.
- `uv run leadpipe vault heartbeat` — passed, 43 notes scanned, 0 broken links, 0 warnings.
- `uv run leadpipe vault hot` — regenerated `_HOT.md`, stale after 2026-06-15.
- `uv run leadpipe vault validate` — final pass, 44 notes OK.
- `uv run leadpipe vault heartbeat` — final pass, 44 notes scanned, 0 broken links, 0 warnings.
- `py -m notebooklm status` — active local context was `NATE HERK GUIDE`, confirming the known context-drift risk.
- `py -m notebooklm source add .\MEMORY.md --notebook bd83690f-e997-46c5-b054-6ff3139e11d6 --title "[Sean] MEMORY.md - 2026-06-10 2356 - lead-source-research"` — uploaded canonical `MEMORY.md` to website-builder brain as source `6a854248-e840-476d-bcf3-db964229dc90`.
- `node C:/Users/mysis/.claude/memory-mcp/indexer.mjs` — sandboxed run embedded chunks but failed to write outside the repo; after explicit approval to run outside the sandbox, reindex succeeded and wrote 317 chunks.
- `uv run pytest tests/ -q` — first sandboxed run failed because the Codex sandbox could not open the global `uv` cache under `AppData`; after Sean's later instruction to go outside the sandbox, the test suite passed: 59 passed in 1.04s.
- Cache inspection showed the blocked `uv` cache `.git` file was owned by `SEAN\mysis`, not read-only, and had normal ACLs; the likely cause was sandbox access to `AppData`, not a broken project cache.

## Files Touched By This Wrap-Up
- `MEMORY.md`
- `docs/session-logs/sean/2026-06-10-2356-lead-source-research.md`

## Existing Worktree Notes
Before this wrap-up, the branch already had modified lead data, generated reports, and branch docs. Those were not authored by this Codex research session and should be preserved/reviewed separately:
- `data/sean/leads.jsonl`
- `reports/Sean - AI Leads.md`
- `reports/Shared - AI Leads.md`
- `docs/_moc/Project-MOC.md`
- `docs/_working-context/leadpipe.md`
- `docs/project/ARCHITECTURE.md`
- `docs/project/ONBOARDING_MATT.md`
- `docs/project/visuals/website-builder-pipeline.md`

## Next Recommended Steps
- Set or confirm Google Cloud budget alerts and Places API quotas before any large verification run.
- Design a free/open seed stage, likely `leadpipe seed-osm`, that stores "website missing from source" as a low-confidence signal rather than a hard no-website fact.
- Plan the SQLite migration before building any truly large local database.
- For the sister project, create an asset provenance model before pulling owner-approved photos into final websites.
