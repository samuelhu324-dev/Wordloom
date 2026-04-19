# DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001 issue tags follow role based naming

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-GITHUB-ISSUES-TAGS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first issue-tag child release from S0A-1A by isolating role-based tag naming beneath the broader GitHub-Issues workflow packet.
  summary: Keep issue tags classed by naming role so readers can distinguish top-level work type, documentation hierarchy, and module or business scope without decoding mixed tag styles.
  governance_area: workflow GitHub issue tag naming governance
  applies_to: GitHub issue tag naming across top-level tags, hierarchy tags, and module or business-area tags for timeline queue work
  enforcement_surface: manual
  violation_semantics: warning
  owner_team: docs-governance
  current_steward: delegated:workflow-issue-tags-contract-maintainer
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
    split_from:
      - DOC-WORKFLOW-GITHUB-ISSUES-0001
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This child contract owns only the tag-rule body beneath the parent GitHub-issues mechanism contract.
    - The local repo currently has no S0A-1A source log, so this draft stays explicit about issue-only sourcing.
    - Current-state governance now reads through owner_team/current_steward/approval_state/reviewed_by/approved_by, while the parent ledger remains the routing and event-history surface that explains how this tag child stays active.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the current-state governance surface for the issue-tag child, while the `S0A-1A` parent ledger preserves the mixed-source routing and event-history chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day tag-taxonomy maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `family-introduced` | `2026-04-10` | `GitHub issue S0A-1A (#23)` | The issue-only source introduced the tag-naming child, but it does not by itself prove the current steward or approval chain for the current contract state. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-GOV-02` | `routing-writeback-event` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `role:packet-reviewer` | `current-child-routing-fixed` | `2026-04-11` | `ledger-S0A-1A-tools-github-issues-projects-and-tags.md` | The parent ledger fixed that tag naming is a dedicated child surface rather than remaining implicit in the broader GitHub-Issues mechanism body. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 third-cycle round` | Stewardship for the current tag child is now explicitly delegated to a narrower tag-taxonomy maintainer role while durable ownership remains with `docs-governance`. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-GOV-04` | `review-approval-separation-event` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-15` | `S0F-9A/P4 third-cycle round` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit on the tag child surface. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-01` | `Role-based tag classes` | `active` | `introduced` | `S0A-1A-R04` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Issue tags must stay classed by naming role rather than collapse into one mixed style. | Parent clause for the tag grammar child. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-02` | `Top-level tags use all caps` | `active` | `introduced` | `S0A-1A-R04` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Use `ALL CAPS` for top-level tags such as `EVOLUTION`, `BUG`, or `FEATURE`. | First explicit top-level naming clause. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-03` | `Hierarchy tags use lowercase` | `active` | `introduced` | `S0A-1A-R04` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Use lowercase for documentation-hierarchy tags such as `p/0`, `p/1`, or `sub/1`. | Keeps hierarchy signaling distinct from work-type and module labels. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-04` | `Module tags use capitalized case` | `active` | `introduced` | `S0A-1A-R04` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Use Capitalized case for module or business-area tags such as `Docs`, `Search`, or `Chronicle`. | Keeps module and business-scope labels visibly separate from hierarchy tags. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-CH-01` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `introduced` | `none` | `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-01; DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-02; DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-03; DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-04` | `unknown` | `2026-04-10` | The first tag child release is being aligned to the current chronology-first clause model so tag-role semantics remain reviewable through stable clause ids and one explicit source-basis anchor. | `S0A-1A-R04` | The release meaning is unchanged; this is a structure repair only. |

## Release Change

- This release remains the first tag-naming child extracted from `S0A-1A`.
- The current repair aligns the file to the current chronology-first contract shape by adding chronology fields, clause ids, and explicit source-basis anchors.
- The owned meaning remains unchanged:
  - issue tags stay classed by naming role
  - top-level tags use all caps
  - hierarchy tags use lowercase
  - module or business-area tags use Capitalized case

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-01`: Issue tags must stay classed by naming role rather than collapse into one mixed style.
- `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-02`: Use `ALL CAPS` for top-level tags such as `EVOLUTION`, `BUG`, or `FEATURE`.
- `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-03`: Use lowercase for documentation-hierarchy tags such as `p/0`, `p/1`, or `sub/1`.
- `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-ST-04`: Use Capitalized case for module or business-area tags such as `Docs`, `Search`, or `Chronicle`.

## Current Reading

- Read this contract when the question is `how should GitHub issue tags reveal hierarchy versus business scope?`
- Read the parent contract first only if the reader still needs the mechanism-introduction boundary for why GitHub Issues were introduced as the canonical breakdown unit.

## Reader Notes

- This child contract isolates tag naming so later tag taxonomy changes can happen without rewriting the parent mechanism contract or the title-rule contract.
- It does not own issue title grammar; that lives in the title child contract.
- In the current lineage model, this contract is one split child from `DOC-WORKFLOW-GITHUB-ISSUES-0001` alongside the title contract.
- The file now uses the current chronology-first clause registry model while preserving the same first child release meaning.