# DOC-WORKFLOW-GITHUB-PROJECTS-0001 project views support execution priority

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-GITHUB-PROJECTS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-GITHUB-PROJECTS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first GitHub-Projects workflow release from S0A-1A by isolating Projects views as the execution-time prioritization and ad hoc insertion support surface beside, but not replacing, canonical GitHub Issues hierarchy.
  summary: Use GitHub Projects views as execution-time support for reprioritization and ad hoc insertion while keeping GitHub Issues as the canonical work-breakdown hierarchy.
  governance_area: workflow GitHub Projects execution-support governance
  applies_to: GitHub Projects views, execution-time reprioritization, ad hoc or priority insertion support, and operator reading of current queue state during delivery
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
    - This child contract owns GitHub Projects as execution-support surface only; it does not replace the canonical GitHub Issues hierarchy.
    - The local repo currently has no S0A-1A source log, so this draft stays explicit about issue-only sourcing.
```

## Release Change

- This release establishes the first Projects-oriented child family extracted from `S0A-1A`.
- The release isolates the execution-support surface that had previously remained implicit beside the broader issue packet:
  - Projects views can be used during execution for ad hoc reprioritization and priority insertion
  - that support surface does not replace the canonical GitHub Issues hierarchy
- This release intentionally does not absorb issue title grammar or issue tag naming; those remain owned by the narrower sibling issue children.

## Contract Statement

- GitHub Projects views may be used as execution-time support for reprioritization, ad hoc insertion, and current work-state scanning during delivery.
- That support surface is secondary to the GitHub Issues hierarchy rather than a replacement for it.
- Canonical work-breakdown and hierarchy ownership remains with GitHub Issues.
- Projects views should therefore be read as one operator-facing execution support surface, not as the source of truth for decomposition semantics.

## Current Reading

- Read this release when the question is `how should GitHub Projects be used during execution without replacing the canonical issue hierarchy?`
- Read `DOC-WORKFLOW-GITHUB-ISSUES-0001` first only when the reader still needs the broader mechanism-introduction boundary.

## Reader Notes

- This draft exists because the source issue explicitly described Projects usage even though the earlier packet did not emit one dedicated Projects contract.
- More detailed Projects operating flow may still need later archaeology from non-log evidence if the repo wants one richer later release.