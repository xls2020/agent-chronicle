"""llm_adapter.py — unified interface for calling any LLM as the narrator.

Part of the agent-chronicle method.

The narrator (novelist) is an independent writing agent. It is invoked through
this adapter so the same narrative pipeline can talk to any backend:
OpenAI, Anthropic Claude, DeepSeek, or a local model (Ollama), or a CLI harness.

The public repository ships generic adapters. Private systems may add their own
by implementing the `generate` contract.
"""
from __future__ import annotations

import abc
from typing import Optional


class LLMAdapter(abc.ABC):
    """Contract every narrator backend must implement."""

    name: str = "base"

    @abc.abstractmethod
    def generate(self, prompt: str, *, system_prompt: str = "", timeout_s: int = 400) -> str:
        """Return the narrator's text output for `prompt`.

        Raises RuntimeError on failure. Implementations must never silently
        return empty text on error.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def check_available(self) -> bool:
        """Return True if this backend is usable in the current environment."""
        raise NotImplementedError


def build_adapter(kind: str, **kwargs) -> Optional[LLMAdapter]:
    """Factory: return an adapter by name, or None if unavailable.

    Supported kinds: 'openai', 'anthropic', 'deepseek', 'ollama', 'cli'.
    Unknown kinds return None (caller decides fallback).
    """
    if kind == "openai":
        from .adapters.http_adapters import OpenAIAdapter

        return OpenAIAdapter(**kwargs)
    if kind == "anthropic":
        from .adapters.http_adapters import AnthropicAdapter

        return AnthropicAdapter(**kwargs)
    if kind == "deepseek":
        from .adapters.http_adapters import DeepSeekAdapter

        return DeepSeekAdapter(**kwargs)
    if kind == "ollama":
        from .adapters.http_adapters import OllamaAdapter

        return OllamaAdapter(**kwargs)
    if kind == "cli":
        from .adapters.http_adapters import CliAdapter

        return CliAdapter(**kwargs)
    return None


def adapters_available() -> list[str]:
    """Return the names of backends that pass check_available() in this env."""
    out = []
    for kind in ("openai", "anthropic", "deepseek", "ollama", "cli"):
        try:
            a = build_adapter(kind)
            if a is not None and a.check_available():
                out.append(kind)
        except Exception:
            continue
    return out
