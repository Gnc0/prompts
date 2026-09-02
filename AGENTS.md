# Branch Relationship & Workflow

## 仓库与分支关系

```
origin  (ssyram/prompts)  ─── 原仓库，上游源码
  └── main                    原仓库主分支（唯一真相源）

fork    (Gnc0/prompts)    ─── 我的 GitHub Fork
  └── main                    镜像 origin/main，保持同步

本地
  ├── main                    ⚠️ 只读镜像，永远与 origin/main 保持一致
  └── tool                    ✅ 主力开发分支，所有改动在这里进行
```

## 核心原则

| 分支 | 用途 | 规则 |
|------|------|------|
| `origin/main` | 原仓库主分支 | 永远不直接推送，只通过 PR 合入 |
| `main`（本地） | origin/main 的本地镜像 | **禁止直接在 main 上 commit**，只做 pull |
| `tool`（本地） | 主力开发分支 | 所有开发、实验、修改都在此分支进行 |

## 标准工作流

### 1. 同步上游
```bash
git checkout main
git pull origin main          # 拉取原仓库最新代码
git push fork main            # 同步到自己的 Fork
```

### 2. 日常开发（在 tool 分支）
```bash
git checkout tool
# ... 进行开发、修改、测试 ...
git add .
git commit -m "描述你的改动"
```

### 3. 将 tool 的改动合入 main 并推送

注意tool不能全量推送到main，而是必须询问用户要推送哪些内容。

下面是禁止推送文件名单：
 - .gitignore
 - CLAUDE.md
 - README.md

```bash
git checkout main
git merge tool                # 将 tool 的改动合并到 main
git push fork main            # 推送到自己的 Fork
git checkout tool              # 切回 tool 继续开发
```

### 4. 向上游提交 PR
在 GitHub 上从 `fork/main` 向 `origin/main` 发起 Pull Request。

### 5. 路径限定同步（如：只把上游的 current/ 覆盖到本地）

当用户请求按**路径**限定范围（「只更新 X」「把上游的 X 覆盖到本地」）时，操作范围必须严格等于请求的路径集合，用路径级覆盖而非整支合并：

```bash
git fetch https://github.com/ssyram/prompts.git main   # 上游无 remote 时按 URL 抓取
git checkout tool
git checkout FETCH_HEAD -- current/     # 路径级覆盖，只动 current/
git commit -m "sync: 覆盖更新 current/（来自 ssyram main <short-sha>）"
git push origin tool                     # 是否推送需用户确认
```

**禁止**用整支 `git merge` / `git pull` 完成路径限定请求——merge 会把上游分支的全部内容（`drafts/`、`docs/`、`.pi/` 缓存、归档目录等）一并带入 tool。

> **over-extend 教训**：用户要求「看 ssyram main 的 current 有什么更新，覆盖到本地 current」，助手却按整支同步流程执行了 `main 快进 + merge main 到 tool`，把上游 `drafts/qpdi*.md`、`docs/occams-razor/`、`.pi/impression-cache/` 等非 current 内容带进 tool，被用户指出后只能 `reset --hard` 回退、路径级重做、force-push 修复。两条规则：
> 1. **方案超出用户请求的字面范围（哪怕只多带一个目录）时，必须显式指出并单独确认**，不能打包进「标准工作流」顺势执行；
> 2. **diff 比较时「内容一致」≠「merge 无副作用」**——tool 分叉点较旧时，即使 current/ 内容一致，merge 仍可能产生 add/add 冲突并带入意外文件。

## 网络配置

- 与 GitHub (gh / git) 通信时，默认使用本地代理端口 **7897**，即设置 `https_proxy=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897`

## 子模块

| 路径 | 远程仓库 | 分支 | 用途 |
|------|----------|------|------|
| `claude-code-system-prompts` | `https://github.com/Gnc0/claude-code-system-prompts` | main | Claude Code 系统提示词集合 |

### 克隆后初始化子模块

```bash
git submodule update --init --recursive
```

### 更新子模块到最新

```bash
git submodule update --remote claude-code-system-prompts
```

## 注意事项

- **永远不要** `git push origin main`（不要直接推原仓库）
- **永远不要** 在 `main` 分支上直接 `commit`
- `tool` 分支可以频繁 commit、rebase、force-push，它是你自己的开发空间
- `main` 分支应该始终保持干净，与 `origin/main` 一致
- 如果 `tool` 积累了大量零散 commit，合入 `main` 前考虑用 `git rebase -i` 整理
- 路径限定请求（「只更新/覆盖某目录」）**禁止整支 merge**，用 `git checkout <ref> -- <path>` 做路径级覆盖（见标准工作流第 5 节的 over-extend 教训）

## current/ 技能路由（当前维护版本）

`current/` 是当前维护版本的**唯一真相源**——涉及具体 prompt / skill 时默认从 `current/` 读取，新增或修改 prompt 也收敛到 `current/`。

| skill | 一句话说明 |
|---|---|
| hoare-prompt / hoare-design / hoare-audit | HoarePrompt 方法参考 / 从实现反推描述性规约 / 有 spec 前提下的持续正确性审计 |
| workflow / workflow-audit | 通用开发流程规范 / 多方向 disprove-first 的 PR 审计 |
| qpdi / qpdi-compose / qpdi-tribunal / scco-recall | QPDI 认知与论证框架 / Q+D 写作 / SCCO 公检法审查 / SCCO 召回扇出（只捞不判） |
| principle-derivation / -v2 / -paper-reading / code-reasoning | 问题意识驱动推导（v1 事后整理 / v2 邀请同行 / 论文阅读特化 / 代码 bug 讲清+判真假特化） |
| finegrained-check / evo-graph / make-survey-plan | 细粒度一致性检查 / 演进关系图梳理 / survey 调研流程 |
| charter-craft / pr-craft | 项目宪法制定与修订 / PR 描述书写规范 |
| explain / no-flattering / pi-consult / prompt-iter | 向具体的人讲清事实 / 拒绝迎合先拷打 / 多模型顾问调度 / 用测量迭代提示词 |
| auto-proof-trajectory-audit | auto-proof-cc 运行轨迹的符合度评判与根因分析 |
| schema-matching-agent | 六对图式匹配认知 Agent 系统提示 |

选 skill 的判别经验见 `current/skill-routing.md`——它不是 skill 规约，而是**给主对话 Claude 看的路由参考**（易混 skill 的区分、用错 skill 的教训）。遇到「该用哪个 skill / 哪个变体」的歧义时先查它。

## prompt-is-winning-so-much 技能库路由

`prompt-is-winning-so-much/` 是**技能类** prompt 合集（对话规范、认知姿态、哲学对话等），与 `current/` 的工程类 prompt 互补；下每个子目录是一个技能，进入任一目录后，`SKILL.md` 提供该技能的版本级路由（二级路由；例外：`designer/` 无 SKILL.md，由各专业 prompt 的 description 与管线分工承担路由）。技能库的增删需同步更新本表。

| 技能 | 路径 | 一句话说明 |
|------|------|------------|
| abstraction-analyst | `prompt-is-winning-so-much/abstraction-analyst/` | 回应前先完成理解：定位真实需求在话题结构中的位置 |
| analytic-philosophy-prose | `prompt-is-winning-so-much/analytic-philosophy-prose/` | 以顶刊分析哲学范式写作/改写/评审哲学文本 |
| designer | `prompt-is-winning-so-much/designer/` | 游戏系统策划三级管线（`sd-module-loop` / `sd-mda` / `sd-writer`）+ `design-purpose-reviewer` 上位设计目的审查 + `system-designer-level-spec` 分级标尺；最终定值与配置交下游数值策划流程 |
| general-prompt | `prompt-is-winning-so-much/general-prompt/` | 七层图式闭合提示词生成（基础 / 判官版） |
| philosophy-explorer | `prompt-is-winning-so-much/philosophy-explorer/` | 哲学探索：思想编辑与暂定判断生成（基础版刚性 / 规约版调节软化） |
| philosophy-interlocutor | `prompt-is-winning-so-much/philosophy-interlocutor/` | 哲学对话：结论放最后、每步推导可被击中、概念从现象自身结构长出、不擅自开辟新论域、不使用排版装饰 |
| schema-matcher | `prompt-is-winning-so-much/schema-matcher/` | 六轴图式判断：每次回复前显式输出 think_schema 块，对齐需求图式位置（含 eval/ 评测脚手架） |

> 屏蔽说明：`prompt-only-look-myself/` 已加入 `.gitignore`，不被版本追踪。


# 如果你不运行在PI-Agent里面，则需要立刻读取.pi/APPEND_SYSTEM.md
