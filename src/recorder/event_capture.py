"""event_capture.py — generic recorder that turns raw agent activity into events.

Part of the agent-chronicle method.

This module is deliberately project-agnostic: it knows nothing about any
specific multi-agent system. It consumes a stream of raw activity records
(whatever shape your system emits) and normalizes them into a uniform event
stream that the rest of the pipeline can consume.

Pipeline shape (see ARCHITECTURE.md):

    raw activity -> normalize_activity() -> event -> store -> sample (public)

A "raw activity record" is any dict with at least a timestamp and some text.
This module only guarantees a stable shape; it does not interpret, tag, or
judge the content (the "record, don't process" principle).
"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Iterable, List, Optional

DEFAULT_TIMESTAMP_KEY = "ts"


def normalize_activity(
    raw: Dict[str, Any],
    *,
    timestamp_key: str = DEFAULT_TIMESTAMP_KEY,
    role_key: str = "role",
    content_keys: Iterable[str] = ("output", "title"),
) -> Dict[str, Any]:
    """Normalize one raw activity record into the uniform event shape.

    The output event always contains: timestamp, role, content.
    Extra keys from the raw record are preserved untouched (never modified).
    """
    ts = str(raw.get(timestamp_key, "")) or time.strftime("%Y-%m-%dT%H:%M:%S")
    role = str(raw.get(role_key, "unknown"))
    content = ""
    for k in content_keys:
        v = raw.get(k)
        if v:
            content = str(v)
            break

    event = {
        "timestamp": ts,
        "role": role,
        "content": content,
    }
    for k, v in raw.items():
        if k not in event:
            event[k] = v
    return event


def iter_events_from_lines(path: str, *, timestamp_key: str = DEFAULT_TIMESTAMP_KEY) -> Iterable[Dict[str, Any]]:
    """Yield normalized events from a JSONL file of raw activity records."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(raw, dict):
                continue
            yield normalize_activity(raw, timestamp_key=timestamp_key)


def events_for_date(
    path: str,
    date: str,
    *,
    timestamp_key: str = DEFAULT_TIMESTAMP_KEY,
) -> List[Dict[str, Any]]:
    """Return normalized events whose timestamp starts with `date` (YYYY-MM-DD)."""
    out = []
    for ev in iter_events_from_lines(path, timestamp_key=timestamp_key):
        if ev.get("timestamp", "").startswith(date):
            out.append(ev)
    return out


def write_events_jsonl(events: Iterable[Dict[str, Any]], out_path: str) -> int:
    """Write events as JSONL. Returns number of events written."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    n = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
            n += 1
    return n
