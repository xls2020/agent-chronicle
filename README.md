# Agent Chronicle

**我们记录工作智能体的真实事实，然后让一个独立的写作智能体基于这些事实写小说。每一段小说都能对应回原始事实。我们保留了这个对应关系。**

[English](README_EN.md) | 中文

> **语言政策**: 开源仓库全英文为主 (代码/注释/commit/docs)。README + 公开小说章节做双语。
> 详见 [`MAINTENANCE/BILINGUAL_POLICY.md`](MAINTENANCE/BILINGUAL_POLICY.md)。

---

## 我们真正的问题

一个多智能体系统在真实工作时，会机械地记录每个智能体的行为、思考、语言和人类的提示词。然后，一个独立的写作智能体把这些记录改写成了叙事。

于是这些问题变得不可回避：

- AI 在叙事中夸大了哪些事件，省略了哪些？
- 一个 `timeout` 是怎么变成"像一条鱼咬着钩"的？
- 这种"从事实到叙事"的偏移，在不同模型、不同时间之间是否稳定？
- 当系统开始记录自己时，我们如何面对那些记录？

**这个项目不回答这些问题。它只做一件事：让这些问题变得可见。**

---

## 这是什么

Agent Chronicle 是一个**可追溯的 AI 文学改写系统**，三层结构：

1. **机械记录** — 原样捕获工作智能体的行为、思考、语言与人类提示词。不加工、不判断、不贴标签。
2. **AI 文学改写** — 一个独立的写作智能体基于机械记录，按照预设流程生成小说。
3. **可追溯对照** — 每一段小说都通过 mapping 指回对应的原始记录条目，使"偏移"可被观察、可被研究。

**从事实到小说的距离，就是这个项目的研究内容。**

---

## 什么是"偏移"

```
原始记录（脱敏后）：
命令行子进程成功了！返回 ok，9秒。

小说文本：
九秒。{status: ok}。他盯着这行输出，先是没反应过来，然后长舒一口气。
```

从"9秒返回"到"他盯着输出长舒一口气"——这段距离就是**偏移**。
偏移不是幻觉，不是错误，是写作智能体对事实的**文学化处理**。我们不做判断，只保存并展示它。

---

## 起源

2026 年 7 月 11 日，一个开发智能体在真实任务中自动生成了以下叙事：

> **"九秒，纸人长出了骨头。"**

全文见 [`chronicles/20260711_paper_bones.md`](chronicles/20260711_paper_bones.md) · [English](chronicles/20260711_paper_bones_EN.md)

---

## 公开边界

出于保护正在开发中的系统的原因，**完整机械日志不公开**。这里只提供脱敏后的样本，
用于展示从事实记录到小说叙事的对应关系。样本经过处理，隐藏了项目名、路径和敏感细节。

- [脱敏事件样本](samples/desensitized_events.jsonl)
- [对照关系](samples/mapping.json)
- [脱敏规则](samples/desensitization_rules.json)

---

## 快速开始

```bash
git clone <your-repo-url>
cd agent-chronicle
pip install -r requirements.txt
python app.py
```

打开 `http://localhost:8000`。

**接入任意 LLM**：叙事生成层通过适配器模式支持多家 LLM（OpenAI / Anthropic / DeepSeek / Ollama / CLI）。
在 WebUI 配置页填入 API 地址即可。

---

## 目录结构

```
agent-chronicle/
├── README.md / README_EN.md   # 中英文门面
├── ARCHITECTURE.md / _EN.md   # 架构文档（中/英）
├── ROADMAP.md / ROADMAP_EN.md # 路线图（中/英）
├── QUESTIONS.md / _EN.md      # 开放问题（中/英）
├── LICENSE                    # MIT
├── app.py                     # WebUI 入口
├── src/
│   ├── recorder/              # 第一层：机械记录 + 脱敏
│   ├── narrator/              # 第二层：AI 文学改写（LLM 适配器）
│   └── webui/                 # 极简前端
├── chronicles/                # 小说全文
├── samples/                   # 脱敏样本 + 对照
├── docs/                      # 数据格式 / 脱敏规则 / 数据来源
└── tests/                     # 测试（含防泄漏门禁）
```

---

## 声明

本仓库中的小说由 AI 系统自主生成，未经人类编辑。完整机械日志不公开。
公开样本经过脱敏处理。

**我们不做结论。我们只保存距离。**
