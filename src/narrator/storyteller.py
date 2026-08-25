"""storyteller.py — turn a day of recorded events into one serial chapter.

Part of the agent-chronicle method.

The storyteller is the NARRATION layer. It:
  1. selects the day's events from the recorder output,
  2. builds a prompt that asks an independent writing agent to dramatize them
     (faithfully — no invented events, literary rewriting allowed),
  3. calls the configured LLM backend through llm_adapter,
  4. writes the chapter, returns its path.

It knows nothing about any specific project. All project-specific behavior is
injected via parameters (events, style guide, chapter number).
"""
from __future__ import annotations

import json
import os
from datetime import date
from typing import Any, Dict, List, Optional

from .llm_adapter import LLMAdapter

DEFAULT_STYLE = """\
# 连载小说文风规范 (Serialized Novel Style Guide)

> 目标: 记录任务期间智能体团队的艰难、沮丧、挫折、探索、喜悦、惊讶、顿悟。
> 要求: 有血有肉、引人入胜的连载小说（每天更新），但不能太夸张，要真实。

## 真实性铁律
1. 每个情节必须能在情感事件流里找到对应记录。novelist 是"编剧"不是"发明者"。
2. 情感强度来自真实节点，不是编造。
3. 禁止空泛情感词; 用原文痕迹。

## 情感色彩（核心）
| 情感 | 如何写 |
|------|--------|
| 艰难 | 描述重复劳动的细节 |
| 沮丧 | 第 N 次的细微变化 |
| 挫折 | 时间流逝感 |
| 探索 | 好奇心的过程 |
| 喜悦 | 释放感（长舒一口气） |
| 惊讶 | 意外感 |
| 顿悟 | 灵光一现 |

## 连载节奏
- 每天 1 章（当天的事件流）
- 每章聚焦 1-2 个核心情感节点
- 章节之间有呼应
- 标题含情感暗示

## 禁与行
禁止: 凭空编造事件 / 过度拟人 / 堆砌形容词 / 断更
提倡: 用真实节点/原始措辞 / 表现努力的过程 / 情感克制但有温度 / 跨章节呼应
"""

DEFAULT_REQUIREMENTS = """\
## CHAPTER REQUIREMENTS
1. Focus on 1-2 emotional core moments (frustration -> breakthrough, or human
   intervention -> progress).
2. Every scene must trace back to an event above.
3. Show the effort: which attempt number, what changed, the exact error message.
4. Human (the project owner) interactions are as important as agent work.
5. Emotional but restrained — no exaggeration, no invented feelings.
6. Length: 500-900 words. Chinese preferred (project language).
7. 有温度、有沉浮; 允许把 agent 拟人化，但要克制、贴合真实事件。
8. 励志基调: 每章结尾必须落在"艰难但仍在前进"的向上情绪。
Output ONLY the chapter text (markdown), no preamble.
"""


def build_prompt(
    day_events: List[Dict[str, Any]],
    *,
    chapter_number: int,
    date_str: str,
    style_guide: str = DEFAULT_STYLE,
    previous_chapter: str = "",
    requirements: str = DEFAULT_REQUIREMENTS,
) -> str:
    """Assemble the narrator prompt exactly as the storyteller will send it.

    Keeping this as a pure function makes the prompt itself auditable: the
    exact input that produced a given chapter can always be reconstructed.
    """
    event_lines = []
    for ev in day_events:
        ts = str(ev.get("timestamp", ""))[:16]
        role = str(ev.get("role", ""))
        emotion = str(ev.get("emotion", ""))
        title = str(ev.get("title", ""))[:120]
        event_lines.append(f"[{ts}] {role}/{emotion} | {title}")

    events_block = "\n".join(event_lines) if event_lines else "(no events)"
    prev_block = previous_chapter or "(no previous chapter — this is the first)"

    prompt = f"""You are the NOVELIST subagent for a multi-agent system project.

## TODAY'S DATE
{date_str}

## YOUR TASK
Write ONE chapter of the serialized novel depicting what happened on {date_str}.
This is a REAL project — the events below actually happened. Your chapter must
faithfully dramatize them. DO NOT invent events that are not in the event list.

## STYLE
{style_guide}

## PREVIOUS CHAPTERS (continuity)
{prev_block}

## TODAY'S REAL EVENTS (from the mechanical record — the truth anchor)
{events_block}

{requirements}
"""
    return prompt


def build_prompt_from_file(
    events_path: str,
    *,
    date_str: str,
    chapter_number: int,
    previous_chapter: str = "",
) -> str:
    """Build a prompt from a JSONL file of raw events (recorder output)."""
    from ..recorder.event_capture import events_for_date

    events = events_for_date(events_path, date_str)
    return build_prompt(
        events,
        chapter_number=chapter_number,
        date_str=date_str,
        previous_chapter=previous_chapter,
    )


def write_chapter(
    adapter: LLMAdapter,
    day_events: List[Dict[str, Any]],
    *,
    chapter_number: int,
    date_str: str,
    out_dir: str,
    style_guide: str = DEFAULT_STYLE,
    previous_chapter: str = "",
    system_prompt: str = "You are a careful literary writer. Base everything on the given facts.",
) -> str:
    """Run the narrator and write the chapter. Returns the written file path."""
    prompt = build_prompt(
        day_events,
        chapter_number=chapter_number,
        date_str=date_str,
        style_guide=style_guide,
        previous_chapter=previous_chapter,
    )
    text = adapter.generate(prompt, system_prompt=system_prompt)

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"chapter_{chapter_number:02d}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")

    # save the exact prompt alongside, so the mapping is reproducible
    prompt_path = os.path.join(out_dir, f"_prompt_ch{chapter_number:02d}.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    return path
