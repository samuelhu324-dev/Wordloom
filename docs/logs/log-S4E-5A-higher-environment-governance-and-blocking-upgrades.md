# log-S4E-5A (Phase 5: Higher-Environment Governance and Blocking Upgrades)

---

**id**: `S4E-5A`
**kind**: `log`
**title**: `higher-environment governance and blocking upgrades + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, ReleaseOperations, Governance, Approval, Auditability, Enforcement, HigherEnvironment, Blocking, Evidence, epic/s4, sub/4e5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **previous_log**: `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
  **reference_log_1**: `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
  **reference_log_2**: `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
  **reference_log_3**: `docs/logs/log-S4E-2A-environment-promotion-and-release-records.md`
**created**: `2026-03-27`
**updated**: `2026-03-27`

---

## Decision / Outcome

**Decision**:

- `S4E-5A` 承接 `S4E-4A` 已固定的 stronger-governance runway，专门定义 higher-environment governance 中哪些 soft policy 需要升级为 blocking rule，以及这些升级如何继续复用既有 governance action record / evidence skeleton；
- v1 先回答 `audit_incomplete`、requester/approver separation、approver independence、manual override / rollback restrictions 在更高环境里的最小 blocking contract，而不是立即引入新的审批平台或完整组织流程系统。

**Default choices (phase defaults / v1)**:

- higher-environment governance v1 仍然以现有 GitHub Actions environment gate、artifact bundle、run URL 和 governance action record 为落脚点，不另起 schema；
- blocking upgrade v1 优先定义“什么情况下必须阻断”，再决定未来是否需要更重的 approval service 或 release ledger backend；
- `S4E-5A` 只处理更高环境的 governance escalation，不重复定义 `S4E-2A` 的 promotion identity、`S4E-3A` 的 authority taxonomy 或 `S4E-4A` 的基础 enforcement/auditability contract。

## Definitions (optional)

- **Higher-environment governance**：面向高于当前 `cloud-dev` 风险等级的 promotion / override / rollback 治理要求。
- **Blocking upgrade**：把当前仍停留在 soft policy 的治理约束升级为执行层必须阻断的规则。
- **Approver independence**：approver 与 requester、override actor、rollback actor 之间需要满足的最小独立性要求。
- **Audit prerequisite**：在继续执行之前，必须具备完整且可回指的 audit evidence。

## Constraints

- 不把当前还不存在的 staging/prod reviewer roster 写成既成事实；
- 不为了 higher-environment governance 另起新的 record schema 或单独 evidence model；
- blocking rule 必须能回接现有 `headSha`、`sourceRecordRef`、`authorityRole`、`actedBy`、`decisionReason`、`runUrl` 与 artifact bundle；
- v1 先定义升级规则与验证入口，不要求仓库当下已经具备真实 higher-environment deploy target。

## Scope

- `P0`: contract（blocking-upgrade matrix、audit prerequisite boundary、approver independence baseline）
- `P1`: policy mapping（higher-environment approval/override/rollback restriction wording）
- `P2`: drill / verify（用现有 record 或受控样本验证 blocking 升级口径是否可表达）
- `P3`: runway（为 future external approval systems / multi-environment release governance 提供入口）

## Success Criteria (DoD)

- 明确哪些 `S4E-4A` soft policy 在 higher environment 必须升级为 blocking rule；
- 明确 `audit_incomplete` 在哪些场景下不再允许继续执行；
- 明确 requester/approver separation、approver independence 与 manual override / rollback restriction 的最小 higher-environment 口径；
- 保持 record/evidence schema 连续，不因 governance 升级而改写既有字段骨架；
- 至少定义一条 future evidence 入口，说明如何验证这些 blocking upgrade。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 higher-environment blocking-upgrade contract 已稳定；
  - The Evidence section includes traceable policy/evidence entries showing how soft-policy rules upgrade to blocking conditions.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4E-5A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S4E-5A` 相关变更当前继续落在 `S4E-release-operating-model-and-governance` 分支，除非后续 `S4E` 再拆更细的 phase 子分支。

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P0 (Contract)

- P0-C1-S1: 固定 higher-environment blocking-upgrade matrix
- P0-C1-S2: 固定 `audit_incomplete` -> blocking prerequisite 的边界
- P0-C1-S3: 固定 approver independence / requester separation baseline

**Current status (S4E-5A / P0)**

- `P0-C1-S1` 已完成第一版 higher-environment blocking-upgrade matrix：当前已明确 `S4E-4A` 中仅停留在 soft policy 的几类约束，在 higher environment 应分别升级为 `must_block_before_execution`、`must_block_before_approval` 或 `must_block_before_override_or_rollback`，而不是继续停留在“记录即可”。
- `P0-C1-S2` 已完成第一版 `audit_incomplete` -> blocking prerequisite 边界：当前已明确 higher-environment promotion、manual override、manual rollback、approval replay 等高风险治理动作，一旦关键 evidence 字段无法回指，就必须阻断，而不能仅记为告警。
- `P0-C1-S3` 已完成第一版 approver independence / requester separation baseline：当前已明确 higher environment 至少要求 requester 与 approver 分离，并把 approver 与 override actor / manual rollback actor 的独立性作为默认更强基线；但 v1 仍不把暂不存在的具体 reviewer roster 写成既成事实。

### P0-C1-S1 (Higher-environment blocking-upgrade matrix | v1)

- 在 `cloud-dev` v1 中仍可作为 soft policy 记录的约束，进入 higher environment 后应按以下矩阵升级：
  - requester / approver separation：从 `recorded_soft_policy` 升级为 `must_block_before_approval`；
  - approver independence（approver 不得同时充当 override actor 或同次 manual rollback authority）：从 `recorded_soft_policy` 升级为 `must_block_before_execution`；
  - `audit_incomplete`：从 `recorded_soft_policy` 升级为 `must_block_before_execution`；
  - manual override justification completeness：从 `recorded_soft_policy` 升级为 `must_block_before_override_or_rollback`；
  - manual rollback evidence completeness：从 `recorded_soft_policy` 升级为 `must_block_before_override_or_rollback`；
  - higher-environment approver cardinality / independence rule：从 `future_tightening_direction` 升级为 `must_block_before_approval`。
- v1 的最小升级口径固定为：
  - 任何会影响 higher-environment stop-go 决策可信度的约束，至少应在 approval 前阻断；
  - 任何会影响 override / rollback 事后可审计性的约束，至少应在对应治理动作执行前阻断；
  - 若当前系统还未具备自动判定能力，也必须先在记录模型中有清楚枚举，避免 future enforcement 时再次改 schema。

### P0-C1-S2 (`audit_incomplete` to blocking prerequisite boundary | v1)

- `audit_incomplete` 在 higher environment 至少覆盖以下 blocking 条件：
  - `headSha`、`sourceRecordRef`、`authorityRole`、`actedBy`、`decisionReason`、`runUrl`、artifact bundle reference 任一关键字段无法稳定回指；
  - governance action type 无法区分是 `approval`、`reject`、`rollback` 还是 `override`；
  - manual override / manual rollback 已发生，但缺少能回指该决定的受控 evidence；
  - approver 身份与 authority independence 无法证明满足当前 target environment 的最小 contract。
- v1 的最小边界固定为：
  - 在 `cloud-dev`，`audit_incomplete` 仍可作为 evidence warning 记录，但不自动推翻既有 v1 baseline；
  - 在任何 higher-environment promotion、manual override、manual rollback、approval replay 场景中，`audit_incomplete` 必须被视为 `blocking_prerequisite_failed`；
  - 只有当关键 evidence 字段全部可回指，且 action type / authority role 可稳定枚举时，higher-environment 治理动作才可继续。

### P0-C1-S3 (Approver independence and requester separation baseline | v1)

- higher-environment v1 至少要求：
  - `requestedBy != actedBy` when `authorityRole=approval_authority`；
  - approver 不应同时作为同一次 higher-environment manual override 的执行者；
  - approver 不应在同一 release decision window 内同时担任 manual rollback authority，除非进入受控 break-glass path 并留下额外 evidence；
  - 若因组织规模限制暂无法实现完全不同的人，也至少要在 record 层明确标记该例外为 `break_glass_exception`，而不是默默沿用 `cloud-dev` 单 actor 现实。
- v1 的最小 baseline 固定为：
  - requester / approver separation 是 higher-environment 的默认 blocking rule，而不是可选优化；
  - approver independence 的默认解释是“不能由同一 actor 同时完成 request, approve, override, rollback 的整条高风险链路”；
  - future stronger governance 可以继续加严 approver 数量、组织归属或 reviewer roster，但不需要改动既有 action/evidence skeleton。

### P1 (Policy mapping)

- P1-C1-S1: 固定 higher-environment approval / override restriction wording
- P1-C1-S2: 固定 higher-environment rollback authority / evidence completeness wording

### P2 (Drill / Verify)

- P2-C1-S1: 用现有 governance records 验证 blocking-upgrade evidence 入口
- P2-C1-S2: 用受控样本验证 higher-environment restriction wording 是否可落账

### P3 (Runway)

- P3-C1-S1: 为 future external approval system / multi-environment release governance 提供入口

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: blocking-upgrade matrix fixed
- [x] `P0-C1-S2`: audit prerequisite boundary fixed
- [x] `P0-C1-S3`: approver independence baseline fixed

### P1 (Policy mapping)

- [ ] `P1-C1-S1`: higher-environment approval/override wording fixed
- [ ] `P1-C1-S2`: higher-environment rollback/evidence wording fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: blocking-upgrade evidence referenced
- [ ] `P2-C1-S2`: higher-environment restriction evidence referenced

### P3 (Runway)

- [ ] `P3-C1-S1`: external-approval / multi-environment runway defined

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

## Recent changes (for traceability, optional)

- 2026-03-27: 已完成 `S4E-5A/P0-C1-S1S2S3` 的第一轮 contract 收口，当前已固定 higher-environment blocking-upgrade matrix、`audit_incomplete -> blocking prerequisite` 边界，以及 approver independence / requester separation 的最小 enforced baseline。
- 2026-03-27: 首次创建 `S4E-5A` draft，用于承接 higher-environment governance / blocking-upgrade follow-up；当前入口重点是 `audit_incomplete -> blocking`、approver independence，以及 manual override / rollback restriction 的更高环境收紧。