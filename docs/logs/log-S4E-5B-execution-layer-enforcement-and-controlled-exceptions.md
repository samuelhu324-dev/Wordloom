# log-S4E-5B (Phase 5B: Execution-Layer Enforcement and Controlled Exceptions)

---

**id**: `S4E-5B`
**kind**: `log`
**title**: `execution-layer enforcement and controlled exceptions + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, ReleaseOperations, Governance, Enforcement, Approval, Auditability, BreakGlass, Runtime, Evidence, epic/s4, sub/4e5b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **previous_log**: `docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md`
  **reference_log_1**: `docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md`
  **reference_log_2**: `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
  **reference_log_3**: `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
**created**: `2026-03-27`
**updated**: `2026-03-27`

---

## Decision / Outcome

**Decision**:

- `S4E-5B` 承接 `S4E-5A` 已固定的 higher-environment governance contract，专门处理 execution-layer implementation path：如何把 approval independence、`audit_incomplete` blocking、`break_glass_exception` 与 controlled rollback restrictions 变成可执行的 gate；
- v1 先定义 execution gate contract、判定来源与受控例外路径，而不是立即实现完整的外部 approval platform 或 release governance backend。

**Default choices (phase defaults / v1)**:

- execution-layer enforcement v1 继续围绕现有 GitHub Actions environment gate、artifact bundle、run URL 与 structured governance record 扩展，不另起 schema；
- 受控例外路径优先要求显式 `break_glass_exception` 记账与 evidence completeness，而不是允许隐式人工绕过；
- `S4E-5B` 只处理 execution gate 与 controlled exception path，不重复定义 `S4E-5A` 的 higher-environment blocking contract 本身。

## Definitions (optional)

- **Execution-layer enforcement**：把治理规则从 policy/record 层提升为真正阻断或放行执行路径的 gate。
- **Controlled exception**：在正常 blocking rule 之外，经显式记账和受控条件允许的例外路径。
- **Break-glass path**：为紧急情况保留的受控例外执行路径，要求额外 evidence 与事后可审计性。
- **Decision source**：用于证明 approval independence、audit completeness 或 exception allowance 的执行层判定来源。

## Constraints

- 不把尚未实现的 approval backend 写成已存在能力；
- 不为 execution gate 单独引入新 record schema 或新 evidence family；
- controlled exception 必须能回接既有 `headSha`、`sourceRecordRef`、`authorityRole`、`actedBy`、`decisionReason`、`result`、`runUrl` 与 artifact bundle；
- v1 先定义 execution path contract 与验证入口，不要求仓库此刻已经实现完整自动 enforcement。

## Scope

- `P0`: contract（execution gate boundary、decision source contract、controlled exception baseline）
- `P1`: policy mapping（approval independence gate、audit-incomplete hard-stop、break-glass execution wording）
- `P2`: drill / verify（用现有或受控样本验证 execution gate/evidence 是否足够表达）
- `P3`: runway（为 future automation / external approval integration 提供实现入口）

## Success Criteria (DoD)

- 明确 execution-layer enforcement 与 record-layer policy 的边界；
- 明确 approval independence、`audit_incomplete` 与 `break_glass_exception` 的最小 execution gate 口径；
- 保持 record/evidence schema 连续，不因进入执行层而改写既有字段骨架；
- 至少定义一条 future implementation/evidence 入口，说明如何验证 execution gate 行为。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 execution-layer enforcement / controlled exception contract 已稳定；
  - The Evidence section includes traceable entries showing how execution gates and exceptions are expressed on the same governance record skeleton.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4E-5B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S4E-5B` 相关变更当前继续落在 `S4E-release-operating-model-and-governance` 分支，除非后续 `S4E` 再拆更细的 phase 子分支。

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P0 (Contract)

- P0-C1-S1: 固定 execution-layer enforcement boundary
- P0-C1-S2: 固定 decision source / evidence source contract
- P0-C1-S3: 固定 break-glass / controlled exception baseline

**Current status (S4E-5B / P0)**

- `P0-C1-S1` 已完成第一版 execution-layer enforcement boundary：当前已明确哪些 higher-environment governance 约束仍停留在 record/policy 层，哪些必须进入 execution stop-go gate；其中 approval independence、`audit_incomplete` blocking 与 controlled rollback/override restrictions 已被明确列为 execution-layer candidates。
- `P0-C1-S2` 已完成第一版 decision source / evidence source contract：当前已明确 execution gate 的判定不能依赖自由文本或 operator 口头判断，而必须来自可回指的 decision source，例如 GitHub environment gate state、structured governance record、artifact bundle、run URL 或 future approval backend output。
- `P0-C1-S3` 已完成第一版 break-glass / controlled exception baseline：当前已明确 break-glass 不是默认 fallback，而是受控例外路径；只有在正常 blocking contract 无法满足但风险接受被显式批准时，才允许进入受控执行，并必须留下额外 evidence。

### P0-C1-S1 (Execution-layer enforcement boundary | v1)

- 以下约束应被视为 execution-layer gate 候选，而不是仅停留在 record/policy 层：
  - approval independence 未满足时的 approval block；
  - `audit_incomplete` 出现在 higher-environment promotion、manual override、manual rollback、approval replay 时的 hard stop；
  - manual override justification 不完整时的 pre-execution block；
  - manual rollback authority / evidence completeness 不完整时的 rollback-entry block；
  - break-glass 未被显式授权时的 exception-entry block。
- 以下事项在 v1 仍可保留在 record/policy 层，而不必立即变成自动 gate：
  - 更细粒度的 approver roster 组织规则；
  - 外部 approval backend 的实现细节；
  - multi-environment reviewer cardinality 的更复杂组合策略。
- v1 的最小边界固定为：
  - execution-layer enforcement 只负责决定“当前动作是否允许继续执行”；
  - record/policy layer 负责提供动作语义、actor/authority mapping 与审计骨架；
  - 任何进入 execution gate 的规则都必须先能被当前 governance action record / evidence skeleton 稳定表达。

### P0-C1-S2 (Decision source and evidence source contract | v1)

- execution gate 的判定来源至少应来自以下一种或多种可回指 source，而不是自由文本：
  - GitHub environment approval state / pending deployment metadata；
  - structured governance action record；
  - artifact bundle（如 `summary.json`、`operator_guidance.txt`、rollback/verify logs）；
  - run URL / workflow run identity；
  - future external approval system output，但必须能回写到既有 action/evidence skeleton。
- v1 的最小 contract 固定为：
  - decision source 必须能证明 approval independence、authority role、decision reason 或 exception allowance；
  - evidence source 必须能证明该判定在具体 run / release action 上已经发生，而不是纯政策文本；
  - 若 decision source 与 evidence source 不能稳定映射到同一 `headSha` / `sourceRecordRef`，则 execution gate 不应视为可信。

### P0-C1-S3 (Break-glass and controlled exception baseline | v1)

- break-glass / controlled exception 的最小 baseline 固定为：
  - break-glass 只能在正常 blocking rule 会阻断、但存在明确更高优先级风险接受理由时进入；
  - break-glass 必须单独记账为受控 governance action，而不是被隐式混进 approval、override 或 rollback 的普通记录里；
  - break-glass 一旦触发，至少要追加 exception reason、exception approver 或 equivalent authority source、时间点、对应 run/artifact reference；
  - break-glass 不能消除 audit requirement；它只允许带着额外 evidence 进入受控执行，而不是豁免审计。
- v1 的最小例外边界固定为：
  - 默认路径是 block，而不是 exception；
  - exception 必须是显式允许，而不是事后解释；
  - future automation 可以把 break-glass gate 自动化，但不需要改写当前 governance record / evidence skeleton。

### P1 (Policy mapping)

- P1-C1-S1: 固定 approval independence gate wording
- P1-C1-S2: 固定 audit-incomplete hard-stop 与 break-glass execution wording

**Current status (S4E-5B / P0-P1)**

- `P1-C1-S1` 已完成第一版 approval independence gate wording：当前 policy 已明确 approval independence 不再只是 higher-environment 的记录层 contract，而是 execution gate；一旦 `requestedBy == actedBy` 或 approver 与 override/rollback authority 的独立性无法证明满足最低要求，执行层应在 approval 前阻断。
- `P1-C1-S2` 已完成第一版 `audit_incomplete` hard-stop / break-glass execution wording：当前 policy 已明确 `audit_incomplete` 在 higher-environment promotion、manual override、manual rollback 与 approval replay 中应直接触发 hard stop；同时 break-glass 只能以显式 exception path 进入，并附带额外 evidence 与事后可审计性。

### P1-C1-S1 (Approval independence gate wording | v1)

- approval independence gate 的最小 wording 固定为：
  - higher-environment approval 进入执行前，系统或 operator-visible gate 必须能确认 `requestedBy != actedBy` when `authorityRole=approval_authority`；
  - 若 approver 同时也是同一 decision window 内的 override actor 或 manual rollback authority，且没有显式 break-glass allowance，则 approval gate 应返回 `blocked_before_approval`；
  - approval independence gate 的失败不应只写进事后审计，而应在 execution path 中表现为“不能继续执行”的 stop-go 结果。
- v1 的最小执行口径固定为：
  - approval independence 的判定优先来自 structured governance record、environment approval metadata 或 future approval backend output；
  - 若这些来源无法证明 independence 满足，则默认结论应是 block，而不是“先继续，后补判断”；
  - future automation 可以把判定做得更强，但失败语义仍应统一落回 `blocking_prerequisite_failed` / `blocked_before_approval` 这类既有结果骨架。

### P1-C1-S2 (`audit_incomplete` hard-stop and break-glass execution wording | v1)

- `audit_incomplete` hard-stop 的最小 wording 固定为：
  - 在 higher-environment promotion、manual override、manual rollback、approval replay 场景中，只要 `headSha`、`sourceRecordRef`、`authorityRole`、`actedBy`、`decisionReason`、`runUrl` 或 artifact reference 任一关键字段无法稳定回指，执行层就应返回 `blocking_prerequisite_failed`；
  - `audit_incomplete` 的处理不应退化为 operator note；它应表现为不能进入目标动作的硬阻断，而不是运行后再补 evidence；
  - 只有当 action type、authority role 与 evidence source 都满足 `audit_complete`，execution gate 才允许继续。
- break-glass execution 的最小 wording 固定为：
  - break-glass 只能在正常 blocking rule 已触发、但存在显式更高优先级风险接受时进入；
  - break-glass 进入执行前，必须已经记录 exception reason、exception authority source、对应 run/reference 与受控 evidence，否则 exception gate 本身也应阻断；
  - break-glass 的成功语义应是“例外被受控允许并留下额外 evidence”，而不是“绕过所有治理要求”；换言之，break-glass 可以绕过部分默认 independence / readiness rule，但不能绕过最低 auditability requirement。

### P2 (Drill / Verify)

- P2-C1-S1: 用受控样本验证 execution gate/evidence 表达能力
- P2-C1-S2: 用现有 governance record 验证 controlled exception 落账入口

**Current status (S4E-5B / P0-P2)**

- `P2-C1-S1` 已完成第一轮 execution gate / evidence verification：当前已用真实 release run 与受控 execution sample 验证，现有 governance record / artifact bundle 已足以表达 execution-layer 的放行、`blocked_before_approval` 与 `blocking_prerequisite_failed`，而不需要为 gate result 另起 schema。
- `P2-C1-S2` 已完成第一轮 controlled exception entry verification：当前已确认 `break_glass_exception` 可以作为单独 governance action 继续落在同一 `headSha` / `sourceRecordRef` / `authorityRole` / `actedBy` / `decisionReason` / `result` / `runUrl` / artifact reference 骨架上；execution-layer 只是在已有骨架上加强 gate 语义，而不是新增 exception 专用账本。

### P3 (Runway)

- P3-C1-S1: 为 future automation / external approval integration 提供实现入口

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: execution enforcement boundary fixed
- [x] `P0-C1-S2`: decision/evidence source contract fixed
- [x] `P0-C1-S3`: controlled exception baseline fixed

### P1 (Policy mapping)

- [x] `P1-C1-S1`: approval independence gate wording fixed
- [x] `P1-C1-S2`: audit-incomplete / break-glass wording fixed

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: execution gate evidence referenced
- [x] `P2-C1-S2`: controlled exception evidence referenced

### P3 (Runway)

- [ ] `P3-C1-S1`: automation / external integration runway defined

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (real run plus controlled execution samples prove current evidence can express execution gate outcomes without changing schema | 2026-03-27)

- headSha: `7f3c417d`
- sourceRecordRef:
  - `run:23599857316`
  - `policy-simulation:execution-gate-outcomes-v1`
- targetEnvironment:
  - `cloud-dev`
  - `simulated-higher-environment`
- policyMode:
  - `recorded_runtime_gate`
  - `hard_gate`
- authorityRoles:
  - `approval_authority`
  - `release_execution_gate`
  - `rollback_authority`
- actedBy:
  - `samuelhu324-dev`
  - `workflow_runtime_gate`
  - `workflow_auto_rollback`
- decisionReasons:
  - `cloud-dev environment gate released for manual release run`
  - `approval_independence_not_satisfied`
  - `audit_incomplete`
  - `verify_fail_auto`
- result:
  - `approval_granted`
  - `blocked_before_approval`
  - `blocking_prerequisite_failed`
  - `candidate_reverted_to_known_good`
  - `PASS_AFTER_ROLLBACK`
- runUrl:
  - `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23599857316`
  - `n/a (controlled execution-gate sample)`
- auditStatus:
  - `audit_complete` for the real release / rollback run
  - `audit_complete` for the controlled approval-independence block sample once actor overlap and decision source are explicitly recorded
  - `audit_incomplete` for the controlled prerequisite-failure sample when required references are intentionally absent
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/operator_guidance.txt`
  - `docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md`
  - `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
- expected:
  - execution-layer evidence 至少要能在同一骨架里表达三类结果：允许继续执行、因 approval independence 失败而 `blocked_before_approval`、以及因 `audit_incomplete` 而 `blocking_prerequisite_failed`；
  - gate result 必须能回指 decision source 与 evidence source，而不是只留下 policy 文本；
  - 若 execution-layer outcome 需要新的字段家族，`S4E-5B` 的“不分叉 schema 进入执行层”前提就不成立。
- observed:
  - `23599857316` 的真实 run 已证明 execution-layer 正常放行与自动 rollback 结果能够通过 `summary.json`、`operator_guidance.txt`、run URL、gateResults、`rollbackTrigger=verify_fail_auto` 与 `result=PASS_AFTER_ROLLBACK` 稳定表达；这说明“允许执行并留下 gate evidence”已经在现有骨架上成立；
  - 同一骨架可以把 approval independence 失败压成 `authorityRole=approval_authority`、`decisionReason=approval_independence_not_satisfied` 与 `result=blocked_before_approval`；受控样本只是在已有 actor/authority 字段上改变解释强度，不需要新增 execution-only 字段；
  - 同一骨架也可以把 prerequisite 缺失压成 `authorityRole=release_execution_gate`、`decisionReason=audit_incomplete` 与 `result=blocking_prerequisite_failed`；缺的是 evidence completeness，而不是表达能力；
  - 因此，`S4E-5B/P2-C1-S1` 已验证 current evidence model 足以承接 execution-layer 的 stop-go 结果词汇，后续要增强的是自动判定与入口实现，而不是改写 record schema。

### P2-C1-S2 (existing governance lineage proves controlled exceptions can be booked as separate actions on the same skeleton | 2026-03-27)

- headSha: `7f3c417d`
- sourceRecordRef:
  - `run:23599857316`
  - `policy-simulation:break-glass-entry-v1`
- targetEnvironment:
  - `cloud-dev lineage reused for exception booking verification`
  - `simulated-higher-environment`
- policyMode:
  - `controlled_exception`
  - `hard_gate_with_exception_path`
- authorityRoles:
  - `approval_authority`
  - `exception_authority`
  - `override_actor`
- actedBy:
  - `samuelhu324-dev`（source approval lineage）
  - `independent_exception_approver`（controlled sample）
  - `release_operator_under_exception`（controlled sample）
- decisionReasons:
  - `break_glass_exception`
  - `higher_environment_recovery_required`
  - `approval_independence_not_satisfied_but_exception_authorized`
- result:
  - `override_allowed_under_break_glass`
  - `exception_recorded`
- runUrl:
  - `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23599857316`
  - `n/a (controlled exception sample)`
- auditStatus:
  - `audit_complete` when exception reason, authority source, actor, timepoint, source record, and artifact reference are all present
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/operator_guidance.txt`
  - `docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md`
  - `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
- expected:
  - controlled exception 不应成为脱离既有 lineage 的旁路记录，而应作为可回指 source action 的独立 governance action 落账；
  - exception entry 至少要能记录 exception reason、authority source、执行 actor、对应 run/reference 与 evidence bundle；
  - 若 break-glass 必须另起 exception-only ledger，`S4E-5B` 的 controlled exception 路线就会破坏既有审计连续性。
- observed:
  - `23599857316` 已经提供可复用的 `headSha`、`sourceRecordRef`、run URL 与 artifact lineage，因此 controlled exception 不需要新身份模型；它只需要在同一 lineage 上追加一条 `authorityRole=exception_authority` 的受控 action；
  - 受控样本表明 `break_glass_exception` 可以直接写入 `decisionReason`，并把执行层结论压成 `result=override_allowed_under_break_glass`；只要 exception authority、actor、reason 与 artifact reference 可回指，该 action 就满足同一 skeleton 的 auditability 要求；
  - 这也说明 execution-layer 的 controlled exception 入口本质上是“在已有 governance lineage 上增加一条显式 action 并收紧 gate prerequisites”，而不是“绕过现有记录系统”；
  - 因此，`S4E-5B/P2-C1-S2` 已验证 controlled exception entry 可以直接承接现有 governance record lineage，后续需要实现的是 exception gate 的自动/半自动入口，而不是另起账本。

## Recent changes (for traceability, optional)

- 2026-03-27: 已完成 `S4E-5B/P2-C1-S1S2` 的第一轮 drill / verify 回填，当前已验证现有 governance record / evidence skeleton 足以表达 execution-layer 的 `blocked_before_approval`、`blocking_prerequisite_failed`、正常放行与 `break_glass_exception` 的受控落账入口。
- 2026-03-27: 已完成 `S4E-5B/P1-C1-S1S2` 的第一轮 policy wording 收口，当前已固定 approval independence gate，以及 `audit_incomplete` hard-stop / break-glass execution 的最小执行层 wording。
- 2026-03-27: 已完成 `S4E-5B/P0-C1-S1S2S3` 的第一轮 contract 收口，当前已固定 execution-layer enforcement boundary、decision/evidence source contract，以及 break-glass / controlled exception 的最小 baseline。
- 2026-03-27: 首次创建 `S4E-5B` draft，用于承接 execution-layer enforcement / controlled exception follow-up；当前入口重点是 approval independence 的自动判定、`audit_incomplete` 的执行层硬阻断，以及 `break_glass_exception` 的受控落账和执行门。