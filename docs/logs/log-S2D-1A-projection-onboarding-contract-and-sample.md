# log-S2D-1A-projection-onboarding-contract-and-sample（Phase 1：Projection onboarding contract + first sample）

---

**id**: `S2D-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection onboarding contract + first sample (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S2D`
**tags**: `EVOLUTION, Projection, Onboarding, Drills, Evidence, epic/s2d, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2D-projection-onboarding-hard-gates.md`
  **previous_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_1**: `docs/logs/log-S2C-1A-projection-spec-registry-harness.md`
**created**: `2026-03-08`
**updated**: `2026-03-08`

---

## Decision / Outcome（结论区）

**Decision**:

- 为 Route A 定义一条“新增 projection 的最小 onboarding contract”，并用一条新投影作为示范链路完整走通该 contract（spec + adapter + writer + rebuild/backfill smoke + drills）。
- 在 dev/test 环境中为这条示范投影产出 S2D 口径的 artifacts（S6A-4A JSON contract），并记录可复跑的 scripts/CI 入口，作为后续 S2D hard gate 的基线样板。

**Default choices（本 phase 默认决策 / v1）**:

- 仅选择 1 条代表性的新投影（或对现有简单投影做一次“按模板重建”），避免一次性迁移所有投影；优先选 DB→DB 或简单统计类，降低失败面。
- onboarding contract 先聚焦“最小可运行 + 可验证”：不强行要求复杂 metrics/dashboard，只要 artifacts 和 exit code 能机械判定 PASS/FAIL。
- 第一版只在本地/Actions 手动触发，不强制挂到所有 PR 上；hard gate 的 CI 接入放到后续 S2D-3A 处理。

## Definitions（概念定义）

- **Projection onboarding contract**：新增或迁移 projection 时必须满足的最小工程约束集合，包括 spec 字段、writer 路径、harness 注册、rebuild/backfill smoke 与 drills 覆盖等。
- **Sample projection**：本 phase 选定的一条代表性投影，用于验证 S2D onboarding contract 的可执行性；后续投影应尽量复用其结构与脚本。
- **Smoke drills**：只验证“能跑通”和“不会破坏稳定面”的最小场景，例如单条事件的投影正确性、最小 rebuild 成功与回滚路径。
- **Chronicle daily stats projection（示范投影）**：以 Chronicle outbox 事件为输入，为每个 tenant/日期/事件类型聚合计数与最近发生时间的 DB→DB 统计投影，目标是一张便于运营/报表查询的日级明细表。

## Constraints（约束）

- 不修改 outbox events 的 schema 或 payload contract，仅通过 `ProjectionSpec` 与 harness/adapter 校验来约束写入与消费行为。
- 不改变现有 S2B/S2C stable entrypoints 的语义；如果需要新增脚本，优先采用 `s2d_*` 前缀，并在 runbook 中登记。
- 本 phase 的示范投影需具备可回滚能力：若发现问题，可以通过 disable/spec 标记和 rebuild/backfill 脚本恢复到迁移前状态。

## Scope（本 log 范围）

- `P0`：contract（定义 Projection onboarding contract 的字段/语义/证据口径）。
- `P1`：实现（在现有 S2C 框架上补充 runtime 校验 + 新增示范投影的 spec/adapter/writer）。
- `P2`：drills（为示范投影补充最小 rebuild/backfill smoke + projection correctness drills，并产出 artifacts）。
- `P3`：小范围 hard gate（提供单命令脚本用于本地/CI 手动执行示范投影的 onboarding 套餐，为后续 S2D-3A 的统一 hard gate 做准备）。

## Success Criteria（DoD）

- 有一份明确的 onboarding contract 文档化在本 log：列出新增 projection 必须提供的字段与脚本清单，并可被后续 S2D phase 复用。
- 选定 1 条 sample projection，并在代码中：
  - 新增/完善对应 `ProjectionSpec`，包含 projection_name/scope_keys/requires/payload_schema_version/apply；
  - 提供 adapter.apply 与统一 writer 路径，注册到现有 harness/registry 中；
  - 将 rebuild/backfill 模板参数化到该 projection，能在 dev/test 环境成功跑通最小 smoke。
- 至少 1 组 drills 在 dev/test 环境成功执行：
  - 验证 sample projection 对单条或少量事件的正确性；
  - 产出符合 S6A-4A/S2C contract 的 artifacts（`_recipe.json/_result.json/_metrics`）。
- Evidence 区记录至少 1 次 run：包含 headSha、suite_id 或 scenario_id、run_dir（或 CI run URL），并说明使用的 sample projection 与关键参数。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0-P3 的 onboarding contract + 实现 + drills + 单命令脚本均已跑通，并在 sample projection 上被验证；
  - Evidence 区有至少 1 条可追溯记录（headSha + run_dir/CI URL），可作为后续 S2D-2A/3A 的参考基线。

## P0（Contract｜v1）

### P0-C1-S1（Onboarding contract：最小字段与工件）

- 新增 projection 至少要提供：
  - `ProjectionSpec`：
    - `projection_name`：唯一标识投影，例如本 phase 的示范投影使用 `chronicle_daily_stats`；
    - `scope_keys`：用于限定重建/回填范围的主维度，示范投影为 `tenant_id` + `date`；
    - `requires`：依赖的 SoT / outbox 事件源（例如 `chronicle_events`）；
    - `payload_schema_version`：与 outbox payload_contract 对齐的 schema 版本；
    - `apply`：处理单条事件或一个 batch 的函数入口，负责把 Chronicle 事件投影/聚合到目标表；
  - writer 端入口：统一的 outbox enqueue 函数（带 projection/op/scope/trace），禁止手写裸 SQL/INSERT；
  - harness 注册：在 projection registry 中注册 spec 与 adapter，确保可以由通用 harness 枚举和驱动。

### P0-C1-S2（Onboarding contract：rebuild/backfill & drills）

- 每个按 S2D 标准 onboarding 的 projection，必须具备：
  - 至少 1 条 rebuild smoke（例如重建部分数据或单租户数据），使用 S2C-3A 模板；
  - 至少 1 条 backfill smoke（如适用），使用 S2C-5A 模板；
  - 至少 1 条 drills 场景，验证 outbox→projection 的端到端正确性，并在 catalog 中可枚举。

### P0-C1-S3（证据口径 contract｜v1）

- evidence JSON 必须包含：
  - 投影标识：projection_name / spec id（例如 `chronicle_daily_stats`）；
  - 输入参数：租户/时间范围/事件 id 范围等（示范投影至少包含 tenant_id 与 date 范围）；
  - 输出产物路径：rebuild/backfill/drills 的 `run_dir` 或 artifacts 根目录；
  - PASS/FAIL 字段：`_result.json.ok` 与 failure taxonomy，兼容 S6A-4A/S2C 的 schema_version。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2D-1A/P<phase>-C<cycle>-S<steps>: <summary>`，例如：`S2D-1A/P1-C1-S1: add sample projection spec`。

## Plan（draft）

### P1（实现：框架收口 + sample projection 接入）

- P1-C1-S1：在 Projection harness 中补充 `ProjectionSpec` 的 runtime sanity check（scope_keys/payload_schema_version/requires 非空且格式合理），避免注册非法 spec 仍然可运行。
- P1-C1-S2：以 `chronicle_daily_stats` 作为 sample projection，补齐其 `ProjectionSpec`、adapter.apply 与 writer 路径，确保可通过统一 harness 跑通。

### P2（drill/verify：rebuild/backfill + correctness）

- P2-C1-S1：为 sample projection 配置并跑通最小 rebuild/backfill smoke（使用 S2C-3A/5A 模板），产出 artifacts。
- P2-C1-S2：新增 drills case（或 scenario），验证 outbox→projection 的端到端正确性，并记录 `_recipe.json/_result.json/_metrics`。

### P3（drill/verify：单命令 onboarding 套餐）

- P3-C1-S1：实现单命令脚本（例如 `scripts/projections/s2d_1a_p3c1s1_sample_onboarding.py`），串联 sample projection 的 rebuild/backfill/drills 套餐，并写入 `artifacts/s2d-runs.json`。
- P3-C1-S2：在 runbook 或 README 中记录该脚本的使用方式，为后续 S2D-3A 的统一 hard gate 复用。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 onboarding 最小字段与工件 contract
- [x] `P0-C1-S2`：定义 rebuild/backfill & drills 要求
- [x] `P0-C1-S3`：定义 evidence JSON 口径

### P1（实现）

- [x] `P1-C1-S1`：在 Projection harness 中补充 runtime 校验
- [x] `P1-C1-S2`：实现 sample projection 的 spec/adapter/writer

### P2（drill/verify）

- [x] `P2-C1-S1`：跑通 sample projection 的 rebuild/backfill smoke
- [x] `P2-C1-S2`：跑通 sample projection 的 drills 并产出 artifacts

### P3（单命令 onboarding 套餐）

- [x] `P3-C1-S1`：实现单命令 onboarding 套餐脚本 + artifacts 记账
- [x] `P3-C1-S2`：在 runbook 中记录使用方式

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（sample projection rebuild/backfill smoke｜YYYY-MM-DD）

- headSha：`<git sha at first green run>`
- artifacts：`backend/scripts/labs/s2d1a_chronicle_daily_stats_backfill_smoke.py` → `<run_dir>`
- env（示例，可选）：
  - `OUTBOX_BACKFILL_ENABLED=true`
  - `DATABASE_URL=...`
- 期望（expected）：
  - 使用 backfill 模板对 `chronicle_daily_stats` 发出 1 条 outbox row；
  - 第 1 次 backfill 插入 1 条，重复执行不新增行（idempotent）。
- 观测（observed）：
  - `pass1.inserted == 1 && pass2.inserted == 0 && after2 == 1`（见 `_result.json`）。

### P2-C1-S2（sample projection correctness drills｜YYYY-MM-DD）

- headSha：`<git sha>`
- artifacts：`<run_dir>`
- 期望（expected）：
  - outbox 事件被正确投影到目标表/索引。
- 观测（observed）：
  - ...
  - 参见：`backend/scripts/labs/s2d1a_chronicle_daily_stats_harness_drill.py` 的 `_result.json`。

## Recent changes（for traceability，可选）

- 2026-03-08：scaffold S2D-1A log，定义 Projection onboarding contract 与 sample projection 的执行计划。
