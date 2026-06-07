# CLAUDE.md — website-builder

> **Read [`AGENTS.md`](./AGENTS.md) first — it is the canonical constitution** for this project
> (status, contributors, principles, conventions, memory, tooling, git, session protocol).
> Then read [`MEMORY.md`](./MEMORY.md) for current state.
>
> Do not duplicate constitution content here — update `AGENTS.md` so all agents stay in sync.

---

## Claude-specific notes

- **Skills auto-load** from `.claude/skills/` — currently `context-transfer`, `reference-visualizer`.
  They trigger on phrases (see `AGENTS.md` §4) or proactively. Skills are reactive; `AGENTS.md` is the
  thing you read on entry.
- **Claude private memory** lives at `.claude/projects/<this-project>/memory/` (notes + `MEMORY.md`
  index). This is Claude-only — the **root `MEMORY.md`** is the portable, multi-agent state file and
  takes precedence for shared state.
- **Caveman output mode** may be active (an installed plugin compresses Claude's prose). It does not
  change code/commits, only conversational output.
- **Hard rule reminder:** do NOT build project scaffolding until the `/grill-me` scaffolding session
  has produced an approved structure (see `AGENTS.md` §0).
