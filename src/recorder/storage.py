"""storage.py — idempotent structured storage for the recorder layer.

Part of the agent-chronicle method.

Guarantees:
  - event dedup by a stable key (default: timestamp + role + first 40 chars
    of content), so re-running a capture never duplicates events;
  - append-only JSONL output;
  - zero interpretation of content (record, don't process).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional, Set

DEFAULT_DEDUP_KEY_FIELDS = ("timestamp", "role")


def event_key(event: Dict[str, Any], fields: tuple = DEFAULT_DEDUP_KEY_FIELDS) -> str:
    """Build a stable dedup key from an event."""
    parts = []
    for f in fields:
        parts.append(str(event.get(f, "")))
    content = str(event.get("content", ""))
    parts.append(content[:40])
    return "|".join(parts)


def load_seen_keys(path: str) -> Set[str]:
    """Load existing event keys from a JSONL file (for idempotent append)."""
    seen: Set[str] = set()
    if not os.path.exists(path):
        return seen
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            seen.add(event_key(ev))
    return seen


def append_unique_events(
    events: Iterable[Dict[str, Any]],
    path: str,
    *,
    seen: Optional[Set[str]] = None,
) -> int:
    """Append events to JSONL, skipping any whose key is already present.

    `seen` may be pre-loaded with load_seen_keys() to make a whole run
    idempotent across processes. Returns the number of new events written.
    """
    if seen is None:
        seen = load_seen_keys(path)
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    written = 0
    with open(path, "a", encoding="utf-8") as f:
        for ev in events:
            key = event_key(ev)
            if key in seen:
                continue
            seen.add(key)
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
            written += 1
    return written


def read_events(path: str) -> List[Dict[str, Any]]:
    """Read all events from a JSONL file into a list."""
    out: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out
