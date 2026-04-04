# log-S0F（Docs Management v6：fail-closed docs/GitHub lifecycle entrypoints）

---

**id**: `S0F-docs-management-v6`
**kind**: `log`
**title**: `docs management v6 (fail-closed docs/GitHub lifecycle entrypoints) v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, epic/s0, sub/0f`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/363`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **reference_log_1**: `docs/logs/log-S0E-docs-management-v5.md`
  **reference_log_2**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **reference_log_3**: `docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
  **reference_log_4**: `docs/logs/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
  **phase_log_1**: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  **phase_log_2**: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
**issue_keyword**: `automation`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/0`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome（结论区）

**Decision**:

- 启动 `S0F` 作为 docs-management v6 的新 spine，专门处理 `issue creation -> PR -> conclusion` 这一整条 docs/GitHub 生命周期里仍然存在的 warning-first、guess-first 和绕过 gate 的入口问题。
- v6 的首要目标不是继续扩写功能，而是把现有入口收口成 fail-closed：输入不明确时停止、结构不完整时停止、需要人工 authoring 的弱结构问题不得伪装成可自动重试。

**Default choices（默认基线 / v1）**（可选，但推荐在 parent/spine 明确）:

- v6 先修入口，再谈 CI 或 GitHub Actions；若本地 entrypoint 仍允许猜测和 warning-only continuation，则 CI 只会稳定重复错误。
- `issue creation`、`PR create`、`issue conclusion` 的 live mutation 必须逐步收口到受控 preflight/gate/wrapper 表面，不能继续依赖“直接调用 family script 也能跑”的裸入口。
- 允许 preview/dry-run 保留结构化 warning，但任何真实 create/apply/publish 动作都必须在 deterministic preflight 之后 fail-closed。
- 在 canonical keyword whitelist 真正落地前，`S0F` 线上的 `issue_keyword` 保持留空；真正的 issue creation 不应再因为空字段而自动推断 title keyword。
- 若 `issue_*` 字段为空，automation 必须保守留空并要求人工确认，而不是猜测 title keyword、labels 或 milestone。
- 若 `pr_*` 字段为空，PR automation 必须保守留空并显式报告缺口，而不是复制 issue metadata 或猜测 base / milestone / development issue。
- roadmap 与 logs 的机械桥接必须通过 `roadmap_path + roadmap_milestone + roadmap_phase` 明确声明；roadmap 内的正式 bridge ledger 默认只计入 child logs，而不是 parent/spine prose。
- `S0F` parent/spine 属于现有 `road-002` 的治理支撑面；这里补的是既有 milestone/roadmap 归属，不引入新的 milestone 或平行 roadmap。

**PR Summary Inputs（可选）**

- 仅当 parent/spine log 本身会作为 PR contract source 时填写；多数情况下，真正的 PR 描述仍应来自 child phase log。
- `PR Summary Inputs` 是 automation-facing contract；execution evidence 的人工账本仍应保留在 `Evidence` 或 child log 的证据段落中。
- parent/spine log 默认不应从 prose 聚合里直接合成 `Evidence Footer Source`；若证据实际属于 child logs，应优先在这里引用 child sources，而不是重写 child evidence ledger。

**Non-goals（不做什么）**（可选，但建议写）:

- v6 不把 prose 质量伪装成可重放修复项；`Context` 的自然语言质量仍然需要 single-item authoring 或明确的人类确认。
- v6 不把 GitHub Actions 当作主修复手段；CI 只在本地 fail-closed contract 成型之后作为 secondary enforcement 使用。
- v6 不把 docs/GitHub 家族压扁成一个“万能 super-command”；family-specific logic 仍然保持在各自 adapter 中。

## Background（背景）

- `S0E` 已经把 issue creation、PR automation、issue conclusion、failure semantics 和 thin gate 基本铺出来，但当前真实入口仍然混合了三类行为：严格 gate、warning-only preview，以及直接 mutate live state 的 family 脚本。
- 最近这一轮问题暴露出，`issue_keyword` 推断、scaffold Context、PR preview placeholder、以及 issue conclusion live apply 绕过 gate 等路径仍可能让输出“结构上可跑、语义上不够严”。
- 如果不先把入口收成 fail-closed，后续不论是本地 wrapper 还是 GitHub Actions，都只能放大已有分叉，而不能解决 contract 漂移。

## Constraints（约束）

- 先修 deterministic entrypoints，再加 secondary enforcement。
- 不允许把 blank-as-blank contract 再次退回为 infer/fallback 行为。
- 不允许把 transient retry 和 semantic retry 混为一谈；语义失败必须修 source contract 后重跑，而不是盲 retry。
- 不允许把 weak-structure authoring 问题塞回批量 replay/apply。

## Scope（本 log 范围）

- 本 log 负责：
  - 固定 docs-management v6 的目标边界、默认基线与后续 phase 拆分；
  - 把 `fail-closed entrypoints`、`preflight/gate unification`、`wrapper consolidation`、`optional CI enforcement` 组织成一条新 spine；
  - 明确 `S0F-docs-management-v6` 作为当前 mixed authoring 分支。
- 本 log 不负责：
  - 直接替换所有现有 family adapter；
  - 在 parent/spine 层发明新的 prose summarization 规则；
  - 未经后续 child log 验证就直接接入 GitHub Actions mandatory path。

## Success Criteria（DoD）

- 结构层面：
  - 读者能在 30 秒内理解 v6 要解决的是“入口 fail-closed”，不是单纯增加更多自动化。
  - `S0F-1A` 能成为第一条直接承接 screenshot 问题的明确切片。
- 工程层面：
  - v6 至少固定一版 issue creation create-time hard-fail contract。
  - v6 至少固定一版 PR create preflight mandatory boundary。
  - v6 至少固定一版 issue conclusion / relationship / PR rewrite live mutation wrapper 边界。
- 证据层面：
  - 每条后续 child log 至少留下一轮 dry-run 或 live verification evidence，证明它没有重新引入 guess-first 行为。

## Phases（切片）

- `S0F-1A`（Phase 1）：fail-closed entrypoints and preflight unification
  - 详见：`docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- `S0F-1B`（Phase 1B）：LLM-authored issue Context generation and exact sentence-count contract
  - 详见：`docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
- `S0F-1C`（Phase 1C）：live mutation wrapper convergence for issue / PR families
  - 详见：``
- `S0F-1D`（Phase 1D）：optional GitHub Actions secondary enforcement rollout
  - 详见：``

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：`S0F` parent/spine created and scope boundary fixed
- [x] `P1`：`S0F-1A` created with the first concrete fail-closed cleanup scope
- [x] `P2`：issue creation create-time hard-fail boundary fixed
- [x] `P3`：PR create preflight becomes the only allowed live publish front-half
- [x] `P4`：issue conclusion / relationship / PR rewrite live mutation wrapper convergence fixed
- [x] `P5`：optional GitHub Actions secondary enforcement policy fixed after local entrypoints converge

## Current Status（进展摘要）

- `S0F` is now opened and pushed as docs-management v6 on branch `S0F-docs-management-v6`.
- The first active child slice `S0F-1A` is no longer just a placeholder: `P0` contract language is fixed and `P1` has already hardened the real issue creation entrypoint.
- The next child slice `S0F-1B` is now reserved for replacing deterministic issue Context templates with LLM-authored Context generation under an exact child/main sentence-count contract.
- The retained evidence now shows four hard boundaries in action: draft-generation still works while real `create-issue` stops on inferred keyword, PR preview planning still works while real `create_pr_from_plan.py` refuses to continue from a stop-state front-half preflight result, raw family apply scripts now fail closed unless they are invoked through the canonical guarded surfaces, and GitHub Actions surfaces are explicitly narrowed back to optional secondary enforcement after local contract ownership is already fixed.
- The corrected live rerun for `S0F-1A` now reaches the entire closed loop under the updated contract: create keeps `Context` structurally present but empty, PR `#365` merged successfully, and issue `#364` concluded through the guarded issue-conclusion surface after a targeted conclusion-owned remediation handoff.

## Evidence（可选，聚合型记账）

- parent/spine log 通常不是 execution evidence 的主记账面；若保留本节，默认应记录聚合性的 traceability，而不是重复 child log 的完整 drill ledger。
- 若 evidence 真正属于 child phase logs，应优先在本节引用 child log 或 child artifacts，而不是把 child 的 `expected/observed` 全量复制回 parent/spine。

### S0F-1A (first fail-closed issue-create sample | 2026-04-04)

- headSha: `ccdf702ff2d2c9aa12aeddff93cdaf0c0906aaae`
- artifacts:
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  - `scripts/issues/gen_issue_draft.py`
  - `docs/issues/issue-S0F-1A-create-preflight-fail.json`
  - `docs/issues/issue-S0F-1A-single-generate-draft.json`
- expected:
  - `S0F-1A` exists as the first concrete v6 child slice
  - real `create-issue` stops before GitHub mutation when `issue_keyword` would be inferred
  - draft-generation still produces a retained preview/result artifact under the same source log
- observed:
  - `S0F-1A` was created from the phase template and wired into the `S0F` parent spine
  - `gen_issue_draft.py --create` now fails closed on the blank `issue_keyword` path for `S0F-1A`
  - the same log still produced a single-generated draft/result artifact for review without crossing into live creation

### S0F-1A (first mandatory PR front-half preflight sample | 2026-04-04)

- headSha: `e2bf872b6bad67c4766ca15c0eebc496c27a8609`
- artifacts:
  - `scripts/issues/create_pr_from_plan.py`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-manifest.json`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-manifest-plan.json`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-manifest-front-half-preflight-result.json`
  - `docs/issues/pr-prep-S0F-1A-p2-stop-create-blocked-utf8.txt`
- expected:
  - real PR publish may no longer continue from plain `plan_pr_prep` output without a matching successful front-half preflight artifact
  - one retained stop sample proves preview planning can still succeed while live PR publish remains blocked before local branch materialization
- observed:
  - `create_pr_from_plan.py` now requires a matching `pr-create-front-half-preflight` result artifact and refuses live publish when that artifact is missing, mismatched, or not publish-eligible
  - the retained `S0F-1A` stop sample still produced a valid PR-prep plan and preview body, but front-half preflight stopped on the occupied `S0F-docs-management-v6` branch before any live publish stage
  - replaying `create_pr_from_plan.py` against that stop sample now exits non-zero with `PR create fail-closed preflight blocked publish before local branch materialization`, proving preview no longer implies publish eligibility

### S0F-1A (wrapper-only live mutation convergence sample | 2026-04-04)

- headSha: `e123c71f3ccb35ef07fd7a4c3ee0bde103ef7c52`
- artifacts:
  - `scripts/issues/raw_live_mutation_guard.py`
  - `scripts/issues/apply_issue_conclusion_from_plan.py`
  - `scripts/issues/apply_issue_relationships.py`
  - `scripts/issues/apply_pr_body_scope_with_pre_gate.py`
  - `scripts/issues/apply_pr_body_rewrite_batch.py`
  - `docs/issues/raw-live-mutation-S0F-1A-p3-inventory.json`
  - `docs/issues/issue-conclusion-S0F-1A-p3-raw-blocked.txt`
  - `docs/issues/issue-relationship-S0F-1A-p3-raw-blocked.txt`
  - `docs/issues/pr-body-rewrite-S0F-1A-p3-raw-blocked.txt`
- expected:
  - raw family apply scripts may remain for bounded internal reuse, but operator-facing live mutation must converge to guarded wrapper or thin-gate surfaces
  - one retained inventory plus one retained block sample per family proves raw issue-conclusion, issue-relationship, and PR body rewrite entrypoints no longer act as default live mutation surfaces
- observed:
  - raw issue-conclusion and issue-relationship apply scripts now fail closed unless a hidden internal-only flag is supplied by their guarded wrappers
  - raw PR body rewrite functions now fail closed outside the guarded single-PR rewrite path, while the historical batch rewrite script remains bounded internal reuse instead of an operator-facing default
  - the retained `S0F-1A` block samples now point operators at `apply_*_with_pre_gate.py` or the thin-gate `--delegate-apply` surfaces, proving wrapper-only convergence is enforced in code rather than only documented

### S0F-1A (GitHub Actions secondary-enforcement narrowing sample | 2026-04-04)

- artifacts:
  - `docs/issues/github-actions-secondary-enforcement-S0F-1A-p4-boundary.json`
  - `.github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
- expected:
  - after local fail-closed entrypoints converge, GitHub Actions remains an optional replay or drift-detection surface rather than the place where publish ownership is first decided
  - workflow-owned summaries and manifests state the local owner explicitly so a stop/error cannot be misread as CI having prevented publish
- observed:
  - `S0F-1A` now retains one explicit boundary artifact that classifies the thin gate and guarded local wrappers as the primary mutation boundary while classifying both audited GitHub workflows as secondary enforcement only
  - the read-only wrapper dispatch workflow now records `secondary_enforcement=true`, `local_primary_boundary=true`, and `publish_owner=local fail-closed family entrypoint` in its retained run manifest
  - the PR body mirror workflow now records `trigger_surface=workflow_dispatch`, `local_primary_boundary=true`, and a post-publish-only role note in its retained manifest while preserving attribution-stop semantics before mirror verification

## Notes（落地原则，可选）

- `S0F-docs-management-v6` is the current mixed authoring branch for this new spine.
- Future CI or wrapper work must stay downstream of local fail-closed contract fixes.
- GitHub Actions summaries and manifests must keep naming the local entrypoint as publish owner so a later workflow change cannot silently become the primary control plane.

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - v6 的默认基线、phase 拆分与 secondary-enforcement 边界已稳定；
  - 至少一条 child slice 已证明 local entrypoints 真正变成 fail-closed。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`<ID>/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。
  - Multi-step 规则：只允许在 **同一 Phase + 同一 Cycle** 下合并多个 step；一旦跨 Phase 或跨 Cycle，必须拆成多次 commit。
  - 若一个 PR 一次性汇总多个完整 phase，应优先压缩成 phase 范围标题：
    - 连续 phase：`<ID>/P0-P3: <log title>`
    - 离散 phase：`<ID>/P0+P3: <log title>`
    - 离散 + 连续混合：`<ID>/P0+P3-P4: <log title>`
  - 若是后续补充型 PR，而不是一次性 phase 汇总，则直接使用精确 unit：`<ID>/P*-C*-S*: <一句话 summary>`。

**Branch 约定（建议）**:

- parent/spine log 负责一个 scope/index（例如 `S0F`），对应的实现/phase logs（如 `S0F-1A`）默认应在与该 scope/index 同名前缀的分支上推进。
- 当前 `S0F` spine 的 mixed authoring branch 固定为 `S0F-docs-management-v6`。

**Commit 纪律（建议）**:

- 对于归属于 `S0F` 的 phase log：完成每个 `P*-C*-S*` 的关键内容后，应在 `S0F-docs-management-v6` 上及时 `commit/push`，避免再次出现本地分支领先远端而造成上下文不同步。

## Recent changes（for traceability，可选）

- 2026-04-04：初始化 `S0F`，把 docs-management v6 的问题定义为 fail-closed entrypoints、preflight/gate unification、以及 optional GitHub Actions secondary enforcement 的新 spine。
- 2026-04-04：`S0F-1A/P0-P1` 已完成第一轮收口；真实 issue creation 现在会在 inferred keyword 路径上 fail-closed，并保留同源 draft-generation evidence 供后续 review 使用。
- 2026-04-04：`S0F-1A/P2` 已完成；真实 `create_pr_from_plan.py` 现在把 front-half preflight result 视为 live publish 的硬前置，且已用一个 occupied-branch stop 样本证明 preview planning 不再等于 publish 资格。
- 2026-04-04：`S0F-1A/P3` 已完成；raw issue-conclusion、issue-relationship 与 PR body rewrite 入口现在都已收口为 internal-only bounded reuse，并以 guarded wrapper / thin-gate surface 作为 canonical operator-facing live mutation path。