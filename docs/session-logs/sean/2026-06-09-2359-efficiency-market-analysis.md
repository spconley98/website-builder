---
type: session-log
contributors: [sean]
agent: gemini
status: active
created: 2026-06-09
updated: 2026-06-09
topic: efficiency-market-analysis
tags: [sessions, research, planning]
related: ["[[MEMORY]]", "[[AGENTS]]"]
---

# Session Log — Efficiency & Market Analysis

This document contains the complete recommendations generated during the pressure test and market analysis of the website-builder pipeline. These are the immediate next priorities to address.

## 1. Codebase Efficiency & Technical Gaps (Pressure Test)
The architecture is wonderfully simple, but the codebase investigator identified significant bottlenecks that will cause the pipeline to fail or stall as you scale beyond small batches (e.g., trying to process hundreds of leads):

*   **O(N²) Data Persistence Bottleneck:** The `LeadStore` (`src/leadpipe/store.py`) reads and rewrites the *entire* JSONL file for every single lead update. In a batch run of 20 leads, the entire database is rewritten 20 times per stage. 
*   **Synchronous I/O:** The Lead Finder, Prioritizer, and Website Intelligence agents process leads completely sequentially. Every Google Places fetch, Firecrawl scrape, and Ollama call waits for the previous one to finish.
*   **Connection Overhead:** Most source modules create a new HTTP client for every single request instead of using connection pooling.
*   **Arbitrary Truncation:** Scraping results are hard-truncated (e.g., 6,000 characters). You risk losing critical data located at the bottom of web pages (like photo galleries) that the Prioritizer needs to evaluate buildability.

**Tools & Methods to Install:**
1.  **`asyncio` + `httpx.AsyncClient`:** Refactor the network layer to be fully asynchronous. This will provide a massive speedup by parallelizing Google Places and Firecrawl calls.
2.  **SQLite (`sqlite3`):** Replace the JSONL flat-file with a local SQLite database. This allows atomic, row-level updates and eliminates the O(N²) read/write bottleneck while keeping the data local and portable.
3.  **`tenacity`:** Install this Python library to implement robust exponential backoff and retry logic for LLM timeouts and API rate limits.

## 2. Constitution Updates (`AGENTS.md`)
Now that the project has transitioned from "scaffolding" to "operations," your constitution needs rules for *operating* the pipeline safely. I recommend updating `AGENTS.md` with the following:

*   **Operational "Hunt" Rhythm:** Add a standard sequence for data acquisition tasks (e.g., `target selection → find (dry-run) → enrich (Firecrawl) → sync data`). This ensures agents know the safe sequence for running the CLI without accidentally burning Firecrawl credits.
*   **Territory Coordination:** Add a rule requiring you and Matt to claim "territories" in `MEMORY.md` (e.g., Sean = NorCal, Matt = TX). This prevents you both from spending Google Places/Firecrawl API credits on the exact same leads.
*   **Mandatory Post-Hunt Syncs:** Update the Selective Import Protocol. Mandate that `data/` and `reports/` must be synced immediately after a hunt completes so the shared deduplication logic (`place_id`) actually works across both profiles.
*   **Validation of AI Generation:** Extend the "No-Self-Review" law to the new Website Briefs. Define whether a human or a secondary LLM must review the generated briefs before they are cleared for actual sales outreach.

## 3. Market Research & Competitor Landscape
The strategy of targeting local businesses without websites via Google Maps is a proven, highly active niche. What makes your approach competitive is the local-AI automation.

*   **The Competitors:** There are Vertical SaaS platforms doing this (Webleadr, Scrap.io) and many growth hackers building automated pipelines using tools like **Apify**, **n8n**, **Make.com**, and **Bright Data**.
*   **What Makes Them Successful (The "Vitality Signal"):**
    *   Raw scraping yields a lot of junk (e.g., closed businesses or solo contractors working out of their trucks). Successful competitors use LLMs specifically to hunt for **Vitality Signals**. 
    *   If a business has *no website* but has *150+ positive reviews, active hours, and recent photos*, they have cash flow but poor digital infrastructure. That is the golden ticket.
*   **Actionable Insights for Our Project:**
    1.  **Cost Advantage:** Because you are using `Ollama` locally instead of OpenAI/Gemini, you can afford to run much deeper, multi-step reasoning on each lead without incurring massive API costs.
    2.  **Cross-Referencing:** Competitors often cross-reference leads with Facebook or Yelp. If a lead has an active social media page but no domain, they understand digital marketing but lack a professional hub—an easier sell. 
    3.  **Demo Generation:** The highest-converting agencies use the scraped data to automatically generate a watermarked "Demo Website" mockup *before* they even contact the lead.