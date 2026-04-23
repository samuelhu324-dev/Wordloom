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
  owner_team: docs-governance
  current_steward: delegated:workflow-lifecycle-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  governance_area: workflow documentation lifecycle and legacy management governance
  applies_to: legacy document classification, Legacy Refs handling, freeze-versus-migrate boundaries, lifecycle cutover, and stub preservation across moved workflow materials
  enforcement_surface: manual
  violation_semantics: warning
  recorded_at: 2026-04-10
  reviewed_at: pending
  effective_from: 2026-02-12
  effective_until: ongoing
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
    - `effective_from` is anchored to the source log creation date `2026-02-12` because the repaired `S0B-3A` parent ledger now defends that day-level source chronology for the lifecycle-facing legacy-taxonomy, cutover-boundary, and stub-preservation rows.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the narrow current-state governance surface for the active `DOC-WORKFLOW-LIFECYCLE-0001` reader, while the parent ledger preserves the mixed-family route and governance-event chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day lifecycle contract maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-LIFECYCLE-0001` | `unknown` | `family-introduced` | `2026-02-12` | `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md` | The original lifecycle-facing source introduced the child release on the source log creation date, but it does not defend a named current steward or approver for the current contract state. |
| `DOC-WORKFLOW-LIFECYCLE-0001-GOV-02` | `delegated-stewardship-event` | `DOC-WORKFLOW-LIFECYCLE-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | Stewardship for the current lifecycle contract reader is now explicitly delegated to the narrower lifecycle contract maintainer role while final approval remains with the broader docs-governance approver role. |
| `DOC-WORKFLOW-LIFECYCLE-0001-GOV-03` | `review-approval-separation-event` | `DOC-WORKFLOW-LIFECYCLE-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit or collapsed into one reviewer identity. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-01` | `Do not delete legacy by default` | `active` | `introduced` | `S0B-3A-R03` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Legacy workflow material should not be deleted by default merely because the managed system becomes clearer later. | First lifecycle clause anchored to the legacy-taxonomy row. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-02` | `Classify reference and freeze older material` | `active` | `introduced` | `S0B-3A-R03` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Older material should first be handled through explicit classification, reference, and freeze so readers can still locate it without mistaking it for the active body. | Keeps the first lifecycle management step explicit rather than implied through examples only. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-03` | `Legacy refs keep continuity` | `active` | `introduced` | `S0B-3A-R03` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | `Legacy Refs` or equivalent explicit pointer surfaces should be used when older materials remain historically useful but are no longer the active managed location. | Pointer-surface clause kept separate for clearer reader auditing. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-04` | `Frozen reference is default standing` | `active` | `introduced` | `S0B-3A-R03` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | The default standing of older material is frozen reference, not continued active expansion. | The default-standing clause is split out because it governs lifecycle stance rather than navigation alone. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-05` | `Migration on demand only` | `active` | `introduced` | `S0B-3A-R05` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Older material should re-enter the active managed system only through migration-on-demand, such as when the older slice is still high-use, high-risk, or blocking later delivery. | This clause owns the lifecycle-boundary half of cutover rather than the logs-intake half. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-06` | `Lifecycle cutover boundary` | `active` | `introduced` | `S0B-3A-R05` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Lifecycle cutover should make the boundary explicit: from the cutover point onward new material enters the new managed system, while older material remains reference-first unless deliberately migrated. | Keeps lifecycle cutover explicit without repeating logs-intake semantics. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-07` | `Stub preservation keeps entry points readable` | `active` | `introduced` | `S0B-3A-R06` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | When active material moves, stub preservation should keep older entry points and old links readable enough that readers can still find the current location without treating the old file as the active body. | This clause isolates continuity-preservation from general legacy taxonomy. |
| `DOC-WORKFLOW-LIFECYCLE-0001-ST-08` | `Logs intake stays elsewhere` | `active` | `introduced` | `S0B-3A-R04; S0B-3A-R05; S0B-3A-R06` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | This contract governs lifecycle and continuity boundaries only; it does not own the logs-facing title and front matter intake rules that route new structured log content into the managed system. | Boundary clause keeps intake semantics routed to `DOC-WORKFLOW-LOGS-0001`. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0001-CH-01` | `DOC-WORKFLOW-LIFECYCLE-0001` | `introduced` | `none` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-01; DOC-WORKFLOW-LIFECYCLE-0001-ST-02; DOC-WORKFLOW-LIFECYCLE-0001-ST-03; DOC-WORKFLOW-LIFECYCLE-0001-ST-04; DOC-WORKFLOW-LIFECYCLE-0001-ST-05; DOC-WORKFLOW-LIFECYCLE-0001-ST-06; DOC-WORKFLOW-LIFECYCLE-0001-ST-07; DOC-WORKFLOW-LIFECYCLE-0001-ST-08` | `2026-02-12` | `2026-04-10` | The first lifecycle child release is being aligned to the current chronology-first clause model so legacy-taxonomy, cutover, and stub-preservation ownership remain reviewable against the repaired S0B-3A ledger. | `S0B-3A-R03; S0B-3A-R04; S0B-3A-R05; S0B-3A-R06` | The release meaning is unchanged; the repair only makes chronology and clause identity explicit. |

## Release Change

- This release establishes the first lifecycle-oriented child family extracted from `S0B-3A`.
- The semantic start of this release is now anchored to the source log creation date `2026-02-12`, while the release record itself entered repo chronology later on `2026-04-10`.
- The release isolates the lifecycle body that had been mixed with log identity and front matter inside the broader source packet:
  - explicit legacy taxonomy and `Legacy Refs` handling
  - default freeze of older material rather than immediate rewrite or deletion
  - migration-on-demand as the rule for reactivating older material
  - the lifecycle half of cutover, which marks how older material leaves the active path and how newer managed material takes over
  - stub preservation so moved material remains discoverable without pretending the old location is still the active body
- This release intentionally does not absorb the logs-facing identifier and front matter intake rules; those remain reserved for `DOC-WORKFLOW-LOGS-0001`.

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-01`: Legacy workflow material should not be deleted by default merely because the managed system becomes clearer later.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-02`: Older material should first be handled through explicit classification, reference, and freeze so readers can still locate it without mistaking it for the active body.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-03`: `Legacy Refs` or equivalent explicit pointer surfaces should be used when older materials remain historically useful but are no longer the active managed location.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-04`: The default standing of older material is frozen reference, not continued active expansion.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-05`: Older material should re-enter the active managed system only through migration-on-demand, such as when the older slice is still high-use, high-risk, or blocking later delivery.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-06`: Lifecycle cutover should make the boundary explicit:
  - from the cutover point onward, new material enters the new managed system
  - older material remains reference-first unless deliberately migrated
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-07`: When active material moves, stub preservation should keep older entry points and old links readable enough that readers can still find the current location without treating the old file as the active body.
- `DOC-WORKFLOW-LIFECYCLE-0001-ST-08`: This contract governs lifecycle and continuity boundaries only; it does not own the logs-facing title and front matter intake rules that route new structured log content into the managed system.

## Current Reading

- Read this release when the question is `what is the first narrow workflow rule for classifying legacy material, freezing it by default, migrating it on demand, and preserving continuity through cutover and stubs?`
- Read the `S0B-3A` ledger when the question is `which parts of S0B-3A entered this lifecycle family and which parts were routed elsewhere?`
- Read `S0B-2A` only when you need the earlier nearby pressure that later may justify extending lifecycle governance beyond this first child release.

## Reader Notes

- This draft is intentionally the first narrow lifecycle extraction, not the final wider owner of every later historical view, observability migration, or archaeology flow that may eventually reuse similar lifecycle logic.
- If later sources prove that lifecycle governance spans additional workflow kinds strongly enough, that widening should happen through a later release or broader family synthesis rather than by retroactively pretending this first release was already fully general.
- The file now uses the current chronology-first clause registry model while preserving the same first child release meaning.