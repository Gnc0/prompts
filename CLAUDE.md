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

## 网络配置

- 与 GitHub (gh / git) 通信时，默认使用本地代理端口 **7892**，即设置 `https_proxy=http://127.0.0.1:7892 http_proxy=http://127.0.0.1:7892`

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
