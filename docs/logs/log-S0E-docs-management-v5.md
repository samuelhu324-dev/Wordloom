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
  **phase_log_7**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **phase_log_8**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **phase_log_2**: `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  **phase_log_3**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **phase_log_4**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **phase_log_5**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **phase_log_6**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
**created**: `2026-03-28`
  **updated**: `2026-03-30`

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
- `S0E-4C`（Phase 4C）：PR summary / development issue rendering / issue relationship attach follow-up
  - 详见：`docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
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
- `S0E-5C` 的下一步将进入 `P3`：基于这个 bounded front-half 结果，决定是否只继续深化 `S4/S5` 的 targeted rules，同时把 `S6` 长期保留为 operator-held boundary；
- `S0E-5D` 已完成 `P0`：canonical issue creation / issue conclusion / PR body families 已固定，`Metadata` 一类子条目不允许夹空段，且 Evidence Footer 已先锁定为 drills/evidence-only 并禁止 commit-footer fallback；
- `S0E-5D` 已完成 `P1`：Evidence Footer 现已固定为只读取 `PR Summary Inputs (optional)` 下的 `Evidence Footer Source`，并且唯一允许的行型要求阶段串与 artifact 路径串都使用反引号；
- `S0E-5D` 已完成 `P2`：section order、metadata 空段规则、allowed link categories、Evidence Footer presence/shape 现已进入 hard gate，可用 pass/stop fixture 机械验证；
- `S0E-5D` 已完成 `P3` 的边界收口：historical rewrite 执行明确挂到新 `P4`，先做代表性历史 PR rewrite，再做历史 closed issue rewrite；
- `S0E-5D` 已完成 `P4`：代表性历史 merged PR `#299/#302/#306/#308` 与 closed issue `#293/#295/#297/#300/#303/#305/#307` 都已在 live GitHub 上按 canonical contract 回写，并分别通过 PR contract verifier 与 lifecycle audit，因此该 slice 现已 `stable`；
- `S0E-5C` 将在后续 `P3` 接手 post-apply verify / Actions ownership，原因是这部分更贴近 `S6/S7` live publish boundary，而不是 `S0E-5D` 的 contract normalization 本身；
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