# log-S4E-4A (Phase 4: Enforcement, Auditability, and Environment Approver Policy)

---

**id**: `S4E-4A`
**kind**: `log`
**title**: `enforcement, auditability, and environment-specific approver policy + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, ReleaseOperations, Governance, Auditability, Enforcement, Approval, Drills, Evidence, epic/s4, sub/4e4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **previous_log**: `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
  **reference_log_1**: `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
  **reference_log_2**: `docs/logs/log-S4E-2A-environment-promotion-and-release-records.md`
  **reference_log_3**: `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
**created**: `2026-03-27`
**updated**: `2026-03-27`

---

## Decision / Outcome

**Decision**:

- `S4E-4A` 承接 `S4E-3A` 已固定的 hierarchy / governance action record contract，继续定义哪些治理约束需要从“记录层 contract”升级到“执行层 enforcement / auditability / environment-specific approver policy”；
- v1 先回答哪些动作必须被 hard-gate、哪些动作只要求可审计留痕、以及不同 target environment 将来如何收紧 approver policy，而不是立即引入新的审批平台或全量组织流程系统。

**Default choices (phase defaults / v1)**:

- enforcement v1 先围绕现有 GitHub Actions environment gate、artifact bundle 与 structured record 扩展，不要求仓库立刻拥有额外的 policy engine；
- auditability v1 优先保证 action record、run URL、artifact path 与 actor/authority mapping 可被一致追溯，而不是先做复杂 dashboard；
- environment-specific approver policy 先定义收紧方向与层级差异，不把当前不存在的 staging/prod reviewer roster 写成既成事实；
- `S4E-4A` 只收口 enforcement / auditability / approver-policy 的入口与 contract，不重复定义 `S4E-2A` 的 promotion identity 或 `S4E-3A` 的 authority taxonomy。

## Definitions (optional)

- **Enforcement gate**：在执行层真正阻断或放行 release/promotion/rollback 的控制点。
- **Auditability**：从 governance action record 回指 actor、authority role、run URL、artifact bundle 与 decision reason 的能力。
- **Environment-specific approver policy**：不同 target environment 对 approver 数量、身份、分权方式的差异化要求。
- **Soft policy**：记录层必须表达，但暂不强制由系统阻断的治理约束。
- **Hard gate**：一旦条件不满足，执行层必须拒绝继续推进的治理约束。

## Constraints

- 不把当前 `cloud-dev` 的单 reviewer 现实误写成更高环境的默认制度；
- 不把所有治理约束都一口气升级为 hard gate，避免超出当前系统成熟度；
- enforcement / auditability contract 必须能回接 `S4E-3A` 的统一 governance action record 字段；
- 所有 future policy 都应能映射回现有 artifact/run URL，而不是只存在口头制度描述。

## Scope

- `P0`: contract（hard-gate vs soft-policy boundary、auditability contract、environment-specific approver policy baseline）
- `P1`: policy mapping（enforcement points、action logging discipline、environment-specific approver tightening path）
- `P2`: drill / verify（用现有 approval/rollback records 检查 enforcement/auditability contract 是否足够表达）
- `P3`: runway（为 future multi-environment governance / stronger approval systems 提供入口）

## Success Criteria (DoD)

- 明确区分哪些治理约束将来必须成为 hard gate，哪些先停留在 soft policy / audit layer；
- 固定一份最小 auditability contract，使每个 governance action record 都能回指 actor、authority、run URL 与 artifact bundle；
- 明确 environment-specific approver policy 的收紧方向，而不是继续把所有环境写成同一 reviewer 模式；
- 至少定义一条从 `S4E-3A` approval/rollback evidence 延伸到 enforcement / auditability 的验证入口；
- 文档层面不再把 authority taxonomy 与 enforcement/auditability 问题写混。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 enforcement / auditability / environment-specific approver policy contract 已稳定；
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Hard-gate vs soft-policy boundary contract | v1)

- 升级为 hard gate 的候选约束至少包括：
  - target environment 没有满足最低 approver policy；
  - governance action record 缺少关键 actor/authority/evidence 字段；
  - rollback/override 缺少可回指的 decision reason 与 artifact bundle；
- 先停留在 soft policy 的约束可以包括：
  - environment-specific approver roster 的更细粒度组织规则；
  - 更复杂的 multi-party approval choreography。

### P0-C1-S2 (Auditability contract | v1)

- 每条 governance action record 至少应能回指：
  - `headSha`
  - `sourceRecordRef`
  - `authorityRole`
  - `actedBy`
  - `decisionReason`
  - `runUrl`
  - artifact bundle reference
- 若任何一个关键字段无法回指，记录应被视为 audit-incomplete，而不是默默接受为“已完成治理动作”。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `headSha`
  - `sourceRecordRef`
  - `targetEnvironment`
  - `policyMode` (`hard_gate` or `soft_policy`)
  - `authorityRole`
  - `actedBy`
  - `decisionReason`
  - `result`
  - `runUrl` or artifact bundle reference

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4E-4A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S4E-4A` 相关变更当前继续落在 `S4E-release-operating-model-and-governance` 分支，除非后续 `S4E` 再拆更细的 phase 子分支。

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P1 (Policy mapping)

- P1-C1-S1: 固定 enforcement points 与最低 auditability 要求
- P1-C1-S2: 固定 environment-specific approver policy 的收紧路径

### P2 (Drill / Verify)

- P2-C1-S1: 用现有 governance action record 验证 auditability contract 是否足够表达
- P2-C1-S2: 用现有 approval/rollback 样本验证 hard-gate vs soft-policy 边界是否可落账

### P3 (Runway)

- P3-C1-S1: 为 future multi-environment governance / stronger approval systems 定义入口

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: hard-gate vs soft-policy boundary fixed
- [ ] `P0-C1-S2`: auditability contract fixed
- [ ] `P0-C1-S3`: enforcement evidence contract fixed

### P1 (Policy mapping)

- [ ] `P1-C1-S1`: enforcement/auditability wording fixed
- [ ] `P1-C1-S2`: environment-specific approver policy wording fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: auditability evidence referenced
- [ ] `P2-C1-S2`: hard-gate/soft-policy evidence referenced

### P3 (Runway)

- [ ] `P3-C1-S1`: stronger governance runway defined

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

## Recent changes (for traceability, optional)

- 2026-03-27: 首次创建 `S4E-4A` draft，用于承接 enforcement、auditability 与 environment-specific approver policy；当前作为 `S4E-3A/P3` 的明确 runway 入口。