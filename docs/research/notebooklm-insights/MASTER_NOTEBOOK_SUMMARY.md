Continuing conversation 23f52159...
Answer:
# website-builder-brain: Comprehensive Research & Project State

This document synthesizes the overarching AI strategy, toolsets, 
frameworks, and live project status for the `website-builder` 
pipeline.

---

## 1. Executive Summary & Project Status
The `website-builder` repository represents a local-AI-powered 
lead generation pipeline designed to find businesses without 
websites, rate them based on online photo availability, and 
output clickable lead lists [1]. The actual building and selling 
of websites is handled in a separate, future repository [2].

**Current Status (As of June 7, 2026):**
*   **Scaffold Built & Validated:** The pipeline is fully 
operational. The `leadpipe` CLI (`find`, `check`, `prioritize`) 
runs end-to-end on real data [3].
*   **Real Data Hunt Executed:** A hunt across 16 Texas cities 
successfully generated 166 leads without websites [4]. 
*   **Bug Fixes & Hardening:** A critical infra bug (IPv6 DNS 
causing 85-second API hangs) was patched to force IPv4, reducing 
latency to 0.05s [3, 5]. Foundational issues were preemptively 
fixed following a Three-Brain → Codex adversarial review [6].
*   **Collaborator Alignment:** Sean and Matt's onboarding is 
complete. Sean is using `gemma4-fast` locally on an RTX 3090, 
while Matt is configured to use `qwen2.5:7b` based on his GPU [3,
7]. 
*   **Collaboration Protocol:** The team will use separate 
`leads.jsonl` data stores for Sean and Matt to avoid overlaps, 
merging visibility through shared generated Obsidian reports with
auto-deduplication and soft-deletes [8, 9].

---

## 2. Core Architecture & Philosophy

### The "Apprentice" Model & Karpathy Principles
The overarching philosophy shifts the developer into a "Manager" 
role, directing intent via natural language while the AI acts as 
an apprentice [10]. Operations must follow Andrej Karpathy's 
principles:
*   **Data First:** Define data structures before writing logic 
[11].
*   **Simplicity First:** Minimal logic, avoid speculative 
abstractions [11]. 
*   **Surgical Changes:** Edit only what needs changing [12].
*   **Fact vs. Judgment Boundary (Critical):** APIs (like Google 
Places) are exclusively used to acquire *facts* ("does this 
business have a website?"). Local LLMs are strictly used to 
reason and make *judgments* (e.g., industry classification, photo
rating) [13, 14].

### Codebase Organization
*   **Tech Stack:** Python via the `uv` package manager, a 
file-based Typer CLI, and Pydantic data contracts [15, 16]. 
*   **Storage:** A central `leads.jsonl` file serves as the 
source of truth, keyed by `place_id`, from which clickable 
Markdown reports are generated [16, 17].
*   **Simplicity over Frameworks:** Keep orchestration simple. Do
not introduce heavy agent frameworks like LangGraph or PydanticAI
until the file-based stage pattern proves insufficient [18, 19].

---

## 3. The AI Toolkit & Model Hierarchy

### The "Three-Brain" Model Routing
The project utilizes an "80/20 Routing" strategy to optimize cost
and capability [20, 21]:
1.  **Local Models (The Workhorses):** Used for 80% of routine 
reasoning, classification, and JSON extraction. `gemma4-fast`, 
`qwen2.5:7b`, and `Llama 3.3` provide free, offline compute via 
Ollama [18, 22-24].
2.  **Cloud Models (The Architects):** Claude 4.6/4.7 Sonnet/Opus
for UI design, deep reasoning, and complex refactoring [25]. 
Gemini 3.1 Pro for handling massive contexts [26].
3.  **Review Models (The Auditors):** Codex (GPT-5.5) or OpenAI 
o1-preview used strictly for final code review, security audits, 
and catching hallucinations [27, 28].

### Essential MCPs (Model Context Protocol)
MCP servers give agents direct "universal remote" access to 
specific tools [29].
*   **Firecrawl:** Web scraping to convert sites to clean 
markdown for lead enrichment. (Currently active in `.mcp.json` 
but requires credit top-ups) [30, 31].
*   **Supabase:** Natural language database queries and 
migrations [30].
*   **Context 7:** Fetches live API documentation to prevent AI 
from hallucinating deprecated code [32].
*   **Playwright / Puppeteer:** Enables the "Screenshot Loop" 
where agents visually self-verify UI changes and self-heal bugs 
[33].

---

## 4. Context Management & Workflows

### Combating "Context Rot"
As AI conversations grow, instructions degrade. Professional 
builders mitigate this using:
*   **One Task Per Message:** Never batch massive features into a
single prompt [34].
*   **The 60% Rule:** Run `/compact` when the context window 
reaches 60% full [35].
*   **3-Tier Memory:** Combine Core rules (`AGENTS.md`), 
Conversational buffers, and Semantic memory (NotebookLM/Pinecone)
[36, 37].
*   **Context Transfer:** A mandatory skill run at the end of 
every session to log summaries, timestamp actions, and sync the 
NotebookLM brain [38, 39].

### Master Frameworks
*   **BLAST Framework:** Blueprint, Links, Architect, Stylize, 
Trigger. A deterministic 5-phase process for building software 
[40, 41].
*   **SITE Framework:** Purpose, Interface, Text, Engine, Ship. 
Used for conversion-focused marketing sites [42, 43].
*   **MONEY Framework:** Map niches, Obtain leads, Nail builds, 
Execute value, Yield recurring revenue (the agency sales 
sequence) [44, 45].
*   **AI Website Cloning System:** For the future sister project,
templates are built using a `siteconfig.ts` architecture. Running
the `/clone-site` skill reads the config, autonomously swaps 
logos, copy, and colors, and yields a new premium site in 5 
minutes [46, 47].

---

## 5. Actionable Next Steps

1.  **Top Up Firecrawl Credits:** The `lead_prioritizer` 
gracefully skips photo-rating and logs a warning when credits are
empty. Credits must be added to rate the 166 newly found leads 
[7, 48, 49].
2.  **Establish Budget Guardrails:** Before authorizing 24/7 
autonomous background runs, implement strict credit caps and 
batch limits for the Firecrawl-heavy Lead Prioritizer [8, 9].
3.  **Implement the Sean/Matt Profile Protocol:** Build out the 
data partitioning (`data/sean/leads.jsonl` vs 
`data/matt/leads.jsonl`) and the automated sync logic to produce 
shared reports before parallel use begins [8].
4.  **Develop Agent #3:** Once the budget guardrails and profile 
protocol are in place, build the next agents. Recommendations are
the **Lead Enrichment Agent** (finding contact info/socials via 
Firecrawl) and the **Website Intelligence Agent** (generating 
competitor opportunity reports) [8, 50, 51].

Resumed conversation: 23f52159-33e1-46b6-857e-621c20d53767
