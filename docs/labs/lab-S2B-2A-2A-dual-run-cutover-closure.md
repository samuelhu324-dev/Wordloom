# Lab-S2B-2A-2A：write-gate completion → dual-run & cutover closure

---

**id**: `S2B-2A-2A`
**kind**: `lab`               # log | lab | runbook | adr | note
**title**: `v2/write-gate completion + dual-run/cutover closure`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, FailureContract, Projection, Chronicle, Search, sub/2`
**links**: ``
  **issue**: `#56`
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-02-18`
**updated**: `2026-02-19`

---

目标：把 Failure Contract v2 的“可切写口径”补齐到能支撑 dual-run 与 cutover 的可执行闭环。

本 lab 聚焦 2A 三件事：

- 排序/分页稳定性（读切换后不掉条/不重复）
- 可观测共享键一致（drill 产物能反查 logs/traces；metrics 为后续增强项）
- dual-run（写侧影子并行）最小实现 + cutover（先读后写）准入清单

说明：本 lab 是 2A 的“操作与证据模板”。对应实现与验收语义在：

- `docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`

---

## 0) 前置条件

- 有可用 Postgres（本地/容器均可）
- 已完成 Alembic migrations
- 1A（write-gate：唯一性/幂等最小代理）已通过：
  - `python backend/scripts/cli.py labs shadow-verify-search-index-write-gate --database-url "postgresql://..."`

---

## 1) 执行方式

本阶段的稳定 CLI 入口将分步落地；当前已落地以下入口（分页稳定性 + 共享键证据包 + readiness gate + canary + sampling）：

- 分页稳定性 verify（Search）：
  - `python backend/scripts/cli.py labs shadow-verify-search-index-paging-stability --database-url "postgresql://..."`
  - 说明：该命令要求验证至少 2 页；若数据库数据不足，可追加：
    - `--ensure-min-rows 120`（用于 CI/空库，让验证具备意义）

- 共享键证据包（Search，最小口径）：
  - `python backend/scripts/cli.py labs shadow-verify-shared-keys --database-url "postgresql://..."`
  - 说明：该命令输出 `shared_keys + evidence_queries`，并额外发出强互证 probe：
    - stdout：打印一行 JSON（`event=labs.shared_keys.probe`，包含 `run_id/scope/sample`）
    - 快照目录：写入 `traces.json`（包含携带相同属性的 span）
    用于在 artifacts 的 logs/traces 中互证；若需要确保 sample 存在，可追加：
    - `--ensure-min-rows 5`

- dry-run readiness gate（2A：把 1A/2A 前置条件聚合成一次 drill 证据包，不写入）：
  - `python backend/scripts/cli.py labs shadow-verify-dual-run-readiness-gate --database-url "postgresql://..."`
  - 说明：该命令会在一个 `_result.json` 中聚合：write-gate（1A）+ paging stability（2A）+ shared keys evidence bundle（2A）。
    - 这一步仍不等于 dual-run 真正写入/切换，只是把“准入证据链骨架”先跑通。

- true dual-run stage1（2A：读侧并行对账，Postgres vs Elasticsearch）：
  - `python backend/scripts/cli.py labs shadow-verify-dual-run-stage1 --database-url "postgresql://..."`
  - 说明：该命令走“CI-safe”路径，不启动 outbox worker，只做最小闭环：
    - 在 `search_index` 里 seed 少量 `entity_type='block'` 的 drill-scoped 数据（可用 `--ensure-min-rows` 保障空库也能跑）
    - 运行 legacy backfill 把 Postgres 的 `search_index` 写入 ES（通过 `ELASTIC_URL/ELASTIC_INDEX` 或参数覆盖）
    - 用同一 token 同时查询 Postgres 与 ES，并对比有序 candidates（`--strategy strict|soft`）
  - 输出：`_result.json` + `traces.json`（probe span），并额外落盘 `backfill.log` 便于排查。

- canary dual-write（2A：最小真写入 + 默认回滚/cleanup）：
  - `python backend/scripts/cli.py labs shadow-verify-canary-dual-write --database-url "postgresql://..."`
  - 说明：该命令会写入极小的 canary 行到两张表：
    - `search_index`（projection）
    - `search_outbox_events`（outbox enqueue）
    然后验证写入成功，并默认执行 cleanup（作为 rollback 证据）。
  - 代码定位（写入点）：`backend/infra/search/search_indexer.py` 的 `PostgresSearchIndexer`（写 `search_index` + enqueue `search_outbox_events`）

- allowlist/sampling sustained dual-write（2A：持续旁写 + 策略/回放证据）：
  - `python backend/scripts/cli.py labs shadow-verify-dual-write-sampling --database-url "postgresql://..."`
  - 说明：该命令不会改动 `search_index`，而是从 `search_index` 采样既有行，向 `search_outbox_events` enqueue（影子旁写），用于把 dual-run 从“canary 写 5 条”升级到“按 allowlist/sampling 持续旁写”。
  - allowlist / sampling：
    - `--library-id <uuid>`：限定租户（最常用的 allowlist）
    - `--entity-types block,book,tag`：限定 entity_type（可选）
    - `--duration-seconds / --interval-seconds / --max-total-events`：持续旁写窗口与上限
  - 新侧失败策略（soft/strict）+ DLQ/replay 证据：
    - `--strategy strict|soft`：strict 表示发现 failed 立即判定不通过；soft 表示允许 failed 但必须落证据
    - `--inject-failed-rate 0.2`：模拟新侧失败（把部分 outbox 行标记为 `status=failed`，视作 DLQ）
    - `--replay-failed --replay-by ops --replay-reason "..."`：模拟/验证 replay（failed -> pending + 审计字段）
  - 默认会 `--cleanup` 删除本次插入的 outbox 行，保持 CI/devtest 干净（作为 rollback 证据的一部分）。

后续待补齐（2A 里程碑）：

- 共享键 metrics 强互证（Prometheus/Grafana 侧可反查到同一链路的指标证据）
- Dual-run drill（新旧链路并行消费 + 对账 + 可回滚的强口径闭环；包含 worker 侧限速/隔离/回滚）

默认输出目录约定（与 1A 一致，自动快照）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/<scenario>/<run_id>/_result.json`

shared keys 额外输出：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_shared_keys/<run_id>/traces.json`

---

## 2) 结果解释（验收口径）

### 2.1 排序/分页稳定性（最小口径）

目标：读切到新侧后，分页翻页不能掉条/重复。

最小证据建议包含：

- `page_size`
- `pages_checked`（至少 2）
- `data_sufficient`（至少有 `page_size * pages_checked` 行可验证）
- `duplicates_across_pages_total`
- `ok`

### 2.2 可观测共享键一致（最小口径）

目标：drill 的 `_result.json` 能给出“如何在 logs/traces 里检索同一条链路”的可执行查询条件。

最小证据建议包含：

- `run_id`
- `scope`（如 `library:<uuid>`）
- `shared_keys`（至少包含 `run_id/library_id/entity_id/outbox_event_id` 的子集，按链路实际可得）
- `evidence_queries`（例如：service/operation/labels 或日志 grep 模板）
- `observability`（例如：probe 的 trace_id/span_id、`traces.json` 写入状态）
- `ok`

### 2.3 Dual-run + Cutover closure（准入清单模板）

目标：把“先读后写”的步骤固化成 runbook 可执行的 checklist。

最小准入建议包含：

- write-gate（1A）已通过（CI+本地可重复）
- 分页稳定性通过
- 共享键一致性通过
- dual-run 已以低速运行并稳定一段窗口（backlog/oldest age/failed 受控）
- 回滚动作明确（关开关/停新 worker/恢复旧 worker）

---

## 3) 证据与关联位置

- 父 log：`docs/logs/log-S2B-2A-failure-contract-v2.md`
- 子 log（语义与验收）：`docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`
- 先决 log（1A）：`docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md`
- Runbook：`docs/runbook/run-S2B-projection-table-merge.md`

CI evidence（2026-02-19）:

- paging stability：run_id=`22164058062-1`（`ok=true`，`pages_checked=2`）
- shared keys（evidence bundle）：run_id=`22164060556-1`（`ok=true`）
- canary dual-write：run_id=`22168857459-1`（`ok=true`，`max_writes=5`，`cleanup_enabled=true`，`remaining=0`）
- dual-write sampling：run_id=`22170284952-1`（`ok=true`，`strategy=strict`，`ensure_min_rows=25`，`sample_size=20`，`max_total_events=20`，`cleanup_enabled=true`，`remaining=0`）

CI evidence（2026-02-19）:

- true dual-run stage1 parity：run_id=`22174370696-1`（`ok=true`，Postgres vs ES ordered candidates strict parity）

Local evidence（2026-02-19，devtest DB）:

- true dual-run stage1 parity：run_id=`local-20260219T150925`（`ok=true`，`seed_rows_inserted=25`，`pg_candidates_total=20`，`es_candidates_total=20`，`parity_ok=true`，`strategy=strict`）
- dual-write sampling（CI-safe strict）：run_id=`20260219T133300-sampling-run1`（`ok=true`，`strategy=strict`，`inject_failed_rate=0.0`）
- dual-write sampling（DLQ+replay demo）：run_id=`20260219T133500-sampling-dlq-replay-run1`（`ok=true`，`strategy=soft`，`dlq_failed_simulated_total>0`，`replayed_total>0`）

说明：按截图1-2合约，成功时 Actions artifact 下载包内仅包含 `summary.json`（其内容即 drill 的 `_result.json`）。

---

## 4) 常见失败与排查（占位）

- 分页不稳定：优先检查稳定排序键与 tie-breaker 是否固定；其次检查游标字段是否存在“同值大量碰撞”。
- 共享键缺失：优先在 worker/query 侧补日志字段与 trace tags，再回填 drill 的 `evidence_queries`。
- dual-run 资源争用：先限速/隔离，再做回放与对账，不要直接上来 full speed。
