# log-S4E-5A (Phase 5: Higher-Environment Governance and Blocking Upgrades)

---

**id**: `S4E-5A`
**kind**: `log`
**title**: `higher-environment governance and blocking upgrades + drills/evidence v1`
**status**: `stable`
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

**Current status (S4E-5A / P0-P1)**

- `P1-C1-S1` 已完成第一版 higher-environment approval / override restriction wording：当前 policy 已明确 higher-environment approval 不能沿用 `cloud-dev` 的单 actor 现实，approval、override 与 break-glass 都必须在既有 governance record skeleton 上分别记账，并在不满足 independence 或 evidence completeness 时阻断。
- `P1-C1-S2` 已完成第一版 higher-environment rollback authority / evidence completeness wording：当前 policy 已明确 manual rollback 不再只是 runtime recovery 动作，而是 higher-environment governance action；若 rollback authority、decision reason 或 evidence bundle 不完整，则应在执行前阻断，而不是事后补写。

### P1-C1-S1 (Higher-environment approval and override restriction wording | v1)

- higher-environment approval 的最小 wording 固定为：
  - promotion requester 只能提出 candidate 或 promotion intent，不能因为发起了 run 就默认获得 approval authority；
  - approval authority 必须在 `requestedBy`、`actedBy`、`authorityRole=approval_authority` 与 `decisionReason` 可稳定回指的前提下放行，否则应阻断为 `blocking_prerequisite_failed`；
  - 若当前 target environment 要求 requester / approver separation 或 approver independence，而 record 无法证明已满足，则 approval 不应继续进入执行阶段。
- higher-environment manual override 的最小 wording 固定为：
  - override 不是“补充说明”，而是独立 governance action，必须单独记录 `authorityRole`、`actedBy`、`decisionReason`、`result` 与对应 run/artifact reference；
  - override actor 不应与同一次 approval actor 视为同一默认主体；若两者必须重合，则只能通过显式 `break_glass_exception` 进入，并留下额外 evidence；
  - 任何缺少 justification completeness、authority independence 或 controlled evidence 的 override，都应在动作执行前阻断，而不是允许先执行后补写记录。

### P1-C1-S2 (Higher-environment rollback authority and evidence completeness wording | v1)

- higher-environment rollback authority 的最小 wording 固定为：
  - rollback authority 必须被表达为独立 governance role，而不是被 approval actor、generic operator 或 workflow 成功/失败文本隐式代替；
  - 若 rollback 属于 manual rollback，则必须在执行前确认 `authorityRole=rollback_authority`、`actedBy`、`decisionReason`、rollback evidence bundle 与 source record continuity 全部可回指；
  - 若无法证明 rollback authority 满足当前 target environment 的 independence contract，则应阻断 rollback entry，并要求进入更受控的 higher-environment recovery path。
- higher-environment evidence completeness 的最小 wording 固定为：
  - approval、override、manual rollback 三类动作都必须在执行前满足 `audit_complete`，不能接受“先动作、后补证据”的 higher-environment 运行方式；
  - evidence completeness 不只包含 artifact 文件存在，还包括 action type、authority role、decision reason、runUrl/sourceRecordRef 能被稳定映射回同一 governance record skeleton；
  - 若 evidence 只能通过自由文本或人工记忆推断，则应视为 `audit_incomplete`，并按 `blocking_prerequisite_failed` 处理，而不是当作可接受的 higher-environment 特例。

### P2 (Drill / Verify)

- P2-C1-S1: 用现有 governance records 验证 blocking-upgrade evidence 入口
- P2-C1-S2: 用受控样本验证 higher-environment restriction wording 是否可落账

**Current status (S4E-5A / P2)**

- `P2-C1-S1` 已完成第一轮 blocking-upgrade evidence 回填：现有 `23599857316` approval/rollback governance records 已证明，当前 schema 不需要新增字段就能把 same-actor approval、rollback authority、decision reason、evidence completeness 重新解释为 higher-environment blocking candidate。
- `P2-C1-S2` 已完成第一轮 controlled-sample verification：当前已用受控 higher-environment policy sample 证明 `break_glass_exception`、approval independence failure 与 manual rollback blocking 都能继续落在同一 governance action record / evidence skeleton 上，而不需要另起一套 higher-environment 专用模型。

### P3 (Runway)

- P3-C1-S1: 为 future external approval system / multi-environment release governance 提供入口

**Current status (S4E-5A / P3)**

- `P3-C1-S1` 已完成第一版 runway 定义：当前 `S4E-5A` 已明确 future GitHub environment reviewers 扩展、外部 approval service 与 release ledger backend 都不应引入新的 governance record family，而应继续把 approval、override、rollback、break-glass 与 blocking prerequisite 的结论回写到同一 action/evidence skeleton。
- 该 runway 已固定三条接入原则：
  - approval control-plane 可以升级，但 governance record schema 不应分叉；
  - environment-specific enforcement 可以升级，但 `headSha`、`sourceRecordRef`、`authorityRole`、`actedBy`、`decisionReason`、`result`、`runUrl` 与 artifact reference 仍是最低公共字段；
  - break-glass、blocking prerequisite 与 approval independence 未来可以由更强执行层自动判断，但最终仍应以统一 evidence model 输出审计结果，而不是各系统各记一套账。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: blocking-upgrade matrix fixed
- [x] `P0-C1-S2`: audit prerequisite boundary fixed
- [x] `P0-C1-S3`: approver independence baseline fixed

### P1 (Policy mapping)

- [x] `P1-C1-S1`: higher-environment approval/override wording fixed
- [x] `P1-C1-S2`: higher-environment rollback/evidence wording fixed

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: blocking-upgrade evidence referenced
- [x] `P2-C1-S2`: higher-environment restriction evidence referenced

### P3 (Runway)

- [x] `P3-C1-S1`: external-approval / multi-environment runway defined

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (existing governance records prove the blocking-upgrade entry can be expressed without changing schema | 2026-03-27)

- headSha: `7f3c417d`
- sourceRecordRef: `run:23599857316`
- targetEnvironment: `cloud-dev (reclassified as higher-environment blocking candidate for verification)`
- policyMode:
  - `recorded_soft_policy` in current `cloud-dev`
  - `blocking_candidate` in future higher-environment governance
- authorityRoles:
  - `approval_authority`
  - `rollback_authority`
- actedBy:
  - `samuelhu324-dev`（approval）
  - `workflow_auto_rollback`（rollback）
- decisionReasons:
  - `cloud-dev environment gate released for manual release run`
  - `verify_fail_auto`
- result:
  - `approval_granted`
  - `candidate_reverted_to_known_good`
- runUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23599857316`
- auditStatus: `audit_complete`
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/operator_guidance.txt`
  - `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
  - `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
- expected:
  - 现有 governance record 应足以支撑 higher-environment blocking-upgrade 的落账入口，而不是一进入更高环境就需要追加一套新字段；
  - same-actor approval、rollback authority、decision reason 与 evidence completeness 应能直接从已有字段中被重新解释为“满足”或“不满足” higher-environment contract；
  - 若 current schema 无法区分 actor overlap、authority role 或 rollback evidence completeness，则 `S4E-5A` 的 blocking-upgrade 路线就还不成立。
- observed:
  - approval record 已有 `requestedBy=samuelhu324-dev`、`actedBy=samuelhu324-dev`、`authorityRole=approval_authority` 与对应 run URL，因此即使当前 `cloud-dev` 将其接受为现实，future higher-environment 也能在不改 schema 的前提下把这条记录重解释为 `approval_independence_not_satisfied` 的 blocking candidate；
  - rollback record 已有 `authorityRole=rollback_authority`、`actedBy=workflow_auto_rollback`、`decisionReason=verify_fail_auto`、`result=candidate_reverted_to_known_good` 与 rollback evidence bundle，因此 future higher-environment 也能在同一骨架上表达“manual rollback 是否满足 evidence completeness / authority independence”；
  - `summary.json` 与 `operator_guidance.txt` 已证明 rollback evidence 不只是一句自由文本，而是能稳定回指到 source record、decision reason 与 artifact path；这说明当前 record/evidence skeleton 已足以作为 `S4E-5A/P2-C1-S1` 的 blocking-upgrade entry point。

### P2-C1-S2 (controlled higher-environment sample proves break-glass, approval independence, and manual rollback blocking are all recordable on the same skeleton | 2026-03-27)

- headSha: `7f3c417d`
- sourceRecordRef: `policy-simulation:23599857316-higher-environment-restrictions`
- targetEnvironment: `simulated-higher-environment`
- policyMode: `hard_gate`
- authorityRoles:
  - `approval_authority`
  - `override_actor`
  - `rollback_authority`
- actedBy:
  - `samuelhu324-dev`（simulated same-actor approval/override）
  - `pending_independent_actor`（required by policy but absent in the failing sample）
- decisionReasons:
  - `approval_independence_not_satisfied`
  - `break_glass_exception`
  - `manual_rollback_evidence_incomplete`
- result:
  - `blocked_before_approval`
  - `override_allowed_under_break_glass`
  - `blocked_before_override_or_rollback`
- runUrl: `n/a (controlled policy sample)`
- auditStatus:
  - `audit_complete` for the break-glass example once exception marker and evidence are present
  - `audit_incomplete` for the manual rollback blocking example when evidence bundle is absent
- artifacts:
  - `docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md`
  - `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
  - `docs/logs/log-S4E-3A-approval-hierarchy-and-rollback-authority.md`
- expected:
  - controlled higher-environment samples 应能在不新增 schema 的前提下，同时表达 approval independence failure、break-glass exception 与 manual rollback blocking；
  - evidence model 至少要能说明谁试图执行动作、为什么被阻断或被放行为例外、以及 evidence completeness 是否满足；
  - 若这些 higher-environment 情况必须依赖新字段或新的 record family，当前 `S4E-5A` 的“沿用 skeleton 加严规则”前提就不成立。
- observed:
  - approval independence failure 可以直接落为现有骨架中的 `authorityRole=approval_authority`、`actedBy=samuelhu324-dev`、`decisionReason=approval_independence_not_satisfied` 与 `result=blocked_before_approval`，不需要新增字段；
  - `break_glass_exception` 也可以继续用同一骨架表达：只需把 exception 原因压到 `decisionReason`，并把执行结论压到 `result=override_allowed_under_break_glass`，再用现有 `runUrl`/artifact reference 或受控文档 evidence 承接；
  - manual rollback blocking 同样可以用 `authorityRole=rollback_authority`、`decisionReason=manual_rollback_evidence_incomplete`、`auditStatus=audit_incomplete` 与 `result=blocked_before_override_or_rollback` 表达，说明 evidence model 已足够描述 “因为证据不全而被阻断”；
  - 因此，`S4E-5A/P2-C1-S2` 已验证 current evidence model 足以表达 `break_glass_exception`、approval independence 与 manual rollback blocking，后续需要加严的是 policy 与 execution gate，而不是 record schema 本身。

### P3-C1-S1 (future external approval systems and multi-environment governance must extend enforcement, not fork the schema | 2026-03-27)

- headSha: `fc5fd56c`
- sourceRecordRef: `phase:S4E-5A/P2`
- targetEnvironment: `future multi-environment governance`
- policyMode: `runway_defined`
- authorityRole: `governance_model_owner`
- actedBy: `documentation_phase_update`
- decisionReason: `future approval systems and release governance must reuse the existing action/evidence skeleton`
- result: `runway_defined`
- runUrl: `n/a (documentation phase handoff)`
- auditStatus: `audit_complete`
- artifacts:
  - `docs/logs/log-S4E-5A-higher-environment-governance-and-blocking-upgrades.md`
  - `docs/logs/log-S4E-release-operating-model-and-governance.md`
  - `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
- expected:
  - future GitHub environment reviewer expansion、external approval service 或 release ledger backend 应该增强 approval enforcement，而不是生成与现有 governance action record 平行的新账本；
  - multi-environment governance 应能沿用当前 `headSha`、`sourceRecordRef`、`authorityRole`、`actedBy`、`decisionReason`、`result`、`runUrl` 与 artifact reference 作为最低公共字段；
  - break-glass、blocking prerequisite、approval independence 等 future stronger enforcement 也应落在同一 evidence model 中，从而保持跨环境审计可比性。
- observed:
  - 当前 runway 已明确 future control-plane 的升级方向是“提升判定来源与执行 gate 的强度”，而不是替换 record schema；GitHub environment reviewers 扩展仍可回写为 `approval_authority` action record，外部 approval service 也应把最终批准/拒绝结果压回相同字段骨架；
  - release ledger backend 若后续出现，其职责应是存储、查询和交叉验证已有 governance action record，而不是把 `approval`、`override`、`rollback`、`break_glass_exception` 改写成另一套字段模型；
  - future multi-environment release governance 因此可以在不破坏现有 evidence continuity 的前提下继续提升 enforcement：例如自动判定 approver independence、自动拒绝 `audit_incomplete`、自动要求 dual approval，但这些都应输出回同一 skeleton；
  - 因此，`S4E-5A/P3` 已完成本 phase 的 runway 目标：未来外部审批系统、多环境治理与更强执行层都可以继续沿当前 schema 演进，而不是重开一条不兼容的治理主线。

## Recent changes (for traceability, optional)

- 2026-03-27: 已完成 `S4E-5A/P3-C1-S1` 的第一轮 runway 收口，当前已固定 future external approval system / multi-environment governance 的接入原则：继续沿用现有 governance action record / evidence skeleton，只增强执行 gate 与判定来源，不分叉 schema。
- 2026-03-27: 已完成 `S4E-5A/P2-C1-S1S2` 的第一轮 evidence 回填，当前已证明现有 governance record / evidence skeleton 足以承载 blocking-upgrade entry，以及 `break_glass_exception`、approval independence、manual rollback blocking 的受控 higher-environment 样本。
- 2026-03-27: 已完成 `S4E-5A/P1-C1-S1S2` 的第一轮 policy wording 收口，当前已固定 higher-environment approval / override restriction，以及 rollback authority / evidence completeness 的最小 blocking wording。
- 2026-03-27: 已完成 `S4E-5A/P0-C1-S1S2S3` 的第一轮 contract 收口，当前已固定 higher-environment blocking-upgrade matrix、`audit_incomplete -> blocking prerequisite` 边界，以及 approver independence / requester separation 的最小 enforced baseline。
- 2026-03-27: 首次创建 `S4E-5A` draft，用于承接 higher-environment governance / blocking-upgrade follow-up；当前入口重点是 `audit_incomplete -> blocking`、approver independence，以及 manual override / rollback restriction 的更高环境收紧。