# governance-contract-record: GC-PRR-0001

- `record_id`: `GC-PRR-0001`
- `contract_id`: `PR-BODY-CANONICAL-REVIEW-CLASSIFICATION`
- `title`: `PR body reviewer classifies exact match, formatting-only drift, and substantive drift against canonical expectations`

```yaml
contract_record:
  contract_id: PR-BODY-CANONICAL-REVIEW-CLASSIFICATION
  status: active
  summary: The read-only PR body completeness reviewer rebuilds canonical expected PR bodies from source logs and classifies exact match, formatting-only drift, substantive drift, stop, or bounded skip without mutating GitHub state.
  governance_area: pr-body-completeness-review
  applies_to: historical merged PR bodies and current review-owned PR body sets whose canonical expected body is derived from source-log ownership
  enforcement_surface: review_pr_body_completeness.py, retained reviewer artifacts, and the reviewer-owned runbook surface
  violation_semantics: report-only
  introduced_by: S0F-1H/P1-C1-S1
  last_changed_by: S0F-3E/P6-C3-S1
  source_refs:
    - docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md
  supersedes: []
  superseded_by: []
  notes:
    - This current record concentrates the read-only classification semantics that were previously fused into the older GC-PRB-0001 umbrella.
```

## Reader Notes

- Current active meaning:
  - The reviewer remains source-log-owned and read-only.
  - Exact match, formatting-only drift, substantive drift, stop, and bounded skip remain classification outcomes produced before any downstream gate or remediation choice.

## Traceability

- Stable reviewer owner:
  - `docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md`