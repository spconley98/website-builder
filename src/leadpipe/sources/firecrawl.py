"""Firecrawl — enrichment fallback (ARCHITECTURE.md §5).

Hits the REST API directly rather than the MCP server: MCP tools only load on
a session restart (see memory note `firecrawl-mcp-rest-workaround` / AGENTS.md
§6), but agent code runs continuously — REST is the only option that works
mid-run regardless of MCP state. Same key, same endpoints either way.

NOTE: as of this scaffold, Sean's Firecrawl account is out of credits — calls
will raise FirecrawlError("insufficient credits...") until topped up. This is
expected; the pipeline should degrade gracefully (skip enrichment, don't crash)
when that happens. See lead_prioritizer.py for how it's handled.
"""
from __future__ import annotations

import httpx

from ..config import load_settings

_BASE = "https://api.firecrawl.dev/v1"
DEFAULT_TIMEOUT = 60.0


class FirecrawlError(RuntimeError):
    """Raised for any Firecrawl failure — including the known 'insufficient
    credits' state, so callers can catch ONE thing and decide how to degrade."""


def _client(api_key: str) -> httpx.Client:
    return httpx.Client(
        base_url=_BASE,
        timeout=DEFAULT_TIMEOUT,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )


def _post(path: str, payload: dict, *, api_key: str | None = None) -> dict:
    settings = load_settings()
    key = api_key or settings.firecrawl_api_key
    if not key:
        raise FirecrawlError(
            "FIRECRAWL_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    try:
        with _client(key) as client:
            resp = client.post(path, json=payload)
    except httpx.TimeoutException as e:
        raise FirecrawlError(f"Firecrawl request to {path} timed out after {DEFAULT_TIMEOUT}s") from e
    except httpx.ConnectError as e:
        raise FirecrawlError(f"could not reach Firecrawl at {_BASE}{path}") from e

    body = resp.json()
    if not body.get("success", False):
        # Firecrawl returns 200 with success=False for things like credit exhaustion —
        # surface the message verbatim so "insufficient credits" is recognizable.
        raise FirecrawlError(body.get("error", f"Firecrawl request to {path} failed: {body}"))
    return body


def search(query: str, *, limit: int = 5) -> list[dict]:
    """Web search — used to find a business's Yelp/Google listing pages when
    Lead Finder didn't already capture a direct URL."""
    body = _post("/search", {"query": query, "limit": limit})
    return body.get("data", [])


def scrape(url: str) -> str:
    """Scrape a page to markdown — used to read a Yelp/Google listing for
    photo-count enrichment when the structured APIs don't give us enough."""
    body = _post("/scrape", {"url": url, "formats": ["markdown"]})
    return body.get("data", {}).get("markdown", "")


def get_credit_usage(*, api_key: str | None = None) -> dict | None:
    """Get the current credit usage from the team API.
    Returns:
        dict: {"remainingCredits": int, "planCredits": int, ...} or None on failure.
    """
    settings = load_settings()
    key = api_key or settings.firecrawl_api_key
    if not key:
        return None
    try:
        with _client(key) as client:
            resp = client.get("https://api.firecrawl.dev/v2/team/credit-usage")
            if resp.status_code == 200:
                body = resp.json()
                if body.get("success", False):
                    return body.get("data")
    except Exception:
        pass
    return None

