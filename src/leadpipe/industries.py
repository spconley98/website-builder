"""Broad-category groupings for Lead.industry, used to render collapsible
sections in reports.py. Pure rendering-time lookup — does not touch the
acquired-fact `industry` string itself.
"""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATEGORIES_PATH = ROOT / "config" / "industry_categories.yaml"


class CategoryRule(BaseModel):
    label: str
    match: list[str] = []


class _CategoriesFile(BaseModel):
    categories: list[CategoryRule] = []
    other_label: str = "Other"


def load_industry_categories(path: Path | None = None) -> tuple[list[CategoryRule], str]:
    """Returns (category rules, other_label). Missing/empty file -> no rules,
    everything falls into the default "Other" label."""
    path = path or DEFAULT_CATEGORIES_PATH
    if not path.exists():
        return [], "Other"
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    parsed = _CategoriesFile.model_validate(raw)
    return parsed.categories, parsed.other_label


def industry_group(industry: str, categories: list[CategoryRule], other_label: str = "Other") -> str:
    lowered = industry.lower()
    for rule in categories:
        if any(keyword.lower() in lowered for keyword in rule.match):
            return rule.label
    return other_label
