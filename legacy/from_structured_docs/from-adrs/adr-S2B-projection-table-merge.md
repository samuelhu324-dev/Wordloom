# ADR-S2B: projection table merge（Shadow → Dual-run → Cutover → Cleanup）

---

**id**: `S2B-projection-table-merge`
**kind**: `adr`               # log | lab | runbook | adr | note
**title**: `adr/S2B-projection-table-merge`
**status**: `stable`          # draft | stable | archived
**scope**: `S2B`
**decision_date**: `2026-02-20`
**context_issue**: `#56, #57`
**decision**: `Consolidate S2B-1A and S2B-2A into one stable projection-merge path with a single runbook/workflow entry, explicit cutover gates, and a cleanup ledger; reserve extension space for later S2B phases without creating parallel entrances.`
  **positive**: `"Single operational entrypoint", "Auditable cutover gates", "Clear rollback + cleanup timeline", "Room for future S2B phases"`
  **negative**: `"Higher documentation discipline", "Need to keep gate thresholds maintained", "Cleanup window requires ongoing governance"`
**supersedes**: `null`
**superseded_by**: `null`

---

## Context

S2B-1A 已建立 Failure Contract v1（shadow verify + read switch + artifacts contract）。
S2B-2A 在此基础上补齐了写侧可切换能力：paging stability、shared keys、true dual-run stage1/stage2、sustained window、canary/sampling 与 DLQ/replay 证据。

在进入 cutover 前，必须避免“实现已具备但入口分叉、证据口径不一致”的维护风险，因此需要把 S2B 的决策收敛为单一操作路径。

## Decision

1) 统一入口（single entrypoint）
- 操作入口统一为：`docs/runbook/run-S2B-projection-table-merge.md`
- 自动化入口统一为：`.github/workflows/drill-write-gate.yml`
- 执行入口统一为：`backend/scripts/cli.py`

2) 固化 cutover 顺序与门槛
- 固定顺序：`Shadow → Dual-run → Cutover(先读后写) → Cleanup`
- 准入以 `_result.json` + workflow artifacts 为事实源：
  - stage1/stage2 parity
  - window hard gate（failed/pending/processing/done==enqueued）
  - shared keys 可反查

3) 固化回滚与 cleanup 记账
- 回滚策略：read switch 一键回退；write switch 可停新写侧并恢复旧 claim。
- cleanup 策略：stub → deprecate window → ADR/Log 记账后再下线。

4) 预留后续空间（S2B future-safe）
- 本 ADR 仅封存 S2B-1A / S2B-2A 已落地规则；
- S2B 后续子阶段（例如更强语义校验、容量/性能门槛）应在本 ADR 下增量扩展，避免新建并行入口。

## Alternatives Considered

- 继续拆分多个 runbook/log 作为“临时真相源”：短期快，但长期会漂移。
- 仅保留代码层入口，不补 runbook/ADR：执行快，但审计与交接成本高。
- 每个场景独立 workflow：可控但运维认知负担大，失败语义难统一。

## Consequences

- 正向：
  - S2B 的操作、证据、回滚路径统一，交接成本降低。
  - 两类窗口语义（allowlist match/mismatch）已成为可复现验收用例。
  - 未来阶段可以在现有结构上递增，不需要重构入口。
- 负向：
  - 需要持续维护 runbook 阈值与 checklist，防止“文档稳定、参数漂移”。
  - cleanup window 需要团队纪律执行，否则会留下长期 stub。

## Implementation Notes

关键文档与证据落点：
- Runbook：`docs/runbook/run-S2B-projection-table-merge.md`
- Parent log：`docs/logs/log-S2B-2A-failure-contract-v2.md`
- Closure log：`docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`
- Labs registry：`docs/labs/INDEX.md`

代表性窗口语义证据（2026-02-20）：
- mismatch（预期失败）：`run_id=22210563050-1`
- match（预期成功）：`run_id=22210619481-1`

## Follow-ups (Reserved)

- 为 S2B 后续阶段补充容量/性能阈值（例如窗口内吞吐、延迟、重试上限）。
- 评估是否将 long-window 连续通过门槛提升为 `stable+` 级别。
- 在不引入新入口的前提下扩展语义对账维度（字段级一致性、排序稳定性压力场景）。
