# DOC-WORKFLOW-LIFECYCLE-0002 continuity, test retirement, and replacement coverage

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LIFECYCLE
  contract_release: 0002
  contract_id: DOC-WORKFLOW-LIFECYCLE-0002
  record_kind: chronology-first-contract
  status: draft
  release_action: simple-revision
  release_change_summary: Advance the lifecycle family from the first narrow docs-lifecycle release to one later integrated current reader that carries forward legacy continuity clauses while explicitly governing obsolete active-test retirement and mandatory replacement coverage.
  summary: Govern workflow lifecycle boundaries through legacy classification, freeze-versus-migrate discipline, cutover and stub continuity, explicit retirement of obsolete active test suites, retirement-message traceability, and mandatory replacement coverage.
  owner_team: docs-governance
  current_steward: delegated:workflow-lifecycle-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  governance_area: workflow lifecycle, continuity, and obsolete active-surface retirement governance
  applies_to: legacy document classification, Legacy Refs handling, freeze-versus-migrate boundaries, lifecycle cutover, stub preservation, obsolete active test-suite retirement, retirement-message traceability, and replacement-coverage requirements
  enforcement_surface: manual
  violation_semantics: warning
  recorded_at: 2026-04-24
  reviewed_at: pending
  effective_from: 2026-02-17
  effective_until: ongoing
  introduced_by: docs/logs/log-S0C-2A-legacy-integration-suite-retired.md
  last_changed_by: docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md
  source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - docs/logs/log-S0C-2A-legacy-integration-suite-retired.md
  cumulative_source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - GitHub issue #44 (direct support for S0B-3A context; issue-only source)
    - docs/logs/log-S0C-2A-legacy-integration-suite-retired.md
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md
    - docs/logs/support-only/ledger-S0C-2A-legacy-integration-suite-retired.md
    - docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md
    - docs/governance/contracts/workflow/lifecycle/register-DOC-WORKFLOW-LIFECYCLE.md
  lineage:
    supersedes:
      - DOC-WORKFLOW-LIFECYCLE-0001
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This draft keeps the stable DOC-WORKFLOW-LIFECYCLE family and treats 0002 as the later integrated release rather than a broad parent stub.
    - The release carries forward the earlier continuity and cutover clauses from 0001 while introducing explicit test-retirement and replacement-coverage governance from the S0C-2A packet.
    - The broader DOC-WORKFLOW family path remains taxonomy only; this release does not claim one split lineage from DOC-WORKFLOW-0001.
    - S0C-2A still has no logs-family impact; its downstream contribution is lifecycle-family widening, not one amendment to DOC-WORKFLOW-LOGS.
    - Later split is allowed if test-retirement lifecycle becomes independently judgeable from the broader lifecycle reader.
    - effective_from is anchored to the S0C-2A source log creation date 2026-02-17 because this is the release where lifecycle governance first makes test retirement and replacement coverage explicit.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the integrated current-state governance surface for the active `DOC-WORKFLOW-LIFECYCLE-0002` reader, while the source-owned ledgers preserve the route and evidence-history chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day lifecycle contract maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0002-GOV-01` | `contribution-event` | `DOC-WORKFLOW-LIFECYCLE family` | `unknown` | `test-retirement-source-admitted` | `2026-02-17` | `docs/logs/log-S0C-2A-legacy-integration-suite-retired.md` | The `S0C-2A` packet first states the reusable retirement and replacement-coverage rules that the later `0002` release makes explicit. |
| `DOC-WORKFLOW-LIFECYCLE-0002-GOV-02` | `release-opening-verdict-event` | `DOC-WORKFLOW-LIFECYCLE-0002` | `role:packet-reviewer` | `current-release-opened` | `2026-04-24` | `docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md` | `S0G-3G` now fixes the downstream family verdict: `S0C-2A` remains out of the logs family but is strong enough to open a later integrated lifecycle release. |
| `DOC-WORKFLOW-LIFECYCLE-0002-GOV-03` | `family-transition-register-event` | `register-DOC-WORKFLOW-LIFECYCLE` | `role:packet-reviewer` | `current-primary-standing-fixed` | `2026-04-24` | `register-DOC-WORKFLOW-LIFECYCLE.md` | The family-level standing is now explicit: `0002` is first-open now and `0001` remains historical-retained. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-01` | `Do not delete legacy by default` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-01` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Legacy workflow material should not be deleted by default merely because the managed system becomes clearer later. | The earlier continuity rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-02` | `Classify reference and freeze older material` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-02` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Older material should first be handled through explicit classification, reference, and freeze so readers can still locate it without mistaking it for the active body. | The earlier lifecycle staging rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-03` | `Legacy refs keep continuity` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-03` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | `Legacy Refs` or equivalent explicit pointer surfaces should be used when older materials remain historically useful but are no longer the active managed location. | The earlier pointer-surface rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-04` | `Frozen reference is default standing` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-04` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | The default standing of older material is frozen reference, not continued active expansion. | The default-standing clause remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-05` | `Migration on demand only` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-05` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Older material should re-enter the active managed system only through migration-on-demand, such as when the older slice is still high-use, high-risk, or blocking later delivery. | The earlier reactivation rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-06` | `Lifecycle cutover boundary` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-06` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Lifecycle cutover should make the boundary explicit: from the cutover point onward new material enters the new managed system, while older material remains reference-first unless deliberately migrated. | The earlier cutover boundary remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-07` | `Stub preservation keeps entry points readable` | `active` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-07` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | When active material moves, stub preservation should keep older entry points and old links readable enough that readers can still find the current location without treating the old file as the active body. | The earlier continuity-preservation rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-08` | `Logs identity and concrete evidence stay elsewhere` | `active` | `amended` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-08; S0C-2A-R04` | `DOC-WORKFLOW-LIFECYCLE-0001` | `2026-02-12` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `2026-02-17` | `ongoing` | `in-force` | This contract governs lifecycle and continuity boundaries, including explicit retirement of obsolete active surfaces, but it does not own logs-facing identity/front-matter rules and it does not elevate concrete pytest pass counts into primary contract text. | The later release widens lifecycle meaning while keeping log identity and packet-specific evidence outside primary lifecycle clause ownership. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-09` | `Obsolete active suites retire by explicit skip` | `active` | `introduced` | `S0C-2A-R01` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `2026-02-17` | `ongoing` | `in-force` | Obsolete active test suites that depend on deprecated layout or removed APIs should be retired by explicit module-level skip instead of being force-fixed into the current system. | This is the first explicit active-test-retirement clause admitted into the lifecycle family. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-10` | `Retirement message carries reason and governing ref` | `active` | `introduced` | `S0C-2A-R02` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `2026-02-17` | `ongoing` | `in-force` | Retirement-by-skip should carry one explicit skip message that states the retirement reason and links to the governing ADR or log packet. | This is the traceability clause beneath the broader retirement rule. |
| `DOC-WORKFLOW-LIFECYCLE-0002-ST-11` | `Replacement coverage is mandatory` | `active` | `introduced` | `S0C-2A-R03` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `DOC-WORKFLOW-LIFECYCLE-0002` | `2026-02-17` | `2026-02-17` | `ongoing` | `in-force` | Retiring one obsolete active suite must be paired with current-system replacement coverage at the application, repository, or still-live domain-invariant layers. | This is the main protection-net clause admitted from the test-retirement packet. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0002-CH-01` | `DOC-WORKFLOW-LIFECYCLE-0002` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-01; DOC-WORKFLOW-LIFECYCLE-0001-ST-02; DOC-WORKFLOW-LIFECYCLE-0001-ST-03; DOC-WORKFLOW-LIFECYCLE-0001-ST-04` | `DOC-WORKFLOW-LIFECYCLE-0002-ST-01; DOC-WORKFLOW-LIFECYCLE-0002-ST-02; DOC-WORKFLOW-LIFECYCLE-0002-ST-03; DOC-WORKFLOW-LIFECYCLE-0002-ST-04` | `2026-02-12` | `2026-04-24` | The later release keeps the earlier continuity and frozen-reference foundations fully active while broadening the current lifecycle reader around them. | `DOC-WORKFLOW-LIFECYCLE-0001-ST-01; DOC-WORKFLOW-LIFECYCLE-0001-ST-02; DOC-WORKFLOW-LIFECYCLE-0001-ST-03; DOC-WORKFLOW-LIFECYCLE-0001-ST-04` | Carried-forward clauses receive new release-local ids in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-CH-02` | `DOC-WORKFLOW-LIFECYCLE-0002` | `carried-forward` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-05; DOC-WORKFLOW-LIFECYCLE-0001-ST-06; DOC-WORKFLOW-LIFECYCLE-0001-ST-07` | `DOC-WORKFLOW-LIFECYCLE-0002-ST-05; DOC-WORKFLOW-LIFECYCLE-0002-ST-06; DOC-WORKFLOW-LIFECYCLE-0002-ST-07` | `2026-02-12` | `2026-04-24` | The earlier migration, cutover, and stub-preservation rules remain active in the later lifecycle reader. | `DOC-WORKFLOW-LIFECYCLE-0001-ST-05; DOC-WORKFLOW-LIFECYCLE-0001-ST-06; DOC-WORKFLOW-LIFECYCLE-0001-ST-07` | These continuity rules remain materially present in `0002`. |
| `DOC-WORKFLOW-LIFECYCLE-0002-CH-03` | `DOC-WORKFLOW-LIFECYCLE-0002` | `amended` | `DOC-WORKFLOW-LIFECYCLE-0001-ST-08` | `DOC-WORKFLOW-LIFECYCLE-0002-ST-08` | `2026-02-17` | `2026-04-24` | The boundary clause is widened so the lifecycle family can own explicit active-surface retirement while still keeping logs identity and concrete evidence outside primary lifecycle clause ownership. | `DOC-WORKFLOW-LIFECYCLE-0001-ST-08; S0C-2A-R04` | The amendment broadens the family reader without turning it into a broad parent contract. |
| `DOC-WORKFLOW-LIFECYCLE-0002-CH-04` | `DOC-WORKFLOW-LIFECYCLE-0002` | `introduced` | `none` | `DOC-WORKFLOW-LIFECYCLE-0002-ST-09; DOC-WORKFLOW-LIFECYCLE-0002-ST-10` | `2026-02-17` | `2026-04-24` | The `S0C-2A` packet adds an explicit retirement surface that was absent from `0001`. | `S0C-2A-R01; S0C-2A-R02` | This is the first direct test-retirement admission into the lifecycle family. |
| `DOC-WORKFLOW-LIFECYCLE-0002-CH-05` | `DOC-WORKFLOW-LIFECYCLE-0002` | `introduced` | `none` | `DOC-WORKFLOW-LIFECYCLE-0002-ST-11` | `2026-02-17` | `2026-04-24` | The `S0C-2A` packet introduces one explicit replacement-coverage rule so retirement remains tied to current-system protection. | `S0C-2A-R03` | This clause keeps retirement from becoming one unowned coverage gap. |

## Release Change

- This release supersedes `DOC-WORKFLOW-LIFECYCLE-0001` by keeping its earlier continuity, freeze, migration, cutover, and stub-preservation foundations while explicitly governing obsolete active-test retirement through the `S0C-2A` packet.
- The release anchors its own semantic start to the `S0C-2A` source date `2026-02-17`, while still preserving earlier carried-forward clause history from `0001` that began on `2026-02-12`.
- Relative to `0001`, this release now fixes three additional lifecycle points:
  - obsolete active suites should retire by explicit skip rather than force-fitting compatibility back into the current system
  - retirement messaging should keep one explicit reason and governing ADR or log reference
  - replacement coverage is mandatory when one obsolete active suite leaves the gate
- This release intentionally leaves reproducible pytest counts and packet-specific evidence in support-only surfaces rather than admitting them as primary contract clauses.
- This release is one later integrated lifecycle reader, not one broad parent stub; if test-retirement lifecycle later becomes independently judgeable, a later split is allowed from this integrated state.

## Contract Statement

- The tables above now separate current clause state from clause lineage; the readable statement below preserves the same current effective meaning in prose form.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-01`: Legacy workflow material should not be deleted by default merely because the managed system becomes clearer later.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-02`: Older material should first be handled through explicit classification, reference, and freeze so readers can still locate it without mistaking it for the active body.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-03`: `Legacy Refs` or equivalent explicit pointer surfaces should be used when older materials remain historically useful but are no longer the active managed location.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-04`: The default standing of older material is frozen reference, not continued active expansion.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-05`: Older material should re-enter the active managed system only through migration-on-demand.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-06`: Lifecycle cutover should make the boundary explicit: new material enters the new managed system, while older material remains reference-first unless deliberately migrated.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-07`: When active material moves, stub preservation should keep older entry points and old links readable enough that readers can still find the current location without treating the old file as the active body.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-08`: This contract governs lifecycle and continuity boundaries, including explicit retirement of obsolete active surfaces, but it does not own logs-facing identity/front-matter rules and it does not elevate concrete pytest pass counts into primary contract text.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-09`: Obsolete active test suites that depend on deprecated layout or removed APIs should be retired by explicit module-level skip instead of being force-fixed into the current system.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-10`: Retirement-by-skip should carry one explicit skip message that states the retirement reason and links to the governing ADR or log packet.
- `DOC-WORKFLOW-LIFECYCLE-0002-ST-11`: Retiring one obsolete active suite must be paired with current-system replacement coverage at the application, repository, or still-live domain-invariant layers.

## Current Reader Shape

- This file is one later integrated lifecycle reader, not a broad parent contract with child-boundary delegation decisions.
- Read the current clause set here in three layers:
  - `carried-forward`: earlier continuity, freeze, migration, cutover, and stub-preservation clauses from `DOC-WORKFLOW-LIFECYCLE-0001` that remain materially present
  - `amended`: the earlier family-boundary clause restated so active-surface retirement is lifecycle-owned while logs identity and concrete packet evidence remain elsewhere
  - `introduced`: new retirement, traceability, and replacement-coverage clauses admitted from `S0C-2A`
- Under this reader model, the contract does not need one parent-style `Current Boundary Map` because the main question is not which child surface owns the narrow body now; it is how carried-forward, amended, and introduced clauses combine into one current lifecycle reader.

## Current Reading

- Read this release when the question is `what is the current lifecycle-family reader once test retirement and replacement coverage become explicit alongside continuity, freeze, migration, cutover, and stubs?`
- Read `Current Reader Shape` first when the question is `which parts of 0002 are carried forward from 0001, which are amended, and which are newly introduced?`
- Read `DOC-WORKFLOW-LIFECYCLE-0001` only when the reader needs the earlier narrower docs-lifecycle release before active test-retirement governance entered the family current reader.
- Read `register-DOC-WORKFLOW-LIFECYCLE.md` when the question is `which lifecycle-family release should be opened first now and why does 0001 still remain reader-relevant?`
- Read `ledger-S0C-2A-legacy-integration-suite-retired.md` when the question is `which parts of S0C-2A entered 0002 and which parts stayed support-only?`

## Reader Notes

- This draft directly opens the next lifecycle-family release from one strong non-logs packet rather than leaving that packet indefinitely below contract level.
- The mixed current clause set here is deliberate: the release is meant to be one integrated current lifecycle reader, so chronology stays in the evolution table rather than in one second ownership table.
- Concrete pytest outputs remain support-only evidence; only the reusable retirement and replacement-coverage rules enter primary contract meaning here.
- Later split is explicitly allowed if a narrower test-retirement lifecycle family becomes independently judgeable from repeated sources.