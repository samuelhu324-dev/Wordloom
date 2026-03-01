# log-S2C-4A-projection-drills-template（Projection Drills Template｜最小 drills 套餐模板化）

---

**id**: `S2C-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection drills template (minimal kit: verify/readiness/dual*/failures)`
**status**: `stable`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Drills, Catalog, Runner, epic/s2, sub/4`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **previous_log**: `docs/logs/log-S2C-3A-projection-rebuild-backfill-template.md`
  **reference_log_1**: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
  **reference_log_2**: `docs/logs/log-S2B-3A-unified-consumer-framework.md`
**created**: `2026-03-01`
**updated**: `2026-03-01`

---

## Decision / Outcome（结论区）

**Decision（本切片要交付什么）**:

- 把“新增一条 projection 时必须配套的 drills 套餐”模板化，形成可复制、可审计、可在 Actions 跑的最小标准。
- 将 drills 的 **catalog 约定**（tags/requirements/outputs）固化，使 reusable runner 能可靠地起依赖（db/es/jaeger）并打包 evidence。

**Why now**:

- `S2C-3A` 已打通最小的 catalog-driven 入口（workflow_dispatch + reusable runner）与 rebuild smoke 样例；但“新增 projection 的完整 drills 套餐”仍靠人工拼装。

## Constraints（约束）

- 不改变 artifacts contract：`_result.json` / snapshot bundle 仍是 SoT。
- 不破坏既有 stable workflows / scripts：如需迁移，优先 shim。
- 不把高基数字段（run_id/worker_id 等）写入 metrics label；这些只进入日志/artifacts。

## Scope（本 log 范围）

- `P0`：Drills Template contract（最小必备场景集合、requirements、输出口径）
- `P1`：Catalog 规则模板化（tags/requirements/outputs 的结构约定；guardrails 规则补齐）
- `P2`：Runner 依赖启动模板化（按 requirements 自动启动 db/es/jaeger；本地与 Actions 一致）
- `P3`：Evidence（至少 1 次 Actions run URL 级证据 + artifacts）

## Success Criteria（DoD）

- 新增一条 projection 时：能直接复制/引用同一套 drills 套餐（verify/readiness/dual_write/dual_run/failures），不需要手写脚本拼装依赖。
- 对每个场景：catalog 里能声明 requirements，runner 按声明自动起依赖并把 evidence 打包。
- 证据：至少 1 条来自 GitHub Actions 的 run URL，并能定位到对应 snapshot bundle。

## P0（Drills template contract｜v1）

> 目标：把 drills 从“能跑就行”升级为“新增 projection 的标准交付件”。

- 最小 drills 套餐（v1）：
  - `verify`：DB-only 或 DB+依赖的最小验证（产出 `_result.json`）
  - `readiness`：依赖就绪性/连通性（用于排障与基线确认）
  - `dual_write`：双写一致性验证（如适用）
  - `dual_run`：双跑一致性验证（如适用）
  - `failures`：故障注入/回放（如适用）

- Catalog 约定（v1，对齐现有 schema）：
  - 每个 scenario 必须声明：`id/cli/requires/defaults/tags`（`aliases` 可选）
  - `requires`（布尔映射，低基数）：`db/es/jaeger/worker`
  - `tags`（最小三元组）：必须包含 `intent:*`、`pipeline:*`、`runtime:*`
  - evidence 输出：必须产出 `_result.json` 或 snapshot bundle（artifacts 为 SoT）

## Plan（draft）

### P0（Contract）

- P0-C1-S1：定义 drills template v1（最小场景集合 + requirements + output 口径）

### P1（Catalog template + guardrails）

- P1-C1-S1：在 catalog 增加模板化字段约定（tags/requirements/outdir）并更新 guardrails 校验

### P2（Runner auto-deps）

- P2-C1-S1：reusable runner 根据 requirements 自动起依赖（本地/Actions 一致）

### P3（Evidence）

- P3-C1-S1：在 Actions 触发至少 1 次 scenario，记录 run URL + snapshot bundle

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 drills template v1（最小场景集合 + requirements + output 口径）

### P1（Catalog template + guardrails）

- [x] `P1-C1-S1`：catalog 字段约定模板化 + guardrails 覆盖

### P2（Runner auto-deps）

- [x] `P2-C1-S1`：reusable runner 按 requirements 自动起依赖

### P3（Evidence）

- [x] `P3-C1-S1`：Actions run URL 级证据入账

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL + 关键参数。

### P3-C1-S1（Actions｜drill-labs-scenario｜verify/chronicle/rebuild_entries_smoke）

- headSha: `a877ceafaa21b004612bf4b7a2007c9662582927`
- run_url: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22539384221`
- workflow: `drill-labs-scenario` (workflow_dispatch)
- scenario_id: `verify/chronicle/rebuild_entries_smoke` (db-only)
- artifact: `labs-evidence-verify_chronicle_rebuild_entries_smoke-22539384221-1`
