# Gemini 2.5 Pro — Adversarial Review of Token-Economy Game Plan (2026-06-10)

(Codex route unavailable — config.toml `service_tier = default` invalid for codex-cli 0.128; `flex`/`fast` rejected by account. Routed to Gemini instead.)

## Per-conclusion verdicts
1. REVISE — 120k cap arbitrary; caching makes large context cheap, purge only when reasoning degrades.
2. CUT — manual /compact = micromanagement; risks stripping implicit reasoning.
3. KEEP — AGENTS.md router pattern prevents per-turn system-prompt bloat.
4. KEEP — markdown conversion mechanically sound (native doc handling mitigates slightly).
5. KEEP — surgical reads universally mandatory.
6. REVISE — "35x" dated; MCP overhead mitigated by lazy loading + prefix caching.
7. KEEP — Skills progressive disclosure maximizes cache hits.
8. REVISE — Haiku massive quality risk for architectural/logic reads; raw extraction only.
9. KEEP — multi-model routing plays to structural strengths.
10. REVISE — /rewind every failure destroys "what not to do" memory; only for polluting loops.
11. KEEP — MEMORY.md handoff most robust mechanism.
12. CUT — "95% confidence gate" misunderstands agentic iterate/fail-fast workflow.
13. KEEP — prefix-cache mechanics factual.
14. REVISE — Antigravity→MEMORY.md risks state duplication; MEMORY.md stays SoT.
15. KEEP — 1M context not a garbage dump; needle-in-haystack degradation persists.

## Attack answers
- (a) ditch-MCP/35x = DATED. Advanced tool use + deferred loading mean schemas don't clog active window; cost is now init + cache-miss, not active drag. Total abandonment over ~15k tokens = premature optimization.
- (b) 120k/12% = pure cargo-culting. For coding, dropping context under arbitrary threshold is harmful if it loses file deps/test outputs. "Let it accumulate" exists because prefix caching makes deep context cheap.
- (c) Haiku heavy-read = yes, real risk. Fine for summary/regex extraction; terrible at code-dependency mapping / nuanced architecture → shallow/hallucinated summaries fed to primary agent.
- (d) Over-engineering = severely. leadpipe (few dozen files) rarely breaches 200k unless dumping venv/JSONL. Solving hyperscale problem for micro-repo.
- (e) Repo-redundant: #3, #5, #11 already solved by existing architecture.

## Single biggest flaw
Treating agents like rigid procedural scripts. Manual /compact + /rewind-on-failure + 95% gate strip the agent's core value (iterative self-correction). Micromanaging the LLM instead of letting it self-correct.

## What's MISSING
1. **Output-token economy** — plan fixated on INPUT tokens. Output tokens costlier/slower. No directive to enforce patch/diff editing (sed/replace) over full-file rewrites — the actual agentic-coding bottleneck.
2. **Exclusion guardrails** — biggest blowup isn't long convo, it's `cat`-ing an ignored file. No enforcement of `.gitignore`/`.geminiignore`/`.aiexclude` to stop swallowing `uv.lock`, `.pytest_cache`, `leads.jsonl`, `venv`.
