# log-S0D-3A-runbook-stub（Phase 3：runbook stub 策略｜按顶层 scope 收敛 runbook 入口 v1）

---

**id**: `S0D-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `runbook stub strategy（按顶层编号筛选、生成、收敛 runbook 入口） v1`
**status**: `stable`           # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Runbook, Workflow, Stubs, Curation, epic/s0, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  **previous_log**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  **reference_log_1**: `docs/runbook/run-S2B-projection-table-merge.md`
  **reference_log_2**: `docs/runbook/run-S2C-projection-framework-platformization.md`
  **reference_log_3**: `docs/runbook/run-S2D-projection-onboarding-hard-gates.md`
  **reference_log_4**: `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
**created**: `2026-03-13`
**updated**: `2026-03-13`

---

## Decision / Outcome（结论区）

**Decision**:

- runbook 的主组织单位采用“顶层 scope 优先”，即优先按 `S2B`、`S2C`、`S2D`、`S5B` 这类顶层主题建立稳定操作入口，而不是为每个子 log 或每个 issue 分别建 runbook。
- 是否建 runbook 不由“资料数量”决定，而由“是否已经形成可重复执行的 operator workflow”决定。
- runbook 只收敛操作入口、证据口径、排障和回滚路径；log、issue、adr、lab 保持各自职责，不被 runbook 吞并。
- 同一个顶层 scope 下存在大量 log 和 issue 时，runbook 只链接少量关键材料，不做全集索引；全集索引应继续留在 spine log、roadmap 或 docs index。

**Default choices（本 phase 默认决策 / v1）**:

- 一个顶层 scope 默认最多维护一个主 runbook 入口。
- 只有满足“稳定入口 + 可重复执行 + 值得 operator 依赖”时，才从 log/issue 升格为 runbook。
- 每个 runbook 默认只保留 3 到 7 个关键引用：`parent log / 核心 phase logs / ADR / lab or workflow / 必要 issue`。
- issue 默认不是 runbook 的必备组成部分；只有当 issue 承载长期 operator 风险或准入条件时才进入引用区。
- runbook 默认写薄：回答“怎么跑、怎么查、怎么回滚、证据在哪”，而不是重写一遍演进史。

## Definitions（概念定义，可选）

- **top-level scope runbook**：按 `S2B`、`S2C`、`S2D` 这类顶层编号建立的主操作入口。
- **runbook stub**：在某个顶层 scope 已经值得建立 runbook，但内容仍需逐步收敛时，用来管理“是否建立、怎么建立、引用哪些材料”的薄主 log。
- **operator workflow**：真实执行者会重复使用的操作面，例如重建、回填、drill、shadow verify、hard gate、cutover、rollback、排障。
- **material sprawl**：同一主题下 log、issue、ADR、lab 过多，若直接全部塞进 runbook，会导致 runbook 退化为第二份 SoT。

## Constraints（约束）

- 不允许为了“资料很多”就为每个子 log、每个 issue 建 runbook。
- 不允许让 runbook 变成全集索引或第二份 roadmap。
- runbook 必须服务真实操作，而不是仅服务叙事归档。
- 已有稳定 runbook 的 scope，不应再平行新增多个竞争入口，除非真的形成独立长期操作面。

## Scope（本 log 范围）

- `P0`：contract（runbook 建立条件、命名规则、引用筛选规则）
- `P1`：实现（把“按顶层 scope 收敛 runbook”的策略写成稳定规则）
- `P2`：inventory/curation（给现有顶层 scope 判断“该建 / 暂不建 / 已有即可”）
- `P3`：adoption（后续新增顶层 runbook 时复用该策略，而不是重新发明口径）

## Success Criteria（DoD）

- 明确规定 runbook 的建立条件，不再依赖临时感觉判断。
- 明确规定 runbook 与 log / issue / adr / lab 的边界，避免 runbook 漂移为第二份 SoT。
- 明确规定顶层 scope 优先的命名与组织方式，使后续 `run-S<scope>-...` 能继续扩展而不失控。
- 给出现有 scope 的筛选规则：哪些该有主 runbook，哪些暂时不该有。
- 本 log 自身可以作为后续新增 runbook 的引用入口，而不是一次性讨论记录。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - 已固化 runbook 的建立条件与默认决策；
  - 已明确“按顶层 scope 收敛 runbook，而不是按每个 log/issue 拆散”；
  - 后续新增 runbook 时可直接复用本 log 的 contract，不必再重开一轮规则讨论。

## P0（Contract｜v1）

### P0-C1-S1（runbook 建立条件｜v1）

- 一个顶层 scope 满足以下任意两条时，应优先建立主 runbook：
  - 已有稳定入口脚本、CLI、GitHub Actions 或 workflow dispatch；
  - 已有重复执行价值，例如重建、回填、对账、切换、回滚、排障；
  - 未来执行者会频繁问“这条线现在怎么跑”；
  - 需要从 logs/labs/issues 中收敛出一个 operator 视角入口。
- 若仅有设计讨论、实验记录或一次性修复，而没有稳定 operator workflow，则不应急着建 runbook。

### P0-C1-S2（runbook 命名与收敛规则｜v1）

- runbook 优先按顶层 scope 命名：`run-S<scope>-<summary>.md`。
- 一个顶层 scope 默认只有一个主 runbook 入口；若未来出现独立长期操作面，再拆成子 runbook。
- runbook 引用材料默认控制在 3 到 7 项：
  - `parent log`
  - 1 到 2 个核心 phase logs
  - 1 个 ADR
  - 1 个 lab 或 workflow
  - 必要时 1 个 issue

### P0-C1-S3（runbook 与 log/issue 边界｜v1）

- runbook 负责：
  - 目的
  - 覆盖范围
  - one-click / local operation
  - evidence bundle
  - troubleshooting
  - rollback / next boundary
- log 负责演进、决策、phase closure、证据入账。
- issue 负责问题、待办、准入、阻塞，不默认进入 runbook。
- ADR 负责“为什么这么做”，只作为 runbook 的少量 reference，不替代操作步骤。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。

**Branch 约定**:

- `S0D-3A` 这类 docs/workflow/runbook-curation 改动优先落在 `S0D-*` 系列分支上推进。
- 如果后续一次 PR 同时包含“某条业务 runbook 的具体内容”和“S0D-3A 的规则调整”，建议拆分，避免规则变更和业务操作内容耦合。

**Commit 纪律（建议）**:

- 新增某条顶层 runbook 时，优先与对应 scope 的 log/ADR/lab 更新分开提交：
  - 一条提交固化 runbook 本体；
  - 必要时另一条提交只补引用、索引或 Evidence 入账。

## Plan（draft）

### P1（实现：runbook stub 规则）

- P1-C1-S1：把“按顶层 scope 收敛 runbook，而不是按每个 log/issue 逐个建 runbook”的规则固化为 `S0D-3A`。
- P1-C1-S2：定义 runbook 的建立条件、默认命名、引用筛选规则。

### P2（inventory / curation）

- P2-C1-S1：现有 scope 采用以下默认判断：
  - `S2B / S2C / S2D / S3A`：已有明确 operator workflow，应保留或继续演进主 runbook；
  - `S5A / S5B / S6A`：若已形成稳定 drills、hard gates、operator entry，应优先补顶层 runbook；
  - `S0`：仅在 docs/tooling 主题本身形成长期执行入口时才需要 runbook，不因资料多而自动建立。
- P2-C1-S2：未来新增 scope 时，先做“是否已形成 operator workflow”的判断，再决定是否升格为 runbook。

### P3（adoption）

- P3-C1-S1：后续新增 runbook 时，以 `S0D-3A` 作为统一策略引用入口。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：runbook 建立条件固化
- [x] `P0-C1-S2`：runbook 命名与收敛规则固化
- [x] `P0-C1-S3`：runbook 与 log/issue 边界固化

### P1（实现：runbook stub 规则）

- [x] `P1-C1-S1`：顶层 scope 收敛规则写入主 log
- [x] `P1-C1-S2`：建立条件与引用筛选规则写入主 log

### P2（inventory / curation）

- [x] `P2-C1-S1`：现有 scope 的默认 runbook 判断写明
- [x] `P2-C1-S2`：未来 scope 的升级判断写明

### P3（adoption）

- [ ] `P3-C1-S1`：按该策略继续补 `S5A / S5B / S6A` 等值得存在的顶层 runbook

## Evidence（预留）

- Evidence 以 repo 内已存在 runbook 与本 log 的规则为事实源；本 log 记录：`headSha + 参考 runbook + 默认判断`。

### P1-C1-S1S2（runbook stub 策略固化｜2026-03-13）

- headSha：`3d27f299a4670a86936e7e01078197a9a7ee33eb`
- artifacts：
  - `docs/logs/log-S0D-3A-runbook-stub.md`
- 期望（expected）：
  - 把 runbook 的建立条件与顶层收敛策略写成稳定规则；
  - 回答“是否要把所有 log / issue 都用上”的问题。
- 观测（observed）：
  - 已明确 runbook 采用顶层 scope 优先；
  - 已明确 runbook 不等于全集索引，也不要求所有 log / issue 全部纳入；
  - 已明确 issue 默认不是 runbook 的必备组成部分。

### P2-C1-S1（现有 runbook 样本对照｜2026-03-13）

- headSha：`3d27f299a4670a86936e7e01078197a9a7ee33eb`
- artifacts：
  - `docs/runbook/run-S2B-projection-table-merge.md`
  - `docs/runbook/run-S2C-projection-framework-platformization.md`
  - `docs/runbook/run-S2D-projection-onboarding-hard-gates.md`
- 期望（expected）：
  - 用现有 runbook 样本证明“顶层 scope 主 runbook”在本仓库里已可行。
- 观测（observed）：
  - `S2B / S2C / S2D` 均已采用顶层 scope runbook 形式，说明该策略与现有仓库组织一致；
  - `S0D-3A` 只是在此基础上把判断标准显式化、模板化。

## Recent changes（for traceability，可选）

- 2026-03-13：基于对现有 `S2B / S2C / S2D` runbook 样本的梳理，正式把“runbook 只在顶层 scope 形成 operator workflow 时建立”的规则固化为 `S0D-3A`。
- 2026-03-13：明确回答 runbook 不应吞并所有 log 和 issue，避免 runbook 漂移为第二份 SoT。