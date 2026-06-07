# GEMINI.md — website-builder

> **Read [`AGENTS.md`](./AGENTS.md) first — it is the canonical constitution** for this project
> (status, contributors, principles, conventions, memory, tooling, git, session protocol).
> Then read [`MEMORY.md`](./MEMORY.md) for current state.
>
> Do not duplicate constitution content here — update `AGENTS.md` so all agents stay in sync.

---

## Gemini-specific notes

- This project is multi-agent (Claude Code, Codex, Gemini). The shared, portable state file is the
  **root `MEMORY.md`** — read it on start, update it on end.
- The scaffold is **built and working** (`leadpipe`, see `MEMORY.md`/`AGENTS.md` §0) — no build gate
  remains. Pick up real work directly.

### One-time setup — get our skills + Firecrawl MCP into Gemini CLI

Gemini doesn't read `.claude/skills/` or `.mcp.json` natively (different conventions/formats —
this is a known gap, not a bug). **Each person runs these once on their own machine**, pointing at
their own clone path (links are absolute-path — not portable, hence not git-tracked):

```powershell
# Skills — link (not copy) so updates to the source stay in sync
gemini skills link "<your-clone-path>\.claude\skills\context-transfer" --scope workspace --consent
gemini skills link "<your-clone-path>\.claude\skills\reference-visualizer" --scope workspace --consent

# Firecrawl MCP — use YOUR OWN key from your local .env (never share/commit it)
gemini mcp add firecrawl npx -y firecrawl-mcp -e "FIRECRAWL_API_KEY=<your-own-key>" --scope user `
  --description "Web scraping/search — Lead Prioritizer enrichment fallback"
```

Verify: `gemini skills list` should show `context-transfer` + `reference-visualizer`;
`gemini mcp list` should show `firecrawl ... Connected`.
