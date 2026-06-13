# Graph Report - .  (2026-06-13)

## Corpus Check
- 142 files · ~1,450,569 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 799 nodes · 1480 edges · 39 communities (37 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 196 edges (avg confidence: 0.67)
- Token cost: 49,346 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Agent Code & Doc Bridges|Agent Code & Doc Bridges]]
- [[_COMMUNITY_Typer CLI Commands|Typer CLI Commands]]
- [[_COMMUNITY_Reports & Industry Grouping|Reports & Industry Grouping]]
- [[_COMMUNITY_Lead Hunts & Sync|Lead Hunts & Sync]]
- [[_COMMUNITY_Governance & Constitution|Governance & Constitution]]
- [[_COMMUNITY_Obsidian Vault Maintenance|Obsidian Vault Maintenance]]
- [[_COMMUNITY_Token Economy & Past Mistakes|Token Economy & Past Mistakes]]
- [[_COMMUNITY_Session Logs & Foundation Sync|Session Logs & Foundation Sync]]
- [[_COMMUNITY_AI Build Bible (Architecture)|AI Build Bible (Architecture)]]
- [[_COMMUNITY_AI Skills & MCP Blueprint|AI Skills & MCP Blueprint]]
- [[_COMMUNITY_Leadpipe Agent Strategy (Visual)|Leadpipe Agent Strategy (Visual)]]
- [[_COMMUNITY_Project Architecture Overview|Project Architecture Overview]]
- [[_COMMUNITY_AI Build Bible Frameworks|AI Build Bible Frameworks]]
- [[_COMMUNITY_AI Skills Catalog (Mind Map)|AI Skills Catalog (Mind Map)]]
- [[_COMMUNITY_Agent Base & Lead Finder|Agent Base & Lead Finder]]
- [[_COMMUNITY_Pipeline Runner & Targets|Pipeline Runner & Targets]]
- [[_COMMUNITY_Agent Contract Tests|Agent Contract Tests]]
- [[_COMMUNITY_NotebookLM Insights Index|NotebookLM Insights Index]]
- [[_COMMUNITY_Lead Prioritizer Internals|Lead Prioritizer Internals]]
- [[_COMMUNITY_Local AI Agents (Leadpipe)|Local AI Agents (Leadpipe)]]
- [[_COMMUNITY_Session Protocol Guides|Session Protocol Guides]]
- [[_COMMUNITY_Sell Methodology & Tiered LLM|Sell Methodology & Tiered LLM]]
- [[_COMMUNITY_MCP Server Database|MCP Server Database]]
- [[_COMMUNITY_AI Skills Blueprint|AI Skills Blueprint]]
- [[_COMMUNITY_Stage Architecture & Data Contracts|Stage Architecture & Data Contracts]]
- [[_COMMUNITY_Multi-Brain Agent Strategy|Multi-Brain Agent Strategy]]
- [[_COMMUNITY_Context Rot & Model Routing|Context Rot & Model Routing]]
- [[_COMMUNITY_Custom SDKs & Private MCPs|Custom SDKs & Private MCPs]]
- [[_COMMUNITY_AI Agent & Model Database|AI Agent & Model Database]]
- [[_COMMUNITY_Project Structuring Guide|Project Structuring Guide]]
- [[_COMMUNITY_Agent Protocol Contract|Agent Protocol Contract]]
- [[_COMMUNITY_Lead Scoring Functions|Lead Scoring Functions]]
- [[_COMMUNITY_Photo-Count Estimation|Photo-Count Estimation]]
- [[_COMMUNITY_Google Places Tests|Google Places Tests]]
- [[_COMMUNITY_Matt Branch Sync Audit|Matt Branch Sync Audit]]

## God Nodes (most connected - your core abstractions)
1. `LeadStore` - 50 edges
2. `load_settings()` - 25 edges
3. `Lead` - 24 edges
4. `Lead` - 23 edges
5. `The Complete AI Build Bible` - 23 edges
6. `LeadStatus` - 21 edges
7. `AGENTS.md Constitution` - 20 edges
8. `AgentResult` - 19 edges
9. `Target` - 19 edges
10. `LeadCreate` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Tiered-LLM pattern (A1, Nate Herk-derived)` --semantically_similar_to--> `No-self-review law (three-brain reciprocal routing)`  [INFERRED] [semantically similar]
  src/leadpipe/agents/website_intelligence.py → AGENTS.md
- `Website Intelligence — turns prioritized leads into build/sales briefs.  This is` --shares_data_with--> `leadpipe vault (validate/heartbeat/hot)`  [AMBIGUOUS]
  src/leadpipe/agents/website_intelligence.py → AGENTS.md
- `Lead Finder Agent` --implements--> `Lead Finder — finds local businesses with no website (ARCHITECTURE.md §3).  Divi`  [INFERRED]
  docs/project/ARCHITECTURE.md → src/leadpipe/agents/lead_finder.py
- `SELL_METHODOLOGY (C1, Nate Herk framework)` --references--> `Website Intelligence — turns prioritized leads into build/sales briefs.  This is`  [INFERRED]
  MEMORY.md → src/leadpipe/agents/website_intelligence.py
- `Website Intelligence Agent` --implements--> `Website Intelligence — turns prioritized leads into build/sales briefs.  This is`  [INFERRED]
  docs/_reference-library/(Raw Text) Local_AI_Agents_for_Leadpipe.md → src/leadpipe/agents/website_intelligence.py

## Import Cycles
- 1-file cycle: `src/leadpipe/llm.py -> src/leadpipe/llm.py`

## Hyperedges (group relationships)
- **Graphify bridges stitch sell-methodology docs to website-intelligence code** — agents_knowledge_graph_graphify, agents_graph_bridges, sell_methodology, agents_website_intelligence [INFERRED 0.85]
- **Tiered-LLM escalation produces sell-methodology briefs** — agents_website_intelligence, agents_website_intelligence_rationale_1, tiered_llm_pattern, agents_website_intelligence_system_prompt, sell_methodology [INFERRED 0.85]
- **Cold-start read-path and authority model anchor on MEMORY.md** — agents_cold_start_read_path, agents_authority_model, agents_memory_md, agents_hot_md [EXTRACTED 0.75]

## Communities (39 total, 2 thin omitted)

### Community 0 - "Agent Code & Doc Bridges"
Cohesion: 0.05
Nodes (69): Curated doc-code bridges (bridges.json / apply_bridges.py), Knowledge graph (graphify) — query before you grep, compact_scraped_content(), Helpers for keeping scraped listing content safe for local LLM prompts., Bound scraped content while preserving the top, useful snippets, and tail., _build_prompt(), _fallback_intelligence(), _generate_intelligence() (+61 more)

### Community 1 - "Typer CLI Commands"
Cohesion: 0.05
Nodes (67): check(), find(), intelligence(), _print_report(), prioritize(), _profile_or_exit(), leadpipe — the Matt-friendly entry point (ARCHITECTURE.md §8).      leadpipe f, Run Lead Finder on prompt only — default cap is 20 candidates per industry. (+59 more)

### Community 2 - "Reports & Industry Grouping"
Cohesion: 0.08
Nodes (65): BaseModel, TargetsFile, _CategoriesFile, CategoryRule, industry_group(), load_industry_categories(), Broad-category groupings for Lead.industry, used to render collapsible sections, Returns (category rules, other_label). Missing/empty file -> no rules,     every (+57 more)

### Community 3 - "Lead Hunts & Sync"
Cohesion: 0.05
Nodes (63): matt-wip-2026-06-09 Branch, Matt WIP Push + Context Transfer Session, AGENTS.md (constitution), Asset Provenance Model (sister sell repo), asyncio + httpx.AsyncClient Refactor, Authority Model (source-of-truth per concern), CA Nursery Leads Hunt, config/ca_small_towns.yaml (reference menu) (+55 more)

### Community 4 - "Governance & Constitution"
Cohesion: 0.06
Nodes (52): Agent run safety (no autonomous scraping, 20-cap, profile isolation), Authority model (single owner per current-truth), Cold-start read-path, AGENTS.md Constitution, Firecrawl MCP + REST fallback, Note frontmatter schema (leadpipe vault validate), _HOT.md (generated digest), Hunt operations rhythm (+44 more)

### Community 5 - "Obsidian Vault Maintenance"
Cohesion: 0.09
Nodes (42): allowlisted_notes(), check_note(), extract_wikilinks(), _first_heading(), heartbeat(), hot(), _is_date(), is_resolvable() (+34 more)

### Community 6 - "Token Economy & Past Mistakes"
Cohesion: 0.08
Nodes (34): Don't Treat Agents as Rigid Procedural Scripts, Prefer CLI over MCP (~35x efficiency), 120k/12% Context Budget Hard-Cap, Exclusion Guardrails (.gitignore/.geminiignore/.aiexclude), Gemini 2.5 Pro Adversarial Review (token economy), Haiku for Heavy-Read Subagents, Token-Economy Game Plan (stress-test input), Output-Token Economy (patch/diff over full rewrites) (+26 more)

### Community 7 - "Session Logs & Foundation Sync"
Cohesion: 0.08
Nodes (31): Matt Session Logs Index, ELI5 Agent Prompt Guides for Matt, Agent Prompt Guides + Industry Grouping, docs/project/ARCHITECTURE.md, Canonical Foundation Sync, Canonical Obsidian-Facing Structure, Context Transfer Wrap-Up (Protocol Hardening), Context Transfer NotebookLM/Obsidian Cleanup (+23 more)

### Community 8 - "AI Build Bible (Architecture)"
Cohesion: 0.08
Nodes (28): The Architect — Claude 4.7 (UI/UX, Design, Complex Reasoning), 80% Cost Reduction (vs All-Premium Models), AI Build Bible (Visualization Image), Layer 1: Infrastructure & Context, Layer 2: Agentic Control, Layer 3: The Model Brain, The Muscle — DeepSeek V4 (Background & Data Processing), The Reviewer — Codex (GPT-5.5) (Final Code Review & Error Detection) (+20 more)

### Community 9 - "AI Skills & MCP Blueprint"
Cohesion: 0.08
Nodes (27): CLAUDE.md Project Constitution, Big Three Instruction Files (CLAUDE/GEMINI/MEMORY.md), BLAST System Prompt, The Blueprint of AI-Assisted Development, GSD Orchestration Framework, Comprehensive AI Skills (Infographic), PIV Execution Loop, Site / Pages Workflow (+19 more)

### Community 10 - "Leadpipe Agent Strategy (Visual)"
Cohesion: 0.11
Nodes (21): Core Implementation Principles, Document-Based Memory, Framework Minimalism, Large Quantized Model, Local Intelligence Tiering (RTX 3090), Mid-Tier Local Model, Build Agents as Pipeline Stages, Separation of Facts and Judgment (+13 more)

### Community 11 - "Project Architecture Overview"
Cohesion: 0.13
Nodes (20): Small-Town-First Targeting, Leadpipe Working Context, The agent contract every pipeline stage implements (ARCHITECTURE.md §3).  Delibe, Lead Finder — finds local businesses with no website (ARCHITECTURE.md §3).  Divi, Lead Prioritizer — rates leads by how much photo material exists online (ARCHITE, The thin runner — orders agents over targets (ARCHITECTURE.md §3).  Deliberately, Project Deep Dive Report, Cold-Start Read-Path (+12 more)

### Community 12 - "AI Build Bible Frameworks"
Cohesion: 0.12
Nodes (18): AI Build Bible (Mind Map), Apple-Style Scroll Animation (Frame Sequence), Clone Site Skill, CODA Framework, The Complete AI Build Bible, DRIP Framework, FLOW Framework, Glassmorphism (+10 more)

### Community 13 - "AI Skills Catalog (Mind Map)"
Cohesion: 0.14
Nodes (17): Comprehensive AI Skills (Mind Map), Master Skills Catalog (Mind Map), GSD (Get Shit Done) Framework, Screenshot Loop Workflow, Browser-in-the-Loop Testing, CEO System (Daily Brief), Comprehensive AI Skills & Workflows Database, Graphify (Codebase Knowledge Graph) (+9 more)

### Community 14 - "Agent Base & Lead Finder"
Cohesion: 0.17
Nodes (15): AgentResult, AgentResult, _normalize_industry(), LLM reasoning step — degrades to the raw search term on any LLM failure., run(), _listing_urls(), run(), LeadStore (+7 more)

### Community 15 - "Pipeline Runner & Targets"
Cohesion: 0.17
Nodes (15): Target, Run a single named stage across every target., Run every stage, in pipeline order, across every target., CLI-flag override vs config-file batch list (ARCHITECTURE.md §8):     explicit -, resolve_targets(), run_all(), run_stage(), RunReport (+7 more)

### Community 16 - "Agent Contract Tests"
Cohesion: 0.13
Nodes (8): Tests for the agent contract and the deterministic rating function.  The rating, A1 tiering: when the fast model fails (timeout/garbage), the retry must use the, A1 tiering for Agent 3: fast failure escalates to the deep model, which can then, C1: the brief's selling voice must be ROI/leverage-anchored, not generic., test_blank_llm_env_values_fall_back_to_defaults(), test_estimate_photo_count_escalates_to_deep_model_on_failure(), test_intelligence_system_prompt_carries_leverage_frame(), test_website_intelligence_escalates_to_deep_model_before_fallback()

### Community 17 - "NotebookLM Insights Index"
Cohesion: 0.15
Nodes (14): Matt Research (folder note), NotebookLM Insights Index, AI Build Bible Guide, BLAST Framework, Context Rot, AI Skills Guide, Plan-Implement-Validate Loop, Custom SDKs Guide (+6 more)

### Community 18 - "Lead Prioritizer Internals"
Cohesion: 0.18
Nodes (12): _credit_pause_error(), _gather_listing_urls(), _matches_target(), Returns [(source_label, url), ...] to enrich from. Prefers URLs Lead     Finder, Scope found leads to the requested target. Google Places addresses start     wit, None means proceed (or "can't tell, don't block"). A string is the     reason to, run(), AgentResult (+4 more)

### Community 19 - "Local AI Agents (Leadpipe)"
Cohesion: 0.21
Nodes (12): Local AI Agents for Leadpipe (Mind Map), Custom Agent Stage Pattern, Local AI Agents for Leadpipe, APIs Acquire Facts, LLMs Reason, Store Enforces Boundary, LangGraph, Lead Enrichment Agent, leadpipe Pipeline, Ollama (local model surface) (+4 more)

### Community 20 - "Session Protocol Guides"
Cohesion: 0.24
Nodes (11): context-transfer Skill, Agent Prompt Guide (End Session), Wrap Up Session Protocol, Matt Getting Up To Date (Sync), Stale Working-Copy Protocol, Agent Prompt Guide (Start Session), website-builder-brain NotebookLM, Obsidian .obsidian Trust Boundary (+3 more)

### Community 21 - "Sell Methodology & Tiered LLM"
Cohesion: 0.22
Nodes (10): No-self-review law (three-brain reciprocal routing), Website Intelligence — turns prioritized leads into build/sales briefs.  This is, SELL_METHODOLOGY (C1, Nate Herk framework), MONEY Framework (agency sales), Core Value Story (capture existing demand), Nate Herk Frameworks, Sell Methodology, 3 Leverage Tests (lead qualification) (+2 more)

### Community 22 - "MCP Server Database"
Cohesion: 0.22
Nodes (10): Comprehensive MCP Database (Mind Map), 3-Tier Memory Architecture, Context 7 MCP, Comprehensive MCP Server & Tool Database, Firecrawl MCP, Model Context Protocol (MCP), NotebookLM (knowledge backbone), Pinecone Vector DB (+2 more)

### Community 23 - "AI Skills Blueprint"
Cohesion: 0.22
Nodes (9): Anatomy of a 'Skill' (SKILL.md), Context Rot Defense, Design & UI Intelligence, Fundamentals & Architecture, Gen-Media & Fal.ai, Global vs. Local Scopes, Specialized Skill Families, Three Installation Paths (+1 more)

### Community 24 - "Stage Architecture & Data Contracts"
Cohesion: 0.22
Nodes (9): Proposed Targets from Matt Onboarding Branch, Local AI Agents for Leadpipe Guide, Pydantic Data Contracts, Simple Stage-Based Architecture, Apprentice / Manager Model, File-Based Pipeline Orchestration, JSONL Source-of-Truth + Markdown Views, Karpathy Simplicity-First Principles (+1 more)

### Community 25 - "Multi-Brain Agent Strategy"
Cohesion: 0.22
Nodes (9): AI Agents Database Guide, Antigravity Orchestration Framework, Multi-Brain Model Strategy, IPv6 DNS API Hang Bugfix, Master Notebook Summary, SITE Framework, 16 Texas Cities Hunt (166 leads), Three-Brain 80/20 Model Routing (+1 more)

### Community 26 - "Context Rot & Model Routing"
Cohesion: 0.25
Nodes (9): Context Rot, Lost in the Middle, Reset by Degradation Symptoms (not token cap), Token & Context Economy, Exclusion Guardrails (ignore lists), No-Self-Review Law, Output-Token Economy (patch-edit not rewrite), Prefix-Cache Discipline (+1 more)

### Community 27 - "Custom SDKs & Private MCPs"
Cohesion: 0.25
Nodes (8): BIBLE Custom SDKs and Proprietary Logic (Mind Map), ACE Framework, AI-First SDK / Agent-Computer Interface (ACI), Custom SDKs, Private MCPs & Proprietary Tooling, FastMCP, Portable / Private MCP Servers, STAND Framework, Stdio Transport (Zero-Network MCP)

### Community 28 - "AI Agent & Model Database"
Cohesion: 0.29
Nodes (8): Comprehensive AI Agents Database (Mind Map), Three Brain System, Google Antigravity IDE, Comprehensive AI Agent & Model Database, Hybrid Multi-Agent Workflow (Planner/Coder/Refiner), Mission Control (Agent Manager), Model Routing Strategy (80/20 Rule), Claude Code Router

### Community 29 - "Project Structuring Guide"
Cohesion: 0.33
Nodes (7): Comprehensive Project Structuring Guide (Mind Map), BLAST Framework, Comprehensive Guide to Project Structuring & Context Management, Karpathy Method (Vibe Coding), Negative Constraints (NEVER rules), See-Say-Run Loop, Karpathy Principles (operating rules)

### Community 30 - "Agent Protocol Contract"
Cohesion: 0.33
Nodes (5): Agent, Do the agent's job for one target (one area + one industry list),         writin, Protocol, LeadStore, Target

### Community 31 - "Lead Scoring Functions"
Cohesion: 0.33
Nodes (6): rate_from_count(), Deterministic 1-5 (or 0) rating from a photo count. Pure + tunable —     the onl, Deterministic lead score from buildability + reachability signals.     Unknown l, score_from_signals(), test_rate_from_count_thresholds(), test_score_from_signals_uses_soft_penalties()

### Community 32 - "Photo-Count Estimation"
Cohesion: 0.40
Nodes (5): _estimate_photo_count(), _parse_photo_count_response(), Parse the strict two-line LLM output for photo-count estimates., LLM reasoning step over scraped page content. Raises LLMError on failure     or, test_parse_photo_count_response()

## Ambiguous Edges - Review These
- `Website Intelligence — turns prioritized leads into build/sales briefs.  This is` → `leadpipe vault (validate/heartbeat/hot)`  [AMBIGUOUS]
  src/leadpipe/agents/website_intelligence.py · relation: shares_data_with

## Knowledge Gaps
- **130 isolated node(s):** `LeadStore`, `Target`, `Path`, `date`, `Pending Approvals queue (Sean-only approval)` (+125 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Website Intelligence — turns prioritized leads into build/sales briefs.  This is` and `leadpipe vault (validate/heartbeat/hot)`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **Why does `Website Intelligence — turns prioritized leads into build/sales briefs.  This is` connect `Sell Methodology & Tiered LLM` to `Agent Code & Doc Bridges`, `Local AI Agents (Leadpipe)`, `Project Architecture Overview`, `Governance & Constitution`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._
- **Why does `Website Intelligence Agent` connect `Local AI Agents (Leadpipe)` to `Sell Methodology & Tiered LLM`?**
  _High betweenness centrality (0.223) - this node is a cross-community bridge._
- **Why does `Master Skills Catalog` connect `AI Skills Catalog (Mind Map)` to `Project Structuring Guide`, `Local AI Agents (Leadpipe)`, `AI Build Bible Frameworks`, `AI Agent & Model Database`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `LeadStore` (e.g. with `RunReport` and `Lead`) actually correct?**
  _`LeadStore` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Lead` (e.g. with `Lead` and `LeadStatus`) actually correct?**
  _`Lead` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Lead` (e.g. with `LeadStore` and `Lead`) actually correct?**
  _`Lead` has 14 INFERRED edges - model-reasoned connections that need verification._