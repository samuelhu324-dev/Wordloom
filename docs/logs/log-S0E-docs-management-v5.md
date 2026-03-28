# log-S0E（Docs Management v5：structured logs → semi-automated Git issue creation）

---

**id**: `S0E-docs-management-v5`
**kind**: `log`
**title**: `docs management v5 (structured logs → semi-automated Git issue creation) v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/draft.md`
  **reference_log_1**: `docs/logs/log-S0D-6A-docs-management-v4.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **phase_log_1**: ``
  **phase_log_2**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **phase_log_3**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **phase_log_4**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
**created**: `2026-03-28`
**updated**: `2026-03-28`

---

## Decision / Outcome（结论区）

**Decision**:

- 启动 `S0E` 作为 `S0` 下承接 docs-management v5 的新 spine，专门处理 `structured logs -> Git issues` 的半自动化创建与分类 contract。
- v1 先把 issue title、label taxonomy、body scaffold、milestone mapping 与 log frontmatter 的关系收口为统一合同，再决定是否进入脚本化或 GitHub-side automation implementation。

**Default choices（默认基线 / v1）**:

- issue creation 默认走“半自动化”路线，而不是一步到位的全文自动总结；
- `SxY-ZA` 与 `<specific subject>` 优先复用既有 log 资产，自动化重点放在 `<fixed-keyword>`、labels、body scaffold 与 structured mapping；
- GitHub labels 必须先有受控词表和预创建集合；automation 不负责在运行时临时发明新 label。

**Non-goals（不做什么）**:

- v1 不做自由文本总结自动生成；`Context` / `DoD` 仍保留人工确认；
- v1 不把 module labels 或 priority labels 强行做成 full-automation；
- v1 不直接改写所有历史 logs/issues，只先固定新 issue 的 contract 和 rollout path。

## Background（背景）

- 当前 issue/log 命名已经形成稳定的 `SxY-ZA` 编号，但 title 前缀词、labels 与 body scaffold 仍有较多临时命名和人工变体；
- 既有 structured logs 已经提供了较强的可复用输入面：scope/id/title/tags/links/runbook/parent-log 等字段都可以为 issue scaffold 提供稳定来源；
- 如果不先收口 contract，直接做自动化会把当前的命名漂移、label 漂移与 milestone 不一致问题固化为脚本行为。

## Constraints（约束）

- 先收口 vocabulary / mapping / labels taxonomy，再进入实现；
- 允许“full-automation / semi-automation / zero-automation”三种自动化等级共存，不追求所有字段同一强度；
- labels 和 milestone 的映射必须是受控、可追溯、低歧义的；
- issue scaffold 不替代 log 本身，log 仍是主事实源。

## Scope（本 log 范围）

- 本 log 负责：
  - 定义 `S0E` 的目标边界、默认基线与 phase 拆分；
  - 统一 `log -> issue` 的命名、labels、body scaffold、milestone mapping 方向；
  - 作为后续脚本化/模板化/自动化入口的 parent spine。
- 本 log 不负责：
  - 立即实现 issue creation script 或 GitHub Actions workflow；
  - 回填和重命名所有历史 issue；
  - 自动判定实际代码改动范围对应的全部 module labels。

## Success Criteria（DoD）

- 结构层面：
  - 读者能在 30 秒内理解 `S0E` 解决什么问题、哪些字段可自动、哪些字段必须人工确认；
  - `S0E-2A` 能作为 title/labels/body/milestone contract 的稳定入口。
- 工程层面：
  - 至少固定一版 title keyword controlled vocabulary；
  - 至少固定一版 labels taxonomy 与 automation-level matrix；
  - 至少固定一版 log frontmatter -> issue fields mapping。
- 证据层面：
  - 后续每个 phase 至少能留下可追溯 sample（代表性 log 输入 + issue scaffold 输出）。

## Phases（切片）

- `S0E-2A`（Phase 2）：Semi-automated Git issue creation contract（title keywords, labels, body scaffold, milestone mapping）
  - 详见：`docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
- `S0E-2B`（Phase 2B）：real GitHub issue creation automation / scripting path
  - 详见：`docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- `S0E-2C`（Phase 2C）：batch issue creation, parent-child linking, and milestone/backfill tooling
  - 详见：`docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：parent spine created and scope boundary fixed
- [x] `P1`：`S0E-2A` scaffolded as the first issue-automation contract phase
- [x] `P2`：issue-aware fields added to log templates
- [x] `P3`：representative scaffold generation path validated and manual creation / future script contract fixed
- [x] `P4`：`S0E-2B` 已建立并完成 `P0`（mode boundary / script IO / creation evidence contract）
- [x] `P5`：`S0E-2B` 已完成 `P1`（local draft-generation implementation + structured result output）
- [x] `P6`：`S0E-2B` 已完成 `P2`（explicit create mode + first real GitHub issue creation）
- [x] `P7`：`S0E-2B` 已完成 `P3`（real-run verification + write-back discipline），并通过同一路径创建了 `S0E-2A` 的真实 issue
- [x] `P8`：`S0E-2C` 已建立，用于承接批量创建、关系补链和 milestone/backfill tooling 的 follow-up scope
- [x] `P9`：`S0E-2C` 已完成 `P2-C1-S1`，把 parent-child linking 的显式输入 contract 收口为稳定 manifest 形状
- [x] `P10`：`S0E-2C` 已完成 `P2-C1-S2`，relationship dry-run 已验证 planned / skipped / error / reconciliation 语义
- [x] `P11`：`S0E-2C` 已完成 `P3`，milestone/write-back reconciliation contract 与 dry-run 都已验证

## Current Status（进展摘要）

- `S0E` 现阶段仍是 `draft`，重点是把 contract 先讲清楚，而不是抢先实现；
- `S0E-2A` 已完成 title keyword、labels taxonomy、body scaffold 与 milestone mapping 的第一轮收口，并把 issue-aware template fields 落到 parent/phase templates；
- `S0E-2A` 已完成第一条自举式 sample、`S4E-5B` / `S6A-4A` 两条 cross-log validation，以及 `P3` 的最小人工创建流程和 future script entry contract；
- `S0E-2B` 已建立并完成 `P0`，明确真正的 GitHub issue 自动创建必须以 `draft-generation` 为默认模式、以 `--create` 为显式 opt-in，并继承 fail-closed contract；
- `S0E-2B` 已完成 `P1`：本地 `log_path -> docs/issues/*.md` draft-generation 脚本和 JSON sidecar 已跑通，下一步应进入 `P2` 的真实 GitHub create issue 入口；
- `S0E-2B` 已完成 `P2`：脚本已通过 `gh` prerequisite checks 成功创建真实 issue `#288`，下一步应进入 `P3` 去验证 write-back discipline，并决定是否继续用同一路径创建 `S0E-2A` 的真实 issue；
- `S0E-2B` 已完成 `P3`：真实 create path 与 write-back discipline 都已验证，`S0E-2A` 的真实 issue `#289` 也已通过同一路径创建并回写到 source log；
- `S0E-2C` 已建立为后续 slice，专门处理单条 issue creation 之后的批量化、关系补链与历史回填；
- `S0E-2C` 已完成 `P2-C1-S1`：parent-child linking 现在只接受显式 issue number / URL 作为关系输入，`log_path` 仅保留为 traceability 字段；
- `S0E-2C` 已完成 `P2-C1-S2`：relationship dry-run 现在可以只读 manifest 并输出 `planned / skipped / error / reconciliation` 四类结果，未引入任何 apply 行为；
- `S0E-2C` 已完成 `P3`：milestone/write-back reconciliation 现在也有明确 contract 和 dry-run 规划器，仍然没有引入 apply 行为；
- 当前最大风险不是“不会写脚本”，而是如果在 contract 未稳定时过早自动化，会把现有命名漂移固化下来。

## Notes（落地原则，可选）

- structured log remains the SoT; issue scaffold is a derived operator/workflow artifact;
- parent issue / child issue / labels taxonomy 应尽量采用受控词表，而不是临时词语；
- automation first solves structure, not summary quality.

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - `S0E` 的 phase 拆分、字段边界与自动化强度分层已稳定；
  - 至少一条可重复的 `log -> issue scaffold` sample path 已被验证。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`S0E-docs-management-v5/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。
  - Multi-step 规则：只允许在同一 Phase + 同一 Cycle 下合并多个 step；一旦跨 Phase 或跨 Cycle，必须拆成多次 commit。

**Branch 约定（建议）**:

- `S0E` 相关改动默认落在 `S0E-*` 顶层工作分支，例如 `S0E-docs-management-v5`；
- 若后续实现拆成 template rollout 与 generator validation 两条并行路径，可在 `S0E-*` 之下临时开短生命周期分支，但默认不为每个子 log 再开常驻顶层分支。

**Commit 纪律（建议）**:

- 完成每个 `P*-C*-S*` 的关键内容后，应在 `S0E-*` 分支上及时 `commit/push`；
- 推荐节奏：先把 contract、template、validation 按 step 粒度切成小 commit，再从 `S0E-*` 分支向 `main` 发起 PR。

## Recent changes（for traceability，可选）

- 2026-03-28：首次创建 `S0E` spine，用于承接 docs-management v5 中的 issue scaffold / taxonomy / structured mapping 主题。
- 2026-03-28：新增 `S0E-2C`，把 batch issue creation / parent-child linking / milestone-backfill tooling 从 `S0E-2B` 中拆出为独立 follow-up slice。
- 2026-03-28：`S0E-2C/P2-C1-S1` 已固定 relationship manifest contract，为下一步 linking/backfill dry-run implementation 提供稳定输入边界。
- 2026-03-28：`S0E-2C/P2-C1-S2` 已完成 relationship dry-run validation，下一步可以进入 milestone/backfill reconciliation contract。
- 2026-03-28：`S0E-2C/P3` 已完成 milestone/write-back reconciliation contract 和 dry-run validation，下一步可以评估是否进入 `P4` 或收口到稳定状态。