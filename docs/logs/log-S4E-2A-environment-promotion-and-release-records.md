# log-S4E-2A (Phase 2: Environment Promotion and Release Records)

---

**id**: `S4E-2A`
**kind**: `log`
**title**: `environment promotion semantics and release records + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, ReleaseOperations, Governance, Promotion, Drills, Evidence, epic/s4, sub/4e2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **previous_log**: `docs/logs/log-S4E-1A-release-trigger-policy-and-governance-boundary.md`
  **reference_log_1**: `docs/logs/log-S4E-1A-release-trigger-policy-and-governance-boundary.md`
  **reference_log_2**: `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
  **reference_log_3**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
**created**: `2026-03-27`
**updated**: `2026-03-27`

---

## Decision / Outcome

**Decision**:

- `S4E-2A` 承接 `S4E-1A` 已固定的 trigger surface / approval boundary 基线，继续定义 environment promotion semantics 与 release record continuity；
- v1 先回答“什么叫 promotion、promotion 过程中哪些 identity/records 必须连续”，而不是直接落地多环境自动发布系统。

**Default choices (phase defaults / v1)**:

- promotion v1 先定义为“从已存在的 lower-environment release record 出发，向更高环境复用同一 candidate identity 的受控晋级动作”；
- release identity 应优先复用 `headSha`、image tag / candidate artifact、source run URL 与 artifact bundle，而不是在每个环境重新生成互不相干的记录；
- `S4E-2A` 先定义字段、语义与最小流程，不要求当前仓库已经存在 staging/prod 真实执行样本；
- deploy / verify / rollback 的运行语义仍留在 `S4D`，本 phase 只收口 promotion / record continuity。

## Definitions (optional)

- **Promotion**：把已经在较低环境形成候选身份与记录的一次 release，受控推进到更高环境的动作。
- **Lower-environment release record**：例如 `cloud-dev` 已形成的 run URL、artifact bundle、summary/result、approval 信息与候选 identity。
- **Release identity**：至少包括 `headSha`、candidate image/tag、source run URL、artifact bundle 引用等，用于跨环境保持同一候选身份。
- **Promotion intent**：说明本次 promotion 为什么发生、从哪个环境来、准备去哪个环境、希望保留哪些 release identity/records 的说明。
- **Source record reference**：能够唯一回指 lower-environment release record 的最小引用，例如 source run URL、artifact bundle 路径或后续 ledger record id。

## Constraints

- 不把当前还不存在的 staging/prod 运行现实写成既成事实；
- 不引入新的数据库或 release management 平台作为前置条件；
- promotion contract 必须能和 `S4E-1A` 的 release record 最小字段衔接；
- 记录面应尽量低基数、可追溯，并能回指现有 artifact/run URL。

## Scope

- `P0`: contract（promotion semantics、release identity continuity、promotion evidence contract）
- `P1`: policy / ledger mapping（最小 release ledger 字段、promotion intent、source/target environment 关系）
- `P2`: drill / verify（用现有 lower-environment 样本验证 record continuity 是否可表达）
- `P3`: runway（为 approval hierarchy / rollback authority phase 提供明确入口）

## Success Criteria (DoD)

- 明确说明什么是 promotion，以及 promotion 与普通 rerun/override 的区别；
- 固定一份可跨环境延续的 release identity 字段集合；
- 固定一份最小 release ledger / release record 扩展字段集；
- 至少定义一条从 `cloud-dev` 记录面出发、可被未来更高环境复用的 evidence 入口；
- 文档层面不再把 trigger policy 问题与 promotion/ledger continuity 问题写混。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 promotion semantics、release identity continuity 与最小 ledger contract 已稳定；
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Promotion semantics contract | v1)

- promotion 必须从“已有 lower-environment release identity”出发，而不是把任何新 run 都称为 promotion；
- promotion 与 rerun/override 的区别必须被写清：
  - rerun/override 仍在同一环境 control-plane 内；
  - promotion 则代表候选身份跨到更高环境或更高风险边界。
- promotion v1 必须同时满足以下条件：
  - 已存在可回指的 lower-environment source record；
  - `headSha` 与 candidate image/tag 仍指向同一候选身份；
  - target environment 明确高于 source environment，而不是同环境内重新执行；
- 如果目标动作会重新 build、重新挑选不同 artifact，或把 candidate identity 改写成另一组 `headSha` / image tag，则该动作应被视为新的 candidate qualification，而不是 promotion。

### P0-C1-S2 (Release identity and ledger continuity contract | v1)

- promotion 时至少应延续以下字段：
  - `headSha`
  - `candidateImage` / image tag
  - `sourceRecordRef`
  - `sourceEnvironment`
  - `sourceRunUrl`
  - `sourceArtifactPath` 或 artifact bundle 引用
  - `promotionTargetEnvironment`
  - `promotionIntent`
- target environment 可以补充自己的 run URL、artifact 路径与 approval 结果，但不得覆盖或丢失 source side 的 identity 字段；
- 若未来 higher environment 无法复用这些字段，则必须明确说明为什么需要生成新 identity，而不是默认丢失 continuity。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `headSha`
  - `sourceRecordRef`
  - `sourceEnvironment`
  - `targetEnvironment`
  - `sourceRunUrl`
  - `sourceArtifactPath` or artifact bundle reference
  - `promotionIntent`
  - `approvalState`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4E-2A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S4E-2A` 相关变更现在继续落在 `S4E-release-operating-model-and-governance` 分支，除非后续 `S4E` 再拆更细的子分支。

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P1 (Policy / ledger mapping)

- P1-C1-S1: 固定 promotion 与 rerun/override 的边界定义
- P1-C1-S2: 固定 release identity continuity 与最小 ledger 扩展字段

**Current status (S4E-2A / P0-P1)**

- `P0-C1-S1` 已完成第一版 promotion semantics contract：当前 `S4E-2A` 已固定“promotion 只能从既有 lower-environment source record 出发，并延续同一 candidate identity 进入更高环境”；凡是会改写 `headSha`、candidate image/tag 或重新挑选 artifact 的动作，不再被记作 promotion，而应先回到新的 candidate qualification / lower-environment record。
- `P0-C1-S2` 已完成第一版 release identity continuity contract：当前 promotion v1 至少要求连续保留 `headSha`、`candidateImage`、`sourceRecordRef`、`sourceEnvironment`、`sourceRunUrl`、`sourceArtifactPath`、`promotionTargetEnvironment` 与 `promotionIntent`；未来 higher-environment run 只能补充 target-side evidence，不能吞掉 source-side identity。
- `P0-C1-S3` 已完成第一版 evidence contract：当前 promotion evidence 已固定必须能同时回指 source record、source artifact/run URL、target environment、approval state 与最终 result，因此后续 `P2` drill 不再只是“找一条 run”，而是要验证 lower-environment record continuity 能否被稳定表达。
- `P1-C1-S1` 已完成第一版 policy boundary：当前 policy 已明确 promotion 与 rerun/override 的边界不以 GitHub Actions 按钮形式区分，而以“是否跨环境且是否延续同一候选身份”区分；同环境 rerun、manual override 或重新挑选 candidate 仍属于 control-plane override，不自动升级为 promotion。
- `P1-C1-S2` 已完成第一版 ledger mapping：当前最小 release ledger / record 扩展字段已固定为 `recordKind`、`headSha`、`candidateImage`、`sourceRecordRef`、`sourceEnvironment`、`targetEnvironment`、`sourceRunUrl`、`sourceArtifactPath`、`promotionIntent`、`requestedBy`、`approvalState`、`approvedBy` 与 `result`；后续更高环境只允许在此基础上追加 target-side run/evidence 字段，而不是另起一套无关记录。

### P2 (Drill / Verify)

- P2-C1-S1: 用现有 `cloud-dev` run 样本验证 lower-environment release identity 是否可被统一引用
- P2-C1-S2: 为未来 higher-environment promotion 定义最小 evidence 入口与 source/target 映射

**Current status (S4E-2A / P2)**

- `P2-C1-S1` 已完成第一版 lower-environment source-record continuity 验证：现有 `cloud-dev` PASS run `23600877818` 已证明一条可晋级候选可以同时被 `headSha`、`candidateImage`、run URL、summary artifact 与 operator guidance 统一引用，而不需要为 promotion 重新生成另一套无关 identity。
- `P2-C1-S2` 已完成第一版 promotion evidence entry 映射：当前 `S4E-2A` 已固定“source-side 字段必须来自已存在的 lower-environment record，而 target-side 字段只在未来 higher-environment run 真正执行后追加回填”的最小入口，因此现阶段可以先把 promotion entry 写成 `source-fixed / target-pending`，而不是伪造不存在的 staging/prod 执行事实。

### P3 (Runway)

- P3-C1-S1: 把 approval hierarchy / rollback authority 的后续问题显式转交 `S4E-3A`

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: promotion semantics fixed
- [x] `P0-C1-S2`: release identity and ledger continuity fixed
- [x] `P0-C1-S3`: promotion evidence contract fixed

### P1 (Policy / ledger mapping)

- [x] `P1-C1-S1`: promotion vs rerun/override boundary fixed
- [x] `P1-C1-S2`: ledger extension fields fixed

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: lower-environment source record evidence referenced
- [x] `P2-C1-S2`: promotion evidence entry fixed

### P3 (Runway)

- [ ] `P3-C1-S1`: hierarchy follow-up handed to S4E-3A

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (lower-environment PASS sample can be unified into a promotion source record | 2026-03-27)

- headSha: `fdd3e812`
- sourceRecordRef: `run:23600877818`
- sourceEnvironment: `cloud-dev`
- targetEnvironment: `future-higher-environment`
- sourceRunUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23600877818`
- sourceArtifactPath: `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/summary.json`
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/operator_guidance.txt`
  - `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
- expected:
  - 至少一条 `cloud-dev` 的真实 PASS record 应能被压缩成 promotion source record，而不是只能在原 phase log 里以自由文本存在；
  - 这条 source record 必须同时保留 `headSha`、candidate image、run URL 与 artifact bundle 引用，确保未来 higher-environment promotion 可以直接回指同一候选身份；
  - source record 不应依赖“重新 build 一次”或“再做一条不同 identity 的 manual run”才能被未来 promotion 使用。
- observed:
  - run `23600877818` 的 `summary.json` 已明确记录 `headSha=fdd3e812...`、`expectedHeadSha=fdd3e812...`、`remoteHeadSha=fdd3e812...`、`imageTag=wordloom-backend:cloud-dev`、`result=PASS` 与 `evidenceComplete=true`，说明该样本已具备可被 promotion 继续引用的最小 identity/ledger 基线；
  - 同一 artifact bundle 还保留了 `operator_guidance.txt`，其中 `next_action=Release verified. Keep the candidate running and retain this artifact bundle as evidence.`，这使 source record 不只是 run URL，而是同时具备可回指的 evidence bundle；
  - 因此，`sourceRecordRef=run:23600877818`、`sourceRunUrl` 与 `sourceArtifactPath` 现在已经能共同组成一条可被未来更高环境直接引用的 lower-environment source record。

### P2-C1-S2 (future promotion evidence entry fixed as source-fixed and target-pending mapping | 2026-03-27)

- headSha: `fdd3e812`
- sourceRecordRef: `run:23600877818`
- sourceEnvironment: `cloud-dev`
- targetEnvironment: `future-higher-environment`
- sourceRunUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23600877818`
- sourceArtifactPath: `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/summary.json`
- promotionIntent: `promote verified cloud-dev candidate to a higher environment without rebuilding or replacing candidate identity`
- approvalState: `pending_target_environment_approval`
- result: `pending_execution`
- expected:
  - 在当前仓库尚无 staging/prod 真实 promotion 样本的前提下，`S4E-2A` 仍应给出一条可落账的最小 promotion evidence entry；
  - 该 entry 必须把 source-side 字段固定下来，同时明确 target-side run/result/approval 只在未来真正执行后追加；
  - 这样 future higher-environment promotion 才能被记为“沿用既有 candidate identity 的晋级”，而不是重新起一条语义不连贯的发布记录。
- observed:
  - 当前 `S4E-2A` 已固定 future promotion entry 的最小写法：`sourceRecordRef`、`sourceEnvironment`、`sourceRunUrl`、`sourceArtifactPath` 与 `promotionIntent` 在 source-side 先被写实；`targetEnvironment` 可以先写成计划中的 higher environment，而 `approvalState` / `result` 则在 target-side 执行前保持 `pending_*`；
  - 该 mapping 明确要求未来 higher-environment run 只能补充 target-side run URL、artifact 路径、approval actor 与最终 result，不能覆盖 `headSha`、candidate image 或 source record 引用；
  - 因此，`S4E-2A/P2` 已把 promotion evidence 入口固定为 `source-fixed / target-pending` 结构，满足当前无真实 higher-environment 样本时的最小可追溯口径。

## Recent changes (for traceability, optional)

- 2026-03-27: 已完成 `S4E-2A/P2-C1-S1S2` 的第一轮 drill/evidence 回填；当前已用 `cloud-dev` PASS run `23600877818` 固定 lower-environment source record continuity，并把 future promotion evidence 入口收口为 `source-fixed / target-pending` 映射。
- 2026-03-27: 已完成 `S4E-2A/P1-C1-S1S2` 的第一轮 policy/ledger mapping 收口，固定了 promotion 与 rerun/override 的边界，以及最小 release ledger 扩展字段。
- 2026-03-27: 已完成 `S4E-2A/P0-C1-S1S2S3` 的第一轮 contract 收口，固定了 promotion semantics、release identity continuity 与 promotion evidence contract。
- 2026-03-27: 首次创建 `S4E-2A` draft，用于承接 environment promotion semantics 与 release record continuity；当前尚未进入正式 contract/evidence 收口。