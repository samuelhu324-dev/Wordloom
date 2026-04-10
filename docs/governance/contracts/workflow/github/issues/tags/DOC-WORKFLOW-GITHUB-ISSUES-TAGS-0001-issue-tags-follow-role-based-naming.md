# DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001 issue tags follow role based naming

```yaml
contract_record:
  contract_id: DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001
  record_kind: chronology-first-contract
  status: draft
  summary: Keep issue tags classed by naming role so readers can distinguish top-level work type, documentation hierarchy, and module or business scope without decoding mixed tag styles.
  governance_area: workflow GitHub issue tag naming governance
  applies_to: GitHub issue tag naming across top-level tags, hierarchy tags, and module or business-area tags for timeline queue work
  enforcement_surface: manual
  violation_semantics: warning
  introduced_by: GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  last_changed_by: GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  source_refs:
    - GitHub issue S0A-1A (issue-only source; no local log exists in workspace)
  supporting_evidence_refs: []
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
```

## Contract Statement

- Issue tags must stay classed by naming role rather than collapse into one mixed style.
- Use `ALL CAPS` for top-level tags such as `EVOLUTION`, `BUG`, or `FEATURE`.
- Use lowercase for documentation-hierarchy tags such as `p/0`, `p/1`, or `sub/1`.
- Use Capitalized case for module or business-area tags such as `Docs`, `Search`, or `Chronicle`.

## Current Reading

- Read this contract when the question is `how should GitHub issue tags reveal hierarchy versus business scope?`
- Read the parent contract first only if the reader still needs the mechanism-introduction boundary for why GitHub Issues were introduced as the canonical breakdown unit.

## Reader Notes

- This child contract isolates tag naming so later tag taxonomy changes can happen without rewriting the parent mechanism contract or the title-rule contract.
- It does not own issue title grammar; that lives in the title child contract.
- In the current lineage model, this contract is one split child from `DOC-WORKFLOW-GITHUB-ISSUES-0001` alongside the title contract.