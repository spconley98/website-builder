> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — ideas, themes, and tools to draw from when building out
> website-builder's actual scaffolding. Treat it as inspiration/lookup, not as the plan.

---

# Comprehensive Guide to Project Structuring & Context Management

This document provides a master framework for organizing codebases and managing AI context to ensure high-performance, autonomous development. It synthesizes Jack Roberts' "BLAST" workflow, the "Karpathy Method" (Vibe Coding), and industry best practices for agentic IDEs like Antigravity, Claude Code, and Cursor.

## 1. The Core Philosophy: AI as a "Director of Intent"

*   **The Karpathy Method (Vibe Coding):** Software development is shifting from writing syntax to **directing intent**. English is the "hottest new programming language."
*   **The "See-Say-Run" Loop:** 
    1.  **See:** Observe the current state/error.
    2.  **Say:** Describe the desired change or fix in plain English.
    3.  **Run:** Execute the agent's code.
    4.  **Repeat:** Iterate until the "vibe" (the user experience) is correct.
*   **The Apprentice Model:** Treat the AI as a highly capable but literal apprentice. You provide the high-level architectural "North Star," and the AI handles the implementation and boilerplate.

## 2. Project Structuring: Organizing for AI Readability

An AI-native project structure reduces the "reasoning hops" a model must take to understand your intent.

### Recommended AI-Optimized Directory Structure
```text
project-root/
├── .cursor/rules/          # Cursor-specific .mdc rules (Pattern-based linting)
├── docs/ai/                # "Spoke" guides (Auth, Data Schema, Testing SOPs)
├── CLAUDE.md               # Claude Code onboarding (Build/Test/Lint commands)
├── GEMINI.md               # Main project "Constitution" (Strategy & Non-negotiables)
├── MEMORY.md               # Pinned state (Active tasks & context - NOT committed)
├── README.md               # Human-centric project overview
└── src/                    # Highly modularized, semantically named source code
```

### Jack Roberts' Rules for Organization
*   **One Project, One URL:** Keep workspaces strictly isolated to prevent context contamination.
*   **Modularization:** Use smaller, single-responsibility files. AI agents modify and validate small files much more accurately than massive ones.
*   **The "Skills" Library:** Maintain a global `anti-gravity skills` folder on your machine containing repeatable automation scripts and prompt templates to import into every new project.

## 3. Context Management: Combating "Context Rot"

AI performance degrades as conversation history grows ("Context Rot"). Information in the middle of a massive window gets diluted ("Lost in the Middle").

### The "Big Three" Instruction Files
*   **CLAUDE.md:** Focuses on the "how-to"—commands for building, testing, and linting.
*   **GEMINI.md:** Focuses on the "what/why"—architectural principles, brand guidelines, and high-level strategy.
*   **MEMORY.md / TODO.md:** A "Pinned State" file the agent updates at every turn to keep track of its own progress and "invariants."

### Strategies for "Clean" Reasoning
*   **One Task, One Window:** Open a brand new terminal/chat window for every atomic task to reset the token count and clear irrelevant history.
*   **Context Compaction:** Before closing a long session, ask the AI to summarize the current state and next steps. Feed this "Context Transfer" document into the next fresh agent.
*   **Repo Maps:** Use a "bird's-eye view" of the codebase (signatures and definitions) to give the agent broad awareness without consuming the entire token budget.
*   **Negative Constraints:** Use explicit "NEVER do X" rules. AI follows prohibitions more reliably than general suggestions.

## 4. The Step-by-Step Workflow (The BLAST Framework)

Jack Roberts recommends a deterministic, five-phase process for building projects from scratch:

### Phase 0: Protocol Zero (The Setup)
Enter **Plan Mode** first. Spar with the AI to refine the project requirements. The AI then autonomously creates the task plan, findings log, and `gemini.md` constitution.

### [B] Blueprint (Vision & Logic)
Identify the "North Star" goal and the "Source of Truth" for data. Define the data schemas and delivery payloads.

### [L] Links (Connections)
Establish and test all API/MCP connections (Supabase, Stripe, Notion, etc.). Ensure the "pipes" are connected before writing a single line of application logic.

### [A] Architect (Deterministic Core)
Build the backend using a strict 3-layer hierarchy:
1.  **Architecture:** Technical SOPs in Markdown.
2.  **Navigation:** Decision-making and routing logic.
3.  **Tools:** Atomic, testable scripts.

### [S] Stylize (UI & UX)
Refine the aesthetics once the logic is proven. Use "UI Sniping" (extracting HTML/CSS from component libraries) to instantly inject premium styling.

### [T] Trigger (Deploy)
Deploy the application live (Vercel, Modal, GitHub) so it can run autonomously or serve users.

## 5. Creator Best Practices Summary

*   **Lee Robinson (Cursor):** Emphasizes **Self-Verifying Loops**. Use TypeScript, linters, and TDD to give the AI immediate, automated feedback to fix its own errors.
*   **Theo (t3.gg):** Advocates for **Minimalist Context**. Don't dump the whole repo into the prompt; let the AI use tools (`grep`, `ls`) to "discover" context as needed.
*   **Agent Parallelism:** Use the Antigravity Agent Manager to deploy specialized agents (e.g., a "QA Auditor" and a "Frontend Designer") to work in parallel.
