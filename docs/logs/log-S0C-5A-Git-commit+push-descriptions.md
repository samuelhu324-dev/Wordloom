# Log-S0C-5A: Git commit + push descriptions (PR templates & conventions)

---

**id**: `S0C-5A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `Git commit + push descriptions (PR templates & conventions)`
**status**: `draft`           # draft | stable | archived
**scope**: `S0C`
**tags**: `DEVX, GIT, PR, TEMPLATE, PROCESS`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-23`
**updated**: `2026-02-23`

---

## Decision / Outcome（结论区）

**Decision**:

- 统一约定：默认只使用“顶层 S2B issue 分支”（避免额外分支爆炸）；子 issue 的推进通过 PR 标题/commit message 体现。
- 统一约定：PR 标题与 commit message 采用“Step（步骤）+ Cycle（轮次）”命名法，而不是用暗示线性次数的 PR 序号命名。
- 统一约定：PR 描述必须包含固定的“账本 + issue”跳转段落，以保持信息入口一致。

**Non-goals**:

- 本 log 只记录约定与自动化策略，不在这里直接落地 CI/workflow 修改（避免把 S0C 的改动混入 S2B 的交付流）。

## Background

随着 S2B-3A（outbox_core extraction & rollout）进入多 PR 切片推进，需要把“命名 + 描述 + 证据入口”的约定固定下来，否则会出现：

- PR/commit 难按 phase 回溯
- 账本信息分散（描述不统一、链接不稳定）
- 同一套 drills 的证据链难复用

## Problem / Malfunction

- 分支/PR/commit 命名不一致会导致历史回放成本上升。
- PR 描述缺少标准跳转信息会导致“最新状态在哪看”不统一。
- 需要一个轻量且可自动化的方式，让团队默认产出符合约定的标题与正文。

## Success criteria（DoD）

- PR 标题与 commit message 具备可机器校验的格式（可选：CI lint）。
- PR 描述包含固定的“账本 + issue”信息段落。
- 约定对单分支串行推进友好，不强制引入额外分支。

## Naming grammar（命名语法）

> 目标：让命名既能表达“线性推进”，也能表达“循环迭代”，并且可被脚本/CI 用正则稳定解析。

**格式（推荐）**：

- `S2B-3A/P0-S1: <summary>`
- `S2B-3A/P0-C2-S3: <summary>`
- `S2B-3A/P0-C2-S2S3: <summary>`

**字段含义**：

- `S2B-3A`：log id（任务/账本 id）
- `P0`：phase（例如 P0/P1）
- `C2`：cycle（可选，表示第 2 轮；用于表达“循环工作流”）
- `S1/S2/S3`：step（步骤编号）
  - 支持组合：`S2S3` 表示一次提交/一次 PR 同时覆盖 S2 与 S3

**避免使用的符号**：

- 不用 `>`（在 PowerShell/CMD 中是重定向符号，自动化很容易踩坑）
- 不用 `+` 表示组合（可读性尚可，但 URL/模板/正则处理成本更高；用 `S2S3` 更直观且更容易解析）

## Conventions（约定）

- **Branch**：默认使用顶层 S2B issue 分支（例如：`S2B-evolution/projection-table-merge`）。
  - 例外：只有在并行推进、冲突风险显著、或需要隔离试验时才引入额外分支。
- **PR title**（示例）：`S2B-3A/P0-S1: extract retry + reasons helpers`
- **Commit message**（示例）：`S2B-3A/P0-S1: extract retry + reasons helpers`
- **PR body（必须包含）**：
  - `- For more current info, take a look at <log-name> and **commits** under the PR`
  - `- About the issue itself, see: <issue>`

**PR body 的字段来源（建议）**：

- `<log-name>`：取当前 log 文件名（例如 `log-S2B-3A-unified-consumer-framework`）
- `<issue>`：取当前 log 的 `links.issue`（例如 `#119`）

## Automation options（自动化策略备选）

> 说明：GitHub 原生 PR template 只能“静态文本”，无法自动从账本里解析 `issue`/`log id`。

- **Option A（低成本，推荐起步）**：`.github/PULL_REQUEST_TEMPLATE/` 增加按账本划分的模板（手动选择模板）。
- **Option B（更自动）**：用脚本（PowerShell/Make/Task）创建 PR：
  - 从指定 log 文件解析 `**issue**` 与 log 名称
  - 自动拼 PR 标题、PR body，并调用 `gh pr create`
- **Option C（硬约束）**：CI 校验 PR title/body（不符合格式则失败）。

## Execution Checklist（可执行清单 + 可验收字段）

### P0（建议）：模板与规范落地

- [ ] 增加/整理 PR template 文件（按账本命名）
- [ ] 提供一条最短的“创建 PR”命令路径（UI 选择模板 或 脚本）

### P1（可选）：自动化/强校验

- [ ] 引入 `gh` 作为标准工具链（Windows/WSL2 都可）
- [ ] 提供脚本：从 log 读取 issue/log id → 自动生成 title/body
- [ ] 增加 CI lint：强制 PR title/body 格式

## Evidence

- Date: `YYYY-MM-DD`
  - Change: `S2B-3A/P0[-C<n>]-S<step>: ...` / `commit ...` / `ref ...`
  - Notes: `what changed; what it enforces`

## References

- `docs/logs/log-S2B-3A-unified-consumer-framework.md`
