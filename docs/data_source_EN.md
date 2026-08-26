# Data Source and Public Boundary

> [中文](data_source.md) | English · [README](../README.md) / [README_EN.md](../README_EN.md) · [Data Format](data_format_EN.md)

## Data Source

All narrative text in this project originates from the mechanical records of a **genuinely running** multi-agent system during task execution.

- **Mechanical records**: Python scripts capture the working agents' behavior, thinking, language, and human prompts as-is.
  The capture process applies **no processing, no judgment, no labeling**.
- **Narrative generation**: an independent writing agent (the novelist subagent) generates the novel from the mechanical records following a preset pipeline.
- **Mapping**: each passage of the novel points back to its corresponding desensitized events.

"Nine Seconds, the Paper Man Grew Bones" is the first public sample, recorded on 2026-07-11.

## Why Full Logs Are Not Public

The complete mechanical logs contain details of a system still under development: project structure, tech stack, development strategy, current progress.
Publishing this information before the system has built a moat would harm its competitiveness.

**Therefore: the full logs belong to the private system and are not published.** Only desensitized samples are provided here, to demonstrate the conversion method from "factual record to narrative". The samples have been processed to hide project names, paths, and sensitive details.

## The Value of This Method

You cannot verify everything, but you can verify the mechanism:

- The samples show how logs are converted into a novel
- The mechanism is public; the code is public
- If you wish, you can reproduce this process in your own system

**This project does not provide "a complete dataset" but "a reproducible method".**
The complete data needs protection, but the method can be public. The method itself is the value.

## Honesty Statement

> I only publish samples, because the real logs involve an unfinished system.

This is not an excuse; it is a statement: this project is real, active, and under development — not a demo built for the sake of open-sourcing.
