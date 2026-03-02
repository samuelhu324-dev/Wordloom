# log-S2C-6A-search-harness-migration（Phase 6：Search outbox worker → projection harness）

---

**id**: `S2C-6A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `search harness migration (DB→ES; migrate search worker into projection harness)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Worker, Search, ES, epic/s2, sub/6`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_1**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # outbox_core baseline
  **reference_log_2**: `docs/logs/log-S2C-1A-projection-spec-registry-harness.md` # harness core
  **reference_log_3**: `docs/logs/log-S2C-2A-projection-writer-template.md` # writer-template baseline
  **previous_log**: `docs/logs/log-S2C-5A-projection-backfill-template.md`
**created**: `2026-03-01`
**updated**: `2026-03-02`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片交付 `S2C Phase 6`：将 Search outbox worker（DB→ES）迁移到 projection harness。
- 由于该迁移涉及 ES 依赖与行为边界（bulk/index mapping/最终一致/失败重试策略），必须独立证据链与回滚说明，不与 backfill/rebuild/writer/drills 混交付。

## Constraints（约束）

- 不破坏路线 B 的稳定面：既有 stable entrypoints（scripts/runbooks/workflows）不随意改名；如需迁移，优先 shim。
- artifacts contract 保持不变（`_result.json` / snapshot bundle 为 SoT）。
- 不引入高基数 metrics labels；run_id/worker_id 只进日志与 artifacts。

## Scope（本 log 范围）

- `P0`：迁移 contract（harness 行为边界、ES 依赖、失败语义、回滚策略）
- `P1`：实现 Search projection 的 harness adapter（复用 outbox_core/harness 的 claim/lease/retry/reclaim/sanitize）
- `P2`：保持 stable entrypoint（脚本层 shim：旧 worker 入口继续可用，内部调用 harness）
- `P3`：drills + evidence（至少 N≥3 rounds；ES 环境依赖明确；记录 run URL / artifacts）

## Success Criteria（DoD）

- 代码层面：
  - Search 的消费主循环由 harness 驱动（claim → apply → mark_done/mark_retry/mark_failed）。
  - Search 的 apply 逻辑从脚本实现中抽离为可复用 adapter（并由 ProjectionSpec 注册）。
  - 旧脚本入口可继续运行（shim 或兼容 wrapper）。

- 证据层面：
  - 至少 1 个 ES-involved scenario 进入 catalog（requires.es=true），并产出可审计 artifacts。
  - 若迁移影响 outbox 行为/重试口径：至少 N≥3 rounds（与 S2B 口径一致）。

## P0（Migration contract｜v1）

- Projection: `search_index_to_elastic`
- SoT: `search_index`（DB）
- Sink: Elasticsearch index（ES）
- 失败语义：
  - apply 失败必须落入 outbox_core 的 reason taxonomy（低基数；可聚合）。
  - 可重试失败：按 backoff/retry/attempts；不可重试失败：mark_failed 并保留 error。
- 回滚策略：
  - harness migration 必须支持快速回退到旧 worker（通过 entrypoint shim 选择或 feature toggle）。

### P0-C1-S1（现状盘点｜Search outbox worker 行为边界与 ES 依赖）

本节目标：把“现有 worker 的实际行为”写成可迁移的边界清单，避免进入 harness 后语义漂移。

**Stable entrypoints / Ops surface**

- 稳定入口：`backend/scripts/search_outbox_worker.py`（支持 `SEARCH_OUTBOX_WORKER_ENABLED=0` 直接退出，作为快速禁用/回滚面）。
- 实现入口：`backend/scripts/search_outbox_worker_impl.py`（当前主循环/ES 调用/metrics/tracing 在此）。
- 手工回放工具：`backend/scripts/search_outbox_replay_failed.py`（将 terminal failed 行回放为 pending，带审计字段）。

**DB scope / Outbox scope**

- Outbox 表：`outbox_events`（统一 outbox），仅处理 `projection=search_index_to_elastic`。
- Claim 语义：通过 outbox_core `claim_pending_batch` 仅 claim `status=pending AND (next_retry_at IS NULL OR next_retry_at<=now)` 的行；`failed` 默认不会被自动 re-claim。
- 可选隔离面：`SEARCH_OUTBOX_LIBRARY_ALLOWLIST=<uuid,uuid,...>` 仅处理允许的 library 范围。

**ES dependencies / API surface**

- ES 连接：`ELASTIC_URL`（默认 `http://localhost:9200`），索引：`ELASTIC_INDEX`（默认 `wordloom-search-index`）。
- Worker 写入面：
  - Per-event：`PUT /{index}/_doc/{doc_id}`、`DELETE /{index}/_doc/{doc_id}`
  - Bulk：`POST /_bulk`（NDJSON；`Content-Type: application/x-ndjson`）
- Worker 不负责 index/mapping/alias lifecycle（假设 index 已存在且 mapping 可接受 payload）。
- 读路径（应用侧 Stage1 recall）在 `infra/search/elastic_candidate_provider.py`：依赖 `/{index}/_search`，并假设 docs 存在 `entity_type/entity_id/text/snippet/event_version` 等字段。

**Apply logic（SoT→ES 的实际内容）**

- upsert 时会回查 SoT：从 `search_index`（`SearchIndexModel`）读取行并构造 ES doc。
  - 若 SoT 行不存在：视为“无事可做”，直接 ack 成功（避免 delete 与 upsert 竞态导致卡死）。
- delete 时：ES 返回 404 视为幂等 noop（记录 `outbox_idempotent_noop_total`）。
- ES doc id：`{entity_type}:{entity_id}`。

**Mode（per-event vs ES bulk）**

- `OUTBOX_USE_ES_BULK=0`（默认）：对每个 outbox row 单独请求 ES；支持 `OUTBOX_CONCURRENCY>1`，但有 per-entity lock 保证同一实体不乱序。
- `OUTBOX_USE_ES_BULK=1`：把单次 poll 的 rows 组装成一次 `_bulk` 请求；此时 concurrency 被忽略（每 poll 1 个 bulk）。

**Failure classification / Retry semantics**

- 异常 reasons：
  - per-event：基于 outbox_core 的 `classify_httpx_exception_reason`（输出低基数 `es_*` reason）。
  - bulk item：基于 outbox_core 的 `classify_es_bulk_item_failure(status_code)`。
- 是否重试：
  - failure_class 仅在 `{429, 5xx, unknown}` 才允许重试；大多数 4xx 视为不可重试（例如 mapping/parsing）。
  - backoff：指数退避（`OUTBOX_BASE_BACKOFF_SECONDS` / `OUTBOX_MAX_BACKOFF_SECONDS`）。
  - attempt 上限：`OUTBOX_MAX_ATTEMPTS`；但当 reason 为 transient 且 `OUTBOX_TERMINAL_ON_TRANSIENT=0`（默认）时，会“忽略 attempt 上限并持续重试”，同时把写回 attempts 进行 cap（防止无界增长）。

**Leases / Repair / Shutdown**

- lease：`OUTBOX_LEASE_SECONDS`；处理前会 reload 行以确认 owner/lease 未失效。
- 修复：周期性执行 terminal sanitize（清理 stray owner/lease）与 reclaim stuck processing（lease 过期或处理超时）。
- drills 友好：支持 `OUTBOX_EXIT_WHEN_IDLE=1`、`OUTBOX_MAX_RUNTIME_SECONDS` 等 one-shot 运行参数。

**Migration risk notes（需要在 harness 化时显式对齐）**

- per-event upsert doc 有强制 `schema_version=1` + `require_schema_version(...)`；bulk 模式构造的 doc 当前未包含 `schema_version`，且未做同样的 payload contract gate（迁移时需统一口径）。

### P0-C1-S2（迁移契约｜最小 contract + 回滚策略 v1）

本节目标：在进入 `P1` 写 adapter 之前，把“必须保持不变的语义”与“可回滚的开关面”先钉死。

#### 1) Compatibility contract（兼容性条款｜必须对齐）

- **Outbox 语义不变**：继续消费统一 outbox 表 `outbox_events`，且 scope 固定为 `projection=search_index_to_elastic`。
- **Claim/lease/reclaim 语义不变**：
  - claim 规则沿用 outbox_core：仅 claim `status=pending AND (next_retry_at IS NULL OR next_retry_at<=now)`。
  - 处理前必须 reload 校验 owner/lease（防 race / lost claim），lease 过期由 reclaim 兜底。
  - 周期性 sanitize terminal rows + reclaim stuck processing（保持与现 worker 一致的“自修复”能力）。
- **Apply 行为不变**：
  - upsert：从 `search_index` 回查 SoT 生成 doc；SoT 行不存在视为成功 ack。
  - delete：ES 404 视为幂等 noop（不应进入 failed/retry）。
- **Payload contract 统一**（修复 P0-C1-S1 暴露的差异）：
  - harness adapter 在所有写入路径（包含 bulk 优化如果保留）都必须强制 `schema_version=1` 并执行 `require_schema_version(...)`。
  - 任何 payload contract 违规（bad payload / schema mismatch）必须 deterministic failed（不可重试）。

#### 2) Failure & retry contract（失败与重试条款｜可观察、可聚合）

- **reason taxonomy**：所有失败原因必须落入 outbox_core 的低基数 reason（`es_*`），禁止写入高基数原因到 metrics label。
- **retry gate**：保持现有策略：
  - 仅在 failure_class 属于 `{429, 5xx, unknown}` 且 outbox_core 判定 retryable 时允许重试。
  - 大多数 4xx（mapping/parsing 等）必须直接 terminal failed（避免无限重试污染队列）。
- **backoff 与 attempts**：
  - 使用指数退避（`OUTBOX_BASE_BACKOFF_SECONDS` / `OUTBOX_MAX_BACKOFF_SECONDS`）。
  - attempt 上限 `OUTBOX_MAX_ATTEMPTS` 必须保留；对 transient + `OUTBOX_TERMINAL_ON_TRANSIENT=0` 的“持续重试但 attempts cap”语义也必须保留（防止 attempts 无界增长）。

#### 3) Mode contract（bulk 取舍｜v1 默认策略）

- v1 迁移默认先实现 **per-event** harness adapter（最小可行、语义最清晰）。
- ES bulk（`POST /_bulk`）作为性能优化：
  - 若短期必须保留 bulk，需在 harness 侧显式实现并满足上述 payload gate 与失败语义；
  - 若暂不实现 bulk，则将 `OUTBOX_USE_ES_BULK` 视为 legacy-only 能力，并在 shim/文档中明确（避免“看似开启但实际无效”的半兼容）。

#### 4) Rollback / control plane（回滚与开关面｜默认方案）

- **硬禁用开关**（保留现状）：`SEARCH_OUTBOX_WORKER_ENABLED=0` 时稳定入口直接退出（用于紧急止血）。
- **迁移切换开关**（新增 contract）：稳定入口引入单一开关选择实现路径：
  - `SEARCH_OUTBOX_RUNNER=legacy|harness`（默认 `legacy` 直至证据链完成并切 stable）。
  - 目标状态：达到 `P3` 的 N≥3 rounds 证据后，将默认值切换为 `harness`（但仍允许显式回退到 `legacy`）。
- **入口稳定性**：无论内部实现如何变化，稳定入口路径保持不变（Procfile / docs 不需要同步改动）。

#### 5) Evidence contract（证据条款｜与 drills 对齐）

- harness 模式必须能以 drills scenario 的方式运行（`OUTBOX_EXIT_WHEN_IDLE=1` / `OUTBOX_MAX_RUNTIME_SECONDS` 等 one-shot knobs 生效）。
- ES-involved scenario 必须明确 requires.es=true，并产出 `_result.json` + snapshot bundle（记录模式：legacy/harness、bulk/per-event、关键 env knobs）。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2C-6A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P0（Contract）

- P0-S1：梳理 Search worker 现状（ES bulk、mapping/index lifecycle、失败分类）
- P0-S2：定义 harness migration 的最小 contract 与回滚面

### P1（Harness adapter）

- P1-S1：抽离 Search apply（输入 outbox row → ES side-effect）为 adapter
- P1-S2：将 `search_index_to_elastic` 接入 registry/harness（ProjectionSpec + adapter entrypoint）

### P2（Stable entrypoint shim）

- P2-S1：保留 `backend/scripts/search_outbox_worker_impl.py` 等稳定入口
- P2-S2：将旧入口内部改为调用 harness runner（必要时 subprocess 避免 nested event loop）

### P3（Evidence）

- P3-S1：新增 scenario（requires.es=true）并通过 guardrails
- P3-S2：跑证据入账（N≥3 rounds 或等价证明）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：梳理 Search worker 行为边界与 ES 依赖
- [x] `P0-C1-S2`：定义最小 contract + 回滚策略

### P1（Harness adapter）

- [x] `P1-C1-S1`：抽离 Search apply 为 adapter
  Impl: `backend/infra/projection_framework/adapters/search_index_to_elastic.py`（`build_es_doc_from_search_row`, `apply_upsert`, `apply_delete`, `apply`）
  Note: legacy worker 已复用 adapter 的 doc builder（bulk 路径补齐 `schema_version` gate）
- [x] `P1-C1-S2`：接入 ProjectionSpec/registry/harness
  Impl: `backend/infra/projection_framework/builtins.py` 将 `search_index_to_elastic` 的 `apply_entrypoint` 接到 adapter `apply`

### P2（Stable entrypoint shim）

- [x] `P2-C1-S1`：稳定入口保留（脚本路径不破坏）
  Impl: `backend/scripts/search_outbox_worker.py`（继续作为稳定入口；保持 `SEARCH_OUTBOX_WORKER_ENABLED=0` 快速禁用面）
- [x] `P2-C1-S2`：shim 内部调用 harness runner
  Impl: `backend/scripts/search_outbox_worker.py` 引入 `SEARCH_OUTBOX_RUNNER=legacy|harness`（默认 legacy；harness 路径调用 `infra.projection_framework.harness.main` 并默认 `--projection search_index_to_elastic`）

### P3（Evidence）

- [x] `P3-C1-S1`：scenario 纳入 catalog + guardrails 校验通过
  Impl: `docs/labs/scenarios/catalog.yml` 新增 `verify/search/harness_es_smoke`（requires.es=true）
- [x] `P3-C1-S2`：最小证据入账（N≥3 或等价证明）
  Impl: `backend/scripts/labs/s2c6a_search_harness_es_smoke.py`（自种子 + 插入 outbox_events + stable entrypoint 以 harness 模式跑一次 + 校验 ES doc）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL（如有）+ 关键参数。
- 本切片完成后，在此追加 Search harness migration 的证据记录。

### Evidence: verify/search/harness_es_smoke（local）

- headSha: `f0aa6c35`
- scenario: `verify/search/harness_es_smoke`（requires.es=true）
- env: `SEARCH_OUTBOX_RUNNER=harness`, `OUTBOX_EXIT_WHEN_IDLE=1`, `ELASTIC_URL=http://localhost:19200`, `ELASTIC_INDEX=wordloom-test-search-index`
- rounds (N=3; all ok=true):
  - run_id: `s2c6a_p3_round1_20260302_110130` → `docs/labs/_snapshot/auto/s2c6a_search_harness_es_smoke/s2c6a_p3_round1_20260302_110130/_result.json`
  - run_id: `s2c6a_p3_round2_20260302_110154` → `docs/labs/_snapshot/auto/s2c6a_search_harness_es_smoke/s2c6a_p3_round2_20260302_110154/_result.json`
  - run_id: `s2c6a_p3_round3_20260302_110211` → `docs/labs/_snapshot/auto/s2c6a_search_harness_es_smoke/s2c6a_p3_round3_20260302_110211/_result.json`
