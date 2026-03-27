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

### P0-C1-S2 (Release identity and ledger continuity contract | v1)

- promotion 时至少应延续以下字段：
  - `headSha`
  - `candidateImage` / image tag
  - `sourceEnvironment`
  - `sourceRunUrl`
  - `sourceArtifactPath` 或 artifact bundle 引用
  - `promotionTargetEnvironment`
  - `promotionIntent`
- 若未来 higher environment 无法复用这些字段，则必须明确说明为什么需要生成新 identity，而不是默认丢失 continuity。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `headSha`
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

- `S4E-2A` changes continue to land on `S4D-cloud-runtime-deploy-verify-rollback` unless `S4E` later gets its own dedicated branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P1 (Policy / ledger mapping)

- P1-C1-S1: 固定 promotion 与 rerun/override 的边界定义
- P1-C1-S2: 固定 release identity continuity 与最小 ledger 扩展字段

### P2 (Drill / Verify)

- P2-C1-S1: 用现有 `cloud-dev` run 样本验证 lower-environment release identity 是否可被统一引用
- P2-C1-S2: 为未来 higher-environment promotion 定义最小 evidence 入口与 source/target 映射

### P3 (Runway)

- P3-C1-S1: 把 approval hierarchy / rollback authority 的后续问题显式转交 `S4E-3A`

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: promotion semantics fixed
- [ ] `P0-C1-S2`: release identity and ledger continuity fixed
- [ ] `P0-C1-S3`: promotion evidence contract fixed

### P1 (Policy / ledger mapping)

- [ ] `P1-C1-S1`: promotion vs rerun/override boundary fixed
- [ ] `P1-C1-S2`: ledger extension fields fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: lower-environment source record evidence referenced
- [ ] `P2-C1-S2`: promotion evidence entry fixed

### P3 (Runway)

- [ ] `P3-C1-S1`: hierarchy follow-up handed to S4E-3A

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

## Recent changes (for traceability, optional)

- 2026-03-27: 首次创建 `S4E-2A` draft，用于承接 environment promotion semantics 与 release record continuity；当前尚未进入正式 contract/evidence 收口。