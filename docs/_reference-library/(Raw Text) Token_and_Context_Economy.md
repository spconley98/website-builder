---
type: reference
contributors: [sean]
agent: claude
status: active
created: 2026-06-10
updated: 2026-06-10
topic: token-and-context-economy
tags: [reference, tokens, context, agents]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Token & Context Economy — agent standards research

**One-paragraph summary.** Token/context-conservation playbook for `website-builder` agents
(Claude Code, Gemini/Antigravity, routed Codex), synthesized from the Nate Herk guide (NotebookLM),
official Claude Code best-practices docs, a context-window deep-dive (damiangalarza), and the
Antigravity technical review — then **adversarially stress-tested via three-brain (Gemini)**. Headline
finding: the repo **already implements most of the high-value input-token tricks** (lean per-turn
pointers, generated `_HOT.md` digest, `MEMORY.md` handoff, CLI-over-MCP, single source of truth), so
the real wins are NOT more influencer micro-rules — they are **(1) output-token discipline (patch-edit,
never full-file rewrite)** and **(2) exclusion guardrails (never let `uv.lock` / `leads.jsonl` /
`.pytest_cache` / `.venv` enter context)**. Reference doc, not a decision — per AGENTS.md §4, anything
adopted as a standard must be promoted into `AGENTS.md` deliberately.

> Status: this is reference/inspiration. It is NOT yet wired into `AGENTS.md`. Promote individual
> rules into a future AGENTS.md "Token & context economy" section only by explicit decision.

---

## 1. Why this matters (the constraint)

Every best practice descends from one fact: **the context window fills fast and model quality
*degrades* as it fills** ("lost-in-the-middle" — models weight the start and end, neglect the middle).
A 1M-token window (Opus 1M, Antigravity/Gemini 3 native 1M) is **insurance, not a target** — needle-in-
haystack degradation persists regardless of headline size. Code is token-dense (~3-4 chars/token, more
for identifiers/syntax), so file reads burn context faster than prose.

---

## 2. What the repo ALREADY does right (don't re-invent)

Verified against `AGENTS.md` §5 + tooling. These match the research; codify, don't re-add:

| Practice | Where it lives | Research backing |
|---|---|---|
| Thin per-turn files | `CLAUDE.md`/`GEMINI.md` are pointers; `AGENTS.md` read-once at entry | Herk "CLAUDE.md as router"; official "keep it short" |
| Cheap cold-start digest | generated `_HOT.md` (~500 words, `stale_after`) | Herk "session handoff" pattern |
| Persistent handoff > recompaction | `context-transfer` + `MEMORY.md` + NotebookLM mirror | Herk session-handoff; official `/clear`+spec |
| Single source of truth | `MEMORY.md` (state), `AGENTS.md` (rules) | avoids summarize-of-summary rot |
| CLI over MCP | NotebookLM CLI, `leadpipe` CLI, `gh`; Firecrawl = only MCP | official "CLI is most context-efficient" |
| Cross-arch challenge | `three-brain` (Gemini long-ctx, Codex review) | subagent isolation principle |
| Surgical reads baseline | grep/Glob/line-range tooling | universal agent hygiene |

**Implication:** the marginal value of bolting on more input-token rules is LOW. The repo is already lean.

---

## 3. Stress-tested game plan (graded)

Each item carries the three-brain verdict. **KEEP** = evidence-backed + non-redundant. **REVISE** =
true but the influencer framing was wrong. **CUT** = cargo-cult / micromanagement / redundant.

### KEEP (adopt as-is)
- **Markdown everywhere.** Convert any PDF/DOCX/HTML reference to `.md` before feeding an agent
  (HTML→MD ~90% fewer tokens, PDF→MD 65-70%, DOCX 33%). Repo is already `.md`-native.
- **Surgical file references.** `@file` + explicit line ranges; grep/Glob to narrow candidates
  *before* reading. Never "read the whole service to find one function."
- **Skills over MCP for optional capability.** Progressive disclosure: a skill costs ~200 tokens at
  startup (name+description) and only loads its body on invocation, vs an MCP server paying its full
  tool-schema cost every turn just by existing.
- **Multi-model routing (three-brain).** Gemini for long-context/whole-repo/media; Codex for
  independent review (no-self-review law). Routes heavy reads OUT of the main thread.
- **Prefix-cache mechanics.** Cache reads ~10x cheaper; ~1hr TTL. **Don't switch models mid-session**
  and **don't edit early-context files (`AGENTS.md`/`CLAUDE.md`) mid-session** — both invalidate the
  downstream cache and force a full re-read.
- **1M ≠ garbage dump.** Front-load critical instructions; never assume the big window forgives
  dumping the monorepo.

### REVISE (true, but the framing was wrong)
- **Context budget — by DEGRADATION, not a number.** Drop the cargo-culted "120k/12% hard cap."
  Prefix caching makes deep context cheap, and agentic coding often *needs* the full thread (file deps,
  test output). Trigger a reset on **symptoms** (forgets earlier decisions, repeats done work, re-asks
  answered questions, contradicts itself), not at an arbitrary token line. Official guidance explicitly
  says "sometimes let context accumulate."
- **MCP is not the enemy anymore.** The "ditch MCP / 35x" claim is **dated**: Anthropic's advanced
  tool use + tool-search / deferred (lazy) tool loading mean schemas no longer clog the active window
  (this very harness loads tools on demand). Real cost is now init + cache-miss, not constant drag.
  Revised rule: **don't pile up unused MCP servers; disconnect idle ones** — but don't abandon MCP over
  ~15k tokens when no CLI exists.
- **Cheap-model offload — extraction only.** Using Haiku (or any small model) for heavy reads is fine
  for **raw extraction / summarization**, a real quality risk for **code-dependency mapping or
  architectural reasoning** (shallow/hallucinated summaries poison the primary agent). Gate by task type.
- **`/rewind` selectively.** Erasing a failed attempt removes context pollution — but also removes the
  agent's memory of *what not to do*. Use it for context-polluting loops (2+ failed corrections), not
  reflexively on every miss.
- **Antigravity artifacts → repo, without duplication.** Map Antigravity's auto-generated markdown
  (task lists/plans/walkthroughs) into `docs/session-logs/<contributor>/`, but `MEMORY.md` stays the
  absolute single source of truth — artifacts are derived, not a second authority.

### CUT (cargo-cult / micromanagement / redundant)
- **Manual `/compact` at 60%.** Micromanagement; risks stripping implicit reasoning. Let auto-compaction
  handle it, and only reach for `/compact <preserve…>` when *deliberately* transitioning between phases.
- **Rigid "95% confidence gate."** Misunderstands the agentic loop (iterate / test / fail-fast). Keep
  **plan mode for multi-file or uncertain changes** (official: skip it when the diff fits one sentence),
  but drop the rigid confidence-percentage framing.
- **AGENTS.md router refactor — defer.** Splitting `AGENTS.md` into index+linked docs is premature for
  a ~334-line file read once per session. Revisit only if it actually bloats.

---

## 4. The two MISSING levers (highest value — surfaced by stress test)

The original draft fixated on **input** tokens. Both gaps below outrank everything in §3:

1. **Output-token economy.** Output tokens are costlier and slower than input. The agentic-coding
   bottleneck is **full-file rewrites**. Standard: **patch/diff editing (targeted `Edit`/replace) over
   regenerating whole files**; ask for the minimal diff, not the whole module.
2. **Exclusion guardrails.** The fastest way to blow a budget is not a long chat — it's one agent
   `cat`-ing a generated/data file. Standard: enforce ignore lists (`.gitignore`, plus
   `.geminiignore` / `.aiexclude` for Matt's Gemini/Antigravity) so agents never swallow
   `uv.lock`, `.venv/`, `.pytest_cache/`, `data/**/leads.jsonl`, build artifacts, or large reports.

---

## 5. Per-agent cheat sheet

**Claude Code (Sean)**
- `/context` at session start to baseline; reset on degradation symptoms, not a token number.
- `/clear` between unrelated tasks; `/rewind` only for failed-correction loops.
- Subagents/Explore for heavy reads — return summaries, keep main thread clean.
- Edit = minimal patch, never full-file rewrite.

**Gemini / Antigravity (Matt)**
- 1M native context ≠ dump the repo; front-load instructions.
- Agent Manager swarms = parallel isolated sub-agents (same context-isolation benefit as subagents).
- Land artifacts in `docs/session-logs/matt/`; `MEMORY.md` stays SoT.
- Add `.geminiignore` / `.aiexclude` mirroring `.gitignore`.

**Codex (routed review)**
- Independent reviewer (no-self-review). Sees the diff, not the reasoning.
- Note: current `~/.codex/config.toml` has `service_tier = default` — **invalid** for codex-cli 0.128
  (expects `fast`/`flex`, account rejects both). Codex review/rescue routes are **down until fixed**.

---

## 6. Bottom line

For a small Python CLI, **most of this is already handled or unnecessary.** Adopt the cheap universal
wins (markdown, surgical reads, skills-over-MCP, cache discipline) and the **two missing levers
(patch-edit output, exclusion guardrails)**. Drop the influencer numerology (120k cap, 60% compact,
95% gate). Don't micromanage the agent into a procedural script — its value is iterative self-correction.

---

## Sources
- Nate Herk guide — NotebookLM `NATE HERK GUIDE` (191dfe34)
- Claude Code best practices — https://code.claude.com/docs/en/best-practices
- Context-window deep-dive — https://www.damiangalarza.com/posts/2025-12-08-understanding-claude-code-context-window/
- Antigravity technical review — https://www.remio.ai/post/google-antigravity-technical-review-the-first-true-agentic-ide-powered-by-gemini-3-pro
- Adversarial stress test — Gemini 2.5 Pro via `three-brain`, logged at `three-brain-out/2026-06-10-token-economy/`
