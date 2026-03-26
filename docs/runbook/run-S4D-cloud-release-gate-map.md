# run-S4D (Cloud Release Gate Map)

---

**id**: `run-S4D-cloud-release-gate-map`
**kind**: `runbook`
**title**: `run/S4D-cloud-release-gate-map`
**status**: `stable`
**scope**: `S4D`
**decision_date**: `2026-03-26`
**context_issue**:
  **DoD**: `Operators and Agent/Copilot can map summary.json gate results to the exact first-read file without loading the full cloud release orchestrator.`
  **Labs**: ``
**decision**: `Use this gate map as the default bridge between summary.json terminalGate/failureClass and the exact runbook/script section to inspect next.`
  **positive**: `"Smaller first-read surface", "Faster gate-to-file routing", "Less need to load cloud_release_workflow.sh whole"`
  **negative**: `"Needs maintenance if gates change", "Still depends on summary.json being present"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 把 `summary.json` 里的 `terminalGate`、`failureClass` 和首读文件做成一张小地图。
- 让排障默认路径从“打开整个 orchestrator”改成“先看 gate map，再看精确对象”。
- 给 S4D-4B / S4D-4C / stable-runner dispatch 共用同一套 gate-level first-read 规则。

## 2) Gate Map

| terminalGate | 常见 failureClass | first read | second read | 何时才读 orchestrator |
| --- | --- | --- | --- | --- |
| `identity_auth_gate` | `identity_auth_failure` | `preflight.log` | `docs/runbook/run-S4D-cloud-runtime-release-operations.md` | 只有在 SSH args 或 preflight decision 仍不清楚时 |
| `target_reachability_gate` | `target_reachability_failure` | `preflight.log` | `docs/runbook/run-S4D-cloud-runtime-release-operations.md` | 只有在 transport failure 归类仍不清楚时 |
| `release_contract_gate` | `contract_validation_failure` | `preflight.log` 或 `deploy.log` | `docs/runbook/run-S4D-cloud-runtime-release-operations.md` | 只有在 contract 是哪一步判失败仍不清楚时 |
| `deploy_execution_gate` | `deploy_execution_failure` | `deploy.log` | `scripts/ops/cloud_release_run_container.sh` | 只有在 deploy gate 如何 promote 成 summary 不清楚时 |
| `dependency_connectivity_gate` | `dependency_connectivity_failure` | `verify.log` | `docs/logs/log-S4D-4C-408-timeout-eradication.md` | 只有在 verify failure taxonomy 仍不清楚时 |
| `post_change_verify_gate` | `verify_failure` | `verify.log` | `scripts/ops/cloud_release_verify.sh` | 只有在 verify PASS/FAIL promote 逻辑不清楚时 |
| `rollback_readiness_gate` | `rollback_failure`, `rollback_recovery` | `rollback.log` | `scripts/ops/cloud_release_rollback.sh` | 只有在 rollback result 如何写回 summary 不清楚时 |
| `evidence_capture` | `evidence_capture_failure` | `summary.json` | `operator_guidance.txt` | 只有在 evidence promotion 逻辑不清楚时 |

## 3) Minimal Investigation Order

1. 先读 `summary.json`
2. 按 `terminalGate` 进入上表对应的 `first read`
3. 只有在 first read 仍不能解释结果时，才打开 `second read`
4. 只有在“为什么 summary 会这样记账”仍不清楚时，才读 `scripts/ops/cloud_release_workflow.sh`

## 4) Notes

- `scripts/ops/cloud_release_workflow.sh` 现在应被视为 gate orchestrator，而不是默认第一入口。
- 对 S4D-4C 来说，这份 gate map 的价值在于减少对大脚本全文检索的依赖。
- 对 S4D-4B 来说，这份 gate map 的价值在于让 Actions run summary 可以稳定落到更窄的人工 handoff 路径。

## 5) Related References

- `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- `docs/runbook/run-S4D-4C-agent-context-navigation.md`
- `scripts/ops/cloud_release_workflow.sh`
- `scripts/ops/cloud_release_verify.sh`
- `scripts/ops/cloud_release_rollback.sh`