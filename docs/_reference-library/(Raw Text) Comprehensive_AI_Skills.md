> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — ideas, themes, and tools to draw from when building out
> website-builder's actual scaffolding. Treat it as inspiration/lookup, not as the plan.

---

# Comprehensive AI Skills & Workflows Database

This document compiles a deduplicated, categorized master list of skills, workflows, and techniques for AI-assisted development using Antigravity, Claude, Cursor, and other agentic tools. The data is aggregated from the "Jack Roberts AI Guide", prominent YouTube creators, and general AI web design research.

## 1. Agent Orchestration & Context Management
*Skills useful for managing AI context windows, orchestrating multiple agents, and ensuring deterministic outputs.*

*   **The GSD (Get Sh*t Done) Framework:** An orchestration layer that takes a vague idea, builds a strict Product Requirements Document (PRD), and bypasses "context rot" by deploying brand-new sub-agents with fresh context windows for every atomic task.
*   **The BLAST Framework (For Apps & Software):** A master system prompt to build deterministic apps across five stages: Blueprint, Links (MCP), Architect, Stylize, and Trigger.
*   **The Ralph Loop:** An autonomous bash-loop workflow that reads a PRD and spins up new agent sessions for uncompleted tasks repeatedly until verified.
*   **Context Stacking / Priming (`/prime`):** Initializing projects with a `claude.md`, `gemini.md`, or `brain.md` constitution file to force the AI to read rules and brand guidelines before coding.
*   **Agent Teams (Mission Control):** Managing specialized sub-agents (e.g., UX Researcher, Tech Architect) that report to a central lead and collaborate simultaneously.
*   **Graphify (Codebase Knowledge Graph):** Vectorizing a codebase so agents can "ride the lines" of dependencies without loading the entire project into context.
*   **3-Tier Memory Architecture:** Splitting memory into Core (permanent rules), Conversational Buffer (last 50 messages), and Semantic (Pinecone/NotebookLM vector DB) tiers.
*   **Self-Generating Skills:** An advanced capability where an agent monitors its complex tasks and autonomously authors a reusable `skill.md` file for future instant execution.
*   **Git Work Trees:** Spinning up multiple AI terminals to work on separate git branches simultaneously.

## 2. Web Design, UI/UX & Aesthetics
*Skills useful for front-end development, responsive layouts, and visual prototyping.*

*   **The SITE / PAGES Framework:** A workflow for high-converting pages: Purpose, Interface, Text, Engine (AI enhancements), and Ship.
*   **UI Sniping / HTML Extraction:** Extracting raw HTML/CSS from open-source libraries (like 21st.dev) or competitors to feed into the IDE as a structural baseline.
*   **UI / UX Pro Max Skill:** A 67-point automated auditing skill for accessibility, contrast, consistency, and spacing.
*   **3D Website Builder & Asset Generator:** Utilizing Spline and Nano Banana to generate immersive 3D environments and cinematic visuals directly within the IDE.
*   **Brand Design / Identity Skill:** Strict guidelines (hex codes, typography) that force AI output to align perfectly with a brand's visual identity.
*   **Visual Placeholders & Vanilla CSS Preference:** Prioritizing native CSS and generating stylized shapes/gradients to ensure prototypes feel complete without relying on heavy frameworks like Tailwind unless requested.
*   **"Vibe Coding" with Visuals:** Pasting UI screenshots or designs (from tools like v0) directly into the chat to guide the AI's aesthetic choices.

## 3. Core Development & Coding Prompting
*Skills useful for writing robust, type-safe, and well-architected code.*

*   **XML Tag Structuring (The "Gold Standard"):** Wrapping context, instructions, and examples in tags like `<context>`, `<rules>`, and `<task>` to prevent instruction drift (highly recommended for Claude).
*   **Plan-Implement-Validate (PIV) Loop:** Defining scope (Plan), generating code in chunks (Implement), and immediately writing/running unit tests (Validate).
*   **The "Implementation Plan" Strategy (Cursor):** Asking the AI to write a detailed implementation plan first, reviewing it, and then executing step-by-step.
*   **Role & Spiderweb Prompting:** Establishing a high-level persona (e.g., "Senior Full-Stack Engineer") and breaking massive tasks into a sequence of smaller, linked prompts.
*   **Context Management with `@` Symbols:** Using `@Files`, `@Folders`, and `@Codebase` aggressively in Cursor/Windsurf to reduce hallucinations.
*   **Small Increments & Surgical Updates:** Breaking features into small chunks and using targeted find-and-replace tools to modify code without rewriting entire files.

## 4. Testing, Validation & Debugging
*Skills useful for quality assurance, browser testing, and automated error resolution.*

*   **Browser-in-the-Loop Testing:** Using built-in browsers (in Antigravity) for agents to self-verify UI changes, test responsiveness, and "self-heal" visual bugs.
*   **Troubleshooting / Debugging Skill:** A repository of common errors and best practices to help the AI break out of debugging loops and heal code autonomously.
*   **Review-Driven Development:** Shifting the developer's role to "Manager," focusing on reviewing and approving AI implementation artifacts.

## 5. Business, Agency & Content Workflows
*Skills useful for SEO, marketing, agency operations, and data extraction.*

*   **The MONEY Framework:** A sales sequence: Map (niches), Obtain (leads), Nail (build websites), Execute (give upfront value), and Yield (sell recurring services).
*   **SEO Infrastructure & Optimization Skill:** Injecting dynamic routing, metadata, sitemaps, and robots.txt into codebases for Google ranking.
*   **Remotion Video Editing Skill:** Writing React components for motion graphics and social media ads.
*   **Gamma / Presentation Skill:** Transforming transcripts or research into fully formatted presentations (PPTX, PDF) via the Gamma API.
*   **Content Factory Repurposing Plugin:** Scraping YouTube transcripts to autonomously draft tailored posts for LinkedIn and X.
*   **The CEO System (Daily Brief):** A 24/7 command center scraping industry data to provide a daily executive summary of trends and blockers.
*   **Automated Client Feedback Portal:** Connecting Notion databases to the IDE via MCP, allowing AI to execute client change requests automatically.