"""Helpers for keeping scraped listing content safe for local LLM prompts."""
from __future__ import annotations

_KEYWORDS = (
    "photo",
    "photos",
    "image",
    "images",
    "gallery",
    "review",
    "reviews",
    "hours",
    "phone",
    "contact",
    "service",
    "services",
    "menu",
    "address",
)


def compact_scraped_content(markdown: str, *, max_chars: int) -> str:
    """Bound scraped content while preserving the top, useful snippets, and tail."""
    text = markdown.strip()
    if len(text) <= max_chars:
        return text

    marker = "\n\n[...scraped content compacted for local LLM timeout guard...]\n\n"
    head_budget = max_chars // 2
    tail_budget = max_chars // 4
    middle_budget = max_chars - head_budget - tail_budget - len(marker)

    head = text[:head_budget].rstrip()
    tail = text[-tail_budget:].lstrip()
    middle = ""
    if middle_budget > 0:
        middle_start = head_budget
        middle_end = len(text) - tail_budget
        middle_region = text[middle_start:middle_end]
        useful_lines = [
            line.strip()
            for line in middle_region.splitlines()
            if any(keyword in line.lower() for keyword in _KEYWORDS)
        ]
        if useful_lines:
            middle_text = "\n".join(useful_lines)
            middle = middle_text[:middle_budget].strip()

    parts = [head, marker.strip()]
    if middle:
        parts.extend(["Relevant middle excerpts:", middle])
    parts.append(tail)
    compacted = "\n\n".join(part for part in parts if part)
    return compacted[:max_chars]
