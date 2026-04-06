# governance-contract-record: GC-PRB-0001

- `record_id`: `GC-PRB-0001`
- `contract_id`: `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS`
- `title`: `historical merged PR substantive drift still fails the standard check`

```yaml
contract_record:
  contract_id: PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS
  status: active
  summary: The standard PR body completeness check currently treats substantive drift on historical merged PR bodies in the review-owned live set as a fail-on-findings non-pass condition.
  governance_area: pr-body-completeness-review
  applies_to: historical merged PR bodies that are canonically owned by source logs and fall inside the current reviewer-owned PR body completeness review set
  enforcement_surface: review_pr_body_completeness.py plus the standard check wrapper surfaces consumed locally and by workflow-dispatch CI replay
  violation_semantics: fail
  introduced_by: S0F-1I/P4-C1-S1
  last_changed_by: S0F-1J/P2-C1-S1
  source_refs:
    - docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md
    - docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md
    - docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md
  supersedes: []
  superseded_by: []
  notes:
    - S0F-P1 currently shows this contract in action rather than changing its meaning: the workflow-dispatch replay stops because historical merged PR #383 still classifies as substantive drift.
    - This record describes the current active fail semantics, not a desired future split between live enforcement and historical audit reporting.
```

## Reader Notes

- Current active meaning:
  - The reviewer-owned standard check may continue to review historical merged PR bodies if they are inside the canonical source-log-owned review set.
  - If one of those items still classifies as `substantive-drift`, the standard check remains non-pass under `fail_on_findings=true`.
- Current concrete example:
  - `S0F-P1` records that run `24004275695` stops because `S0F-1J/#383` is still substantive drift after normalization.

## Traceability

- Current active packaging surface:
  - `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- Current active triage surface:
  - `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md`
- Earlier standard-check baseline:
  - `docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md`