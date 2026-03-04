# log-S5A-security-governance（S5A：安全与治理 Epic 路线）

---

**id**: `S5A-security-governance`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `security & governance (AuthContext, tenant boundary, policy, audit, drills, membership/roles)`
**status**: `stable`          # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Auth, Authorization, Policy, Audit, Drills, epic/s5, epic/s5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/ROADMAP.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # low-cardinality reasons + evidence habits baseline
  **reference_log_2**: `docs/logs/log-S2C-projection-framework-platformization.md` # platformization + drills/evidence baseline
  **phase_log_1**: `docs/logs/log-S5A-1A-authcontext-policy-audit.md`
  **phase_log_2**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
  **phase_log_3**: `docs/logs/log-S5A-3A-backup-sanitization.md`
  **phase_log_4**: `docs/logs/log-S5A-3B-object-storage-backup.md`
**created**: `2026-03-02`
**updated**: `2026-03-04`

---

## Decision / Outcome（结论区）

**Decision**:

- 启动 `S5A` 作为 `S5` 下的 security/governance **epic 路线**：把认证、多租户、授权、审计从“散落 if-else”升级为“统一骨架”，并用 drills/evidence 固化可验证性。
- 默认基线（后续全部切片沿用，除非显式升级 contract）：
  - 认证载体：JWT Bearer token。
  - tenant 模型：`library_id` 作为 tenant（`tenant_id == library_id`）。

## Constraints（约束）

- 先收口契约与边界，再做工程化落地；避免一开始引入复杂 DSL/OPA 或全库 RLS。
- roles 先最小化再演进：从 owner-only（或空 roles）过渡到 membership/roles SoT。
- 审计先做 append-only 最小闭环（只插入不更新/不删除），后续再考虑 outbox/export。
- 统一低基数 reason taxonomy（deny/error reasons 可聚合；禁止高基数写入 metrics labels）。

## Scope（本 log 范围）

- 本 log 负责定义 `S5A epic` 的目标边界、默认基线与 phase 拆分；每个 phase 的实现与证据落在对应子 log。

## Success Criteria（DoD）

- 代码层面：
  - 请求进入 handler/service 前能得到统一 `AuthContext`（含 `request_id`）。
  - 所有资源访问默认强制 tenant 边界（`WHERE library_id = :tenant_id`）；例外必须显式设计。
  - 授权规则集中在 policy 层，避免散落 if-else。
  - audit_log 作为 append-only SoT，能按 `request_id` 追溯操作。

- 证据层面：
  - 每个 phase 至少包含可运行 drills，并产出 artifacts（JSON），在子 log 里记录路径与关键参数。

## Phases（切片）

- `S5A-1A`（Phase 1）：AuthContext + tenant boundary + policy + audit v1（含 drills/evidence）
  - 详见：`docs/logs/log-S5A-1A-authcontext-policy-audit.md`
- `S5A-2A`（Phase 2）：Library membership + roles（RBAC-lite）+ policy 扩展 + audit v2 + drills/evidence
  - 详见：`docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
- `S5A-3A`（Phase 3）：dev/test 可恢复备份 + 恢复演练 + 脱敏（sanitization）v1
  - 详见：`docs/logs/log-S5A-3A-backup-sanitization.md`
- `S5A-3B`（Phase 4）：对象存储化备份（MinIO/S3）+ 生命周期 + drills/evidence v1
  - 详见：`docs/logs/log-S5A-3B-object-storage-backup.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：contract（JWT + library tenant + request_id + error semantics）
- [x] `P1`：AuthContext（统一注入 + 贯穿 request_id）
- [x] `P2`：tenant boundary + policy layer（收口授权规则）
- [x] `P3`：audit append-only + drills/evidence（固化）

## Current Status（进展摘要）

- `S5A-1A` 与 `S5A-2A` 已形成可运行的安全/多租户/审计统一骨架，并以 drills + artifacts 固化证据链。
- `S5A-2A` 已推进到 `P3-C4`：将读路径“non-member/tenant_mismatch → 404 + audit not_found(reason)”扩展到 Book 关键读接口（`book.list` / `book.get`），并产出 artifacts 证据（详见 phase log）。
- `S5A-3B` 已补齐单命令 pipeline drill（backup → upload → restore+verify → sanitize+verify），形成可重复的端到端证据链。

## Notes（落地原则）

- 默认 404 优先于 403（用于越权读场景，减少信息泄露）；但需要统一口径并产出审计。
- audit 记录点优先：policy deny / allow + 关键写操作成功（最小闭环）。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：S5A epic 的 phase 拆分、默认 contract 与证据口径已稳定；具体实现与 evidence 以各 phase log 为准。
- 端到端入口（备份/恢复/脱敏 + 对象存储化）：
  - 见 phase log：`docs/logs/log-S5A-3B-object-storage-backup.md`
  - 单命令 drill：`python scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`
