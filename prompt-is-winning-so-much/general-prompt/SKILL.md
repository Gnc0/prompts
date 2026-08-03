---
name: general-prompt
description: 通用提示词生成技能路由（七层图式闭合方法论）。将领域提示词需求映射为可执行的多层闭合约束系统。包含基础版、简易版(gpt-5.5 优化)等版本，按目标模型与交互风格选择。
---

# General Prompt（通用提示词生成路由）

本目录收录「七层图式闭合提示词生成」的不同版本（frontmatter name 均为 `schema-closure-prompt-generator`），按目标模型与交互风格选择：

| 版本 | 文件 | 适用场景 |
|------|------|----------|
| 基础版 | general-prompt-base.md | 多轮逐步探询（每个子阶段一轮），全角中文标点，默认通用选择 |
| 简易版 | general-prompt-easy.md | 面向 gpt-5.5 优化：Phase 1 单批 5 个短问题，容忍稀疏回答（标记【未知】） |
| 判官版 | general-prompt-judge.md | 与基础版内容基本一致，主要差异为标点编码改为半角（ASCII） |

## 选择逻辑

- 目标模型为 gpt-5.5 / 希望首轮快速收集信息 → `general-prompt-easy`
- 默认多轮深度探询 → `general-prompt-base`
- 需要半角标点编码（便于下游程序解析） → `general-prompt-judge`
