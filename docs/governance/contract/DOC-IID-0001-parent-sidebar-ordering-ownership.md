# doc-contract-record: DOC-IID-0001

- `record_id`: `DOC-IID-0001`
- `contract_id`: `ISSUE-PARENT-SIDEBAR-ORDERING-OWNERSHIP`
- `title`: `parent sidebar ordering ownership stays explicit across current DOC issue-governance surfaces`

```yaml
doc_contract:
  record_id: DOC-IID-0001
  contract_id: ISSUE-PARENT-SIDEBAR-ORDERING-OWNERSHIP
  family: DOC
  area: IID
  status: active
  summary: Top-level parent issue sidebar ordering is owned by the source-log child ledger, and live GitHub sidebar order is an audited projection that must be repaired or failed when it drifts.
  primary_source_owner: docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md
  applies_to: top-level parent issues whose live GitHub sub-issue order must match the canonical source-log-owned child order
  enforcement_surface: lifecycle audit semantics plus the bounded parent-subissue reprioritize surface used only when the live child set matches the canonical source-owned set
  violation_semantics: fail
  introduced_by: S0F-1G/P1-C1-S1
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

- GitHub sidebar order is not authoritative when it conflicts with the source-log-owned child ledger.
- Reordering is allowed only through the bounded canonical reprioritize path, not through ad hoc remove-and-readd mutations.

## Compact History

- `Current source-owner origin`:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- `Why this current contract exists`:
  - issue-identity governance now reads as family-owned DOC current meaning rather than as GC-registry-only admission vocabulary
- `Major evolution chain`:
  - `S0F-1G` fixed the issue-identity rule surface
  - `S0F-4I` landed the family-owned DOC replacement body for parent sidebar ordering

## Reader Notes

- `GC-IID-0001` remains a lineage-safe narrow-registry row during transition, but current family-owned reading may now start here.

## Traceability

- Source-owner log:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- Promotion lane:
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`