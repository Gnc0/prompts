---
name: qpdi
description: QPDI 静态认知与论证框架——理解 Q、递归 D-frame（P/M/R）、I 及其关系，并用 Structural Locality、SCCO、Discover 与 re-unification 整理复杂用户材料。工作流和输出形式只是可覆盖的推荐。
---

# QPDI — 静态认知与论证框架（Draft）

任务材料：
$ARGUMENTS

QPDI 首先是一组内容角色与论证关系，不是固定流程、文档层数或输出 schema。后文的分析方法和文件布局只是默认建议，可以被用户指令覆盖。

# 一、静态本体

## 1. 总图

```text
Q = Q.I + Q.A + Q.E

upstream obligation + relevant Q
          └─ R.Derivation ─→ P

D-frame = P + M + R
M = components + composition
          └─ R.Satisfaction ─→ M ⊨ P

I ── realizes/refines ─→ leaf M
```

只有以下内容角色属于核心本体：`Q.I / Q.A / Q.E / P / M / R / I`。root、component、leaf、local/global、candidate/confirmed 等是位置、作用域或状态，不是新的内容类型。

## 2. Q：问题意识

Q 是人的最小不可委托边界。AI 可以整理、挑战或提出 candidate Q，但不能替人确认规范方向。

### Q.I — 规范定义

Q.I 定义当前问题中什么算正确、真正想要什么、边界在哪里：

- **Correctness**：什么结果可接受，什么构成错误；
- **Wanted**：在正确候选中追求、保护或优先什么；
- **Boundary**：评价适用于哪里、不可接受什么、哪些不在承诺范围内。

三者是同一规范判断的观察面，不是三种 Q.I。Q.I 应能排除至少一类结果，但不提前指定机制或实现。

### Q.A — 被采纳的认知命题

Q.A 是实际参与 R 的环境、对象或机制命题。它说明“承认什么为真”，不自行产生“应该如何”的方向。

只记录真正被推导消费的命题。事实状态（verified / pending / contested）是证据元数据，不是 Q.A 的子类型。

### Q.E — 经验材料

Q.E 是实际参与论证的观察、样本、成功经验和失败 pattern。它提供证据与经验支撑，不自动成为事实真值或规范授权。

Q.A 与 Q.E 不重复存同一概括：若经验被归纳成世界模型命题，写成 `Q.A supported-by Q.E`。单次现象通常只是有限范围的 Q.E candidate。

## 3. D-frame = P + M + R

一层完整设计是一个递归 D-frame：

- **P**：规定本层设计必须满足什么；
- **M**：给出本层设计如何由 components 组合呈现；
- **R**：证明为什么得到这些 P，以及为什么 M 满足 P。

同一对象在父 frame 中可以是 component；继续展开时，它成为自己的 D-frame。`D.root` 直接回答 Q.I；其他 frame 的直接上游是父层分配的 obligation，而不是重新解释原始 Q。

### P — 可判定设计性质

P 是 frame 拥有的全部可判定设计性质。commitment、pre/post、invariant、存在性、关系约束、禁止条件和显式保护的自由度，都是 P 的内容或表达形式，不与 P 并列。

P 的作用域只有两种模式：

- `scope = owner`：只约束当前 frame，常称 local P；
- `scope = descendants(selector)`：对条件命中的后代 frame 生成 obligation，常称 global P。

Local/global 是 `P.scope`，不是两类本体。父层不会把整组 local P 复制给 component，而是从 P 投影出 component contract。

未被 P 规定的部分是补空间，不另立“未规定空间”内容；若某种自由度本身必须被保护，它就成为显式 P。

### M — Operational Model

M 由两部分组成：

- **components**：各 component 在本层的角色、接口与被分配的 contract；
- **composition**：它们如何通过控制、数据、状态、顺序、失败或责任关系形成整体行为。

只有零件清单而无 composition，不是完整 M。父 M 只引用 component occurrence 与 contract，不内联完整 child frame。

M 只需具体到足以证明 P，可以是抽象且非确定的；同一 P 可以有多个 M。

### R — Reasoning

R 具有两个必需证明目标和一个按需目标：

- **Derivation**：上游 obligation、Q.I、相关 Q.A/Q.E 与适用 global P 足以推出本层 P；
- **Satisfaction**：component contracts 与 composition 联合证明 `M ⊨ P`；
- **Choice evidence**：存在真实候选时，说明为何当前 P/M 更简单、稳健或依赖更小。

Choice evidence 是 SCCO Optimality 的对象级证据，不是新的本体。SCCO 负责判断候选是否真实、比较是否充分；没有真实候选时不制造比较。

R 不能暗中新增 P。若证明需要未写明的约束，应通过 Discover 把它写回 P。

## 4. I — 具体 realization

I 是叶子 M 在具体环境中的 realization/refinement：代码、可执行配置、具体字段、命令、部署物或最终文案。

D/I 边界取决于语义角色，不取决于文件格式或“是否技术化”：

> 若两个选择不同，但全部 P 与 M 的可观察行为不变，差异属于 I；若差异改变可观察行为、跨组件契约或风险边界，它仍属于 P/M。

I 不直接从 Q 取得规范授权。测试、命令、simulation 和实际产物为 `I realizes M` 提供证据；“代码能跑”不等于 realization 成立。

# 二、关系规则

## 5. Structural Locality

Structural Locality 规定每条 R 可以使用哪些来源：

- root frame 从 Q 取得规范上游；
- child frame 从父 contract 与适用 global P 取得直接 obligation；
- child 可引用相关 Q.A/Q.E，但不能绕过父 contract 重新解释 Q.I；
- sibling 的 owner-scope P 不能横向泄漏；共同设计约束提升到公共祖先 P，共同领域命题进入 Q.A；
- 传播必须有 owner、scope 与 selector，不能仅凭“位置更高”。

## 6. SCCO

SCCO 是对内容、证明边和整体闭包的评价器：

- **Sound**：来源合法、前提状态诚实、推导有效，`I realizes M`；
- **Complete**：上游 obligation、P、component discharge、global P 实例和 realization 均被覆盖；
- **Concise**：无重复所有权、孤立项、陈旧库存、无消费者字段或重叠规则；
- **Optimality / Orthogonality**：真实候选中不存在无理由的更优路径；职责与性质集合不过度重叠。

SCCO 不自动证明事实真值、经验可靠性、审美或默会判断。R 提供对象级证明，SCCO 检查证明是否充分，二者不重复。

## 7. Discover

Discover 是发现缺口后的归层与修订算子：

```text
新的规范方向                 → candidate Q.I
世界模型命题变化              → candidate Q.A
经验材料确认、反驳或修正       → candidate Q.E
缺少可判定性质                → P
缺少 component / composition → M 或 child frame
P/M 已有但证明缺失             → R
具体 realization 偏差         → I
```

应回到能够完整拥有缺口、且不引入额外规范授权的最近上游 owner，而不是机械地“越高越好”。

## 8. Re-unification

分析可以展开概念；回答或落盘前必须重新统一：

1. 同义项合并；
2. 子类与表达形式收回父概念；
3. 角色、位置、状态和证据移出内容本体；
4. 同一命题只保留一个权威位置，其他处引用；
5. 只留下真正正交、具有消费者的内容。

例如：pre/post 收回 P；local/global 收回 `P.scope`；component/leaf 收回 D-frame 的相对位置；confirmed/pending 属于元数据；Q.A 与 Q.E 用 support 边连接而不复制概括。

# 三、轻量推荐用法

## 9. 分析用户话语

先识别用户论域、话语动作与授权范围。复合话语先保全前提、证据、推导和结论，再逐节点锚定；下游影响不改变主论域，也不自动授权修改。

推荐短链：

```text
识别论域
→ 去除偶然实现专名
→ 保全用户 proof
→ 锚定 Q / P / M / R / I
→ 检查上下游与 SCCO
→ re-unify
→ 回答或执行
```

可用简短 `/` 对齐开头，但用户格式优先：

```text
/论域：
/论证：
/锚定：
/行动：
```

## 10. 推荐文件视图

```text
docs/design/
  principles.md      # Task Overview + Q
  design/            # 一个或多个递归 D-frame

docs/audit/          # SCCO 与证据（需要时）
```

文件名和层数不是本体。小项目可以合并，大项目按真实 frame 展开。状态、证据、路径和授权属于工作元数据，不得反向制造新的内容类型。
