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

## Contract Statement

- Issue titles must encode level and category directly in the title key.
- The parent issue key should use `S + No. + capital letter`, such as `S0A`.
- A direct child issue key should add `/ + No.`, such as `S0A/1`.
- If a child issue later needs an explicit sub-category distinction, that child key should include a capital letter rather than hiding the distinction in freeform prose only.

## Current Reading

- Read this contract when the question is `how should GitHub issue titles expose hierarchy and category?`
- Read the parent contract first only if the reader still needs the `why GitHub Issues exist here at all` boundary.

## Reader Notes

- This child contract isolates title grammar so it can later be revised, superseded, or extended without rewriting the parent introduction contract.
- It does not own tag naming rules; those live in the tag child contract.
- In the current lineage model, this contract is one split child from `DOC-WORKFLOW-GITHUB-ISSUES-0001` alongside the tag contract.