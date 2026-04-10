# governance-contract-record: GC-WF-0001

- `record_id`: `GC-WF-0001`
- `contract_id`: `PUBLISH-VERIFY-REMEDIATION-FAILURE-TAXONOMY-AND-HANDLING`
- `title`: `publish-verify-remediation failures stay split into strong-versus-weak structure families with explicit handling semantics`

```yaml
contract_record:
  contract_id: PUBLISH-VERIFY-REMEDIATION-FAILURE-TAXONOMY-AND-HANDLING
  status: active
  summary: Publish-verify-remediation workflow failures must stay split into strong-structure versus weak-structure families, follow one ordered replay/backfill pipeline, and resolve through explicit block, replayable, manual, or reconciliation handling rather than one generic fix-later bucket.
  governance_area: workflow-failure-handling-governance
  applies_to: docs and GitHub automation surfaces whose drift or mutation decisions are evaluated through publish, verify, remediation, and post-apply verify semantics across issue-side and PR-side workflow families
  enforcement_surface: S0E-7D taxonomy artifacts, thin gate planning surfaces, and later wrapper or transport surfaces that replay the same decision vocabulary without owning a separate front-door rule
  violation_semantics: fail
  introduced_by: S0E-7D/P0-C1-S1
  last_changed_by: S0F-3F/P4-C2-S2
  source_refs:
    - docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md
  supersedes: []
  superseded_by: []
  notes:
    - S0E-7D owns the stable current workflow-failure taxonomy, ordered replay/backfill contract, and handling semantics concentrated here.
    - S0E-7E, S0E-7F, and S0E-7G remain support-only orchestration, wrapper, and transport surfaces that reuse this contract without becoming parallel current records.
    - GC-REMED-0001 remains adjacent but narrower: it owns multi-item remediation-stage boundaries rather than the broader workflow failure taxonomy and handling model.
```

## Reader Notes

- Current active meaning:
  - Workflow failures must be classified as strong-structure or weak-structure rather than flattened into one generic drift bucket.
  - Replay and backfill must follow one explicit ordered pipeline.
  - Block, replayable, manual, and reconciliation remain distinct handling outcomes with different operator consequences.

## Traceability

- Stable workflow-failure owner:
  - `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`