# S0E-2C: automation/batch issue creation and issue relationship backfill tooling

## Metadata

- Title: `S0E-2C: automation/batch issue creation and issue relationship backfill tooling`
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Milestone: ``
- Source log: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
- Parent issue: ``

## Context

- `S0E-2C` 作为 `S0E-2B` 之后的新 follow-up slice，处理单条 issue creation 已经跑通之后的批量化与回填问题。
- v1 先把 batch selection、parent-child linking、milestone/backfill tooling 的 contract 收口，再决定是否进入单命令 bulk pipeline。
- `S0E-2C` 只扩展 operator tooling，不回头修改 `S0E-2A` 的命名合同，也不重做 `S0E-2B` 的单条 create path。

## Definition of Done (DoD)

- 至少固定一版 batch manifest 和 dry-run contract；
- 至少固定一版逐项结果输出 contract，区分 create/link/backfill 三类操作；
- 至少明确 parent-child linking 不做语义猜测，只接受显式输入或受控映射；
- 至少明确 milestone/backfill tooling 的 apply boundary 与回写边界；
- 至少有一轮 representative dry-run evidence，证明批量工具不会绕过 `S0E-2A/S0E-2B` 的 fail-closed 语义。

## Links

- Log: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent Log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous Log: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Reference Log 1: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
- Reference Log 2: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Reference Log 3: `docs/runbook/run-S0E-log-to-issue-creation.md`
