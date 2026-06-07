> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — ideas, themes, and tools to draw from when building out
> website-builder's actual scaffolding. Treat it as inspiration/lookup, not as the plan.

---

# Comprehensive AI Agent & Model Database (Local & Cloud)

This document provides a deduplicated, categorized master list of AI models, agents, and strategies for use within the Antigravity IDE and wider agentic development ecosystems. It combines Jack Roberts' "Multi-Brain" strategy with industry recommendations from top creators and the latest technical implementation methods.

## 1. Cloud-Based Models (The "High-Reasoning" Brains)
*Best for complex architecture, deep logic, and high-fidelity UI design.*

*   **Claude 3.5 / 3.7 Sonnet (Anthropic):** The "Gold Standard" for daily coding. Renowned for its "vibe"—writing idiomatic code, following complex instructions, and excelling at React/TypeScript/UI development.
*   **Claude Opus 4.6 (Anthropic):** The "Design King" & Architect. Used for high-level architectural thinking, multi-file refactoring, and extreme creative polish.
*   **OpenAI o1-preview / R1:** Specialized "Reasoning" models. Used for "sledgehammering" (massive folder rewrites) and solving deep algorithmic bugs where standard models fail.
*   **GPT-5.5 / Codex (OpenAI):** The "Code Reviewer." Best for final debugging, security audits, and catching hallucinations from other models.
*   **Gemini 3.1 Pro (Google):** The "Multimodal Expert." Unrivaled for analyzing massive context (videos, audio, 2000+ page PDFs) and designing interactive, data-heavy dashboards.
*   **Gemini 2.0 / 3.5 Flash (Google):** The "Speed King." Ideal for large-scale boilerplate generation, file conversions, and codebase-wide pattern matching due to extreme speed and massive context windows.

## 2. Local Models (The "Privacy & Efficiency" Brains)
*Best for routine tasks, sensitive data, and offline development via Ollama or LM Studio.*

*   **DeepSeek Coder V2 (236B / Lite) & DeepSeek R1:** The top-tier local alternative to Claude. DeepSeek R1 provides cloud-level reasoning on local hardware or via cheap APIs.
*   **Qwen 2.5 Coder (32B / 7B):** The "Sweet Spot." Highly optimized for agentic tool-calling and high-speed autocomplete (Fill-In-the-Middle).
*   **Llama 3.1 / 3.3 (70B & 8B):** The most stable generalist models for local "Chat with Codebase" features, known for reliable function calling.
*   **Gemma 4 (Google):** The "Local Assistant." Designed for 100% offline usage in Antigravity, handling basic HTML, scripting, and file management with zero API cost.

## 3. Antigravity Orchestration & Strategies
*How to effectively use these agents within the Antigravity IDE.*

*   **Model Routing Strategy (The 80/20 Rule):** Use local models (Ollama/Gemma) for 80% of routine, mundane tasks for $0 cost. Reserve premium cloud models (Claude/Gemini Pro) for the 20% of "hard stuff."
*   **Mission Control (Agent Manager):** Spawn up to 16 specialized agents (Frontend, Backend, DevOps, etc.) in parallel. Each agent can be assigned a different "brain" based on its role.
*   **Hybrid Multi-Agent Workflow:**
    1.  **Planner:** Use a high-reasoning model (Claude or DeepSeek R1) to create the implementation plan.
    2.  **Coder:** Use a fast local model (Qwen 2.5) to execute file changes.
    3.  **Refiner:** Use a secondary model to run tests and self-correct.
*   **Routing via `SKILL.md`:** Create custom rules within the project to force agents to use specific models for specific folders (e.g., "Use local Llama for `/src/sensitive/`, use Claude for `/src/ui/`").

## 4. Implementation Methods (Connecting the IDE)
*Technical ways to link Antigravity to local and cloud providers.*

*   **MCP (Model Context Protocol):** The primary bridge. Connect local Ollama instances using `ollama-mcp-server` and cloud providers via OpenRouter MCP proxies.
*   **Open Code Extension:** Enables dynamic, real-time model swapping within the IDE interface via OpenRouter.
*   **Local-First Advantage:** Agents have direct access to your filesystem, terminal, and local compilers, allowing for autonomous "Plan -> Act -> Validate" loops.
*   **Browser-in-the-Loop:** Antigravity agents can launch local browser instances to visually verify UI changes and self-heal CSS bugs.
*   **Artifacts System:** Agents generate verifiable deliverables (plans, diffs) to ensure the human "Reviewer" can maintain control over the autonomous process.
