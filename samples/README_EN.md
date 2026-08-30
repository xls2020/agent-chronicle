# Samples — Desensitized Events + Mapping

> [中文](README.md) | English · [README](../README.md) / [README_EN.md](../README_EN.md) · [Chronicles](../chronicles/README_EN.md)

This directory demonstrates the mapping from "mechanical record to novel narrative" — the project's **core research interface**.

## Files

- **`desensitized_events.jsonl`** — 11 desensitized mechanical events (each matching a plot point of the novel "Nine Seconds")
- **`desensitization_rules.json`** — desensitization rules (extensible; fill in your own private term list before publishing)
- **`../mapping/mapping.json`** — the mapping of novel passages ↔ desensitized events + offset classification

## How to Read

1. First read the novel "Nine Seconds, the Paper Man Grew Bones" (`../chronicles/20260711_paper_bones.md`)
2. Then look at `desensitized_events.jsonl` (these are the desensitized samples of the mechanical records)
3. Finally look at `../mapping/mapping.json` (each novel passage → which events → what kind of offset occurred)

## What Is "Offset"

**Raw record** (desensitized):
```
Command-line subprocess succeeded! Returned ok, 9 seconds.
```

**Novel**:
```
Nine seconds. {status: ok}. He stared at this line of output, didn't react at first, then let out a long breath.
```

The distance from "returned in 9 seconds" to "he stared at the output and let out a long breath" — that distance is the offset. Offset is not an error; it is the narrator's literary treatment of the facts. We make no judgment; we only preserve and display it.

## Desensitization Statement

The raw mechanical records belong to the private system and are not published. Only desensitized samples are provided here, to demonstrate the **fact → narrative** conversion method.
The samples have been processed to hide project names, paths, credentials, and specific tech-stack details. The `blacklist` in `desensitization_rules.json` should be extended with your own private terms before publishing.
