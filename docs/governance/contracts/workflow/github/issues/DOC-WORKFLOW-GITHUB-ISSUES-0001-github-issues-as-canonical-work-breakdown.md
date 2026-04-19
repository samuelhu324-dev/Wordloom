# DOC-WORKFLOW-GITHUB-ISSUES-0001 github issues as canonical work breakdown

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-GITHUB-ISSUES
  contract_release: 0001
  contract_id: DOC-WORKFLOW-GITHUB-ISSUES-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first GitHub-Issues workflow release from S0A-1A by introducing Issues as the canonical work-breakdown unit while keeping title grammar, tag naming, and Projects usage reviewable as narrower sibling surfaces.
  summary: Introduce GitHub Issues as the canonical breakdown mechanism for timeline queue work, while treating GitHub Projects views as execution-time prioritization aids rather than replacements for issue hierarchy.
  governance_area: workflow GitHub issue mechanism governance
  applies_to: timeline queue planning, GitHub issue decomposition, issue hierarchy design, and operator reading of work breakdown state
  enforcement_surface: manual
  violation_semantics: warning
  owner_team: docs-governance
  current_steward: delegated:workflow-github-issues-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  recorded_at: 2026-04-10
  reviewed_at: pending
  effective_from: unknown
  effective_until: ongoing
  introduced_by: GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  last_changed_by: GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  source_refs:
    - GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  cumulative_source_refs:
    - GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into:
      - DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001
      - DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001
      - DOC-WORKFLOW-GITHUB-PROJECTS-0001
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This parent contract owns mechanism introduction, why, and boundary; it does not try to carry the full title-rule or tag-rule text itself.
    - The local repo currently has no S0A-1A source log, so this draft stays explicit about issue-only sourcing.
    - Current-state governance now reads through owner_team/current_steward/approval_state/reviewed_by/approved_by, while the parent ledger remains the routing and event-history surface that explains why this mechanism parent is still current.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the current-state governance surface for the GitHub-Issues mechanism parent, while the `S0A-1A` parent ledger preserves the mixed-source routing and event-history chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day GitHub-Issues parent maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `family-introduced` | `2026-04-10` | `GitHub issue S0A-1A (#23)` | The issue-only source introduced the GitHub-Issues mechanism parent, but it does not by itself prove the current steward or approval chain for the current contract state. |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-GOV-02` | `routing-writeback-event` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `role:packet-reviewer` | `current-parent-routing-fixed` | `2026-04-11` | `ledger-S0A-1A-tools-github-issues-projects-and-tags.md` | The selective backfill ledger fixed that the GitHub-Issues mechanism remains the parent contract while title, tag, and Projects surfaces can be read through narrower child contracts. |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 third-cycle round` | Stewardship for the current GitHub-Issues parent is now explicitly delegated to a narrower mechanism maintainer role while durable ownership remains with `docs-governance`. |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-GOV-04` | `review-approval-separation-event` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-15` | `S0F-9A/P4 third-cycle round` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit on the parent mechanism surface. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-01` | `Canonical work breakdown` | `active` | `introduced` | `S0A-1A-R01` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Timeline queue work should be decomposed into GitHub Issues rather than kept only in one prose queue or one operator memory stream. | Primary mechanism-introduction clause for the issue packet. |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-02` | `Projects does not replace hierarchy` | `active` | `introduced` | `S0A-1A-R01; S0A-1A-R02` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | GitHub Projects views may help with reprioritization during execution, but they do not replace the issue hierarchy as the canonical breakdown surface. | This keeps the parent contract structurally tied to the later Projects child without transferring hierarchy ownership away from Issues. |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-03` | `Title rule delegated to child` | `active` | `introduced` | `S0A-1A-R03` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Issue title grammar is owned by a narrower child contract beneath this parent rather than being restated here as mixed mechanism text. | Parent-boundary clause clarifying ownership split for title grammar. |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-04` | `Tag rule delegated to child` | `active` | `introduced` | `S0A-1A-R04` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Issue tag naming is owned by a narrower child contract beneath this parent rather than remaining embedded in the mechanism-introduction body. | Parent-boundary clause clarifying ownership split for tag naming. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001-CH-01` | `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `introduced` | `none` | `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-01; DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-02; DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-03; DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-04` | `unknown` | `2026-04-10` | The first issue-mechanism release is being aligned to the current chronology-first clause model so the parent/child ownership boundaries remain reviewable against the repaired S0A-1A ledger. | `S0A-1A-R01; S0A-1A-R02; S0A-1A-R03; S0A-1A-R04` | The release meaning is unchanged; only the current contract structure is made explicit. |

## Release Change

- This release remains the first parent GitHub-Issues contract extracted from `S0A-1A`.
- The current repair aligns the file to the current chronology-first contract shape by adding chronology fields, clause ids, and explicit source-basis anchors.
- This release still owns mechanism introduction and boundary only:
  - GitHub Issues become the canonical work-breakdown unit
  - GitHub Projects may support execution-time reprioritization without replacing issue hierarchy
  - title grammar and tag naming remain delegated to narrower child contracts

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-01`: Timeline queue work should be decomposed into GitHub Issues rather than kept only in one prose queue or one operator memory stream.
- `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-02`: GitHub Projects views may help with ad hoc reprioritization during execution, but they do not replace the issue hierarchy as the canonical breakdown surface.
- `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-03`: Title rules are owned by narrower child contracts beneath this parent.
- `DOC-WORKFLOW-GITHUB-ISSUES-0001-ST-04`: Tag rules are owned by narrower child contracts beneath this parent.

## Current Reading

- Read this contract when the question is `why did this workflow start using GitHub Issues as the canonical breakdown mechanism?`
- Then open the child contracts when the question becomes `how should issue titles be encoded?` or `how should issue tags be named?`

## Reader Notes

- This is the parent contract in the first parent-and-child packet generated from issue-only source `S0A-1A`.
- It is intentionally narrower than the earlier mixed preview because it keeps mechanism introduction separate from the narrower rule bodies.
- In the current lineage model, this broader issue-mechanism contract splits into the title and tag child contracts beneath it.
- The file now uses the current chronology-first clause registry model while preserving the same first-release mechanism boundary.