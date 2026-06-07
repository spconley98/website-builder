> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — ideas, themes, and tools to draw from when building out
> website-builder's actual scaffolding. Treat it as inspiration/lookup, not as the plan.

---

# THE COMPLETE AI BUILD BIBLE
## A Lifetime Reference for Building Websites, Apps & Projects with AI Tools
### Based on Antigravity, Claude Code, Gemini, ChatGPT, Codex, Ollama & More

---

> **How to use this document:** Read it top to bottom once. After that, use it as a reference dictionary. Every section stands alone. Bookmark this file. You will come back to it hundreds of times.

---

## TABLE OF CONTENTS

1. [The Big Picture: How AI Building Works](#1-the-big-picture)
2. [Your Toolkit: Every AI Tool Explained](#2-your-toolkit)
3. [AI Models: Who Does What](#3-ai-models)
4. [IDEs & Development Environments](#4-ides--development-environments)
5. [The Master Frameworks](#5-the-master-frameworks)
6. [Your Project Constitution: CLAUDE.md & GEMINI.md](#6-your-project-constitution)
7. [Context Management: The Most Critical Skill](#7-context-management)
8. [Prompting Strategies That Actually Work](#8-prompting-strategies)
9. [Design: How to Build Premium-Looking Websites](#9-design)
10. [UI Component Libraries & Code Stacks](#10-ui-component-libraries--code-stacks)
11. [3D, Animation & Scroll Effects](#11-3d-animation--scroll-effects)
12. [Backend, Databases & Deployment](#12-backend-databases--deployment)
13. [MCP Servers: Giving AI Superpowers](#13-mcp-servers)
14. [Skills & Super Skills](#14-skills--super-skills)
15. [Memory Systems for AI](#15-memory-systems-for-ai)
16. [Automation & 24/7 Workflows](#16-automation--247-workflows)
17. [Sub-Agents & Agent Teams](#17-sub-agents--agent-teams)
18. [SEO, Performance & Website Visibility](#18-seo-performance--website-visibility)
19. [Business Frameworks for Selling AI Work](#19-business-frameworks)
20. [The Biggest Mistakes Beginners Make](#20-the-biggest-mistakes-beginners-make)
21. [Your First Project: Step-by-Step](#21-your-first-project-step-by-step)
22. [Quick Reference Cheat Sheet](#22-quick-reference-cheat-sheet)

---

## 1. THE BIG PICTURE

### What Is "AI Building"?

AI building means using artificial intelligence tools to do the heavy lifting of writing code, designing interfaces, debugging errors, and deploying applications — work that used to require a team of engineers, designers, and DevOps specialists.

A single person using AI tools correctly can now build in one day what used to take a team one month. This is not an exaggeration.

### The Mental Model You Need

Think of building with AI in three layers:

```
LAYER 1: The Pilot (YOU)
  └─ You set the direction, make decisions, review output, and catch errors.
     You never stop thinking. The AI is your employee, not your boss.

LAYER 2: The Fighter Jet (The IDE / Environment)
  └─ Google Antigravity, Claude Code, Cursor, Windsurf
     These are the environments where AI lives inside your project.

LAYER 3: The Engine (The AI Model)
  └─ Claude, Gemini, ChatGPT, DeepSeek, Ollama (local)
     The actual intelligence generating the code and content.
```

You must understand all three layers. Beginners only think about Layer 3 (which model is best?). Experts obsess over all three.

### The Current Landscape (2026)

The AI build ecosystem has stabilized into clear winners:

| Use Case | Best Tool |
|---|---|
| Full-stack app building | Google Antigravity + Claude Code |
| Fast UI prototyping | Google AI Studio / Lovable / Bolt.new |
| Design system creation | Google Stitch 2.0 / Open Design |
| Backend automation | n8n / Make.com |
| Database | Supabase |
| Hosting/Deployment | Vercel + GitHub |
| 3D Websites | Spline + Three.js |
| Local/Private AI | Ollama (Gemma 4, Llama) |
| Code review | Codex (GPT-5.5) |
| Research | NotebookLM |

---

## 2. YOUR TOOLKIT

Every tool you will ever need, explained plainly.

### CODING ENVIRONMENTS (IDEs)

**Google Antigravity**
Google's "agent-first" IDE. Think of it as Mission Control — you deploy multiple parallel AI agents that research, plan, code, and test simultaneously. It has a built-in browser that lets the AI see your app and fix visual bugs on its own. It generates "Artifacts" (task lists, implementation plans) you review before the AI executes. Natively supports Gemini 3 and Claude. This is the most powerful build environment available in 2026.

**Claude Code**
Anthropic's terminal-based coding assistant. Unlike autocomplete tools, Claude Code lives inside your project folders and acts as a senior software architect. Key features:
- **Plan Mode** (Shift+Tab): Forces the AI to ask questions and plan before coding
- **Remote Control**: Code from your phone while your laptop does the processing
- **Skills system**: Reusable workflows you build once, run forever
- **`/compact`**: Compress context when sessions get long
- **`/clear`**: Wipe context clean before starting a new task
- **`/ultrathink`**: Unlocks 32,000-token extended reasoning budget

**Cursor**
An advanced desktop code editor with AI deeply integrated. Best used alongside Claude Code — Cursor handles file editing and visual diffs while Claude Code handles planning and execution. Cursor works with any model.

**Windsurf**
Similar to Cursor. A solid alternative. Good for developers who prefer a more traditional editor feel with AI assistance.

**Open Code**
An open-source AI coding agent that acts as a universal bridge. You can swap the AI "brain" behind it to use 150+ models via OpenRouter, including free ones. Lets you bypass rate limits when Claude or Gemini throttle you.

**Replit (Agent 3)**
Browser-based. Excellent for backend building and automated self-testing. Lacks advanced multi-agent features but great for quick projects and beginners who don't want to install anything.

**VS Code**
Microsoft's free code editor. Not AI-native but pairs perfectly with Claude Code and GitHub Copilot extensions.

### RAPID PROTOTYPING TOOLS

**Google AI Studio**
Use this to generate beautiful initial website layouts in seconds. Feed it a screenshot of a site you love, or describe what you want. Download the code. Bring it into Antigravity for real engineering. The workflow is: AI Studio → prototype → Antigravity → production.

**Lovable**
Browser-based "vibe coding" platform. Generates complete, interactive web apps from text descriptions. Connects directly to Supabase for backend. Perfect for building MVPs in hours.

**Bolt.new**
Similar to Lovable. Type what you want, get a working app. Strong at full-stack projects with authentication.

**Google Stitch 2.0**
Google's AI design agent — described as a "Figma killer." It generates multi-page design systems, can extract design identity from competitor websites, and exports directly to Antigravity as React components. Use it for the design phase before any serious coding.

**Aura.build**
Instantly clone an outdated client website, rebuild it in a modern Silicon Valley template in under 2 minutes. Ideal for agency work.

**Open Design**
A 100% local (runs on your computer) clone of Claude Design with 71+ built-in brand systems. Uses Apache 2.0 license. No API costs. Great for unlimited design iteration.

**Figma Make**
Generates fully responsive React designs directly from text prompts inside Figma. Turn designs into code automatically.

**Relume**
AI-powered site map and wireframe generator. Feed it a niche/business type and it generates a complete site structure before any design or styling. Always wireframe before designing.

### AUTOMATION PLATFORMS

**n8n**
The gold standard for complex AI workflow automation. Open-source. Self-hostable. Handles non-linear workflows, error recovery, custom Python scripts, webhooks, and multi-trigger systems. Harder to learn than Make.com but far more powerful.

**Make.com**
The beginner-friendly automation builder. Visual, linear drag-and-drop. Build separate "scenarios" that AI agents use as tools. Perfect first automation platform.

**Zapier**
8,000+ app integrations. Use Zapier Central for simple AI agents. Most useful for connecting obscure software that n8n/Make doesn't support yet.

**Relevance AI**
Dedicated platform for building custom AI tool suites and orchestrating multi-agent workforces. More powerful than Make for agent-specific tasks.

**Lindy**
Pre-built AI systems you can launch instantly. Good for email management, scheduling, and CRM automation without building from scratch.

### AI IMAGE & VIDEO GENERATION

**Nano Banana (ImageFX) Pro 2/3**
Google's premium image generator. Creates hyper-realistic product shots, UI mockups, atmospheric hero backgrounds. Access via K.ai API for 50% cost reduction vs. direct.

**Google Flow**
Takes start and end frame images, interpolates cinematic video transitions between them. The "exploding product" and "assembling product" animation effects are built with this.

**Google Whisk**
Generates high-end product shots with precise reference styling. Create identical start and end frames for animation workflows.

**Kling 3.0**
Generates seamless, looping video animations and dynamic backgrounds. Excellent for scroll-stopping video sections.

**Runway / Higgsfield / Pika**
AI video tools for rendering transitions and animations from image inputs.

**Midjourney**
Best for creative illustration, mood boards, and artistic baseline assets.

**Ideogram**
AI image generator with excellent text rendering inside images.

**Weevi.ai**
Mood board tool that blends images and prompts to generate custom UI/UX visual references.

### RESEARCH & KNOWLEDGE TOOLS

**NotebookLM**
Google's AI research platform. Upload up to 50 sources (PDFs, YouTube videos, websites). It generates deep summaries, podcasts, infographics, and research reports. When connected to Antigravity via MCP, your coding agents can use your curated knowledge as a factual baseline — preventing hallucinations.
- CLI: `py -m notebooklm` (the tool used to access it from Claude Code)

**Firecrawl**
AI-powered web scraper. Navigates sub-pages, extracts specific answers, maps site architecture, pulls competitor colors and typography. Returns clean markdown/JSON instead of messy HTML. Use it instead of manual copy-pasting.

**Apify**
Runs actor scripts for massive-scale web scraping. Ideal for lead generation (scraping Google Maps, LinkedIn, etc.).

**Obsidian**
Markdown-based note-taking app. Acts as a "second brain." Connect it to Claude Code to give it persistent memory of your notes and decisions.

**Context 7**
An MCP tool that automatically fetches the latest API documentation from the internet before your AI writes code. Critical — prevents AI from writing code against deprecated APIs.

### COMPONENT & INSPIRATION SOURCES

**21st.dev**
Premium component library for React and Next.js. Browse for high-end animations, interactive elements, and UI patterns. Copy the code directly into your project.

**CodePen**
Community-driven HTML/CSS/JS experiments. Find specific animations, effects, and micro-interactions. Copy and paste directly.

**ShadCN UI**
The most popular open-source component library for React. Beautifully designed, fully accessible, and customizable. Start every React project with ShadCN.

**Magic UI**
Adds shimmer effects, gradient borders, animated backgrounds, and futuristic elements on top of ShadCN.

**Aceternity UI**
Hyper-polished interactive elements: 3D cards, rainbow buttons, glowing borders, floating elements.

**Dribbble / Mobbin / Godly / Designjoy**
Visual design inspiration platforms. Browse before starting any project. Screenshot what you love, feed into AI.

---

## 3. AI MODELS

### The Right Model for the Right Job

The biggest mistake beginners make is using one model for everything. Different models have different strengths. Here is the complete breakdown:

### Claude (Anthropic) — The Design & Reasoning King

**Models:** Claude Opus 4.7, Sonnet 4.6, Haiku 4.5

**Best for:**
- Creative design and UI/UX decisions
- Complex multi-file refactoring
- Long-form writing and copywriting
- Natural language understanding
- Building CLAUDE.md files and project architectures
- Anything requiring aesthetic judgment

**When to avoid:** Heavy numerical computation, simple repetitive tasks (too expensive)

**Cost tier:** Premium (Opus) → Mid (Sonnet) → Cheap (Haiku)

**Claude Code specific commands:**
```
Shift+Tab        → Enter Plan Mode (always start here)
/ultrathink      → Unlock 32k token reasoning budget
/compact         → Compress context when getting long
/clear           → Wipe context, start fresh
/context         → See what is eating your token budget
```

### Gemini (Google) — The Multimodal Powerhouse

**Models:** Gemini 3.0, 3.1 Pro High, 3.1 Flash, Deep Think

**Best for:**
- Analyzing video, audio, PDFs, and images natively
- Massive context windows (1M+ tokens — entire codebases fit)
- Spatial reasoning and map-based logic
- Google ecosystem integration (Docs, Sheets, Drive)
- Long-running research tasks
- Antigravity's primary model

**Flash models:** Faster and cheaper. Use for quick tasks, initial prototyping.
**Pro High / Deep Think:** Use for complex reasoning, architecture decisions.

### ChatGPT / Codex (OpenAI) — The Code Reviewer

**Models:** GPT-4o, GPT-5.2, GPT-5.5 (Codex)

**Best for:**
- Code review and error detection (Codex is the best reviewer)
- Data analysis and structured outputs
- Image generation (DALL-E integration)
- Initial project scaffolding
- Acting as the "second opinion" in a multi-model workflow

**The "Three Brain" System:**
```
Claude   → Builds (creative, design, architecture)
DeepSeek → Scrapes and does heavy lifting (cheap, fast)
Codex    → Reviews everything (catches bugs, spots errors)
```
This system saves 60-80% on token costs while improving reliability.

### DeepSeek (V4, V4 Flash, V3.1) — The Cost-Effective Workhorse

**Best for:**
- Background automation scripts
- Algorithmic problems
- Python scripts
- Web scraping logic
- Any heavy lifting where visual design doesn't matter
- Up to 100x cheaper than Claude Opus

**When to avoid:** Anything requiring aesthetic judgment or complex UI work

### Ollama (Local Models) — 100% Free & Private

**Models available:** Gemma 4 (4B to 26B), Llama 3.3, Mistral, Phi-4, Qwen

**What it is:** A tool that runs AI models completely locally on your computer. No API costs. No internet required. Zero privacy risk.

**Install:** `https://ollama.com` → download → `ollama pull gemma4`

**Best for:**
- Sensitive/private codebases
- Repetitive tasks where you don't want to pay per token
- Offline development
- Learning and experimenting without cost

**Limitation:** Quality below cloud models, but improving rapidly.

### Model Selection Decision Tree

```
Is it a design or UI task?
  YES → Claude Opus/Sonnet

Does it involve video, audio, or huge files?
  YES → Gemini Pro

Is it a repetitive heavy task with no visual component?
  YES → DeepSeek or Ollama

Do I need to review/audit existing code?
  YES → Codex (GPT-5.5)

Is it simple and I want it free?
  YES → Ollama (Gemma 4)

Is it complex reasoning with a large codebase?
  YES → Gemini 3.1 Pro (1M context)
```

---

## 4. IDEs & DEVELOPMENT ENVIRONMENTS

### Which Environment to Use When

| Situation | Best Environment |
|---|---|
| Building a full-stack production app | Google Antigravity |
| Terminal-based power user workflow | Claude Code (CLI) |
| Quick prototype in the browser | Lovable or Bolt.new |
| Editing existing code with visual diffs | Cursor or VS Code |
| Running automation 24/7 on a server | Claude Code on VPS |
| Free, private, offline building | Open Code + Ollama |

### Setting Up Claude Code (Terminal)

```bash
# Install
npm install -g @anthropic-ai/claude-code

# Start in your project folder
cd your-project
claude

# First thing every session: check your setup
gh auth status
py -m notebooklm list
```

### Google Antigravity Key Features

- **Agent Manager:** Spawn multiple parallel sub-agents. One agent researches, one codes, one tests — all simultaneously.
- **Inbox:** Approve or reject agent tasks before they execute. You stay in control.
- **Native localhost testing:** See your app running inside the IDE without switching windows.
- **Artifacts:** Task lists and implementation plans generated before execution — review the plan before approving.
- **Native MCP support:** Connect to Supabase, GitHub, Vercel, n8n directly.

### Running Multiple Claude Code Sessions (Parallel Building)

Use Git Worktrees to run multiple independent Claude sessions building different features simultaneously:

```bash
# Create isolated branch in separate folder
claude-worktree feature-auth
claude-worktree feature-dashboard

# Each folder has its own Claude session
# Features don't overwrite each other
```

---

## 5. THE MASTER FRAMEWORKS

These are the structured systems used by top AI builders. Learn them. Apply them. They are the difference between amateur output and professional output.

### FRAMEWORK 1: BLAST (For Full-Stack Apps)

Use this when building any application with a backend.

```
B - Blueprint
    Define the "North Star" goal. What does this app do?
    What integrations does it need?
    What is the single source of truth for data?

L - Links
    Test and establish every API connection.
    Set up all MCP servers.
    Verify authentication works.
    Do this BEFORE writing any feature code.

A - Architect
    Build the minimal viable product (MVP) first.
    Use 3-layer deterministic architecture:
      Layer 1: Workflows (markdown SOPs / rules)
      Layer 2: Navigation (decision routing logic)
      Layer 3: Tools (testable Python/TS scripts)
    Keep every file under 500 lines.

S - Stylize
    Refine the UI/UX.
    Apply design system, colors, typography.
    Run the UI Sniping workflow (see Design section).

T - Trigger
    Decide how the app deploys and runs.
    Static site? → Vercel
    Cron jobs? → Modal
    Long-running agents? → Trigger.dev
    24/7 background? → Railway or VPS
```

### FRAMEWORK 2: SITE / PAGES (For Conversion Websites)

Use this when building a marketing or business website.

```
S - Strategy
    Who is the target audience?
    How warm is the traffic? (Cold = paid ads, Warm = SEO, Hot = referral)
    What are their top 3 objections?
    What is the single action you want them to take?

I - Interface
    Build a mood board (Dribbble, Mobbin, Godly).
    Find a competitor website with a layout you love.
    Extract the HTML/CSS (viewpagesource.com or browser inspect).
    Use this as your structural skeleton in AI Studio or Stitch.

T - Text
    Write ALL copy before touching design.
    Every section needs: Hook → Value Prop → Proof → CTA
    Hardcode CTAs. Never let AI guess the copy.

E - Engine
    Add AI-powered features:
      - 11Labs voice chatbot for lead capture
      - Custom pricing calculator
      - AI recommendation tool
    These are the "unfair advantages" that cheap competitors can't copy.

(Ship)
    Deploy via Vercel. Connect to GitHub for auto-deploys.
    Run SEO audit. Submit to Google Search Console.
```

### FRAMEWORK 3: CODA (For Claude Code Projects)

Use this as your session structure every time you open Claude Code.

```
C - Configure
    Build and update your CLAUDE.md file.
    Set the brand guidelines, tech stack, API keys location.
    Read the existing CLAUDE.md if one exists.

O - Outline
    ALWAYS start in Plan Mode (Shift+Tab).
    Spar with the AI. Ask it to question your requirements.
    Get a formal Product Requirements Document (PRD) before any code.

D - Deploy
    Run multiple agents in parallel across different terminal tabs.
    Each agent gets ONE task. Never combine tasks.

A - Automate
    Turn every repeatable workflow into a permanent Skill (markdown file).
    Skills mean you never re-explain the same process twice.

(Review)
    Set pass/fail checklists for the AI.
    Use /ultrareview to spawn QA agents in a cloud sandbox.
    Verify before shipping. Always.
```

### FRAMEWORK 4: WAT (For Agentic Workflows)

Use this to organize any project that involves AI automation.

```
W - Workflows
    Markdown files that act as SOPs (Standard Operating Procedures).
    Written in plain English. Tell the agent what to do step-by-step.
    Stored in: /workflows/

A - Agent
    The AI (Claude Code, Antigravity) reads the workflow.
    It acts as project manager: delegates to tools, handles errors.
    One agent per workflow.

T - Tools
    Python or TypeScript scripts that do specific deterministic actions.
    Examples: scrape_google_maps.py, generate_pdf.py, send_email.py
    Stored in: /tools/
    Rule: Tools should be atomic. One tool = one action.
```

### FRAMEWORK 5: FLOW (For Software Architecture)

```
F - Frame
    Define the problem in one sentence.
    Write an SOP before any code.

L - Layout
    Set up brand guidelines (colors, fonts, spacing).
    Define file structure.
    Establish the visual "vibe" reference.

O - Orchestration
    Use parallel agents to build components simultaneously.
    Front-end agent + Back-end agent + QA agent = faster builds.

W - World
    Publish and host.
    Connect analytics.
    Monitor and iterate.
```

### FRAMEWORK 6: DRIP (For Stitch/Design Projects)

```
D - Design
    Vibe design using Stitch or AI Studio.
    Extract brand identity from competitor sites.
    Generate 3 variants simultaneously (3x Mode in Stitch).

R - Refine
    Edit page by page, element by element.
    Use "Stitch Loop" skill for autonomous multi-page generation.

I - Integrate
    Export to Antigravity or Claude Code.
    Convert design to React/Next.js components.
    Connect to backend logic.

P - Publish
    Final QA pass.
    Deploy to Vercel.
    Connect domain.
```

### FRAMEWORK 7: GSD — Get Shit Done (For Long Projects)

The GSD framework solves the #1 problem with AI coding: context rot and hallucination over long sessions.

```
How it works:
1. Feed GSD your project idea.
2. GSD generates a strict PRD (Product Requirements Document).
3. PRD is broken into atomic micro-tasks.
4. FOR EVERY SINGLE MICRO-TASK:
   → A fresh sub-agent is spawned.
   → The sub-agent has a brand new context window.
   → It completes exactly one task.
   → It reports back.
5. No task spans multiple context windows.
6. No hallucination accumulation.

Result: The AI maintains perfect performance from task 1 to task 100.
```

---

## 6. YOUR PROJECT CONSTITUTION

### The CLAUDE.md File

Every project must have a `CLAUDE.md` file at the project root. This is Claude's system prompt. It is read before every single message. It tells Claude who it is, what the project is, and what the rules are.

**What to put in it:**

```markdown
# Project Name

## What This Is
[One paragraph describing the project purpose]

## Tech Stack
- Frontend: Next.js 15, React 19, Tailwind CSS 4
- Backend: Supabase (PostgreSQL)
- Deployment: Vercel
- State: Zustand
- Auth: Supabase Auth

## Brand Guidelines
- Primary color: #ffb786
- Secondary color: #83cfff  
- Background: #0C0E10
- Font: Inter (headings), System UI (body)
- Aesthetic: Precision ag glassmorphism

## File Structure Rules
- Components: /components/
- Pages: /app/
- Workflows: /workflows/
- Tools: /tools/
- Keep all files under 500 lines
- No monolithic files

## Development Rules
- Always use semantic HTML5 elements
- 8px grid system for all spacing
- CSS variables for all colors and spacing
- Reduced-motion fallbacks for all animations
- Never put API keys in code — use .env

## API Keys Location
All secrets are in .env file. Never hardcode.

## Current Active Work
→ See /workflows/current-sprint.md

## For Communication Styles
→ Read /rules/communication.md
```

**Critical rules for CLAUDE.md:**
- Keep it under 150-200 lines total
- Use "routing" — point Claude to external reference files rather than cramming everything in one file
- Update it whenever your stack or rules change
- Never put actual API keys in this file

### The .claude/ Folder Structure

```
.claude/
  settings.json          → Team-wide standards (commit this to git)
  settings.local.json    → Your personal overrides (DO NOT commit)
  skills/                → Your custom skill markdown files
  agents/                → Multi-agent team configurations
  commands/              → Custom slash commands (wrapup.md, etc.)
```

### The .env File

```bash
# Always use .env for secrets
SUPABASE_URL=your_url
SUPABASE_ANON_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

Add `.env` to your `.gitignore` immediately. Never commit it.

---

## 7. CONTEXT MANAGEMENT

### Why This Is The Most Critical Skill

AI models have a limited "working memory" called a context window. As your conversation gets longer, the AI has to "remember" more. Eventually it starts forgetting earlier instructions. It writes inconsistent code. It contradicts itself. It hallucinates. This is called **context rot**.

Every professional AI builder obsesses over context management. Beginners ignore it and wonder why their AI starts breaking things halfway through a project.

### The Rules

**Rule 1: One task per message**
Never ask the AI to "build the entire authentication system AND the dashboard AND the settings page." One message = one task. Always.

**Rule 2: Monitor your context**
Run `/context` in Claude Code to see a percentage breakdown of what is consuming your tokens. Common culprits:
- MCP servers you forgot to disable
- Large files Claude read earlier
- Long conversation history

**Rule 3: The 60% Rule**
When context hits 60% full, run `/compact`. Claude will compress the conversation while preserving key architectural decisions. You can tell it what to keep:
```
/compact Keep the database schema decisions and the auth architecture. Compress everything else.
```

**Rule 4: The Fresh Start**
When switching to a completely different task, always run `/clear` first. This wipes the context entirely. Think of it like opening a new tab in your browser.

**Rule 5: GSD for long projects**
For anything with more than 10 tasks, use the GSD framework to ensure each task gets a fresh context window. Never try to build an entire app in one session.

### The Context Window Reference

| Model | Context Window |
|---|---|
| Claude Sonnet 4.6 | 200,000 tokens |
| Claude Opus 4.7 | 200,000 tokens |
| Gemini 3.1 Pro | 1,000,000 tokens |
| GPT-4o | 128,000 tokens |
| Gemma 4 (local) | 128,000 tokens |

Gemini's 1M context window is a genuine advantage for large codebases. If you have a massive project, Gemini via Antigravity handles it better.

### The Context Mode Plugin

Playwright and browser automation tools often dump massive 50kb snapshots into context. The Context Mode Plugin intercepts these raw dumps, routes them through a sandbox, and returns only the essential bytes. Enables hours-long sessions without degradation.

---

## 8. PROMPTING STRATEGIES

### The Golden Rule

**Spend 95% of your time defining the problem. Spend 5% executing.**

Amateurs dive straight into "build me X." Professionals spend most of their time in Plan Mode, asking the AI clarifying questions, surfacing edge cases, and producing a proper spec before a single line of code is written.

### Plan Mode: Always Start Here

In Claude Code, press Shift+Tab before every significant task. Plan Mode forces the AI to:
1. Ask you clarifying questions
2. Identify potential problems
3. Explore edge cases
4. Draft an implementation plan
5. Wait for your approval before coding

In Antigravity, the Artifacts system does the same thing. Review the artifact (task list and plan) before clicking "Execute."

### The One-Task-Per-Prompt Rule

```
WRONG: "Build me user authentication with email and Google OAuth, a user profile page, settings, and a dashboard with charts."

RIGHT (4 separate messages):
  Message 1: "Plan the authentication system. Use Supabase Auth. Support email and Google OAuth only. Show me the plan before writing any code."
  Message 2 (after approval): "Implement the email auth flow based on the plan."
  Message 3: "Implement the Google OAuth flow."
  Message 4: "Build the user profile page. Auth is already done."
```

### Breaking Hallucination Loops

When the AI is stuck, producing the same broken output repeatedly, use this exact prompt:

> "Stop. Do not write any code. Explain to me, succinctly but in detail, exactly how you are going to solve this problem, and specifically what will be different this time compared to your previous attempts."

Force it to think before acting. 90% of the time this breaks the loop.

### The Principle of Least Access

When giving AI access to your accounts via MCP, **never give write/delete/send permissions unless absolutely necessary.** Only grant read and draft permissions.

```
BAD:  AI has permission to send emails, delete files, push to main branch.
GOOD: AI can read emails and draft replies. Humans send. AI suggests git commits. Humans push.
```

One mistake with write access can send hundreds of emails to clients, delete production data, or push broken code live. This has happened. Don't let it happen to you.

### Prompt Enhancement with Glido

Use Glido (Agentic Mode) to improve your own prompts before sending them. Highlight your rough prompt text, press the shortcut, and Glido rewrites it into a precise, effective prompt. You send the enhanced version.

### UltraThink for Complex Problems

When facing a genuinely hard architectural problem, invoke `ultrathink` in Claude Code:

```
ultrathink about the best way to architect a real-time geofencing system that handles 10,000 concurrent users, uses Supabase for data storage, and needs to work on both iOS and web.
```

This unlocks a 32,000-token reasoning chain where Claude reasons extensively before answering. Use it sparingly — it consumes tokens fast.

### The "Visual Logic" Fix

For complex decision-making flows (like AI routing logic or business rules), build the logic as a visual tree before giving it to AI. Use Whimsical, Miro, or even a simple drawing to externalize the logic. Then photograph/screenshot the tree and feed it to the AI. This eliminates miscommunication about branching logic.

### HTML Extraction / UI Sniping

AI models are bad at guessing what looks premium. Don't ask them to invent design from scratch.

**The workflow:**
1. Find a competitor website or template you love
2. Right-click → "View Page Source" in your browser (or use viewpagesource.com)
3. Copy the raw HTML/CSS
4. Paste into AI Studio, Stitch, or Claude Code
5. Tell the AI: "Use this as the structural and visual skeleton. Replace the content with our brand."

This technique alone produces dramatically better results than prompting from scratch.

---

## 9. DESIGN

### The Foundational Design Rules

**Rule 1: The 60-30-10 Color Rule**
- 60% of your design = Primary color (usually background)
- 30% = Secondary color (sections, cards)
- 10% = Accent color (buttons, highlights, CTAs)

Example from a real project:
```
Background (60%): #0C0E10 (near-black)
Cards/Sections (30%): #1a1d21 (dark glass panels)
Accent/CTA (10%): #ffb786 (warm orange)
```

**Rule 2: One Fold, One Message**
The part of the page visible without scrolling (the "fold") must communicate ONE thing clearly. Not three things. Not a nav with 8 items. One message, one action.

**Rule 3: Avoid AI Slop**
AI-generated designs default to these overused patterns. Avoid them:
- Purple/blue linear gradients
- Inter font everywhere
- Three rounded boxes side by side
- Generic stock-photo hero images
- Centered everything with no visual tension

**What to use instead:**
- Glassmorphism (frosted glass panels)
- Aurora UI (soft glowing backgrounds)
- Linear/Vercel aesthetic (dark, precise, technical)
- Bento grid layouts (asymmetric card grids)
- Brutalist elements (high contrast, visible borders)

### Design Aesthetics Reference

**Glassmorphism**
```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}
```

**Aurora UI (animated glowing background)**
```css
.aurora-bg {
  background: radial-gradient(ellipse at top, #1a1a2e 0%, #0C0E10 100%);
  position: relative;
}
.aurora-bg::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(131, 207, 255, 0.15), transparent 70%);
  animation: aurora 8s ease infinite;
}
```

**Gradient text**
```css
.text-gradient {
  background: linear-gradient(135deg, #ffb786, #83cfff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Typography Rules

- **Never use more than 2 font families in one project**
- Headings: Display or sans-serif (Inter, Geist, Sora, Space Grotesk)
- Body: Highly readable (Inter, System UI, -apple-system)
- Monospace (for code/technical): JetBrains Mono, Fira Code
- Font sizes should follow a modular scale: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px
- Line height: 1.5 for body, 1.2 for headings
- Never use font-weight below 400 for body text (unreadable on screens)

### Spacing System: The 8px Grid

Everything in your layout should be a multiple of 8px:
- Spacing: 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px
- Apply this to: padding, margins, gaps, border-radius

In Tailwind CSS, this maps to: p-2, p-4, p-6, p-8, p-12, p-16, p-24, p-32

**Why:** The 8px grid creates visual rhythm and makes your layout feel structured even when the user can't identify why.

### Design System Setup

Before writing a single component, define your design tokens in a central file:

```css
/* design-tokens.css */
:root {
  /* Colors */
  --color-primary: #ffb786;
  --color-secondary: #83cfff;
  --color-bg: #0C0E10;
  --color-bg-card: rgba(255, 255, 255, 0.05);
  --color-text: #e5e7eb;
  --color-text-muted: #6b7280;
  --color-error: #ef4444;
  --color-success: #22c55e;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
  --shadow-glow: 0 0 32px rgba(255, 183, 134, 0.2);
}
```

Store this system in `web/DESIGN.md` for AI reference.

### The UI Sniping Workflow (Step by Step)

1. Open a website you want to emulate (competitor, inspiration, premium brand)
2. Right-click → View Page Source
3. Copy the HTML structure (focus on the section you want to replicate)
4. Open your AI tool
5. Paste the HTML and say: "Analyze the layout structure and visual hierarchy of this HTML. Now build a similar section for [my business] using my design tokens. Use [my stack: Next.js/Tailwind]."
6. Iterate with: "Make the cards more glassy" / "Increase the contrast" / "Add hover animations"

The "Awesome Design" GitHub repo (46k+ stars) is a plaintext design system library. Add it to your project and instruct Claude: "Design this component following the Stripe aesthetic from the Awesome Design library." This forces Claude to produce premium-tier outputs.

---

## 10. UI COMPONENT LIBRARIES & CODE STACKS

### The Recommended Tech Stack (2026)

For any production web project, use this stack. It is the most supported, best-documented, and most AI-friendly stack available.

```
Frontend Framework:  Next.js 15 (App Router)
UI Library:          React 19
Styling:             Tailwind CSS v4
Component Library:   ShadCN UI
Animations:          Framer Motion
Icons:               Lucide React
State Management:    Zustand
Forms:               React Hook Form + Zod validation
Database:            Supabase (PostgreSQL)
Auth:                Supabase Auth
File Storage:        Supabase Storage
Deployment:          Vercel
Version Control:     GitHub
```

### Why This Stack

- **Next.js:** Server-side rendering, file-based routing, API routes all in one. Vercel (Next.js creators) makes deployment one-click.
- **Tailwind CSS:** AI models write Tailwind better than custom CSS because it's been trained on more of it. Faster iteration.
- **ShadCN UI:** Not a package you install — you copy the components directly into your project and own them. Fully customizable.
- **Supabase:** Replaces Firebase with PostgreSQL power. Row-level security, realtime subscriptions, authentication, storage — all in one.
- **Vercel:** Auto-deploys from GitHub. Free tier is generous. The fastest path from code to live URL.

### Component Priority Order

When building any UI feature, check these sources in order:

1. **ShadCN UI** — Does a component already exist? Use it.
2. **Magic UI / Aceternity UI** — Need something more animated or visual?
3. **21st.dev** — Need a specific micro-interaction or effect?
4. **CodePen** — Need a very specific CSS effect?
5. **Build custom** — Only as a last resort

### Tailwind CSS Essential Patterns

```jsx
// Glass card
<div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6">

// Gradient text
<h1 className="bg-gradient-to-r from-orange-300 to-sky-300 bg-clip-text text-transparent">

// Glow effect
<button className="shadow-[0_0_32px_rgba(255,183,134,0.4)] hover:shadow-[0_0_48px_rgba(255,183,134,0.6)] transition-shadow">

// Animated gradient background
<div className="animate-gradient bg-gradient-to-r from-purple-500 via-blue-500 to-cyan-500 bg-[length:200%_200%]">
```

---

## 11. 3D, ANIMATION & SCROLL EFFECTS

### Why This Matters

Animation and 3D are the #1 visual differentiator between a "$500 website" and a "$10,000 website." The gap between average and premium is almost entirely in motion design, not static layout.

### Tool 1: Spline (Interactive 3D)

Spline is the easiest way to add interactive 3D elements to any website.

**Workflow:**
1. Go to spline.design — build or download a 3D model
2. Publish → Get the public URL or download the JS
3. Embed in your website:

```html
<!-- Vanilla JS -->
<script type="module" src="https://unpkg.com/@splinetool/viewer@1.0.0/build/spline-viewer.js"></script>
<spline-viewer url="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"></spline-viewer>
```

```jsx
// React
import Spline from '@splinetool/react-spline';
<Spline scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode" />
```

**Best practices for Spline:**
- Keep asset size under 3MB for acceptable load time
- Disable "Page Scroll" in Spline to prevent it from hijacking your site's scroll
- Render on a vanilla.js web component behind your main UI layer
- Always set a static fallback image for users on slow connections

### Tool 2: Three.js (Advanced 3D)

Three.js gives you full control over 3D rendering in the browser. Steeper learning curve, but unlimited capability.

**Use cases:**
- Custom 3D character animations
- Particle systems and simulations
- Interactive data visualizations
- Gesture-controlled experiences
- Loading 3D models from Sketchfab (glTF format)

**Quick setup:**
```bash
npm install three @types/three
```

```jsx
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// Load a .glb model from Sketchfab
const loader = new GLTFLoader();
loader.load('/models/robot.glb', (gltf) => {
  scene.add(gltf.scene);
});
```

### Tool 3: The Apple-Style Scroll Animation (Frame Sequence)

This is the technique Apple uses on product pages — the product "animates" as you scroll. Video scrubbing tied to scroll position.

**Full workflow:**

**Step 1: Generate the video**
- Use Google Whisk to generate start frame (product assembled, white background)
- Use Google Whisk to generate end frame (product exploded/deconstructed)
- Use Google Flow to interpolate a cinematic 3D transition video between them
- Export as MP4

**Step 2: Extract frames**
- Go to ezgif.com → Video to GIF → Extract frames
- Settings: 15-30 FPS → yields 80-240 images
- Download as a ZIP of JPEGs/PNGs

**Step 3: Implement canvas scroll scrubbing**

```javascript
// Core scroll scrubbing implementation
const canvas = document.getElementById('hero-canvas');
const ctx = canvas.getContext('2d');
const frameCount = 147; // total frames
const images = [];

// Preload all frames
for (let i = 0; i < frameCount; i++) {
  const img = new Image();
  img.src = `/frames/frame_${String(i).padStart(4, '0')}.jpg`;
  images.push(img);
}

// Draw frame based on scroll position
function updateFrame() {
  const scrollTop = window.scrollY;
  const maxScrollTop = document.body.scrollHeight - window.innerHeight;
  const scrollFraction = scrollTop / maxScrollTop;
  const frameIndex = Math.min(
    frameCount - 1,
    Math.ceil(scrollFraction * frameCount)
  );
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(images[frameIndex], 0, 0, canvas.width, canvas.height);
}

window.addEventListener('scroll', updateFrame);
```

**Performance optimizations:**
- Preload frames in chunks of 20-30 rather than all at once
- Convert to WebP format (60% smaller than JPEG at same quality)
- Cap canvas resolution on mobile (max 1x device pixel ratio)
- Use `requestAnimationFrame` instead of direct scroll events

### Tool 4: GSAP ScrollTrigger

For scroll-driven animations without frame extraction:

```bash
npm install gsap
```

```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

// Animate element into view on scroll
gsap.from('.hero-title', {
  scrollTrigger: {
    trigger: '.hero-title',
    start: 'top 80%',
    end: 'top 20%',
    scrub: 1, // ties animation to scroll position
  },
  opacity: 0,
  y: 60,
  duration: 1,
});

// Pin a section while scrolling through it
ScrollTrigger.create({
  trigger: '.product-section',
  start: 'top top',
  end: '+=500',
  pin: true,
});
```

### Tool 5: Framer Motion

For React-native animations:

```bash
npm install framer-motion
```

```jsx
import { motion } from 'framer-motion';

// Fade in on mount
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: 'easeOut' }}
>
  Content
</motion.div>

// Stagger children animations
<motion.div
  variants={{ show: { transition: { staggerChildren: 0.1 } } }}
  initial="hidden"
  animate="show"
>
  {items.map(item => (
    <motion.div
      variants={{ hidden: { opacity: 0 }, show: { opacity: 1 } }}
    >
      {item}
    </motion.div>
  ))}
</motion.div>
```

**Always add reduced-motion fallbacks:**
```jsx
import { useReducedMotion } from 'framer-motion';

function AnimatedCard() {
  const shouldReduceMotion = useReducedMotion();
  return (
    <motion.div
      animate={{ y: shouldReduceMotion ? 0 : -10 }}
      transition={{ repeat: Infinity, repeatType: 'reverse', duration: 2 }}
    />
  );
}
```

### Where to Source 3D Models

**Sketchfab** — The largest library of free and premium 3D models. Download in `.glb` (glTF binary) format. Drop directly into your project folder. Use with Three.js.

**Search terms that work well:** "product 3D model free glTF", "abstract shape Sketchfab CC0", "low poly character glb"

---

## 12. BACKEND, DATABASES & DEPLOYMENT

### Supabase: Your Backend-in-a-Box

Supabase is a hosted PostgreSQL database with auth, storage, and real-time subscriptions built in. It replaces Firebase but uses SQL instead of NoSQL.

**Setup:**
```bash
npm install @supabase/supabase-js
```

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

// Fetch data
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('active', true);

// Insert data
const { error } = await supabase
  .from('tasks')
  .insert({ title: 'New task', user_id: userId });

// Real-time subscription
supabase
  .channel('tasks')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'tasks' }, 
    (payload) => console.log('Change:', payload))
  .subscribe();
```

**Row Level Security (RLS):** Always enable RLS on every table. This ensures users can only see their own data.

```sql
-- Enable RLS
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Policy: users can only see their own tasks
CREATE POLICY "Users see own tasks" ON tasks
  FOR SELECT USING (auth.uid() = user_id);
```

### Pinecone: Long-Term AI Memory

Supabase stores structured data. Pinecone stores embeddings — meaning your AI can semantically search through past conversations, documents, and knowledge.

**Use case:** "What did Spencer tell me about his preference for button styles 3 sessions ago?" → Pinecone retrieves it.

```python
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key="your-key")
index = pc.Index("your-index")

# Store a memory
client = OpenAI()
embedding = client.embeddings.create(
    input="User prefers rounded buttons with warm orange color",
    model="text-embedding-3-small"
).data[0].embedding

index.upsert(vectors=[{
    "id": "memory-001",
    "values": embedding,
    "metadata": {"content": "User prefers rounded buttons with warm orange color", "date": "2026-05-16"}
}])

# Retrieve relevant memories
results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
```

### GitHub: Your Safety Net

Connect your project to GitHub immediately. Every time the AI makes significant progress, commit it:

```bash
git add -A
git commit -m "feat: add user authentication flow"
git push
```

If the AI breaks something catastrophic, you can always:
```bash
git log --oneline          # Find the last good commit
git checkout abc1234       # Go back to it
```

**Never work without Git. It is your undo button for the AI.**

### Vercel: Zero-Configuration Deployment

1. Push code to GitHub
2. Go to vercel.com → New Project → Import from GitHub
3. Select your repo → Deploy
4. Every future `git push` auto-deploys

**Environment variables in Vercel:** Settings → Environment Variables. Add all your `.env` variables here for production.

### Modal: Serverless Background Tasks

For Python scripts that need to run 24/7 (scrapers, cron jobs, AI pipelines):

```python
import modal

app = modal.App("daily-scraper")

@app.function(schedule=modal.Cron("0 6 * * *"))  # Run at 6am daily
def scrape_leads():
    # Your scraping logic here
    pass
```

Deploy with: `modal deploy scraper.py`
You pay only for actual execution time (seconds).

### Railway: Full App Hosting

For apps that need a persistent server (not serverless):
- Connects to GitHub
- Auto-deploys on push
- Supports Node.js, Python, PostgreSQL, Redis
- Better than Modal when you need a constantly-running process

### Trigger.dev: Long-Running AI Tasks

For AI agents that might run for 10-30 minutes (researcher, report generator):

```typescript
import { task, schedules } from "@trigger.dev/sdk/v3";

export const researchTask = task({
  id: "deep-research",
  maxDuration: 1800, // 30 minutes max
  run: async (payload: { topic: string }) => {
    // Long-running research logic
    // Automatic retries on failure
    // Full logging
  },
});
```

Deploy via `trigger.dev` and it handles all the infrastructure.

---

## 13. MCP SERVERS

### What MCP Is

Model Context Protocol (MCP) is a standard that lets AI IDEs (Claude Code, Antigravity, Cursor) connect to external tools and services. Think of it as a "universal remote control" — your AI can now directly manipulate Supabase databases, read Gmail, push to GitHub, trigger n8n workflows, etc.

Without MCP: You copy-paste outputs between tools manually.
With MCP: The AI does everything autonomously in one session.

### Installing MCP Servers in Claude Code

```bash
# Add an MCP server to your project
claude mcp add firecrawl

# Or add to global settings (available in all projects)
claude mcp add --scope global supabase
```

### Essential MCP Servers

**Firecrawl** (Web Scraping)
```bash
claude mcp add firecrawl
```
- Scrape any website into clean markdown
- Map an entire site's architecture
- Extract competitor design tokens and typography
- Deep-scrape niche data for research

**Supabase** (Database)
```bash
claude mcp add supabase
```
- Query your database in natural language
- Run migrations
- Debug data issues
- Generate TypeScript types from your schema

**GitHub** (Version Control)
```bash
claude mcp add github
```
- Create branches
- Open pull requests
- Read/write files
- Search code across repos

**Vercel** (Deployment)
```bash
claude mcp add vercel
```
- Deploy from within Claude
- Check build logs
- Manage environment variables
- Monitor performance

**n8n** (Workflow Automation)
```bash
claude mcp add n8n
```
- Trigger workflows
- Read workflow status
- Build and deploy automations

**Google Workspace** (GWS)
- Read and search Gmail
- Read Google Sheets (for data input)
- Write to Google Docs
- Search Google Drive
- Generate Google Slides

**Zapier**
```bash
claude mcp add zapier
```
- Connect to 8,000+ apps
- Trigger Zaps from within Claude
- **IMPORTANT:** Only grant READ and DRAFT access. Never grant send/delete.

**NotebookLM**
- Read your research notebooks
- Push new content to notebooks
- Use as factual baseline for coding (zero hallucinations)

**Context 7** (Live API Docs)
- Fetches latest documentation before AI writes any code
- Prevents using deprecated APIs
- Critical for any project using third-party APIs

**Apify** (Mass Scraping)
- Run actor scripts for large-scale data extraction
- Google Maps lead scraping
- LinkedIn profile scraping
- E-commerce price monitoring

**TestSprite** (Autonomous QA)
- Runs frontend tests automatically
- Checks animations and interactions
- Catches memory leaks
- Verifies responsive design before deployment

**Playwright / Puppeteer** (Browser Automation)
- Take screenshots of your running app
- Visual regression testing
- Automate browser interactions for QA
- Used in the "Screenshot Loop" workflow

### The Screenshot Loop Workflow

Tell Claude Code: "Spin up the local dev server, take a screenshot using Playwright, compare it to the design reference image, list all visual discrepancies, then fix them one by one."

This creates an autonomous visual QA loop where the AI fixes UI bugs without you manually reviewing every change.

---

## 14. SKILLS & SUPER SKILLS

### What Is a Skill?

A skill is a reusable markdown file that teaches Claude Code how to execute a specific process perfectly, every single time, without you re-explaining it.

Example: Instead of explaining "how to do a UI redesign" every session, you write a "ui-redesign.md" skill once. From then on, you just type `/ui-redesign` and Claude executes the entire process perfectly.

**Skills = Your intellectual property. Build them aggressively.**

### Skill File Structure

```markdown
---
name: ui-redesign
description: Redesigns a UI module to match the V2 design system with glassmorphism, gradient text, and Framer Motion animations.
tools: [read, edit, bash, browser]
---

# UI Redesign Skill

## Step 1: Read the design tokens
Read `/web/DESIGN.md` for all color, typography, and spacing tokens.

## Step 2: Analyze the current component
Read the target component file. Identify what needs updating.

## Step 3: Apply the V2 design system
- Replace all hardcoded colors with CSS variables from DESIGN.md
- Add `.glass` utility class to all card elements
- Replace `motion/react` with `framer-motion`
- Add `.text-gradient` class to primary headings
- Ensure all spacing follows the 8px grid

## Step 4: Verify
Spin up local server. Take screenshot. Compare to design reference.
Report what changed.
```

### How Progressive Context Loading Works

Claude doesn't load the full skill markdown on every message. The process is:

1. Claude reads the YAML frontmatter (name, description) — lightweight, fast
2. It decides if this skill is relevant to the current task
3. If yes, it loads the full markdown instructions
4. If the skill references external files, it pulls those only if needed

This keeps skills efficient and avoids bloating context.

### The Essential Skills to Build First

**1. Wrapup Skill** (`/wrapup`)
At session end: summarizes the entire conversation, saves key decisions to memory, pushes summary to NotebookLM Brain notebook.

**2. UI/UX Pro Max** (`/ui-ux-pro-max`)
Applies 50+ WCAG AA accessibility fixes, contrast improvements, SEO meta tags, and performance optimizations in one pass.

**3. Website Intelligence** (`/website-intel`)
Uses Firecrawl to scrape a URL, analyzes top 5 competitors, extracts brand identity and differentiators, generates a printable comparison report.

**4. SEO Audit** (`/seo-audit`)
Cross-page technical SEO audit. Checks meta tags, heading hierarchy, internal links, image alt text, sitemap, robots.txt.

**5. Design System Extractor** (`/design-extract`)
Scrapes a competitor website and extracts colors, fonts, spacing, and layout patterns into your DESIGN.md format.

**6. Skill Creator** (`/create-skill`)
The meta-skill. Given a description of a process, it autonomously drafts, tests, benchmarks, and refines a new skill file.

**7. Stitch Loop** (`/stitch-loop`)
Generates multi-page design systems autonomously using Stitch, page by page, with consistent design tokens throughout.

**8. Clone Site** (`/clone-site`)
Deconstructs an existing site into a config-driven architecture (`siteconfig.ts`). AI can then clone it for different businesses, swapping colors, logos, and copy dynamically.

### Super Skills (Karpathy's Framework)

Built on Andrej Karpathy's four foundational principles:

1. **Think before coding** — Plan before execution, always
2. **Simplicity first** — Do the simplest thing that works. Refactor later.
3. **Surgical changes** — Edit only what needs changing. Don't rewrite working code.
4. **Goal-driven execution** — Every action must move toward the defined goal. No tangents.

Super skills also **self-improve**: they score their own outputs, log what worked, and update their own `.md` files over time.

---

## 15. MEMORY SYSTEMS FOR AI

### Why This Matters

Claude Code has no memory between sessions. Every time you open a new session, it starts fresh. Without a memory system, you re-explain your preferences, your project context, and your business rules every single time. This wastes hours.

The solution is a three-bucket memory system.

### The Three-Bucket Memory System

**Bucket 1: Session Logs (Episodic Memory)**
What it stores: Summaries of past Claude Code sessions — what was built, what decisions were made, what problems were solved.
Where it lives: Your NotebookLM Brain notebook + Pinecone vector database
How it gets updated: The `/wrapup` skill runs at session end and pushes a summary

**Bucket 2: Immutable Knowledge (Semantic Memory)**
What it stores: Books, API documentation, course transcripts, technical guides — things that don't change often.
Where it lives: NotebookLM notebooks (by topic) + Pinecone
How to add: Upload documents to NotebookLM, embed into Pinecone for semantic search

**Bucket 3: Active Profile (Working Memory)**
What it stores: Your current strategy, active projects, brand colors, API constraints, personal preferences.
Where it lives: A mutable markdown file: `brain.md` or `spencer.md`
How to update: Manually edit it + the `/wrapup` skill updates it automatically

### The brain.md File

```markdown
# Spencer's AI Brain

## Current Focus
- Primary project: GeoTaskCheck V2
- Active sprint: UI redesign, V2 dashboard

## Brand Identity
- Primary: #ffb786
- Secondary: #83cfff
- Background: #0C0E10
- Aesthetic: Precision Ag glassmorphism

## Tech Stack Preferences
- Always: Next.js + Tailwind + Supabase + Vercel
- Animation: Framer Motion
- Components: ShadCN base + custom glass system

## Rules
- Never suggest WordPress
- Always propose mobile-first
- Commit to GitHub after every major feature
- Run /wrapup at session end

## Active Projects
- GeoTaskCheck: Farming ops platform (main project)
- CropPortal iOS: Swift iOS companion app
- Green Atlas: [status]
```

Claude reads this file at session start and maintains context across sessions.

### The Hermes Agent (Telegram-based AI OS)

An advanced setup where you connect a Telegram bot to your Claude Code environment. You can send tasks to Claude Code from your phone while away from your desk. The agent routes messages through specialized personas (called the "Pantheon"):

- **Labyrinth**: Deep research tasks
- **Architect**: System design decisions
- **Designer**: UI/UX feedback
- Each routes to the optimal model (Claude, Gemini, DeepSeek)

### The Agentic OS "Dreaming" System

Overnight, a background agent analyzes your chat logs, token costs, and workflow patterns. It generates "dreams" — recommendations such as:
- "Switch from Claude Opus to DeepSeek for this task → save $40/month"
- "Build a skill for the SEO workflow you ran 5 times this week"
- "Your context is hitting 80% before tasks complete — split them"

These run while you sleep. You review recommendations in the morning.

---

## 16. AUTOMATION & 24/7 WORKFLOWS

### The Automation Stack (Simple to Complex)

**Level 1: Make.com** (Beginner)
- Visual, linear, no code
- Perfect for connecting two apps
- Example: "When new Supabase row → send Gmail → log to Sheet"

**Level 2: n8n** (Intermediate)
- Complex branching workflows
- Error handling and retries
- Self-hosted (no per-operation fees)
- Integrates with custom Python scripts
- Example: "AI agent reads RSS feeds, generates captions, posts to Instagram"

**Level 3: Modal + Python** (Advanced)
- Serverless execution
- Cron schedules
- Complex multi-step pipelines
- Example: "Every morning at 6am: scrape 1000 leads, enrich emails, send to CRM"

**Level 4: Trigger.dev** (Advanced, long-running)
- For tasks that take 10-30+ minutes
- Automatic retries
- Full execution logs
- Example: "Deep research agent that crawls 100 pages and generates a report"

### The Lead Generation Automation (End to End)

This is a complete, working system for AI agency lead generation:

```
1. Apify actor scrapes Google Maps for target niche (e.g., HVAC companies in California)
   → Outputs: business name, address, website, phone

2. AnyMailFinder enriches the data with verified email addresses

3. Firecrawl scrapes each business website
   → Identifies design quality (is it an ugly website worth rebuilding?)

4. Claude scores each lead (1-10 attractiveness score)

5. Instantly.ai sends personalized cold email sequence
   → Email 1: "We built you a free website" + preview link
   → Email 3 (3 days later): Follow up
   → Email 5 (7 days later): Final follow up

6. GoHighLevel CRM tracks all responses and schedules calls

7. Claude Code generated the "free website" using the Clone Site skill
```

### RSS Feed to Social Media Automation

```
n8n workflow:
1. RSS Feed trigger (every 2 hours) → reads new articles from 20 industry sources
2. Gemini Flash summarizes each article into key insights
3. Claude Sonnet generates 3 Instagram caption variations
4. Nano Banana generates matching hero image
5. Human approval step (optional) or auto-post
6. Schedule post via Buffer or directly to Instagram API
```

### The AI Website Cloning System

Once you have a great website built, clone it for every client:

1. Build a "config-driven" version with a `siteconfig.ts` file:
```typescript
const siteConfig = {
  businessName: "Valley HVAC",
  phone: "(559) 555-0100",
  email: "info@valleyhvac.com",
  colors: { primary: "#FF6B35", secondary: "#1E3A5F" },
  services: ["AC Repair", "Installation", "Maintenance"],
  testimonials: [...],
  hero: { headline: "Fast HVAC Repair You Can Trust", ... }
}
```

2. Build the Clone Site skill: tells Claude to read `siteconfig.ts` and rebuild all content while keeping design

3. For each new client: update `siteconfig.ts` → run `/clone-site` → new website in 5 minutes

---

## 17. SUB-AGENTS & AGENT TEAMS

### Sub-Agents (Stateless Workers)

Sub-agents are specialized AI workers that:
- Run in parallel, each with their own fresh context window
- Handle specific atomic tasks
- Report concise summaries back to the main session
- Often use cheaper models (Haiku, DeepSeek) for cost savings

**When to use:** Any task involving heavy data processing, research across multiple sources, or parallel execution of independent work.

```
Main Session (Claude Sonnet) ─ orchestrator
  ├─ Sub-Agent 1 (Haiku): Scrape competitor 1 website
  ├─ Sub-Agent 2 (Haiku): Scrape competitor 2 website
  ├─ Sub-Agent 3 (Haiku): Scrape competitor 3 website
  └─ Main: Synthesize all three reports into strategy
```

### Agent Teams (Collaborative)

Agent teams differ from sub-agents: team members **share a task list** and can communicate with each other.

**Example team for a full-stack build:**
```
Project Manager Agent:
  - Reads requirements
  - Breaks into tasks
  - Assigns to team members
  - Reviews final output

Frontend Agent (Claude Sonnet):
  - Receives: "Build the dashboard component"
  - Builds it
  - Hands off to QA

Backend Agent (Claude Sonnet):
  - Receives: "Build the API endpoints for dashboard"
  - Builds it
  - Hands off to QA

QA Agent (Claude Haiku):
  - Tests frontend against backend
  - Reports bugs back to respective agents
  - Approves when passing
```

### The Three Brain Auto Router

The most cost-effective multi-model system:

```python
# Routing logic (simplified)
def route_task(task_description):
    if "design" in task_description or "UI" in task_description:
        return "claude-sonnet"  # Design king
    elif "scrape" in task_description or "data" in task_description:
        return "deepseek-v4"    # Cheap workhorse
    elif "review" in task_description or "audit" in task_description:
        return "gpt-5.5-codex"  # Best reviewer
    else:
        return "claude-sonnet"  # Default
```

---

## 18. SEO, PERFORMANCE & WEBSITE VISIBILITY

### Core Web Vitals (Google's Ranking Signals)

These three metrics directly affect your Google search ranking:

**LCP (Largest Contentful Paint)** — How fast does the main content load?
- Target: Under 2.5 seconds
- Fix: Optimize hero images (WebP format), preload critical fonts, use Vercel's Edge Network

**FID / INP (Interaction to Next Paint)** — How fast does it respond to clicks?
- Target: Under 200ms
- Fix: Remove large JavaScript bundles, use React Suspense, lazy-load components

**CLS (Cumulative Layout Shift)** — Does the page jump around while loading?
- Target: Under 0.1
- Fix: Always set explicit width/height on images, avoid inserting content above existing content

**Check your scores:** PageSpeed Insights (pagespeed.web.dev) + Vercel Analytics

### Image Optimization

The single biggest performance win on most websites:

```jsx
// Next.js Image component handles everything automatically
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority    // preload above-fold images
  quality={80}
  placeholder="blur"
  blurDataURL="/hero-blur.jpg"
/>
```

For manual optimization: convert all images to WebP using the Airlift plugin or squoosh.app. WebP is typically 60% smaller than JPEG at identical visual quality.

### Font Performance

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>

<!-- Use font-display: swap to prevent invisible text during load -->
<style>
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter.woff2') format('woff2');
    font-display: swap;
  }
</style>
```

### On-Page SEO Checklist

Every page must have:
```html
<!-- Title: 50-60 characters, includes primary keyword -->
<title>AI Farming Software | GeoTaskCheck - Precision Ag Platform</title>

<!-- Description: 150-160 characters, compelling, includes keyword -->
<meta name="description" content="Track field tasks, geofences, and weather data in real-time. Built for California farmers. Free trial.">

<!-- Open Graph (social sharing) -->
<meta property="og:title" content="GeoTaskCheck - Precision Ag Platform">
<meta property="og:description" content="...">
<meta property="og:image" content="https://yourdomain.com/og-image.jpg">

<!-- Canonical URL (prevents duplicate content penalties) -->
<link rel="canonical" href="https://yourdomain.com/page">
```

In Next.js:
```typescript
export const metadata: Metadata = {
  title: 'AI Farming Software | GeoTaskCheck',
  description: 'Track field tasks, geofences, and weather data...',
  openGraph: {
    images: ['/og-image.jpg'],
  },
};
```

### Technical SEO

```
✓ Submit sitemap to Google Search Console (sitemap.xml)
✓ Check robots.txt allows crawling of important pages
✓ All pages use HTTPS (Vercel does this automatically)
✓ Mobile-responsive (test with Google Mobile-Friendly Test)
✓ Structured data (JSON-LD) for local businesses
✓ Internal linking between related pages
✓ Image alt text on every image
✓ Heading hierarchy: one H1 per page, logical H2/H3 structure
```

### Analytics Setup

**Google Analytics 4:** Track users, sessions, events, conversions.

```javascript
// Add to Next.js layout
import { GoogleAnalytics } from '@next/third-parties/google';

<GoogleAnalytics gaId="G-XXXXXXXXXX" />
```

**Vercel Analytics:** Built-in performance monitoring. Enable in Vercel dashboard. Tracks Core Web Vitals automatically.

**Hotjar:** Records user sessions as videos. Shows exactly where users click, scroll, and get confused. Invaluable for CRO (Conversion Rate Optimization).

### Conversion Rate Optimization (CRO)

Getting traffic is one challenge. Getting that traffic to take action is another.

**The above-the-fold checklist:**
- [ ] Clear headline that states the value in under 8 words
- [ ] Subheadline that explains who it's for and what problem it solves
- [ ] Social proof visible without scrolling (logos, testimonial, user count)
- [ ] Primary CTA button is high-contrast and action-oriented ("Start Free Trial" not "Learn More")
- [ ] No navigation items that distract from the CTA

**Trust signals that convert:**
- Client logos (even 3-4 logos significantly increase trust)
- Specific numbers ("saves 4 hours per week" not "saves time")
- Before/after comparisons
- Video testimonials
- Money-back guarantee with specific terms

---

## 19. BUSINESS FRAMEWORKS

### The MONEY Framework (For Selling AI Websites)

```
M - Map the niche
    Target boring, unsexy, profitable businesses:
    - HVAC contractors
    - Pool cleaners
    - Plumbers
    - Roofing companies
    - Pest control
    - Lawn care
    
    Why these? High revenue per customer, terrible websites, can't hire
    technical staff, desperately need leads.

O - Obtain leads
    Use Apify to scrape Google Maps for "[niche] in [city]"
    → Get: business name, phone, website URL, rating, reviews
    Use AnyMailFinder to get verified emails
    Target: businesses with < 3.5 stars AND ugly websites

N - Nail the website
    Build a free, gorgeous website using the Clone Site skill
    Set up a preview URL on Vercel
    Personalize with their logo, colors, service list

E - Execute outreach
    Cold email: "We built [Business Name] a free website upgrade."
    Subject: "Free website for [Business Name]"
    Body: 3 sentences. Preview link. No fluff.
    Use Instantly.ai to send 50-100 emails/day automatically

Y - Yield the recurring revenue
    "Razor blades" model:
    - Give the website for free (or $0-500 setup)
    - Charge $300-500/month for: hosting, maintenance, SEO, AI chatbot
    - 10 clients × $300/month = $3,000 MRR passive income
```

### The ROI Pitch

Never sell "a website." Sell the business outcome.

**Wrong:** "I'll build you a modern website with animations for $2,000."

**Right:** "Your current website converts at under 1%. Industry average is 3%. If you close 10 leads/month at $3,000 each, a 1% conversion improvement = $3,000 extra revenue. My fee pays for itself in the first month."

Calculate the ROI before pitching. Present it first.

### The AI Agency Stack (Full Build)

```
Client Discovery:     Firecrawl → Website Intelligence Skill
Proposal:             Claude → Custom ROI calculation document
Design:               Stitch + AI Studio → Figma-quality mockup in 2 hours
Build:                Antigravity + Claude Code → Production in 1-3 days
QA:                   TestSprite MCP + Screenshot Loop
Deploy:               GitHub → Vercel (automatic)
Ongoing:              n8n automations for client's business processes
Reporting:            Claude → Monthly performance report from GA4 data
Upsell:               AI chatbot (11Labs), SEO retainer, lead gen automation
```

---

## 20. THE BIGGEST MISTAKES BEGINNERS MAKE

### Mistake 1: Starting Without a CLAUDE.md

AI has no idea what your project is, your brand colors, your tech stack, or your rules unless you tell it. Every session. Without a CLAUDE.md, you waste the first 10-15 minutes re-explaining context that should be automatic.

**Fix:** Build your CLAUDE.md before writing a single line of code.

### Mistake 2: Ignoring Context Rot

The AI degrades as sessions get longer. Beginners add more and more tasks to one conversation and wonder why the AI starts breaking things it built earlier.

**Fix:** One task per message. Use `/compact` at 60%. Use `/clear` between different task types.

### Mistake 3: Using One Model for Everything

Claude for your Python scraper costs 100x more than DeepSeek and produces the same result. ChatGPT for your UI design produces worse results than Claude.

**Fix:** Learn the Three Brain system. Route tasks to the appropriate model.

### Mistake 4: Building Without Version Control

The AI will break things. It will delete working code. It will make a change that cascades into 20 other broken files. Without Git, you lose that work permanently.

**Fix:** `git init` + `git commit` after every significant working state. Never build without it.

### Mistake 5: Giving AI Too Much Permission

Auto-approved MCP access to send emails, delete files, or push to main branch. One bad prompt and your AI sends 500 emails to clients, deletes your production database, or pushes broken code live.

**Fix:** Only read + draft permissions. Humans review and execute all destructive/external actions.

### Mistake 6: Not Using Plan Mode

Jumping straight to "build it" without having the AI plan first. This produces code that works for the happy path but breaks on every edge case.

**Fix:** Always press Shift+Tab in Claude Code before any significant task. Always.

### Mistake 7: Building Visually Blind

Asking AI to "make it look good" without giving it a reference. AI default aesthetics are generic. "AI slop" is real and clients notice it.

**Fix:** Always provide HTML extraction from a reference site, or pull from 21st.dev/CodePen for specific components.

### Mistake 8: Deploying Without Performance Optimization

Large unoptimized images, no font preloading, no lazy loading = slow site = poor Google ranking = poor user experience = lost clients.

**Fix:** Run every site through PageSpeed Insights before delivery. Fix all red items.

### Mistake 9: Not Building Skills

Doing the same multi-step workflow by hand every time. Typing out the same instructions repeatedly.

**Fix:** After doing anything complex more than twice, turn it into a skill. The time investment to write the skill pays back in hours immediately.

### Mistake 10: Treating AI as Infallible

AI makes mistakes. It hallucinates. It confidently writes code that breaks. It uses deprecated APIs. It misunderstands requirements.

**Fix:** Always review output. Use Codex as a second reviewer for important code. Test before shipping. Never blindly approve AI output.

---

## 21. YOUR FIRST PROJECT: STEP BY STEP

### Project: Build a Business Website (Marketing Site)

This walkthrough assumes zero prior experience.

**Phase 1: Research & Planning (1 hour)**

1. Choose a business type (use one you understand — your own business, a relative's business, or a local business)
2. Open Claude.ai or Claude Code
3. Prompt: "I want to build a marketing website for [business type]. Before we start any design or code, help me define: the target audience, the top 3 pain points they have, the top 3 objections to hiring this business, and the single action we want visitors to take."
4. Save this output — it becomes your copywriting foundation
5. Open Dribbble.com and find 3 websites in a similar style to what you want. Screenshot them.
6. Open a website you love (competitor or inspiration). Right-click → View Page Source. Copy the HTML.

**Phase 2: Design (30 minutes)**

1. Go to Google AI Studio (aistudio.google.com)
2. Upload your screenshot references
3. Prompt: "Using these visual references, generate a homepage layout for [business type]. Use a dark color scheme with [color] as the accent. Include: hero section, services section, testimonials, and CTA."
4. Review the output. Download the code.
5. Iterate 2-3 times until satisfied.

**Phase 3: Setup (15 minutes)**

1. Install Node.js (nodejs.org)
2. Create a Next.js project:
```bash
npx create-next-app@latest my-project
cd my-project
```
3. Create a GitHub repository and push
4. Link to Vercel for automatic deployment

**Phase 4: Build (2-4 hours)**

1. Open Claude Code in your project folder:
```bash
claude
```
2. Press Shift+Tab (Plan Mode)
3. Prompt: "Build me a homepage for [business type] based on this design. Tech stack: Next.js 15, Tailwind CSS, ShadCN UI. Here is the design from AI Studio: [paste code]. Here are the brand guidelines: primary color [color], font [font]. Start by building just the Hero section. Ask me questions before coding."
4. Review the plan Claude provides. Add corrections.
5. Approve. Let it build.
6. Review the output. Request adjustments.
7. Continue section by section: Hero → Services → Testimonials → Footer → CTA

**Phase 5: Deploy (10 minutes)**

1. Push to GitHub: `git add -A && git commit -m "initial build" && git push`
2. Vercel auto-deploys. You have a live URL.
3. Run PageSpeed Insights on the live URL.
4. Fix any critical performance issues.

**Phase 6: Submit to Google (5 minutes)**

1. Create Google Search Console account
2. Submit your domain
3. Submit sitemap: `yourdomain.com/sitemap.xml` (Next.js generates this automatically)

**Total time: 4-6 hours for a professional marketing website.**

---

## 22. QUICK REFERENCE CHEAT SHEET

### Claude Code Commands

| Command | What It Does |
|---|---|
| Shift+Tab | Enter Plan Mode |
| /compact | Compress context |
| /clear | Wipe context clean |
| /context | Show token usage breakdown |
| /ultrathink | Extended reasoning mode |
| /ultrareview | Cloud-based multi-agent QA review |
| claude-worktree | Create isolated parallel build session |

### Model Quick Pick

| Task | Model |
|---|---|
| Design / UI / UX | Claude Opus/Sonnet |
| Large codebase / multimodal | Gemini Pro |
| Code review / error finding | Codex (GPT-5.5) |
| Heavy data tasks / automation | DeepSeek V4 |
| Private / free | Ollama (Gemma 4) |

### The Daily Build Workflow

```
1. Start session → CLAUDE.md auto-loaded
2. Check auth: gh auth status && py -m notebooklm list
3. Plan Mode (Shift+Tab) → Define task clearly
4. Build → ONE task at a time
5. Review output → git commit working state
6. /compact at 60% context
7. /clear before switching task types
8. /wrapup at session end → saves to NotebookLM Brain
```

### Framework Quick Reference

| Building a... | Use Framework |
|---|---|
| Full-stack app | BLAST |
| Marketing website | SITE |
| Claude Code session | CODA |
| Agentic workflow | WAT |
| Software architecture | FLOW |
| Stitch design project | DRIP |
| Long multi-step project | GSD |

### The Tech Stack

```
Frontend:   Next.js 15 + React 19 + Tailwind CSS 4
Components: ShadCN UI + Magic UI + Aceternity UI
Animation:  Framer Motion + GSAP
3D:         Spline + Three.js
Database:   Supabase (PostgreSQL)
Auth:       Supabase Auth
Deploy:     Vercel + GitHub
Serverless: Modal (Python) / Trigger.dev (long-running)
Automation: n8n (complex) / Make.com (simple)
```

### Design Tokens Template

```css
--color-primary: #ffb786;
--color-secondary: #83cfff;
--color-bg: #0C0E10;
--color-bg-card: rgba(255,255,255,0.05);
--space-unit: 8px;
--radius-card: 16px;
--font-sans: 'Inter', system-ui, sans-serif;
```

### The Three Brain System

```
Claude    → Design, UI, architecture, writing
DeepSeek  → Scraping, heavy data, background tasks
Codex     → Code review, error detection, auditing
```

### MCP Priority List

1. Context 7 (always — prevents deprecated API hallucinations)
2. Supabase (every app project)
3. GitHub + Vercel (every deployment)
4. Firecrawl (every research or competitor analysis task)
5. Playwright (every UI project — visual QA)

---

## FINAL WORDS

The gap between a beginner and an expert AI builder is not intelligence. It is **systems**.

Experts have:
- A CLAUDE.md that front-loads all context
- A set of skills that never repeat work
- A memory system that never loses decisions
- A model routing system that matches task to tool
- A framework that eliminates ad-hoc prompting
- Git running at all times
- Plan Mode as a default reflex

Build these systems. Start small. Add one skill this week. Add another next week. By month three you will build in a day what used to take a week.

The tools change rapidly. The principles in this document are permanent. Come back to it often.

---

*Last updated: May 2026 | Sources: Jack Roberts AI Guide, JACK AI UPDATED, AI Coding (Antigravity) Structure & Tips, AI Studio Redesign, 3D Website Creation*
