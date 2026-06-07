"""The master lead store — data/leads.jsonl.

One JSON record per line, keyed by place_id. Single source of truth
(ARCHITECTURE.md §9): Lead Finder CREATES, Lead Prioritizer ENRICHES the same
record — reports.py renders human views FROM this file, never the reverse.

Concurrency note (post three-brain/Codex review): "plain processes" (§7) means
no orchestrator guarantees single-writer execution, so this store IS the
coordination boundary. Every mutation takes an OS-level file lock and writes
via temp-file + atomic replace — a crash mid-write can't corrupt the store,
and two CLI invocations can't silently lose each other's writes.
"""
from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

from filelock import FileLock

from .models import Lead, LeadCreate, LeadPrioritization, LeadStatus

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_PATH = ROOT / "data" / "leads.jsonl"


class LeadStore:
    def __init__(self, path: Path | None = None):
        self.path = path or DEFAULT_STORE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = FileLock(str(self.path) + ".lock")

    # ---- low-level I/O -------------------------------------------------

    def _read_all(self) -> dict[str, Lead]:
        if not self.path.exists():
            return {}
        leads: dict[str, Lead] = {}
        for n, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                lead = Lead.model_validate_json(line)
            except Exception as e:
                raise ValueError(f"{self.path}:{n}: corrupt lead record — {e}") from e
            leads[lead.place_id] = lead
        return leads

    def _write_all(self, leads: dict[str, Lead]) -> None:
        """Write via temp file + atomic rename — no partial-write corruption."""
        body = "\n".join(lead.model_dump_json() for lead in leads.values())
        body = body + "\n" if body else ""
        fd, tmp_path = tempfile.mkstemp(dir=self.path.parent, prefix=".leads-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(body)
            os.replace(tmp_path, self.path)  # atomic on POSIX and Windows
        except BaseException:
            Path(tmp_path).unlink(missing_ok=True)
            raise

    @contextmanager
    def _locked(self):
        with self._lock:
            yield

    # ---- public read API ------------------------------------------------

    def load(self) -> dict[str, Lead]:
        with self._locked():
            return self._read_all()

    def by_status(self, status: LeadStatus) -> list[Lead]:
        return [l for l in self.load().values() if l.status == status]

    # ---- public write API — stage-scoped, allowlisted -------------------

    def create(self, data: LeadCreate) -> Lead:
        """Lead Finder entry point. Refuses leads that already have a website —
        this store is for businesses we can pitch, not ones we can't (Codex #4).
        Re-running on an existing place_id refreshes the acquisition facts only
        (a later agent's enrichment is preserved, never the other way around).
        """
        if data.has_website:
            raise ValueError(
                f"refusing to store {data.place_id} ({data.name!r}) — has_website=True; "
                "Lead Finder should filter these out before calling create()"
            )
        with self._locked():
            leads = self._read_all()
            existing = leads.get(data.place_id)
            if existing is None:
                leads[data.place_id] = Lead.from_create(data)
            else:
                # refresh ONLY the acquisition-fact fields; everything else (status,
                # prioritization) survives untouched
                fact_fields = set(LeadCreate.model_fields) - {"place_id"}
                refreshed = {k: v for k, v in data.model_dump().items() if k in fact_fields}
                leads[data.place_id] = existing.model_copy(update=refreshed)
            self._write_all(leads)
            return leads[data.place_id]

    def apply_prioritization(self, update: LeadPrioritization) -> Lead:
        """Lead Prioritizer entry point. Judgment only — cannot touch identity,
        acquisition facts, or move status backwards (Codex #1, #3)."""
        with self._locked():
            leads = self._read_all()
            existing = leads.get(update.place_id)
            if existing is None:
                raise KeyError(
                    f"no lead {update.place_id} — Prioritizer can only enrich leads "
                    "that Lead Finder already created"
                )
            leads[update.place_id] = existing.with_prioritization(update)
            self._write_all(leads)
            return leads[update.place_id]

    def set_status(self, place_id: str, status: LeadStatus) -> Lead:
        """Manual lifecycle moves (e.g. marking `contacted` / `sold`). Monotonic —
        refuses to move backwards."""
        with self._locked():
            leads = self._read_all()
            existing = leads.get(place_id)
            if existing is None:
                raise KeyError(f"no lead {place_id}")
            if status.rank < existing.status.rank:
                raise ValueError(
                    f"refusing to move {place_id} backwards: "
                    f"{existing.status.value} -> {status.value}"
                )
            leads[place_id] = existing.model_copy(update={"status": status})
            self._write_all(leads)
            return leads[place_id]
