# log-S5B-1A-policy-audit-hard-gate-drills（Phase 1：Policy/Audit hard-gate drills v1）

---

**id**: `S5B-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `policy/audit hard-gate drills (tenant boundary + deny reasons + request_id traceability) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Authorization, Policy, Audit, Drills, Evidence, HardGate, epic/s5, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **previous_log**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
  **reference_log_1**: `docs/logs/log-S5A-1A-authcontext-policy-audit.md`
  **reference_log_2**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
**created**: `2026-03-06`
**updated**: `2026-03-06`

---

## Decision / Outcome（结论区）

**Decision**:

- 把路线 C 的“安全骨架正确性”做成 **hard-gate drills**：每次变更 policy/audit/auth context 都能用一组最小场景回归验证，并产出 machine-verifiable evidence。
- v1 先交付最小闭环：
  - tenant boundary（跨 tenant 访问被拒）
  - role deny reasons（not_member/not_admin/tenant_mismatch）
  - audit traceability（request_id 能串起 deny/allow 的审计记录）

**Default choices（本 phase 默认决策 / v1）**:

- 演练环境优先 dev/test（DB-only + API）；不引入生产级 IdP。
- evidence 以 artifacts JSON 为事实源（PASS/FAIL 可机械判定），log 只记 headSha + 路径/Run URL。
- 拒绝语义：默认 404（防存在性泄露），但 deny 的审计必须记录低基数 reason（详见 P0）。

## Definitions（概念定义，可选）

- **AuthContext**：统一请求安全上下文（`user_id/tenant_id/roles/request_id`）。
- **Policy**：集中授权规则表达层；handler/service 只负责加载资源（含 tenant filter）并调用 policy。
- **Audit**：append-only 操作日志（deny/allow/关键写成功），以 `request_id` 关联。
- **Hard gate drill**：可重复执行的最小场景集合，输出 artifacts 并给出 PASS/FAIL。

## Constraints（约束）

- reason taxonomy 必须低基数白名单（禁止把 exception message、ids 直接当 reason）。
- drills 必须能在 CI 或本地重复跑通；产物结构稳定。
- 不扩展到复杂 RBAC/ACL；只验证 RBAC-lite + tenant boundary 的最小集合。

## Scope（本 log 范围）

- `P0`：contract（deny 语义、audit 口径、reason 白名单、evidence schema）
- `P1`：实现最小 drills runner（脚本/场景）
- `P2`：drills: tenant escape（越权读/写）
- `P3`：drills: audit completeness（request_id/actor/tenant/action/result/reason）
- `P4`：hard gate（可选）：CI workflow 或单命令 pipeline

## Success Criteria（DoD）

- contract 层面：
  - 统一 deny 语义（404 vs 403）与审计 result/reason 口径，写入 P0。
  - reason 白名单明确：`tenant_mismatch/not_member/not_admin/not_owner`（可扩展但需显式）。

- drills 层面：
  - 至少 3 个 drills scenario（每个都能独立 PASS/FAIL）：
    - tenant 越权读（预期 404 或 403；按 contract）
    - role 不足写（预期 403 + reason=not_admin 或等价）
    - audit 完整性（预期写入 1 条 audit_log，且 request_id 能关联）
  - 每个 scenario 输出 artifacts：
    - `_result.json`（含 pass/fail + observed/expected）
    - `_logs/`（至少 1 个非空日志文件）
    - `_metrics/`（至少 1 个非空指标文件，或明确声明不适用并给出替代证据）

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0 contract 稳定；
  - 至少 3 个 drills scenario 可复跑且 PASS/FAIL 机械可判定；
  - Evidence 区有可追溯 headSha + artifacts 路径（或 CI run URL）。

## P0（Contract｜v1）

### P0-C1-S1（Authorization contract：deny semantics + reason taxonomy）

- 未认证：401（不写 audit，除非未来需要专门的 authn audit）。

**Deny semantics（v1 固定选择）**

- 跨 tenant（`auth.tenant_id != request.library_id` 或等价判定）：
  - read：404（避免泄露存在性），audit：`result=not_found`，reason=`tenant_mismatch`
  - write/admin：403，audit：`result=denied`，reason=`tenant_mismatch`

- 同 tenant 但无 membership：
  - read：404，audit：`result=not_found`，reason=`not_member`
  - write/admin：403，audit：`result=denied`，reason=`not_member`

- 同 tenant 且为 member 但非 admin（admin 动作）：403，audit：`result=denied`，reason=`not_admin`

**Drills guardrail（避免 404 歧义）**

- drills 中所有验证 404 的用例必须确保资源真实存在；否则“资源不存在”与“授权拒绝”不可区分。
- v1 drills 里：404 只用于验证 **授权拒绝的 404**（tenant/membership），不覆盖“自然缺失资源”的 404。

### P0-C1-S2（Audit contract：action/result/reason 字段口径）

**Schema alignment（与 DB 表一致）**

- `audit_log` 字段上限：
  - `request_id`：<= 64 chars
  - `action`：<= 80 chars
  - `result`：<= 32 chars
  - `reason`：<= 80 chars

**Action 命名（v1 固定选择）**

- 格式：`<resource>.<verb>`（优先）或 `<domain>.<resource>.<verb>`（需要分域时再用）。
- 允许字符：`a-z0-9_` 与 `.`；必须全小写；禁止空格与 `-`。
- 建议 verbs 白名单（v1）：`get | list | create | update | delete | grant | revoke`。
- 示例（与现有模块对齐）：
  - `bookshelf.get` / `bookshelf.list` / `bookshelf.create`
  - `book.get` / `book.list`
  - `membership.grant` / `membership.revoke`

**Result 枚举（v1 固定选择）**

- `success | denied | not_found | error`
- HTTP 映射（drills 用于机械判定）：
  - `success` → 2xx
  - `denied` → 403
  - `not_found` → 404（仅用于“授权拒绝的 404”，见 `P0-C1-S1` guardrail）
  - `error` → 4xx/5xx（drills 里一律视为失败，除非显式声明期望）

**Reason taxonomy（低基数白名单）**

- v1 白名单：`tenant_mismatch | not_member | not_admin | not_owner | bad_request | internal_error | dependency_error`
- 必填规则：
  - `result in {denied, not_found}` → `reason` 必填且必须来自白名单
  - `result == success` → `reason` 必须为空
  - `result == error` → `reason` 可选；若填写必须来自白名单（优先 `bad_request/internal_error/dependency_error`）

**Required / Optional fields（v1）**

- 必填：`tenant_id`, `actor_user_id`, `request_id`, `action`, `result`
- 推荐：`resource_type`, `resource_id`（当 action 针对某个资源实例时）
- `meta_json`（可选）：
  - 允许的稳定键（v1）：`http_method`, `path_template`, `status_code`, `policy_rule`, `decision_point`
  - 禁止写入：token/密码/原始 header、以及会造成高基数聚合爆炸的自由文本（如 exception message）

### P0-C1-S3（证据口径 contract｜v1）

目标：evidence 必须 **可机械判定 PASS/FAIL**，并且能把“期望/观测/差异”结构化落盘。

**Artifacts directory layout（v1 固定）**

- 每次 run 输出到一个唯一目录：
  - `docs/labs/_snapshot/auto/S5B-1A/<suite_id>/<run_id>/`
- 目录内至少包含（全部非空）：
  - `_recipe.json`（运行参数与输入；必须是合法 JSON）
  - `_result.json`（判定结果与 evidence；必须是合法 JSON）
  - `_logs/`（至少 1 个非空文件，如 `run.log`）
  - `_metrics/`（至少 1 个非空文件，如 `summary.json` 或 `metrics.prom`）

**_result.json schema（v1）**

- 顶层字段（必填）：
  - `schema_version`: `"s5b-1a.result.v1"`
  - `ok`: boolean（整次 run 是否通过；hard gate 直接用它）
  - `meta`:
    - `run_id`: string（UUID recommended）
    - `suite_id`: string（例如 `tenant_escape_read`）
    - `started_at`: string（ISO-8601, UTC）
    - `finished_at`: string（ISO-8601, UTC）
    - `git_sha`: string（可选，但 CI 必填）
  - `summary`:
    - `total`: int
    - `passed`: int
    - `failed`: int
  - `cases`: array（至少 1 个 case）

- `cases[*]` 字段（必填）：
  - `case_id`: string（低基数、稳定；例如 `tenant_cross_read_404`）
  - `title`: string
  - `inputs`（最小集合；必填）：
    - `request_id`: string（若由服务生成，则记录获取方式）
    - `tenant_id`: string
    - `actor_user_id`: string
    - `roles`: array[string]
    - `http`:
      - `method`: string
      - `path`: string
      - `path_template`: string（推荐；便于聚合）
  - `expected`（必填）：
    - `http_status`: int
    - `audit_expected`: boolean
    - `audit`（当 `audit_expected=true` 时必填）：
      - `action`: string
      - `result`: string（来自 `P0-C1-S2` result 枚举）
      - `reason`: string | null（按 `P0-C1-S2` 必填规则）
  - `observed`（必填）：
    - `http_status`: int
    - `audit_rows`:
      - `count`: int
      - `rows`: array[object]（建议包含 `action/result/reason/occurred_at`；允许截断，但必须保证能机械判定）
  - `verdict`（必填）：
    - `ok`: boolean
    - `failure_reason`: string | null（若 `ok=false` 必填；必须低基数，见下）

**failure_reason taxonomy（v1 白名单）**

- `http_status_mismatch`
- `audit_missing`
- `audit_count_mismatch`
- `audit_action_mismatch`
- `audit_result_mismatch`
- `audit_reason_mismatch`
- `schema_violation`
- `unexpected_error`
- `dependency_unreachable`

**Notes（机械判定约束）**

- `ok` 必须等价于：所有 `cases[*].verdict.ok == true`。
- `audit_rows.rows` 里禁止包含敏感信息（token/密码/原始 headers）。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5B-1A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（实现 drills runner）

- P1-C1-S1：新增最小 drills runner（建议 Python），支持：设置请求头（tenant/request_id）、发起 API 请求、查询 audit_log、输出 `_result.json`。
- P1-C1-S2：固化 artifacts contract（目录结构 + 非空检查 + PASS/FAIL 判定）。
- P1-C1-S3：跑 1 次 smoke run 并入账 Evidence（记录 headSha + artifacts 路径 + ok/failed 摘要）。

### P2（Drills：tenant escape）

- P2-C1-S1：tenant 越权读（跨 library_id 读 book/bookshelf）
- P2-C1-S2：tenant 越权写（跨 library_id 写 book/bookshelf/block）

### P3（Drills：audit completeness）

- P3-C1-S1：deny 的 audit 记录完整性（action/result/reason/request_id）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：deny semantics + reason taxonomy 固化
- [x] `P0-C1-S2`：audit action/result/reason 口径固化
- [x] `P0-C1-S3`：evidence JSON schema 固化

### P1（实现）

- [x] `P1-C1-S1`：drills runner 产出 `_result.json` + logs/metrics
- [x] `P1-C1-S2`：artifacts contract 检查（非空 + PASS/FAIL）
- [x] `P1-C1-S3`：smoke run + Evidence 入账（首条可追溯 artifacts）

### P2（drill/verify）

- [x] `P2-C1-S1`：tenant escape read drill
- [x] `P2-C1-S2`：tenant escape write drill

### P3（drill/verify）

- [ ] `P3-C1-S1`：audit completeness drill

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

- 代码落地点（P1）：
  - drills runner：`scripts/drills/s5b1a_p1c1s1_drills_runner.py`
  - artifacts verifier：`scripts/drills/s5b1a_verify_artifacts.py`

### P1-C1-S3（smoke run｜2026-03-06）

- headSha：`80de87140c9e4df136cfe8c5cd029e03f1df0d90`
- artifacts：`docs/labs/_snapshot/auto/S5B-1A/tenant_escape_read/d3d9073c-4c26-4218-94fe-83eaa4257243/`
- 结果：FAIL（`ok=false`；case=`tenant_cross_read_404`；`failure_reason=unexpected_error`）
- 观测：`_logs/run.log` 记录 `error_type=ConnectError`（依赖不可达；优先检查 API `WORDLOOM_API_BASE_URL` 与 DB `DATABASE_URL`）。

### P1-C2-S1（smoke run｜2026-03-06｜green）

- headSha：`9bdd2dd50c160be2abaea74a27fe00f997c07acd`
- artifacts：`docs/labs/_snapshot/auto/S5B-1A/tenant_escape_read/bea96ea4-448c-4ee8-a385-490f766ef593/`
- 结果：PASS（`ok=true`；case=`tenant_cross_read_404`）
- 环境要点：API `WORDLOOM_API_BASE_URL=http://localhost:31001`；DB `DATABASE_URL=...:5435/wordloom_dev`；actor 默认 `S5B_1A_ACTOR_USER_ID=550e8400-e29b-41d4-a716-446655440000`

### P2-C1-S1（tenant escape read drill｜2026-03-06｜green）

- headSha：`d9bbd4593802beefccf339e19a25277e8ffc5bfb`
- artifacts：`docs/labs/_snapshot/auto/S5B-1A/tenant_escape_read/a9b12489-490a-42f8-9c7a-5f0c8ae11e2c/`
- 结果：PASS（`ok=true`；cases=`tenant_cross_read_404` + `tenant_cross_book_read_404`）
- 期望（expected）：
  - cross-tenant bookshelf.get → 404 + audit `not_found` + reason=`tenant_mismatch`
  - cross-tenant book.get → 404 + audit `not_found` + reason=`tenant_mismatch`
- 观测（observed）：
  - 两个 case 都命中 404；并能通过 request_id 在 `audit_log` 找到对应 deny 记录（reason 低基数且可机械判定）。

### P2-C1-S2（tenant escape write drill｜2026-03-06｜green）

- headSha：`18b1406050afa62f93a66d6ee14cd5933c4ec84e`
- artifacts：`docs/labs/_snapshot/auto/S5B-1A/tenant_escape_write/d93e1710-9e31-4ee4-a425-d28df7cff7fe/`
- 结果：PASS（`ok=true`；case=`tenant_cross_write_403`）
- 期望（expected）：
  - cross-tenant bookshelf.create → 403 + audit `denied` + reason=`tenant_mismatch`
- 观测（observed）：
  - 命中 403；并能通过 request_id 在 `audit_log` 找到对应 denied 记录（reason 低基数且可机械判定）。

## Recent changes（for traceability，可选）

- 2026-03-06：scaffold Phase 1 log skeleton.
