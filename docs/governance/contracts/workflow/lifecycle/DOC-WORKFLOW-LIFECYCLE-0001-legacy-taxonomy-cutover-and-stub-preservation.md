# DOC-WORKFLOW-LIFECYCLE-0001 legacy taxonomy cutover and stub preservation

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LIFECYCLE
  contract_release: 0001
  contract_id: DOC-WORKFLOW-LIFECYCLE-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first lifecycle-oriented child release from S0B-3A by extracting legacy taxonomy, freeze-versus-migrate boundaries, lifecycle cutover, and stub preservation into one dedicated workflow family.
  summary: Govern documentation lifecycle boundaries through explicit legacy taxonomy, default freeze of older material, migration-on-demand, lifecycle cutover, and stub preservation so older content can remain findable without staying active by default.
  governance_area: workflow documentation lifecycle and legacy management governance
  applies_to: legacy document classification, Legacy Refs handling, freeze-versus-migrate boundaries, lifecycle cutover, and stub preservation across moved workflow materials
  enforcement_surface: manual
  violation_semantics: warning
  introduced_by: docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
  last_changed_by: docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
  source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - GitHub issue #44 (direct support for S0B-3A context; issue-only source)
  cumulative_source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - GitHub issue #44 (direct support for S0B-3A context; issue-only source)
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This draft is the first narrow lifecycle-oriented extraction from the mixed S0B-3A source packet rather than one already-generalized workflow parent release.
    - The broader DOC-WORKFLOW family path remains taxonomy only; this record does not claim split lineage from DOC-WORKFLOW-0001.
    - The contract intentionally keeps the lifecycle side of cutover separate from the logs-intake side, which is routed to DOC-WORKFLOW-LOGS-0001 through the same-source ledger split.
    - The older S0B-2A mixed source is retained as supporting evidence because its legacy and cutover pressure may later be re-routed into this family, but this first release is still owned directly by S0B-3A.
```

## Release Change

- This release establishes the first lifecycle-oriented child family extracted from `S0B-3A`.
- The release isolates the lifecycle body that had been mixed with log identity and front matter inside the broader source packet:
  - explicit legacy taxonomy and `Legacy Refs` handling
  - default freeze of older material rather than immediate rewrite or deletion
  - migration-on-demand as the rule for reactivating older material
  - the lifecycle half of cutover, which marks how older material leaves the active path and how newer managed material takes over
  - stub preservation so moved material remains discoverable without pretending the old location is still the active body
- This release intentionally does not absorb the logs-facing identifier and front matter intake rules; those remain reserved for `DOC-WORKFLOW-LOGS-0001`.

## Contract Statement

- Legacy workflow material should not be deleted by default merely because the managed system becomes clearer later.
- Older material should first be handled through explicit classification, reference, and freeze so readers can still locate it without mistaking it for the active body.
- `Legacy Refs` or equivalent explicit pointer surfaces should be used when older materials remain historically useful but are no longer the active managed location.
- The default standing of older material is frozen reference, not continued active expansion.
- Older material should re-enter the active managed system only through migration-on-demand, such as when the older slice is still high-use, high-risk, or blocking later delivery.
- Lifecycle cutover should make the boundary explicit:
  - from the cutover point onward, new material enters the new managed system
  - older material remains reference-first unless deliberately migrated
- When active material moves, stub preservation should keep older entry points and old links readable enough that readers can still find the current location without treating the old file as the active body.
- This contract governs lifecycle and continuity boundaries only; it does not own the logs-facing title and front matter intake rules that route new structured log content into the managed system.

## Current Reading

- Read this release when the question is `what is the first narrow workflow rule for classifying legacy material, freezing it by default, migrating it on demand, and preserving continuity through cutover and stubs?`
- Read the `S0B-3A` ledger when the question is `which parts of S0B-3A entered this lifecycle family and which parts were routed elsewhere?`
- Read `S0B-2A` only when you need the earlier nearby pressure that later may justify extending lifecycle governance beyond this first child release.

## Reader Notes

- This draft is intentionally the first narrow lifecycle extraction, not the final wider owner of every later historical view, observability migration, or archaeology flow that may eventually reuse similar lifecycle logic.
- If later sources prove that lifecycle governance spans additional workflow kinds strongly enough, that widening should happen through a later release or broader family synthesis rather than by retroactively pretending this first release was already fully general.