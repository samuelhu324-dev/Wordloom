# Log-S2C: projection framework platformization（路线 A：把 Projection 体系抽象成“可复制框架”）

---

**id**: `S2C-projection-framework-platformization`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection framework platformization (spec/registry/harness/templates)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Worker, epic/s2, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/ROADMAP.md`
  **sibling_log**: `docs/logs/log-S2B-projection-table-merge.md` # Route B outcome that unlocks Route A
  **child_log_1**: `docs/logs/log-S2C-1A-projection-spec-registry-harness.md`
  **child_log_2**: `docs/logs/log-S2C-2A-projection-writer-template.md`
  **child_log_3**: `docs/logs/log-S2C-3A-projection-rebuild-backfill-template.md`
  **child_log_4**: `docs/logs/log-S2C-4A-projection-drills-template.md`
**created**: `2026-02-28`
**updated**: `2026-03-01`

---

## Background

在 `S2B`（路线 B）里我们已经把 outbox/worker 做到了“抗坏 + 自愈”，并形成了可审计的 drills + artifacts contract（证据链）。这使得我们进入路线 A 的前置条件已经具备：

- 有稳定的消费语义模块：`backend/infra/outbox_core/*`（claim/lease/retry/reclaim/replay/mark/payload_contract）
- 有统一 outbox 表与投影 multiplex：`outbox_events(projection=...)`
- 有 drills 的数据驱动入口：`docs/labs/scenarios/catalog.yml` + reusable runners

但当前新增一个 projection 仍然会遇到“需要复制脚本/拼装 worker 主循环/手写 enqueue/rebuild/验证”的工程成本，且容易语义漂移。

路线 A 的目标：把 Projection 从“工程项目”升级为“平台能力”——以后新增投影尽量变成：

- 填一份 `ProjectionSpec`（声明能力/依赖/范围）
- 写一个 `apply()`（业务转换逻辑）
- 复用同一套 harness（claim/lease/retry/metrics/evidence/runbook）

## Decision / Outcome（结论区）

**Decision**:

- 将“Projection 平台化”拆成可独立交付的阶段：
  - Phase 1：Spec/Registry（声明式的投影元数据 + 注册表）
  - Phase 2：Worker Harness（通用 outbox worker 主循环，投影只插入 apply 逻辑）
  - Phase 3：Writer Template（统一 enqueue / trace 注入 / scope keys）
  - Phase 4：Rebuild/Backfill Template（统一 rebuild bookkeeping + metrics + runbook 口径）
  - Phase 5：Drills Template（新增投影时的最小 drills 套餐与 catalog 规则）
  - Phase 6（deferred）：Search harness migration（DB→ES；后续切片单独交付）

**Constraints（硬约束）**:

- 不破坏路线 B 的稳定面：
  - 既有 stable entrypoints（scripts/runbook/workflows）不随意改名；如需迁移，优先做 shim。
  - artifacts contract 保持不变（summary.json / failure zip / `_result.json` 为 SoT）。
- “框架化”不等于“推倒重写”：优先从 Chronicle（DB→DB）这类简单投影抽样落地，验证模板可行，再逐步迁 Search（DB→ES）。

## Success criteria（DoD）

- 新增一个 projection（第 3 条投影）时：
  - 不需要复制整份 worker 脚本；只需新增一个 spec + apply 逻辑。
  - 能用既有 drills 套餐跑出可审计证据（Actions artifacts / 本地 artifacts）。
  - outbox reason taxonomy 与 payload contract 不漂移（仍是低基数可聚合）。

## Execution Checklist（S2C 总清单）

> 说明：这里用 `P0/P1/P2/...` 管 S2C 的大阶段；具体切片与证据在子 log（例如 `S2C-1A`）里持续细化。

### P0（基线与边界：明确平台化的“最小接口”）

- [x] 明确 `ProjectionSpec` 最小字段：projection_name/scope_keys/requires/payload_schema/apply
- [x] 明确“平台负责什么/不负责什么”（Non-goals）：不强行统一业务数据结构；只统一 outbox 语义与运维契约

### P1（Phase 1：Spec/Registry）

- [x] 定义 `ProjectionSpec` 数据结构与注册表入口（能枚举所有投影）
- [x] 把现有两条投影（Search/Chronicle）登记进 registry（先不改行为）

### P2（Phase 2：Worker Harness）

- [x] 实现通用 worker 主循环：claim → apply → mark_done/mark_retry/mark_failed → reclaim/sanitize/metrics
- [x] 选 Chronicle 作为 reference：将其 worker 迁移为 harness + adapter（保留 stable entrypoint）

### P3（Phase 3：Writer Template）

- [x] 统一 outbox enqueue（投影/实体/op/scope/trace 注入）为通用 repo
- [x] 把 Search/Chronicle 写路径切到通用 repo（事务语义不变）

### P4（Phase 4：Rebuild/Backfill Template）

- [x] 提供通用 rebuild runner：投影选择 + ProjectionStatusModel 记账 + metrics
- [ ] 提供通用 backfill runner（如需要）：从 SoT 重建/回填 outbox

### P5（Phase 5：Drills Template）

- [ ] 为“新增投影”定义最小 drills 套餐（verify/readiness/dual_write/dual_run/failures）
- [ ] 在 catalog 增加模板化 tags/requirements，runner 自动起依赖（db/es/jaeger）

### P6（Phase 6：Search harness migration｜deferred）

- [ ] 将 Search（DB→ES）以独立切片迁移到 harness（不与 writer/rebuild/drills 混交付）

## Evidence（证据与 SoT 规则）

- S2C 的 Evidence 复用既有规则：artifacts 为事实源；log 只记录 run URL / 参数 / headSha。
- 每个子 log 至少应记录：
  - pre/post 固定回归包（或最小 verify）
  - 若迁移影响 worker/harness：至少 N≥3 rounds（与 S2B 口径一致）

## Notes（现状摘记：已具备的平台化“素材”）

- outbox runtime：`backend/infra/outbox_core/*`
- unified outbox toggles：`backend/infra/outbox_unified/toggles.py`
- drills catalog + guardrails：`docs/labs/scenarios/catalog.yml` + `backend/scripts/ci/validate_scenario_catalog.py`
- writer 端雏形：Search 有 `SearchOutboxRepository`，Chronicle 写 outbox 目前内联（需要统一）
