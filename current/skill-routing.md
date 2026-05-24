# skill-routing — 用哪个 skill 的经验记录

> 不是 skill 规约，是**使用 skill 时的选择经验沉淀**。每次发现选错了 skill 就回这里加一条。
> 这个文件本身不被 `/<name>` 调用——它是给主对话里的 Claude 看的 routing 参考。

---

## principle-derivation v1 vs v2

两个 skill 同骨架（意识 → 原则 → 推导），但姿态相反。

| 场景 | 选 |
|---|---|
| 已收敛分析的**事后整理** | **v1** |
| audit 报告、code review、设计回顾、bug 复盘 | **v1** |
| 引导读者**从零产生独立洞察** | v2 |
| 教学材料、概念入门、新人 onboarding | v2 |
| 自己设计要立结构 / 提原则 | v1 |
| 单层、扁平、原则少 | v1 |
| 多层认识在不同时刻形成，要展示这一过程 | v2 |
| 主体不清楚 / 还在共同探索 | 都不用，先 trial-and-error |

### v1 vs v2 选用案例：audit 报告

**情境**：审计 ciim2022p6 trajectory，3 份独立 reviewer 产出的 audit 报告被要求"用 principle-derivation-v2 语言重写"。

**结果**：审视者**已经知道答案** → v2 的"邀请同行"姿态变成"把事后回顾包装成意识展开"——principle-derivation-v2 §四警告的"用方法替代思考"几乎踩中。具体内容（commit hash / 字段值 / 覆盖检查结论）被叙述节奏遮蔽，决策者读起来反而不知道审视者具体发现了什么。

**判据**：审计 / 复盘这种"已收敛分析的事后陈述"用 v1（直接给结构 + 推导表）。v2 用于"还在展开中" / "邀请同行"。

**记忆点**：v2.md §六已经有这张选用表，**容易在被任务 prompt 推进时忘记查表**。下次启动任何"重写 / 重表达 / 重新组织已有内容"的任务，先回 v2.md §六对一下姿态匹配。

---

## workflow / workflow-audit / hoare-audit

三个 skill 名字都带 workflow / audit，容易混。

### 一句话区别

- **workflow** — 开发**做事**的规范，不审计任何东西
- **workflow-audit** — 审视一份 **GitHub PR** 的多方向并行 review（驳回优先）
- **hoare-audit** — 审视**代码 vs 设计 spec** 的正确性（spec 必需）

### 对比

| skill | 输入 | 输出 | 是否需要 spec | 主体关系 |
|---|---|---|---|---|
| workflow | 任务描述 | 设计 + 代码 + 测试 | 否（自己产生设计文档） | 做事的人 |
| workflow-audit | GitHub PR 编号 | review 报告 | 项目 workflow.md 优先，可降级 | 外部审查（不同主体）|
| hoare-audit | 代码 + 设计 spec | findings + auto-fix | **必需**（"No audit without a spec"） | 自审 / 他审都可 |

### 选用决策

- 在写新功能 → **workflow**
- 别人提了 PR 要 review → **workflow-audit**
- 拿到一份代码，想审"是否满足设计意图" → **hoare-audit**（先确认有 spec；没有 spec → 先建 spec 或拒绝 audit）

### 联系

- workflow 立 spec → hoare-audit 验代码满足 spec
- workflow-audit 跟"做事的人"是不同主体（外部 PR review）
- hoare-audit 跟"做事的人"可以是同一主体（自审）也可以是外审

### 容易混淆点

- **workflow 含的"代码审核"段（§4.2）**不是独立 audit skill——那是开发过程内的自审，完全在 workflow 内做完，不调 audit skill
- **workflow-audit vs ultrareview**：都是 PR review，但 workflow-audit 是单 agent 做 multi-direction；ultrareview 是 multi-agent cloud parallel（user-triggered 计费）。ultrareview 不能由 Claude 自己调起
- **hoare-audit vs trajectory-audit**（如 auto-proof-trajectory-audit）：前者审代码正确性 vs spec，后者审 agent 跑动轨迹是否符合设计精神。不同对象、不同输入

### `/hoare-audit` 与 Lv0–Lv4 的关系

参见 `prompts/meta-principles.md` 的层级定义。

- `/hoare-audit` 工作在 **Lv3 ↔ Lv4**：design report 描述应该做什么，代码 / YAML 是否真的做到了
- **Lv3（方案 / design report）= `/hoare-audit` 的硬底线 spec**；缺则先 `/hoare-design` 还原
- **Lv1 / Lv2 不是 `/hoare-audit` 的输入**；它们是 Lv3 出现「方案本身可疑」时的**仲裁杠杆**。有则减少 Decisional 数量，无则不阻塞 audit（只是更多歧义被推到 Decisional gate）
- **`/hoare-design` 只产 Lv3** descriptive spec，不产 Lv1 / Lv2
- **立 Lv1 / Lv2 是 `/charter-craft` 的工作**，不是 `/hoare-audit` 的工作
- 「函数级 Pre/Post/Invariant」是 Lv3 内部颗粒度选择，不是新的层级

**误区警示**：曾把 Lv0–Lv3 误读为「意图 / 架构 / 接口 / 函数」四级文档粒度。这是错的。Lv 是制宪体系的推导层次，不是文档粒度。

---

## audit 类 skill 的共性："驳回优先 / 先反后反反"

workflow-audit / hoare-audit / charter-craft §4.8 都共享一个机制——**审视者应先挑刺，再 counter-challenge**。

理论根据（charter-craft §4.8.1）：LLM 转换立场就能挑出问题（高 recall），单纯 confirm 几乎不发现问题（低 recall）；counter-challenge 过滤无效挑刺（高 precision）。反两次是经验最优点。

实际项目里：
- audit-principles.md 制宪用了 §4.8 先反后反反
- workflow-audit 直接把多方向并行 challenge 嵌入流程
- hoare-audit 用 spec 作为 ground truth 让 challenge 有可证伪 anchor

**判别**：写任何新 audit 流程，"先反后反反"应该是默认结构，不是 nice-to-have。

---

## schema-matching-agent：认知图式自适应路由

schema-matching-agent 不是传统意义上的 task skill，而是一个**认知姿态调节层**——它在回复前强制执行六对图式维度（抽象↔具体、中心↔边界、融贯↔符合、精确↔召回、压缩↔展开、构成↔调节）的显式判断，然后根据判断结果组织回答。

### 核心价值：纠正大模型默认输出偏置

裸调用大模型时，用户经常"红温"（感到烦躁、无力、被敷衍）——这通常不是因为回答内容错误，而是因为**认知姿态错配**。大模型有强烈的默认偏置：

- 倾向给出**中心性**回答（典型、泛化、教科书式），忽略用户真正关心的边界和例外
- 偏好**融贯**叙事（逻辑自洽、结构漂亮），即使与实际不符
- 压缩为**构成性断言**（"答案是X"），即使问题本身需要探索和调节
- 在**抽象-具体**轴上往往停在中间偏抽象，既不够原则也不够实操

schema-matching-agent 通过每轮强制 `<think_schema>` 判断来对抗这些偏置，显著缓解"答非所问""正确但无用""合理但不真"这三类最消耗用户耐心的体验。

### 适用场景

| 场景 | 为什么适合 | 示例
|---|---|---|
| **多轮对话中用户复杂意图的对齐** | 每轮强制重新判断图式，不会固化到初始姿态；`<steering>` 机制允许用户显式转向 | 用户从"给我概览"逐渐深入到"这个边界 case 怎么处理"，Agent 自动从抽象+中心移向具体+边界 |
| **人文知识、人文思考的通用助手** | 人文问题天然高模糊度、多视角，需要融贯与符合之间灵活切换，构成与调节之间恰当落位 | 讨论一个哲学概念时，Agent 能区分"给出确定解读"和"展示不同学派的张力"两种需求 |
| **各种技术方案的讨论（不涉及极度具体领域的落地细节）** | 方案讨论在精确/召回、压缩/展开、构成/调节三对维度上频繁切换；需要逻辑一致（融贯）但也要可验证（符合） | 架构选型讨论中，Agent 自动识别用户是在"做决策"还是"做探索"，切换构成/调节姿态 |

### 不适用场景

| 场景 | 为什么不适合 |
|---|---|
| 固定格式的执行任务（翻译、数据提取、代码生成） | 图式判断引入不必要的开销，执行型任务需要的是确定性和一致性，不是姿态调节 |
| 极度专业领域的精确诊断（医疗、法律文书） | 这些场景要求"符合+构成"端固定姿态，图式灵活性反而有害 |
| 需要高速批量处理的流水线任务 | 每轮强制 think_schema 有 token 和延迟成本 |

### 选用判据

- **问自己：这个回答的"姿态"比"内容"更重要吗？** 如果是 → 考虑 schema-matching-agent
- **问自己：用户会因为我们"怎么答"而红温，还是因为"答错了"而红温？** 如果是前者 → schema-matching-agent 有价值
- **问自己：这个任务需要每轮重新评估回答方式吗？** 如果不需要（一次性确定就够） → 图式机制是负担，不用

---

## 记入此文件的触发条件

- 用错了 skill / 用错了 skill 变体（如 v1/v2）发现的经验
- 两个看似可换的 skill 实际有清晰分工的情况
- skill 名字相似但定位不同的情况
- 通用项目工作流里反复证实的"在 X 场景该用 Y skill"判别
