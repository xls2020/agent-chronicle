"""Generic HTTP adapters for the narrator. Public, project-agnostic.

These adapters implement the LLMAdapter contract in src/narrator/llm_adapter.py.
They call the standard chat-completions style HTTP API. Endpoints and keys are
read from environment variables / caller kwargs only — nothing is hard-coded.
"""
from __future__ import annotations

import json
import os
import urllib.request
import urllib.error

from ..llm_adapter import LLMAdapter

_TIMEOUT = 400


def _post_json(url: str, payload: dict, headers: dict, timeout_s: int) -> str:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return body


class _HttpAdapter(LLMAdapter):
    name = "http"

    env_key: str = ""
    default_url: str = ""
    model_env_key: str = ""

    def __init__(self, api_key: str = "", base_url: str = "", model: str = ""):
        self.api_key = api_key or os.environ.get(self.env_key, "")
        self.base_url = base_url or os.environ.get(self.model_env_key + "_BASE", self.default_url)
        self.model = model or os.environ.get(self.model_env_key, "")

    def check_available(self) -> bool:
        return bool(self.api_key) or bool(self.base_url)

    def generate(self, prompt: str, *, system_prompt: str = "", timeout_s: int = _TIMEOUT) -> str:
        if not self.api_key:
            raise RuntimeError(f"{self.name}: missing API key ({self.env_key})")
        url = self.base_url
        payload = {
            "model": self.model or "default",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = _post_json(url, payload, headers, timeout_s)
        try:
            obj = json.loads(body)
            return obj["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001 — surface raw for debugging
            raise RuntimeError(f"{self.name}: unexpected response: {body[:200]} ({exc})") from exc


class OpenAIAdapter(_HttpAdapter):
    name = "openai"
    env_key = "OPENAI_API_KEY"
    default_url = "https://api.openai.com/v1/chat/completions"
    model_env_key = "OPENAI"


class DeepSeekAdapter(_HttpAdapter):
    name = "deepseek"
    env_key = "DEEPSEEK_API_KEY"
    default_url = "https://api.deepseek.com/chat/completions"
    model_env_key = "DEEPSEEK"


class AnthropicAdapter(_HttpAdapter):
    name = "anthropic"
    env_key = "ANTHROPIC_API_KEY"
    default_url = "https://api.anthropic.com/v1/messages"
    model_env_key = "ANTHROPIC"

    def generate(self, prompt: str, *, system_prompt: str = "", timeout_s: int = _TIMEOUT) -> str:
        if not self.api_key:
            raise RuntimeError("anthropic: missing API key")
        payload = {
            "model": self.model or "default",
            "max_tokens": 2048,
            "system": system_prompt,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        body = _post_json(self.base_url, payload, headers, timeout_s)
        try:
            obj = json.loads(body)
            return obj["content"][0]["text"]
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"anthropic: unexpected response: {body[:200]} ({exc})") from exc


class OllamaAdapter(LLMAdapter):
    name = "ollama"

    def __init__(self, base_url: str = "", model: str = ""):
        self.base_url = base_url or os.environ.get("OLLAMA_BASE", "http://localhost:11434/api/chat")
        self.model = model or os.environ.get("OLLAMA_MODEL", "")

    def check_available(self) -> bool:
        return bool(self.model)

    def generate(self, prompt: str, *, system_prompt: str = "", timeout_s: int = _TIMEOUT) -> str:
        if not self.model:
            raise RuntimeError("ollama: missing model (set OLLAMA_MODEL)")
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        body = _post_json(self.base_url, payload, {"Content-Type": "application/json"}, timeout_s)
        try:
            obj = json.loads(body)
            return obj["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"ollama: unexpected response: {body[:200]} ({exc})") from exc


class CliAdapter(LLMAdapter):
    """Invoke a CLI harness (e.g. `claude -p`) with the prompt on stdin.

    The exact command is supplied by the caller/environment — this adapter
    never hard-codes a tool path.
    """

    name = "cli"

    def __init__(self, command: list[str] | None = None):
        import shlex

        self.command = command or []
        raw = os.environ.get("LLM_CLI_COMMAND", "")
        if raw and not self.command:
            self.command = shlex.split(raw)

    def check_available(self) -> bool:
        return bool(self.command)

    def generate(self, prompt: str, *, system_prompt: str = "", timeout_s: int = _TIMEOUT) -> str:
        import subprocess

        if not self.command:
            raise RuntimeError("cli: missing command (set LLM_CLI_COMMAND)")
        try:
            proc = subprocess.run(
                self.command,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"cli: timeout after {timeout_s}s") from exc
        if proc.returncode != 0:
            raise RuntimeError(f"cli: exit {proc.returncode}: {proc.stderr[:200]}")
        return proc.stdout
