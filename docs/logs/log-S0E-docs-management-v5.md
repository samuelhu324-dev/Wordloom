# log-S0E（Docs Management v5：structured logs → semi-automated Git issue creation）

---

**id**: `S0E-docs-management-v5`
**kind**: `log`
**title**: `docs management v5 (structured logs → semi-automated Git issue creation) v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/248`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/draft.md`
  **reference_log_1**: `docs/logs/log-S0D-6A-docs-management-v4.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **phase_log_1**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  **phase_log_9**: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  **phase_log_10**: `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
  **phase_log_11**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **phase_log_12**: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
  **phase_log_13**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **phase_log_14**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **phase_log_15**: `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
  **phase_log_16**: `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  **phase_log_17**: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  **phase_log_18**: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  **phase_log_19**: `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
  **phase_log_20**: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
  **phase_log_21**: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
  **phase_log_22**: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
  **phase_log_23**: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
  **phase_log_24**: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
  **phase_log_25**: `docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`
  **phase_log_26**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **phase_log_27**: `docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
  **phase_log_7**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **phase_log_8**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **phase_log_2**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **phase_log_3**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **phase_log_4**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **phase_log_5**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **phase_log_6**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
**created**: `2026-03-28`
  **updated**: `2026-04-02`

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
- `S0E-2D`（Phase 2D）：issue creation metadata enrichment and English body contract
  - 详见：`docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- `S0E-2E`（Phase 2E）：issue conclusion and development linkage contract
  - 详见：`docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
- `S0E-4D`（Phase 4D）：review-hold / full-auto lifecycle orchestration follow-up
  - 详见：`docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
- `S0E-5A`（Phase 5A）：lifecycle audit gate and dry-run planner
  - 详见：`docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
- `S0E-6A`（Phase 6A）：log structure normalization and dual-track evidence contract
  - 详见：`docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
- `S0E-6F`（Phase 6F）：issue body metadata and links boundary follow-up
  - 详见：`docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
- `S0E-4F`（Phase 4F）：PR body metadata-links redundancy follow-up
  - 详见：`docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`
- `S0E-4C`（Phase 4C）：PR summary / development issue rendering / issue relationship attach follow-up
  - 详见：`docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- `S0E-3A`（Phase 3A）：roadmap milestone and child-log bridge contract
  - 详见：`docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
- `S0E-4A`（Phase 4A）：GitHub pull request automation contract
  - 详见：`docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- `S0E-4B`（Phase 4B）：PR title / label / body follow-up
  - 详见：`docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
- `S0E-7D`（Phase 7D）：publish / verify / remediation / failure semantics
  - 详见：`docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
- `S0E-7E`（Phase 7E）：publish-verify-remediation gate thin orchestration entrypoint
  - 详见：`docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`

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
- [x] `P26`：`S0E-4B/P3-C1-S7S8S9` 已完成 stacked PR review 语义、标题 phase-span 优先级，以及 mixed working branch / parent-log 落点规则的收口
- [x] `P27`：`S0E-4B/P3-C1-S10S11` 已完成真实 issue/project 验证与 PR base 对齐回 `main`，因此 `S0E-4B` 现已进入 `stable`
- [x] `P28`：`S0E-2D` 已建档，用于把 milestone、relationship、projects 与 English issue body contract 收口到 enriched issue creation
- [x] `P29`：`S0E-2E` 已建档，用于把 post-merge issue conclusion、Development linkage 与 final DoD PR refs 收口为独立 contract
- [x] `P30`：`S0E-2D` 已完成 `P3`，旧 issue `#288` 已按当前 creation body contract 回收，当前 log 的真实 sample issue `#297` 也已创建并回写
- [x] `P31`：`S0E-2E` 已完成 `P0-P1`，GitHub auto-close 与 final conclusion 的边界、exact-ID merged PR 选择规则，以及 final English conclusion body shape 已固定
- [x] `P32`：`S0E-2E` 已完成 `P2`，manifest-driven issue-conclusion dry-run planner 与代表性 sample validation 已落地，且 `S0E-4A` 已验证多 merged PR 情况
- [x] `P33`：`S0E-2E` 已完成 `P3`，真实 issue-conclusion write-back 已通过 `#297` 跑通，并验证了 open-after-merge issue 的 body update + explicit close 路径
- [x] `P34`：`S0E-2E` 已完成 format revision cycle：最终 body 去掉 `Development`、DoD 改为短 PR refs，并用 `#295` 完成第二条真实 write-back 样本
- [x] `P35`：`S0E-4C` 已建档，用于集中收口 PR Summary 占位符、Development issue 短引用，以及 child issue sidebar Relationships attach 这三类 follow-up
- [x] `P36`：`S0E-4C` 已完成 `P0-P1`，PR create 现在会阻止 placeholder Summary 上线，Development issue 已统一到短引用，relationship apply 脚本也已补齐
- [x] `P37`：`S0E-4C` 已完成 `P2`，`S0E-2D` 的 PR-prep 样本已重生成且 Summary 不再占位，`S0E` child relationship 的 plan/apply 样本也已补齐
- [x] `P38`：`S0E-4C` 已完成 `P3-C1-S1/S3`，四条历史 `S0E` PR 已审查，live PR `#296` 与 `#298` 已按现行 body contract 回写，`#294` 与 `#299` 则确认无需修改
- [x] `P39`：`S0E-4C` 已完成 `P3-C1-S2` 与 `P4`，真实 issue `#300`、PR `#301`、parent relationship attach 与 final issue conclusion 已跑完一条完整闭环，因此该 slice 现可视为 `stable`
- [x] `P40`：`S0E-4C` 已完成 `P5`，`create_pr_from_plan.py` 现可在 long-lived mixed branch 的 cherry-pick 冲突后回退到 source-head snapshot，并已用真实 PR `#302` 与 issue `#300` 更新完成验证
- [x] `P41`：`S0E-4C` 已完成 `P6`，PR title / checklist / evidence footer 现已按统一 scope 选择器收口，且历史 live PR `#296` 已按新规则回写
- [x] `P42`：`S0E-4C` 已完成 `P7`，merged PR `#301/#302` 现可按最终 title scope 重放 checklist/evidence，历史 body drift 已完成回写
- [x] `P43`：`S0E-4D` 已建档，用于把 `review-hold` / `full-auto` 与 default human-gated handoff 边界独立收口到 lifecycle orchestration 侧
- [x] `P44`：`S0E-4D` 已完成 `P2`，staged review / resume-after-review / post-merge full-auto 三类命令口径与 fail-closed examples 已正式固定
- [x] `P45`：`S0E-4D` 已完成 `P3`，live issue `#303`、draft-to-merged PR `#304`、parent relationship attach 与 final conclusion 已跑通一条真实 staged-to-closed-loop 样本
- [x] `P46`：`S0E-4D` 已扩展历史验证轮次，`S0E-2A/#289`、`S0E-2B/#288` 与 `S0E-4A/#293` 均已按 Creation -> PR -> merge -> conclusion 路径完成 write-back 与 close
- [x] `P47`：`S0E-4D` 已完成 representative issue audit 与 `P4`，补齐缺失的 sidebar relationships `#248 -> #289/#293/#297`，并正式记录 body-complete 不等于 relationship-complete 的审计边界
- [x] `P48`：`S0E-5A` 已完成 `P0-P2`，现已定义 lifecycle audit gate contract，落地 dry-run planner，并以 `#289/#297/#293/#300/#303` 的 representative sample 证明 audit 输出可直接作为 mutation 前置 gate
- [x] `P49`：`S0E-5A` 已完成 `P3`，历史 warning/blocked audit 结果现可被转换成 relationship / issue-conclusion 的 dry-run remediation manifests，作为后续真正前置 gate 的修复规划层
- [x] `P50`：`S0E-5A` 已完成 `P4`，统一 pre-gate entrypoint 已把 audit / decision / remediation-planning 串起来，并固定 `warning` 为 stop-and-plan-remediation 的 gate 策略
- [x] `P51`：`S0E-5A` 已完成 `P5`，pre-gate 已接到 issue-conclusion mutation 前面，并用一条真实 pass->apply 样本和一条 frozen stop drill 证明 gated apply 行为成立
- [x] `P52`：`S0E-5A` 已完成自身真实 lifecycle 闭环，issue `#305`、merged PR `#306`、sidebar relationship attach 与 final issue conclusion 已全部落地；同时已新建 `S0E-5B` 作为 guarded apply 扩展的后续 slice
- [x] `P53`：`S0E-5B` 已完成 `P0-P1`，guarded relationship attach 现可在“仅有 relationship remediation”时从 `stop-for-remediation` 继续，并已用 live issue `#307` 的真实 attach 与一条 frozen mixed-remediation stop drill 完成验证
- [x] `P54`：`S0E-5B` 已完成 `P2`，已选定 guarded `PR body rewrite` 作为下一条 PR-side family，并用 converged `S0E-5A/#305 -> PR #306` 的 live rewrite plus 一条 frozen stop drill 完成验证
- [x] `P55`：`S0E-5B` 已完成 `P3`，`#307 -> PR #308` 现已形成一条真实 closed-loop sample，并在同一 issue/PR pair 上连续验证了 guarded relationship attach 与 guarded PR-body rewrite 两条 mutation family
- [x] `P56`：`S0E-5B` 已正式收口为 `stable`，并已新建 `S0E-5C` 用于单独拆解 guarded `PR create` 的阶段边界，而不再继续扩张 `S0E-5B` 的 scope
- [x] `P57`：`S0E-5C` 已完成 `P0`，当前 `PR create` path 已被拆成 dry-run 输入解析、scope selection、create preflight、local branch materialization、remote publish、live PR publish、post-create evidence finalize 七段，并已固定这些 failure boundaries 不能被压扁成一个 guarded yes/no mutation
- [x] `P58`：`S0E-5C` 已完成 `P1`，现已固定 reuse-vs-new-rule 边界：没有任何阶段可以原样复用现有 lifecycle pre-gate 作为整条 create path 的总闸门，只有 create preflight 可把它作为 issue-readiness 前置层，而 local materialization、remote publish、live PR publish 仍需独立边界
- [x] `P59`：`S0E-5C` 已完成 `P2`，live issue `#309` 已作为 representative sample 建立并挂到父 issue `#248`，bounded front-half preflight 现已证明 `S1-S3` 可以在进入 `S4` 前输出清晰的 pass/stop 证据，其中 stop 样本来自 create-specific branch-collision 而非 lifecycle gate 本身
- [x] `P60`：已新建 `S0E-5D`，专门收口 issue creation / issue conclusion / PR body / Evidence Footer 的 canonical contract，以及 hard gate 需要新增的 body-shape 检查范围，避免继续把格式合同问题混进 `S0E-5C`
- [x] `P61`：`S0E-5D` 已完成 `P0`，issue creation / issue conclusion / PR body 的 canonical body families 现已按 operator 规则固定，metadata rows 不允许出现空段，Evidence Footer 也已先固定为 drills/evidence-only 且禁止 commit-footer fallback
- [x] `P62`：`S0E-5D` 已完成 `P1`，Evidence Footer 现已固定为只从 `Evidence Footer Source` 读取，并采用唯一行型 ``- `P1-C1-S1` | artifact: `...```，其中阶段串与 artifact 路径串都必须带反引号
- [x] `P63`：`S0E-5D` 已完成 `P2`，hard gate 现已补上 body-shape checks，PR prep/rewrite 只读 `Evidence Footer Source`，并已有一条 pass 样本与两条 stop 样本分别覆盖 canonical footer、未加反引号 footer 和错误来源块
- [x] `P64`：`S0E-5D` 已完成 `P3`，rollout 顺序现已固定为 `gate-first + post-apply live verify + selective historical rewrite`，同时已新增 live PR verifier，并把“无 drills/evidence 资格却塞 Evidence Footer”固定为可驳回条件
- [x] `P65`：已进一步收口 `S0E-5D/P3` 的边界：historical rewrite 执行现明确挂到 `S0E-5D/P4`，而后置 gate / post-apply verify / GitHub Actions ownership 则延后到 `S0E-5C/P3` 讨论，不再继续塞在 `S0E-5D`
- [x] `P66`：`S0E-5D` 已完成 `P4`，代表性历史 merged PR `#299/#302/#306/#308` 与 closed issue `#293/#295/#297/#300/#303/#305/#307` 均已按 canonical body contract 回写并通过 live verifier / lifecycle audit，因此 `S0E-5D` 现已进入 `stable`
- [x] `P67`：已新建 `S0E-6A`，用于收口 logs 的双轨证据模型、结构化输入块边界，以及 parent/phase templates 的后续优化方向，避免继续把 log 结构问题混进 `S0E-5C` 或 `S0E-5D`
- [x] `P68`：`S0E-6A` 已完成 parent/phase templates 的双轨证据 guidance rollout，并已把代表性混合块样本 `S0E-5C` / `S0E-4C` 迁移到 split `PR links` + `Evidence Footer Source` 结构
- [x] `P69`：`S0E-6A` 已完成本地 issue draft scaffold sample，`docs/issues/issue-S0E-6A-*.md/.json` 已生成，因此该 slice 现已可视为 `stable`
- [x] `P70`：`S0E-5C` 已完成 `P3`，现已固定 `S6` live PR publish 在 v1 继续由 operator 持有，而 post-apply live verify 应位于 `S6` 之后、`S7` 之前，GitHub Actions 仅作为后续 secondary enforcement
- [x] `P71`：`S0E-5C` 现已进入 `stable`，因为 guarded `PR create` 的分解、front-half evidence、publish boundary ownership 与 post-apply verification placement 都已收口
- [x] `P72`：`S0E-5C` 已完成 `P4`，`create_pr_from_plan.py` 现已把 post-apply live verifier 直接接到真实 `gh pr create` 后面，并把验证状态与 artifact 路径写回同一份 `pr-create result` JSON
- [x] `P73`：`S0E-5C/P4` 已用历史样本 `S0E-5B/#308` 完成非破坏性验证，`docs/issues/pr-prep-S0E-5B-real-post-apply-live-body.md` 与 `...-verify-result.json` 已证明新执行顺序可产出稳定证据
- [x] `P74`：已新建 `S0E-6B`，用于收口 AI-authored logs 的本地 gate / `stable` 后验 gate 策略，并把这部分从 GitHub Actions slice 中拆开
- [x] `P75`：`S0E-6B` 已完成 `P0`，现已固定 local log gates 只应约束 automation-facing surfaces 与 `stable` 转换质量，而不应演化成 prose linter
- [x] `P76`：`S0E-7A` 已重构回 GitHub-side slice，现仅负责 Actions secondary enforcement、artifact publishing 与 CI failure surfacing 边界
- [x] `P77`：`S0E-6B` 已完成 `P1`，现已固定第一版 local log gate 只检查五类 deterministic surfaces：frontmatter、required sections、`PR Summary Inputs` 形状、`Evidence Footer Source` 行型、placeholder hygiene
- [x] `P78`：`S0E-6B/P1` 已固定四类最小 failure taxonomy：`missing-required-block`、`invalid-structured-block`、`placeholder-left`、`stable-contradiction`
- [x] `P79`：`S0E-6B` 已完成 `P2`，现已固定第一轮必须 hard-require pass gate 的入口只包括 `log -> issue draft/create` 与 `log -> PR prep/create`
- [x] `P80`：`S0E-6B/P2` 已固定 advisory-only rollout boundary：普通 draft authoring、非 automation logs、以及 aggregator-only parent logs 先不做 hard block
- [x] `P81`：`S0E-6B` 已完成 `P3`，现已固定 `stable` promotion 前必须执行更强的后验 checks：required surfaces 无 placeholder、contract blocks 仍有效、status/checklist/evidence 之间不得出现 material contradiction
- [x] `P82`：`S0E-6B/P3` 已固定 `stable` gate 的执行归属为 local-first / CI-mirror-later：本地 gate 先作为 authoritative owner，GitHub Actions 只在后续 `S0E-7A` 中作为 secondary mirror enforcement
- [x] `P83`：`S0E-7A` 已完成 `P1-C1-S1`，现已固定第一版 GitHub Actions mirror-verifier workflow 先以 `workflow_dispatch` 启动，并显式接收 `source_log_path`、`pr_ref`、`repo` 输入，产出 live body / result JSON / console JSON 三类 artifact
- [x] `P84`：`S0E-7A/P1-C1-S2` 已固定 secondary-enforcement 的 failure surfacing：workflow summary 必须明确“post-publish drift detected”而非“prevented publish”，且必须在 artifact 上传后再 fail job
- [x] `P85`：`S0E-7A` 已完成 `P2-C1-S1`，现已固定 mirror-verifier 的 retained artifact set 为 live body、verify result JSON、console JSON、workflow summary markdown、artifact manifest JSON 五类证据
- [x] `P86`：`S0E-7A/P2-C1-S2` 已固定 failure surfacing 的三层面：workflow summary、GitHub check annotations、以及 retained evidence manifest，且 failure classification 必须保持 secondary-enforcement 语义
- [x] `P87`：`S0E-7A` 已完成 `P3-C1-S1`，现已固定第一轮 rollout boundary 继续保持 `workflow_dispatch` only，而不提前接入 `pull_request` 事件，因为当前还没有稳定的 `source_log_path` 自动归属规则
- [x] `P88`：`S0E-7A/P3-C1-S2` 已固定 CI adoption success criteria：至少需要 representative pass/non-pass 两类 retained evidence，并且未来自动触发方案必须先解释 `source_log_path` 的确定性来源
- [x] `P89`：已新建 `S0E-4E`，用于专门承接 `PR event -> source_log_path` 的自动归属问题，并把它重新归类到 PR-family follow-up，而不是继续放在 `7x` workflow family 下
- [x] `P90`：`S0E-4E` 已完成 `P0`，现已固定 automatic PR-event mirroring 仍被 attribution contract 阻塞，直到 repo 能 fail-closed 地确定单一 contract-owning source log
- [x] `P91`：`S0E-4E` 已完成 `P1-C1-S1`，现已固定允许参与 attribution 的 machine-readable ownership surfaces 只包括 trusted explicit provenance、canonical PR-body `Log:` row，以及 exact-ID head-branch fallback
- [x] `P92`：`S0E-4E/P1-C1-S2` 已固定 attribution precedence：explicit provenance > PR-body `Log:` row > exact-ID branch fallback；而 prose/title 模糊匹配、labels/milestone/project、Development Link、Evidence Footer 都不得单独声明 ownership
- [x] `P93`：`S0E-4E` 已完成 `P2-C1-S1`，现已固定 attribution ambiguity 的第一版 stop taxonomy：`missing-attribution`、`conflicting-attribution`、`multi-candidate-attribution`、`invalid-attribution-shape` 都必须 fail-closed
- [x] `P94`：`S0E-4E/P2-C1-S2` 已固定代表性样本期望：后续 rollout widening 前至少需要一条 deterministic owner sample 和一条 ambiguity stop sample，而且 ambiguity case 不得在 guessed source log 上继续 verify
- [x] `P95`：`S0E-4E` 已完成 `P3-C1-S1`，现已固定 `4E -> 7A` 的 attribution handoff payload：只有 `result=resolved`、`source_log_path` 精确存在且 `eligible_for_secondary_enforcement=true` 时，mirror verifier 才能继续执行
- [x] `P96`：`S0E-4E/P3-C1-S2` 已固定 limited automatic-rollout unblocking criteria：至少需要一条 resolved handoff sample 和一条 attribution-stop sample，并且 stop case 必须在 verifier 之前停下并保留独立 attribution evidence
- [x] `P97`：已新建 `S0E-7B`，用于承接 attribution payload 的实现、`7A` consume-or-stop 接线，以及 resolved/stop 两类端到端样本验证，而不再继续挤压 `S0E-4E` 的 contract scope
- [x] `P98`：`S0E-7B` 已完成 `P0`，现已固定 `S0E-4E` 只继续拥有 attribution contract，而 planner/result JSON 与 GitHub-side integration implementation 由 `S0E-7B` 独立承接
- [x] `P99`：`S0E-7B` 已完成 `P1-C1-S1`，现已新增 attribution resolver entrypoint，可从 trusted explicit provenance、canonical PR-body `Log:` row 与 exact-ID branch fallback 产出 `4E -> 7A` consume-or-stop payload
- [x] `P100`：`S0E-7B/P1-C1-S2` 已固定 retained attribution artifact path pair：normalized PR payload snapshot JSON 与 attribution result JSON 都使用稳定 repo-relative path reporting，便于后续 `7A` 直接接线
- [x] `P101`：`S0E-7B` 已完成 `P2-C1-S1`，现已把 GitHub Actions workflow 改成 attribution-first：只有 `result=resolved` 且 `eligible_for_secondary_enforcement=true` 时才继续 mirror verification
- [x] `P102`：`S0E-7B/P2-C1-S2` 已把 attribution-stop 收口为 verifier 之前的独立 retained-evidence outcome，workflow summary / annotations / manifest / final failure 都不再把它伪装成 verifier drift
- [x] `P103`：`S0E-7B` 已完成 `P3-C1-S1`，现已有一条 representative resolved sample，证明 handoff 会以 `pr-body-log-row` 作为 winning surface 并进入 `continue-to-verifier` gate
- [x] `P104`：`S0E-7B/P3-C1-S2` 已完成 attribution-stop sample，现已有一条 `stop-conflicting-attribution` 代表性样本，并通过 sample manifest 明确记住 `skipped-before-verifier` 边界
- [x] `P105`：已新建 `S0E-7C`，用于承接历史 logs 的批量 review / format 审查 / lifecycle completeness sampling，而不把这类 follow-up 混进 `S0E-7B` 或直接升级成 bulk apply
- [x] `P106`：`S0E-7C` 已完成 `P1-P2`，现已新增 manifest-driven historical log review planner，并保留一组覆盖 closed-loop / issue-open-no-pr / log-only 的 representative samples
- [x] `P107`：`S0E-7C` 已完成 `P3`，现已新增 manual GitHub Actions mirror workflow，可通过 `workflow_dispatch` 重放同一 review planner 并保留 summary / plan artifacts
- [x] `P108`：`S0E-5C` 已完成真实 lifecycle follow-through：PR `#310` 已创建并合并，issue `#309` 已完成 final issue-conclusion write-back，因此这条 slice 不再只是 issue-only sample
- [x] `P109`：`S0E-7C` 已完成 `P4-C1-S1`，现已新增覆盖整个 `S0E` family 的 full-series historical review manifest/plan，历史 backlog 现在有了第一份结构化基线读数
- [x] `P110`：`S0E-7C` 已完成 `P4-C1-S2`，focused PR `#311` 已把历史 review mirror workflow 挂到默认分支，且 `S0E-docs-management-v5` 上的 live dispatch `run 23827100968` 已成功保留首条 full-series replay evidence
- [x] `P111`：`S0E-6C` 已完成 `P0-P3`，issue `Context` 现已固定为 main log `5` 句 / child log `4` 句的英文单句逐行合同，并已通过 `#309` 的真实 conclusion replay 与 lifecycle audit gate 验证
- [x] `P112`：`S0E-7C` 已完成 `P4-C1-S3`，focused PR `#312` 已移除 historical review planner 在默认分支上的 runtime closure 缺口，`main` 上的 live dispatch `run 23827684652` 也已成功闭环
- [x] `P113`：`S0E-7C` 已完成 `P4-C1-S4`，截图范围内全部已关闭 `S0E` 子 issues 都已重新检查并重跑 conclusion，`9/10` 条 `Context` 漂移已被批量修复，修复后 `10/10` lifecycle audit 全部通过
- [x] `P114`：已新建并完成 `S0E-6D/P0-P3`，issue `Context` contract 已从 rigid sentence-slot template 升级为 natural-summary + weak gate，draft/conclusion renderer 与 lifecycle audit 现已统一到同一规则
- [x] `P115`：`S0E-7C` 已完成 `P4-C1-S5`，刚才审查过的 `10` 条已关闭 `S0E` 子 issues 已按 `S0E-6D` 的 natural-summary `Context` 规则重写，并再次通过 `10/10` lifecycle audit
- [x] `P116`：`S0E-6D` 已完成 `P4-C1-S1`，`Context` gate 现已收缩为 prose-first 弱约束，只检查 `3-5` 条可读英文句子行、基本完整性和 placeholder hygiene，不再强制 prose anchors
- [x] `P117`：`S0E-6D` 已完成 `P4-C1-S2`，issue `Context` renderer 现已改成 `fact pool + style family`，preview bodies 开始按 issue 变化句子顺序和入口，而不再共享同一条 sentence-slot 骨架
- [x] `P118`：`S0E-6D` 已完成 `P4-C1-S3`，刚才那 `10` 条 closed `S0E` 子 issues 已按 fact-pool/style-family renderer 完成 live replay，并再次通过 `10/10` lifecycle audit
- [x] `P119`：已新建并完成 `S0E-6E/P0-P3`，`Context` 现已改成“单条生成、批量保留”的 ownership model；issue draft 默认回到 scaffold，batch conclusion 默认只保留并告警，不再顺手代写正文
- [x] `P120`：`S0E-6E` 已完成 `P4-C1-S1`，`S0E-2B/#288` 与 `S0E-2A/#289` 已按单条 authoring 路径逐条优化 `Context`，随后再次通过 lifecycle audit
- [x] `P121`：`S0E-2E` 与 `S0E-6E` 已补充 final conclusion body wording 约定：`Context` 末句负责说明 slice 留下的结果/基线，精确 PR 证据只保留在 `DoD`
- [x] `P122`：`S0E-6E` 已把同一条 outcome-ending 规则扩展到其余已关闭 `S0E` 子 issues，并同步把单条 conclusion generator 的默认末句从 PR-evidence wording 改成结果/基线 wording
- [x] `P123`：已新建 `S0E-6F`，用于收口 issue body 的字段归属微调：`Metadata` 去掉 `Source log`，`Links` 新增可选 `Previous log`，并把后续 renderer / gate / runbook 的落地措施集中记账
- [x] `P124`：`S0E-6F` 已完成 `P0-P1`，issue draft / issue conclusion preview / lifecycle audit / owner logs / runbook 现已统一到“Metadata 只留状态字段、Links 承接 deterministic navigation”的新边界
- [x] `P125`：`S0E-6F` 已完成 `P2`，新的代表性 artifacts 已生成，当前 `10` 条 closed `S0E` child issues 也已按同一边界完成 bounded refresh，并通过 `10/10` post-refresh lifecycle audit
- [x] `P126`：`S0E-6F` 已完成 `P3`，issue body contract 现已显式区分 top-level parent 与 child issue：`#248` 已刷新到 parent-aware body shape，且 `S0E` parent-plus-child `11` 条 issue 现已一起通过 post-refresh lifecycle audit
- [x] `P127`：已新建 `S0E-4F`，专门收口 PR body 中 `Development Link` 与 `Links -> Issue` 的重复问题，并把当前 `17` 条 live `S0E` PR 的全量审查范围固定到同一条 log
- [x] `P128`：`S0E-4F` 已完成 `P0-P1`，shared PR contract / preview-create-rewrite renderer / canonical spec / log templates 现已统一到“Development issue 只留在 Metadata、Links 只保留 deterministic navigation”的新边界
- [x] `P129`：`S0E-4F` 已完成 `P2`，当前 `17` 条 live `S0E` PR 已全量审查为 `17/17 fail`，后续 rewrite scope 也已固定为一个按 `4` 类 drift family 分层执行的 bounded batch
- [x] `P130`：`S0E-4F` 已完成 `P3`，rewrite rollout 最终分成 `4` 个 cycle：先修 parser/source-log blocker，再跑 `2` 轮 live PR rewrite batch，最后对同一组 `17` 条 live `S0E` PR 做 post-apply verify，并得到 `17/17 pass`
- [x] `P131`：`S0E-4F` 已完成 `P4`，现已补上 PR Development/label 的 live GitHub metadata gap，补建并 conclude 了原先缺失的 `S0E-1A/#316`、`S0E-2C/#313`、`S0E-3A/#314`、`S0E-7C/#315`，同一组 `17` 条 audited PR 现已达到 body + metadata 双重完整
- [x] `P132`：已新建 `S0E-7D`，用于把当前 docs/GitHub workflow 的 `publish -> verify -> remediation -> failure handling` 语义收口为明确的 failure taxonomy、replay/backfill contract 与 handling semantics
- [x] `P133`：`S0E-7D` 已完成 `P0-P1`，现在已经保留第一份 failure taxonomy artifact，把当前已知 issue/PR/log drift surfaces 显式映射到 `strong-structure` / `weak-structure` 以及 `block` / `replayable` / `manual` / `reconciliation`
- [x] `P134`：`S0E-7D` 已完成 `P2-P3`，现在已经保留 representative manifest / audit summary，并把 replay-only remediation contract、mixed-batch split 规则、以及 post-apply verify stop rules 固定为结构化证据
- [x] `P135`：`S0E-7D` 已完成 `P4`，现在已经把 future `publish-verify-remediation gate` 的名称、决策词汇、adapter reuse 边界和非目标面固定为结构化 surface contract
- [x] `P136`：已新建 `S0E-7E`，用于把 `S0E-7D/P4` 命名的 future `publish-verify-remediation gate` 落成一层薄编排入口，并明确其与既有 guarded adapters 的实现边界
- [x] `P137`：`S0E-7E` 已完成 `P0-P1`，现在已经保留 thin gate contract artifact，并实现了一条新的 `publish-verify-remediation gate` planner，用统一 decision artifact 复用 lifecycle-family allow path 与 `pr-create-preflight` stop path
- [x] `P138`：`S0E-7E` 已完成 `P2`，现在 thin gate 已能把 `issue-conclusion`、`issue-relationship` 与 `pr-body-rewrite` 委托到既有 guarded adapters，同时保持 `pr-create-preflight` 仍是 planning-only front-half family
- [x] `P139`：`S0E-7E` 已完成 `P3`，现在 thin gate 已保留 representative issue-side pass、PR-side pass、`pr-create-preflight` planning-only stop 与 delegated-apply rejection 四类边界证据
- [x] `P140`：`S0E-7E` 已完成 `P4`，现在 thin gate 的 local/publish-time/CI wrapping boundary 与 top-level post-apply verify exposure 都已固定为结构化 contract

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
- `S0E-2D` 已完成 `P3`：旧样本 issue `#288` 已按新 creation body contract 去掉正文 title 并清空预写的 `Context/DoD`，当前 log 也已通过真实 issue `#297` 完成 enriched create sample 与 write-back；
- `S0E-2D` 已补充 `P1-C2/P3-C3` follow-up：child issue 现在会从 `parent_log.links.issue` 继承顶层 `S0E` issue `#248`，而顶层 issue body 则不会再渲染空白的 `Parent issue`；
- `S0E-2D` 已补充 `P1-C2-S3/P3-C3-S2` follow-up：`Parent issue` 现在只保留在 `Metadata`，并统一使用 `#248` 这类短 GitHub 引用，不再在 `Links` 重复出现；
- `S0E-4D` 已完成 `P3`：live issue `#303`、PR `#304`、`#248 -> #303` relationship attach，以及 final issue conclusion 已形成一条真实 staged-to-closed-loop 样本，因此该 slice 现可视为 `stable`；
- `S0E-4D` 已补跑历史验证轮次：`S0E-2A` 的 PR `#287` 与 issue `#289`、`S0E-2B` 的 PR `#290` 与 issue `#288`、以及 `S0E-4A` 的 issue `#293` 均已完成最终 write-back / close；
- `S0E-4D` 已完成 representative issue 审计：`#289`、`#293`、`#295`、`#297`、`#300`、`#303` 的最终 body 均已合规，而缺失的 sidebar relationships `#248 -> #289/#293/#297` 也已补齐；
- `S0E-5A` 已完成 dry-run gate 起步版：planner 现在可对 live issue body、labels、exact-ID merged PR evidence 与 sidebar relationship 做 stage-aware 审计，且 representative sample 五条 child issues 均已 `pass-audit`；
- `S0E-5A` 已完成 `P3`：新增 remediation planner，可把 archived historical findings 中的 `#288` warning 与 `#289/#293/#297` blocked findings 分别转换成 issue-conclusion / relationship dry-run manifests，而不必重新破坏 live GitHub 状态；
- `S0E-5A` 已完成 `P4`：新增 unified pre-gate orchestrator，现可从单一 manifest 输出 `allow-apply` / `stop-for-remediation` / `hard-fail-input` 三类 gate decision，并已固定 warning 在 gate 层一律 stop 而非直接放行；
- `S0E-5A` 已完成 `P5`：新增 guarded issue-conclusion apply 入口，现已证明 pre-gate 可直接位于 mutation command 前面，既能放行真实 `S0E-4D/#303` 的 live rewrite，也能在 frozen stop sample 上于 apply 前硬停；
- `S0E-5A` 已完成自身真实闭环：live issue `#305` 已经通过 merged PR `#306` 交付，sidebar relationship `#248 -> #305` 已补齐，最终 closed issue body 也已回写，因此该 slice 现已不再只停留在 gate drill；
- `S0E-5B` 已完成 `P0-P1`：guarded relationship attach 现已作为第一条扩展 mutation family 落地，live issue `#307` 已通过这条路径挂到父 issue `#248`，而混合 remediation 的 frozen sample 仍会在 apply 前被硬停；
- `S0E-5B` 已完成 `P2`：guarded `PR body rewrite` 现已接到同一 pre-gate 后面，merged PR `#306` 已通过一条真实 allow-apply 路径完成重写，而 blocked fixture 仍在 edit 前被硬停；
- `S0E-5B` 已完成 `P3`：issue `#307` 先通过 guarded relationship attach 接到父 issue `#248`，随后在同一样本上生成并合并 PR `#308`，再对这条 merged PR 跑 guarded body rewrite，最后把 issue 正式 conclusion 到 closed state；
- `S0E-5B` 现已可视为 `stable`：该 slice 已经完成 in-place guarded mutation families 的边界、单项验证和同样本组合闭环；
- `S0E-5C` 已完成 `P0`：guarded `PR create` 现已被拆成 7 个明确阶段，且已确认 remote branch publish 与 live PR publish 是两个不同的 publish boundary，不能继续被当成一个原子 guarded mutation；
- `S0E-5C` 已完成 `P1`：当前结论是不允许把现有 lifecycle pre-gate 原样抬升为整条 create path 的总闸门，只有 create preflight 能把它作为 issue-readiness 前置层，而 branch materialization、remote publish、live PR publish 必须继续拆开；
- `S0E-5C` 已完成 `P2`：`#309` 现已作为 live representative sample 证明 bounded front half 可以同时产出 pass 和 stop 两类结果，而且两条路径都明确停在 `S4-local-branch-materialization` 之前；
- `S0E-5C` 已完成 `P4` 并保持 `stable`：真实 `PR create` 路径现已按 `S6 -> live verify -> S7` 执行，并会把 post-apply verification status、live body artifact 与 verify result artifact 一并写回 `pr-create result`；若后续还要深化 guarded rollout，也仍只建议单独评估 `S4/S5` targeted rules 或补充 secondary GitHub Actions enforcement；
- `S0E-6B` 已建立并完成 `P0`：本地 AI-authored logs 现已明确需要窄面 contract gates，且 `stable` 也已明确需要更强的后验 gate；下一步应先定义最小 deterministic checks，而不是直接上全量 lint；
- `S0E-6B` 已完成 `P1`：第一版 local log gate 的 deterministic checks 与最小 failure taxonomy 都已固定，下一步可以转入“哪些 automation entrypoints 必须要求 pass gate”这个更具体的问题，而不必继续停留在抽象原则层；
- `S0E-6B` 已完成 `P2`：第一轮 automation entry-gate rollout boundary 已固定，issue/PR automation 入口现在被定义为 hard-require pass gate，而普通 authoring 与 aggregator-only 路径仍保持 advisory-only；
- `S0E-6B` 已完成 `P3`：`stable` promotion 前的更强后验 checks 与 local-first / CI-mirror-later execution policy 现已固定，因此本地 log stability contract 已从“要不要 gate”推进到“何时可以信任 stable”这一层；
- `S0E-7A` 已重构为纯 GitHub-side slice：当前只讨论 Actions mirror-verifier workflow、artifact publishing 与 failure surfacing，不再混入 log stability policy；
- `S0E-7A` 已完成 `P1`：第一版 GitHub Actions mirror-verifier workflow 已以手动触发方式落地，并已固定输入合同、artifact 输出与 secondary-enforcement wording；下一步应继续收口 `P2` 的 retained artifacts 与 failure surfacing 细则，而不是过早扩大自动触发范围；
- `S0E-7A` 已完成 `P2`：mirror-verifier 的 retained artifact set、artifact manifest 与 UI/check surfaces 已经固定，因此后续 `P3` 可以专注讨论触发边界与 adoption criteria，而不必再回头争论 run evidence 怎么保存；
- `S0E-7A` 已完成 `P3`：第一轮 rollout 现明确继续保持 manual-only，后续是否扩大到自动 PR-event mirroring 现在有了清晰的 attribution 前提和 adoption criteria，因此该 slice 的 v1 决策链已闭合；
- `S0E-4E` 已完成 `P3`：`PR event -> source_log_path` attribution 现已具有明确的 consume-or-stop handoff contract，因此 `S0E-7A` 后续接入自动 PR-event mirroring 时不必再猜什么时候 verify、什么时候应在 attribution 阶段先停下；
- `S0E-7B` 已完成并进入 `stable`：attribution resolver、GitHub Actions consume-or-stop wiring，以及 resolved/stop representative samples 现已全部落地，因此 `4E -> 7A` 的 implementation follow-up 已从 contract follow-up 推进到可验证的执行层；
- `S0E-7C` 已完成并进入 `stable`：历史 logs 的批量 review planner、representative sample manifest/plan，以及 manual dispatch mirror workflow 现已全部落地，因此后续 historical backfill 可以先从结构化 review 结果进入 targeted follow-up；
- `S0E-7C/P4` 已完成第一轮 Actions 打通：`#311` 现已让历史 review mirror workflow 对默认分支可见，而 `run 23827100968` 也已证明同一 workflow 可以在 `S0E-docs-management-v5` 上成功重放 full-series `S0E` historical review；
- `S0E-7C/P4` 已进一步完成默认分支 runtime closure：focused PR `#312` 移除了 planner 对 `body_contract.py` 的 `main` 运行时依赖，而 `run 23827684652` 已证明 historical review mirror workflow 现在可以直接在默认分支成功完成 full-series replay；
- `S0E-7C/P4` 已进一步完成 closed child issue 修复闭环：截图范围内全部已关闭 `S0E` 子 issues 都已重新检查，`#288/#289/#293/#295/#297/#300/#303/#305/#307` 的 `Context` 漂移已通过批量 conclusion replay 回补，随后批量 lifecycle audit 对 `10` 条子 issue 全部给出 `pass`；
- `S0E-6D` 已完成并进入 `stable`：issue `Context` 已从 rigid sentence slots 升级为 source-log-derived natural-summary renderer + weak deterministic gate，draft / conclusion / lifecycle audit 三条路径现已统一；
- `S0E-7C/P4` 已进一步完成 `S0E-6D` 的 live replay：刚才审查过的 `10` 条 closed `S0E` child issues 已按 natural-summary `Context` 规则重写，并再次通过 `10/10` lifecycle audit；
- `S0E-6D` 已重新打开 `P4`：下一步不再继续加弱模板，而是要把 `Context` 收口成 prose-first weak gate + fact-pool/style-family renderer，让 issue `Context` 真正回到“给人读”的摘要入口；
- `S0E-6D/P4-C1-S1` 已完成：lifecycle audit 不再强制 `Context` 在正文里显式携带 prose anchors，当前 gate 已收缩为 `3-5` 条可读英文句子行、基本完整性与 placeholder hygiene；
- `S0E-6D/P4-C1-S2` 已完成：issue `Context` renderer 现已从 sentence-slot assembly 切到 `fact pool + style family`；
- `S0E-6D/P4-C1-S3` 已完成：刚才审查过的 `10` 条 closed `S0E` child issues 已按 fact-pool/style-family renderer 完成新一轮 live replay，并再次通过 `10/10` lifecycle audit，因此这条 slice 现已重新回到 `stable`；
- `S0E-6E` 已完成并进入 `stable`：`Context` 的 ownership 现已从“batch-capable rewrite surface”改成“single-item authoring surface”，新的单条生成脚本、scaffold-first issue draft 默认值，以及 batch-preserve conclusion planning 都已落地并留存样本；
- `S0E-6E/P4-C1-S1` 已完成：`S0E-2B/#288` 与 `S0E-2A/#289` 现已作为第一对真实 one-item live refresh 样本，用新的 authoring 路径逐条优化 `Context` 并再次通过审计；
- `S0E-2E` 与 `S0E-6E` 现已补上 conclusion wording 约定：若 final body 同时保留 `Context` 与 `DoD`，则 `Context` 尾句只讲最终留下的结果/可复用状态，不再重复 `#287/#290` 这类 PR 证据；
- `S0E-6E/P4-C1-S2` 已完成：除 `S0E-2A/#289` 与 `S0E-2B/#288` 之外，其余已关闭 `S0E` 子 issues 也已全部改写为同一条 outcome-ending 规则，并再次通过批量 lifecycle audit；同时单条 conclusion generator 的默认 outcome 句也已改掉，不再生成 `closed through #...` 这类重复尾句；
- 已新建 `S0E-6F` 作为 issue body 字段归属微调 follow-up：目标只收两件事，`Metadata` 去掉 `Source log`，以及 `Links` 增加可选 `Previous log`，并把 renderer / gate / runbook / validation 的后续实施措施集中到同一条 log；
- `S0E-6F` 已完成 `P0-P1`：issue draft rendering、issue conclusion preview、lifecycle audit、`S0E-2D` / `S0E-2E` / `S0E-5D` owner wording 与 runbook 现已一起切到新边界，不再把 `Source log` 当作 `Metadata` 行；
- `S0E-6F` 已完成 `P2`：代表性 draft/conclusion artifacts 已重生成，当前 `10` 条 closed `S0E` child issues 也已完成 bounded live refresh，post-refresh lifecycle audit 现为 `10/10 pass`；
- `S0E-6F` 已完成 `P3` 并继续保持 `stable`：当前 contract 已进一步显式区分 top-level parent issue 与 child issue，live parent issue `#248` 现已回写到 parent-aware body shape，且扩展后的 `11` 条 `S0E` parent-plus-child issues 已通过同一份 post-refresh lifecycle audit；
- 已新建 `S0E-4F` 作为下一条 PR-body follow-up：目标是去掉 PR body 里重复的 `Development Link` 与 `Links -> Issue`，并对当前 `17` 条 live `S0E` PR 做一轮显式全量审查；
- `S0E-6C` 已完成并进入 `stable`：issue `Context` 现已固定 main/child 两档英文句子合同，issue draft / issue conclusion / lifecycle audit 也已接到同一规则上，`#309` 已通过真实重写与 re-audit；
- `S0E-5C` 的真实链路现已打通：issue `#309` 不再停留在 issue-only sample，PR `#310` 已创建并合并，inline post-apply verification 已通过，final issue conclusion 也已写回 closed issue；
- `S0E-5D` 已完成 `P0`：canonical issue creation / issue conclusion / PR body families 已固定，`Metadata` 一类子条目不允许夹空段，且 Evidence Footer 已先锁定为 drills/evidence-only 并禁止 commit-footer fallback；
- `S0E-5D` 已完成 `P1`：Evidence Footer 现已固定为只读取 `PR Summary Inputs (optional)` 下的 `Evidence Footer Source`，并且唯一允许的行型要求阶段串与 artifact 路径串都使用反引号；
- `S0E-5D` 已完成 `P2`：section order、metadata 空段规则、allowed link categories、Evidence Footer presence/shape 现已进入 hard gate，可用 pass/stop fixture 机械验证；
- `S0E-5D` 已完成 `P3` 的边界收口：historical rewrite 执行明确挂到新 `P4`，先做代表性历史 PR rewrite，再做历史 closed issue rewrite；
- `S0E-5D` 已完成 `P4`：代表性历史 merged PR `#299/#302/#306/#308` 与 closed issue `#293/#295/#297/#300/#303/#305/#307` 都已在 live GitHub 上按 canonical contract 回写，并分别通过 PR contract verifier 与 lifecycle audit，因此该 slice 现已 `stable`；
- `S0E-6A` 已完成并进入 `stable`：双轨证据模型已固定，parent/phase templates 已回写 guidance，代表性混合块样本 `S0E-5C` / `S0E-4C` 已迁移，且本地 issue draft sample 也已生成；
- `S0E-5C` 已接手并完成 create-path 内联 post-apply verify wiring，而 GitHub Actions ownership 现在只剩 secondary enforcement 的后续可选项，因为 primary publish-time verification 已落在本地 create path；
- `S0E-2E` 已完成 `P0-P1`：issue conclusion 现已明确区分 GitHub auto-close 与 final body write-back，exact-ID merged PR 选择和多 PR 排序规则也已固定；
- `S0E-2E` 已完成 `P2`：issue conclusion dry-run planner 现已能从 manifest 读取显式 issue refs，查询 exact-ID merged PR evidence，并生成 final body preview；
- `S0E-2E` 已完成 `P3`：真实 apply 路径现已把 `#297` 的 final conclusion body 写回到 GitHub，并在该 issue 仍为 open 时显式关闭为 `completed`；
- `S0E-2E` 已完成新的 format revision cycle：最终 issue body 不再渲染 `Development`，而是让 `DoD` 只保留 `#298` / `#296` 这类短 PR refs；
- `S0E-4C` 已建档：下一轮 follow-up 将集中处理 PR `Summary` 必填化、`Development issue` 短引用一致性，以及 child issue `Relationships` 的真实 attach 路径；
- `S0E-4C` 已完成 `P0-P1`：PR preview/create 路径现已统一 `Development issue` 的短引用格式，live PR create 也会对 placeholder `Summary` fail-closed，而 child issue sidebar `Relationships` 已具备独立 apply 脚本；
- `S0E-4C` 已完成 `P2`：`S0E-2D` 的 PR-prep 样本现已带真实 Summary bullets，`S0E` child issue `#295` 的 relationship plan/apply 样本也已验证幂等 attach 行为；
- `S0E-4C` 已完成 `P3-C1-S1/S3`：历史 merged PR `#294/#296/#298/#299` 已完成审查，其中 `#296` 已回写为短引用 `Development issue: #295`，`#298` 已回写为非占位 Summary + 独立 `Development Link`，而 `#294` 与 `#299` 已确认符合当前规范；
- `S0E-4C` 已完成 `P3-C1-S2` 与 `P4`：真实 issue `#300` 已创建并挂到父 issue `#248`，PR `#301` 已从 clean `pr-prep/s0e-4c` 分支创建并合并，最终 conclusion 也已写回到 closed issue，因此 creation / PR / relationship / conclusion 四段现已在同一真实样本上完成闭环；
- `S0E-4C` 在闭环 drill 中顺手修正了 PR-prep 的 base 选择：dry-run commit selection 现在会优先对齐 `origin/<base>`，避免 stale local base 和 real create-path 的 remote base 发生漂移；
- `S0E-4C` 已完成 `P5`：`create_pr_from_plan.py` 在真实 `#302` 路径中已验证，当 long-lived mixed branch 的 raw cherry-pick 在 `18fbfe40` 处冲突时，会自动改走 source-head snapshot 构建 clean prep branch，而不是直接失败；
- `S0E-4C` 的 closed issue `#300` 也已再次回写，当前 DoD 明确列出 `#301` 与 `#302` 两条 merged PR；
- `S0E-4C` 已完成 `P6`：`plan_pr_prep.py` 现已把 title、`Execution Checklist`、`Evidence Footer` 的 scope 统一到同一选择器上，`S0E-4B` 样本与历史 merged PR `#296` 也已按新规则重写；
- `S0E-4C` 已完成 `P7`：merged PR body 现在可以按最终 title scope 重放 `Execution Checklist` 与 `Evidence Footer`，因此 `#301` 与 `#302` 的历史 drift 也已被定向修复；
- `S0E-2E` 现在可视为 `stable`：contract、dry-run planner、real write-back 与 attached PR accounting 都已完成闭环；
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
- `S0E-4B/P3-C1-S7` 已完成：stacked PR 的 review 口径现已明确收口到 compare base 和 `Files changed`，GitHub timeline 里重复出现的上游 commits 只作为 ancestry traceability 读取；
- `S0E-4B/P3-C1-S8` 已完成：aggregate PR title 现在优先按 source log 的完成 checklist 覆盖范围生成，因此像 `S0E-4B` 这种“创建时已完成 `P0-P2`、实现阶段完成 `P3`”的 log 不会再被错误显示成只做了 `P3`；
- `S0E-4B/P3-C1-S9` 已完成：`S0E-docs-management-v5` 继续作为 mixed authoring branch 和 parent-log ledger 落点，而 `pr-prep/*` 被明确限定为单次评审用的短生命周期分支；
- `S0E-4B/P3-C1-S10` 已完成：真实 issue `#295` 现已确认落在 `wordloom Board`，此前的 project write-scope 阻塞已被实际消除；
- `S0E-4B/P3-C1-S11` 已完成：在上游 `#294` 合并后，live PR `#296` 已从临时 stacked base 对齐回 `main`；
- `S0E-4B` 现在可视为 `stable`，因为 issue project、PR title、body 结构、以及 post-merge base realignment 都已完成验证；
- 既然 `S0E-4B` 的 PR follow-up 已收口，当前最自然的回流路径就是继续推进 `S0E-2D` 与 `S0E-2E`，把 issue create 和 issue conclusion 两端重新接回已经稳定的 roadmap/PR contracts。

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
- `S0E-*` 顶层工作分支的职责是承接 mixed authoring：parent/spine log 记账、多个 child logs 的并行推进，以及尚未切成独立 review slice 的 contract 更新；
- `pr-prep/*` 分支是从某个明确 base 派生出来的 review-only 分支，只承载某一条 PR 要送审的选中提交，不替代顶层工作分支；
- 如果是 parent/spine log 自身的持续记账内容，默认先落在 `S0E-*` 顶层工作分支，而不是为 parent log 再额外常驻一条新的总分支；
- 若后续实现拆成 template rollout 与 generator validation 两条并行路径，可在 `S0E-*` 之下临时开短生命周期分支，但默认不为每个子 log 再开常驻顶层分支。

**Commit 纪律（建议）**:

- 完成每个 `P*-C*-S*` 的关键内容后，应在 `S0E-*` 分支上及时 `commit/push`；
- 推荐节奏：先把 contract、template、validation 按 step 粒度切成小 commit，再从 `S0E-*` 分支向 `main` 发起 PR。
- 当某个 child log 需要独立评审时，再由 `S0E-*` 顶层工作分支通过 PR-prep 规则切出 `pr-prep/*`；如果只是 parent/spine 的滚动 ledger 更新，则继续留在 `S0E-*` 顶层工作分支即可。

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
- 2026-03-29：补充了 stacked PR review 语义、aggregate PR title 的 phase-span 优先级，以及 mixed working branch / parent-log 落点规则，避免把 GitHub ancestry-heavy commit 视图误读成真实增量范围。
- 2026-03-29：`S0E-4B` 的真实 issue `#295` 已确认挂到 `wordloom Board`，并且 live PR `#296` 已在上游合并后重新对齐到 `main`，因此这条 follow-up 已基本完成收口。
- 2026-03-29：新增 `S0E-2D` 与 `S0E-2E` 两条 follow-up logs，把 enriched issue creation 和 post-merge issue conclusion 明确拆成两个独立 contract，而不再只停留在口头记忆里的“2D/2E”。
- 2026-04-01：`S0E-7B/P1` 已完成：新增 attribution resolver entrypoint，并固定 normalized PR payload snapshot + attribution result JSON 这对 retained artifact paths，为后续 `S0E-7A` consume-or-stop 接线提供直接输入。
- 2026-04-01：`S0E-7B/P2-P3` 已完成：GitHub Actions workflow 现已先做 attribution 再分流到 continue-or-stop，同时 repo 也已补齐 resolved / stop 两类 representative samples 与 sample manifest，因此 `S0E-7B` 现可视为 `stable`。
- 2026-04-01：新增 `S0E-7C`，并完成 historical log review planner、representative sample manifest/plan 与 manual mirror workflow，为旧 logs 的批量审查和后续 targeted backfill 提供 review-first 入口。
- 2026-04-01：`S0E-7C/P4` 已完成第一轮 full-series backlog + live Actions enablement：`#311` 已把 mirror workflow 挂到默认分支，`run 23827006381` 证明了 dispatch visibility，而 `run 23827100968` 已在 `S0E-docs-management-v5` 上成功保留第一条 full-series replay evidence。
- 2026-04-01：`S0E-7C/P4-C1-S3` 已完成：focused PR `#312` 已移除 planner 在 `main` 上的 runtime closure 缺口，随后 `run 23827684652` 已在默认分支成功完成 full-series historical review replay。
- 2026-04-01：`S0E-7C/P4-C1-S4` 已完成：截图范围内全部已关闭 `S0E` 子 issues 都已重新检查并重跑 conclusion，`9/10` 条失效 `Context` 已批量修复，后续 lifecycle audit 也已对 `10/10` 子 issues 给出 `pass`。
- 2026-04-01：新增并完成 `S0E-6D`，issue `Context` contract 已从 rigid sentence-slot template 升级为 natural-summary renderer + weak deterministic gate，并把 draft / conclusion / lifecycle audit 三条路径统一到同一规则。
- 2026-04-01：`S0E-7C/P4-C1-S5` 已完成：刚才审查过的 `10` 条 closed `S0E` 子 issues 已按 `S0E-6D` 的 natural-summary `Context` 规则重写，并再次通过 `10/10` lifecycle audit。
- 2026-04-01：根据 operator review，`S0E-6D` 已新增 `P4`，后续将继续把 `Context` gate 收缩为 prose-first 弱约束，并把 renderer 改成 fact-pool + style-family，而不再停留在 template-shaped natural-summary。
- 2026-04-01：`S0E-6D/P4-C1-S1` 已完成：`Context` gate 现已收缩为 prose-first 弱约束，只检查 `3-5` 条可读英文句子行、基本完整性和 placeholder hygiene，不再强制 prose anchors。
- 2026-04-01：`S0E-6D/P4-C1-S2` 已完成：issue `Context` renderer 现已切到 `fact pool + style family`，preview bodies 已开始按不同 issue 变化句子顺序和 lead sentence，而不再共享同一条 sentence-slot 骨架。
- 2026-04-01：`S0E-6D/P4-C1-S3` 已完成：刚才那 `10` 条 closed `S0E` 子 issues 已按 fact-pool/style-family renderer 完成 live replay，并再次通过 `10/10` lifecycle audit；`S0E-6D` 也因此重新回到 `stable`。
- 2026-04-01：新增并完成 `S0E-6E`，`Context` 现在明确改成“单条生成、批量保留”的边界：新增单条 `Context` draft 脚本，issue draft 默认回到 scaffold，而 batch issue-conclusion 计划默认只保留 live `Context` 并报告 drift。
- 2026-04-01：`S0E-6E/P4-C1-S1` 已完成：`S0E-2B/#288` 与 `S0E-2A/#289` 已按新的单条 authoring 路径逐条优化 live `Context`，并再次通过 lifecycle audit。
- 2026-04-01：补充 final issue-conclusion wording 约定：若结案 body 同时保留 `Context` 与 `DoD`，则 `Context` 末句改为描述 slice 留下的结果/基线，精确 PR 证据只保留在 `DoD`。
- 2026-04-01：`S0E-6E/P4-C1-S2` 已完成：其余已关闭 `S0E` 子 issues 也已统一改写为 outcome-ending `Context`，同时单条 conclusion generator 的默认结尾不再重复 `DoD` 里的 PR evidence wording。
- 2026-04-02：新增 `S0E-6F`，用于把 issue body 的字段归属进一步收紧为“状态留在 Metadata，导航留在 Links”：本轮 follow-up 的明确目标是移除 `Metadata` 中的 `Source log`，并为 `Links` 增加可选 `Previous log`，同时预先记住 renderer / gate / runbook / validation 的实施路径。
- 2026-04-02：`S0E-6F/P0-P1` 已完成：issue create / conclusion 的 renderer、lifecycle audit 的 link-boundary 检查，以及 `2D/2E/5D` owner wording 与 runbook 现已全部对齐到新规则，后续只剩 representative artifacts 与 live-reconciliation scope 决策。
- 2026-04-02：`S0E-6F/P2` 已完成：`6F` representative draft/conclusion artifacts 已生成，live reconciliation scope 已固定为当前 `10` 条 closed `S0E` child issues，并已完成 bounded refresh 与 `10/10` post-refresh lifecycle audit。
- 2026-04-02：`S0E-6F/P3` 已完成：issue body contract 现已显式区分 top-level parent 与 child issue，`#248` 已刷新为 parent-aware body shape，且扩展后的 `11` 条 `S0E` parent-plus-child issues 已通过同一份 post-refresh lifecycle audit。
- 2026-04-02：新增 `S0E-4F`，用于收口 PR body 的两处重复面：去掉独立 `Development Link` section，并把 `Links` 里的 `Issue` 行移除，随后对当前 `17` 条 live `S0E` PR 做一轮显式全量审查。
- 2026-04-01：新增并完成 `S0E-6C`，issue `Context` 现已固定为 main log `5` 句 / child log `4` 句的英文单句逐行合同；`#309` 也已在真实 conclusion replay 后通过新的 lifecycle audit gate。
- 2026-04-01：完成 `S0E-5C` 的真实 lifecycle follow-through，PR `#310` 已创建并合并，issue `#309` 已完成 final body write-back；当时的 GitHub Actions mirror dispatch 也据此暴露出“workflow 需先对默认分支可见”这一前置条件，并在后续 `S0E-7C/P4` 中被正面解决。
- 2026-04-02：新增 `S0E-7D`，作为 `S0E-7C` historical review 和 `S0E-4F` metadata backfill 之后的 failure-semantics follow-up，后续将集中收口强/弱结构化 failure taxonomy、replay/backfill 顺序以及 `block/replayable/manual/reconciliation` handling semantics。
- 2026-04-02：`S0E-7D/P0-P1` 已完成：第一份 failure taxonomy / mapping artifact 已落地，当前 docs/GitHub workflow 的主要 drift surfaces 现已显式归类到 strong/weak structure 与四类 handling semantics。
- 2026-04-02：`S0E-7D/P2-P3` 已完成：现在已有覆盖四类 handling semantics 的 representative manifest / audit summary，同时 replay-only remediation contract、mixed-batch split 规则和 post-apply verify stop rules 也已固定为结构化证据。
- 2026-04-02：`S0E-7D/P4` 已完成：future `publish-verify-remediation gate` 的名称、决策词汇、adapter reuse 边界与非目标面现已固定，后续若实现统一入口，只需要做一层薄编排而不是重写既有 guarded adapters。
- 2026-04-02：`S0E-7E/P0-P1` 已完成：thin gate contract artifact 已落地，新 planner 现已能统一一条 lifecycle-family `allow-apply` 样本和一条 `pr-create-preflight` `hard-fail-input` stop 样本的顶层 decision artifact，而不替换现有 family adapters。
- 2026-04-02：`S0E-7E/P2` 已完成：thin gate 现已能委托 issue-conclusion、issue-relationship、pr-body-rewrite 三条 guarded apply handoff，同时显式拒绝把 `pr-create-preflight` 扁平化成 create 后半段 apply。
- 2026-04-02：`S0E-7E/P3` 已完成：thin gate 现已保留 representative issue-side pass、PR-side pass、`pr-create-preflight` planning-only stop，以及 delegated-apply rejection 的结构化 ledger，因此 `P4` 只剩 future wrapping boundary 的 follow-up。
- 2026-04-02：`S0E-7E/P4` 已完成：thin gate 的 local/publish-time/CI wrapping boundary 与 summary-only post-apply verify exposure 现已固定，因此该入口后续只需在这些边界内被接入，而不必再重谈 family-owned semantics。
- 2026-04-02：新增 `S0E-7E`，作为 `S0E-7D/P4` 的直接实现 follow-up，后续将把 future `publish-verify-remediation gate` 从命名 surface 落成一个薄编排入口，并复用现有 issue/relationship/PR guarded adapters。
- 2026-03-29：完成 `S0E-2D/P1`，issue draft 生成器已切换到 enriched metadata precedence，并且不再把 source log 的中英文 bullets 直接灌进 GitHub issue body。
- 2026-03-29：完成 `S0E-2D/P2`，`S4E-5B` 与 `S4A-1A` 的 enriched draft 样本已验证 roadmap milestone 解析与关系字段缺失时的保守留空。
- 2026-03-29：完成 `S0E-2D/P3`，历史真实 issue `#288` 已按当前 creation body contract 审核并回收，当前 `S0E-2D` 也已成功创建真实 sample issue `#297` 并完成 write-back。
- 2026-03-29：完成 `S0E-2D` 的 parent-issue follow-up：`S0E` 顶层 issue `#248` 已写回 parent spine，child issue 现可通过 `parent_log.links.issue` 自动继承父级，而顶层 issue draft 已验证不会出现 `Parent issue` 行。
- 2026-03-29：完成 `S0E-2D` 的 parent-issue format follow-up：`Parent issue` 现已收口为 `Metadata`-only 且使用 `#248` 这类短引用，`Links` 不再重复该字段。
- 2026-03-30：完成 `S0E-2E/P0-P1`，当前 contract 已固定 post-merge conclusion 的 lifecycle boundary、exact-ID merged PR selection，以及 final English issue-conclusion body shape；下一步进入 dry-run planning 和一次真实 closed-issue write-back 验证。
- 2026-03-30：完成 `S0E-2E/P2`，新增 manifest-driven issue-conclusion dry-run planner，并用 `#293/#295/#297` 验证了 single-PR 与 multi-PR conclusion body preview。
- 2026-03-30：完成 `S0E-4C/P3-C1-S1S3`，已审查历史 merged PR `#294/#296/#298/#299`，并把仍有 body drift 的 `#296`、`#298` 回写到当前 PR contract；下一步进入 `P4` 做 creation -> PR -> conclusion 的闭环 drill。
- 2026-03-30：完成 `S0E-4C/P3-C1-S2 + P4`，真实 issue `#300`、PR `#301`、relationship attach 与 issue conclusion 已形成一条完整闭环，`S0E-4C` 因而进入 `stable`；同时修正了 PR-prep planner 对 stale local base 的依赖，令 dry-run 与 real create-path 都以 remote-tracking base 为准。
- 2026-03-30：完成 `S0E-4C/P5`，`create_pr_from_plan.py` 现已在真实 `#302` 路径上证明可从 cherry-pick conflict 自动回退到 source-head snapshot；issue `#300` 也已随之更新为包含 `#301/#302` 的最终 DoD ledger。
- 2026-03-30：完成 `S0E-4C/P6`，PR body 现已按 title scope 同步收紧 `Execution Checklist` 与 `Evidence Footer`，并已把历史 merged PR `#296` 的 title/body metadata 回写到新规则。
- 2026-03-30：完成 `S0E-4C/P7`，新增 merged-PR scope replay helper，并已把历史 merged PR `#301/#302` 的 checklist/evidence drift 回写到与最终 title 一致。
- 2026-03-30：完成 `S0E-2E/P3`，新增 real apply 脚本并完成 `#297` 的线上 body write-back 与 explicit close，因此 issue conclusion 这条线已形成端到端闭环。
- 2026-03-30：完成 `S0E-2E` 的新一轮 format revision：最终 body 去掉 `Development`、DoD 改为短 PR refs，并以 `#295` 作为第二条真实 closed sample 完成回写验证。
- 2026-03-30：新增 `S0E-4C`，用于集中处理 PR `Summary` 占位符、`Development issue` 短引用，以及 issue sidebar `Relationships` 与 `Parent issue` 元数据未对齐的问题。
- 2026-03-30：完成 `S0E-4C/P0-P1`，PR create 现已对 placeholder `Summary` fail-closed、Development issue 统一为短引用，且 child-parent sidebar relationship 已具备独立 apply 路径。
- 2026-03-30：完成 `S0E-4C/P2`，已为 `S0E-2D` 重生成无 placeholder 的 PR-prep 样本，并为 `#248 -> #295` 产出正式 relationship plan/apply 样本。
- 2026-03-30：新增 `S0E-4D`，把 `review-hold` / `full-auto`、默认 human-gated handoff，以及 staged review 与 full closed-loop 的命令口径独立收口到 lifecycle orchestration follow-up。
- 2026-03-30：完成 `S0E-4D/P2`，明确 staged review、resume-after-review 与 post-merge full-auto 三类命令口径，并补齐 ambiguous / blocked request 的 fail-closed examples。
- 2026-03-30：完成 `S0E-4D/P3`，创建 live issue `#303`、draft-to-merged PR `#304`、parent relationship attach 与 final issue conclusion，证明 staged review 和 resumed closed loop 已可落到同一真实样本。
- 2026-03-30：扩展 `S0E-4D/P3` 历史验证轮次，已把 `S0E-2A/#289`、`S0E-2B/#288` 与 `S0E-4A/#293` 这三条仍未 conclusion 的旧 issue 按 exact-ID merged PR 证据完成回写并关闭。
- 2026-03-30：完成 `S0E-4D/P3-C4` 与 `P4`，审计 representative child issues 的 live sidebar relationships，补齐 `#248 -> #289/#293/#297`，并正式记录 issue body 与 GitHub relationship 需分开核验的审计边界。
- 2026-03-30：新增 `S0E-5A`，把 lifecycle audit gate 从 `review-hold / full-auto` 之外独立抽出来，并完成第一版 manifest-driven dry-run planner 与 representative sample 验证。
- 2026-03-30：完成 `S0E-5A/P3`，新增 `plan_lifecycle_remediation.py`，把 archived historical lifecycle defects 转成可复用的 relationship / issue-conclusion dry-run manifests，作为下一步真正前置 gate 的修复规划层。
- 2026-03-30：完成 `S0E-5A/P4`，新增 `plan_lifecycle_pre_gate.py`，把 audit / decision / remediation planning 串成统一 pre-gate 入口，并固定 warning 为 stop-and-plan-remediation 的 gate 决策。
- 2026-03-30：完成 `S0E-5A/P5`，新增 `apply_issue_conclusion_with_pre_gate.py`，把 pre-gate 真正接到 issue-conclusion mutation 前面，并完成 live pass->apply 与 frozen stop-before-apply 两条验证路径。
- 2026-03-30：完成 `S0E-5A` 的真实 create-issue -> PR -> merge -> relationship -> conclusion 闭环，live issue `#305` 与 merged PR `#306` 已形成完整样本。
- 2026-03-30：新增 `S0E-5B`，用于承接 guarded apply 从单一 issue-conclusion 路径向更多 lifecycle mutation families 的扩展。
- 2026-03-30：完成 `S0E-5B/P0-P1`，新增 guarded relationship attach 入口，并已用 live issue `#307` 与 frozen mixed-remediation stop drill 验证 targeted-remediation continuation 规则。
- 2026-03-30：完成 `S0E-5B/P2`，新增 guarded PR-body rewrite 入口，并已用 converged `S0E-5A/#305 -> #306` 的 live rewrite 与一条 frozen stop drill 验证 allow-apply-only 语义。
- 2026-03-30：完成 `S0E-5B/P3`，`#307 -> #308` 现已作为代表性真实样本完成 relationship attach、PR merge、guarded PR body rewrite 与 final issue conclusion 的组合闭环。
- 2026-03-30：将 `S0E-5B` 正式标记为 `stable`，并新增 `S0E-5C` 用于单独处理 guarded `PR create` 的细分问题，而不把它直接压进既有 guarded in-place mutation slice。
- 2026-03-30：完成 `S0E-5C/P0`，把当前 `PR create` path 拆成 7 个显式阶段，并固定 local branch materialization、remote branch publish、live PR publish、post-create evidence finalization 之间的 failure boundaries。
- 2026-03-30：完成 `S0E-5C/P1`，把 7 个阶段固定到 reuse-vs-new-rule 边界图中，结论是只有 create preflight 可部分复用现有 lifecycle pre-gate，而 local materialization、remote publish、live PR publish 仍需独立边界或人工持有。
- 2026-03-30：完成 `S0E-5C/P2`，新增 bounded front-half preflight 入口并用 live issue `#309` 记录一条 pass sample 和一条 create-specific branch-collision stop sample，两条路径都止步于 `S4` 之前。
- 2026-03-31：新增 `S0E-5D`，用于单独收口 body contract、Evidence Footer 低基数规则，以及 hard gate 应新增的 body-shape 审核项。
- 2026-03-31：完成 `S0E-5D/P0`，把 operator 给出的格式规则写成 canonical body spec，并将 Evidence Footer 的适用范围先锁定为 drills/evidence-only 且禁止 commit-footer fallback。
- 2026-03-31：完成 `S0E-5D/P1`，把 `Evidence Footer Source` 的唯一来源、唯一行型和 inline-code 规则正式固定，为后续 hard gate body-shape checks 提供可机器验证的输入合同。
- 2026-03-31：完成 `S0E-5D/P2`，实现 shared body-contract gate、切断 footer 推断回退路径，并用 pass/stop fixture 证明 canonical footer、未加反引号 footer 和错误来源块都能被机械区分。
- 2026-03-31：完成 `S0E-5D/P3`，固定 rollout 策略为 `gate-first + post-apply live verify + selective historical rewrite`，并新增 live PR verifier 与 footer eligibility reject 规则，为后续 GitHub Actions 接线提供执行面。
- 2026-03-31：进一步收口 `S0E-5D/P3` 边界，明确 `rewrite` 挂到新 `S0E-5D/P4`，而后置 gate / post-apply verify / GitHub Actions ownership 延后到 `S0E-5C/P3` 处理。
- 2026-03-31：完成 `S0E-5D/P4`，已把代表性历史 merged PR `#299/#302/#306/#308` 与 closed issue `#293/#295/#297/#300/#303/#305/#307` 回写到 canonical contract，并通过 live PR verifier 与 lifecycle audit 证明 `S0E-5D` 的 selective historical rewrite 已收口。
- 2026-03-31：新增 `S0E-6A`，用于把 logs 的结构问题从 body contract 本身拆出来，正式定义 `Evidence Footer Source` 和 `Evidence` 双轨并存的 contract，以及后续 parent/phase templates 的优化边界。
- 2026-03-31：完成 `S0E-6A/P3-P4`，已把 parent/phase templates 回写为双轨证据 authoring 规则，迁移代表性旧样本 `S0E-5C` / `S0E-4C`，并生成 `S0E-6A` 的本地 issue draft sample，因此 `S0E-6A` 现已进入 `stable`。
- 2026-03-31：完成 `S0E-5C/P3`，现已固定 `S6` live PR publish 继续为 operator-held boundary，post-apply live verify 位于 `S6` 之后、`S7` 之前，而 GitHub Actions verification 只作为后续 secondary enforcement；因此 `S0E-5C` 现已进入 `stable`。
- 2026-03-31：完成 `S0E-5C/P4`，现已把 reusable live PR verifier 直接接入真实 `create_pr_from_plan.py` 执行链路，并用历史样本 `S0E-5B/#308` 非破坏性验证 `S6 -> live verify -> S7` 顺序与结果落盘行为。
- 2026-03-31：新增 `S0E-6B` 并完成 `P0`，已先收口本地 AI-authored logs 的 gate 与 `stable` 后验 gate 策略，作为后续 local deterministic checks 的前置合同。
- 2026-03-31：完成 `S0E-6B/P1`，已把第一版 local deterministic checks 与最小 failure taxonomy 正式收口，后续 `P2` 可直接转向 automation entrypoint gating。
- 2026-03-31：完成 `S0E-6B/P2`，已把第一轮 hard-require gate entrypoints 与 advisory-only rollout boundary 固定下来，可继续进入 `stable` transition gate 设计。
- 2026-03-31：完成 `S0E-6B/P3`，已把 `stable` promotion 需要的更强 contradiction/hygiene checks 与 local-first / CI-mirror-later execution policy 固定下来，因此本地 log stability policy 已能独立定义“何时可信地标记 stable”。
- 2026-03-31：重构 `S0E-7A` 的职责边界，现仅保留 GitHub Actions secondary enforcement、artifact publishing 与 failure surfacing 相关内容。
- 2026-03-31：完成 `S0E-7A/P1`，已新增第一版手动触发的 mirror-verifier workflow，并固定 secondary-enforcement summary wording 与 artifact-first fail path，为后续 `P2/P3` 留出 retained-evidence 与 rollout boundary 的独立决策空间。
- 2026-03-31：完成 `S0E-7A/P2`，已为 mirror-verifier workflow 固定 retained artifact set、artifact manifest JSON，以及 workflow summary + check annotations + retained evidence 的三层 failure surfacing 结构。
- 2026-03-31：完成 `S0E-7A/P3`，已明确第一轮 rollout 继续保持 manual-only，并把未来自动 PR-event mirroring 所需的 attribution 前提与 CI adoption success criteria 一并写成显式合同。
- 2026-03-31：新增 `S0E-4E` 并完成 `P0`，已把 `PR event -> source_log_path` attribution 正式拆成独立 slice，并重新归类到 PR-family follow-up；后续自动触发扩大前必须先在这里收口 deterministic ownership contract。
- 2026-03-31：完成 `S0E-4E/P1`，已把 attribution candidate surfaces 收口为 explicit provenance / canonical PR-body `Log:` row / exact-ID branch fallback 三类，并固定 precedence 为前者优先、后者仅作缺失时的受限补位。
- 2026-03-31：完成 `S0E-4E/P2`，已把 attribution ambiguity 收口为 missing / conflicting / multi-candidate / invalid-shape 四类 fail-closed stop 条件，并固定至少一条 deterministic sample 与一条 ambiguity stop sample 的代表性期望。
- 2026-03-31：完成 `S0E-4E/P3`，已把 `4E -> 7A` 的 attribution result payload 与 limited rollout unblocking criteria 固定下来，后续自动 PR-event mirroring 可以在 consume-or-stop 边界上接线，而无需重议 attribution ownership。
- 2026-04-01：新增 `S0E-7B` 并完成 `P0`，已把 attribution payload implementation、`7A` consume-or-stop 接线，以及 resolved/stop 端到端样本验证独立成新的 GitHub-side follow-up。