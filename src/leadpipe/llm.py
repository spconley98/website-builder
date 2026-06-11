"""Thin wrapper over the local LLM — agents call generate() and stay blind to
which model runs underneath (ARCHITECTURE.md §6).

Ollama exposes an OpenAI-compatible endpoint, so we reuse the `openai` client
rather than write a bespoke HTTP layer. Model name comes from config (.env
LLM_MODEL) — swap models without touching agent code.

Sean runs `gemma4-fast` on an RTX 3090. Matt sets his own LLM_MODEL based on
his hardware — this module doesn't care which.

Hardening notes (post three-brain/Codex review): local OpenAI-compatible
endpoints aren't always perfectly compatible and can be down/loading/hung —
so every call has an explicit timeout, normalized errors via `LLMError`
(callers get an actionable message instead of a raw SDK exception or a bare
IndexError), and the client is cached rather than rebuilt per call.
"""
from __future__ import annotations

from functools import lru_cache

from openai import APIConnectionError, APIError, APITimeoutError, OpenAI

from .config import Settings, load_settings

DEFAULT_TIMEOUT = 60.0


class LLMError(RuntimeError):
    """Raised for any local-LLM failure, with enough context to actually debug it."""


@lru_cache(maxsize=1)
def _client(base_url: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key="ollama", timeout=DEFAULT_TIMEOUT)  # key ignored by Ollama


def get_client(settings: Settings | None = None) -> tuple[OpenAI, str]:
    settings = settings or load_settings()
    return _client(settings.llm_base_url), settings.llm_model


def generate(
    prompt: str,
    *,
    system: str | None = None,
    temperature: float = 0.2,
    settings: Settings | None = None,
    model: str | None = None,
    timeout: float | None = None,
) -> str:
    """Single-shot text generation — the default for classify/summarize/rate calls.

    `model`/`timeout` override the configured fast model + DEFAULT_TIMEOUT — agents
    pass these to escalate a hard case to the deep tier (config.llm_model_deep /
    llm_deep_timeout) after the fast model times out or returns garbage.

    Raises LLMError (never a raw SDK/connection exception) so agent code can
    catch one thing and decide how to degrade (skip the lead, retry, etc).
    """
    client, default_model = get_client(settings)
    model = model or default_model
    timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=timeout,
        )
    except APITimeoutError as e:
        raise LLMError(
            f"local LLM timed out after {timeout}s "
            f"(model={model!r}, base_url={client.base_url!r}). Is Ollama running and is the "
            f"model pulled? Try: `ollama run {model}`"
        ) from e
    except APIConnectionError as e:
        raise LLMError(
            f"could not reach local LLM at {client.base_url!r}. Is Ollama running? "
            f"Try: `ollama serve`"
        ) from e
    except APIError as e:
        raise LLMError(f"local LLM returned an error (model={model!r}): {e}") from e

    if not response.choices:
        raise LLMError(
            f"local LLM returned no choices (model={model!r}, base_url={client.base_url!r}) — "
            "the endpoint responded but the response shape was unexpected"
        )

    content = response.choices[0].message.content
    if content is None:
        raise LLMError(f"local LLM returned an empty message (model={model!r})")
    return content.strip()
