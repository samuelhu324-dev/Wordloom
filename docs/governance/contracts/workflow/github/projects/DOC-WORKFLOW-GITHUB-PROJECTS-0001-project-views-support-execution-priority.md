# DOC-WORKFLOW-GITHUB-PROJECTS-0001 project views support execution priority

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-GITHUB-PROJECTS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-GITHUB-PROJECTS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first GitHub-Projects workflow release from S0A-1A by isolating Projects views as the execution-time status-board, lookup, sequencing, and bounded reprioritization surface beside, but not replacing, canonical GitHub Issues hierarchy.
  summary: Use GitHub Projects views as execution-time support for status-board reading, fast lookup, timeline sequencing, and bounded reprioritization while keeping GitHub Issues as the canonical work-breakdown hierarchy.
  governance_area: workflow GitHub Projects execution-support governance
  applies_to: GitHub Projects views, execution-time reprioritization, ad hoc or priority insertion support, and operator reading of current queue state during delivery
  enforcement_surface: manual
  violation_semantics: warning
  owner_team: docs-governance
  current_steward: delegated:workflow-projects-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  recorded_at: 2026-04-11
  reviewed_at: pending
  effective_from: unknown
  effective_until: ongoing
  introduced_by: GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  last_changed_by: docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md
  source_refs:
    - GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
    - docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md
  cumulative_source_refs:
    - GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
    - docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md
    - docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md
    - docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from:
      - DOC-WORKFLOW-GITHUB-ISSUES-0001
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This child contract owns GitHub Projects as execution-support surface only; it does not replace the canonical GitHub Issues hierarchy.
    - Current supporting evidence now directly shows three common operator readings for this surface: status-board columns, fast table lookup, and timeline sequencing.
    - The local repo currently has no S0A-1A source log, so this draft stays explicit about issue-only sourcing.
    - Current-state governance now reads through owner_team/current_steward/approval_state/reviewed_by/approved_by, while source and supplement history remain event metadata rather than current ownership markers.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or current approval identity.
- This contract therefore acts as the current-state governance surface for the Projects child, while the parent ledger and `SUP-001` preserve the route and evidence-history chain that led here.
- The current steward is now intentionally delegated rather than implicitly identical to the owner team, which lets the sample prove delegated stewardship without altering durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `family-introduced` | `2026-04-11` | `GitHub issue S0A-1A (#23)` | The issue-only source introduced the Projects slice, but it does not defend a named current steward or approver for the current contract state. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-GOV-02` | `current-draft-sharpened` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `role:packet-reviewer` | `statement-surface-sharpened` | `2026-04-11` | `ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md` | The accepted screenshot supplement sharpened the current draft wording for status-board, lookup, and timeline readings without changing current ownership semantics. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P2 sample drill` | Stewardship for the current Projects child is now explicitly delegated to the narrower Projects contract maintainer role while final approval remains with the broader docs-governance approver role. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-GOV-04` | `review-approval-separation-event` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-15` | `S0F-9A/P2 sample drill` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit or pending. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-01` | `Status-board execution reading` | `active` | `introduced` | `S0A-1A-R02; S0A-1A-R02-SUP-01` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | GitHub Projects views may be used as one visible execution-status surface with operating states such as `Doing`, `Done`, `Backlog`, and `Blocked`. | Screenshot-backed sharpening now makes this concrete reading explicit inside the first release rather than leaving it as only generic execution support prose. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-02` | `Fast table lookup reading` | `active` | `introduced` | `S0A-1A-R02; S0A-1A-R02-SUP-02` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | GitHub Projects views may be used as one fast lookup surface for issue identity, progress, linked PR context, and assignee context during delivery. | This keeps the operator-facing discovery function visible as part of the contract rather than burying it in supporting prose only. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-03` | `Timeline sequencing reading` | `active` | `introduced` | `S0A-1A-R02; S0A-1A-R02-SUP-03` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | GitHub Projects views may be used as one timeline and sequence-awareness surface for order, insertion, and interruption reading across the current work stream. | The screenshot-backed Projects evidence now makes the sequencing view explicit as contract-facing meaning. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-04` | `Bounded reprioritization support` | `active` | `introduced` | `S0A-1A-R02` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | GitHub Projects views may support bounded reprioritization or ad hoc insertion while work is already in flight. | This clause remains directly owned by the issue packet even though the screenshots mainly sharpen the three concrete view classes. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-05` | `Issues hierarchy remains canonical` | `active` | `introduced` | `S0A-1A-R01; S0A-1A-R02` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | GitHub Projects remains one execution-support surface only; canonical work-breakdown and hierarchy ownership stays with GitHub Issues. | This keeps the Projects child contract structurally tied to the issue hierarchy boundary rather than drifting into hierarchy ownership. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001-CH-01` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001` | `introduced` | `none` | `DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-01; DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-02; DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-03; DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-04; DOC-WORKFLOW-GITHUB-PROJECTS-0001-ST-05` | `unknown` | `2026-04-11` | The first Projects child release now records the concrete execution-support meanings that selective backfill and the accepted screenshot supplement made readable without transferring hierarchy ownership away from GitHub Issues. | `S0A-1A-R02; S0A-1A-R02-SUP-01; S0A-1A-R02-SUP-02; S0A-1A-R02-SUP-03` | One initial release row is sufficient here because the current file still acts as the first family release rather than as a later amendment to an earlier release id. |

## Release Change

- This release establishes the first Projects-oriented child family extracted from `S0A-1A`.
- The release isolates the execution-support surface that had previously remained implicit beside the broader issue packet:
  - Projects views can be used during execution for status-board reading, table-based lookup, and timeline sequencing
  - Projects views can also support ad hoc reprioritization and priority insertion
  - that support surface does not replace the canonical GitHub Issues hierarchy
- This release intentionally does not absorb issue title grammar or issue tag naming; those remain owned by the narrower sibling issue children.

## Contract Statement

- GitHub Projects views may be used as one operator-facing execution support surface during delivery.
- That execution support now reads in at least three evidenced common view classes:
  - one status-board reading for visible work state such as `Doing`, `Done`, `Backlog`, and `Blocked`
  - one table reading for fast lookup across issue identity, progress, linked PRs, and assignee context
  - one timeline reading for order, insertion, and sequence awareness across the work stream
- Projects views may also support bounded reprioritization or ad hoc insertion while work is already in flight.
- That support surface is secondary to the GitHub Issues hierarchy rather than a replacement for it.
- Canonical work-breakdown and hierarchy ownership remains with GitHub Issues.
- Projects views should therefore be read as one operator-facing execution support surface, not as the source of truth for decomposition semantics.

## Current Reading

- Read this release when the question is `how should GitHub Projects be used during execution without replacing the canonical issue hierarchy?`
- It is especially the current reader when the question is about status-board reading, everyday lookup, or timeline sequencing inside the Projects surface.
- Read the `S0A-1A` parent ledger or `SUP-001` packet when the question is `how did this Projects contract get sharpened and what evidence anchors currently defend those three view classes?`
- Read `DOC-WORKFLOW-GITHUB-ISSUES-0001` first only when the reader still needs the broader mechanism-introduction boundary.

## Reader Notes

- This draft exists because the source issue explicitly described Projects usage even though the earlier packet did not emit one dedicated Projects contract.
- The first accepted `SUP` pilot now sharpens this draft with screenshot-backed evidence for status-board, table, and timeline views, but does not change the primary routing boundary.
- Under `S0F-9A/P1`, this contract now carries current-state governance metadata directly, while the parent ledger and supplement remain the event/history surfaces that explain how the current reading was reached.
- Under `S0F-9A/P2`, this contract now also acts as the delegated-stewardship sample inside the family, while the supplement proves the verifier and approver separation that should not be flattened into current-state ownership.
- More detailed Projects operating flow may still need later archaeology from non-screenshot evidence if the repo wants one richer later release.