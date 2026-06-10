---
type: project
contributors: [sean]
status: active
created: 2026-06-09
updated: 2026-06-09
topic: past-mistakes
tags: [lessons, gotchas]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

> Known bugs, gotchas, and design traps already paid for. **Read before debugging** — don't rediscover
> these. Add an entry whenever a session hits a non-obvious bug or an agent hallucination.

## IPv6 DNS hang on every API call
Google/Firecrawl HTTPS calls hung ~85s on Sean's network because DNS returned a broken IPv6 route. The
fix is `src/leadpipe/config.py::_force_ipv4_dns()` (IPv4-only resolution → ~0.05s). If API calls are
mysteriously slow, verify that patch is present rather than re-debugging the network.

## Google "Places API (New)" 403
A 403 `SERVICE_DISABLED` means the **"Places API (New)"** toggle is off — the legacy "Places API" is not
enough. `PlacesError` messages carry the exact enable URL. Common when a collaborator first wires a key.

## Firecrawl is credit-backed — never auto-spend
`prioritize`, `run`, and `intelligence` spend Firecrawl credits and require an explicit `--use-firecrawl`
flag. No autonomous or scheduled scraping. The account has hit "Insufficient credits" before — check first.

## Don't merge `origin/onboarding-matt` wholesale
Matt's old branch predates the scaffold; merging it reverts profile isolation, Agent 3, and the guardrails.
Import only Matt-owned `data/`, `docs/research/matt/`, `docs/session-logs/matt/` (AGENTS.md §7).

## Facts vs judgment must stay separated
The three-brain/Codex review caught status regression and enrichment overwriting facts. Each agent writes
ONLY its stage's fields (LeadCreate → LeadPrioritization → LeadWebsiteIntelligence) and status is monotonic.
Don't "simplify" the stage-scoped writes in `models.py`/`store.py` away without re-reading the reasoning.

## NotebookLM: one current-state source, always provenance-titled
Duplicate plain `MEMORY.md` uploads once required a provenance repair. Mirror **`MEMORY.md` only** (never
`_HOT.md`), titled `[<Name>] MEMORY.md - YYYY-MM-DD HHMM - <topic>`; retire/rename stale sources.

## Obsidian types properties globally by name
A property name has one type across the whole vault, so `contributors` must ALWAYS be a list (even for one
person) or Bases/Properties misbehave. Leave optional fields absent rather than blank — an empty date breaks
Bases filters. `leadpipe vault validate` enforces this.

## `.obsidian/` is an executable trust boundary
A real campaign (REF6598) hid a PHANTOMPULSE RAT in `.obsidian/plugins/<x>/data.json`. Never git-track or
sync `.obsidian/plugins/` or `community-plugins.json`. Restricted Mode ON; no shell/JS-executing plugins.
