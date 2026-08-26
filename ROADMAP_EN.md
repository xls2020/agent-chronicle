# Roadmap

> [中文](ROADMAP.md) | English · [README](README.md) / [README_EN.md](README_EN.md)

## Current State (v0.1)

- ✅ Mechanical Recording layer (Recorder): capture + structured storage + desensitization
- ✅ Narrative Generation layer (Narrator): LLM adapter + writing pipeline
- ✅ Mapping layer: novel passage ↔ desensitized events + A–F offset taxonomy
- ✅ First public sample: "Nine Seconds, the Paper Man Grew Bones" + 11 desensitized events

## Next Steps

### 0. WebUI markdown rendering for novel body text (improvement, backlog)

The current WebUI novel tab displays the markdown source as **escaped plain text with `<br>` line breaks** (faithful to the source file; zero dependencies, works offline).
Markdown symbols such as `#` and backticks are shown literally. This is an intentional design choice.

Planned improvement: provide an **optional** markdown render mode (e.g. introduce marked.js so `##` renders as a real heading and code blocks render in monospace),
as a "plain text / rendered" toggle the user can freely choose. Introducing an external library requires evaluating offline availability and dependencies.

> Source: 2026-08-26 user feedback from testing (the `#` renders as plain text — current behavior is intentional, improvement moved to backlog).
> Status: **Not implemented**, deferred to a future version.

### 1. Shadow state channel (experimental)

The current version uses a **post-hoc rewriting** architecture: record the working agent's facts, then have an independent writing agent rewrite them into narrative.

We plan to add an experimental feature in a later version: allow the working agent to record a minimal state description of itself through a private field while executing tasks. This field does not participate in task evaluation, does not enter the workflow, and is archived only as research material. The prompt version will be published together with the data so that the elicitation conditions remain auditable.

> The goal of this feature is to answer a more fundamental question: when a working agent is allowed to "write nothing",
> will it spontaneously produce expressions about its own state? If it does, what does it write?
> We leave this question to the next version.

**Details will be published in a later version.**

### 2. Continuous observation archive

- Collect mechanical events daily → generate a new chapter daily → build a timeline
- Turn the project from "an interesting repository" into "a long-term observation archive"

### 3. More data samples

- Expand the public sample scope gradually, depending on how the system develops
- If the project becomes a core product, we may open an "observation window" for other developers to connect their own multi-agent systems
