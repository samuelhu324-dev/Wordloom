# log-S5B-3A-audit-coverage-operator-workflow（Phase 3：Audit coverage expansion + operator workflow v1）

---

**id**: `S5B-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `audit coverage expansion + operator workflow (drills/evidence) v1`
**status**: `stable`           # draft | stable | archived
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

- [x] `P0-C1-S1`：选择覆盖范围 + action 命名
- [x] `P0-C1-S2`：reason taxonomy（低基数白名单）
- [x] `P0-C1-S3`：evidence/artifacts contract（复用 S5B-1A verifier）

### P1（实现）

- [x] `P1-C1-S1`：定位 audit 覆盖缺口
- [x] `P1-C1-S2`：补齐/统一出口口径（action/result/reason）

### P2（drill/verify）

- [x] `P2-C1-S1`：新增 drills scenario
- [x] `P2-C1-S2`：verifier 通过并记录 evidence

### P3（operator workflow）

- [x] `P3-C1-S1`：最小查询/回放流程固化

### P4（hard gate）

- [x] `P4-C1-S1`：CI hard gate 接入（或记录不接入原因）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

**P1-C1-S1（现状定位：membership audit coverage｜2026-03-07）**

- Chain 1：`membership.grant`（POST /libraries/{library_id}/memberships）
  - Call chain：HTTP router → `assert_actor_can_manage_memberships`（policy）→ `SQLAlchemyLibraryMembershipRepository.grant_role`（repo）。
  - Audit（today）：
    - allow：grant/update 成功时写 1 行 audit，`action=membership.grant`，`result=success`，`reason=null`，`resource_type=library_membership`，`resource_id=<membership_id>`，并在 meta_json 里附带 `library_id/member_user_id/role`。
    - deny（403）：仅当 policy 抛出 403 时写 audit，`action=membership.grant`，`result=denied`，`reason` 来自 `exc.detail["reason"]`（即 `not_member|not_admin|tenant_mismatch`），`resource_type=library`，`resource_id=<tenant_id>`。
  - Gaps vs P0 contract：
    - not_found：当前 grant 语义是幂等 upsert，不存在 404/not_found 分支 → 视作 N/A（P0 中 not_found 要求对 grant 链路不强制）。
    - error：当出现非 403 的 `HTTPException` 或其他未捕获异常时（例如 DB 错误/业务异常），router 不写 audit 行，未能覆盖 P0 中 `result=error` + `reason in {domain_error, unexpected_error}` 的约定。

- Chain 2：`membership.revoke`（DELETE /libraries/{library_id}/memberships/{user_id}）
  - Call chain：HTTP router → `assert_actor_can_manage_memberships`（policy）→ `SQLAlchemyLibraryMembershipRepository.revoke`（repo）。
  - Audit（today）：
    - allow：无论 `deleted` 为 0 还是 1，router 都固定写 1 行 audit，`action=membership.revoke`，`result=success`，`reason=null`，`resource_type=library`，`resource_id=<tenant_id>`，meta_json 中记录 `deleted` 布尔值。
    - deny（403）：当 policy 抛出 403 时写 audit，`action=membership.revoke`，`result=denied`，`reason` 来自 `exc.detail["reason"]`（`not_member|not_admin|tenant_mismatch`），`resource_type=library`，`resource_id=<tenant_id>`。
  - Gaps vs P0 contract：
    - not_found：P0 期望“目标 membership 不存在 / 已撤销”分类为 `result=not_found` + `reason=null`，但当前实现将 `deleted=0` 也记为 `result=success`，仅在 meta_json 中埋点，导致 operator 从 audit_log 难以区分“删除成功”与“已不存在”。
    - error：与 grant 类似，非 403 的 `HTTPException`（例如未来的 404/409）以及 DomainException/500 目前不会写 audit 行，缺少 `result=error` + `reason in {domain_error, unexpected_error}` 覆盖。
    - resource 粒度：grant 的 success 审计以 membership 作为 resource，而 revoke 的 success/deny 都以 library 作为 resource，虽然不违反本 phase contract，但会在后续 P3（operator workflow）中显式权衡是否需要统一。

**P1-C1-S2（实现摘要：membership audit exits 对齐｜2026-03-07）**

- grant（`membership.grant`）：
  - 入口不变，继续依赖 `assert_actor_can_manage_memberships` 做 403 deny（`reason` 来自 `not_member|not_admin|tenant_mismatch`）。
  - 补齐 error 出口：
    - `HTTPException`：
      - 403 → `result=denied`，`reason` 来自 `detail.reason`（白名单）。
      - 其他 4xx/5xx → `result=error`，`reason` 若为空则归一到 `domain_error`。
    - `LibraryDomainException` / shared `DomainException` → `result=error`，`reason=domain_error`，并在 `meta_json.error_type` 记录异常类型。
    - 兜底 `Exception` → `result=error`，`reason=unexpected_error`，同样带 `error_type`。
  - allow 出口保持为 `result=success` + `reason=null`，未引入 not_found 分支（grant 仍视为幂等 upsert）。

- revoke（`membership.revoke`）：
  - allow/not_found 出口合并到统一审计：
    - repo 返回 `deleted=True` → `result=success`，`reason=null`。
    - repo 返回 `deleted=False` → `result=not_found`，`reason=null`，并在 `meta_json.deleted` 标记 0/1，满足 P0 对“已不存在”的分类要求。
  - 403/404/其他 HTTP 错误归一：
    - 403（policy deny）→ `result=denied`，`reason` 来自 `detail.reason`（白名单）。
    - 404 → `result=not_found`，`reason` 沿用 `detail.reason`（若空则为 null）。
    - 其他 4xx/5xx → `result=error`，`reason` 若为空则归一到 `domain_error`。
  - `LibraryDomainException` / shared `DomainException` → `result=error`，`reason=domain_error`，带 `error_type`；兜底 `Exception` → `result=error`，`reason=unexpected_error`。
  - resource 粒度暂维持 `resource_type=library resource_id=tenant_id`，与 P0 合同一致，是否需要切到 membership 级别留待 P3 再评估。

**P2-C1-S1（membership_audit_coverage drills scaffold｜2026-03-07）**

- 新增 drills runner：`scripts/drills/s5b3a_p2c1s1_drills_runner.py`，复用 S5B-1A 的 artifacts contract/schema 与 failure taxonomy，suite_id=`membership_audit_coverage`。
- 当前 cases（v1）：
  - `grant_success`：admin grant 成功 → `membership.grant` `success`。
  - `revoke_success`：admin revoke 成功 → `membership.revoke` `success`。
  - `revoke_not_found`：第二次 revoke 同一 membership → `membership.revoke` `not_found`。
  - `grant_not_admin_403`：member 尝试管理 membership → `membership.grant` `denied` reason=`not_admin`。
  - `revoke_domain_error`：故意构造异常场景（tenant header mismatch 等）→ `membership.revoke` `error`（reason 归一到低基数）。
- 本地运行记录：
  - Run #1（dev env, DB 未就绪）：
    - headSha=`b56cd9c63bd9d20fbc9e922cbb29a5428f32b00d`。
    - run_dir=`backend/docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/96f9f002-28e5-4835-9efb-cdc5092c0e42/`。
    - 所有 cases 因 `OperationalError`（数据库未连通）被标记为 `unexpected_error`，仅作为早期 scaffold 记录，不视为 P2 green evidence。
  - Run #2（指向 wordloom_test 测试库）：
    - headSha=`7995b73482a1dbfd30b79af4c927c71d72ff5a61`。
    - run_dir=`backend/docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/6eed8594-9a55-462f-8ed2-c92e8e8f7b7b/`。
    - runner 使用 `DATABASE_URL=postgresql://wordloom:wordloom@127.0.0.1:5435/wordloom_test`，API base=`http://127.0.0.1:31001`。
    - `_logs/run.log`：`error_type=ProgrammingError`，说明数据库已连通，但在访问 audit 相关表或 SQL 时出现编程级错误（例如 schema 不一致 / SQL 兼容性问题）。
    - `_result.json.summary`：`total=5, passed=0, failed=5`，每个 case 的 `failure_reason=unexpected_error`（属于 runner 顶层异常兜底）。
    - verifier：`python scripts/drills/s5b1a_verify_artifacts.py --run-dir <run_dir>` 输出 `[contract_ok] Artifacts contract OK`，但 exit code=1（因为 `_result.json.ok=false`），说明 artifacts 结构/字段满足 S5B-1A contract，但业务语义尚未通过。
  - Run #3（通过 S0D-2A hard gate 入口 `scripts/drills/s5b3a_p4_hard_gate.py`｜指向 wordloom_test 测试库）：
    - headSha=`7995b73482a1dbfd30b79af4c927c71d72ff5a61`。
    - run_dir=`docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/9d3cdfc1-2fb0-43c8-8364-a00b5db4e87e/`。
    - hard gate 入口在 repo 根执行：`python scripts/drills/s5b3a_p4_hard_gate.py`，内部复用同一 runner + verifier，并将结果写入 `artifacts/s5b3a-runs.json`。
    - 本次 run drills 本身仍然 `ok=false`（5 个 case red，verifier rc=1），但通过 S0D-2A 的入口产生了一条结构化记录：`log_id=S5B-3A, phase=P2, cycle=C1, step=S1, ok=false, contract_ok=true, result_ok=false`，为后续 green evidence 奠定自动化管道。
- 结论：目前 P2 drills 已可在测试库环境下完整跑通并产出符合 contract 的 artifacts，且已通过 S5B-3A hard gate / S0D-2A pipeline 接入 write_gate 汇总；上面的 Run #1-3 主要记录早期 red evidence，正式满足 P2 DoD 的 green run 见下方 `P2-C1-S2`。

**P2-C1-S2（membership_audit_coverage 首次 green run｜2026-03-08）**

- headSha：`a5fa15bff07369430516bae55af876fdda188822`
- run_dir：`docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/16b34278-d370-4be4-9e8f-29a455e25111/`
- ci_url：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22810323199`
- env：
  - `WORDLOOM_API_BASE_URL=http://127.0.0.1:31001`
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@127.0.0.1:5435/wordloom_test`
- 期望（expected）：
  - hard gate 入口 exit code=0；
  - verifier `contract_ok=true` 且 `_result.json.ok=true`；
  - `artifacts/s5b3a-runs.json` 追加一条 `ok=true / contract_ok=true / result_ok=true` 记录。
- 观测（observed）：
  - 通过 CI workflow `hard-gate-s5b3a-membership-audit`（见上方 ci_url）触发 S5B-3A hard gate 入口；
  - `Run S5B-3A hard gate` 步骤输出：
    - `runner_rc=0`，drills runner 正常完成；
    - `verify_rc=0`，`[contract_ok] Artifacts contract OK`；
    - `--- summary --- log_id=S5B-3A phase=P2 cycle=C1 step=S1 ok=True contract_ok=True result_ok=True run_dir=docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/16b34278-d370-4be4-9e8f-29a455e25111`；
  - CI artifacts 中包含对应的 `docs/labs/_snapshot/auto/S5B-3A/...` 与 `artifacts/s5b3a-runs*.json`，可在 `artifacts/s5b3a-runs.json` 中找到对应的 `HardGateRunRecord` 条目；
  - 至此，S5B-3A 侧 P2 drills + verifier 已有首条通过 CI / hard gate 入口的 green evidence，可勾选本 log 的 P2-C1-S1 / P2-C1-S2 checklist。

**P3-C1-S1（membership audit operator workflow｜2026-03-08）**

- 目标：给 membership grant/revoke 相关的排障/取证提供一套最小“查询→定位→复现”流程，并与本 log 的 drills/hard gate 证据对齐；
- 查询阶段：
  - 通过 `request_id` / `actor_user_id` / `tenant_id` 在 `audit_log` 中定位相关行，关注 `action=result=reason` 组合是否落在本 log 约定的低基数空间内；
  - 将观测到的组合映射到 `membership_audit_coverage` 的 cases（如 `grant_success` / `revoke_not_found` / `grant_not_admin_403` / `revoke_domain_error`），判断属于哪一类出口；
- 复现阶段（test / staging 环境）：
  - 在设置好 `WORDLOOM_API_BASE_URL` 与 `DATABASE_URL` 后，运行 `python scripts/drills/s5b3a_p2c1s1_drills_runner.py` 或直接调用 hard gate 入口 `python scripts/drills/s5b3a_p4_hard_gate.py`；
  - 通过 stdout 中的 run_dir 或 `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/...` 路径找到对应 `_recipe.json/_result.json/_logs/_metrics`，对比 case 结果与真实 incident；
- 对齐阶段：
  - 若 drills 结果为 green（如上 `P2-C1-S2` 所示），但线上 incident 暗示行为不一致，则以 drills 为“期望行为”，以 `audit_log` 行为“实际行为”，推动进一步的 schema/代码修复；
  - 若 drills 本身为 red，则先以 S5B-3A/S0D-2A 的 pipeline 为主线修复，实现新的 green run 再回到 operator 视角复盘。

**P4-C1-S1（CI hard gate wiring｜2026-03-08）**

- hard gate 入口脚本：`scripts/drills/s5b3a_p4_hard_gate.py`：
  - 运行 `membership_audit_coverage` drills runner；
  - 通过 `_shared_artifacts.extract_run_dir_from_output` 发现最新 run_dir；
  - 调用 `scripts/drills/s5b1a_verify_artifacts.py` 对 run_dir 做 contract + result 校验；
  - 将 `log_id=S5B-3A, phase=P2, cycle=C1, step=S1, head_sha, suite_id, run_dir, ok, contract_ok, result_ok, ci_url, created_at` 等字段写入 `artifacts/s5b3a-runs.json`；
  - 以 verifier 的 exit code 作为 hard gate 进程的返回码。
- CI workflow：`.github/workflows/hard-gate-s5b3a-membership-audit.yml`：
  - 触发条件：对 backend membership/audit 相关代码、S5B-3A log、S0D-2A log 或本 workflow 自身的 PR 变更，或手动 `workflow_dispatch`；
  - job 步骤摘要：
    - 使用 `docker-compose.devtest-db.yml` 启动 devtest Postgres，并准备好 `wordloom_test` 数据库；
    - 安装 backend 依赖并对 `wordloom_test` 运行 Alembic 迁移；
    - 以 `uvicorn api.app.main:app --host 127.0.0.1 --port 31001` 启动 API；
    - 设置 `WORDLOOM_API_BASE_URL` 与 `DATABASE_URL`，执行 `python scripts/drills/s5b3a_p4_hard_gate.py`；
    - 将 `docs/labs/_snapshot/auto/S5B-3A/**` 与 `artifacts/s5b3a-runs*.json` 作为 CI artifacts 上传，便于后续审计与取证；
  - hard gate 语义：CI 直接以 hard gate 脚本的 exit code 作为 job 成功/失败依据；结合 `artifacts/s5b3a-runs.json` 与 `_result.json.ok`，确保只有 `ok=true / contract_ok=true / result_ok=true` 的 run 才被视为通过。

## P0（Contract｜v1）

### P0-C1-S1（Coverage scope：选择覆盖范围）

- v1 选定 2 条与多租户 RBAC 强相关的写路径，并固定 canonical action：
  - Chain 1：`POST /libraries/{library_id}/memberships` → 授予/更新库成员角色
    - Audit action：`membership.grant`
  - Chain 2：`DELETE /libraries/{library_id}/memberships/{user_id}` → 撤销库成员资格
    - Audit action：`membership.revoke`
- 两条链路都视为“关键写路径”，要求在下列出口 best-effort 写入 audit_log 行（action 固定为上面的 canonical 名）：
  - allow：2xx（grant / revoke 成功）→ `result=success`，`reason=null`
  - deny（auth/policy）：403（`assert_actor_can_manage_memberships` 触发）→ `result=denied`，`reason` 来源于 reason 白名单
  - not_found：404（目标 membership 不存在 / 已被撤销）→ `result=not_found`，`reason=null`
  - error：4xx/5xx domain / unexpected error → `result=error`，`reason` 落在错误类白名单中（见下一小节）。

### P0-C1-S2（Reason taxonomy：低基数白名单）

- 两条 membership 写路径共享一套低基数 reason 白名单，并且所有非 null 的 reason 必须写入 `audit_log.reason` 字段（不得只写在 `meta_json` 中）：
  - `not_member`：无库 membership / 无角色（来源：`library_membership_policy.REASON_NOT_MEMBER`）
  - `not_admin`：仅为 member，权限不足以管理 membership（来源：`library_membership_policy.REASON_NOT_ADMIN`）
  - `tenant_mismatch`：请求访问非本 tenant 的 library（来源：`library_membership_policy.REASON_TENANT_MISMATCH`）
  - `domain_error`：业务校验失败但仍由应用层捕获（例如参数非法、状态不允许变更）。
  - `unexpected_error`：未预期的 5xx / 未被更细粒度分类覆盖的异常。
- 允许 `reason=null` 仅出现在：
  - `result=success`（正常写路径成功）；
  - `result=not_found`（资源不存在 / 已被撤销，不引入高基数 reason）。

### P0-C1-S3（Evidence & artifacts contract｜v1）

- suite（v1）：
  - `suite_id`：`membership_audit_coverage`
  - runner：`python scripts/drills/s5b3a_p2c1s1_drills_runner.py`
- artifacts layout：复用 `S5B-1A`：
  - `docs/labs/_snapshot/auto/S5B-3A/<suite_id>/<run_id>/`
    - `_recipe.json`
    - `_result.json`
    - `_logs/run.log`
    - `_metrics/summary.json`
- schema_version：复用 `s5b-1a.recipe.v1 / s5b-1a.result.v1 / s5b-1a.metrics.v1`。
- verifier & failure taxonomy：
  - verifier：`python scripts/drills/s5b1a_verify_artifacts.py --run-dir <run_dir>`
  - failure_reason 仅允许：`http_status_mismatch` / `audit_missing` / `audit_action_mismatch` / `audit_result_mismatch` / `audit_reason_mismatch` / `schema_violation` / `unexpected_error`。


## Recent changes（for traceability，可选）

- 2026-03-07：scaffold Phase 3 log skeleton.
