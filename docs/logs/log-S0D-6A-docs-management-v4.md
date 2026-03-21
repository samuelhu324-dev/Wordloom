# log-S0D-6A-docs-management-v4（Docs Management v4：logs + drills/evidence + runbooks + UI + packing + roadmap/demo）

---

**id**: `S0D-6A-docs-management-v4`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `Docs management v4（log/drills/runbook/UI/packing/roadmap+demo spine）`
**status**: `stable`           # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Tooling, Evidence, epic/s0, sub/6a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: ``
  **reference_log_1**: `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  **reference_log_2**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  **reference_log_3**: `docs/logs/log-S0D-3A-runbook-stub.md`
  **reference_log_4**: `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
  **reference_log_5**: `docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
  **reference_log_6**: `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome（结论区）

**Decision**:

- 将 S0D 这一层的 docs/tooling/evidence 工作收口为一条 "docs management v4" 主脊柱：从 log 组织方式、drills/evidence 自动化、runbook 收敛、UI 轻轨、drills evidence packing、一致化的 roadmap/demo 容器，形成可以长期复用的管理框架。
- 明确 parent epic `S0D-6A-docs-management-v4` 与六个子 phase logs（S0D-1A…S0D-6A）之间的边界：epic 负责目标、约束、切片与整体 DoD；子 logs 负责各自子领域的 contract / implementation / drills / closure。
- 对外暴露一套稳定的编号与 commit 纪律（基于 `P<phase>-C<cycle>-S<step>`），让 logs、artifacts、CI runs 和 demo/roadmap 之间形成可机械追溯的证据链。

**Default choices（默认基线 / v1）**:

- S0D 顶层只维护一个 docs-management epic：`log-S0D-6A-docs-management-v4`；所有子 logs 通过 `id = S0D-<n>A` 与 tags 中的 `epic/s0` 建立从属关系。
- 子 logs 各自负责一个清晰的子主题：
  - S0D-1A：log entries orchestration（主 log + 子 log 模板与闭环）；
  - S0D-2A：drills/evidence 自动化结构（run_dir 发现 + write_gate 汇总）；
  - S0D-3A：runbook stub 策略（按顶层 scope 收敛 runbook 入口）；
  - S0D-4A：UI evidence-lite 轻轨（前端分层证据链与 note 模板）；
  - S0D-5A：drills evidence packing 统一（单场景 minimal / failure full bundle 规则）；
  - S0D-6A：structured roadmap + demo 容器（road-Sx 与 demo-001 等）。
- parent epic 不重复描述实现细节，只维护：
  - S0D-1A…S0D-6A 的定位与边界；
  - 横切约束（编号、commit/branch、artifacts/stability 口径）；
  - 顶层 Execution Checklist 与当前整体进度摘要。

**Non-goals（不做什么）**:

- 不在本 epic 中引入新的领域级 drill / hard gate 设计（例如 S5B 安全治理或 S6A evidence drills 本身的业务 contract），这些继续由各自 scope 的 epic 负责。
- 不把所有 docs 与 UI 问题强行拉入统一的重型流程；对前端/文档的小修小补仍允许轻量处理，只在满足升级条件时进入 S0D 体系。

## Background（背景）

- 随着仓库中 logs / labs / runbooks / UI notes / workflows 持续增加，单独围绕某个主题的 logs（例如 S6A 或 S5B）已经有比较稳定的演进轨迹，但 docs/automation 本身仍容易出现：入口分散、命名漂移、证据链不容易统一回顾的问题。
- 早期版本的 docs management 更偏向一次性整理（v1~v3），缺少一个贯穿 log 结构、drills 自动化、runbook 收敛、前端/UI 轻轨、打包与 roadmap/demo 整体故事的“docs meta 层 epic”。
- 因此需要以 S0D 为 scope，集中固定一条 docs-management 主脊柱：通过 6 个子 phase log 把各个子主题做成可复制的模式，并用本 epic 负责总览与 DoD。 

## Constraints（约束）

- epic 自身保持薄：不复制子 log 的长篇合同与样例，只给必要的 summary 与 cross-link，保证读者 1 分钟内能理解结构与入口。
- S0D 只负责 docs / tooling / automation / UI 轻轨 / roadmap+demo 这类“支撑层”，不负责具体业务 domain 的 contract；业务 epic（例如 S5B / S6A）只在需要时引用 S0D 的规则。
- 编号与 commit 纪律必须保持与 S0D 子 logs 一致：
  - `P` 表示 phase，`C` 表示 cycle，`S` 表示 step；
  - commit/PR 命名遵循 `<ID>/P<phase>-C<cycle>-S<steps>: <summary>` 规则；
  - 多个 steps 合并只在同一 phase/cycle 内允许；跨 phase/cycle 的变更需要分开记账。

## Scope（本 log 范围）

- 本 log 负责：
  - 作为 `S0D` docs-management v4 的 parent epic，描述 6 个子 logs 的目标分工、横切约束和整体 DoD；
  - 对 S0D-1A…S0D-6A 的 Execution Checklist 做高层汇总，标记哪些子主题已经 stable，哪些仍可继续演进；
  - 为后续 S0D-7A+ 等新 phase 提供接入点，避免再新建平行 docs management epic。
- 本 log 不负责：
  - 重新落地具体模板 / scripts / workflows / UI notes / roadmap/demo 文件，这些仍由各自子 log 管理；
  - 描述单次 run evidence 细节或 CI 配置 YAML 内容。

## Success Criteria（DoD）

- 结构层面：
  - 读者在本 log 中能 30 秒内看懂：S0D-1A…S0D-6A 各自负责什么、当前状态（draft / stable）、以及它们之间如何拼成 docs-management v4。
  - 本 log 的 links 与 reference_log_* 能导航到每个子 log 与关键模板（如 `_template-log-parent-epic-spine`、`_template-log-phase-drills-evidence`）。
- 工程与证据层面：
  - 至少 5/6 个子 logs 处于 `stable`，并各自有一条以上 evidence 记账条目（headSha + artifacts/run_dir/CI URL 等）。
  - S0D 范围内的主要 docs/automation 入口（logs 模板、drills automation、runbook 规则、UI 轻轨、packing 规则、roadmap/demo 容器）均由某个子 log 明确承接，而不是悬空存在。
- 未来演进层面：
  - 当新增 docs/automation 主题时，优先评估是否可以以 `S0D-7A+` 子 log 的形式接入本 epic，而不是新建一个平行 epic，确保 docs-management 主脊柱不分叉。

## Phases（切片）

- `S0D-1A`（Phase 1）：log entries orchestration（主 log + 子 logs 闭环）
  - 详见：`docs/logs/log-S0D-1A-log-entries-orchestration.md`
- `S0D-2A`（Phase 2）：drills/evidence automation（run_dir 发现 + 汇总 JSON）
  - 详见：`docs/logs/log-S0D-2A-drills-evidence-automation.md`
- `S0D-3A`（Phase 3）：runbook stub strategy（按顶层 scope 收敛 runbook 入口）
  - 详见：`docs/logs/log-S0D-3A-runbook-stub.md`
- `S0D-4A`（Phase 4）：UI layered fix notes（前端轻轨证据链）
  - 详见：`docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
- `S0D-5A`（Phase 5）：drills evidence packing unification（minimal/full packing 合约）
  - 详见：`docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
- `S0D-6A`（Phase 6）：structured roadmap & demo containers（roadmap + demo 容器骨架）
  - 详见：`docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：S0D docs-management epic contract 与切片清单写清（本 log）
- [x] `P1`：S0D-1A：log entries orchestration 模板与闭环样本（S6A / S0D-5A）完成，并标记 stable
- [x] `P2`：S0D-2A：drills/evidence run_dir + 汇总 JSON 结构完成，并在 S5B-3A 上形成首条完整 hard gate 证据链
- [x] `P3`：S0D-3A：runbook stub 规则与现有 scope（S2B/S2C/S2D/S3A/S5B/S6A）筛选 snapshot 完成，并标记 stable
- [x] `P4`：S0D-4A：UI evidence-lite 轻轨规则、模板与首批样例入账完成（含 assets 规则），整体标记 stable
- [x] `P5`：S0D-5A：drills evidence packing 合约与 reusable runner 采纳完成，并在单场景 + matrix 路径上验证
- [x] `P6`：S0D-6A：structured roadmap + demo 容器骨架完成，并在 S1/S1-1 + demo-001 上落地

## Current Status（进展摘要）

- S0D docs-management v4 已经覆盖从 log 结构、drills/evidence 自动化、runbook 收敛、UI 轻轨、drills packing 到 roadmap/demo 容器的完整链路，6 个子 logs 均已标记为 stable。
- 后续演进重点从“建立规则与模板”转向“在更多 scope 中滚动采用这些规则”（例如更多 S2*/S5*/S6* 主题的 logs 与 runbooks、更多 demo-* 容器）。
- 未来若新增 S0D-7A+ 之类子 log，应在本 epic 的 Phases 与 Execution Checklist 中登记，避免 docs-management 入口分裂。

## Notes（落地原则）

- 新增任何 docs/tooling/automation 相关的规则类工作，优先评估是否应纳入 S0D scope：
  - 若是一次性修复/迁移，可作为其他 epic 的子 log；
  - 若是可复用的规则/模板/工作流，优先作为 `S0D-<n>A` 子 log 并在本 epic 中登记。
- 在描述 evidence 与 CI 行为时，继续沿用 S0D-2A/S0D-5A 的 contract：log 只记录 headSha + run_dir + artifacts 索引，详情交由 artifacts/CI 负责。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - S0D-1A…S0D-6A 至少 5 条为 `stable`，且各自 Execution Checklist 有实际 evidence 记账样本；
  - docs-management v4 的主脊柱结构（6 个子主题 + 编号/commit discipline + evidence 口径）不再大幅变更，只做增量补充；
  - 新增 docs/automation 主题可直接按本 epic 的 contract 接入，而不需要另起一套编号或规则。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`S0D-6A-docs-management-v4/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。
- Multi-step 规则：只允许在 **同一 Phase + 同一 Cycle** 下合并多个 step；一旦跨 Phase 或跨 Cycle，必须拆成多次 commit。

**Branch 约定（建议）**:

- S0D docs-management 相关改动优先在 `S0D-*` 系列分支上推进，例如 `S0D-docs-management-v4` 或简化为 `S0D`。
- 若一次演进同时涉及其他 scope（如 S5B/S6A）的业务内容与 S0D 的规则调整，建议拆成多条 PR：每条 PR 聚焦一个 scope/index，方便回溯 `scope → branch → commits → artifacts` 的证据链。

**Commit 纪律（建议）**:

- 对于归属于 S0D scope 的子 log（例如 `S0D-4A`、`S0D-6A`）：
  - 完成每个 `P*-C*-S*` 的关键内容后，应在 `S0D-*` 系列分支上及时 `commit/push`；
  - 仅当某个 phase 体量较大、需要多人协同时，才在顶层分支之下再建短生命周期子分支，避免碎片化；
  - 推荐节奏：按 `P*-C*-S*` 粒度在 scope 分支上积累小而清晰的 commit → 定期从这些 scope 分支向 `main` 发起 PR，并通过 Review/合并把证据链收口到主干。

## Recent changes（for traceability，可选）

- 2026-03-21：汇总 S0D-1A…S0D-6A 的结构与 DoD，建立 `log-S0D-6A-docs-management-v4.md` 作为 docs management v4 的主 epic，后续 docs/automation 规则统一归口到本 log。

## Evidence（reserved）

### P0-C1-S1（S0D docs-management epic established｜2026-03-21）

- headSha: `e14660d2c50ca9f452bd136086eda5a6229ce2eb`
- scope: `S0D`
- artifacts:
  - `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  - `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  - `docs/logs/log-S0D-3A-runbook-stub.md`
  - `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
  - `docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
  - `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`
  - `docs/logs/log-S0D-6A-docs-management-v4.md`
- expected:
  - S0D-1A…S0D-6A are all discoverable from this epic and each remains self-contained for its sub-scope.
  - docs-management v4 provides a stable parent spine for future S0D-* phase logs.
- observed:
  - 当前 headSha 对应的仓库状态已满足上述结构与 discoverability 要求，本 epic 标记为 stable。