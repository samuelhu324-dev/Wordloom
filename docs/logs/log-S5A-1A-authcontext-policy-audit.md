# log-S5A-1A-authcontext-policy-audit（Phase 1：AuthContext + tenant boundary + policy + audit v1）

---

**id**: `S5A-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `security skeleton v1 (JWT, library tenant, AuthContext, policy, audit, drills)`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Auth, Authorization, Policy, Audit, Drills, epic/s5, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5A-security-governance-skeleton.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # low-cardinality reasons + evidence discipline
  **reference_log_2**: `docs/logs/log-S2C-projection-framework-platformization.md` # platformization + drills/evidence
**created**: `2026-03-02`
**updated**: `2026-03-02`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片交付 `S5A Phase 1`：把安全/多租户/审计的最小骨架落为可复用契约：
  - 统一请求上下文：`AuthContext`（`user_id`, `tenant_id`, `roles`, `request_id`）。
  - 强制 tenant 边界（默认所有资源带 `library_id`，查询必须按 tenant 过滤）。
  - 授权规则收口到 policy 层（集中表达，避免散落 if-else）。
  - 审计采用 append-only 表先闭环（deny/allow/关键写入成功）。

## Constraints（约束）

- **默认值优先**：先选一个默认并写入 contract，后续所有代码与 drills 以此为基线。
- **最少坑优先**：不引入复杂授权 DSL/OPA；不一开始上 RLS；roles 先最小化。
- **审计先闭环**：append-only、结构化字段、可按 `request_id` 追溯；后续再考虑 outbox/export。
- **reason 低基数**：deny / error 的 reason 必须低基数可聚合。

## Scope（本 log 范围）

- `P0`：contract（默认决策 + 接口 + 错误语义 + 审计字段）
- `P1`：`AuthContext`（统一注入 + request_id 贯穿）
- `P2`：tenant 边界强制 + policy 层骨架
- `P3`：audit append-only 最小闭环 + drills/evidence

## Success Criteria（DoD）

- 代码层面：
  - 能从请求中解析 JWT 并生成 `AuthContext`；非法 token 一致返回 401（dev 环境允许缺失 token 时用 `DEV_USER_ID` 回退）。
  - 所有资源 load 默认带 tenant filter；越权读不得泄露存在性（默认 404）。
  - 授权规则从 handler/service 中移除为 policy 层集中表达（最少 1 条关键链路落地）。
  - audit_log 为 append-only SoT：deny/allow 与关键写入成功会写入审计，并携带 `request_id`。

- 证据层面：
  - 至少 3 个 drills 并产出 artifacts：
    - tenant 越权读（A 不能读 B 的资源）
    - role 不足写（member 不能做 admin 动作）
    - 审计完整性（一次成功写操作必须产生 audit success）

## P0（Contract｜v1）

### P0-C1-S1（决定题｜默认值 v1）

本节目标：选一个默认值并写入 contract，避免后续工程“边做边改”。

**Q1 认证载体与 roles 来源**

- 默认：**JWT Bearer token**。
- claims：必须包含 `user_id`。
- roles：v1 允许最小化（可先空/只做 owner）；角色/成员关系细节优先放 DB policy 里演进。

**Q2 多租户 tenant 模型**

- 默认：`library_id` 即 `tenant_id`。
- 解释：未来若引入 workspace/org，可让 workspace 映射到 library 或 library 归属 workspace，但“所有资源访问必须带 tenant 边界”先锁死。

### P0-C1-S2（最小 contract｜接口 + 错误语义 + 审计口径 v1）

#### 1) `AuthContext` contract（统一请求上下文）

- 字段：
  - `user_id: UUID`
  - `tenant_id: UUID`（v1 等同 `library_id`）
  - `roles: tuple[str, ...]`（v1 最小化，允许为空）
  - `request_id: str`（每个请求必须存在，回传在响应头 `X-Request-Id`）
- tenant 选择：v1 使用请求头 `X-Library-Id`（兼容 `X-Tenant-Id`）作为 `tenant_id`。

#### 2) Tenant boundary contract（强制 tenant 边界）

- 默认所有资源表包含 `library_id`（tenant id）。
- 所有查询/写入必须带 tenant filter：`WHERE library_id = :tenant_id`。
- 例外（全局资源）必须显式设计与标注，默认禁止。

#### 3) Authorization contract（Policy 层收口）

- 授权规则集中在 policy 层：每个动作一个函数（或同等结构）。
  - 例：`can_read_book(ctx, book)`、`can_write_book(ctx, book)`、`can_admin_library(ctx, library)`。
- handler/service 只做两件事：
  - load resource（带 tenant filter）
  - `policy.check(...)`（不通过就拒绝）

#### 4) Error semantics contract（错误语义）

- 未认证：401。
- 越权读（避免信息泄露）：默认 404（或统一为 403，但必须全局一致）。
- 越权写/角色不足：403。

#### 5) Audit contract（append-only 最小闭环）

- 建表：`audit_log`（append-only：只 INSERT，不 UPDATE/DELETE）。
- 最小字段：
  - `occurred_at`
  - `tenant_id`
  - `actor_user_id`
  - `action`
  - `resource_type`, `resource_id`
  - `result`（success/denied/error）
  - `request_id`
  - `meta_json`（可选）
- 记录点：
  - policy deny / allow
  - 关键写操作成功（v1 先覆盖 1 条写链路）

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5A-1A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（AuthContext）

- P1-S1：JWT 解析 + `request_id` 生成/贯穿（middleware/dependency）
- P1-S2：把 service/handler 的调用签名统一为接收 `AuthContext`

### P2（Tenant + Policy）

- P2-S1：为 1 条关键链路落地 tenant filter（Library→Bookshelf→Book）
- P2-S2：新增 policy 层骨架与 `policy.check(...)` 入口

### P3（Audit + Drills）

- P3-S1：新增 `audit_log` 表与最小写入 API
- P3-S2：新增 3 个 drills scenario + evidence（tenant 越权读 / role 不足写 / 审计完整性）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：默认值（JWT + library_id tenant）
- [x] `P0-C1-S2`：最小 contract（接口/错误语义/审计口径）

### P1（AuthContext）

- [x] `P1-C1-S1`：实现 AuthContext 注入（JWT + request_id）
- [x] `P1-C1-S2`：调用点统一改造（service/handler 入口收口；先迁移 1 条链路作为样板）

### P2（Tenant + Policy）

- [x] `P2-C1-S1`：tenant filter 强制落地（关键链路）
- [ ] `P2-C1-S2`：policy 层收口（最少 1 条动作）

### P3（Audit + Drills）

- [ ] `P3-C1-S1`：audit_log append-only 最小闭环
- [ ] `P3-C1-S2`：drills/evidence（至少 3 个 scenario + artifacts）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL（如有）+ 关键参数。
- 本切片完成后，在此追加 drills/evidence 记录。
