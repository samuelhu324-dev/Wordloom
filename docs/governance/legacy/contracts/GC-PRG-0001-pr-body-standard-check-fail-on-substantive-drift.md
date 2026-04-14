# governance-contract-record: GC-PRG-0001

- `record_id`: `GC-PRG-0001`
- `contract_id`: `PR-BODY-STANDARD-CHECK-FAIL-ON-SUBSTANTIVE-DRIFT`
- `title`: `standard PR body check stays non-pass when reviewer findings include substantive drift`

```yaml
contract_record:
  contract_id: PR-BODY-STANDARD-CHECK-FAIL-ON-SUBSTANTIVE-DRIFT
  status: active
  summary: The packaged standard PR body completeness check remains non-pass when the reviewer reports substantive drift inside the canonical review-owned set while fail_on_findings is enabled.
  governance_area: pr-body-gate-governance
  applies_to: local task and workflow-dispatch standard-check surfaces that consume reviewer results for PR body completeness decisions
  enforcement_surface: plan_pr_body_completeness_check_wrapper.py, invoke_pr_body_completeness_check.ps1, package task packaging, and workflow-dispatch CI replay
  violation_semantics: fail
  introduced_by: S0F-1I/P4-C1-S1
  last_changed_by: S0F-3E/P6-C3-S1
  source_refs:
    - docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md
    - docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md
  supersedes: []
  superseded_by: []
  notes:
    - This current record concentrates the gate semantics that were previously fused into the older GC-PRB-0001 umbrella.
    - S0F-1I now survives only as the archived convergence baseline that introduced this gate standing; it is no longer the stable current source anchor for this record.
```

## Reader Notes

- Current active meaning:
  - Reviewer classification and gate decision are no longer the same contract.
  - When the reviewer reports substantive drift in the current review-owned set, the packaged standard check remains non-pass under `fail_on_findings=true`.

## Traceability

- Stable gate packaging owner:
  - `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- Historical baseline introduced by:
  - `S0F-1I/P4-C1-S1`