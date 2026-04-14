# governance-contract-record: GC-PRB-0001

- `record_id`: `GC-PRB-0001`
- `contract_id`: `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS`
- `title`: `historical merged PR substantive drift still fails the standard check`

```yaml
contract_record:
  contract_id: PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS
  status: deprecated
  summary: The standard PR body completeness check currently treats substantive drift on historical merged PR bodies in the review-owned live set as a fail-on-findings non-pass condition.
  governance_area: pr-body-completeness-review
  applies_to: historical merged PR bodies that are canonically owned by source logs and fall inside the current reviewer-owned PR body completeness review set
  enforcement_surface: review_pr_body_completeness.py plus the standard check wrapper surfaces consumed locally and by workflow-dispatch CI replay
  violation_semantics: fail
  introduced_by: S0F-1I/P4-C1-S1
  last_changed_by: S0F-3E/P6-C3-S2
  source_refs:
    - docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md
    - docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md
  supersedes: []
  superseded_by: []
  notes:
    - This preserved umbrella record now redirects readers to GC-PRR-0001 and GC-PRG-0001 after the S0F-3E P6-C3 split.
```

## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `split into GC-PRR-0001 and GC-PRG-0001`
- Read now:
  - `GC-PRR-0001`
  - `GC-PRG-0001`

## Reader Notes

- Historical umbrella meaning preserved:
  - The old fused `PRB` contract used to combine read-only reviewer classification and fail-on-findings gate semantics in one record.
  - That combined current reading is now replaced by one reviewer contract and one gate contract.
- Current successors:
  - `GC-PRR-0001`
  - `GC-PRG-0001`

## Traceability

- Current active packaging surface:
  - `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- Current active triage surface:
  - `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md`
- Earlier standard-check baseline introduced by:
  - `S0F-1I/P4-C1-S1`