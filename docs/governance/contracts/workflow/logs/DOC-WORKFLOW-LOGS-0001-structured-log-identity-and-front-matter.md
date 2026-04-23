# DOC-WORKFLOW-LOGS-0001 structured log identity and front matter

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LOGS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-LOGS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first logs-oriented child release from S0B-3A by extracting the narrow workflow rule for stable structured log identity, log-facing front matter, and cutover-based intake discipline.
  summary: Govern structured logs through stable workflow identifiers, logs-facing front matter, and one cutover rule that requires new log content to enter the managed system under the new identifier and metadata discipline.
  owner_team: docs-governance
  current_steward: delegated:workflow-logs-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  governance_area: workflow structured log identity and front matter governance
  applies_to: structured log ids, log titles, log-facing front matter fields, index-facing log identity, and new structured log intake after the cutover boundary
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
    - docs/governance/contracts/workflow/legacy logs/DOC-WORKFLOW-LEGACY-LOGS-0001-earliest-structured-logs-capability-thesis-and-numbered-rule-blocks.md
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
  lineage:
    supersedes:
      - DOC-WORKFLOW-LEGACY-LOGS-0001
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This draft is the first narrow logs-oriented extraction from the mixed S0B-3A source packet rather than one already-generalized workflow parent release.
    - The broader DOC-WORKFLOW family path remains taxonomy only; this record does not claim split lineage from DOC-WORKFLOW-0001.
    - Front matter is intentionally kept narrow here on first extraction, while later parent or sibling-spanning widening remains explicitly reserved if repeated evidence justifies it.
    - DOC-WORKFLOW-LEGACY-LOGS-0001 is now retained as predecessor context for the earliest historical structured-log reader shape, and this current logs-family reader now records the reciprocal `supersedes` back-link without claiming that the earlier clause body was absorbed here.
    - `effective_from` is anchored to the source log creation date `2026-02-12` because the repaired `S0B-3A` parent ledger now defends that day-level source chronology for the logs-facing identifier, front-matter, and cutover-intake rows.
```

## Legacy Reader Bridge

- Earlier historical reader:
  - `DOC-WORKFLOW-LEGACY-LOGS-0001`
- Current reader standing:
  - `DOC-WORKFLOW-LOGS-0001` remains the active logs-family contract surface
- Bridge rule:
  - read `DOC-WORKFLOW-LEGACY-LOGS-0001` for the earliest historical structured-log reader shape
  - read `DOC-WORKFLOW-LOGS-0001` for the current logs-facing rule on identity, front matter, and cutover intake
  - do not read this bridge as `absorbed_from`, clause carry-forward, or family renumbering

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the narrow current-state governance surface for the active `DOC-WORKFLOW-LOGS-0001` reader, while the parent ledger preserves the mixed-family route and governance-event chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day logs contract maintenance distinct from durable family ownership.
- The earlier historical reader for the earliest structured-log shape is now preserved separately at `DOC-WORKFLOW-LEGACY-LOGS-0001`; this file remains current without claiming that the earlier clause body was absorbed here.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-LOGS-0001` | `unknown` | `family-introduced` | `2026-02-12` | `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md` | The original logs-facing source introduced the child release on the source log creation date, but it does not defend a named current steward or approver for the current contract state. |
| `DOC-WORKFLOW-LOGS-0001-GOV-02` | `delegated-stewardship-event` | `DOC-WORKFLOW-LOGS-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | Stewardship for the current logs contract reader is now explicitly delegated to the narrower logs contract maintainer role while final approval remains with the broader docs-governance approver role. |
| `DOC-WORKFLOW-LOGS-0001-GOV-03` | `review-approval-separation-event` | `DOC-WORKFLOW-LOGS-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-15` | `S0F-9A/P4 second-cycle round` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit or collapsed into one reviewer identity. |
| `DOC-WORKFLOW-LOGS-0001-GOV-04` | `historical-reader-bridge-event` | `DOC-WORKFLOW-LOGS-0001` | `role:packet-reviewer` | `predecessor-context-linked` | `2026-04-22` | `ledger-SUP-S0A-2A-004-legacy-logs-earliest-structured-shape.md; DOC-WORKFLOW-LEGACY-LOGS-0001` | The current logs-family reader now points back to the earlier historical legacy reader as predecessor context only, without implying clause absorption or renumbered family lineage. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0001-ST-01` | `Stable structured log identifier` | `active` | `introduced` | `S0B-3A-R01` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Structured logs must use one stable workflow identifier pattern that expresses delivery/topic identity without binding that identity to directory layout or chronology. | Earliest logs-facing identifier clause extracted from the S0B-3A ledger. |
| `DOC-WORKFLOW-LOGS-0001-ST-02` | `Identity visible in titles and indices` | `active` | `introduced` | `S0B-3A-R01` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Log titles and index-facing log references should expose that stable identity clearly enough that readers can recognize the governed topic without reconstructing meaning from file placement alone. | Keeps title and index readability tied to the same identifier basis. |
| `DOC-WORKFLOW-LOGS-0001-ST-03` | `Mechanically managed front matter` | `active` | `introduced` | `S0B-3A-R02` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | Structured logs should carry one mechanically managed front matter surface rather than scattering status, scope, links, and audit metadata through freeform prose. | Front-matter ownership stays narrow to the logs-facing surface in this first child release. |
| `DOC-WORKFLOW-LOGS-0001-ST-04` | `Minimum log-facing fields` | `active` | `introduced` | `S0B-3A-R02` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | The logs-facing front matter should at least keep the fields that make structured logs navigable and mechanically readable, such as stable `id`, `kind`, human-readable `title`, `status`, `scope`, low-cardinality `tags`, preserved link fields, and `created` plus `updated` audit fields. | This keeps the field list explicit without widening the contract into every possible future metadata surface. |
| `DOC-WORKFLOW-LOGS-0001-ST-05` | `Cutover intake discipline` | `active` | `introduced` | `S0B-3A-R04` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | From the cutover boundary onward, new structured log content must enter the system under the new identifier and front matter discipline rather than continuing the older unmanaged intake habits. | This clause owns only the logs-intake half of the same-source cutover split. |
| `DOC-WORKFLOW-LOGS-0001-ST-06` | `Lifecycle semantics stay elsewhere` | `active` | `introduced` | `S0B-3A-R04; S0B-3A-R05; S0B-3A-R06` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `DOC-WORKFLOW-LOGS-0001` | `2026-02-12` | `2026-02-12` | `ongoing` | `in-force` | This contract governs the logs-facing intake and identity body only; it does not by itself decide how legacy material is frozen, migrated on demand, or preserved through stubs. | The boundary clause keeps lifecycle semantics routed to `DOC-WORKFLOW-LIFECYCLE-0001`. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0001-CH-01` | `DOC-WORKFLOW-LOGS-0001` | `introduced` | `none` | `DOC-WORKFLOW-LOGS-0001-ST-01; DOC-WORKFLOW-LOGS-0001-ST-02; DOC-WORKFLOW-LOGS-0001-ST-03; DOC-WORKFLOW-LOGS-0001-ST-04; DOC-WORKFLOW-LOGS-0001-ST-05; DOC-WORKFLOW-LOGS-0001-ST-06` | `2026-02-12` | `2026-04-10` | The first logs child release is being aligned to the current chronology-first clause model so identifier, front-matter, and cutover-intake ownership remain reviewable against the repaired S0B-3A ledger. | `S0B-3A-R01; S0B-3A-R02; S0B-3A-R04; S0B-3A-R05; S0B-3A-R06` | The release meaning is unchanged; the repair only makes clause identity and chronology explicit. |

## Release Change

- This release establishes the first logs-oriented child family extracted from `S0B-3A`.
- The semantic start of this release is now anchored to the source log creation date `2026-02-12`, while the release record itself entered repo chronology later on `2026-04-10`.
- The release isolates three rule surfaces that were previously mixed together inside the broader source packet:
  - stable workflow identifiers as they appear in structured log titles and index-facing log identity
  - logs-facing front matter as the mechanically managed metadata surface for logs
  - the logs-intake half of cutover, which requires new structured log content to enter the managed system under the new identifier and metadata discipline
- This release intentionally does not absorb legacy taxonomy, stub preservation, or lifecycle-boundary cutover semantics; those remain reserved for `DOC-WORKFLOW-LIFECYCLE-0001`.

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-LOGS-0001-ST-01`: Structured logs must use one stable workflow identifier pattern that expresses delivery/topic identity without binding that identity to directory layout or chronology.
- `DOC-WORKFLOW-LOGS-0001-ST-02`: Log titles and index-facing log references should expose that stable identity clearly enough that readers can recognize the governed topic without reconstructing meaning from file placement alone.
- `DOC-WORKFLOW-LOGS-0001-ST-03`: Structured logs should carry one mechanically managed front matter surface rather than scattering status, scope, links, and audit metadata through freeform prose.
- `DOC-WORKFLOW-LOGS-0001-ST-04`: The logs-facing front matter should at least keep the fields that make structured logs navigable and mechanically readable, such as:
  - stable `id`
  - `kind`
  - human-readable `title`
  - `status`
  - `scope`
  - low-cardinality `tags`
  - link fields that preserve issue, PR, ADR, runbook, or nearby context anchors
  - `created` and `updated` audit fields
- `DOC-WORKFLOW-LOGS-0001-ST-05`: From the cutover boundary onward, new structured log content must enter the system under the new identifier and front matter discipline rather than continuing the older unmanaged intake habits.
- `DOC-WORKFLOW-LOGS-0001-ST-06`: This contract governs the logs-facing intake and identity body only; it does not by itself decide how legacy material is frozen, migrated on demand, or preserved through stubs.

## Current Reading

- Read this release when the question is `what is the first narrow workflow rule for structured log identity, log-facing front matter, and post-cutover logs intake?`
- Read `DOC-WORKFLOW-LEGACY-LOGS-0001` first when the question is `what was the earlier historical structured-log reader shape before this current logs-family rule existed?`
- Read the `S0B-3A` ledger when the question is `which parts of S0B-3A entered this logs family and which parts were routed elsewhere?`
- Read the broader workflow family only when the question is about the higher-level workflow path rather than this specific logs-facing rule body.

## Reader Notes

- This draft is intentionally narrower than any eventual generalized parent surface that might later synthesize identifier or front-matter meaning across logs, labs, runbooks, ADRs, or other workflow children.
- It is the first candidate owner of the earliest explicit logs-facing wording, not the final owner of every later cross-kind reuse of the same concepts.
- Its new bridge to `DOC-WORKFLOW-LEGACY-LOGS-0001` is historical-reader context only, not clause carry-forward.
- The file now uses the current chronology-first clause registry model while preserving the same first child release meaning.