# log-S5A-2A-library-membership-roles-policy-audit（Phase 2：Library membership + roles + policy + audit v2）

---

**id**: `S5A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `library membership & roles v1 (RBAC-lite), policy expansion, audit coverage, drills`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Auth, Authorization, Policy, Audit, RBAC, Membership, Drills, epic/s5, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5A-security-governance.md`
  **previous_log**: `docs/logs/log-S5A-1A-authcontext-policy-audit.md`
**created**: `2026-03-02`
**updated**: `2026-03-02`

---

## Decision / Outcome（结论区）

**Decision**:

- 在 `S5A-1A` 的 AuthContext/tenant/policy/audit v1 骨架之上，补齐 “真实 membership + roles 来源” 与更完整的 policy 覆盖：
  - roles 不再主要依赖 dev fallback，而是由 `library_membership`（或等价模型）作为 SoT 驱动。
  - 扩展 policy 覆盖到关键写操作与管理操作（至少 1 条 admin 动作 + 1 条非 admin 被拒绝）。
  - 扩展审计覆盖：membership 变更、关键写成功、关键拒绝（低基数 reason）。

## Constraints（约束）

- **RBAC-lite 优先**：先落地 `owner/admin/member` 最小角色集合，不引入复杂 ACL/OPA。
- **tenant 边界不回退**：所有 membership/policy 查询仍必须按 `tenant_id == library_id` 约束。
- **reason 低基数**：拒绝原因只允许来自白名单（如 `not_member/not_admin/not_owner/tenant_mismatch`）。
- **审计 append-only**：继续保持 audit_log 只 INSERT；禁止 UPDATE/DELETE。

## Scope（本 log 范围）

- `P0`：Membership/Roles contract（字段、来源、错误语义、审计口径）
- `P1`：实现 membership SoT（表/ORM/repo）+ AuthContext roles 解析（最小可用）
- `P2`：Policy 扩展（至少覆盖 1 个 admin 动作 + 1 个写动作）
- `P3`：Audit 扩展 + drills/evidence（至少 3 个 scenario + artifacts）

## Success Criteria（DoD）

- 代码层面：
  - 有明确的 membership SoT（`library_membership` 或等价表），可查询得到 `user_id` 在 `library_id` 下的角色。
  - `AuthContext.roles` 来自 membership（dev fallback 仅限 dev/test 且可配置关闭）。
  - policy 层能表达并强制：
    - 非 member 不能访问 tenant 内资源（按 contract 决定 404 或 403，但全局一致）。
    - member 不能执行 admin 动作（403 + reason）。
  - audit_log 覆盖：
    - membership 变更成功（success）
    - admin 动作拒绝（denied + low-cardinality reason）

- 证据层面：
  - 至少 3 个 drills 并产出 artifacts（JSON）：
    - 非 member 访问被拒（404/403 + audit denied/not_found）
    - member 执行 admin 动作被拒（403 + audit denied + reason=not_admin）
    - admin/owner 执行 admin 动作成功（2xx + audit success）

## P0（Contract｜v1）

### P0-C1-S1（角色模型与来源）

- 默认 roles：`owner | admin | member`
- SoT：`library_membership`（每条记录属于一个 `library_id`，将 `user_id` 映射到角色集合）
- 约束：每个 `library_id` 必须至少有一个 `owner`

### P0-C1-S2（错误语义 v2）

- 未认证：401
- 非 member 访问 tenant 内资源：默认 404（避免泄露存在性）；若选择 403，则必须全局一致并记录审计 reason
- member 执行 admin 动作：403（reason=`not_admin`）

### P0-C1-S3（审计口径 v2）

- 新增/统一 action 命名（示例）：
  - `membership.grant` / `membership.revoke`
  - `library.admin_action.<x>`（实际以具体路由动作命名）
- result：`success | denied | not_found | error`
- reason（白名单示例）：`not_member | not_admin | not_owner | tenant_mismatch`

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5A-2A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（Membership + Roles）

- P1-S1：新增 membership 表/ORM + 最小 repo（按 `library_id` 查询 user roles）
- P1-S2：AuthContext 注入 roles（从 membership 加载；dev fallback 可关闭）

### P2（Policy 扩展）

- P2-S1：新增 1 个明确 admin 动作，并落地 policy.check（例：成员管理 / 书架管理动作之一）
- P2-S2：为 1 条写链路补齐 “member vs admin/owner” 的拒绝路径 + reason

### P3（Audit + Drills）

- P3-S1：为 membership 变更与 admin 动作补齐审计写入点（success/denied）
- P3-S2：新增 drills 脚本（至少 3 scenario）并输出 artifacts 到 `artifacts/_tmp_s5a1a_p3c2sX/`（命名以执行时确定）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：roles 模型与来源（membership SoT + 约束）
- [x] `P0-C1-S2`：错误语义 v2（非 member、非 admin）
- [x] `P0-C1-S3`：审计口径 v2（action/result/reason taxonomy）

### P1（Membership + Roles）

- [x] `P1-C1-S1`：membership 表/ORM/repo
- [x] `P1-C1-S2`：AuthContext.roles 从 membership 注入（fallback 可控）

### P2（Policy）

- [x] `P2-C1-S1`：admin 动作落地（policy + handler）
- [x] `P2-C1-S2`：关键写链路补齐角色拒绝路径（403 + reason）

### P3（Audit + Drills）

- [ ] `P3-C1-S1`：membership/admin 动作的 audit 记录点
- [ ] `P3-C1-S2`：drills/evidence（至少 3 个 scenario + artifacts）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径。
- 代码落地点（P1）：
  - migration：`backend/infra/database/migrations/versions/9f2c7d1a4b63_add_library_memberships.py`
  - ORM：`backend/infra/database/models/library_membership_models.py`
  - repo：`backend/infra/storage/library_membership_repository_impl.py`
  - roles 注入：`backend/api/app/config/security.py:get_auth_context`

- 代码落地点（P2）：
  - policy：admin-only create：`backend/api/app/policy/bookshelf_policy.py:assert_actor_can_create_bookshelf`
  - handler：`backend/api/app/modules/bookshelf/routers/bookshelf_router.py:create_bookshelf`（member → 403 + reason=`not_admin`）
