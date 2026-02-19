# Log-S2B-2A-2A: transition/write-gate completion → dual-run & cutover closure

---

**id**: `S2B-2A-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `v2/write-gate completion + dual-run/cutover closure`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, FailureContract, Projection, Chronicle, Search, epic/s2, sub/2`
**links**: ``
  **issue**: `#56`
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-02-18`
**updated**: `2026-02-19`

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
- ⏳ 2A 进行中：
  - ✅ 排序/分页稳定性 drill 入口已落地（要求至少 2 页；CI 可通过 `--ensure-min-rows` 确保有足够数据）
  - ✅ 共享键证据包（最小口径）入口已落地（产出 `shared_keys + evidence_queries`）
  - ✅ dry-run readiness gate 入口已落地（聚合 1A/2A 前置验证；不写入）
  - ✅ canary dual-write（最小真写入 + 默认回滚/cleanup）入口已落地（写入 `search_index` + `search_outbox_events`）
  - ⏳ 强口径共享键互证（logs/metrics/traces 可检索到与 drill 互证的证据）仍待补齐

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

说明：按截图1-2合约，成功时 artifact 下载包内仅包含 `summary.json`（其内容即 drill 的 `_result.json`）。

写入点定位（给 2A dual-run/canary 用）：

- 投影表（projection）：`search_index`
- Outbox 表（enqueue events）：`search_outbox_events`
- 入口代码：`backend/infra/search/search_indexer.py` → `PostgresSearchIndexer`（写 `search_index`，并通过 outbox repo enqueue 到 `search_outbox_events`）

**Acceptance checklist（验收清单）**:

- [x] 排序/分页稳定性验证落地并进入 `ok` 判定（至少覆盖 2 页以上的游标翻页一致性）
- [ ] 共享键一致性可通过 logs/metrics/traces 证据定位（drill 产物能反查到观测证据）
- [ ] Dual-run 最小实现上线且具备限速/隔离与回滚（默认不影响外部读写）
- [ ] runbook 的准入清单可执行（先读后写、每一步有回滚动作与准入证据）
- [ ] cleanup 的 stub/deprecate/ADR 记账完成

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

- 在 1A 完成后，按本子 log 的 DoD 逐项拆成可执行任务并落到 runbook 与 drill 证据链。
- 推荐的下一步（优先级最高）：先落地 “dry-run readiness gate”（不写入），把 dual-run/cutover 的开关、范围、回滚、证据链骨架跑通后，再引入最小 canary 写入版本。

## References

- `docs/logs/log-S2B-2A-failure-contract-v2.md`
- `docs/runbook/run-S2B-projection-table-merge.md`
