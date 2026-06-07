> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — ideas, themes, and tools to draw from when building out
> website-builder's actual scaffolding. Treat it as inspiration/lookup, not as the plan.

---

# Comprehensive MCP Server & Tool Database

This document provides a deduplicated, categorized master list of Model Context Protocol (MCP) servers and tools for AI-assisted development. The data is aggregated from the "Jack Roberts AI Guide" (Antigravity), YouTube AI coding creators, and specialized web design research.

## 1. Core Development, Coding & Collaboration
*MCPs for managing repositories, tasks, design specs, and team communication.*

*   **GitHub:** Essential for managing PRs, issues, and repository history directly. Automates "Source Code in Description" workflows.
*   **Figma (Official & Framelink):** Enables "design-to-code" workflows. Exposes layer hierarchies, auto-layout, and tokens. Framelink optimizes for React/Tailwind conversion.
*   **Linear:** Syncs the agent with task management. Fetch issue details or update task statuses via natural language.
*   **Slack:** Allows agents to read team conversations or search for context not present in the codebase.
*   **Notion:** Project management and documentation. Agents read client requests, create SOPs, and log action items.
*   **Context 7:** Fetches latest API documentation for thousands of libraries (React, Tailwind, Next.js, etc.) to prevent LLM hallucinations.
*   **Sequential Thinking:** Helps the AI "think out loud" through complex architectural or debugging steps.
*   **Open Code (OpenRouter):** Unlocks access to over 150 AI models, allowing the orchestrator to swap models based on task complexity.

## 2. Web Design, UI/UX & Asset Generation
*MCPs specifically for frontend development, iconography, and visual asset creation.*

*   **Google Stitch 2.0:** UI/UX design agent that extracts brand visual identities and builds multiple app screens simultaneously.
*   **Nano Banana 2 / Pro:** In-IDE image generation model for creating consistent visual assets, graphics, and thumbnails.
*   **Shadcn / Radix UI MCP:** Specialized for the `shadcn/ui` registry and Radix primitives. Ensures correct imports and accessible implementation patterns.
*   **TailwindCSS MCP:** Utility class lookups, CSS-to-Tailwind conversion, and documentation search.
*   **Better Icons:** Supports 200+ icon libraries (Lucide, FontAwesome, etc.). Injects icons directly into code files.
*   **Spline:** Used for building interactive 3D elements and scrolling animations into websites.
*   **Gamma:** Presentation AI for generating formatted PowerPoint decks and PDFs from raw notes or transcripts.
*   **Canva MCP:** Generates structured app UIs and ensures compliance with design guidelines.

## 3. Research, Memory & RAG (Retrieval Augmented Generation)
*MCPs for deep data extraction, web search, and long-term memory.*

*   **NotebookLM:** Google’s research engine. Acts as the "knowledge backbone" for agents to provide fact-based insights and generate reports.
*   **Firecrawl / Crawl4AI:** Agentic web scrapers for "chatting with websites." Converts documentation or competitor sites into clean Markdown for RAG.
*   **Brave Search / Exa:** Gives agents live web access. Exa is optimized for providing high-quality, AI-ready technical documentation context.
*   **Pinecone:** Vector database for long-term semantic memory, allowing agents to recall project-specific info without bloating the context window.
*   **Nia (nozomioai):** Provides "Sandbox Agentic Search" to reduce hallucinations in tools like Claude Code.
*   **Apify:** Platform with 8,000+ API actors for extracting structured leads (Google Maps, LinkedIn, etc.) or niche datasets.

## 4. Backend, Databases & Infrastructure
*MCPs for managing databases, serverless functions, and deployment.*

*   **Supabase:** Primary relational database integration. Agents can write SQL, manage schemas, handle auth, and store files autonomously.
*   **Neon / PlanetScale:** Postgres/MySQL integrations. Allows the AI to create projects and run queries using natural language.
*   **Vercel:** Hosting platform integration. Pulls live web analytics and build logs directly back into the IDE.
*   **Modal / Railway:** Serverless platforms for running background scripts (e.g., Python scrapers) that run autonomously 24/7.
*   **Stripe:** Handles monetization, checkouts, and payments for full-stack SaaS applications.
*   **Cloudflare:** Allows agents to write TypeScript code to interact with Cloudflare's Edge APIs and Workers directly.

## 5. Testing, Validation & Multimedia
*MCPs for browser automation, video production, and quality assurance.*

*   **Playwright:** Browser automation for self-verifying UI changes, testing responsiveness, and "self-healing" visual bugs.
*   **BrowserStack:** Cross-browser and real-device testing (e.g., testing on iPhone Safari) to identify CSS bugs.
*   **Remotion:** Allows agents to generate videos programmatically using React code.
*   **VidLens:** Advanced visual indexing for searching frames and analyzing visual hooks in YouTube videos.
*   **ElevenLabs:** The gold standard for AI voiceovers. Agents generate high-fidelity narration directly from script files.
*   **Sentry / Datadog:** Investigates runtime logs and error states directly from the IDE for debugging.
