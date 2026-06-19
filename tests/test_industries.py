"""Tests for the industry -> broad-category grouping used by reports.py."""
from __future__ import annotations

from leadpipe.industries import CategoryRule, industry_group, load_industry_categories

_RULES = [
    CategoryRule(label="Trades", match=["plumb", "electric", "hvac", "roof", "handyman", "landscap"]),
    CategoryRule(label="Food & Beverage", match=["coffee", "cafe", "restaurant"]),
]


def test_industry_group_matches_trades():
    assert industry_group("plumbing", _RULES, "Other") == "Trades"
    assert industry_group("HVAC contractors", _RULES, "Other") == "Trades"


def test_industry_group_matches_food_and_beverage_case_insensitively():
    assert industry_group("Coffee Shops", _RULES, "Other") == "Food & Beverage"


def test_industry_group_falls_back_to_other():
    assert industry_group("pet grooming", _RULES, "Other") == "Other"


def test_load_industry_categories_reads_repo_config():
    categories, other_label = load_industry_categories()

    assert other_label == "Other"
    labels = [c.label for c in categories]
    assert "Trades" in labels
    assert "Nursery & Garden" in labels
    assert industry_group("plumbing", categories, other_label) == "Trades"
    assert industry_group("coffee shops", categories, other_label) == "Food & Beverage"
    # nurseries/garden centers are their own niche, not "Other" (regression guard)
    assert industry_group("plant nursery", categories, other_label) == "Nursery & Garden"
    assert industry_group("garden center", categories, other_label) == "Nursery & Garden"
    # landscaping still wins for Trades (rule order: Trades before Nursery & Garden)
    assert industry_group("landscaping", categories, other_label) == "Trades"
    assert industry_group("concrete curbing", categories, other_label) == "Trades"
