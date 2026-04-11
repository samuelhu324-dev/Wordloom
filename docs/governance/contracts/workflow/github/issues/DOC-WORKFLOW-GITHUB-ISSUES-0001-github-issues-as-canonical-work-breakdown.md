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
```

## Contract Statement

- Timeline queue work should be decomposed into GitHub Issues rather than kept only in one prose queue or one operator memory stream.
- GitHub Projects views may help with ad hoc reprioritization during execution, but they do not replace the issue hierarchy as the canonical breakdown surface.
- This contract introduces the mechanism and boundary only:
  - GitHub Issues become the canonical work-breakdown unit
  - title rules and tag rules are owned by narrower child contracts beneath this parent

## Current Reading

- Read this contract when the question is `why did this workflow start using GitHub Issues as the canonical breakdown mechanism?`
- Then open the child contracts when the question becomes `how should issue titles be encoded?` or `how should issue tags be named?`

## Reader Notes

- This is the parent contract in the first parent-and-child packet generated from issue-only source `S0A-1A`.
- It is intentionally narrower than the earlier mixed preview because it keeps mechanism introduction separate from the narrower rule bodies.
- In the current lineage model, this broader issue-mechanism contract splits into the title and tag child contracts beneath it.