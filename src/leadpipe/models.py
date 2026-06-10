"""The Lead record — the single shape every agent reads and writes.

Schema + status lifecycle locked in during the architecture grill session
(see docs/project/ARCHITECTURE.md §4 / §9).

DESIGN NOTE (post three-brain/Codex adversarial review): a single mutable
`Lead` used as both the canonical record AND the update payload let any agent
silently overwrite any field — including Google-Places-acquired FACTS getting
clobbered by LLM-derived enrichment, and lifecycle `status` regressing
backwards. That breaks the architecture's core principle: "APIs acquire facts,
the LLM only reasons." So writes are now split by stage:

  - LeadCreate              — what Lead Finder is allowed to write (facts)
  - LeadPrioritization      — what Lead Prioritizer is allowed to write (judgment)
  - Lead                    — the canonical merged record in the store

Agents never construct a bare `Lead` to upsert; they build a stage-specific
object and the store applies it through an explicit allowlist (store.py).
"""
from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field

# Ordered lifecycle — used to prevent status from moving backwards.
_STATUS_ORDER = ["found", "prioritized", "contacted", "sold", "invalid", "archived"]


class LeadStatus(StrEnum):
    FOUND = "found"
    PRIORITIZED = "prioritized"
    CONTACTED = "contacted"
    SOLD = "sold"
    INVALID = "invalid"
    ARCHIVED = "archived"

    @property
    def rank(self) -> int:
        return _STATUS_ORDER.index(self.value)


class LeadCreate(BaseModel):
    """What Lead Finder produces. These are ACQUIRED FACTS — the store treats
    them as authoritative on first insert and never lets later stages mutate
    them (a re-run of Lead Finder may refresh them; Prioritizer may not)."""

    place_id: str
    name: str
    industry: str
    location: str
    has_website: bool = Field(
        ..., description="Must be False to become a stored Lead — see store.create()."
    )
    found_date: date
    source: str = "google_places"
    google_maps_url: str | None = None
    yelp_url: str | None = None
    phone_present: bool | None = None
    recent_review_count: int | None = Field(default=None, ge=0)
    hours_present: bool | None = None
    staleness_flags: list[str] = Field(default_factory=list)


class LeadPrioritization(BaseModel):
    """What Lead Prioritizer produces. JUDGMENT, not fact — never touches
    identity/acquisition fields. `photo_rating=0` is valid (reviewed, nothing
    usable found) and distinct from `None` (not yet reviewed)."""

    place_id: str
    photo_rating: int = Field(..., ge=0, le=5)
    lead_score: int = Field(..., ge=0, le=100)
    photo_count: int = Field(..., ge=0)
    photo_links: list[str] = Field(default_factory=list)
    photo_sources: list[str] = Field(default_factory=list)
    rating_reason: str | None = None
    prioritized_date: date


class LeadWebsiteIntelligence(BaseModel):
    """What Website Intelligence produces. BUILD/SALES JUDGMENT only — it
    turns already-prioritized evidence into a concise brief without changing
    acquisition facts or lifecycle status."""

    place_id: str
    site_brief: str
    selling_angle: str
    suggested_pages: list[str] = Field(default_factory=list)
    content_notes: str | None = None
    visual_notes: str | None = None
    intelligence_sources: list[str] = Field(default_factory=list)
    intelligence_date: date


class Lead(BaseModel):
    """Canonical stored record — the only shape that lives in data/<profile>/leads.jsonl."""

    # Identity + acquisition facts (Lead Finder territory; immutable after insert
    # except via an explicit refresh of the SAME facts)
    place_id: str
    name: str
    industry: str
    location: str
    has_website: bool
    found_date: date
    source: str = "google_places"
    google_maps_url: str | None = None
    yelp_url: str | None = None
    phone_present: bool | None = None
    recent_review_count: int | None = Field(default=None, ge=0)
    hours_present: bool | None = None
    staleness_flags: list[str] = Field(default_factory=list)

    # Lifecycle — monotonic, never regresses (see LeadStatus.rank + store.set_status)
    status: LeadStatus = LeadStatus.FOUND

    # Prioritizer judgment (None = not yet reviewed; 0 = reviewed, nothing usable)
    photo_rating: int | None = Field(default=None, ge=0, le=5)
    lead_score: int | None = Field(default=None, ge=0, le=100)
    photo_count: int | None = Field(default=None, ge=0)
    photo_links: list[str] = Field(default_factory=list)
    photo_sources: list[str] = Field(default_factory=list)
    rating_reason: str | None = None
    prioritized_date: date | None = None

    # Website Intelligence judgment (None/empty = not yet reviewed)
    site_brief: str | None = None
    selling_angle: str | None = None
    suggested_pages: list[str] = Field(default_factory=list)
    content_notes: str | None = None
    visual_notes: str | None = None
    intelligence_sources: list[str] = Field(default_factory=list)
    intelligence_date: date | None = None

    @classmethod
    def from_create(cls, data: LeadCreate) -> "Lead":
        return cls(**data.model_dump(), status=LeadStatus.FOUND)

    def with_prioritization(self, p: LeadPrioritization) -> "Lead":
        """Apply Prioritizer judgment via an explicit allowlist — never touches facts."""
        if p.place_id != self.place_id:
            raise ValueError(f"place_id mismatch: lead={self.place_id} update={p.place_id}")
        return self.model_copy(
            update={
                "photo_rating": p.photo_rating,
                "lead_score": p.lead_score,
                "photo_count": p.photo_count,
                "photo_links": p.photo_links,
                "photo_sources": p.photo_sources,
                "rating_reason": p.rating_reason,
                "prioritized_date": p.prioritized_date,
                "status": self._advance_status(LeadStatus.PRIORITIZED),
            }
        )

    def with_website_intelligence(self, i: LeadWebsiteIntelligence) -> "Lead":
        """Apply Website Intelligence judgment via an explicit allowlist."""
        if i.place_id != self.place_id:
            raise ValueError(f"place_id mismatch: lead={self.place_id} update={i.place_id}")
        return self.model_copy(
            update={
                "site_brief": i.site_brief,
                "selling_angle": i.selling_angle,
                "suggested_pages": i.suggested_pages,
                "content_notes": i.content_notes,
                "visual_notes": i.visual_notes,
                "intelligence_sources": i.intelligence_sources,
                "intelligence_date": i.intelligence_date,
            }
        )

    def _advance_status(self, target: LeadStatus) -> LeadStatus:
        """Status is monotonic — never moves backwards (Codex finding #1)."""
        return target if target.rank > self.status.rank else self.status
