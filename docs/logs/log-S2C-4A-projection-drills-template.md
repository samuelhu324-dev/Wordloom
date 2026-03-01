# log-S2C-4A-projection-drills-template（Projection Drills Template｜最小 drills 套餐模板化）

---

**id**: `S2C-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection drills template (minimal kit: verify/readiness/dual*/failures)`
**status**: `draft`           # draft | stable | archived
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

- `P-1`：Baseline（现状盘点：catalog schema / runner 入口 / artifacts contract / guardrails）
- `P0`：Drills Template contract（最小必备场景集合、requirements、输出口径）
- `P1`：Catalog 规则模板化（tags/requirements/outputs 的结构约定；guardrails 规则补齐）
- `P2`：Runner 依赖启动模板化（按 requirements 自动启动 db/es/jaeger；本地与 Actions 一致）
- `P3`：Evidence（至少 1 次 Actions run URL 级证据 + artifacts）

## Success Criteria（DoD）

- 新增一条 projection 时：能直接复制/引用同一套 drills 套餐（verify/readiness/dual_write/dual_run/failures），不需要手写脚本拼装依赖。
- 对每个场景：catalog 里能声明 requirements，runner 按声明自动起依赖并把 evidence 打包。
- 证据：至少 1 条来自 GitHub Actions 的 run URL，并能定位到对应 snapshot bundle。

## P-1（Baseline / Current State｜2026-03-01）

> 目标：先把“我们现在已经有什么”写清楚，避免在 P0/P1/P2 里重复造轮子或写出落不了地的 contract。

- 单一事实源（Scenario catalog）：`docs/labs/scenarios/catalog.yml`
  - schema（当前真实字段）：
    - `id`：canonical（`{intent}/{pipeline}/{topic}` 三段）
    - `aliases`：legacy ids（可选，runner 可解析）
    - `cli`：实际执行命令（runner 从 catalog 解析并执行）
    - `requires`：依赖开关（当前已存在字段：`db/es/jaeger/worker`）
    - `defaults`：参数默认值（可选）
    - `tags`：反向索引（intent/pipeline/runtime/workflow 等）

- 可复用 runner（Actions）：`.github/workflows/reusable-labs-scenario-runner.yml`
  - 输入：`scenario_id/env_file/duration/lookback/keep_last`（workflow_call）
  - 行为：从 catalog 解析 `cli` → 启动 infra（当前实现为 DB + ES + Jaeger 都起）→ migrate → run → upload artifacts
  - 约定：`RUN_ID` 由 Actions run id + attempt + scenario 拼接；artifact name 使用 runner 计算的 safe id（避免 `/` 导致上传失败）

- 手动入口（workflow_dispatch）：`.github/workflows/drill-labs-scenario.yml`
  - 目标：提供一个“只输入 scenario_id 就能跑”的通用入口（不依赖 intent-suites）
  - 说明：如果你在 Actions 左侧列表看不到它，通常是因为它还不在默认分支或 workflow 列表被折叠。

- Guardrails（静态校验）：`backend/scripts/ci/validate_scenario_catalog.py`
  - 目前已覆盖：catalog 基本结构、`id` 格式、`cli` 非空、`id/aliases` 唯一性、workflow 引用完整性、artifact name 安全用法等。

- Operator discovery（查询工具）：`backend/scripts/ci/list_scenarios.py`
  - 用途：按 intent / 关键字查 `scenario_id`（避免 string 输入不知道填什么）

- Artifacts contract（证据）：以 `_result.json` / snapshot bundle 为 SoT（S0C/S2B 体系已建立）。

## P0（Drills template contract｜v1）

> 目标：把 drills 从“能跑就行”升级为“新增 projection 的标准交付件”。

### 最小 drills 套餐（v1）

> 这里的“最小”指：新增 projection 时，必须具备一套可审计的场景入口；但不是所有 projection 都必须实现 dual_* / fault。

- **必做（所有 projection）**
  - `verify/<pipeline>/smoke`：最小正确性验证（DB-only 或按依赖声明），必须产出 `_result.json`
  - `readiness/<pipeline>/connectivity`（或等价 topic）：依赖就绪/连通性 + 最小查询（用于排障与基线确认），必须产出 `_result.json`

- **条件性（按投影迁移阶段/风险选择）**
  - `dual_write/<pipeline>/*`：当存在“旧写/新写并行”或写开关时必须提供
  - `dual_run/<pipeline>/*`：当存在“旧消费/新消费并行”或 worker 路径验证时必须提供
  - `fault/<pipeline>/*`：当投影依赖 ES 或 worker 复杂度较高、且需要证明抗坏/自愈时再提供

### Scenario entry contract（catalog v1）

> 对齐当前仓库真实 schema（见 P-1）。P1/P2 会在此基础上做“模板化 + 自动化”。

- `id`：必须符合 `intent/pipeline/topic` 三段；建议：intent 与 tags 同步（例如 `verify/...` + `intent:verify`）
- `aliases`（可选）：保留 legacy id；一旦对外使用过就不要随意删
- `cli`：必须可直接执行，并尽量支持 runner 注入：
  - 推荐接受：`--database-url "$DATABASE_URL" --run-id "$RUN_ID" --outdir "$OUTDIR"`
  - 如果为了证据固定落盘，也可以把 outdir 固定到 `docs/labs/_snapshot/auto/<scenario>/${RUN_ID}`（但要一致）
- `requires`：必须显式声明（即使当前 runner 暂时“全起”）：
  - `db/es/jaeger/worker` 为 boolean
- `defaults`：可选；用于 runner/workflow 覆写参数的默认值（不要求齐全，但要可审计）
- `tags`：必须至少包含以下三类（用于查询与治理）：
  - `intent:<intent>`（例如 `intent:verify`）
  - `pipeline:<pipeline>`（例如 `pipeline:chronicle`）
  - `runtime:<runtime>`（例如 `runtime:db_only`, `runtime:db_es`, `runtime:db_es_jaeger`）

### Evidence contract（`_result.json` v1）

- 每个最小场景必须输出 `_result.json`（位于 outdir 内），至少包含：
  - `ok: true|false`
  - `scenario_id` 与关键参数摘要（例如 `run_id`, `duration_s`）
  - 关键计数/断言摘要（例如 `rows_checked`, `mismatches`, `errors_count`）

### YAML 模板（复制起步）

```yaml
- id: verify/<pipeline>/smoke
  aliases: []
  cli: >-
    python backend/scripts/labs/<your_runner>.py
    --database-url "$DATABASE_URL"
    --run-id "$RUN_ID"
    --outdir "$OUTDIR"
  requires:
    db: true
    es: false
    jaeger: false
    worker: false
  defaults: {}
  tags:
    - intent:verify
    - pipeline:<pipeline>
    - runtime:db_only
    - s2c:s2c4a
```

## Plan（draft）

### P-1（Baseline）

- P-1-C1-S1：盘点现有 catalog schema / runner 入口 / guardrails / artifacts contract，并在本 log 固化

### P0（Contract）

- P0-C1-S1：定义 drills template v1（最小场景集合 + requirements + output 口径）

### P1（Catalog template + guardrails）

- P1-C1-S1：在 catalog 增加模板化字段约定（tags/requirements/outdir）并更新 guardrails 校验

### P2（Runner auto-deps）

- P2-C1-S1：reusable runner 根据 requirements 自动起依赖（本地/Actions 一致）

### P3（Evidence）

- P3-C1-S1：在 Actions 触发至少 1 次 scenario，记录 run URL + snapshot bundle

## Execution Checklist（unchecked）

### P-1（Baseline）

- [x] `P-1-C1-S1`：固化现状基线（catalog schema / runner 入口 / guardrails / artifacts contract）

### P0（Contract）

- [x] `P0-C1-S1`：定义 drills template v1（最小场景集合 + requirements + output 口径）

### P1（Catalog template + guardrails）

- [ ] `P1-C1-S1`：catalog 字段约定模板化 + guardrails 覆盖

### P2（Runner auto-deps）

- [ ] `P2-C1-S1`：reusable runner 按 requirements 自动起依赖

### P3（Evidence）

- [ ] `P3-C1-S1`：Actions run URL 级证据入账

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL + 关键参数。
