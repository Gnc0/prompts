---
name: qpdi-compose
description: 编写 Q 与递归 D-frame——从用户材料整理 Q.I/Q.A/Q.E，以 P/M/R 写设计并逐层展开，必要时按授权落盘。专注内容写作，不生成 I，不代替 SCCO 审查。
argument-hint: "[材料、目标文件或要编写的 Q/D 范围]"
---

# QPDI Compose — Q 与 D 写作方法（Draft）

输入材料：
$ARGUMENTS

本 prompt 使用 `/qpdi` 的静态定义，专注“怎么写”。以下模板均可被用户指令或项目结构覆盖；没有真实内容或消费者的字段直接省略。

# 一、写作入口

## 1. Task Overview 与 Q.I 分开

先用最少文字说明整件事，再写 Q：

```markdown
# Task Overview
- 问题对象与现状：
- 本次范围：
- 主要材料：
- 预期产物：
```

Overview 负责导航，不取得规范效力。Q.I 只定义什么正确、什么想要、边界在哪里；背景、事实、经验、方案和理由分别进入 Overview、Q.A、Q.E、P/M、R。

## 2. 写前分析

用户话语复合时：

1. 识别论域、话语动作和授权范围；
2. 保全用户给出的前提、证据、推导和结论；
3. 区分用户原话、既有内容、隐含前提、待核事实与模型候选；
4. 去除偶然实现专名，判断真正缺失的是 Q、P、M、R 还是 I；
5. 写完后 re-unify：合并同义项，把表达形式、状态和视角收回原生概念。

简单材料直接写，不强制输出分析账本。

# 二、Q 怎么写

## 3. 共同规则

- 一条 Q 只表达一个可独立确认或修订的内容；
- 用户原话与模型归纳分开；AI 归纳的 Q 默认是 candidate；
- 只保留会被 D.root、R 或用户裁决实际消费的内容；
- 内容采纳、事实核验和写入授权是三条独立状态轴，不相互推出。

## 4. Q.I — 规范定义

Q.I 定义 current problem 的 correctness、wanted result 与 boundary。三者是写作视角，不必机械分栏。

```markdown
### Q.I.<id> — <标题>
**statement**：<什么算正确、想要或不可接受>
**scope**：<适用范围与非目标>
**content status**：candidate | confirmed | superseded
**source**：<用户原话或确认依据>
```

好 Q.I 能排除至少一类候选结果，但不提前指定机制。背景介绍、世界事实、失败经验和解决方案不进入 Q.I。

## 5. Q.A — 被采纳命题

```markdown
### Q.A.<id> — <标题>
**statement**：<实际参与 R 的环境、对象或机制命题>
**scope**：<成立范围>
**content status**：candidate | confirmed | superseded
**evidence status**：verified | pending | contested
**source / support**：<依据或 Q.E 引用>
```

Q.A 不涉及根本对错，也不独立产生规范方向。只有参与推导的命题才进入；纯背景留在 Overview。

若某事实构成 Q.I 含义本身的存在条件，应在 Q.I 中展开；若只是当前世界如何运作，则属于 Q.A。

## 6. Q.E — 经验材料

```markdown
### Q.E.<id> — <标题>
**observation / pattern**：<发生了什么>
**sample and scope**：<样本、场景、边界>
**content status**：candidate | confirmed | superseded
**evidence status**：verified | pending | contested
**evidence**：<记录或来源>
```

分开 observation 与归纳。若经验被概括成供 R 使用的世界模型命题，建立 `Q.A supported-by Q.E`，不要在两处复制同一句话。单次事件不自动成为普遍 pattern。

# 三、D-frame 怎么写

## 7. 核心结构

```text
D-frame = P + M + R
```

- **P**：本层设计必须满足的全部可判定性质；
- **M**：components 及其 composition 构成的 operational model；
- **R**：证明上游推出 P，且 `M ⊨ P`；真实候选存在时提供选择依据。

同一 component 在父层只是 M 中的出现项；展开后才成为自己的 D-frame。只有 D.root 直接回答 Q.I，其他 frame 接受父层分配的 contract。

## 8. P — 写规格

P 的最小写法：

```markdown
### P.<id> — <性质名称>
**predicate**：<可判定性质>
**scope**：owner | descendants(<selector>)
**source**：<root 使用 Q.I；child 使用 parent allocated contract；必要时加适用 global P>
**excludes**：<不满足时排除什么>
```

`scope=owner` 常称 local P；`scope=descendants(selector)` 常称 global P。它们是同一 P 的作用域模式，不需要两套本体。

pre/post、invariant、存在性、关系约束、禁止条件和显式保护的自由度，都是 predicate 的表达形式。根据材料选最清楚的形式，不把它们列成并列概念。

Global P 命中后代时生成 obligation；仅写在祖先文档中而无 scope、selector 或 discharge，不算落实。

## 9. M — 写 operational model

```markdown
### M
**components**：
- <component>：<role；allocated contract>

**composition**：
<components 如何通过控制、数据、状态、顺序、失败或责任关系形成整体行为>
```

规则：

- component 只保留父层需要的 role 与 contract，不内联完整 child frame；
- contract 是父 P 的投影，不是复制一份 P；
- 组件清单没有 composition，不构成完整 M；
- M 具体到足以证明 P 即可，同一 P 可以有多个 M。

## 10. R — 写证明

```markdown
### R
**Derivation**：<root：为什么从 Q 得到 P；child：为什么从 parent contract 与适用 global P 得到 P；Q.A/Q.E 只作认知或经验支撑>
**Satisfaction**：<component contracts 与 composition 如何联合证明 M ⊨ P>
**Choice evidence**：<仅在存在真实候选时，说明为何当前 P/M 更合适>
**Open obligations**：<尚未被 discharge 的义务；没有则省略>
```

R 不暗中新增 P；需要新约束时先写回 P。Choice evidence 是 SCCO Optimality 的审查对象，不必每次制造候选。

## 11. 递归展开

```markdown
## D.<id> — <frame 名称>
**upstream**：<Q.I（仅 root）或 parent allocated contract>
**applicable global P**：<命中的规则>

### P
...
### M
...
### R
...
```

只有 component 仍有未解决的语义设计问题时才展开下一层。展开时：

```text
parent allocated contract
→ child P
→ child M
→ child R
```

没有剩余语义设计问题时，它是叶子 frame；不制造空层级。

# 四、I 边界与证据

Compose 不写 I，但必须知道何处停止：

> 若两个选择不同而全部 P 与 M 的可观察行为不变，差异属于 I；若差异改变行为、跨组件契约或风险边界，仍应写进 P/M。

I 通过具体代码、配置、字段、命令或部署物 realizes/refines 叶子 M。测试、命令和 simulation 是 realization 的证据，不是新的设计内容。

# 五、Trace、状态与 re-unification

## 12. 最小关系

```text
Q.I ← answered-by D.root
Q.A ← supported-by Q.E
R ← depends-on Q / parent contract / applicable P
component ← role-in parent M
child frame ← allocated-contract parent M
I ← realization-of leaf M
```

只保留有 reader 的反向链接和字段；能从结构推导的索引不重复手写。

## 13. 状态与授权

- 内容：candidate / confirmed / superseded；
- 事实：verified / pending / contested；
- 文件：response-only / write-authorized / written。

三者相互独立。确认 Q 不等于事实已验证或允许写文件；授权写文件也不等于确认 candidate Q。

## 14. 写完后的 re-unification

提交草案前检查：

- 是否把父概念和例子并列；
- 是否把 scope、状态、位置或角色写成内容类型；
- 是否用不同词重复同一命题；
- 是否存在无消费者字段、孤立 P 或空 D 层；
- 是否把 R 中的新约束漏写回 P；
- 是否越界写入 I。

SCCO 在此只要求 P/M/R 可检查；系统性召回、攻击与裁决交给专门审查 prompt。

# 六、落盘

推荐但不强制：

```text
docs/design/
  principles.md   # Task Overview + Q
  design/         # 递归 D-frame
```

小项目可以合并，大项目按真实 frame 展开。用户只要求草案时默认 response-only；明确授权路径后才写入。覆盖前读取，写后复核，只修改获授权的 Q/P/D 文件。

推荐回复：

```text
Task Overview：
Q 草案或修订：
D-frame：P / M / R
待核事实与 open obligations：
需要用户确认：
已写文件（如有）：
```

格式服务内容，用户指定优先；不为填满模板制造概念。
