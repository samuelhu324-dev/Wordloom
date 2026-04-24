# DOC-WORKFLOW-LOGS-0002 body structure and reader-facing log shape

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LOGS
  contract_release: 0002
  contract_id: DOC-WORKFLOW-LOGS-0002
  record_kind: chronology-first-contract
  status: draft
  release_action: simple-revision
  release_change_summary: Advance the logs family from identity, front matter, and cutover intake only to one current reader that carries those foundations forward while explicitly governing conclusion blocks, top-level lifecycle ownership, and current-effective body structure.
  summary: Govern structured logs through stable workflow identity, log-facing front matter, top-level conclusion blocks, frontmatter-owned lifecycle state, current-effective body prose, and post-cutover intake discipline.
  owner_team: docs-governance
  current_steward: delegated:workflow-logs-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  governance_area: workflow structured log identity, front matter, and reader-facing body-structure governance
  applies_to: structured log ids, titles, log-facing front matter, top-level Decision / Outcome sections, minimum conclusion fields, top-level lifecycle ownership, current-effective body content, and post-cutover structured-log intake
  enforcement_surface: manual
  violation_semantics: warning
  recorded_at: 2026-04-24
  reviewed_at: pending
  effective_from: 2026-02-15
  effective_until: ongoing
  introduced_by: docs/logs/log-S0C-1A-log-extensions.md
  last_changed_by: docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md
  source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - docs/logs/log-S0C-1A-log-extensions.md
  cumulative_source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - GitHub issue #44 (direct support for S0B-3A context; issue-only source)
    - docs/logs/log-S0C-1A-log-extensions.md
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md
    - docs/logs/support-only/ledger-S0C-1A-log-extensions.md
    - docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md
    - docs/governance/contracts/workflow/logs/register-DOC-WORKFLOW-LOGS.md
  lineage:
    supersedes:
      - DOC-WORKFLOW-LOGS-0001
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This draft keeps the stable DOC-WORKFLOW-LOGS family and treats 0002 as the later effective release state.
    - The release carries forward the earlier identity and intake foundations from 0001 while making the reader-facing body structure explicit through the S0C-1A source packet.
    - This local opening is direct from the first explicit post-cutover body-structure packet rather than from repeated corroborating samples; later samples may still sharpen or split later logs-family releases.
    - The broader DOC-WORKFLOW family path remains taxonomy only; this release does not claim one split lineage from DOC-WORKFLOW-0001.
    - effective_from is anchored to the S0C-1A source log creation date 2026-02-15 because this is the release where body-structure governance first becomes explicit in the logs family.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through owner_team, current_steward, approval_state, reviewed_by, and approved_by.
- Older fields such as introduced_by, last_changed_by, source_refs, and cumulative_source_refs remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the narrow current-state governance surface for the active DOC-WORKFLOW-LOGS-0002 reader, while the parent ledgers preserve the route and evidence-history chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day logs contract maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0002-GOV-01` | `contribution-event` | `DOC-WORKFLOW-LOGS family` | `unknown` | `body-structure-source-admitted` | `2026-02-15` | `docs/logs/log-S0C-1A-log-extensions.md` | The `S0C-1A` source first states the reusable body-structure rules that the later `0002` release makes explicit. |
| `DOC-WORKFLOW-LOGS-0002-GOV-02` | `release-opening-verdict-event` | `DOC-WORKFLOW-LOGS-0002` | `role:packet-reviewer` | `current-release-opened` | `2026-04-24` | `docs/logs/log-S0G-3G-logs-body-structure-extraction-and-logs-0002-opening-governance.md` | `S0G-3G` now fixes the direct-opening verdict and emits the next logs-family release without waiting for a second corroborating sample. |
| `DOC-WORKFLOW-LOGS-0002-GOV-03` | `family-transition-register-event` | `register-DOC-WORKFLOW-LOGS` | `role:packet-reviewer` | `current-primary-standing-fixed` | `2026-04-24` | `register-DOC-WORKFLOW-LOGS.md` | The family-level standing is now explicit: `0002` is first-open now and `0001` remains historical-retained. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0002-ST-01` | `Stable structured log identifier` | `active` | `carried-forward` | `DOC-WORKFLOW-LOGS-0001-ST-01` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Structured logs must use one stable workflow identifier pattern that expresses delivery/topic identity without binding that identity to directory layout or chronology. | The identity rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LOGS-0002-ST-02` | `Identity visible in titles and indices` | `active` | `carried-forward` | `DOC-WORKFLOW-LOGS-0001-ST-02` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Log titles and index-facing log references should expose that stable identity clearly enough that readers can recognize the governed topic without reconstructing meaning from file placement alone. | The title/index readability rule remains materially present in `0002`. |
| `DOC-WORKFLOW-LOGS-0002-ST-03` | `Mechanically managed front matter` | `active` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-03; S0C-1A-R03` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | Structured logs should carry one mechanically managed front matter surface for lifecycle state and navigation metadata rather than scattering those signals through freeform body prose. | The later release narrows front matter to lifecycle-and-navigation ownership while body structure becomes explicit below. |
| `DOC-WORKFLOW-LOGS-0002-ST-04` | `Minimum log-facing front matter fields` | `active` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-04; S0C-1A-R03` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | The logs-facing front matter should at least keep stable id, kind, human-readable title, status, scope, low-cardinality tags, preserved links, and created plus updated audit fields. | The later release keeps the field floor while clarifying that body structure is no longer hidden inside front-matter ownership. |
| `DOC-WORKFLOW-LOGS-0002-ST-05` | `Top-level Decision / Outcome section` | `active` | `introduced` | `S0C-1A-R01` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | Structured logs should expose one top-level Decision / Outcome section so readers can identify the current decision state without reconstructing it from later body prose. | This is the first explicit body-structure clause admitted into the logs family. |
| `DOC-WORKFLOW-LOGS-0002-ST-06` | `Minimum conclusion fields` | `active` | `introduced` | `S0C-1A-R02` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | That conclusion surface should at least keep Decision, Drivers, Non-goals, and Success criteria as the stable minimum handoff fields. | This is the structured child detail beneath the broader conclusion-surface rule. |
| `DOC-WORKFLOW-LOGS-0002-ST-07` | `Top-level status ownership` | `active` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-03; DOC-WORKFLOW-LOGS-0001-ST-04; DOC-WORKFLOW-LOGS-0001-ST-06; S0C-1A-R03` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | Top-level front matter status should own log lifecycle state instead of repeating draft, stable, or archived timelines across body sections. | This clause makes the earlier frontmatter/body boundary explicit as one reader-facing rule. |
| `DOC-WORKFLOW-LOGS-0002-ST-08` | `Current-effective body content` | `active` | `introduced` | `S0C-1A-R04` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | Log bodies should preserve current effective content, while historical drift should normally leave through git history, legacy, or stub paths rather than remain as multi-timeline prose. | This is the clearest long-lived maintenance discipline admitted by the body-structure packet. |
| `DOC-WORKFLOW-LOGS-0002-ST-09` | `Cutover intake discipline` | `active` | `carried-forward` | `DOC-WORKFLOW-LOGS-0001-ST-05` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | From the cutover boundary onward, new structured log content must enter the system under the stable identifier, front matter, and current reader discipline rather than continuing older unmanaged intake habits. | The intake clause remains materially present in `0002`. |
| `DOC-WORKFLOW-LOGS-0002-ST-10` | `Lifecycle semantics stay elsewhere` | `active` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-06; S0C-1A-R03; S0C-1A-R04` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0002` | `2026-02-15` | `2026-02-15` | `ongoing` | `in-force` | This contract governs log identity, front matter, and reader-facing body structure only; it does not by itself decide how legacy material is frozen, migrated on demand, or preserved through stubs. | The later release keeps lifecycle-boundary routing while updating what the logs family now explicitly owns. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0002-CH-01` | `DOC-WORKFLOW-LOGS-0002` | `carried-forward` | `DOC-WORKFLOW-LOGS-0001-ST-01; DOC-WORKFLOW-LOGS-0001-ST-02` | `DOC-WORKFLOW-LOGS-0002-ST-01; DOC-WORKFLOW-LOGS-0002-ST-02` | `2026-02-12` | `2026-04-24` | The later release keeps the earlier identity foundations fully active while broadening the family reader around them. | `DOC-WORKFLOW-LOGS-0001-ST-01; DOC-WORKFLOW-LOGS-0001-ST-02` | Carried-forward clauses receive new release-local ids in `0002`. |
| `DOC-WORKFLOW-LOGS-0002-CH-02` | `DOC-WORKFLOW-LOGS-0002` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-03; DOC-WORKFLOW-LOGS-0001-ST-04` | `DOC-WORKFLOW-LOGS-0002-ST-03; DOC-WORKFLOW-LOGS-0002-ST-04` | `2026-02-15` | `2026-04-24` | The later release narrows front-matter ownership to lifecycle and navigation now that reader-facing body structure is governed explicitly. | `DOC-WORKFLOW-LOGS-0001-ST-03; DOC-WORKFLOW-LOGS-0001-ST-04; S0C-1A-R03` | The amendment keeps the front-matter floor while changing the family boundary. |
| `DOC-WORKFLOW-LOGS-0002-CH-03` | `DOC-WORKFLOW-LOGS-0002` | `introduced` | `none` | `DOC-WORKFLOW-LOGS-0002-ST-05; DOC-WORKFLOW-LOGS-0002-ST-06` | `2026-02-15` | `2026-04-24` | The S0C-1A packet adds an explicit conclusion-block surface that was absent from `0001`. | `S0C-1A-R01; S0C-1A-R02` | This is the first direct body-structure admission into the logs family. |
| `DOC-WORKFLOW-LOGS-0002-CH-04` | `DOC-WORKFLOW-LOGS-0002` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-03; DOC-WORKFLOW-LOGS-0001-ST-04; DOC-WORKFLOW-LOGS-0001-ST-06` | `DOC-WORKFLOW-LOGS-0002-ST-07` | `2026-02-15` | `2026-04-24` | The later release makes top-level status ownership explicit instead of leaving that boundary implied inside broader front-matter wording. | `S0C-1A-R03` | This is the main boundary-amendment clause admitted from the first sample. |
| `DOC-WORKFLOW-LOGS-0002-CH-05` | `DOC-WORKFLOW-LOGS-0002` | `introduced` | `none` | `DOC-WORKFLOW-LOGS-0002-ST-08` | `2026-02-15` | `2026-04-24` | The S0C-1A packet introduces one explicit current-effective body discipline that was not spelled out in `0001`. | `S0C-1A-R04` | This clause makes the body-retention rule independently reviewable. |
| `DOC-WORKFLOW-LOGS-0002-CH-06` | `DOC-WORKFLOW-LOGS-0002` | `carried-forward` | `DOC-WORKFLOW-LOGS-0001-ST-05` | `DOC-WORKFLOW-LOGS-0002-ST-09` | `2026-02-12` | `2026-04-24` | The cutover-intake rule remains active in the later reader and does not need a new source packet to stay in force. | `DOC-WORKFLOW-LOGS-0001-ST-05` | This keeps new log intake bound to the managed system. |
| `DOC-WORKFLOW-LOGS-0002-CH-07` | `DOC-WORKFLOW-LOGS-0002` | `amended` | `DOC-WORKFLOW-LOGS-0001-ST-06` | `DOC-WORKFLOW-LOGS-0002-ST-10` | `2026-02-15` | `2026-04-24` | The lifecycle-boundary clause is updated so the logs family now owns explicit body structure while legacy freeze, migration, and stub semantics still remain elsewhere. | `DOC-WORKFLOW-LOGS-0001-ST-06; S0C-1A-R03; S0C-1A-R04` | The family boundary is widened but not collapsed into lifecycle routing. |

## Release Change

- This release supersedes `DOC-WORKFLOW-LOGS-0001` by keeping its earlier identity, front-matter, and intake foundations while explicitly governing the reader-facing log body shape through the `S0C-1A` packet.
- The release anchors its own semantic start to the `S0C-1A` source date `2026-02-15`, while still preserving earlier carried-forward clause history from `0001` that began on `2026-02-12`.
- Relative to `0001`, this release now fixes four additional points:
  - structured logs should expose one top-level Decision / Outcome section
  - that conclusion block should keep one stable minimum field set
  - top-level front matter status should own lifecycle state without per-section body repetition
  - the body should preserve current effective content while historical drift leaves through git, legacy, or stub paths
- This release directly opens from the first explicit post-cutover body-structure packet rather than waiting for a second corroborating sample before any later logs-family release exists.
- This release intentionally keeps template snippets and applied examples outside primary contract meaning; those remain support-only evidence in the source packet and ledger.

## Contract Statement

- The tables above now separate current clause state from clause lineage; the readable statement below preserves the same current effective meaning in prose form.
- `DOC-WORKFLOW-LOGS-0002-ST-01`: Structured logs must use one stable workflow identifier pattern that expresses delivery/topic identity without binding that identity to directory layout or chronology.
- `DOC-WORKFLOW-LOGS-0002-ST-02`: Log titles and index-facing log references should expose that stable identity clearly enough that readers can recognize the governed topic without reconstructing meaning from file placement alone.
- `DOC-WORKFLOW-LOGS-0002-ST-03`: Structured logs should carry one mechanically managed front matter surface for lifecycle state and navigation metadata rather than scattering those signals through freeform body prose.
- `DOC-WORKFLOW-LOGS-0002-ST-04`: That front matter should at least keep stable id, kind, title, status, scope, low-cardinality tags, preserved links, and created plus updated audit fields.
- `DOC-WORKFLOW-LOGS-0002-ST-05`: Structured logs should expose one top-level Decision / Outcome section so readers can identify the current decision state quickly.
- `DOC-WORKFLOW-LOGS-0002-ST-06`: That conclusion surface should at least keep Decision, Drivers, Non-goals, and Success criteria.
- `DOC-WORKFLOW-LOGS-0002-ST-07`: Top-level front matter status should own lifecycle state instead of repeating draft, stable, or archived timelines through body sections.
- `DOC-WORKFLOW-LOGS-0002-ST-08`: Log bodies should preserve current effective content, while historical drift should normally leave through git history, legacy, or stub paths rather than remain as multi-timeline prose.
- `DOC-WORKFLOW-LOGS-0002-ST-09`: From the cutover boundary onward, new structured log content must enter the system under the stable identifier, front matter, and current reader discipline rather than through older unmanaged intake habits.
- `DOC-WORKFLOW-LOGS-0002-ST-10`: This contract governs log identity, front matter, and reader-facing body structure only; it does not by itself decide how legacy material is frozen, migrated on demand, or preserved through stubs.

## Current Reader Shape

- This file is one narrow current logs-family reader, not a broad parent contract with child-boundary delegation decisions.
- Read the current clause set here in three layers:
  - `carried-forward`: earlier identity and intake clauses from `DOC-WORKFLOW-LOGS-0001` that remain materially present in the current release
  - `amended`: earlier frontmatter and lifecycle-boundary clauses that are restated now that body structure is explicit
  - `introduced`: new conclusion-block and current-effective-body clauses admitted from `S0C-1A`
- Under this reader model, the contract does not need one parent-style Current Boundary Map because the main question is not which child surface owns the narrow body now; it is how carried-forward, amended, and introduced clauses combine into one current logs reader.

## Current Reading

- Read this release when the question is `what is the current logs-family reader once body structure is explicitly governed alongside identity, front matter, and intake?`
- Read `Current Reader Shape` first when the question is `which parts of 0002 are carried forward from 0001, which are amended, and which are newly introduced?`
- Read `DOC-WORKFLOW-LOGS-0001` only when the reader needs the narrower earlier release before body-structure governance was made explicit.
- Read `register-DOC-WORKFLOW-LOGS.md` when the question is `which logs-family release should be opened first now and why does 0001 still remain reader-relevant?`
- Read `ledger-S0C-1A-log-extensions.md` when the question is `which parts of S0C-1A entered 0002 and which parts stayed support-only?`

## Reader Notes

- This draft directly opens the next logs-family release from the first explicit body-structure packet rather than waiting for corroborating samples to force that family evolution later.
- The mixed current clause set here is deliberate: the release is meant to be one integrated current logs reader, so chronology stays in the evolution table rather than in one second ownership table.
- Template snippets and applied examples are intentionally left out of release-local contract meaning; they remain support-only unless a later release admits them through repeated evidence.
- The statement ids in this file are intentionally release-local `0002-ST-*` ids; earlier `0001-ST-*` ids remain history anchors in the statement-evolution table rather than being reused as the current ids.