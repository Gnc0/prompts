# prompts

这里存放持续打磨的一些 prompt，主要是面向代码审计、设计规约推导，以及提示词的哲学探索。

这些文件本质上都是可复用的 prompt 模板。

tool分支为开发版本，有很多private内容，main分支是跟ssyram的原仓库同步的。会从tool推送可分享给ssyram内容到main，然后从main推送到ssyram的仓库。

## 目录说明

- `current/`: 当前维护中的版本，默认应优先使用这里的内容。以下「主要内容」全部对应 `current/` 下的同名文件（`.md` 后缀）。
- `prompt-is-winning-so-much/`: 提示词技能库——图式闭合提示词生成、哲学对话/探索、图式匹配等技能的合集，详见下方「prompt-is-winning-so-much 技能库」。
- `history/`: 经验记录与事件复盘（如 skill-routing 误判事件记录）。
- `claude-code-system-prompts/`: Claude Code 系统提示词子模块。
- ~~`old/`、`sp-ver/`、`system-designer/`、`test/`~~: 历史目录，已不在仓库中。

## 主要内容

> 以下所有 prompt 的当前维护版本均位于 `current/`。

### Hoare 系列

- `hoare-prompt`: HoarePrompt 方法本身的定义或主提示。
- `hoare-design`: 当缺少设计文档时，从实现和调用方式反推描述性规约。
- `hoare-audit`: 在已有规约前提下做持续正确性审计，把非决策问题和决策性问题分开处理。

这三个 prompt 可以连起来用：先定规约，再做审计，再迭代修正。

### 工作流系列

- `workflow`: 通用开发工作流程规范——三阶段（调研 → 架构 → 细化）+ 实现 + 修复迭代 + 文档管理。面向新功能开发与 Bug 修复的标准流程，AI 助手的行为准则与禁令。
- `workflow-audit`: 多方向、disprove-first 的 PR 审计工作流，并行 challenge 轮 + evidence-gated 结论。
- `qpdi`: QPDI 宪政式 AI 工作框架——以 /workflow 等 SDD skill 为骨架，从问题意识（Q）出发推进设计（D）→ 实现（I）全流程：意图落宪、架构起草与原则抽离、细化、实现测试、公检法审查。自包含，不依赖任何外部仓库。
- `qpdi-tribunal`: SCCO 公检法审查——对任意产物（设计文档 / 代码 / 计划 / 论证）做 challenger & prover → counter → judge 的对抗式审查，按 Sound / Complete / Concise / Optimization 四维收敛，问题分流为可直接修与须用户裁决。
- `scco-recall`: SCCO 召回扇出——审查体系的召回层。把审查对象按 SCCO 维度拆成互盲、正交、低阈值的并行 finder 镜头（强制含跨文件/消费者角度），先捞候选池、再交精度层（qpdi-tribunal / hoare-audit）裁决。只捞不判。

### 辅助 prompt

- `finegrained-check`: 适合做更细粒度的检查或补充验证。
- `evo-graph`: 用来梳理演进关系、推导路径或结构变化。
- `make-survey-plan`: 用来设计 survey / organise / plan 类型的调研与整理流程。
- `charter-craft`: 项目根本约束 / 长期承诺文档（principles.md / 项目宪法）的制定与修订方法学。
- `pr-craft`: Pull Request 描述书写规范，强制暴露跨 PR 的设计哲学、不变式契约与风险边界。
- `principle-derivation` / `principle-derivation-v2` / `principle-deriv-paper-reading`: 问题意识驱动的设计推导方法学——从问题意识出发，派生设计原则，再展开具体推导。v2 为迭代版，paper-reading 为论文阅读场景特化版。
- `code-reasoning`: 代码 Bug 的问题意识驱动推理——把 code bug 讲清楚 / 判真假 / 定可达性（调用链契约传播 + 可达性裁定）。`principle-derivation-v2` 的代码场景特化。
- `explain`: 把一件事对具体的人讲清楚——面向已经查清事实、要让一个具体的人真的听懂的场景。
- `no-flattering`: 拒绝迎合的对话者——对用户的判断、指令、意见先拷打再执行，不顺着改。
- `pi-consult`: 多模型顾问调度器——派多个模型独立分析 / 复核 / 集思广益，再以 no-flattering 姿态拷打每份回复的辩护结构后综合。
- `prompt-iter`: 用测量而不是凭感觉迭代提示词——围绕真实消费该提示词的系统建尽量小、可反复跑的评测循环（定测试对象 → 建 fixture → 建 runner → 定度量 → 装配 + 诚实迭代）。
- `auto-proof-trajectory-audit`: 面向 auto-proof-cc 运行轨迹的符合度评判与根因分析。
- `schema-matching-agent`: 具备六对图式（Schema）匹配能力的认知 Agent 系统提示。
- `skill-routing`: skill 选择经验沉淀记录——不是 skill 规约，而是用哪个 skill 的经验记录。

### prompt-is-winning-so-much 技能库

`prompt-is-winning-so-much/` 下每个子目录是一个可复用提示词技能（skill），描述一种可被反复调用的提示词工作方式。两级路由：本 README 按场景选技能目录（一级路由），进入目录后由 `SKILL.md` 做版本级路由（二级路由）。

| 技能 | 目录 | 一句话说明 |
|------|------|------------|
| abstraction-analyst | `prompt-is-winning-so-much/abstraction-analyst/` | 回应前先完成理解：定位真实需求在话题结构中的位置 |
| analytic-philosophy-prose | `prompt-is-winning-so-much/analytic-philosophy-prose/` | 以顶刊分析哲学范式写作/改写/评审哲学文本 |
| designer | `prompt-is-winning-so-much/designer/` | 游戏设计五路由（文案策划 / 系统 MDA / 系统策划案 / 数值 MDA / 数值建模）；最终定值与配置交下游数值策划流程 |
| general-prompt | `prompt-is-winning-so-much/general-prompt/` | 七层图式闭合提示词生成（基础 / 判官版） |
| philosophy-explorer | `prompt-is-winning-so-much/philosophy-explorer/` | 哲学探索：思想编辑与暂定判断生成（基础版刚性 / 规约版调节软化） |
| philosophy-interlocutor | `prompt-is-winning-so-much/philosophy-interlocutor/` | 哲学对话：结论放最后、每步推导可被击中、概念从现象自身结构长出、不擅自开辟新论域、不使用排版装饰 |
| schema-matcher | `prompt-is-winning-so-much/schema-matcher/` | 六轴图式判断：每次回复前显式输出 think_schema 块，对齐需求图式位置（含 eval/ 评测脚手架） |

经验笔记：`prompt-is-winning-so-much/EXPERIENCE-schema-matcher.md` 记录了 schema-matcher 提示词的打磨过程与可复用流程（不是提示词，不进入系统提示）。

## 使用约定

- 直接使用 prompt 时，统一从 `current/` 读取（当前维护版本）。
- 技能类 prompt（对话规范、认知姿态、哲学对话等）见 `prompt-is-winning-so-much/` 技能库。
- 选 skill 的判别经验见 `current/skill-routing.md`。

## 维护原则

- 新增或修改 prompt 时，收敛到 `current/`。
- `current/` 是当前维护版本的唯一真相源；本 README 的「主要内容」必须与 `current/` 目录保持同步。
- 技能库的增删需同步更新「prompt-is-winning-so-much 技能库」章节与 `CLAUDE.md` 技能路由表。
