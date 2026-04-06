# governance-contract-record: GC-ISS-0005

- `record_id`: `GC-ISS-0005`
- `contract_id`: `ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY`
- `title`: `issue title keyword prefixes must come from the controlled vocabulary at create time and audit time`

```yaml
contract_record:
  contract_id: ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY
  status: active
  summary: Issue title keyword prefixes must come from the controlled vocabulary, and both create-time issue generation and lifecycle audit must fail closed when live titles drift outside that deterministic source-log-owned expectation.
  governance_area: issue-identity-governance
  applies_to: issue title prefixes rendered from source-log issue_keyword values for real issue creation and later lifecycle audit review
  enforcement_surface: create-time issue generation, shared title derivation helpers, and lifecycle audit title-prefix validation
  violation_semantics: fail
  introduced_by: S0F-1G/P2-C1-S1
  last_changed_by: S0F-1G/P3-C1-S2
  source_refs:
    - docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md
  supersedes: []
  superseded_by: []
  notes:
    - Historical live title repair completed later in S0F-1G without changing the current controlled-vocabulary contract concentrated here.
```

## Reader Notes

- Current active meaning:
  - Blank or disallowed keywords stop real issue creation.
  - Live title-prefix drift is now a deterministic audit failure rather than an informal naming complaint.

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`