# Sean Context Transfer - Safe Matt Import Protocol

**Contributor:** Sean  
**Agent:** Codex  
**Timestamp:** 2026-06-07T14:57:35-07:00  
**Topic:** Safe import rules for Matt context and research

## What Changed
- Added a selective import protocol so Sean can fetch and inspect Matt's branch without merging an
  outdated local framework into `main`.
- Defined the files/folders that can be imported from Matt automatically:
  - `docs/session-logs/matt/`
  - `docs/research/matt/`
  - `data/matt/`
  - Matt-owned generated reports when report generation is the stated task
- Defined files/folders that require Sean review before import:
  - shared protocol files (`AGENTS.md`, `MEMORY.md`, `CLAUDE.md`, `GEMINI.md`)
  - scaffold/code files (`src/`, `tests/`, `config/`, `pyproject.toml`, `uv.lock`)
  - agent/tooling files (`.claude/skills/`, `.gemini/`, `.github/`)
  - architecture/scaffold docs (`docs/project/`)
- Updated the context-transfer skill so Matt-owned sessions write detailed handoffs under
  `docs/session-logs/matt/` by default instead of rewriting shared `MEMORY.md`.

## Why It Matters
Sean and Matt can both contribute without accidentally overwriting each other's work. Matt's research
and context remain visible in Obsidian/GitHub, while shared project structure, memory, code, and agent
rules stay protected until Sean reviews them.

## Commands Run
- `git status --short --branch`
- `Get-Content` on `AGENTS.md`, `MEMORY.md`, `docs/project/ONBOARDING_MATT.md`, and
  `.claude/skills/context-transfer/SKILL.md`
- `Get-Date -Format o`

## Next Steps
- Matt should pull the latest `main`, re-read `AGENTS.md` and `MEMORY.md`, then use
  `docs/session-logs/matt/` for session handoffs.
- If Matt's agent wants to change shared memory or scaffold files, it should write a proposal in its
  Matt context-transfer note and wait for Sean review.
