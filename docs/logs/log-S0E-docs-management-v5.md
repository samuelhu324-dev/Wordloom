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
  **phase_log_1**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  **phase_log_2**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **phase_log_3**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **phase_log_4**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **phase_log_5**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **phase_log_6**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
**created**: `2026-03-28`
**updated**: `2026-03-29`

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
- `S0E-3A`（Phase 3A）：roadmap milestone and child-log bridge contract
  - 详见：`docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
- `S0E-4A`（Phase 4A）：GitHub pull request automation contract
  - 详见：`docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- `S0E-4B`（Phase 4B）：PR title / label / body follow-up
  - 详见：`docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`

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
- [x] `P12`：`S0E-3A` 已起草，用于把 roadmap milestone 和 child logs 的桥接从 prose references 升级到统一 ledger
- [x] `P13`：`S0E-4A` 已起草，用于把 GitHub PR automation 从 issue automation 中独立出来
- [x] `P14`：`S0E-3A` 已完成 `P0-P1`，roadmap bridge contract 和 template rollout 已正式收口
- [x] `P15`：`S0E-3A/P1` 已继续细化为主线/支线 roadmap 双模板，便于后续支线回流主线时保持清晰记账
- [x] `P16`：`S0E-3A/P2` 已完成首条真实迁移样例，`road-S1` 与 `road-S1-1` 已显式记住 parent/branch bridge ledger
- [x] `P17`：`S0E-3A/P3` 已完成 mechanical extraction dry-run，roadmap bridge 现在可以在不扫 prose 的前提下输出结构化计划结果
- [x] `P18`：`S0E-3A/P3-C2` 已完成 child-log bridge metadata backfill，sample pair 的 `36` 条 warning rows 已被压成 `aligned`
- [x] `P19`：`S0E-4A/P0` 已完成 PR automation contract 收口，commit selection、PR metadata/description、development-link boundary 已固定
- [x] `P20`：`S0E-4A/P1` 已完成 template rollout，`pr_*` 字段说明和 PR description scaffold 已写回 parent/phase templates
- [x] `P21`：`S0E-4A/P2` 已完成 dry-run PR-prep 验证，mixed working branch 上的 `S0E-4A` 提交已能被结构化选出并生成 PR body preview
- [x] `P22`：`S0E-4A/P3` 已完成真实 PR create 验证，issue `#293` 与 draft PR `#294` 已通过 clean PR-prep branch 成功链接
- [x] `P23`：`S0E-4B/P0-P2` 已完成第一轮 follow-up 修正与 sample 验证，PR 标题压缩、结构化 labels 继承和 body footer/link 格式已回写到脚本、模板和 sample artifact
- [x] `P24`：`S0E-4B/P3-C1` 已完成 drills 规则、issue-only project 默认语义、live PR `#294` 回写校正，以及 issue project path 的本地接线；剩余阻塞仅在 GitHub-side project auth / lookup 验证
- [x] `P25`：`S0E-4B/P3-C1-S5` 已完成正文顶部 title 去重，并已把 issue project 阻塞精确收口到缺失 `project` write scope，而不是泛化为 read/project 可见性问题

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
- `S0E-3A` 草案已把 roadmap/log bridge 的核心问题收口为 child-log-first contract，并把 roadmap/log templates 增加了统一 bridge 字段；
- `S0E-3A` 已完成 `P0-P1`：phase log 已固定 bridge ownership / field contract / fail-closed semantics，template rollout 也已落到 parent/phase/roadmap 三类模板；
- `S0E-3A/P1` 已进一步拆分 roadmap authoring 为 mainline / branch 两种模板，以对应 `road-S1` 和 `road-S1-1` 这类非线性关系；
- `S0E-3A/P2` 已完成第一条真实迁移：`road-S1` 和 `road-S1-1` 现在都用 child-log-first bridge ledger 记账，并且支线产出能显式回流主线；
- `S0E-3A/P3` 已完成：现在可以从 roadmap bridge ledger 机械抽取 `M*-P* -> child log` 结构化结果，并且 parent/branch alignment 也能做 dry-run 验证；
- `S0E-3A/P3-C2` 已完成：sample pair 涉及的历史 child logs 已补齐 primary `roadmap_*` anchors 和 exact-slot `roadmap_bridge_refs`，sample plan 现在保留 `4` 个显式 `unmapped` slots，但不再有 warning fallback；
- `S0E-4A/P0` 已完成：PR automation 的 contract 已明确收口到 clean PR-prep branch strategy、`pr_*` frontmatter precedence、PR description boundary 和 Development linkage boundary；
- `S0E-4A/P1` 已完成：parent/phase templates 现在已经带有统一的 `pr_*` fail-closed 说明，以及 PR summary/checklist/evidence scaffold 输入区；
- `S0E-4A/P2` 已完成：manifest-driven planner 现在可以从 `S0E-docs-management-v5` 这条 mixed branch 中只选出 `S0E-4A` 的 `4` 条提交，并输出 clean PR-prep branch 计划与 body preview；
- `S0E-4A/P3` 已完成：真实 issue `#293`、draft PR `#294`、clean head branch `pr-prep/s0e-4a` 与 GitHub-side Development linkage 已全部验证，因此 `S0E-4A` 现在可以视为 `stable`；
- `S0E-4B` 已启动：第一轮 follow-up 已把 PR 标题范围压缩、PR 结构化 labels 继承，以及 `Evidence Footer` / `Development Link` 的 body 结构修正写回脚本和模板；
- `S0E-4B/P3-C1-S3` 已完成：线上 PR `#294` 现已对齐到 `P0-P3` 标题、`EVOLUTION + s0/knowledge system + sub/1 + drills` labels 与新的 body 结构，并且不再携带默认 project 噪音；
- `S0E-4B/P3-C1-S4` 已完成本地接线：issue create 路径已支持默认 `wordloom Board`，剩余仅是 GitHub-side project auth / lookup 验证；
- `S0E-4B/P3-C1-S5` 已完成：生成的 issue / PR body 都不再重复顶层 title，而是直接从 `Metadata` 开始；
- `S0E-4B` 当前唯一外部阻塞已被精确定位为 GitHub token 缺少 `project` write scope，因此真实 issue project 落项仍未通过；
- 既然 `S0E-3A` 的 bridge contract 已经从模板、真实 roadmap、child logs 到 extraction sample 全部闭环，下一条优先结构线应切到 `S0E-4A`，而不是先回到 `S0E-2D`。

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
- 2026-03-29：补充 roadmap/log bridge 与 PR metadata fields 到 templates，并新增 `S0E-3A` / `S0E-4A` 草案，作为 v2 issue+PR automation 的前置设计层。
- 2026-03-29：`S0E-3A/P0-P1` 已完成，下一步应进入真实 roadmap path migration，避免新 bridge 只停留在模板层。
- 2026-03-29：`S0E-3A/P1` 已进一步拆成 mainline / branch roadmap 双模板，并保留兼容 chooser，下一步可以直接迁移 `road-S1` / `road-S1-1`。
- 2026-03-29：`S0E-3A/P2` 已完成：`road-S1` / `road-S1-1` 都已迁移到显式 bridge ledger，下一步进入 `P3` 做 mechanical extraction 验证。
- 2026-03-29：`S0E-3A/P3` 已完成：manifest-driven roadmap bridge dry-run 已落地，并通过 sample plan 验证了 mainline/branch extraction 与 parent alignment；下一步可以把这套输出接到 issue/milestone automation v2。
- 2026-03-29：`S0E-3A/P3-C2` 已完成：sample pair 涉及的历史 child logs 已回填 exact-slot roadmap metadata，roadmap bridge dry-run 的 mapped rows 现已全部对齐；下一步应切到 `S0E-4A` 收口 PR automation contract 与 dry-run PR-prep 路径。
- 2026-03-29：`S0E-4A/P0` 已完成：PR automation 的 contract 已固定，下一步应进入 `P1` 把 `pr_*` fields 和 PR description scaffold 正式写回模板。
- 2026-03-29：`S0E-4A/P1` 已完成：模板层已具备 PR metadata 和 PR body scaffold 的稳定输入面，下一步应进入 `P2` 做 mixed working branch -> clean PR-prep branch 的 dry-run 验证。
- 2026-03-29：`S0E-4A/P2` 已完成：PR-prep dry-run planner 已用真实 `S0E-4A` commits 验证通过，下一步应进入 `P3` 评估真实 PR creation 和 metadata assignment 路径。
- 2026-03-29：`S0E-4A/P3` 已完成：真实 PR create 路径已经跑通，`S0E-4A` 这条线从 contract、template、dry-run 到 real-run 现已闭环；下一步应评估是否为 `S0E` 收口或另开新的 PR/issue automation follow-up。
- 2026-03-29：新增 `S0E-4B`，专门收口第一条真实 PR 暴露出来的 follow-up：标题 phase-range 命名、PR 结构化 labels 继承，以及 `Evidence Footer` / `Development Link` 的 body 版式。
- 2026-03-29：`S0E-4B/P3-C1` 已把 live PR `#294` 回写到新规则，并把 `wordloom Board` 默认语义收口到 issue create；下一步只需在具备 project 权限的环境里完成一次真实 issue project 验证。
- 2026-03-29：进一步确认 `S0E-4B` 的真实 issue create 阻塞并不是 project 不可见，而是 token 仍缺少 `project` write scope；同时去掉了生成 body 顶部重复 title。