# governance-contract-record: GC-COMPL-0001

- `record_id`: `GC-COMPL-0001`
- `contract_id`: `LIFECYCLE-THREE-STAGE-COMPLETENESS-AUDIT`
- `title`: `lifecycle completeness is audited separately at creation, PR, and conclusion stages`

```yaml
contract_record:
  contract_id: LIFECYCLE-THREE-STAGE-COMPLETENESS-AUDIT
  status: active
  summary: Lifecycle completeness is audited as three distinct stage-owned surfaces covering creation, PR, and conclusion rather than as one final-state-only review.
  governance_area: lifecycle-completeness-audit
  applies_to: source-log-owned issue and PR lifecycle surfaces that must be classified as create-time, PR-time, or conclusion-time complete against the current docs-GitHub lifecycle contract
  enforcement_surface: the read-only lifecycle audit entrypoint plus the stage-owned completeness matrix that classifies body and sidebar state before later repair work is chosen
  violation_semantics: fail
  introduced_by: S0F-1D/P0-C1-S2
  last_changed_by: S0F-1D/P4-C1-S1
  source_refs:
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
    - docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md
  supersedes: []
  superseded_by: []
  notes:
    - S0E-5A remains the planner and pre-gate orchestration shell, while S0F-1D owns the stable semantic completeness matrix concentrated here.
```

## Reader Notes

- Current active meaning:
  - Lifecycle review must classify missing or malformed state according to the correct ownership stage instead of comparing every item against one final expected body.
  - Creation, PR, and conclusion completeness each own both body and sidebar surfaces where those surfaces are already deterministically known.
- Current concentration boundary:
  - This record owns the semantic completeness matrix.
  - It does not separately index every supporting audit planner or evidence artifact.

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
- Supporting planner shell:
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`