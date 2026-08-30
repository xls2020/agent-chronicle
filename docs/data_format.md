# 数据格式说明

> [English](data_format_EN.md) | 中文 · [README](../README.md) / [README_EN.md](../README_EN.md) · [数据来源](data_source.md)

本仓库公开的机械记录使用 JSONL（每行一个 JSON 对象）。

## 脱敏事件格式（`samples/desensitized_events.jsonl`）

| 字段 | 类型 | 说明 |
|------|------|------|
| `seq` | int | 相对序号（用于对照可追溯） |
| `event_type` | string | `action` / `thought` / `utterance` / `human_prompt` |
| `timestamp` | string | 事件时间 |
| `agent` | string | 智能体角色（human / agent / subagent / system） |
| `emotion` | string | 情感标签（breakthrough / frustration / insight / neutral ...） |
| `content` | string | 脱敏后的事件内容 |

### 示例

```json
{"seq": 7, "event_type": "action", "timestamp": "2026-07-11T11:58:00", "agent": "agent", "emotion": "breakthrough", "content": "命令行子进程成功了！返回 ok，9秒。关键：改用标准输入管道代替 -p 参数。"}
```

## 对照格式（`mapping/mapping.json`）

| 字段 | 说明 |
|------|------|
| `narrative_paragraph` | 小说中的段落（引用原文） |
| `source_event_ids` | 对应脱敏事件（如 `seq1`） |
| `offset_description` | 偏移说明 |
| `offset_types` | 偏移分类（A–F） |

## 内部完整格式（不公开）

完整机械记录包含更多字段（原始会话 ID、思考轨迹、来源文件等），属于私有系统，不公开。
公开样本经过脱敏处理，隐藏了这些字段与具体项目信息。
