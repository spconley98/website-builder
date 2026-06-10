"""Loads .env (secrets) and profile-owned hunt lists into one place.

Each collaborator runs this against their own .env — see .env.example for the
required keys. Nothing here should ever read a value that isn't local-only.

Validation note (post three-brain/Codex review): config/targets.<profile>.yaml
is Matt-friendly config that humans hand-edit — bad YAML should fail with a
clear, located message, not a raw constructor TypeError. Pydantic gives us that
for free.
"""
from __future__ import annotations

import os
import socket
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _force_ipv4_dns() -> None:
    """Workaround for a real-world finding: on Sean's network, DNS returns an
    IPv6 address for googleapis.com but the IPv6 route is broken/slow — every
    HTTPS connection (Places, Firecrawl, ...) hung ~40s before connecting.
    Forcing IPv4-only resolution brought that to ~0.05s (measured fix).

    This is a common Windows/ISP issue, not specific to our code — patching
    socket.getaddrinfo globally, once, here (config is the first thing every
    module imports) is the simplest fix that doesn't touch every httpx client.
    Safe no-op on networks where IPv6 works fine.
    """
    if getattr(socket, "_leadpipe_ipv4_patched", False):
        return
    _original_getaddrinfo = socket.getaddrinfo

    def _ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
        return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    socket.getaddrinfo = _ipv4_only
    socket._leadpipe_ipv4_patched = True


_force_ipv4_dns()


class TargetsConfigError(ValueError):
    """Raised when config/targets.<profile>.yaml is malformed — message is meant to be
    read directly by a human (Matt) editing the file."""


class Target(BaseModel):
    area: str
    radius: str
    industries: list[str]


class TargetsFile(BaseModel):
    targets: list[Target] = []


class Settings(BaseModel):
    google_places_api_key: str | None
    firecrawl_api_key: str | None
    firecrawl_pause_credits_pct: float
    llm_model: str
    llm_base_url: str
    targets: list[Target]


def _env_str(name: str, default: str | None = None) -> str | None:
    """Read env vars human-edited in .env, treating blank values as unset."""
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value or default


def _load_targets(path: Path) -> list[Target]:
    if not path.exists():
        return []
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise TargetsConfigError(f"{path}: invalid YAML — {e}") from e
    try:
        return TargetsFile.model_validate(raw).targets
    except ValidationError as e:
        # Pydantic's error already includes the field path (e.g. targets.0.industries);
        # surface it with the file path so Matt knows exactly where to look.
        raise TargetsConfigError(f"{path}: {e}") from e


def targets_path_for_profile(profile: str | None) -> Path:
    """Profile-specific batch target list; examples live in targets.example.yaml."""
    suffix = (profile or "").strip().lower()
    candidate = ROOT / "config" / f"targets.{suffix}.yaml" if suffix else ROOT / "config" / "targets.sean.yaml"
    return candidate if candidate.exists() else ROOT / "config" / "targets.example.yaml"


def load_settings(targets_path: Path | None = None) -> Settings:
    """Single entry point every module/agent uses to read config."""
    targets_path = targets_path or ROOT / "config" / "targets.sean.yaml"
    return Settings(
        google_places_api_key=_env_str("GOOGLE_PLACES_API_KEY"),
        firecrawl_api_key=_env_str("FIRECRAWL_API_KEY"),
        firecrawl_pause_credits_pct=float(_env_str("FIRECRAWL_PAUSE_CREDITS_PCT", "5.0") or "5.0"),
        llm_model=_env_str("LLM_MODEL", "gemma4-fast") or "gemma4-fast",
        llm_base_url=_env_str("LLM_BASE_URL", "http://localhost:11434/v1") or "http://localhost:11434/v1",
        targets=_load_targets(targets_path),
    )
