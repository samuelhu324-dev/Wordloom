# governance-contract-record: GC-ISS-0005

- `record_id`: `GC-ISS-0005`
- `contract_id`: `ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY`
- `title`: `issue title keyword prefixes must come from the controlled vocabulary at create time and audit time`

```yaml
contract_record:
  contract_id: ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY
  status: deprecated
  summary: Issue title keyword prefixes must come from the controlled vocabulary, and both create-time issue generation and lifecycle audit must fail closed when live titles drift outside that deterministic source-log-owned expectation.
  governance_area: issue-identity-governance
  applies_to: issue title prefixes rendered from source-log issue_keyword values for real issue creation and later lifecycle audit review
  enforcement_surface: create-time issue generation, shared title derivation helpers, and lifecycle audit title-prefix validation
  violation_semantics: fail
  introduced_by: S0F-1G/P2-C1-S1
  last_changed_by: S0F-3E/P6-C1-S2
  source_refs:
    - docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md
  supersedes: []
  superseded_by: []
  notes:
    - This preserved legacy ISS-area record now redirects readers to GC-IID-0002 after the S0F-3E P6 namespace split.
```

## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `split into IID as GC-IID-0002`
- Read now:
  - `GC-IID-0002`

## Reader Notes

- Historical meaning preserved:
  - Blank or disallowed keywords stop real issue creation.
  - Live title-prefix drift is now a deterministic audit failure rather than an informal naming complaint.
- Current successor:
  - `GC-IID-0002`

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`