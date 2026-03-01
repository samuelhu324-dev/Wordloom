# log-S2C-5A-projection-backfill-template（Backfill Template：从 SoT 回填 outbox 的通用 runner）

---

**id**: `S2C-5A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection backfill template (emit outbox from source-of-truth)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Backfill, Template, epic/s2, sub/5`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # outbox_core baseline
  **reference_log_2**: `docs/logs/log-S2C-3A-projection-rebuild-backfill-template.md` # rebuild template + drills wiring
  **previous_log**: `docs/logs/log-S2C-4A-projection-drills-template.md`
**created**: `2026-03-01`
**updated**: `2026-03-01`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片交付 S2C Phase 4 的未完成项：提供通用 backfill runner/template。
- 目标不是“修完所有 backfill 脚本”，而是把 backfill 从“脚本碎片”升级为可复制的 **平台契约 + 模板实现 + 最小样例 + 证据链**。

**Why now**:

- `S2C-3A` 已交付 rebuild template（bookkeeping + metrics 口径统一）并跑通最小 smoke；但 backfill（从 SoT 回填 outbox）仍缺少统一入口与可审计证据，容易在迁移/故障时语义漂移。
- `S2C-4A` 已稳定化 drills（catalog + reusable runner + guardrails）；backfill template 可以直接复用该证据入口，形成更低成本、更可重复的运维闭环。

## Constraints（约束）

- 不改变 artifacts contract：evidence 以 `_result.json` / snapshot bundle 为 SoT。
- 不破坏既有 stable entrypoints（scripts/workflows/runbooks）；如需迁移，优先 shim。
- 不把高基数字段（run_id/worker_id 等）写入 metrics label；它们只进入结构化日志与 artifacts。
- 本切片不做 Search harness migration（DB→ES）：该迁移属于 S2C Phase 6，后续用 `S2C-6A` 独立交付。

## Trade-off（P2 样例选择：SoT→outbox（DB-only） vs ES bulk backfill）

本切片在 `P2/P3` 选择 **SoT → outbox_events（DB-only emit）** 的 backfill 样例，不选择直接做 **ES bulk backfill**。

- 选择 DB-only（SoT→outbox）的收益：
  - 与 `S2C-5A` 的平台边界一致：backfill 负责“写 outbox”，消费与最终一致性交给 harness/worker/drills。
  - 复用既有 outbox contract（idempotence / payload / reason taxonomy / claim ordering），证据口径更统一。
  - 运行面更窄：只依赖 DB，减少 ES/索引状态带来的不确定性与环境成本。

- 不选 ES bulk 的代价：
  - 无法在本切片直接证明“DB→ES 最终一致 + bulk 性能”这条链路。
  - 对于极大规模数据的重建，DB-only emit 可能需要更长的消费窗口（需要 worker/harness 参与）。

- 结论（本切片的取舍）：
  - `S2C-5A` 先交付“可复制的 backfill contract + runner + DB-only 样例 + 可审计证据”。
  - 若需要 ES bulk backfill/worker 行为迁移，按 `S2C Phase 6` 用 `S2C-6A` 独立切片交付（避免把 ES 依赖与行为迁移混入模板切片）。

## Scope（本 log 范围）

- `P0`：Backfill contract（定义 backfill 的最小输入/输出/幂等/失败语义/风险边界）
- `P1`：Backfill template（通用 runner：参数解析 + 分批扫描 + 幂等 enqueue + 证据输出）
- `P2`：One minimal example（选择 1 个 backfill 样例落地到 template，并保留/添加 stable shim 如需要）
- `P3`：Evidence（按 S2B 口径补齐最小证据：N≥3 或等价稳定性证明）

## Success Criteria（DoD）

- 代码层面：
  - 能用同一套 backfill runner 对任意 projection 执行“从 SoT 回填 outbox（emit events）”，并保证幂等。
  - backfill 默认 DB-only（只写 outbox）；是否消费/是否触发 ES 由 harness/后续切片决定。

- 证据层面：
  - 至少 1 个 backfill scenario 进入 catalog，能用 reusable runner 在本地或 Actions 运行并产出可审计 artifacts。
  - 若 backfill 影响 outbox 行为（idempotence / payload contract / claim ordering），补齐 N≥3 rounds 或等价稳定性证明。

## P0（Backfill contract｜v1）

> 目标：把 backfill 从“临时脚本”升级为“平台契约”，避免后续新增/迁移投影时语义漂移。

### Definition（定义）

- Backfill 是 **从 SoT（source-of-truth）** 生成/修复 outbox backlog 的过程。
- v1 默认只做 “emit outbox events”（写 `outbox_events`），不负责消费（消费由 harness/worker 完成）。

### Inputs（最小输入集合）

- `projection`（必填）：例如 `chronicle_events_to_entries` / `search_index_to_elastic`
- `--dry-run`（可选）：只统计不写入 outbox
- `--batch-size`（可选）：分批扫描/写入（避免大事务）
- `--limit`（可选）：限制总处理量（用于 drills 与风险隔离）
- `--since`（可选）：时间窗（例如按 SoT.updated_at / created_at）
- `--scope-*`（可选）：按 scope keys 过滤（例如 `library_id` / `book_id`），用于隔离运行面
- `--require-enabled-env`（可选，默认开启）：通过 env gate 防止误触发（例如 `OUTBOX_BACKFILL_ENABLED=true`）

### Idempotence（幂等）

- v1 约束：同一 SoT 实体在同一 `event_version` 下重复执行 backfill，不应造成重复的“有效事件”。
- 推荐实现（v1）：使用确定性 outbox id（例如 `uuid5`）或等价的 DB 约束/去重策略。
  - 示例 key（概念）：`{projection}:{entity_type}:{entity_id}:{op}:{event_version}`

### Payload contract（payload 口径）

- v1 约束：写入 `outbox_events.payload` 必须是 JSON object。
- 默认行为：若 backfill 不需要额外 envelope，写入 `{}`（而不是 `NULL`）。

### Outputs（输出与证据）

- 结构化日志必须包含：`projection`、`run_id`、`worker_id`（如适用）、关键 flags（dry-run/limit/since/scope）。
- Evidence 必须产出 `_result.json`（或 snapshot bundle）并记录：
  - headSha、run_id、参数、扫描/写入计数（scanned/enqueued/skipped/errors）

### Non-goals / Risk Boundaries（平台不负责/风险边界）

- v1 不强制统一每个投影的 SoT 扫描策略（全表扫描 vs 增量窗口），但要求每个 backfill 显式声明其扫描边界。
- v1 不负责“投影消费链路的端到端一致性验证”（例如 DB→ES 的最终一致）；那属于 drills/迁移切片（如 `S2C-6A`）。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。同一切片需要“修复后重跑一轮”时才递增。

**Commit / PR 命名**:

- `S2C-5A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P0（Contract）

- P0-S1：明确 backfill v1 的最小输入/输出/幂等/失败语义
- P0-S2：明确 payload contract 与风险边界（不做 search harness migration）

### P1（Backfill template implementation）

- P1-S1：新增 backfill template（runner + result schema + structured logs）
- P1-S2：对齐 shared keys 与 metrics（仅低基数：`projection/op/reason`）

### P2（One minimal example migration）

- P2-S1：选择 1 个最小 backfill 样例落地到 template（优先 DB-only：SoT → outbox）
- P2-S2：保留/新增 stable entrypoint shim（如果该脚本路径已被 runbooks/Procfiles 引用）

### P3（Evidence）

- P3-S1：将 backfill scenario 纳入 catalog 并通过 guardrails
- P3-S2：跑最小证据包并入账（必要时 N≥3 rounds）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 backfill v1 contract（inputs/outputs/idempotence/failure semantics）
- [x] `P0-C1-S2`：明确 Non-goals 与风险边界（不做 Search harness migration）

### P1（Backfill template implementation）

- [x] `P1-C1-S1`：实现通用 backfill runner/template
  Impl: `backend/infra/projection_framework/backfill_template.py` (`run_backfill`, `BackfillEmitter`)
- [x] `P1-C1-S2`：对齐 payload contract（payload default `{}`）与 shared keys（run_id/worker_id only in logs/artifacts）

### P2（One minimal example）

- [x] `P2-C1-S1`：1 个 backfill 样例收敛到 template（SoT → outbox；DB-only）
  Impl: `backend/scripts/labs/s2c5a_backfill_search_outbox_smoke.py`（seed `search_index` → emit `outbox_events(projection=search_index_to_elastic)`）
- [x] `P2-C1-S2`：stable entrypoint shim（如需要）
  Note: 本切片的最小样例以 drills/labs scenario 形式交付；未替换任何既有 ops/runbook 的稳定入口，因此无需 shim。

### P3（Evidence）

- [x] `P3-C1-S1`：scenario 纳入 catalog + guardrails 校验通过
  Scenario: `verify/search/backfill_outbox_smoke`
- [x] `P3-C1-S2`：最小证据入账（N≥3 或等价证明）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL（如有）+ 关键参数。
- 本切片完成后，在此追加至少一条 backfill 相关证据记录（本地或 Actions）。

### Local evidence（DB-only, N=3 rounds）

- Scenario: `verify/search/backfill_outbox_smoke`
- headSha: `4017d56a`
- DB: `postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test`
- Rounds:
  - `local_s2c5a_r2` → `docs/labs/_snapshot/auto/s2c5a_backfill_search_outbox_smoke/local_s2c5a_r2/_result.json`
  - `local_s2c5a_r3` → `docs/labs/_snapshot/auto/s2c5a_backfill_search_outbox_smoke/local_s2c5a_r3/_result.json`
  - `local_s2c5a_r4` → `docs/labs/_snapshot/auto/s2c5a_backfill_search_outbox_smoke/local_s2c5a_r4/_result.json`
