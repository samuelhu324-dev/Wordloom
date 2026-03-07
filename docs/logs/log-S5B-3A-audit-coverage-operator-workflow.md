# log-S5B-3A-audit-coverage-operator-workflow（Phase 3：Audit coverage expansion + operator workflow v1）

---

**id**: `S5B-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `audit coverage expansion + operator workflow (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Authorization, Policy, Audit, Drills, Evidence, HardGate, Ops, epic/s5, epic/s5b, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **previous_log**: `docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md`
  **reference_log_1**: `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  **reference_log_2**: `docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md`
**created**: `2026-03-07`
**updated**: `2026-03-07`

---

## Decision / Outcome（结论区）

**Decision**:

- 扩展关键写入链路的 audit 覆盖面：保证 allow/deny/not_found/error 的口径一致，并保持 reason 低基数可枚举。
- 固化 operator workflow：给出可复跑的 drills/evidence，用于快速回放（replay）与取证（forensics），并可接入 CI hard gate。

**Default choices（本 phase 默认决策 / v1）**:

- 延续 `S5B-1A` 的 artifacts contract + verifier（schema_version 与 failure taxonomy 复用）。
- 依旧以“选少量高价值链路”推进，不做全库扫荡式重构。
- 不把高基数字段写入 metrics label；高基数只进 logs/artifacts。

## Definitions（概念定义，可选）

- **Audit coverage**：指定 action 的关键出入口，都能写入 audit_log 行（best-effort），并且 action/result/reason/tenant_id/request_id 可追溯。
- **Operator workflow**：面向排障/取证的最小流程：给定 request_id / actor_user_id / tenant_id 能快速定位相关 audit 行与关键上下文。
- **Replay**：用 drills 在相同 contract 下复现某类 deny/allow 场景，产出 artifacts 作为事实源。

## Constraints（约束）

- reason 必须低基数、可枚举，并写入 `audit_log.reason`（不得只写 meta_json）。
- 审计写入点与 action/result/reason 口径必须可被 drills 验证。
- 变更优先收口到既有 policy entrypoint / audit repo，不新增“又一套”散落逻辑。

## Scope（本 log 范围）

- `P0`：contract（覆盖范围、action 命名、reason taxonomy、evidence 口径）
- `P1`：实现（扩展 audit 覆盖点/一致化出口；必要的 policy/entrypoint 收口）
- `P2`：drills（新增/扩展 drills scenario 覆盖新增链路或新增出口）
- `P3`：operator workflow（把“怎么查/怎么回放”写成可执行脚本或最小 runbook，并用 evidence 验证）
- `P4`：hard gate（把 suite 接入 CI；或显式声明不接入原因）

## Success Criteria（DoD）

- 至少 1 条新增或强化的关键写入链路满足：
  - allow/deny/not_found/error 都能 best-effort 写 audit（action/result/reason 口径稳定）
  - reason 低基数且落在 `audit_log.reason`
  - drills 能复跑并产出可机械判定的 artifacts
- operator workflow 至少覆盖：
  - 通过 request_id 关联到 audit 行
  - 能给出最小“查询→定位→复现”步骤
- CI hard gate（如接入）：verifier exit code=0 且 `_result.json.ok==true` 才通过。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - `P0-P4` 的 contract + drills + operator workflow + hard gate（若适用）已跑通
  - Evidence 区有可追溯的 `headSha` + artifacts 路径（或 CI run URL）

## P0（Contract｜v1）

### P0-C1-S1（Coverage scope：选择覆盖范围）

- v1 选择 1~2 条高价值链路（写路径优先），明确 action 命名与“必须写 audit 的出口集合”。

### P0-C1-S2（Reason taxonomy：低基数白名单）

- 为新增链路/新增出口定义 reason allowlist（低基数），并声明落点必须为 `audit_log.reason`。

### P0-C1-S3（Evidence & artifacts contract｜v1）

- artifacts layout：复用 `S5B-1A`：
  - `docs/labs/_snapshot/auto/S5B-3A/<suite_id>/<run_id>/`
    - `_recipe.json`
    - `_result.json`
    - `_logs/run.log`
    - `_metrics/summary.json`
- schema_version：复用 `s5b-1a.recipe.v1 / s5b-1a.result.v1 / s5b-1a.metrics.v1`。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5B-3A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（实现：coverage expansion）

- P1-C1-S1：选定目标链路，定位当前 audit 覆盖缺口（出口/异常路径/口径漂移点）。
- P1-C1-S2：补齐/统一 audit 写入点与 reason taxonomy（必要时新增/复用 policy entrypoint）。

### P2（drills/evidence）

- P2-C1-S1：为目标链路新增 drills scenario（至少覆盖 1 个 deny 与 1 个非 deny 出口）。
- P2-C1-S2：用 verifier 验证 artifacts contract，并记录 evidence（headSha + artifacts 路径）。

### P3（operator workflow）

- P3-C1-S1：固化最小查询流程（request_id → audit 行 → action/result/reason → 复现入口）。

### P4（hard gate）

- P4-C1-S1：新增 hard gate entrypoint + CI workflow（或记录不接入原因）。

## Execution Checklist（unchecked）

### P0（Contract）

- [ ] `P0-C1-S1`：选择覆盖范围 + action 命名
- [ ] `P0-C1-S2`：reason taxonomy（低基数白名单）
- [ ] `P0-C1-S3`：evidence/artifacts contract（复用 S5B-1A verifier）

### P1（实现）

- [ ] `P1-C1-S1`：定位 audit 覆盖缺口
- [ ] `P1-C1-S2`：补齐/统一出口口径（action/result/reason）

### P2（drill/verify）

- [ ] `P2-C1-S1`：新增 drills scenario
- [ ] `P2-C1-S2`：verifier 通过并记录 evidence

### P3（operator workflow）

- [ ] `P3-C1-S1`：最小查询/回放流程固化

### P4（hard gate）

- [ ] `P4-C1-S1`：CI hard gate 接入（或记录不接入原因）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

## Recent changes（for traceability，可选）

- 2026-03-07：scaffold Phase 3 log skeleton.
