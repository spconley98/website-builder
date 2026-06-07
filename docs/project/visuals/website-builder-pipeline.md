# website-builder Architecture

> Mind map of the project goal + pipeline, generated from `docs/project/ARCHITECTURE.md`.
> Open with **Markmap** plugin in Obsidian for an interactive visual tree. Share-ready for Matt.

---

- website-builder Architecture
  - Vision & Goal
    - Local-AI lead pipeline
    - Target businesses without websites
    - Local processing (Ollama/RTX 3090)
    - Automated research & prioritization
  - Project Scope
    - In Scope
      - Lead research pipeline
      - Lead Finder & Prioritizer agents
      - Data store & reports
    - Out of Scope
      - Website templates
      - Site production & sales
      - Branding & photo transfer
  - Technical Architecture
    - Language: Python
    - Orchestration: File-based pipeline
    - Storage: JSONL (leads.jsonl)
    - Interface: Typer CLI
    - Package Manager: uv
  - The Pipeline Process
    - Acquisition: Google Places API
    - Enrichment: Firecrawl
    - Reasoning: Local LLM (Ollama)
    - Human View: Generated Markdown
  - Data Schema
    - Key: place_id
    - Status: found, prioritized, contacted, sold
    - Rating: 1-5 photo-count thresholds
    - Details: industry, location, urls
  - Current Constraints
    - Firecrawl credits needed
    - Google Places billing setup
    - Local model selection pending
    - Matt onboarding pending
