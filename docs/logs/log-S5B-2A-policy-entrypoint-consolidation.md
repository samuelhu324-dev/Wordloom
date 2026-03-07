# log-S5B-2A-policy-entrypoint-consolidation（Phase 2：Policy entrypoint consolidation v1）

---

**id**: `S5B-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `policy entrypoint consolidation (owner checks → policy + tenant filter) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S5`
**tags**: `EVOLUTION, Security, Governance, MultiTenant, Authorization, Policy, Audit, Drills, Evidence, HardGate, epic/s5, epic/s5b, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **previous_log**: `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  **reference_log_1**: `docs/logs/log-S5A-1A-authcontext-policy-audit.md`
  **reference_log_2**: `docs/logs/log-S5A-2A-library-membership-roles-policy-audit.md`
  **reference_log_3**: `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
**created**: `2026-03-07`
**updated**: `2026-03-07`

---

## Decision / Outcome（结论区）

**Decision**:

- 选 1 条关键链路，把分散在 router/usecase/service 中的 owner check / tenant 过滤 / deny reason 统一收口到 policy entrypoint（并保证审计口径不漂移）。
- Phase 2 的交付以“可复跑的 drills/evidence + 统一入口函数”为核心，而不是大范围重构。

**Target chain（v1）**:

- 选择：`bookshelf.delete`
- Canonical audit action：`bookshelf.delete`

**Default choices（本 phase 默认决策 / v1）**:

- 继续沿用 `S5B-1A` 的 contract（deny 语义、audit action/result/reason、evidence artifacts contract）。
- 目标链路优先选已有测试覆盖的资源（bookshelf/book/library 的 get/delete 等），避免引入新模块。

## Definitions（概念定义，可选）

- **Policy entrypoint**：统一授权入口（例如 `policy.authorize_<action>(ctx, resource)`），负责：tenant 边界、角色/owner 判定、deny reason 输出。
- **Tenant filter**：资源加载时必须按 tenant 限定（防止“先 load 再 deny”的越权泄露）。
- **Owner check**：对资源实例的 owner 归属判定（deny reason=`not_owner`）。

## Constraints（约束）

- 禁止在 handler/usecase 里散落 if-else 授权逻辑；必须收口到 policy entrypoint。
- deny reason 必须低基数（白名单），并写入 `audit_log.reason`（不能只放 meta_json）。
- 变更必须能被 drills 验证，并产出可机械判定的 evidence。

## Scope（本 log 范围）

- `P0`：contract（本 phase 的目标链路、action 命名、reason 口径与落点约束）
- `P1`：实现（policy entrypoint + usecase/router 改造到统一入口）
- `P2`：drills（新增/扩展 1 个 scenario，覆盖 owner/tenant 边界的关键动作）
- `P3`：CI hard gate（把新的 scenario 接入现有 hard gate 入口；或显式声明为何不接入）

## Success Criteria（DoD）

- 至少 1 条关键链路完成“入口收口”：
  - 资源加载带 tenant filter（或可证明不会跨 tenant 读到资源）
  - 授权判定经 policy entrypoint
  - deny reason 来自白名单且写入 `audit_log.reason`
- drills 产物满足 artifacts contract，且可在 CI hard gate 重复跑通。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - `P0-P3` 的 contract + 入口函数 + drills 已跑通
  - Evidence 区有可追溯的 `headSha` + artifacts 路径（或 CI run URL）

## P0（Contract｜v1）

### P0-C1-S1（Target chain selection：选择 1 条关键链路）

- 目标：从下列候选里选 1 条作为本 phase 的收口对象，并固定 action 命名：
  - `bookshelf.get/delete/update`
  - `book.get/list/update/delete`
  - `library.get/delete`
- 原则：优先选已有测试覆盖且能稳定复现 owner/tenant deny 的链路。

**Selected（v1）**:

- Chain：`bookshelf.delete`
- Action：`bookshelf.delete`

**Why this chain**:

- 当前 `DELETE /bookshelves/{bookshelf_id}` 缺少 `AuthContext`（tenant / roles / request_id），且没有审计写入，属于“高风险且口径易漂移”的链路。
- `DeleteBookshelfUseCase` 目前对资源加载不做 tenant filter（`get_by_id(bookshelf_id)`），是典型“load 后再判定”的形态，适合作为 Phase 2 的收口样例。
- 该链路天然需要 owner deny（`not_owner`）与 tenant boundary deny（`tenant_mismatch`）两个关键维度，且现有 policy/reason 常量已存在，改造成本可控。

### P0-C1-S2（Authorization & audit：owner/tenant deny 口径）

**bookshelf.delete（v1）**:

- allow：`owner` / `admin`
- deny（not_admin）：`member` → 403 + audit `result=denied` + `reason=not_admin`
- deny（not_member）：无 membership/roles → 403 + audit `result=denied` + `reason=not_member`
- tenant mismatch（write-path）：跨 tenant 访问资源 → 403 + audit `result=denied` + `reason=tenant_mismatch`
- not found：资源自然不存在 → 404 + audit `result=not_found` + `reason=null`

**Audit 约束（沿用 S5B-1A contract）**:

- action：固定为 `bookshelf.delete`
- 当 `result in {denied, not_found}`：reason 必须来自低基数白名单，且写入 `audit_log.reason`（不得只写 meta_json）

### P0-C1-S3（Evidence & artifacts contract）

- 复用 `S5B-1A` 的 artifacts 目录与 `_result.json` schema；新增 case 需遵守 failure_reason taxonomy。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S5B-2A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（实现：policy entrypoint consolidation）

- P1-C1-S1：选定目标链路，定位当前 owner/tenant check 分散点（router/usecase/service）。
- P1-C1-S2：引入/完善 policy entrypoint（返回 decision + reason），并改造目标链路只调用 entrypoint。
- P1-C1-S3：确保 audit reason 落在 `audit_log.reason`，并保持 action/result 口径稳定。

### P2（drills/evidence）

- P2-C1-S1：新增或扩展 1 个 scenario：
  - owner deny（`not_owner`）
  - tenant boundary deny（`tenant_mismatch`）
  - request_id 可回查到 audit_log 行

### P3（hard gate）

- P3-C1-S1：把新增 scenario 接到 hard gate（优先复用 `scripts/drills/s5b1a_p4_hard_gate.py` 的模式）。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：选定目标链路 + action 命名
- [x] `P0-C1-S2`：owner/tenant deny 语义 + audit reason 落点固化
- [ ] `P0-C1-S3`：evidence schema/contract 明确（复用 S5B-1A）

### P1（实现）

- [ ] `P1-C1-S1`：定位分散的 owner/tenant checks
- [ ] `P1-C1-S2`：收口到 policy entrypoint（最小改动）
- [ ] `P1-C1-S3`：审计 action/result/reason 对齐 contract

### P2（drill/verify）

- [ ] `P2-C1-S1`：新增/扩展 drills scenario 并产出 green evidence

### P3（hard gate）

- [ ] `P3-C1-S1`：CI hard gate 接入（或记录不接入原因）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（<scenario>｜YYYY-MM-DD）

- headSha：`<git sha>`
- artifacts：`docs/labs/_snapshot/auto/S5B-2A/<suite>/<run_id>/`
- 期望（expected）：
  - ...
- 观测（observed）：
  - ...

## Recent changes（for traceability，可选）

- 2026-03-07：scaffold Phase 2 log skeleton.
- 2026-03-07：P0-C1-S1 选定 `bookshelf.delete`；启动 P1：delete 引入 tenant scope + audit action/result/reason 基线。
