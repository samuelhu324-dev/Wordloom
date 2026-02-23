# Log-S2B-2A-2A: transition/write-gate completion → dual-run & cutover closure

---

**id**: `S2B-2A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `v2/write-gate completion + dual-run/cutover closure`
**status**: `stable`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, FailureContract, Projection, Chronicle, Search, epic/s2, sub/2`
**links**: ``
  **issue**: `#56`
  **pr**: ``
  **adr**: `docs/adr/adr-S2B-projection-table-merge.md`
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-02-18`
**updated**: `2026-02-23`

---

## Decision / Outcome（结论区）

**Decision**:

- 将 v2 的第二阶段（2A）定义为“完成 write-gate 剩余两项口径 + 形成 dual-run/cutover 的可执行闭环”，以便 `log-S2B-2A` 可以宣告收工：
  - 排序/分页稳定性（读切换后不掉条/不重复）
  - 可观测共享键一致（新旧链路可串联）
  - dual-run（写侧影子并行）最小实现 + cutover（先读后写）准入清单

**Drivers**:

- 仅有幂等证据仍不足以切写：读侧分页漂移会直接破坏用户体验与审计一致性。
- 缺少共享键，证据链无法落到 traces/logs 的可查询证据，排障与审计不可持续。

**Non-goals**:

- 不追求一次性完成最终合表 schema；本阶段目标是“切换流程可执行、可回滚、可审计”。

**Success criteria（DoD）**:

- 排序/分页稳定性：
  - 定义对外稳定排序键与 tie-breaker
  - shadow verify 覆盖至少两页以上的游标/分页窗口一致性检查
- 可观测共享键一致：
  - drill/runbook 规定最小共享键集合（例如 `run_id`, `library_id`, `outbox_event_id`, `entity_id`）
  - 能在 logs/metrics/traces 中检索到与 drill 产物相互印证的证据
- Dual-run 最小实现：
  - 新 worker 影子并行，但默认不影响外部读写
  - 资源隔离/限速可控，并纳入同一 artifacts 证据链
- Cutover closure：
  - runbook 提供“先读后写”操作步骤与回滚动作
  - cleanup 有 stub + deprecate window + ADR/Log 记账

**Current status（现状）**:

- ✅ 1A（write-gate 第一刀：幂等/唯一性）已收工并具备 CI+本地证据：`docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md`
- ✅ 2A 已收工：
  - ✅ 排序/分页稳定性 drill 入口已落地（要求至少 2 页；CI 可通过 `--ensure-min-rows` 确保有足够数据）
  - ✅ 共享键证据包（最小口径）入口已落地（产出 `shared_keys + evidence_queries`）
  - ✅ dry-run readiness gate 入口已落地（聚合 1A/2A 前置验证；不写入）
  - ✅ true dual-run stage1（读侧并行对账：Postgres vs Elasticsearch）入口已落地（通过 ES backfill + 查询对齐进行最小对账）
  - ✅ canary dual-write（最小真写入 + 默认回滚/cleanup）入口已落地（写入 `search_index` + `search_outbox_events`）
  - ✅ allowlist/sampling sustained dual-write（持续旁写 + soft/strict + DLQ/replay 证据）入口已落地（写入 `search_outbox_events`，默认 cleanup）
  - ✅ 强口径共享键互证（artifacts logs + traces 可检索互证；`_result.json` 提供 grep/jq hints）已补齐
  - ✅ 300s sustained window 证据已补齐（两次 profile 结果均为“真持续 + 真 drain + 严格对账通过”）
  - ✅ window 参数语义（同 id 应成功 / 不同 id 应失败）已补齐（2026-02-20 workflow_dispatch：allowlist mismatch 时 worker claimed=0 且 strict parity 失败；allowlist match 时 strict parity 通过）

**Evidence（代码证据 / 入口证据）**:

- 父 log：`docs/logs/log-S2B-2A-failure-contract-v2.md`
- 子 log（先决）：`docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md`
- Lab manual（本阶段）：`docs/labs/lab-S2B-2A-2A-dual-run-cutover-closure.md`
- Runbook：`docs/runbook/run-S2B-projection-table-merge.md`
- Actions workflow（scenario）：`.github/workflows/drill-shadow-verify-entries.yml`
- Actions workflow（write-gate 专用）：`.github/workflows/drill-write-gate.yml`

CI evidence（2026-02-19）:

- `drill-write-gate` → `shadow_verify_search_index_paging_stability`：run_id=`22164058062-1`（ok=true，pages_checked=2）
- `drill-write-gate` → `shadow_verify_shared_keys`：run_id=`22164060556-1`（ok=true，seed_rows_inserted=5）
- `drill-write-gate` → `shadow_verify_canary_dual_write`：run_id=`22168857459-1`（ok=true，max_writes=5，cleanup_enabled=true，remaining=0）
- `drill-write-gate` → `shadow_verify_dual_write_sampling`：run_id=`22170284952-1`（ok=true，strategy=strict，ensure_min_rows=25，sample_size=20，max_total_events=20，cleanup_enabled=true，remaining=0）

CI evidence（2026-02-19）:

- `drill-write-gate` → `shadow_verify_dual_run_stage1`：run_id=`22174370696-1`（ok=true，strict parity；ES backfill + ordered candidates match）
- `drill-write-gate` → `shadow_verify_dual_run_stage2`：run_id=`22178056521-1`（ok=true，outbox → worker(one-shot) → ES；ordered candidates strict parity）
- `drill-write-gate` → `shadow_verify_dual_run_window`：run_id=`22181124988-1`（ok=true，duration=15s，max_total_events=75，outbox.done=75，worker.exit_code=0，strict parity）

Manual long-window evidence（2026-02-19，workflow_dispatch）:

- `drill-write-gate` → `shadow_verify_dual_run_window`（Profile A，300s）：run_id=`22183281887-1`（ok=true，compare.parity_ok=true，worker.exit_code=0，runtime≈301s，total_events=1490；说明：loop 按到时长结束，事件数略小于理论上限属正常）
- `drill-write-gate` → `shadow_verify_dual_run_window`（Profile B，300s）：run_id=`22183301322-1`（ok=true，compare.parity_ok=true，worker.exit_code=0，runtime≈301s，enqueued_total=300）

Manual allowlist semantics evidence（2026-02-20，workflow_dispatch）:

- Case A（mismatch，预期失败）：run_id=`22210563050-1`
  - scope/library_id=`83c6268e-1b70-4021-9ba3-f7e6242cb860`
  - worker allowlist=`f19bf478-1063-4bee-b4ae-1707304480c6`（不包含 scope id）
  - result：ok=false；outbox.enqueued_total=75；outbox.done=0 pending=75；worker.exit_code=0 但 claimed=0；compare.parity_ok=false；ES candidates=0
  - artifacts：按 Failure Contract 上传 `summary.json + logs.txt + traces.json + worker.log`（你本地下载目录含“四件套”）
- Case B（match，预期成功）：run_id=`22210619481-1`
  - scope/library_id=`83c6268e-1b70-4021-9ba3-f7e6242cb860`
  - worker allowlist=`83c6268e-1b70-4021-9ba3-f7e6242cb860`
  - result：ok=true；outbox.enqueued_total=75；compare.parity_ok=true；ES ids 与 expected_pg_ids 一致
  - artifacts：按 Failure Contract 仅上传 `summary.json`（成功时无 zip 是预期行为）

Local evidence（2026-02-19，devtest DB）:

- `labs shadow-verify-dual-run-stage1`（Postgres vs ES strict parity）：run_id=`local-20260219T150925`（ok=true，seed_rows_inserted=25，pg_candidates_total=20，es_candidates_total=20，parity_ok=true）
- `labs shadow-verify-dual-run-window`（sustained window，periodic enqueue + drain）：run_id=`local-window-20260219T192757`（ok=true；说明：window 结束会主动停止 worker，`worker.exit_code` 可能非 0，以 `_result.json.ok=true` 为准）
- `labs shadow-verify-dual-write-sampling`（CI-safe strict）：run_id=`20260219T133300-sampling-run1`（ok=true，strategy=strict，inject_failed_rate=0.0，cleanup_enabled=true）
- `labs shadow-verify-dual-write-sampling`（DLQ+replay demo）：run_id=`20260219T133500-sampling-dlq-replay-run1`（ok=true，strategy=soft，dlq_failed_simulated_total>0，replayed_total>0，cleanup_enabled=true）

### Artifacts / Failure Contract（截图1-2，落地口径）

- 稳定入口：所有 drills/labs 只允许通过 `backend/scripts/cli.py` 触发（禁止 workflow 内分叉脚本入口）。
- 单一事实源：每次 drill 必须落盘 `_result.json`（作为机器判定与回放的事实源）。
- GitHub Actions artifacts contract：
  - 成功（exit code=0）：只上传 `summary.json`（内容等同该次 `_result.json`）。
  - 失败（exit code≠0，当前约定使用 2）：上传 `artifacts.zip`（至少包含 `summary.json + logs.txt + traces.json`）并让 job 失败。

说明：因此在 Actions UI 里看到“成功时只有 summary.json”是预期行为；需要更详细排查信息时应查看失败时的 zip（或在本地跑同一 CLI drill 取全量快照目录）。

写入点定位（给 2A dual-run/canary 用）：

- 投影表（projection）：`search_index`
- Outbox 表（enqueue events）：`search_outbox_events`
- 入口代码：`backend/infra/search/search_indexer.py` → `PostgresSearchIndexer`（写 `search_index`，并通过 outbox repo enqueue 到 `search_outbox_events`）

**Acceptance checklist（验收清单）**:

- [x] 排序/分页稳定性验证落地并进入 `ok` 判定（至少覆盖 2 页以上的游标翻页一致性）
- [x] 共享键一致性可通过 logs/traces 证据定位（drill 产物可互证；metrics 仍为后续增强项）
- [x] sustained dual-write（allowlist/sampling）具备 soft/strict 策略，并能落 DLQ/replay 的机器可读证据（写入 `_result.json`）
- [x] true dual-run stage1（Postgres vs Elasticsearch）对账 drill 可在 CI 跑通，并产出可审计的 `_result.json + traces.json` 证据
- [x] true dual-run stage2（outbox → worker → ES → 对账）drill 可在 CI 跑通，并产出可审计的 `_result.json + worker.log` 证据
- [x] sustained dual-run window（持续窗口：worker 常驻 + 周期性 enqueue + drain）在 CI 跑通，并形成阈值化准入口径（backlog/failed/retry 受控）
- [x] Dual-run 最小实现上线且具备限速/隔离与回滚（默认不影响外部读写；`SEARCH_OUTBOX_WORKER_ENABLED=0/1` + `OUTBOX_*` knobs + `SEARCH_OUTBOX_LIBRARY_ALLOWLIST`）
- [x] runbook 的准入清单可执行（先读后写、每一步有回滚动作与准入证据；见 `run-S2B` 第 9 节）
- [x] cleanup 的 stub/deprecate/ADR 记账完成（见 `run-S2B` 第 10 节 + ADR 记录）

## Background

v2 在 1A 解决“重复投递/重复副作用”的第一风险后，仍需要解决“读一致性（分页）”与“证据链可串联（共享键）”，才能把 dual-run 与 cutover 变成工程化流程而不是人肉冒险。

## Problem / Malfunction

- 缺少分页稳定性验证会导致读切换后出现掉条/重复，风险直接暴露给用户。
- 缺少共享键会导致 drills 的 `_result.json` 与 traces/logs 无法互证，难以审计。

## What/How to do（落地规则）

### 1) 排序/分页稳定性（建议最小口径）

- 在 runbook/接口层明确“对外排序口径”（含 tie-breaker）。
- 在 drill 中固定一组样本窗口（例如 top-N）并做多页游标翻页一致性检查。

### 2) 可观测共享键一致（建议最小口径）

- 规定共享键集合，并在 worker/查询侧日志中输出。
- drill artifacts 中记录用于检索 traces 的查询条件（例如 service/operation/tags-json）。

### 3) Dual-run + Cutover closure

- dual-run：新旧链路并行消费（写侧影子并行），默认不对外；限速/隔离；可回滚。
- cutover：先读后写；每一步都要有“失败时回滚动作”和“准入证据”。
- cleanup：保留 stub、标注 deprecate window、补 ADR/Log 记账。

## Next

- 把 `shadow_verify_dual_run_stage2` 视为“dual-run 写侧闭环的门槛证据”已就绪；下一步进入 sustained dual-run：以低速/隔离方式让 worker 持续跑一段窗口，观察 backlog/failed/retry（不是只跑一次性 drill）。
- 准入口径已落到 runbook：`docs/runbook/run-S2B-projection-table-merge.md`（Window hard gate + 300s long-window 示例命令）；建议把“连续 N 次（例如 N=3）long-window 均 ok=true”作为推进到更接近可放行的最小门槛。
- Actions 手动触发支持长窗口参数：`drill-write-gate` 在 `scenario=shadow_verify_dual_run_window` 时可通过 `window_*` inputs 覆盖窗口参数（CI 默认仍为 15s）。
- 已验证两次 300s long-window（Profile A/B）均 ok=true 且 strict parity（run_id=`22183281887-1`、`22183301322-1`）。
- 后续维护聚焦到阈值运营：按 runbook 的 long-window 门槛持续抽检（建议连续 N 次）并记录异常回放。
- 若进入下一阶段（S2B 后续子阶段），沿用同一 runbook/ADR 入口扩展，不再分叉脚本入口。

## References

- `docs/logs/log-S2B-2A-failure-contract-v2.md`
- `docs/runbook/run-S2B-projection-table-merge.md`
