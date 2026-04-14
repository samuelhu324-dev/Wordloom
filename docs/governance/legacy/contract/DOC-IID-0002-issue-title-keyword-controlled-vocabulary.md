# doc-contract-record: DOC-IID-0002

- `record_id`: `DOC-IID-0002`
- `contract_id`: `ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY`
- `title`: `issue title keyword vocabulary stays explicit across current DOC issue-governance surfaces`

```yaml
doc_contract:
  record_id: DOC-IID-0002
  contract_id: ISSUE-TITLE-KEYWORD-CONTROLLED-VOCABULARY
  family: DOC
  area: IID
  status: active
  summary: Issue title keyword prefixes must come from the controlled vocabulary, and both create-time issue generation and lifecycle audit must fail closed when live titles drift outside that deterministic source-log-owned expectation.
  primary_source_owner: docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md
  applies_to: issue title prefixes rendered from source-log issue_keyword values for real issue creation and later lifecycle audit review
  enforcement_surface: create-time issue generation, shared title derivation helpers, and lifecycle audit title-prefix validation
  violation_semantics: fail
  introduced_by: S0F-1G/P2-C1-S1
  last_changed_by: S0F-4I/P2-C1-S1S2
  source_refs:
    - docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md
    - docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is one of the two issue-identity DOC contract bodies landed from the shared IID execution unit.
    - The corresponding GC row remains in place during transition until matching demotion and reader-transition writes complete.
```

## Current Rule

- Blank or disallowed keywords stop real issue creation.
- Live title-prefix drift is now a deterministic audit failure rather than an informal naming complaint.

## Compact History

- `Current source-owner origin`:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- `Why this current contract exists`:
  - issue-identity governance now reads as family-owned DOC current meaning rather than as GC-registry-only admission vocabulary
- `Major evolution chain`:
  - `S0F-1G` fixed the issue-identity rule surface
  - `S0F-4I` landed the family-owned DOC replacement body for controlled title vocabulary

## Reader Notes

- `GC-IID-0002` remains occupied as a lineage-safe legacy redirect surface during transition, but current family-owned reading now starts here.

## Traceability

- Source-owner log:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- Promotion lane:
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`