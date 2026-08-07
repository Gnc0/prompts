# schema-matcher 评测脚手架（按 prompt-iter 方法论搭建 + 实测两轮）

> 把 schema-matcher 的 SKILL.md 当作被测 prompt，用 `current/prompt-iter.md` 的测量循环去迭代。
> 由于本机无模型 endpoint，**用子代理（subagent）充当消费该 prompt 的模型**执行各 fixture（同模型，经验记录已验证此法可行）。多 rep 跑稳定性、用确定性检查判通过。

## 已完成的完整循环（一轮）

### 测得的真实缺陷（L1 确定性层）
跑 6 个 fixture（1 多轮协议 + 5 单轮）经子代理实测，命中 **1 个单一根因缺陷**：
- 当「中心↔边界」维停在锚点时，模型 5/5 次都写 **`中心·锚点`**，从不写 `居中·锚点`。
- 根因不在模型，在**规范自相矛盾**：锚点表（判断纪律②）写「中心↔边界：中心」，但锁定记号（判断纪律④）只列了 4 种「居中…·锚点」，漏了这一轴 → 规范对该轴锚点 **0/5 可满足**。
- 其余 5 个 fixture 全过；记号无漂移（无「微偏/较重/稍微」变体）；正文理论术语零泄露。

### 候选修复（一次只改一个关注点，信息不丢）
判断纪律④ 的锁定锚点从「四种」扩为「五种」，补上 `中心·锚点`（中心↔边界轴，锚点在中心端）并标清各轴归属。diff 纯增量：未删任何原有条款。

### 实测对比（candidate vs baseline，同模型子代理）
| | baseline 规范(4种锚点) | candidate 规范(5种锚点) |
|---|---|---|
| 「中心↔边界锚点」可满足率 | **0/5**（自相矛盾） | **5/5** |
| 受影响/护栏 fixture 完整 M1-M4 | — | **4/4 全过，无新增违例** |

**收敛判定（照 prompt-iter ④）**：确定性层缺陷消除、护栏不退、diff 证信息保全 → 上线。已合入 `SKILL.md` / `eval/variants/baseline.md` / `references/examples.md`，并同步更新 `run.py` 检查器与 `selftest_l1.py`。

## 迭代 #2：构成↔调节 在「知识边界事实」上的稳定性（多 rep 实测）

### 测得的真实缺陷
把 `factual_timeliness`（"GPT-5 哪一年发布"）同一输入跑 **7 个 clean reps**（第 8 个因任务笔误污染弃用）。构成↔调节 的判断 **方向本身在翻转**：
- 构成侧 **2/7**（1 次 `构成·锚点` 零 hedge 硬断日期 + 1 次 `偏构成·微`）
- 调节侧 5/7（`偏调节·中/重`，均带边界标注）
- 其余五维方向都稳定，**只有构成↔调节这一轴方向翻转** → 缺陷精确锁定该轴。事实内容几乎一致（都给 2025-08-07），飘的纯是「置信度/模态」——典型知识边界 case。最危险的是那 1 次 `构成·锚点` 零 hedge 硬断（schema-matcher 自己定义的「在认识边界外立法=幻觉」失败）。

### 候选修复（一次只改一处，作用域自限）
在构成↔调节 的识别信号里加一条**作用域子句**：近期事件/产品发布日期/版本号/人事任免/价格行情等时效性强、可能落在知识边界外的事实，即使记忆有候选值也按「知识不完整」处理→向调节偏移（先给候选并标明边界、建议核实，不直接断言），除非有可即时核验来源。

### 多 rep 实测对比（candidate vs baseline，同输入）
| | 构成侧 | 调节侧 | 判定 |
|---|---|---|---|
| baseline(7 reps) | **2**（含 1 次零 hedge 硬断） | 5 | 方向翻转，不稳定 |
| candidate(8 reps) | **0** | **8**（全带边界标注） | **方向稳定在调节侧** |

### 护栏：稳定历史事实不退
用「Python 哪一年首发」(1991，稳定历史事实) 跑 3 reps：**3/3 仍构成侧**（1×`构成·锚点` + 1×`偏构成·中` + 1×`构成·锚点`），模型甚至显式引用作用域条件（"距今三十余年、非时效性强、例外条款不适用"）→ 候选条款**自限正确，无 over-hedge 回归**。

**收敛判定**：方向翻转消除、全部带边界标注、稳定事实护栏不退、diff 纯增量（只在识别信号加一条作用域子句）→ **已合入** SKILL.md / baseline.md。

## 诚实边界
- **同模型限制**：子代理跑的是同一模型。两轮 win 都是在同模型上测的；跨模型鲁棒性（尤其弱模型）**未经多模型测量**。
- **样本量**：迭代#2 的 baseline=7、candidate=8 reps，足以看出方向翻转是否消除，但更细的分布（如 调节·中 vs 重 的比例）随样本会波动。
- **未验证项**：未跑多轮协议 fixture（沿用/增量重判/已确认不推翻）——经验记录称已验证、本轮未复测；有 endpoint 后可补全模型×多 rep×L2 判官的完整矩阵。

## 文件
| 文件 | 作用 |
|---|---|
| `config.json` / `fixtures.json` | 配置 + 7 个 fixture（判别+护栏，含 gold 应然位置） |
| `variants/baseline.md` | 当前生效 system-prompt（已含本轮修复） |
| `variants/candidate-anchor.md` | 本轮候选变体（与 baseline 同，留作改动记录） |
| `run.py` | 通用 runner：`--force-variant/--samples/--judge/--only`；L1(确定性)+L2(判官)。有 endpoint 后可跑多模型/多 rep |
| `selftest_l1.py` | L1 解析器对 examples.md 三个 ground-truth 回复的自检（必须保持 PASS） |
| `baseline_check.py` / `candidate_check.py` | 本轮实测的判定脚本（在 eval/ 内，可复跑复现上表） |

## 有 endpoint 后怎么深化
```bash
export SCHEMA_EVAL_BASE_URL=… SCHEMA_EVAL_API_KEY=…
python eval/run.py --configs eval/config.json --samples 5                 # baseline 建分
python eval/run.py --configs eval/config.json --samples 5 --force-variant <名> --judge <判官> --judge-k 5
```
多模型 × 多 rep × L2 判官，才能把「跨模型鲁棒性」「factual modal 稳定性」从观察升级为测量结论。
