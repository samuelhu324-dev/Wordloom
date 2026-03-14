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
  **reference_log_5**: `docs/runbook/_template-runbook.md`
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
- 总结当前仓库已有 runbook 的共同结构，并沉淀一份可直接复用的 `_template-runbook`。
- 追踪 `S5B / S6A` 主 log 与关键子 log，产出一份“该升格什么、不该升格什么”的 curations snapshot。
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

### P0-C2-S1（现有 runbook 共同骨架｜v1）

- 基于 `S2B / S2C / S2D / S3A` 现有样本，当前仓库里的 runbook 共同骨架已经足够稳定：
  - metadata header：`id / kind / title / status / scope / decision_date / context_issue / decision / supersedes`
  - body sections：`Purpose -> Scope -> Evidence Bundle -> One-click Automation(optional) -> Local Operation -> Troubleshooting -> Notes and Boundaries`
- 共同特征不是“写得一样长”，而是都遵守同一个 operator 视角：
  - 先给稳定入口；
  - 再给 evidence root；
  - 再给排障/边界；
  - 不把 phase 历史、细颗粒 contract、所有 artifacts 历史都搬进正文。
- 现有样本差异应被视为“厚薄差异”，而不是结构冲突：
  - `run-S2B-*` 更厚，因为它承担 cutover / rollback / shadow verify 等长期 operator 动作；
  - `run-S2C-*` 与 `run-S2D-*` 更薄，更接近后续模板的默认厚度；
  - `run-S3A-*` 说明当 one-click automation 已稳定时，可以把 GitHub Actions 直接纳入主 runbook，而不需要再拆一层 docs。

### P0-C2-S2（_template-runbook 文件｜v1）

- 复用模板路径：`docs/runbook/_template-runbook.md`
- 使用方式：
  - 仅在顶层 scope 已形成稳定 operator workflow 时复制此模板；
  - 默认保留 7 个核心段落，不足的就删，不额外发明新骨架；
  - 若某个 scope 还没有稳定 one-click 入口，就删除 `One-click Automation` 段，而不是写空段落；
  - 若某个 phase 只是 contract / implementation / evidence 子材料，则把它保留在 links 或 `Scope` 引用中，不单独升格为 runbook。

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

### P2-C2-S1（S5B / S6A curations snapshot｜2026-03-13）

- `S5B`：应补 1 个顶层 runbook stub，不应按 `1A / 2A / 3A / 4A` 再拆 4 个子 runbook。
  - 推荐文件：`docs/runbook/run-S5B-security-governance-hard-gates.md`
  - operator 入口应聚焦：policy/audit hard gates、本地或 CI 触发入口、evidence ledger、deny reason drift 排障。
- `S6A`：应补 1 个顶层 runbook stub，但文件名必须与对应顶层 log `log-S6A-evidence-drills-spine.md` 对齐，而不是另起 summary 名称。
  - 推荐文件：`docs/runbook/run-S6A-evidence-drills-spine.md`
  - operator 入口应聚焦：fault suite run/verify/export、evidence JSON、stable entry、reason contract、hard-gate failure triage。
- `S5B-1A / 2A / 3A / 4A`：本轮不建议各自独立升格 runbook。
- `S6A-1A / 2A / 3A / 4A`：本轮不建议各自独立升格 runbook。

### P2-C2-S2（S5B：为什么已经值得升格顶层 runbook）

- `log-S5B-security-governance-hard-gates` 已经不是纯叙事 spine，而是稳定 operator 主题索引：定义了默认基线、phase 拆分、DoD、evidence 纪律与 hard-gate 入口。
- `S5B-1A` 提供了 drills/verifier/evidence contract，是主 runbook 的 contract 基底。
- `S5B-2A` 主要是 implementation consolidation，适合继续作为 reference log，而不是独立 operator 入口。
- `S5B-3A` 已经显式固化 operator workflow（查询、回放、取证），它应成为未来 `run-S5B-*` 的核心引用材料之一。
- `S5B-4A` 让 search authorization 进入同一 hard-gate 家族，说明 `S5B` 已不再是单一 demo phase，而是可复跑的 security/governance gate 主题。
- 结论：`S5B` 现在缺的不是更多 phase log，而是一个更薄的 operator 入口，把“怎么跑、证据在哪、先查什么”收口起来。

### P2-C2-S3（S6A：为什么已经值得升格顶层 runbook）

- `log-S6A-evidence-drills-spine` 虽名为 spine，但其子 log 已经围绕同一 operator workflow 闭环：稳定入口、统一供给、reason contract、hard-gate artifacts。
- `S6A-1A` 解决的是 stable entry，属于 runbook 的 prerequisites 和 troubleshooting 基底。
- `S6A-2A` 解决的是 supply creation contract，属于 operator 执行前必须知道的 supply/evidence 规则。
- `S6A-3A` 解决的是 reason contract，属于 verify 与 triage 的核心判定口径。
- `S6A-4A` 已经把 hard-gate + evidence JSON 产品化，说明 `S6A` 具备非常明确的 runbook 主体。
- 结论：`S6A` 适合补一份“执行入口型” runbook，把 `run -> verify -> export -> inspect evidence` 作为主路径，而不是继续只靠 spine log 导航。

### P3（adoption）

- P3-C1-S1：后续新增 runbook 时，以 `S0D-3A` 作为统一策略引用入口。

### P3-C2-S1（命名一致性与 legacy runbook 收敛｜2026-03-13）

- 这次收敛属于 `S0D-3A` 的 adoption 扩展，因此记为 **新 cycle，不开新 phase**：
  - `P3` 没变，因为问题域仍然是 runbook strategy 的 adoption；
  - 新增的是 `C2`，因为现在做的是“把策略落实到既有 runbook 和新 runbook 命名”这一轮落地。
- 规则收紧如下：
  - runbook 文件名中的 summary suffix，必须与对应顶层 log 文件名中的 summary suffix 一致；
  - 例如 `log-S5B-security-governance-hard-gates.md` 对应 `run-S5B-security-governance-hard-gates.md`；
  - 例如 `log-S6A-evidence-drills-spine.md` 对应 `run-S6A-evidence-drills-spine.md`；
  - 旧 runbook 若使用了历史性 summary（如 `docs-management-v3`、`observability-v2`），应逐步迁到与当前主 log 对齐的新名字，并在必要时把旧文件视为 superseded。

### P3-C3-S1（runbook 排障有效性验证 contract｜2026-03-13）

- runbook 是否“有用”，不以段落是否齐全判断，而以它能否把 operator 从问题带到明确下一步判断。
- 每条候选主 runbook 在从 `draft` 走向可依赖状态前，至少要完成以下 3 类验证中的 2 类，且必须包含 `known failure`：
  - `happy path`：操作者能从 runbook 找到正确入口、拿到真实 evidence，并确认一条成功样例；
  - `known failure`：操作者能用 runbook 把已知失败快速归类，而不是直接掉进源码排查；
  - `ambiguity / stale evidence / CI-only evidence`：操作者遇到“文档提到的 run 不在本地”、“证据只在 CI artifact bundle 内”或“现象跨 phase 边界”时，runbook 能给出正确的分流目标。
- 固定验证记录字段如下：
  - `entry found`：是否能从 runbook 直接找到正确 suite / workflow / 本地命令；
  - `evidence found`：是否能定位到 run directory、ledger、或明确说明“此 phase 无 ledger”；
  - `failure classified`：是否能在 `_result.json` / verifier / ledger 层面先完成归类；
  - `next action clear`：是否给出下一步该查哪个 phase、哪个文件、哪类 evidence；
  - `wrong-turn count`：是否在进入源码前就完成上述判断，目标是低 wrong-turn。
- 若 runbook 只能告诉操作者“去看代码”而不能先完成 evidence 定位与失败归类，则该 runbook 仍然是装饰性文档，不算通过验证。

### P3-C3-S2（S5B 样例验证基线｜2026-03-13）

- `run-S5B-security-governance-hard-gates` 作为首个 validation sample，采用以下三路样例：
  - `happy path`：`S5B-2A` 绿色样例 `docs/labs/_snapshot/auto/S5B-2A/bookshelf_delete_entrypoint/7e464272-8352-41b6-b655-b5077597edfe`
  - `known failure`：`S5B-3A` 红色样例 `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/9d3cdfc1-2fb0-43c8-8364-a00b5db4e87e`
  - `ambiguity / stale evidence`：历史上提到但当前工作区缺失的 `S5B-3A` run dir `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/16b34278-d370-4be4-9e8f-29a455e25111`
- 该样例的目的不是证明所有 `S5B` phase 都永远为绿，而是证明这份 runbook 能在 `green / red / missing evidence` 三种常见操作面下给出不同且正确的第一判断。

### P3-C3-S3（S6A 样例验证基线｜2026-03-14）

- `run-S6A-evidence-drills-spine` 作为第二个 validation sample，采用以下三路样例：
  - `happy path`：`S6A-2A` 绿色样例 `docs/labs/_snapshot/auto/S3A-2A-3A/es_down_connect/S6A-2A-P1-C2-S1`
  - `known failure`：`S6A-1A` 红色样例 `docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/20260304T195127`
  - `ambiguity / CI-only evidence`：本地缺失但已在 CI artifact bundle 中存在的 `es_timeout` run `artifacts/_tmp_ci_run_22746408022/labs-evidence-fault_obs_infra_es_timeout-22746408022-1-fault_obs_infra_es_timeout-r1/S3A-2A-3A/es_timeout/22746408022-1-fault_obs_infra_es_timeout-r1`
- 该样例的目的不是证明 `S6A` 每个 fault scenario 都要在本地保留完整快照，而是证明 runbook 能区分“本地 green / 本地 red / 仅存在于 CI bundle 的 green evidence”三种操作面。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：runbook 建立条件固化
- [x] `P0-C1-S2`：runbook 命名与收敛规则固化
- [x] `P0-C1-S3`：runbook 与 log/issue 边界固化
- [x] `P0-C2-S1`：现有 runbook 共同骨架总结
- [x] `P0-C2-S2`：`_template-runbook` 模板落地

### P1（实现：runbook stub 规则）

- [x] `P1-C1-S1`：顶层 scope 收敛规则写入主 log
- [x] `P1-C1-S2`：建立条件与引用筛选规则写入主 log

### P2（inventory / curation）

- [x] `P2-C1-S1`：现有 scope 的默认 runbook 判断写明
- [x] `P2-C1-S2`：未来 scope 的升级判断写明
- [x] `P2-C2-S1`：`S5B / S6A` 顶层 runbook 候选清单完成
- [x] `P2-C2-S2`：`S5B` 候选判断依据完成
- [x] `P2-C2-S3`：`S6A` 候选判断依据完成

### P3（adoption）

- [ ] `P3-C1-S1`：按该策略继续补 `S5A / S5B / S6A` 等值得存在的顶层 runbook
- [x] `P3-C2-S1`：runbook suffix 与对应顶层 log suffix 的命名一致性规则落地
- [x] `P3-C2-S2`：legacy runbook（`S0C / S3A`）按当前主 log 名称收敛
- [x] `P3-C2-S3`：`S5B / S6A` 顶层 runbook stub 落地
- [x] `P3-C3-S1`：runbook 排障有效性验证 contract 固化
- [x] `P3-C3-S2`：`run-S5B` 样例验证路径固化
- [x] `P3-C3-S3`：`run-S6A` 样例验证路径固化

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

### P0-C2-S1S2 / P2-C2-S1S2S3（结构模板与候选梳理｜2026-03-13）

- artifacts：
  - `docs/runbook/_template-runbook.md`
  - `docs/logs/log-S0D-3A-runbook-stub.md`
- 期望（expected）：
  - 把现有 runbook 的共同骨架总结出来，而不是每次新写 runbook 都重新发明结构；
  - 只做 `S5B / S6A` 的 runbook 升格梳理，不提前生成厚 runbook。
- 观测（observed）：
  - 已形成统一模板：metadata + Purpose + Scope + Evidence Bundle + One-click Automation(optional) + Local Operation + Troubleshooting + Notes and Boundaries；
  - 已明确 `S5B / S6A` 都值得补顶层 runbook stub；
  - 已明确本轮不建议把 `S5B-*` 或 `S6A-*` 子 phase 进一步拆成一组平行 runbook。

### P3-C2-S1S2S3（命名一致性与 stub adoption｜2026-03-13）

- artifacts：
  - `docs/runbook/run-S0C-scenarios-taxonomy.md`
  - `docs/runbook/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/runbook/run-S5B-security-governance-hard-gates.md`
  - `docs/runbook/run-S6A-evidence-drills-spine.md`
- 期望（expected）：
  - 让旧 runbook 向当前骨架和命名规则收敛；
  - 把 `S5B / S6A` 顶层 runbook 先以薄 stub 的方式真正落地；
  - 明确这是一轮 adoption cycle，而不是新的 strategy phase。
- 观测（observed）：
  - `S0C / S3A` 旧 runbook 已改为与对应主 log suffix 对齐；
  - `S5B / S6A` 顶层 runbook 已按顶层 log 名称落地；
  - `S0D-3A` 已明确：本轮记为 `P3-C2`，不新开 phase。

### P3-C3-S1S2（runbook 排障验证 contract + S5B 样例｜2026-03-13）

- artifacts：
  - `docs/logs/log-S0D-3A-runbook-stub.md`
  - `docs/runbook/run-S5B-security-governance-hard-gates.md`
  - `docs/labs/_snapshot/auto/S5B-2A/bookshelf_delete_entrypoint/7e464272-8352-41b6-b655-b5077597edfe/_result.json`
  - `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/332361bc-3bb1-4d99-862c-a40d586190db/_result.json`
  - `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/9d3cdfc1-2fb0-43c8-8364-a00b5db4e87e/_result.json`
  - `artifacts/s5b3a-runs.json`
- 期望（expected）：
  - 把“runbook 是否有排障价值”从主观看法改成固定验证合同；
  - 用 `run-S5B` 证明 operator 能区分绿色成功、contract-ok 但红、以及 stale evidence path。
- 观测（observed）：
  - `S5B-2A` 绿色样例可从 runbook 直接定位到 suite 与 run dir，且 verifier 返回 `[contract_ok]`；
  - `S5B-3A` 绿色样例 `332361bc-3bb1-4d99-862c-a40d586190db` 的 `_result.json.ok=true`，证明 `happy path` 在本地可复查；
  - `S5B-3A` 红色样例 `9d3cdfc1-2fb0-43c8-8364-a00b5db4e87e` 同时满足 `contract_ok=true` 与 `result_ok=false`，说明 runbook 的第一步应是先看 `failure_reason`，而不是先怀疑 artifact contract；
  - 缺失目录 `16b34278-d370-4be4-9e8f-29a455e25111` 会被 verifier 归类为 `missing_run_dir`，证明 stale evidence path 需要单独分流，而不是与测试失败混为一谈。

### P3-C3-S3（runbook 排障验证样例 + S6A｜2026-03-14）

- artifacts：
  - `docs/logs/log-S0D-3A-runbook-stub.md`
  - `docs/runbook/run-S6A-evidence-drills-spine.md`
  - `docs/labs/_snapshot/auto/S3A-2A-3A/es_down_connect/S6A-2A-P1-C2-S1/_result.json`
  - `docs/labs/_snapshot/auto/S3A-2A-3A/es_timeout/s6a3a-p3c5s4-20260305-211200/_result.json`
  - `docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/20260304T195127/_result.json`
  - `artifacts/_tmp_ci_run_22746408022/labs-evidence-fault_obs_infra_es_timeout-22746408022-1-fault_obs_infra_es_timeout-r1/S3A-2A-3A/es_timeout/22746408022-1-fault_obs_infra_es_timeout-r1/_result.json`
- 期望（expected）：
  - 证明 `run-S6A` 不依赖独立 ledger，也能把 operator 正确带到 local snapshot、phase contract、或 CI bundle；
  - 证明 `S6A` 的第三类分支应归类为 `CI-only evidence`，而不是一概按 stale failure 处理。
- 观测（observed）：
  - `S6A-2A` 绿色样例 `S6A-2A-P1-C2-S1` 的 `_result.json` 同时给出 `supply_db_check.ok=true` 与 `ok=true`，说明 runbook 可先在 supply 层完成 happy-path 确认；
  - `S6A-3A` 绿色样例 `s6a3a-p3c5s4-20260305-211200` 的 `_result.json` 给出 `db_reasons=[es_timeout]`、family=`timeout` 且 `ok=true`，说明 runbook 可先在 reason contract 层完成 happy-path 确认；
  - `S6A-1A` 红色样例 `20260304T195127` 的 `_result.json.ok=false` 且 metrics delta 全为 `0`，说明 runbook 应先分流到 stable-entry / trigger-path，而不是直接怀疑 reason taxonomy；
  - 本地不存在 `docs/labs/_snapshot/auto/S3A-2A-3A/es_timeout/22746408022-1-fault_obs_infra_es_timeout-r1`，但 CI bundle 中存在对应 `_result.json.ok=true`，说明 `CI-only evidence` 是独立且常见的 operator 分支。

## Recent changes（for traceability，可选）

- 2026-03-13：基于对现有 `S2B / S2C / S2D` runbook 样本的梳理，正式把“runbook 只在顶层 scope 形成 operator workflow 时建立”的规则固化为 `S0D-3A`。
- 2026-03-13：明确回答 runbook 不应吞并所有 log 和 issue，避免 runbook 漂移为第二份 SoT。
- 2026-03-13：补充现有 runbook 共同骨架总结，并新增 `docs/runbook/_template-runbook.md` 作为薄 runbook 模板。
- 2026-03-13：补充 `S5B / S6A` runbook 候选梳理，明确“顶层 runbook 应补，子 phase runbook 暂不补”。
- 2026-03-13：把“runbook suffix 必须与对应顶层 log suffix 一致”的规则写入 adoption cycle，并将 `S0C / S3A` 旧 runbook 与 `S5B / S6A` 新 runbook 一并收敛到该规则。
- 2026-03-13：新增 runbook 排障有效性验证 contract，并用 `run-S5B` 固化 `happy path / known failure / stale evidence` 三路样例。
- 2026-03-14：把 `CI-only evidence` 纳入第三类验证分支，并用 `run-S6A` 固化 `local green / local red / CI-only green` 三路样例。