# Log-S0C-3A-1A: shim/double-parallel

---

**id**: `S0C-3A-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `tools/cli breakdown`
**status**: `draft`          # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLOTION, Docs, Projection, Search, chronicle, lab, sub/1`
**links**: ``
  **issue**: `#83, #66`
  **pr**: `null`
  **adr**: ``
  **runbook**: `null`
**created**: `2026-02-20`
**updated**: `2026-02-21`

---

## Decision / Outcome（结论区）

- 截图1选择：本阶段采用 **shim / double-parallel（双轨）** 拆解策略。
  - 保留现有 argparse 子命令与对外行为（命令路径、参数名、help、exit code、产物落盘规则）不变。
  - 将每个旧实现逐步改为“薄 shim”：把 `args` 映射为 `DrillInputs`，再调用 `cli_app.registry` 中注册的 scenario handler。
- Trade-off（取舍）：
  - **优点（为什么选 shim）**：变更面最小、可逐场景迁移、可随时回滚、可做输出一致性对比；对 GitHub Actions / 本地脚本的扰动最低。
  - **缺点（要付出的代价）**：迁移期间会同时存在“旧 parser + 新 handler”两套结构，短期内代码会有重复路由层；最终仍需收口清理旧 `_cmd_*`。
  - **不选“直接统一分发”的原因**：一次性改动更大，容易在 CLI help/参数兼容/默认值/边界分支上出回归，且回归定位更难。

## Background

- `backend/scripts/cli.py` 体积过大（8k+ 行）会导致工具侧上下文膨胀与交互不稳定。
- 目前已具备：`backend/scripts/cli_app/` 的骨架（`registry/types/common/scenarios`）以及入口侧“新分发短路”能力。
- 拆解目标不是“重写 CLI”，而是 **在不破坏对外契约的前提下逐步减体积**。

## Problem / Constraints（问题与约束）

- 不可破坏契约（CI 与 runbook 依赖）：
  - 子命令路径与参数名不变（包括 `--help` 输出的关键结构）。
  - exit code 语义不变（成功/失败的返回码）。
  - Evidence Bundle/产物 contract 不变（如 `_result.json`、失败时 zip、以及 CI artifacts 依赖的落盘规则）。
- 迁移需要可分批交付：每搬一个 scenario 就能验收，不要求“大爆破式”合并。

## Approach（落地方式）

### Step 0：建立“金丝雀基线”

- 固化至少两类基线：
  - `--help` 输出（用于确认子命令结构与参数未变）。
  - 典型 scenario 跑一遍，保留 `_result.json` 的结构基线（字段名/类型/`ok`/错误结构）。
- 规则：允许新增字段；不允许删字段或改名（除非同步更新所有依赖方）。

### Step A：先抽离 artifacts contract（入口立刻瘦身）

- 将以下通用能力集中到 `cli_app/common.py`：
  - outdir 计算（按 `scope_id/scenario/run_id` 或约定结构）
  - 写 `_result.json` / `summary.json`
  - traces/logs 文件位置约定
  - failure 时打包 zip（CI artifacts 使用）
- 入口侧改法：把 `cli.py` 内零散的写盘/打包逻辑替换为 `common.write_json(...)`、`common.zip_directory(...)` 一类调用。

### Step B：逐个 scenario 迁移（核心：旧实现变 shim）

- 每迁移一个 scenario 的固定动作：
  - 在 `backend/scripts/cli_app/scenarios/<scenario>.py` 定义 `@register("<scenario>")` 的 handler
  - handler 入参用 `DrillInputs`（pydantic 入口层，允许 `extra` 透传 workflow/cli 额外字段）
  - handler 产出统一 `DrillResult`（或等价结构）
  - 在 `registry.load_builtin_scenarios()` 增加 import（触发注册）
  - 将 `cli.py` 中对应 `_cmd_labs_*` 的函数体替换为 shim：
    - `inputs = DrillInputs.model_validate(vars(args) + 必要字段补全)`
    - `handler = registry.get(inputs.scenario)`
    - 统一写 evidence + 返回 exit code

### Step C：完成迁移后收口入口壳

- 当主要场景迁完：
  - `cli.py` 只保留 parser + dispatch + 统一 artifacts 写盘
  - 删除或迁移旧 `_cmd_*`（可移到 legacy 目录）

## Migration Order（迁移优先级）

- 优先迁移 write-gate workflow 的核心路径（高频、回归可见）：
  - `shadow_verify_search_index_write_gate`
  - `shadow_verify_search_index_paging_stability`
  - `shadow_verify_shared_keys`
- 后续再迁移：readiness gate / dual-run stages / window / canary / sampling 等。

## Verification（验证方式）

- 每迁移一个 scenario：
  - 跑一次对应子命令的 `--help`（确认参数未变）
  - 跑一次 scenario（在可用环境变量/数据库连接下）
  - 对比 `_result.json` 的结构与关键字段（至少 `ok`、错误结构、summary/meta 的关键字段）

## Evidence（本阶段实证 / 运行证据）

> 目的：证明 shim/double-parallel 在 CI/本地执行中 **不破坏对外契约**（scenario 名、`_result.json`/summary 结构、ok 语义），并形成可回溯证据链。

### Run 1 — shared_keys（OK）

- artifact: `summary.json`
- scenario: `shadow_verify_shared_keys`
- run_id: `22250360145-1`
- result: `ok=true`
- 关键输出（节选）：
  - `ensure_min_rows=5`
  - `seed_rows_inserted=5`
  - 含 observability 互证字段：
    - `log_probe_emitted=true`
    - `trace_probe.traces_json_written=true`

### Run 2 — write_gate（OK）

- artifact: `summary.json`
- scenario: `shadow_verify_search_index_write_gate`
- run_id: `22250355123-1`
- result: `ok=true`
- 关键输出（节选）：
  - `duplicates_groups_total=0`
  - `duplicates_extra_rows_total=0`

### Run 3 — paging_stability（OK）

- artifact: `summary.json`
- scenario: `shadow_verify_search_index_paging_stability`
- run_id: `22250357446-1`
- result: `ok=true`
- 关键输出（节选）：
  - `rows_total=120`
  - `page_size=50`, `pages_checked=2`, `pages_returned=2`
  - `ordering_ok=true`, `duplicates_across_pages_total=0`

### Run 4 — readiness_gate（OK, 聚合验证）

- artifact: `summary.json`（来自 zip 内）
- scenario: `shadow_verify_dual_run_readiness_gate`
- run_id: `22250386470-1`
- result: `ok=true`
- 关键输出（节选）：
  - `dry_run=true`
  - `checks.write_gate.ok=true`，并引用子检查结果路径：
    - `.drill_snapshot/_checks/shadow_verify_search_index_write_gate/_result.json`
  - `checks.paging_stability.ok=true`：
    - `.drill_snapshot/_checks/shadow_verify_search_index_paging_stability/_result.json`
  - `checks.shared_keys.ok=true`：
    - `.drill_snapshot/_checks/shadow_verify_shared_keys/_result.json`

### Run 5 — dual_run_stage1（OK, Actions 通过）

- artifact: `summary.json`
- scenario: `shadow_verify_dual_run_stage1`
- run_id: `22255317033-1`
- result: `ok=true`
- 关键输出（节选）:
  - `strategy=strict`
  - `ensure_min_rows=25`, `seed_rows_inserted=25`
  - `candidate_limit=20`
  - `es_health_ok=true`, `backfill_ok=true`, `es_search_ok=true`
  - `parity_ok=true`

### Run 6 — readiness_gate（OK, shim→scenario 后复跑）

- artifact: `summary.json`
- scenario: `shadow_verify_dual_run_readiness_gate`
- run_id: `22255455516-1`
- result: `ok=true`
- 关键输出（节选）:
  - `checks.write_gate.ok=true`（引用子检查结果路径）
  - `checks.paging_stability.ok=true`
  - `checks.shared_keys.ok=true`

### Run 7 — dual_run_stage2（OK, 写侧 outbox worker 验证）

- artifact: `summary.json`
- scenario: `shadow_verify_dual_run_stage2`
- run_id: `22255653342-1`
- result: `ok=true`
- 关键输出（节选）:
  - `strategy=strict`
  - `ensure_min_rows=25`, `seed_rows_inserted=25`
  - `candidate_limit=20`
  - outbox：`enqueued_total=20`, `done=20`, `failed=0`
  - worker：`ok=true`, `exit_code=0`, `runtime_seconds≈1.62`
  - ES：`health_ok=true`, `index_ok=true`, `refresh_ok=true`, `search_ok=true`
  - `parity_ok=true`

### Run 8 — dual_run_window（OK, window drill 端到端验证）

- artifact: `summary.json`
- scenario: `shadow_verify_dual_run_window`
- run_id: `22256492131-1`
- result: `ok=true`
- 关键输出（节选）:
  - `strategy=strict`
  - `ensure_min_rows=25`, `seed_rows_inserted=25`
  - window：`enqueued_total=75`
  - worker：`ok=true`, `exit_code=0`, `runtime_seconds≈15.29`
  - ES：`health.ok=true`, `index.ok=true`, `refresh.ok=true`
  - compare：`parity_ok=true`

### Run 9 — canary_dual_write（OK, canary 小流量双写 + 回滚验证）

- artifact: `summary.json`
- scenario: `shadow_verify_canary_dual_write`
- run_id: `22257277206-1`
- result: `ok=true`
- 关键输出（节选）:
  - canary：`max_writes=5`
  - verify：`search_index_rows_found=5`, `search_outbox_rows_found=5`, `duplicates_extra_rows_total=0`
  - rollback：`cleanup_enabled=true`, `deleted_search_index=5`, `deleted_search_outbox_events=5`
  - rollback：`remaining_search_index=0`, `remaining_search_outbox_events=0`

## Status Update（阶段结论）

- Step B（迁移优先级前三个场景 + readiness gate 复合验证）已通过实证：`Run 1~4` 均 `ok=true`。
- dual-run（stage1）已迁移并在 GitHub Actions 中跑通：`Run 5` 为 `ok=true`（strict 对齐）。
- readiness gate 已完成 “shim → scenario” 转接并复跑通过：`Run 6` 为 `ok=true`。
- dual-run（stage2）已迁移并通过写侧 outbox worker 实证：`Run 7` 为 `ok=true`（strict 对齐）。
- dual-run（window）已迁移并通过 window drill 端到端实证：`Run 8` 为 `ok=true`（strict 对齐）。
- canary dual-write 已迁移并通过 canary + 回滚实证：`Run 9` 为 `ok=true`。


## Risks（风险与缓解）

- 风险：shim 映射时遗漏参数、默认值变化、help 文案/参数顺序变化。
  - 缓解：对每个 scenario 固化基线（help + 运行结果），shim 仅做字段映射与调用，不新增业务逻辑。
- 风险：迁移期间双轨并存导致“路由链路”变复杂。
  - 缓解：明确约束：只允许在 `_cmd_*` 内做 shim；核心逻辑只存在于 `cli_app/scenarios/*`。

## Next

- 先做 Step A：把写盘/打包等 artifacts contract 全量收敛到 `cli_app/common.py` 调用点。
- 然后按优先级迁移前三个 scenario，并把对应旧实现改为 shim。
- 等迁移覆盖率足够后，再推进 Step C 收口，最终把 `cli.py` 控制在 100~300 行量级。