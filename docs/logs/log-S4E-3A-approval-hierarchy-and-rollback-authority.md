# log-S4E-3A (Phase 3: Approval Hierarchy and Rollback Authority)

---

**id**: `S4E-3A`
**kind**: `log`
**title**: `approval hierarchy and rollback authority + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, ReleaseOperations, Governance, Approval, Rollback, Drills, Evidence, epic/s4, sub/4e3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **previous_log**: `docs/logs/log-S4E-2A-environment-promotion-and-release-records.md`
  **reference_log_1**: `docs/logs/log-S4E-2A-environment-promotion-and-release-records.md`
  **reference_log_2**: `docs/logs/log-S4E-1A-release-trigger-policy-and-governance-boundary.md`
  **reference_log_3**: `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
**created**: `2026-03-27`
**updated**: `2026-03-27`

---

## Decision / Outcome

**Decision**:

- `S4E-3A` 承接 `S4E-2A` 已固定的 promotion semantics / source-record continuity，继续定义谁可以请求 promotion、谁可以 approve、谁可以执行 rollback/override，以及这些治理动作如何记账；
- v1 先定义 approval hierarchy 与 rollback authority 的最小 role/action contract，而不是立即落地新的 RBAC 平台或多环境审批系统。

**Default choices (phase defaults / v1)**:

- approval authority 必须独立于 trigger surface 与 candidate identity，不能因为“谁启动了 run”就默认拥有批准或回滚权限；
- rollback authority 与 promotion approval 应分开记账，即使现实中暂时可能由同一 operator 执行，也不能在记录层面混成一个动作；
- `S4E-3A` v1 先收口 role matrix、governance action 命名和最小 evidence 字段，不要求仓库现在已经有 higher-environment 的真实审批样本；
- 仍以现有 artifact/run URL 为证据源，不引入新的审批数据库或外部 ticket 系统作为前置条件。

## Definitions (optional)

- **Promotion requester**：提出把既有 lower-environment candidate 晋级到更高环境的人或系统主体。
- **Approval authority**：有权批准某个 target environment promotion 进入执行阶段的主体。
- **Rollback authority**：有权对既有 candidate 执行 rollback、保持 known-good 或终止 promotion 的主体。
- **Override action**：在默认 release path 之外，由 operator 明确执行的受控治理动作，例如 manual rerun、manual rollback、approval override。
- **Governance action record**：记录一次 approval / rejection / rollback / override 的最小条目，至少要能回指 source record、target environment、actor 与 action result。

## Constraints

- 不把当前还不存在的 staging/prod reviewer 组织结构写成既成事实；
- 不把 trigger surface、promotion identity 与 approval authority 混写成同一概念；
- role/action contract 必须能回接 `S4E-1A` 的 approval boundary 与 `S4E-2A` 的 source-record continuity；
- evidence 字段必须保持低基数、可追溯，并能落回现有 artifact/run URL。

## Scope

- `P0`: contract（role matrix、approval/rollback authority、governance action evidence contract）
- `P1`: policy mapping（approval hierarchy、separation-of-duties、override/rollback action wording）
- `P2`: drill / verify（用现有 `cloud-dev` approval/rollback 样本验证记录面是否足够表达）
- `P3`: runway（为 future enforcement / auditability / environment-specific authority 提供入口）

## Success Criteria (DoD)

- 明确区分 requester、approver、rollback authority、override actor 至少四类治理动作角色；
- 明确说明 approval authority 不等于 trigger actor，不等于 candidate identity owner；
- 固定一份最小 governance action record 字段集；
- 至少定义一条能从 `S4E-1A` approval sample 与 `S4E-2A` source record continuity 衔接过来的 evidence 入口；
- 文档层面不再把 promotion semantics 与 hierarchy / rollback authority 问题写混。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 approval hierarchy、rollback authority 与 governance action record contract 已稳定；
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Role and authority boundary contract | v1)

- 至少区分以下四类动作主体：
  - promotion requester；
  - approval authority；
  - rollback authority；
  - override actor；
- 同一人可以暂时兼任多个角色，但记录层必须把动作类型拆开，而不是用单个 `operator` 字段覆盖所有治理动作；
- 任何 higher-environment promotion 都必须说明：谁请求、谁批准、谁有权在失败时回滚或保持 known-good。

### P0-C1-S2 (Governance action record contract | v1)

- governance action record 至少应包含：
  - `headSha`
  - `sourceRecordRef`
  - `targetEnvironment`
  - `governanceActionType`
  - `requestedBy`
  - `actedBy`
  - `approvalState`
  - `result`
  - `runUrl` 或 artifact/run URL reference
- `approval`、`reject`、`rollback`、`override` 必须作为可枚举动作类型出现，而不是埋在自由文本里；
- 若同一 release 发生多次治理动作，后续记录应追加而不是覆盖此前 action record。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `headSha`
  - `sourceRecordRef`
  - `targetEnvironment`
  - `governanceActionType`
  - `requestedBy`
  - `actedBy`
  - `approvalState`
  - `result`
  - `runUrl` or artifact bundle reference

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4E-3A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S4E-3A` 相关变更当前继续落在 `S4E-release-operating-model-and-governance` 分支，除非后续 `S4E` 再拆更细的 phase 子分支。

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P1 (Policy mapping)

- P1-C1-S1: 固定 requester / approver / rollback authority / override actor 的最小 hierarchy wording
- P1-C1-S2: 固定 governance action record 与 separation-of-duties 的最小约束

### P2 (Drill / Verify)

- P2-C1-S1: 用现有 `cloud-dev` approval sample 验证 approval action record 的最小入口
- P2-C1-S2: 用现有 rollback sample 验证 rollback authority record 的最小入口

### P3 (Runway)

- P3-C1-S1: 为 future enforcement / auditability / environment-specific approver policy 定义入口

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: role and authority boundary fixed
- [ ] `P0-C1-S2`: governance action record fixed
- [ ] `P0-C1-S3`: hierarchy evidence contract fixed

### P1 (Policy mapping)

- [ ] `P1-C1-S1`: hierarchy wording fixed
- [ ] `P1-C1-S2`: governance action/separation-of-duties wording fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: approval action evidence referenced
- [ ] `P2-C1-S2`: rollback authority evidence referenced

### P3 (Runway)

- [ ] `P3-C1-S1`: enforcement/auditability runway defined

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

## Recent changes (for traceability, optional)

- 2026-03-27: 首次创建 `S4E-3A` draft，用于承接 approval hierarchy、rollback authority 与 governance action record；当前作为 `S4E-2A/P3` 的明确 handoff 入口。