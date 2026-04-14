# governance-contract-record: GC-IID-0001

- `record_id`: `GC-IID-0001`
- `contract_id`: `ISSUE-PARENT-SIDEBAR-ORDERING-OWNERSHIP`
- `title`: `top-level parent sidebar ordering remains source-log-owned rather than GitHub-owned`

```yaml
contract_record:
  contract_id: ISSUE-PARENT-SIDEBAR-ORDERING-OWNERSHIP
  status: deprecated
  summary: Top-level parent issue sidebar ordering is owned by the source-log child ledger, and live GitHub sidebar order is an audited projection that must be repaired or failed when it drifts.
  governance_area: issue-identity-governance
  applies_to: top-level parent issues whose live GitHub sub-issue order must match the canonical source-log-owned child order
  enforcement_surface: lifecycle audit semantics plus the bounded parent-subissue reprioritize surface used only when the live child set matches the canonical source-owned set
  violation_semantics: fail
  introduced_by: S0F-1G/P1-C1-S1
  last_changed_by: S0F-4I/P3-C1-S1S2
  source_refs:
    - docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md
  supersedes: []
  superseded_by:
    - DOC-IID-0001
  notes:
    - This preserved GC registry record now redirects readers to DOC-IID-0001 after the S0F-4I family-owned promotion-extension packet.
    - The root path remains occupied as a lineage-safe redirect surface during family-first transition.
```

## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `re-homed into DOC as DOC-IID-0001`
- Read now:
  - `DOC-IID-0001`

## Reader Notes

- Historical meaning preserved:
  - GitHub sidebar order is not authoritative when it conflicts with the source-log-owned child ledger.
  - Reordering is allowed only through the bounded canonical reprioritize path, not through ad hoc remove-and-readd mutations.
- Current family-owned successor:
  - `DOC-IID-0001`

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`