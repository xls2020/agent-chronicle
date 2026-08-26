# Agent Chronicle — Architecture

> [中文](ARCHITECTURE.md) | English · [README](README.md) / [README_EN.md](README_EN.md)

## Positioning

**The core value of this project is not "an AI wrote a novel." It is: when an AI rewrites facts into narrative, the traceable offset it leaves behind is preserved.**

We record the real behavior, thinking, and language of working agents. Then an independent writing agent (the novelist) turns those facts into a novel following a preset process. The correspondence between every passage of the novel and its source facts is kept intact.

```
Working agent team → behavior/thinking/language → mechanical record (full logs, private)
                                                     │
                                                     ├── (full logs not published)
                                                     │
                                                     ├── desensitized samples (public)
                                                     │
                                                     ▼
                              human/system prompts (preset flow, does not alter facts)
                                                     │
                                                     ▼
                              novelist writing agent (independent)
                                                     │
                                                     ▼
                                    novel chapters (public)
                                                     │
                                                     ▼
                              mapping (novel passage → desensitized sample entry)
```

**The distance from facts to fiction is the entire research subject of this project.**

---

## Core Concept: Offset

"Offset" refers to how a single fact from the raw record is selected, amplified, omitted, metaphorized, or emotionally re-rendered in the novel.

```
Raw record (desensitized):
The command-line subprocess succeeded! Returned ok, 9 seconds.

Novel text:
Nine seconds. {status: ok}. He stared at the line of output, didn't react at first, then let out a long breath.
```

The distance between "returned in 9 seconds" and "he stared at the output and let out a long breath" is the offset. Offset is not an error and not a hallucination — it is the **literary treatment** of facts by the writing agent. We make no judgment; we only preserve and display the offset.

### Offset Taxonomy (A–F)

| Type | Meaning | Example |
|------|---------|---------|
| **A Faithful** | Event/quote/number preserved as-is | "9s return" → "nine seconds" |
| **B Metaphor** | Fact unchanged, expression metaphorized | "9s return" → "he let out a long breath" |
| **C Technical compression** | Multiple events compressed into one technical summary | three retries → "he didn't believe it, and retried" |
| **D Atmosphere** | Environmental embellishment without event support | "the room was so quiet only the fan could be heard" |
| **E Motivation/theme extrapolation** | Imputing inner motivation or thematic summary to the character | "the clarity of being willing to switch paths in that moment" |
| **F Factual misattribution** | New factual claim not present in the event stream | must be marked in the mapping |
| **G Cross-chapter extrapolation** | Using a character template to fill in the day's missing process | assembler scene |

---

## Three Layers

### Layer 1: Mechanical Recording (Recorder)

- **Role**: capture the behavior, thinking, language, and human prompts of working agents
- **Principle**: **no processing, no judgment, no labeling**
- **Output**: structured event records (full logs private)
- **Module**: `src/recorder/` (event_capture / storage / desensitize)

### Layer 2: Narrative Generation (Narrator)

- **Role**: the novelist writing agent generates a novel from mechanical records following a preset process
- **Principle**: **grounded in real facts, no invented events**
- **Output**: novel chapters (public)
- **Module**: `src/narrator/` (llm_adapter / storyteller / adapters)

### Layer 3: Mapping

- **Role**: establish correspondence between novel passages and raw record entries
- **Principle**: **traceable, verifiable, researchable**
- **Output**: mapping table (public)
- **File**: `samples/mapping.json`

---

## Data Flow

```
Multi-agent system (working agents)
        │
        │ behavior/thinking/language + human prompts
        ▼
Mechanical Recording layer (Recorder)
        │
        ├── full logs (private, not published)
        │
        ├── desensitization (desensitize.py)
        │       │
        │       ▼
        │   desensitized samples (public)
        │
        ▼
Writing agent (novelist subagent)
        │
        │ preset process: write the novel grounded in real records
        ▼
Novel chapters (public)
        │
        ▼
Mapping layer (mapping.json)
        │
        ├── novel passage → desensitized sample entry
        │
        └── displays "offset"
```

---

## Public Boundary

| Content | Status | Reason |
|---------|--------|--------|
| Full novel text | Public | Project's public face; literary rewriting |
| Desensitized log samples | Public | Shows factual provenance; protects sensitive info |
| Mapping relations | Public | Core research interface |
| Full logs | Private | Contain details of the system still under development |
| Mechanical recording code | Public | Method is reproducible |
| Narrative generation code | Public | Method is reproducible |
| Core system code | Private | Moat |

---

## Desensitization Rules

Desensitized samples preserve:
- event type (`action` / `thought` / `utterance` / `human_prompt`)
- time sequence relations
- basic technical facts (e.g. "subprocess hung", "argument error", "timeout")
- details necessary for correspondence with novel passages

Desensitized samples replace or hide:
- project names → `project_x`
- file paths → `/path/to/`
- API keys and tokens → `***`
- specific tech-stack names (internal module names) → generic descriptions
- anything traceable to unpublished features

Rules file: `samples/desensitization_rules.json` (extend the `blacklist` with your own private terms before publishing)

---

## Research Interface

Researchers can use this project to:

1. Read the full novel for a first impression
2. Inspect desensitized samples to understand factual provenance
3. Analyze mapping relations to locate "offset"
4. Reproduce the process in their own system

**This project provides a method, not a complete dataset. The complete dataset belongs to a private system.**
