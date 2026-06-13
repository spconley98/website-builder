# Graph Report - .  (2026-06-13)

## Corpus Check
- Large corpus: 142 files · ~1,450,569 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 789 nodes · 1437 edges · 41 communities (39 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 184 edges (avg confidence: 0.66)
- Token cost: 628,598 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Reports & Industry Grouping|Reports & Industry Grouping]]
- [[_COMMUNITY_Governance & Constitution|Governance & Constitution]]
- [[_COMMUNITY_Session Logs & Sync|Session Logs & Sync]]
- [[_COMMUNITY_Obsidian Vault Maintenance|Obsidian Vault Maintenance]]
- [[_COMMUNITY_Lead Hunts & Sourcing|Lead Hunts & Sourcing]]
- [[_COMMUNITY_Typer CLI Commands|Typer CLI Commands]]
- [[_COMMUNITY_Config & Firecrawl Client|Config & Firecrawl Client]]
- [[_COMMUNITY_Lead Store (Persistence)|Lead Store (Persistence)]]
- [[_COMMUNITY_Token Economy & Past Mistakes|Token Economy & Past Mistakes]]
- [[_COMMUNITY_Lead Data Model|Lead Data Model]]
- [[_COMMUNITY_AI Build Bible (Architecture)|AI Build Bible (Architecture)]]
- [[_COMMUNITY_AI Skills & MCP Blueprint|AI Skills & MCP Blueprint]]
- [[_COMMUNITY_Agent Contract Tests|Agent Contract Tests]]
- [[_COMMUNITY_Config Loading & Pipeline Runner|Config Loading & Pipeline Runner]]
- [[_COMMUNITY_Leadpipe Agent Strategy (Visual)|Leadpipe Agent Strategy (Visual)]]
- [[_COMMUNITY_Lead Prioritizer Agent|Lead Prioritizer Agent]]
- [[_COMMUNITY_Agent Base & Lead Finder|Agent Base & Lead Finder]]
- [[_COMMUNITY_AI Build Bible Frameworks|AI Build Bible Frameworks]]
- [[_COMMUNITY_AI Skills Catalog (Mind Map)|AI Skills Catalog (Mind Map)]]
- [[_COMMUNITY_NotebookLM Insights Index|NotebookLM Insights Index]]
- [[_COMMUNITY_Website Intelligence Agent|Website Intelligence Agent]]
- [[_COMMUNITY_Local AI Agents (Leadpipe)|Local AI Agents (Leadpipe)]]
- [[_COMMUNITY_MCP Server Database|MCP Server Database]]
- [[_COMMUNITY_Project Architecture Overview|Project Architecture Overview]]
- [[_COMMUNITY_Session Protocol Guides|Session Protocol Guides]]
- [[_COMMUNITY_Context Rot & Model Routing|Context Rot & Model Routing]]
- [[_COMMUNITY_AI Skills Blueprint|AI Skills Blueprint]]
- [[_COMMUNITY_Stage Architecture & Data Contracts|Stage Architecture & Data Contracts]]
- [[_COMMUNITY_Project Structuring Guide|Project Structuring Guide]]
- [[_COMMUNITY_Multi-Brain Agent Strategy|Multi-Brain Agent Strategy]]
- [[_COMMUNITY_Custom SDKs & Private MCPs|Custom SDKs & Private MCPs]]
- [[_COMMUNITY_AI Agent & Model Database|AI Agent & Model Database]]
- [[_COMMUNITY_Agent Protocol Contract|Agent Protocol Contract]]
- [[_COMMUNITY_Sell Methodology (Nate Herk)|Sell Methodology (Nate Herk)]]
- [[_COMMUNITY_Obsidian Spine & Targeting|Obsidian Spine & Targeting]]
- [[_COMMUNITY_Google Places Tests|Google Places Tests]]
- [[_COMMUNITY_Matt Branch Sync Audit|Matt Branch Sync Audit]]

## God Nodes (most connected - your core abstractions)
1. `LeadStore` - 50 edges
2. `load_settings()` - 25 edges
3. `Lead` - 24 edges
4. `Lead` - 23 edges
5. `The Complete AI Build Bible` - 23 edges
6. `LeadStatus` - 21 edges
7. `AgentResult` - 19 edges
8. `Target` - 19 edges
9. `LeadCreate` - 17 edges
10. `LeadPrioritization` - 17 edges

## Surprising Connections (you probably didn't know these)
- `test_rate_from_count_thresholds()` --calls--> `rate_from_count()`  [INFERRED]
  tests/test_agents.py → src/leadpipe/agents/lead_prioritizer.py
- `test_score_from_signals_uses_soft_penalties()` --calls--> `score_from_signals()`  [INFERRED]
  tests/test_agents.py → src/leadpipe/agents/lead_prioritizer.py
- `test_compact_scraped_content_preserves_head_middle_and_tail()` --calls--> `compact_scraped_content()`  [INFERRED]
  tests/test_agents.py → src/leadpipe/agents/scraped_content.py
- `test_blank_llm_env_values_fall_back_to_defaults()` --calls--> `load_settings()`  [EXTRACTED]
  tests/test_agents.py → src/leadpipe/config.py
- `test_profiles_are_limited_to_known_owners()` --calls--> `normalize_profile()`  [EXTRACTED]
  tests/test_store.py → src/leadpipe/store.py

## Import Cycles
- 1-file cycle: `src/leadpipe/llm.py -> src/leadpipe/llm.py`

## Hyperedges (group relationships)
- **Agent brain authority model (Obsidian primary, NotebookLM mirror)** — agents_authority_model, memory_state, hot_digest, memory_notebooklm_brain, agents_cold_start_read_path [EXTRACTED 1.00]
- **Multi-agent constitution + pointers** — agents_constitution, claude_pointer, gemini_pointer, memory_state [EXTRACTED 1.00]
- **Session protocol skills + vault maintenance** — agents_session_protocol, context_transfer_skill, reference_visualizer_skill, agents_leadpipe_vault [INFERRED 0.85]
- **AI Build Bible Master Frameworks** — raw_text_ai_build_bible_blast_framework, raw_text_ai_build_bible_site_framework, raw_text_ai_build_bible_coda_framework, raw_text_ai_build_bible_gsd_framework [EXTRACTED 0.90]
- **Context-Rot Defense Stack** — raw_text_ai_build_bible_context_rot, raw_text_comprehensive_project_structuring_guide_lost_in_the_middle, raw_text_ai_build_bible_gsd_framework, raw_text_token_and_context_economy_degradation_reset [INFERRED 0.80]
- **Multi-Model Routing Pattern** — raw_text_ai_build_bible_three_brain_system, raw_text_comprehensive_ai_agents_database_model_routing_8020, raw_text_master_skills_catalog_claude_code_router, raw_text_local_ai_agents_for_leadpipe_rtx_3090_routing [INFERRED 0.80]
- **Leadpipe Pipeline: acquire facts then reason locally** — project_architecture_lead_finder_agent, project_architecture_lead_prioritizer_agent, project_architecture_google_places_api, project_architecture_ollama_local_llm, project_architecture_lead_schema [EXTRACTED 0.85]
- **Session Protocol Loop: sync, cold-start, wrap-up** — project_agent_prompt_guide_matt_getting_up_to_date_matt_sync_guide, project_agent_prompt_guide_start_session_start_session_guide, project_agent_prompt_guide_end_session_end_session_guide, project_agent_prompt_guide_end_session_context_transfer_skill [EXTRACTED 0.85]
- **Three-Brain Model Hierarchy: local workhorses, cloud architects, review auditors** — notebooklm_insights_master_notebook_summary_three_brain_routing, notebooklm_insights_ai_agents_database_guide_multi_brain_strategy, project_architecture_ollama_local_llm [INFERRED 0.75]
- **Leadpipe Three-Agent Pipeline (find→prioritize→intelligence)** — sean_lead_finder_agent, sean_lead_prioritizer_agent, sean_website_intelligence_agent [EXTRACTED 1.00]
- **Sean/Matt Safe Collaboration Protocol** — sean_safe_matt_import_protocol, sean_memory_md, sean_agents_md, matt_wip_branch_2026_06_09 [INFERRED 0.85]
- **Deterministic Lead Scoring Flow** — sean_google_places_source, sean_score_from_signals, sean_lead_score [INFERRED 0.85]
- **Token-Economy Stress-Test Three-Brain Flow** — 2026_06_10_token_economy_input, 2026_06_10_token_economy_gemini_review, three_brain_out_log [EXTRACTED 0.85]
- **Leadpipe Three-Stage Lead Lifecycle** — reports_matt_ai_leads, reports_matt_prioritized_leads, reports_matt_website_briefs, past_mistakes_stage_scoped_writes [INFERRED 0.75]
- **Three-Brain Efficiency System Roles** — visualization_ai_build_bible_architect_claude, visualization_ai_build_bible_muscle_deepseek, visualization_ai_build_bible_reviewer_codex [EXTRACTED 1.00]
- **Three-Layer Mental Model Stack** — visualization_ai_build_bible_layer3_model_brain, visualization_ai_build_bible_layer2_agentic_control, visualization_ai_build_bible_layer1_infrastructure_context [EXTRACTED 1.00]
- **Multi-Brain Model Tiers (Cloud / Local / Hybrid)** — visualization_comprehensive_ai_agents_database_cloud_high_reasoning, visualization_comprehensive_ai_agents_database_local_privacy_efficiency, visualization_comprehensive_ai_agents_database_hybrid_orchestrated [EXTRACTED 1.00]
- **Blueprint of AI-Assisted Development components** — visualization_comprehensive_ai_skills_gsd_orchestration, visualization_comprehensive_ai_skills_three_tier_memory, visualization_comprehensive_ai_skills_blast_prompt, visualization_comprehensive_ai_skills_piv_loop [EXTRACTED 1.00]
- **MCP Modular Framework functional layers** — visualization_comprehensive_mcp_database_design_to_code, visualization_comprehensive_mcp_database_repository_management, visualization_comprehensive_mcp_database_agentic_web_research, visualization_comprehensive_mcp_database_backend_management, visualization_comprehensive_mcp_database_testing_multimedia [EXTRACTED 1.00]
- **BLAST Framework phases** — visualization_comprehensive_project_structuring_guide_blueprint_links, visualization_comprehensive_project_structuring_guide_architect_stylize, visualization_comprehensive_project_structuring_guide_trigger [EXTRACTED 1.00]
- **Tiered Inference Routing across local model sizes** — local_ai_agents_for_leadpipe_small_local_model, local_ai_agents_for_leadpipe_mid_tier_local_model, local_ai_agents_for_leadpipe_large_quantized_model [EXTRACTED 1.00]
- **Lead pipeline workflow stages** — visuals_website_builder_pipeline_api_fact_acquisition, visuals_website_builder_pipeline_local_llm_reasoning, visuals_website_builder_pipeline_lead_status_lifecycle [EXTRACTED 1.00]
- **Technical architecture components** — visuals_website_builder_pipeline_local_first_computation, visuals_website_builder_pipeline_file_based_orchestration, visuals_website_builder_pipeline_typer_cli_interface [EXTRACTED 1.00]

## Communities (41 total, 2 thin omitted)

### Community 0 - "Reports & Industry Grouping"
Cohesion: 0.08
Nodes (63): _CategoriesFile, CategoryRule, industry_group(), load_industry_categories(), Broad-category groupings for Lead.industry, used to render collapsible sections, Returns (category rules, other_label). Missing/empty file -> no rules,     every, _active(), _all_leads_row() (+55 more)

### Community 1 - "Governance & Constitution"
Cohesion: 0.06
Nodes (49): Agent run safety (no autonomous scraping, 20-cap, profile isolation), Authority model (single owner per current-truth), Cold-start read-path, AGENTS.md Constitution, Firecrawl MCP + REST fallback, Note frontmatter schema (leadpipe vault validate), Hunt operations rhythm, Karpathy operating principles (+41 more)

### Community 2 - "Session Logs & Sync"
Cohesion: 0.06
Nodes (50): Matt Session Logs Index, matt-wip-2026-06-09 Branch, Matt WIP Push + Context Transfer Session, ELI5 Agent Prompt Guides for Matt, Agent Prompt Guides + Industry Grouping, AGENTS.md (constitution), docs/project/ARCHITECTURE.md, Authority Model (source-of-truth per concern) (+42 more)

### Community 3 - "Obsidian Vault Maintenance"
Cohesion: 0.09
Nodes (42): allowlisted_notes(), check_note(), extract_wikilinks(), _first_heading(), heartbeat(), hot(), _is_date(), is_resolvable() (+34 more)

### Community 4 - "Lead Hunts & Sourcing"
Cohesion: 0.07
Nodes (44): Asset Provenance Model (sister sell repo), asyncio + httpx.AsyncClient Refactor, CA Nursery Leads Hunt, config/ca_small_towns.yaml (reference menu), Firecrawl Credit-Pause Guard, firecrawl_pause_credits_pct (account-wide pause), Efficiency & Market Analysis, Leadpipe as Feeder for Future Sell Repo (+36 more)

### Community 5 - "Typer CLI Commands"
Cohesion: 0.11
Nodes (33): check(), find(), intelligence(), _print_report(), prioritize(), _profile_or_exit(), leadpipe — the Matt-friendly entry point (ARCHITECTURE.md §8).      leadpipe f, Run Lead Finder on prompt only — default cap is 20 candidates per industry. (+25 more)

### Community 6 - "Config & Firecrawl Client"
Cohesion: 0.09
Nodes (34): _env_str(), load_settings(), Single entry point every module/agent uses to read config., Read env vars human-edited in .env, treating blank values as unset., RuntimeError, _client(), FirecrawlError, get_credit_usage() (+26 more)

### Community 7 - "Lead Store (Persistence)"
Cohesion: 0.13
Nodes (24): LeadStore, Lead Finder entry point. Refuses leads that already have a website —         thi, Lead Prioritizer entry point. Judgment only — cannot touch identity,         acq, Website Intelligence entry point. Build/sales judgment only — cannot         tou, Manual lifecycle moves (e.g. marking `contacted` / `sold`). Monotonic —, Write via temp file + atomic rename — no partial-write corruption., Lead, _create() (+16 more)

### Community 8 - "Token Economy & Past Mistakes"
Cohesion: 0.07
Nodes (35): Don't Treat Agents as Rigid Procedural Scripts, Prefer CLI over MCP (~35x efficiency), 120k/12% Context Budget Hard-Cap, Exclusion Guardrails (.gitignore/.geminiignore/.aiexclude), Gemini 2.5 Pro Adversarial Review (token economy), Haiku for Heavy-Read Subagents, Token-Economy Game Plan (stress-test input), Output-Token Economy (patch/diff over full rewrites) (+27 more)

### Community 9 - "Lead Data Model"
Cohesion: 0.14
Nodes (26): Lead, LeadCreate, LeadPrioritization, LeadStatus, LeadWebsiteIntelligence, The Lead record — the single shape every agent reads and writes.  Schema + statu, Apply Prioritizer judgment via an explicit allowlist — never touches facts., Apply Website Intelligence judgment via an explicit allowlist. (+18 more)

### Community 10 - "AI Build Bible (Architecture)"
Cohesion: 0.08
Nodes (28): The Architect — Claude 4.7 (UI/UX, Design, Complex Reasoning), 80% Cost Reduction (vs All-Premium Models), AI Build Bible (Visualization Image), Layer 1: Infrastructure & Context, Layer 2: Agentic Control, Layer 3: The Model Brain, The Muscle — DeepSeek V4 (Background & Data Processing), The Reviewer — Codex (GPT-5.5) (Final Code Review & Error Detection) (+20 more)

### Community 11 - "AI Skills & MCP Blueprint"
Cohesion: 0.08
Nodes (26): BLAST System Prompt, The Blueprint of AI-Assisted Development, GSD Orchestration Framework, Comprehensive AI Skills (Infographic), PIV Execution Loop, Site / Pages Workflow, 3-Tier Memory Architecture, XML Tag Structuring (+18 more)

### Community 12 - "Agent Contract Tests"
Cohesion: 0.10
Nodes (18): _matches_target(), Scope found leads to the requested target. Google Places addresses start     wit, Target, Target, Tests for the agent contract and the deterministic rating function.  The rating, A1 tiering: when the fast model fails (timeout/garbage), the retry must use the, A1 tiering for Agent 3: fast failure escalates to the deep model, which can then, C1: the brief's selling voice must be ROI/leverage-anchored, not generic. (+10 more)

### Community 13 - "Config Loading & Pipeline Runner"
Cohesion: 0.13
Nodes (20): BaseModel, _force_ipv4_dns(), _load_targets(), Loads .env (secrets) and profile-owned hunt lists into one place.  Each collabor, Workaround for a real-world finding: on Sean's network, DNS returns an     IPv6, Raised when config/targets.<profile>.yaml is malformed — message is meant to be, Settings, TargetsConfigError (+12 more)

### Community 14 - "Leadpipe Agent Strategy (Visual)"
Cohesion: 0.11
Nodes (21): Core Implementation Principles, Document-Based Memory, Framework Minimalism, Large Quantized Model, Local Intelligence Tiering (RTX 3090), Mid-Tier Local Model, Build Agents as Pipeline Stages, Separation of Facts and Judgment (+13 more)

### Community 15 - "Lead Prioritizer Agent"
Cohesion: 0.14
Nodes (19): _credit_pause_error(), _estimate_photo_count(), _gather_listing_urls(), _parse_photo_count_response(), rate_from_count(), Lead Prioritizer — rates leads by how much photo material exists online (ARCHITE, Parse the strict two-line LLM output for photo-count estimates., Returns [(source_label, url), ...] to enrich from. Prefers URLs Lead     Finder (+11 more)

### Community 16 - "Agent Base & Lead Finder"
Cohesion: 0.17
Nodes (14): AgentResult, The agent contract every pipeline stage implements (ARCHITECTURE.md §3).  Delibe, _normalize_industry(), Lead Finder — finds local businesses with no website (ARCHITECTURE.md §3).  Divi, LLM reasoning step — degrades to the raw search term on any LLM failure., run(), _listing_urls(), run() (+6 more)

### Community 17 - "AI Build Bible Frameworks"
Cohesion: 0.12
Nodes (18): AI Build Bible (Mind Map), Apple-Style Scroll Animation (Frame Sequence), Clone Site Skill, CODA Framework, The Complete AI Build Bible, DRIP Framework, FLOW Framework, Glassmorphism (+10 more)

### Community 18 - "AI Skills Catalog (Mind Map)"
Cohesion: 0.15
Nodes (16): Comprehensive AI Skills (Mind Map), Master Skills Catalog (Mind Map), GSD (Get Shit Done) Framework, CEO System (Daily Brief), Comprehensive AI Skills & Workflows Database, Graphify (Codebase Knowledge Graph), Plan-Implement-Validate (PIV) Loop, The Ralph Loop (+8 more)

### Community 19 - "NotebookLM Insights Index"
Cohesion: 0.15
Nodes (14): Matt Research (folder note), NotebookLM Insights Index, AI Build Bible Guide, BLAST Framework, Context Rot, AI Skills Guide, Plan-Implement-Validate Loop, Custom SDKs Guide (+6 more)

### Community 20 - "Website Intelligence Agent"
Cohesion: 0.22
Nodes (11): compact_scraped_content(), Helpers for keeping scraped listing content safe for local LLM prompts., Bound scraped content while preserving the top, useful snippets, and tail., _build_prompt(), _fallback_intelligence(), _generate_intelligence(), _parse_response(), Website Intelligence — turns prioritized leads into build/sales briefs.  This is (+3 more)

### Community 21 - "Local AI Agents (Leadpipe)"
Cohesion: 0.21
Nodes (12): Local AI Agents for Leadpipe (Mind Map), Custom Agent Stage Pattern, Local AI Agents for Leadpipe, APIs Acquire Facts, LLMs Reason, Store Enforces Boundary, LangGraph, Lead Enrichment Agent, leadpipe Pipeline, Ollama (local model surface) (+4 more)

### Community 22 - "MCP Server Database"
Cohesion: 0.20
Nodes (11): Comprehensive MCP Database (Mind Map), Screenshot Loop Workflow, Browser-in-the-Loop Testing, Context 7 MCP, Comprehensive MCP Server & Tool Database, Firecrawl MCP, Model Context Protocol (MCP), NotebookLM (knowledge backbone) (+3 more)

### Community 23 - "Project Architecture Overview"
Cohesion: 0.22
Nodes (11): Project Deep Dive Report, website-builder Architecture & Vision, Firecrawl Enrichment, Google Places API, GSD Framework, Lead Finder Agent, Lead Prioritizer Agent, Leadpipe Lead Pipeline (+3 more)

### Community 24 - "Session Protocol Guides"
Cohesion: 0.27
Nodes (10): context-transfer Skill, Agent Prompt Guide (End Session), Wrap Up Session Protocol, Matt Getting Up To Date (Sync), Stale Working-Copy Protocol, Agent Prompt Guide (Start Session), website-builder-brain NotebookLM, Onboarding — Matt (+2 more)

### Community 25 - "Context Rot & Model Routing"
Cohesion: 0.22
Nodes (10): Context Rot, Three Brain System, Lost in the Middle, Reset by Degradation Symptoms (not token cap), Token & Context Economy, Exclusion Guardrails (ignore lists), No-Self-Review Law, Output-Token Economy (patch-edit not rewrite) (+2 more)

### Community 26 - "AI Skills Blueprint"
Cohesion: 0.22
Nodes (9): Anatomy of a 'Skill' (SKILL.md), Context Rot Defense, Design & UI Intelligence, Fundamentals & Architecture, Gen-Media & Fal.ai, Global vs. Local Scopes, Specialized Skill Families, Three Installation Paths (+1 more)

### Community 27 - "Stage Architecture & Data Contracts"
Cohesion: 0.22
Nodes (9): Proposed Targets from Matt Onboarding Branch, Local AI Agents for Leadpipe Guide, Pydantic Data Contracts, Simple Stage-Based Architecture, Apprentice / Manager Model, File-Based Pipeline Orchestration, JSONL Source-of-Truth + Markdown Views, Karpathy Simplicity-First Principles (+1 more)

### Community 28 - "Project Structuring Guide"
Cohesion: 0.25
Nodes (9): Comprehensive Project Structuring Guide (Mind Map), BLAST Framework, CLAUDE.md Project Constitution, Big Three Instruction Files (CLAUDE/GEMINI/MEMORY.md), Comprehensive Guide to Project Structuring & Context Management, Karpathy Method (Vibe Coding), Negative Constraints (NEVER rules), See-Say-Run Loop (+1 more)

### Community 29 - "Multi-Brain Agent Strategy"
Cohesion: 0.22
Nodes (9): AI Agents Database Guide, Antigravity Orchestration Framework, Multi-Brain Model Strategy, IPv6 DNS API Hang Bugfix, Master Notebook Summary, SITE Framework, 16 Texas Cities Hunt (166 leads), Three-Brain 80/20 Model Routing (+1 more)

### Community 30 - "Custom SDKs & Private MCPs"
Cohesion: 0.25
Nodes (8): BIBLE Custom SDKs and Proprietary Logic (Mind Map), ACE Framework, AI-First SDK / Agent-Computer Interface (ACI), Custom SDKs, Private MCPs & Proprietary Tooling, FastMCP, Portable / Private MCP Servers, STAND Framework, Stdio Transport (Zero-Network MCP)

### Community 31 - "AI Agent & Model Database"
Cohesion: 0.33
Nodes (7): Comprehensive AI Agents Database (Mind Map), Google Antigravity IDE, Comprehensive AI Agent & Model Database, Hybrid Multi-Agent Workflow (Planner/Coder/Refiner), Mission Control (Agent Manager), Model Routing Strategy (80/20 Rule), Claude Code Router

### Community 32 - "Agent Protocol Contract"
Cohesion: 0.33
Nodes (5): Agent, Do the agent's job for one target (one area + one industry list),         writin, Protocol, LeadStore, Target

### Community 33 - "Sell Methodology (Nate Herk)"
Cohesion: 0.47
Nodes (6): MONEY Framework (agency sales), Core Value Story (capture existing demand), Nate Herk Frameworks, Sell Methodology, 3 Leverage Tests (lead qualification), Website Intelligence Agent (Agent 3)

### Community 34 - "Obsidian Spine & Targeting"
Cohesion: 0.40
Nodes (5): Obsidian Agent-Brain Spine, Small-Town-First Targeting, Leadpipe Working Context, Cold-Start Read-Path, Obsidian .obsidian Trust Boundary

## Ambiguous Edges - Review These
- `Website Intelligence Agent (Agent 3)` → `Website Intelligence Agent (Agent 3)`  [AMBIGUOUS]
  docs/project/SELL_METHODOLOGY.md · relation: conceptually_related_to

## Knowledge Gaps
- **128 isolated node(s):** `LeadStore`, `Target`, `Path`, `date`, `Pending Approvals queue (Sean-only approval)` (+123 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Website Intelligence Agent (Agent 3)` and `Website Intelligence Agent (Agent 3)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `LeadStore` connect `Lead Store (Persistence)` to `Reports & Industry Grouping`, `Typer CLI Commands`, `Lead Data Model`, `Agent Contract Tests`, `Config Loading & Pipeline Runner`, `Lead Prioritizer Agent`, `Agent Base & Lead Finder`, `Website Intelligence Agent`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Config & Firecrawl Client` to `Typer CLI Commands`, `Agent Contract Tests`, `Config Loading & Pipeline Runner`, `Lead Prioritizer Agent`, `Website Intelligence Agent`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `AgentResult` connect `Agent Base & Lead Finder` to `Agent Protocol Contract`, `Agent Contract Tests`, `Config Loading & Pipeline Runner`, `Lead Prioritizer Agent`, `Website Intelligence Agent`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `LeadStore` (e.g. with `RunReport` and `Lead`) actually correct?**
  _`LeadStore` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Lead` (e.g. with `Lead` and `LeadStatus`) actually correct?**
  _`Lead` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Lead` (e.g. with `LeadStore` and `Lead`) actually correct?**
  _`Lead` has 14 INFERRED edges - model-reasoned connections that need verification._