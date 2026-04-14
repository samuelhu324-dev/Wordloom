# DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001 issue title encodes level and category

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-GITHUB-ISSUES-TITLE
  contract_release: 0001
  contract_id: DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first issue-title child release from S0A-1A by isolating title-level hierarchy and category grammar beneath the broader GitHub-Issues workflow packet.
  summary: Encode issue level and category directly in the issue title key so readers can identify hierarchy and scope at a glance without reconstructing structure from prose alone.
  governance_area: workflow GitHub issue title grammar governance
  applies_to: timeline queue issue titles, parent issue title keys, direct child issue title keys, and later sub-category title extensions
  enforcement_surface: manual
  violation_semantics: warning
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
    - This child contract owns only the title-rule body beneath the parent GitHub-issues mechanism contract.
    - The local repo currently has no S0A-1A source log, so this draft stays explicit about issue-only sourcing.
```

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-01` | `Title key encodes hierarchy` | `active` | `introduced` | `S0A-1A-R03` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Issue titles must encode level and category directly in the title key. | Parent rule for the title grammar child. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-02` | `Parent issue key grammar` | `active` | `introduced` | `S0A-1A-R03` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | The parent issue key should use `S + No. + capital letter`, such as `S0A`. | First explicit parent-key grammar clause. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-03` | `Direct child key grammar` | `active` | `introduced` | `S0A-1A-R03` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | A direct child issue key should add `/ + No.`, such as `S0A/1`. | Keeps the immediate hierarchy step explicit rather than implied from examples only. |
| `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-04` | `Sub-category distinction` | `active` | `introduced` | `S0A-1A-R03` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | If a child issue later needs an explicit sub-category distinction, that child key should include a capital letter rather than hiding the distinction in freeform prose only. | Keeps later title extensions reviewable without reopening the parent issue contract. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-CH-01` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `introduced` | `none` | `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-01; DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-02; DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-03; DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-04` | `unknown` | `2026-04-10` | The first title child release is being aligned to the current chronology-first clause model so the title grammar is reviewable through stable statement ids and one explicit source-basis anchor. | `S0A-1A-R03` | The release remains the same first child state; the repair only strengthens structure. |

## Release Change

- This release remains the first title-grammar child extracted from `S0A-1A`.
- The current repair aligns the file to the current chronology-first contract shape by adding chronology fields, clause ids, and explicit source-basis anchors.
- The owned meaning remains unchanged:
  - issue titles encode level and category directly in the title key
  - parent issue keys and direct child issue keys use stable grammar
  - later sub-category distinction should stay visible in the key rather than disappear into freeform prose

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-01`: Issue titles must encode level and category directly in the title key.
- `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-02`: The parent issue key should use `S + No. + capital letter`, such as `S0A`.
- `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-03`: A direct child issue key should add `/ + No.`, such as `S0A/1`.
- `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-ST-04`: If a child issue later needs an explicit sub-category distinction, that child key should include a capital letter rather than hiding the distinction in freeform prose only.

## Current Reading

- Read this contract when the question is `how should GitHub issue titles expose hierarchy and category?`
- Read the parent contract first only if the reader still needs the `why GitHub Issues exist here at all` boundary.

## Reader Notes

- This child contract isolates title grammar so it can later be revised, superseded, or extended without rewriting the parent introduction contract.
- It does not own tag naming rules; those live in the tag child contract.
- In the current lineage model, this contract is one split child from `DOC-WORKFLOW-GITHUB-ISSUES-0001` alongside the tag contract.
- The file now uses the current chronology-first clause registry model while preserving the same first child release meaning.