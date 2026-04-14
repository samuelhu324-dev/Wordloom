# governance-contract-record: GC-REMED-0001

- `record_id`: `GC-REMED-0001`
- `contract_id`: `GUARDED-BATCH-MULTI-ITEM-REMEDIATION-STAGES`
- `title`: `multi-item remediation keeps preview planning, guarded apply, and preserve-existing post-verify as separate fail-closed stages`

```yaml
contract_record:
  contract_id: GUARDED-BATCH-MULTI-ITEM-REMEDIATION-STAGES
  status: active
  summary: Manifest-driven multi-item remediation must remain preview-first, delegate every live mutation through one family-owned guarded apply path, split before mixed-family mutation, and require preserve-existing post-verify before a batch counts as complete.
  governance_area: remediation-governance
  applies_to: manifest-driven historical refresh and bounded live repair batches that plan, apply, and re-verify more than one issue or PR target under one remediation-owned workflow
  enforcement_surface: plan_lifecycle_pre_gate.py, plan_lifecycle_remediation.py, family-owned *_with_pre_gate.py wrappers, and the S0F-1C operator runbook surface
  violation_semantics: fail
  introduced_by: S0F-1C/P0-C1-S2
  last_changed_by: S0F-3F/P6-C1-S2
  source_refs:
    - docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md
    - docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md
  supersedes: []
  superseded_by: []
  notes:
    - S0F-1C owns the current batch-stage boundary for preview planning, guarded apply, split-on-mixed-family mutation, and mandatory preserve-existing post-verify.
    - S0E-7D remains the broader publish-verify-remediation taxonomy and future gate surface; it does not replace this narrower current remediation-stage contract.
    - REMED is admitted as the stable reusable area code from the S0F-3C shortlist because this current surface spans more than one mutation family without widening into a whole-workflow taxonomy.
```

## Reader Notes

- Current active meaning:
  - Multi-item remediation must start with preview planning rather than live mutation.
  - Live apply remains family-owned, even when one remediation manifest or batch plan covers several targets.
  - Mixed remediation families must split before mutation instead of being flattened into one generic apply step.
  - A live remediation batch is incomplete until preserve-existing post-verify is retained per target.

## Traceability

- Stable multi-item remediation owner:
  - `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
- Broader publish-verify-remediation taxonomy context:
  - `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`