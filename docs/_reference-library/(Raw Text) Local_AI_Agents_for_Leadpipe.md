# Local AI Agents for Leadpipe

> Research synthesis for `website-builder` / `leadpipe`.
> Prepared for Sean on 2026-06-07 from the `JACK AI UPDATED` NotebookLM brain plus 12 Firecrawl-scraped external resources.
> This is reference material only, not an implementation plan or scaffold change.

---

## Executive take

The best near-term agent strategy for `leadpipe` is not to adopt a heavy agent framework yet.
The repo already has the right v1 shape: a file-based Python pipeline, explicit Pydantic data
contracts, stage-scoped store writes, generated reports, and clear human-readable memory.

For the current project, custom agents should be built as small, testable pipeline stages:

1. One module in `src/leadpipe/agents/`.
2. One stage registration in `pipeline.STAGES`.
3. One stage-specific Pydantic input/output model.
4. Store writes through explicit allowlisted methods.
5. Tests for the contract, idempotency, and failure/degradation behavior.

Frameworks like LangGraph, CrewAI, AutoGen, PydanticAI, smolagents, LiteLLM, Qdrant, DSPy, and Ragas
are useful, but they should be pulled in for specific pressure points rather than because the word
"agent" appears in the project.

Recommended default:

- Keep `leadpipe` orchestration simple for now.
- Use Ollama's OpenAI-compatible API as the local model surface.
- Use local models on the RTX 3090 for routine classification, extraction, summarization, and scoring.
- Use Firecrawl for web search/scrape/extract enrichment, now that credits are active.
- Add agent #3 as a normal `leadpipe` stage before adding any framework.
- Revisit PydanticAI or LangGraph only after 2-3 real hunts reveal repeated branching, tool-calling, or structured-output pain.

---

## Project fit

`website-builder` is a local-AI lead pipeline. It finds local businesses with no website, prioritizes
them by available online photo material, and produces clickable lead lists so Sean and Matt can build
and sell websites.

Current live architecture:

- Python / `uv`.
- Typer CLI: `find`, `prioritize`, `run`, `report`.
- Google Places is the fact source for "has website".
- Firecrawl is the web enrichment source.
- Ollama is the local reasoning endpoint.
- `data/leads.jsonl` is the source of truth.
- Reports are generated Markdown.
- NotebookLM and Obsidian are knowledge/memory surfaces.

The core principle to preserve:

> APIs acquire facts. LLMs reason over facts. The store enforces the boundary.

---

## RTX 3090 implications

Sean's RTX 3090 has 24 GB VRAM. That is enough for serious local inference, but not unlimited.

Practical routing tiers:

| Tier | Good local use | Notes |
|---|---|---|
| Small local model | Fast category cleanup, short extraction, simple JSON repair | Use for cheap, repeated work. |
| Mid local model | Lead summaries, photo reasoning, competitive notes | Likely the daily driver tier. |
| Larger quantized model | Harder synthesis, multi-step business reasoning | Use selectively; slower, watch context size. |
| Cloud/human review | High-value strategy, final outreach language, tricky failures | Optional, not a baseline requirement. |

Do not make the model router complicated before the workflow exists. Start with one reliable local
model in `.env`, then add task-specific routing only when the workload proves it needs it.

Suggested task split:

- `Lead Finder` industry normalization: small/mid local model.
- `Lead Prioritizer` photo-count reasoning: mid local model.
- Future `Website Intelligence` competitor synthesis: mid/large local model.
- Future `Outreach Prep`: mid/large local model, optionally reviewed by Sean before sending.
- Future `QA Reviewer`: deterministic checks first, LLM second.

---

## What the Jack AI notebook contributed

Notebook: `JACK AI UPDATED`

Most relevant themes:

- **Local/free model workflows:** use Ollama/local models for the 80 percent of repeated tasks that
  do not need premium reasoning.
- **Routing mindset:** reserve expensive or highest-intelligence models for the hard 20 percent.
- **Firecrawl as an agent tool:** use it to turn messy web pages into AI-ready content for research,
  website intelligence, competitor review, and lead enrichment.
- **Long-term memory:** use a layered memory system rather than trusting any single chat session:
  project files, session wrap-ups, NotebookLM, Obsidian, and eventually vector search if needed.
- **Custom skills/agents:** build reusable capabilities with clear trigger conditions, required
  inputs, output shape, and tool permissions.
- **Agentic OS/self-improvement loop:** periodically review repeated manual work and turn it into
  a skill or agent once the pattern is real.

Project translation:

- `AGENTS.md` + `MEMORY.md` are already the "constitution + memory" layer.
- Obsidian is already the human visual layer.
- NotebookLM is already the research synthesis layer.
- `leadpipe` agents should become the production automation layer.
- Avoid building an elaborate "agentic OS" until lead hunts produce enough repeated manual friction.

---

## Firecrawl research resources

The following 12 resources were retrieved with Firecrawl on 2026-06-07. Preference was given to
official documentation and durable project pages.

| # | Resource | Why it matters for `leadpipe` |
|---|---|---|
| 1 | [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility) | Confirms `leadpipe.llm` can keep using the OpenAI client against local Ollama. |
| 2 | [vLLM documentation](https://docs.vllm.ai/en/latest/) | High-throughput serving option if local inference becomes a bottleneck. Not needed for v1. |
| 3 | [LiteLLM documentation](https://docs.litellm.ai/docs/) | Unified model interface, routing, retries, fallbacks, cost tracking, and proxy gateway. |
| 4 | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Low-level orchestration for long-running, stateful agents when simple stages are no longer enough. |
| 5 | [CrewAI introduction](https://docs.crewai.com/introduction) | Multi-agent teams and structured flows; useful if roles need to collaborate. |
| 6 | [Microsoft AutoGen](https://microsoft.github.io/autogen/stable/) | Conversational single/multi-agent app framework and prototyping UI. |
| 7 | [PydanticAI agents](https://ai.pydantic.dev/agents/) | Strong fit for typed agents, tools, dependencies, and structured outputs in a Pydantic-heavy repo. |
| 8 | [Hugging Face smolagents](https://huggingface.co/docs/smolagents/index) | Lightweight code/tool agents for experiments and local/open-model workflows. |
| 9 | [Model Context Protocol introduction](https://modelcontextprotocol.io/introduction) | Standard pattern for connecting AI apps to external tools and data sources. |
| 10 | [Firecrawl introduction](https://docs.firecrawl.dev/introduction) | Search, scrape, crawl, and extract API for AI agents; directly relevant to enrichment agents. |
| 11 | [Qdrant overview](https://qdrant.tech/documentation/overview/) | Vector memory/search option if NotebookLM/files stop being enough. |
| 12 | [DSPy](https://dspy.ai/) | Framework for programming and optimizing LLM behavior with signatures instead of prompt sprawl. |

Extra useful resource gathered but not counted in the 12:

- [Ragas](https://docs.ragas.io/en/stable/) - systematic LLM app evaluation loops.

---

## Tool-by-tool recommendation

### Ollama

Use now.

`leadpipe` already points at Ollama through an OpenAI-compatible endpoint. This is the right local
model surface for the current codebase. It keeps agents provider-agnostic without adding another
framework.

Near-term action:

- Decide the default `LLM_MODEL`.
- Make sure `.env` does not accidentally set a blank model.
- Later, add per-task routing only if needed.

### Firecrawl

Use now.

Firecrawl is directly relevant to lead enrichment. It should power:

- Yelp/Google listing scrape.
- Competitor website search.
- Social/profile discovery.
- Website-intelligence reports.
- Brand/photo/source extraction.

Guardrail:

- Firecrawl findings are evidence. The LLM can summarize or score them, but store writes should keep
  fact fields separate from judgment fields.

### PydanticAI

Most likely first framework to consider, but not required yet.

Why it fits:

- The repo already uses Pydantic models.
- Agents can define instructions, tools, dependencies, and structured output types.
- Good for replacing brittle "parse text response" code with typed outputs.

Adopt when:

- The same LLM-output parsing pattern repeats across 2-3 agents.
- You need stricter structured-output validation than the current thin `llm.generate()` wrapper.

### LangGraph

Defer until orchestration becomes stateful.

Use if future agents need:

- Branching workflows.
- Human approval steps.
- Retries with state.
- Long-running jobs.
- Durable resumability.

Current `leadpipe` does not need it yet.

### CrewAI

Defer.

CrewAI is compelling for collaborative role-based teams, but `leadpipe` is currently a linear pipeline,
not a debate chamber. It may become useful later for a "website opportunity analysis" crew:

- Researcher.
- Competitor analyst.
- Copywriter.
- QA reviewer.

Do not use it for Lead Finder or Lead Prioritizer.

### AutoGen

Use for experiments, not production v1.

AutoGen is strongest when you want conversational multi-agent prototyping. The current project needs
repeatable CLI runs and inspectable files more than agent chat.

### smolagents

Use for experiments or isolated tool agents.

This is attractive for lightweight local experiments, but `leadpipe` already has a simpler stage
contract. Consider it only for throwaway research prototypes.

### LiteLLM

Consider after local model routing decisions.

LiteLLM becomes useful when you want:

- Multiple local/cloud providers behind one interface.
- Retry/fallback policies.
- Cost tracking.
- A local gateway/proxy.

Do not add it until one model is not enough.

### MCP

Use at the agent-tool boundary, not inside every Python stage.

MCP is best for connecting interactive coding agents to tools like Firecrawl, Google Drive, Notion,
or local files. For `leadpipe` runtime code, direct REST/SDK calls are simpler and easier to test.

Current split is good:

- MCP for Claude/Codex/Gemini tool access.
- REST/SDK calls inside `leadpipe` code.

### Qdrant

Defer.

A vector database is useful only after there is too much lead/research memory for JSONL, Markdown,
NotebookLM, and Obsidian to handle. For now, it would add operational weight.

Possible future uses:

- Semantic search across lead notes.
- Reusing outreach lessons.
- Competitor/site pattern library.
- Long-term agent memory outside NotebookLM.

### DSPy

Defer until prompts stabilize.

DSPy is useful when you know the task and want systematic optimization. It is premature while the
pipeline is still discovering the right lead workflow.

Best future use:

- Tune photo-rating prompts against a hand-labeled set.
- Tune outreach-quality prompts against Sean-reviewed examples.

### Ragas

Keep in mind for evaluation.

Ragas is more relevant once `leadpipe` has RAG-like behavior or question-answering over scraped
context. It can support systematic eval loops, but it is not needed for initial lead hunts.

---

## Custom agent pattern for this repo

Use this as the local standard before adopting a framework:

```text
src/leadpipe/agents/<agent_name>.py
  NAME = "<agent_name>"
  run(store: LeadStore, target: Target) -> AgentResult

src/leadpipe/models.py
  <AgentName>Input / <AgentName>Output or stage-specific update model

src/leadpipe/store.py
  apply_<agent_name>_update(update)
  explicit allowlist of fields the agent may write

src/leadpipe/pipeline.py
  STAGES["<stage>"] = <agent_module>

tests/
  contract tests
  degradation tests
  idempotency tests
```

Rules:

- Each agent owns one stage.
- Each stage has a narrow write surface.
- Each LLM response is validated before it touches the store.
- Each external dependency has a graceful skip path.
- Reports are generated views, never source of truth.
- Agents must be re-runnable.

---

## Recommended next custom agents

### 1. Lead Enrichment Agent

Purpose:

- Add contact/social/profile details for leads already found.

Inputs:

- Existing `found` or `prioritized` leads.

Sources:

- Firecrawl search/scrape.
- Google Maps URL.
- Yelp/business directories.

Outputs:

- Contact URL.
- Phone/email if publicly visible.
- Social links.
- Evidence links.
- Confidence score.

Why first:

- It is a natural extension of Firecrawl now that credits are active.
- It improves sales usefulness without changing the core finder.

### 2. Website Intelligence Agent

Purpose:

- Build a short evidence-backed opportunity report for each promising lead.

Inputs:

- Lead record.
- Competitor pages.
- Listing/photo data.

Outputs:

- "Why this business needs a website."
- Competitor patterns.
- Suggested site sections.
- Available assets.
- Sales angle.

Jack notebook fit:

- This is closest to the "Website Intelligence" skill pattern.

### 3. Outreach Prep Agent

Purpose:

- Draft personalized outreach snippets from evidence, not generic cold email.

Outputs:

- One short opener.
- One value proposition.
- One call-to-action.
- Evidence citations.

Guardrail:

- Do not auto-send. Generate drafts only.

### 4. QA / Review Agent

Purpose:

- Review lead records and generated reports for contradictions before Sean sees them.

Checks:

- Does the lead truly have no website?
- Are URLs clickable?
- Does the rating have evidence?
- Did an LLM write unsupported claims?

This can be mostly deterministic before it is LLM-driven.

---

## Process recommendation

For every new agent:

1. Write the data contract first.
2. Define what facts the agent may acquire.
3. Define what judgments the agent may make.
4. Define the store write allowlist.
5. Add fixtures from one real lead.
6. Add tests for the riskiest failure mode.
7. Run a tiny target.
8. Inspect `data/leads.jsonl`.
9. Regenerate reports.
10. Update `MEMORY.md` through `context-transfer`.

This matches the project's Karpathy principles:

- Data first.
- Surgical changes.
- Simplicity first.
- Goal-driven.
- Explore -> plan -> code -> commit.

---

## Suggested plan-mode questions

Use these when moving from research into design:

1. What is agent #3: enrichment, website intelligence, outreach prep, or QA?
2. What exact fields should that agent add to `Lead`?
3. Which fields are facts and which are judgments?
4. What should happen when Firecrawl fails?
5. What model should handle each task on the RTX 3090?
6. Do we need PydanticAI now, or is `llm.generate()` enough for one more agent?
7. What report should Sean/Matt actually want to open after the run?
8. What is the smallest real hunt that proves the agent works?

---

## Bottom-line recommendation

Do not build a generalized autonomous agent system yet.

Build one more custom `leadpipe` agent the same way the first two were built, probably
`lead_enrichment` or `website_intelligence`. Keep the architecture boring, typed, inspectable, and
file-based. Use the RTX 3090 through Ollama for routine reasoning. Use Firecrawl for evidence. Add
PydanticAI or LangGraph only when the third or fourth agent proves the current thin wrapper is too
limited.

