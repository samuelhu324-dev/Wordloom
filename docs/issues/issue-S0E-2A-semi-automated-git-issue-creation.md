# S0E-2A: contract/semi-automated Git issue creation contract

## Metadata

- Title: `S0E-2A: contract/semi-automated Git issue creation contract`
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Milestone: ``
- Source log: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
- Parent issue: ``

## Context

- `S0E-2A` 收口一版面向 structured logs 的半自动化 Git issue 创建合同，明确哪些字段可以 full-automation、哪些字段必须 semi-automation、哪些字段继续手工维护。
- v1 的目标不是直接生成高质量 issue 总结，而是优先稳定 title keyword vocabulary、labels taxonomy、body scaffold、milestone mapping 与 log frontmatter 的映射关系。
- 同步把 parent/phase log templates 增加 issue-aware frontmatter 字段，并明确“字段缺失时必须保守留空”的 fallback 规则。

## Definition of Done (DoD)

- 至少固定一版 `fixed-keyword` 受控词表，并说明每个词的使用边界；
- 至少固定一版 labels taxonomy，明确哪些 labels 属于 full / semi / zero automation；
- 至少明确回答“labels 是否需要预创建”：答案为是，并写入 contract；
- 至少定义一版 issue body scaffold，且能稳定回链对应 log；
- 至少定义一版 milestone mapping 规则，并明确“有字段才自动，没有字段就留空”；
- 至少给出一版 log frontmatter -> issue fields mapping；
- 至少保留 2~3 个代表性 sample（例如 `S4E-5B`、`S5B-4A`、`S6A-4A`）作为后续验证对象。

## Links

- Log: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent Log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous Log: `docs/logs/log-S0D-6A-docs-management-v4.md`
- Reference Log 1: `docs/logs/log-S4E-release-operating-model-and-governance.md`
- Reference Log 2: `docs/logs/log-S6A-evidence-drills-spine.md`
- Reference Log 3: `docs/roadmap/draft.md`
