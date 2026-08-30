# Data Format

> [中文](data_format.md) | English · [README](../README.md) / [README_EN.md](../README_EN.md) · [Data Source](data_source_EN.md)

The mechanical records published in this repository use JSONL (one JSON object per line).

## Desensitized Event Format (`samples/desensitized_events.jsonl`)

| Field | Type | Description |
|-------|------|-------------|
| `seq` | int | Relative sequence number (for mapping traceability) |
| `event_type` | string | `action` / `thought` / `utterance` / `human_prompt` |
| `timestamp` | string | Event time |
| `agent` | string | Agent role (human / agent / subagent / system) |
| `emotion` | string | Emotion label (breakthrough / frustration / insight / neutral ...) |
| `content` | string | Desensitized event content |

### Example

```json
{"seq": 7, "event_type": "action", "timestamp": "2026-07-11T11:58:00", "agent": "agent", "emotion": "breakthrough", "content": "Command-line subprocess succeeded! Returned ok, 9 seconds. Key: use a standard input pipe instead of the -p flag."}
```

## Mapping Format (`mapping/mapping.json`)

| Field | Description |
|-------|-------------|
| `narrative_paragraph` | The paragraph in the novel (quoted verbatim) |
| `source_event_ids` | Corresponding desensitized events (e.g. `seq1`) |
| `offset_description` | Description of the offset |
| `offset_types` | Offset classification (A–F) |

## Full Internal Format (Not Public)

The complete mechanical record contains more fields (raw session ID, thinking trace, source files, etc.) and belongs to the private system; it is not published.
The public samples have been desensitized and hide these fields along with project-specific information.
