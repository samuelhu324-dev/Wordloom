# log-S2C-1A-projection-spec-registry-harness（第一个可交付切片：Spec/Registry + Chronicle reference harness）

---

**id**: `S2C-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection spec/registry + worker harness (chronicle reference)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Worker, Chronicle, epic/s2, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # outbox_core baseline
**created**: `2026-02-28`
**updated**: `2026-03-01`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片的目标是把“路线 A 的最小平台化接口”真正落地：
  1) 定义 `ProjectionSpec` + registry（声明式登记投影）
  2) 落一个通用 worker harness 的最小版本（只依赖 outbox_core）
  3) 用 Chronicle 投影做 reference 实现（DB→DB），验证 harness 形态是可用的

**Why Chronicle-first**:

- Chronicle 是 DB→DB（`chronicle_events → chronicle_entries`），依赖更少、外部副作用更可控；更适合作为 harness 的样板。
- 先跑通 Chronicle reference，可以在不引入 ES/HTTPX 复杂度的情况下验证：claim/lease/retry/reclaim/sanitize/mark/metrics 的通用闭环。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。同一切片需要“修复后重跑一轮”时才递增。
- 组合写法：`S1S2`（一次提交覆盖多个步骤）。

**Commit / PR 命名**:

- `S2C-1A/P<phase>-C<cycle>-S<step>: <summary>`

## Constraints（约束）

- 不新增第二套对外入口：
  - 仍以现有 stable 脚本路径作为入口（如 `backend/scripts/chronicle_outbox_worker.py`），必要时通过 shim 指向新实现。
- 不改变 artifacts contract：所有 drills 的证据结构不变。
- 不在本切片中强行统一 Search（DB→ES）：Search 迁移到 harness 作为后续切片（避免一次性引入 ES bulk 的复杂性）。

## Scope（本 log 范围）

- `P0`：Spec/Registry：能枚举投影，且包含最低限度元数据
- `P1`：Harness：通用 outbox worker 主循环（可运行、可观测、可审计）
- `P2`：Chronicle reference：用 harness 跑通 chronicle_events_to_entries，并保持稳定入口不变

## Success Criteria（DoD）

- 代码层面：
  - 能通过 registry 枚举当前投影（至少 Search/Chronicle 两条）
  - harness 能以 `projection_name` 参数启动，并完成：claim → apply → mark_done/mark_retry/mark_failed
  - Chronicle worker 从 legacy 脚本迁移为 harness + adapter（入口仍稳定）

- 证据层面：
  - 最少一轮 `verify/chronicle/entries`（或等价的 Chronicle verify）可跑通并生成 artifacts
  - 若 worker 行为有改动：按 S2B 口径补齐 N≥3 rounds（避免偶发性漂移）

## Plan（draft）

### P0（Spec/Registry）

- P0-S1：定义 `ProjectionSpec`（最小字段：projection_name/scope_keys/requires/payload_schema/apply_entrypoint）
- P0-S2：实现 registry（静态注册或自动发现；先用最简单可读方案）
- P0-S3：把 Search/Chronicle 以“声明式条目”登记进去（不改现有实现）

### P1（Worker Harness）

- P1-S1：实现通用 worker loop（基于 `infra/outbox_core/*`）：
  - claim（按 projection + scope predicates）
  - lease renew
  - apply（投影注入的业务逻辑）
  - mark_done / mark_retry / mark_failed
  - reclaim stuck + sanitize terminal
  - metrics：复用现有 outbox_metrics labels（projection/op/reason）

### P2（Chronicle reference migration）

- P2-S1：抽出 Chronicle 的 apply 逻辑为 adapter（例如 `chronicle_events_to_entries.apply(row)`）
- P2-S2：用 harness 运行 Chronicle 投影（保留 stable entrypoint；必要时 shim）
- P2-S3：跑 drills & 入账 evidence（至少 1 轮；若行为改动则 N≥3）

## Execution Checklist（checked）

### P0（Spec/Registry）

- [x] `P0-C1-S1`：定义 `ProjectionSpec` + 最小字段
-     Impl: `backend/infra/projection_framework/spec.py` (`ProjectionSpec`)
- [x] `P0-C1-S2`：实现 registry，并能列出投影
-     Impl: `backend/infra/projection_framework/registry.py` (`register/get_spec/list_specs`)
- [x] `P0-C1-S3`：登记 Search/Chronicle 为条目（不改行为）
-     Impl: `backend/infra/projection_framework/builtins.py` (`register_builtin_specs`)

### P1（Worker Harness）

- [x] `P1-C1-S1`：实现通用 harness（可运行）
-     Impl: `backend/infra/projection_framework/harness.py` (`run_harness`)
- [x] `P1-C1-S2`：metrics/shared keys 对齐（projection/op/reason；run_id/worker_id）
-     Impl: `backend/infra/projection_framework/harness.py` (outbox_* counters + structured logs)

### P2（Chronicle reference migration）

- [ ] `P2-C1-S1`：Chronicle adapter（events→entries apply）
- [ ] `P2-C1-S2`：Chronicle worker 改为 harness 驱动（stable entrypoint 不变）
- [ ] `P2-C1-S3`：drills 证据入账（至少 1 轮；必要时 N≥3）

## Evidence（证据与 SoT 规则）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL + 关键参数。
- 建议复用 suite：
  - `drill-shadow-verify-entries` | scenario_id: `verify/chronicle/entries`
  - 若 harness 涉及 outbox 行为：补齐 `drill-write-gate` 的最小 6-pack（与 S2B 对齐）

## Notes（实现落点建议，供开工时对齐）

- Spec/Registry 建议落在：`backend/infra/projection_framework/`（或同级目录；以不打扰现有模块为优先）
- harness 建议复用：`backend/infra/outbox_core/*`
- Chronicle apply 逻辑来源：现有 `backend/scripts/legacy/chronicle_outbox_worker.py` 中的 upsert/insert-on-conflict 逻辑（抽成纯函数或类方法）

**Trade-off（记账）**:

- 当前阶段 `apply_entrypoint` 使用 stub（显式 `NotImplementedError("apply_entrypoint not wired yet")`）以最小化改动面、加速推进，并避免“静默 noop”掩盖 wiring 问题。
- 等 harness/adapter 形态稳定、并且需要支持“已注册但暂时禁用”的 spec 时，再把 `apply_entrypoint` 演进为 optional（或引入 `enabled: bool` / `mode: enum` 这类更明确的状态机）。
