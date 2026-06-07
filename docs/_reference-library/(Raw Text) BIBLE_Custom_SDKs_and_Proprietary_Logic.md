> ⚠️ **NOTE:** This document is **NOT** the official scaffold/structure of this project.
> It's a reference library — ideas, themes, and tools to draw from when building out
> website-builder's actual scaffolding. Treat it as inspiration/lookup, not as the plan.

---

# Chapter 6: Custom SDKs, Private MCPs & Proprietary Tooling

This document outlines the strategy and technical implementation for building custom Software Development Kits (SDKs) and private Model Context Protocol (MCP) servers. These tools allow a company to encapsulate proprietary business logic and unique workflows into reusable assets that AI agents can consume with high reliability.

## 1. The "AI-First" SDK: Designing for Agent-Computer Interfaces (ACI)

Traditional SDKs are built for humans (HCI). An "AI-First" SDK is built for agents (ACI), shifting the focus from ease of reading to **determinism of execution**.

### Design Principles:
*   **Docstrings as Executable Prompts:** Functions should be named by their intent (e.g., `calculate_custom_roofing_quote` vs `get_quote`). Docstrings must describe the "why," specify constraints, and define the expected output format.
*   **Type-Safety as a Sandbox:** Use Pydantic (Python) or Zod (TypeScript) to enforce strict schemas. This prevents agents from passing hallucinated or malformed data into your business logic.
*   **Diagnostic Error Handling:** Instead of "Error 500," return actionable, natural-language feedback (e.g., "Error: 'Material_Type' must be 'Tile' or 'Shingle'. Please choose one and retry."). This allows the agent to self-correct and pivot without human intervention.
*   **Workflow-Centric Tools:** Build "Compound Tools" that encapsulate entire business processes (e.g., `onboard_new_vendor`) rather than exposing low-level, individual database calls.

## 2. Private MCP Servers: The Ultimate Portable SDK

Jack Roberts recommends **"Portable MCPs"** to house proprietary logic that should stay separate from the main application code but remains accessible across all your AI projects.

### Implementation Patterns:
*   **FastMCP (Python):** Use the `mcp` library to turn any existing Python script or internal API into an AI-ready tool in minutes using the `@mcp.tool()` decorator.
*   **Stdio Transport for Privacy:** Run your custom MCP servers via **Standard Input/Output (stdio)** instead of a web port. This creates a "Zero-Network" attack surface, as the server runs as a local child process, keeping your data 100% private.
*   **Local-First Database Wrappers:** Wrap local SQLite or Postgres databases in an MCP server. This allows agents to query inventory, CRM data, or logs without exposing a public API endpoint.

## 3. Packaging & Distributing "Skills" as Assets

To make excellence "super repeatable" and "scalable," Jack Roberts suggests packaging workflows as company-wide assets.

### Distribution Strategies:
*   **Global Skills:** Flags within the IDE to make specific `.skill` files available across all project workspaces on a machine.
*   **Bundled Plugins:** Grouping related skills (e.g., a "Sales Stack" containing a LinkedIn scraper, Lead Qualifier, and CRM Logger) into a single downloadable plugin for the whole team.
*   **Internal AI Operating Systems:** Moving from "single agents" to a centralized system that connects a company’s entire data world—integrating local memory, vector databases, and multi-model routing into one cohesive dashboard.

## 4. Proprietary Frameworks & Determinism

Use rigid frameworks to force the AI into a deterministic path. Jack Roberts' "Secret Sauce" includes:
*   **STAND Framework:** Used for building profitable AI dashboards (Structure, Table, Auth, No-code, Design).
*   **BLAST Framework:** The master logic for deterministic app development (Blueprint, Links, Architect, Stylize, Trigger).
*   **ACE Framework:** A methodology for scaling a raw idea into a fully automated enterprise system.

---
**Summary:** By building your own SDKs and MCPs, you move from "asking the AI to write code" to "directing the AI to use your proprietary tools." This ensures consistency, security, and true scalability for your AI-powered agency or business.
