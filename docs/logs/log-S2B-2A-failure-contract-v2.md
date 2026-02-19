# Log-S2B-2A: maintainability/failure contract v2

---

**id**: `S2B-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `maintainability/failure contract v2`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Projection, Search, epic/s2, sub/2`
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

- 在 Failure Contract v1（Shadow verify + Read switch + 统一证据链）的基础上，定义 Failure Contract v2：将“可切写（write cutover）”前置为明确的验收门槛，并把演进路径固定为：Shadow → Dual-run（写侧影子并行）→ Cutover（先读后写）→ Cleanup。
- v2 的核心不是引入新工具，而是把 v1 的 artifacts contract（summary/logs/traces/zip + `_result.json`）升级为“切写级别”的证据链：对账维度必须覆盖幂等/唯一性、排序/分页稳定性、可观测共享键一致。
- v2 强制要求“同一份 runbook 入口 + 同一份 workflow/scenario”，避免 dual-run 之后出现新旧两套故障语义与操作入口。

**Drivers**:

- v1 已经证明“可回滚的读切换 + shadow verify + 证据链”是可落地的；下一阶段风险集中在写侧：dual-run 会放大重复投递、资源抢占、语义漂移等问题。
- 若缺少“切写级别”的验收口径，Dual-run 会退化成“跑着玩”，无法为 cutover 提供审计级证据。

**Non-goals**:

- 不要求立即完成“真正合表/合 projection”的最终形态；v2 关注的是从 v1 进入 dual-run/cutover 的稳定流程。
- 不要求一次性重写所有历史 runbook/drill；优先保证入口稳定，旧位置用 stub 维持链接稳定。
- 不承诺 schema 永远不变；承诺的是对外语义、证据链、回放/排障入口的可维护性。

**Success criteria（DoD）**:

- Shadow verify 升级为“可切写口径”，并持续产出统一 artifacts；当 mismatch/异常发生时，能以非 0 退出并留下可追溯证据。
- Dual-run 期间，新旧处理链路的幂等键明确、资源隔离可控；任何异常可通过开关/限速回滚到安全状态。
- Cutover 顺序固定：先读切换（可一键回滚）再写切换（停旧 worker/不再 claim）；并以指标/trace/对账报告作为准入证据。
- Cleanup 有“stub + deprecate window + ADR/Log 记账”，避免演进烂尾。

**Current status（现状）**:

- v1 已覆盖 Chronicle + Search（Shadow verify + Read switch + GitHub Actions artifacts contract）。
- v2 当前为 draft：本 log 用于把“下一步怎么从 Shadow 进入 Dual-run/cutover”的规则语义结构化，作为后续实现与验收的准绳。

**Evidence（代码证据 / 入口证据）**:

- v1（已存在）：
  - Runbook：`docs/runbook/run-S2B-projection-table-merge.md`
  - Actions workflow（scenario dropdown）：`.github/workflows/drill-shadow-verify-entries.yml`
  - Chronicle shadow verify（stable CLI）：`backend/scripts/cli.py`（`labs shadow-verify-chronicle-entries`）
  - Search shadow verify（stable CLI）：`backend/scripts/cli.py`（`labs shadow-verify-search-index`）
  - Chronicle lab manual：`docs/labs/lab-S2B-1A-1A-chronicle-concurrent-handling.md`
  - Search lab manual：`docs/labs/lab-S2B-1A-2A-search-concurrent-handling.md`
  - Chronicle read switch：`MERGED_READ_ENABLED`
  - Search read switch：`SEARCH_MERGED_READ_ENABLED`
- v2（待补齐）：
  - Shadow verify 校验维度扩展（幂等/唯一性、排序/分页稳定性、共享键一致）
  - Dual-run 写侧影子并行（新 worker/daemon + 隔离/限速/证据链）
  - Write switch 与 cleanup 的验证与 deprecate 记录
  - 子 log 拆分（用于收工 v2）：
    - `docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md`
    - `docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`

补充（已具备的最小闭环证据链）：

- `drill-write-gate` workflow 已包含并跑通 `shadow_verify_dual_run_stage2`（outbox → worker → ES → ordered candidates parity；成功时 artifacts 仅 `summary.json`）。

**Acceptance checklist（验收清单）**:

- [ ] Shadow verify 覆盖“可切写口径”（幂等/唯一性、排序/分页、共享键）
- [ ] Dual-run 默认不影响外部读写，且资源隔离/限速可控
- [ ] Cutover 先读后写，开关/回滚路径清晰
- [ ] Cleanup 通过 stub + deprecate window + ADR/Log 记账完成

## Background

你现在的状态非常清晰：**Shadow verify + Read switch + 证据链（Actions artifacts）**这套“安全护栏”已经在 Chronicle 和 Search 两条链路跑通了。接下来按同一条主线走：Shadow → Dual-run → Cutover → Cleanup。

## Problem / Malfunction

- 当前 shadow verify 仍是“最小有用口径”（如 counts/missing/extra）。这足以做早期对比，但不足以支撑写切换：dual-run 会放大重复投递、乱序/分页漂移、以及新旧链路可观测键不一致等问题。
- 若没有统一的“切写级别”验收口径与证据链，cutover 的风险无法被工程化降低，只能靠人肉判断。

## What/How to do（落地规则）

### 1) 把 Shadow 的验收口径补成“可切写口径”

将 shadow verify 从 counts 对账升级为以下三类（都要进入同一份 artifacts 证据链）：

- 幂等与唯一性：同一 `outbox_event_id/entity_id` 在新侧不能重复（尤其 Search bulk/retry 场景）。
- 排序/分页稳定性：读切到新侧后，分页翻页不能“掉条/重复”。
- 可观测共享键一致：新旧链路 logs/metrics/traces 能用同一组 key 串起来（Failure Contract 的核心）。

### 2) 开始 Dual-run：写侧并行/影子写（不是“读并行”）

同一份输入（outbox）驱动“旧处理器 + 新处理器”并行消费，但默认不影响外部读写。

Dual-run 的最小交付（按优先级）：

- 新 worker/daemon 上线但不对外：只写“新侧表/新侧索引/新侧投影”，对外读仍然受开关控制。
- 幂等键明确：新旧两条消费链路都必须能“重复投递不产生重复副作用”。
- 并行隔离与限速：新链路先低速跑，避免和旧链路抢资源。
- 同一套 Failure Contract & runbook 入口：别新链路一套、旧链路一套。

### 3) Cutover Step A：先切读（你已具备开关与回滚）

- Staging：开启 `MERGED_READ_ENABLED` / `SEARCH_MERGED_READ_ENABLED` 观察一段窗口。
- Prod：canary（小流量/小租户）→ 全量。
- 任意异常：一键关开关回滚。

### 4) Cutover Step B：再切写（停旧 worker → 只留新 worker）

- 先停旧 worker（或让旧 worker 不再 claim）。
- 新 worker 承担 100% 写侧。
- 观察：backlog/oldest age/failed/retry scheduled + traces（证据链继续出）。

### 5) Cleanup：别急着删，先“stub + deprecate + ADR/Log 记账”

- 保留旧入口的 stub（文档/脚本路径别碎掉）。
- 标注 deprecated window（何时下线旧表/旧脚本/旧开关）。
- 写一条 ADR/Log 结论：删除的前提证据是什么（哪些 drills 全绿、哪些指标稳定）。

## Next

- 将 Shadow verify 的校验维度补齐为“可切写口径”，并固化为统一 artifacts 证据链。
- 上线 Dual-run（写侧影子并行）的最小实现：新 worker/限速/隔离 + 对账证据。
- 形成 cutover runbook 的“准入清单”：哪些 drills/指标/对账结果必须满足才允许切读/切写。

## References

- `docs/logs/log-S0C-1A-log-extensions.md`（log 结构规范）
- `docs/logs/log-S2B-1A-failure-contract-v1.md`（Failure Contract v1）
- `docs/runbook/run-S2B-projection-table-merge.md`（合表/合 projection 相关上下文）