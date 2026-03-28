# S0E-2B: automation/real GitHub issue creation automation

## Metadata

- Title: `S0E-2B: automation/real GitHub issue creation automation`
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Milestone: ``
- Source log: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Parent issue: ``

## Context

- `S0E-2B` 作为 `S0E-2A` 的 follow-up slice，只处理真正的 issue creation automation：从稳定的 draft-generation 入口推进到显式 opt-in 的 `create-issue` 模式。
- v1 先固定模式边界、脚本输入输出 contract 与 creation-side evidence contract，再进入本地 draft 生成实现与 GitHub create issue 真正调用。
- `S0E-2B` 不回头改写 `S0E-2A` 的 contract；`S0E-2A` 继续作为命名、labels、body scaffold 与 sample validation 的事实源。

## Definition of Done (DoD)

- 至少固定一版 `draft-generation` vs `create-issue` mode boundary；
- 至少固定一版脚本最小输入/输出 contract，并说明哪些字段允许 override；
- 至少固定一版 creation-side evidence contract，明确 draft mode 与 create mode 各自必须留下什么；
- 至少明确声明：真正创建 GitHub issue 的实现阶段属于 `S0E-2B`，不再回头挤进 `S0E-2A`；
- 后续 `P1/P2` 实现不需要再回头争论默认模式和失败语义。

## Links

- Log: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent Log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous Log: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
- Reference Log 1: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
- Reference Log 2: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Reference Log 3: `docs/roadmap/draft.md`
