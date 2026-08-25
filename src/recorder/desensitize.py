"""desensitize.py — field + structural desensitization for public samples.

Part of the agent-chronicle method.

This is METHOD code: it is generic and project-agnostic. The sensitive-term
blacklist is loaded from an external JSON file (`desensitization_rules.json`)
so this source file itself never names any specific project, product, or path.

Rules (kept in sync with docs/desensitization_rules.md):
  - identifiers       -> project_x / agent_N / subagent_N / reviewer_N
  - absolute paths    -> /path/to/
  - secrets/credentials -> ***
  - specific model names -> [llm]
  - theorem/proof terms -> [formal-system]
  - P-coded lesson ids  -> [lesson-N]
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Iterable, List, Optional

# --- default rules path (overridable via env AGENT_CHRONICLE_RULES) ----------
DEFAULT_RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..",
    "samples",
    "desensitization_rules.json",
)


def _load_rules(path: Optional[str] = None) -> Dict[str, Any]:
    """Load the desensitization rules (regex blacklist etc.).

    The shipped default file contains a generic blacklist. Operators may extend
    it with project-specific terms WITHOUT modifying this source file.
    """
    if path is None:
        path = os.environ.get("AGENT_CHRONICLE_RULES", DEFAULT_RULES_PATH)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def _compile_patterns(rules: Dict[str, Any]):
    """Build compiled regexes from the rules dict. Returns (replacements, blacklist)."""
    replacements: List[tuple] = []
    for group in rules.get("replacements", []):
        pat = group.get("pattern")
        rep = group.get("to", "")
        if pat:
            try:
                replacements.append((re.compile(pat), rep))
            except re.error:
                continue
    blacklist = rules.get("blacklist", [])
    compiled_blacklist: List[re.Pattern] = []
    for raw in blacklist:
        try:
            compiled_blacklist.append(re.compile(raw))
        except re.error:
            continue
    return replacements, compiled_blacklist


# --- default generic replacements (no project-specific terms) ----------------
_DEFAULT_REPLACEMENTS = [
    (re.compile(r"(?i)\b(?:token|api[_-]?key|secret|password|authorization|bearer)\b[=:\s]+[^\s,;]+"), "***"),
    (re.compile(r"(?i)\b(deepseek[a-z0-9_.-]*|claude[a-z0-9_.-]*|gpt[a-z0-9_.-]*|gemini[a-z0-9_.-]*)\b"), "[llm]"),
    (re.compile(r"\bP[0-9]{2,4}\b"), "[lesson-N]"),
    (re.compile(r"(?i)\b(?:cospherical|ptolemy|euclid|mathlib|olean|lean|theorem|lemma)\b"), "[formal-system]"),
    (re.compile(r"\breviewer_[0-9]\b"), "reviewer_N"),
    (re.compile(r"\bagent_[a-z0-9_]+\b"), "agent_N"),
    (re.compile(r"\bsubagent[_a-z0-9]*\b"), "subagent_N"),
    (re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:)?[/\\][A-Za-z0-9_./\\-]+"), "/path/to/"),
]

# Generic fallback blacklist (used when the rules file ships an empty blacklist).
# IMPORTANT: these are SHAPE-based (credential-shaped) patterns, NOT bare-word
# matches. A commit title like "remove hardcoded token" is a technical phrase,
# not a leak; but a credential assignment (e.g. `secret=abc123`) IS a leak.
_DEFAULT_BLACKLIST = [
    re.compile(r"(?i)\b(?:token|api[_-]?key|secret|password|authorization|bearer)\b\s*[=:]\s*[^\s,;]+"),
    re.compile(r"(?i)\b(?:sk|ghp|gho|ghu|ak|Bearer)[-_][A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bP[0-9]{2,4}\b"),
    re.compile(r"(?i)\blesson-?[0-9]+\b"),
    re.compile(r"(?i)\b(?:deepseek|claude|gpt|gemini)[a-z0-9_.-]*\b"),
]


def _apply(text: str, replacements: List[tuple]) -> str:
    t = text
    for pat, rep in replacements:
        t = pat.sub(rep, t)
    return t


def _desensitize_text(text: str, replacements: List[tuple]) -> str:
    return _apply(text, replacements)


def desensitize_event(event: Dict[str, Any], rules_path: Optional[str] = None) -> Dict[str, Any]:
    """Return a copy of `event` with every string field desensitized."""
    rules = _load_rules(rules_path)
    replacements, _blacklist = _compile_patterns(rules)
    replacements = replacements or _DEFAULT_REPLACEMENTS

    out: Dict[str, Any] = {}
    for key, value in event.items():
        if value is None or isinstance(value, (int, float, bool)):
            out[key] = value
            continue
        if not isinstance(value, str):
            out[key] = value
            continue
        out[key] = _desensitize_text(value, replacements)
    return out


# --- structural desensitization (topology fingerprint removal) ----------------
_PUBLIC_FIELDS = ("event_type", "timestamp", "agent", "emotion", "content")

_ROLE_MAP = {
    "human": "human",
    "history": "system",
    "git": "system",
    "codex": "agent",
    "subagent": "subagent",
    "planner": "subagent",
    "constructor": "subagent",
    "repair": "subagent",
    "assembler": "subagent",
    "watchdog": "subagent",
    "unknown": "system",
    "deepseek": "agent",
}


def desensitize_event_for_public(
    event: Dict[str, Any],
    rules_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Transform a raw internal event into its public shape.

    Structural rules:
      - source_file / session_id / thinking_arc are dropped (origin fingerprint)
      - role is mapped to a generic class
      - content is the field-level-desensitized title/output
    """
    rules = _load_rules(rules_path)
    replacements, _blacklist = _compile_patterns(rules)
    replacements = replacements or _DEFAULT_REPLACEMENTS

    role_raw = str(event.get("role", "unknown"))
    role_class = _ROLE_MAP.get(role_raw, "system")

    content = _desensitize_text(
        str(event.get("output", "")) if event.get("output") else str(event.get("title", "")),
        replacements,
    )

    public = {
        "event_type": str(event.get("event_type", "thought")),
        "timestamp": str(event.get("ts", event.get("timestamp", ""))),
        "agent": role_class,
        "emotion": str(event.get("emotion", "neutral")),
        "content": content,
    }
    return {k: public[k] for k in _PUBLIC_FIELDS if k in public}


# --- sample-level leak gate ---------------------------------------------------
def assert_sample_clean(public_events: Iterable[Dict[str, Any]], rules_path: Optional[str] = None) -> bool:
    """Raise if any public sample leaks a blacklisted fingerprint.

    The blacklist comes from desensitization_rules.json, falling back to a
    generic built-in blacklist when the file ships an empty list.
    """
    rules = _load_rules(rules_path)
    _replacements, blacklist = _compile_patterns(rules)
    if not blacklist:
        blacklist = _DEFAULT_BLACKLIST

    hits = []
    for ev in public_events:
        for k, v in ev.items():
            s = str(v)
            for pat in blacklist:
                if pat.search(s):
                    hits.append((k, pat.pattern, s[:80]))
    if hits:
        raise AssertionError("SAMPLE LEAK: %r" % hits[:5])
    return True
