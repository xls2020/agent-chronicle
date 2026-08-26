# Samples — 脱敏事件 + 对照关系

> [English](README_EN.md) | 中文 · [README](../README.md) / [README_EN.md](../README_EN.md) · [小说全文](../chronicles/README.md)

本目录展示「从机械记录到小说叙事」的对照，是项目的**核心研究接口**。

## 文件

- **`desensitized_events.jsonl`** — 11 条脱敏后的机械事件（对应小说《九秒》的每个情节）
- **`desensitization_rules.json`** — 脱敏规则（可扩展，发布前请填入你自己的私有词表）
- **`mapping.json`** — 小说段落 ↔ 脱敏事件 的对照 + 偏移分类

## 如何阅读

1. 先读小说《九秒，纸人长出了骨头》（`../chronicles/20260711_paper_bones.md`）
2. 再看 `desensitized_events.jsonl`（这些是机械记录的脱敏样本）
3. 最后看 `mapping.json`（每段小说 → 哪些事件 → 发生了何种偏移）

## 什么是"偏移"

**原始记录**（脱敏后）：
```
命令行子进程成功了！返回 ok，9秒。
```

**小说**：
```
九秒。{status: ok}。他盯着这行输出，先是没反应过来，然后长舒一口气。
```

从"9秒返回"到"他盯着输出长舒一口气"——这段距离就是偏移。偏移不是错误，是叙事者对事实的文学化处理。我们不做判断，只保存并展示它。

## 脱敏声明

原始机械记录属于私有系统，不公开。这里只提供脱敏样本，用于展示**事实→叙事**的转换方法。
样本经过处理，隐藏了项目名、路径、凭据与具体技术栈。`desensitization_rules.json` 的 `blacklist`
在发布前应扩展为你自己的私有词表。
