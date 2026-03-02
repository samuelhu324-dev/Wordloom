# log-S5A-security-governance-skeleton（路线 C：安全/多租户/审计“统一骨架”）

---

**id**: `S5A-security-governance-skeleton`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `security & governance skeleton (AuthContext, tenant boundary, policy, audit, drills)`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Auth, Authorization, Policy, Audit, epic/s5, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/ROADMAP.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # low-cardinality reasons + evidence habits baseline
  **reference_log_2**: `docs/logs/log-S2C-projection-framework-platformization.md` # platformization + drills/evidence baseline
  **child_log_1**: `docs/logs/log-S5A-1A-authcontext-policy-audit.md`
  **child_log_2**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
**created**: `2026-03-02`
**updated**: `2026-03-02`

---

## Decision / Outcome（结论区）

**Decision**:

- 启动 `S5 Route C`：把安全/多租户/审计从“散落 if-else”升级为“统一骨架”，并用 drills/evidence 固化。
- 默认选择（作为后续全部工程实现的基线）：
  - 认证载体：JWT Bearer token。
  - tenant 模型：`library_id` 作为 tenant（`tenant_id == library_id`）。

## Constraints（约束）

- 先收口契约与边界，再做工程化落地；避免一开始引入复杂 DSL/OPA 或全库 RLS。
- roles 先最小化（允许先只做 owner / member，或先只做 owner），规则细节放在 DB + policy 层逐步演进。
- 审计先做 append-only 最小闭环（只插入不更新/不删除），后续再考虑 outbox/export。
- 统一低基数 reason taxonomy（deny/error reasons 可聚合；禁止高基数写入 metrics labels）。

## Scope（本 log 范围）

- `P0`：contract（JWT + library tenant + error semantics + request_id）
- `P1`：统一请求上下文 `AuthContext`
- `P2`：tenant 边界强制 + policy 层收口（集中表达授权规则）
- `P3`：审计 append-only 最小闭环 + drills/evidence 固化

## Success Criteria（DoD）

- 代码层面：
  - 请求进入 service/handler 前能得到统一 `AuthContext`（含 `request_id`）。
  - 所有资源访问默认强制 tenant 边界（`WHERE library_id = :tenant_id`）；例外必须显式设计。
  - 授权规则集中在 policy 层，避免散落 if-else。
  - audit_log 作为 append-only SoT，能按 `request_id` 追溯操作。

- 证据层面：
  - 至少 3 个 drills：tenant 越权读、role 不足写、审计完整性。
  - 每个 drills 产出可审计 artifacts（`_result.json`），并记录到子 log。

## Plan（draft）

- P0：定义 contract（见 `S5A-1A`）
- P1：实现 `AuthContext` 注入（middleware/dependency）
- P2：实现 policy 层骨架 + 典型资源链路（Library→Bookshelf→Book）迁移
- P3：实现 audit_log + 最小 drills/evidence

## Execution Checklist（unchecked）

- [x] P0：contract（JWT + library tenant + request_id + error semantics）
- [x] P1：AuthContext（统一注入 + 贯穿 request_id）
- [x] P2：tenant boundary + policy layer（收口授权规则）
- [x] P3：audit append-only + drills/evidence（固化）

## Notes（落地原则）

- 默认 404 优先于 403（用于越权读场景，减少信息泄露）；但需要统一口径并产出审计 denied。
- audit 记录点优先：policy deny / allow + 关键写操作成功（最小闭环）。
