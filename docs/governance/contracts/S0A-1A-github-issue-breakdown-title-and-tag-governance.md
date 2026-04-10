# S0A-1A github issue breakdown title and tag governance

```yaml
contract_record:
  contract_id: S0A-1A
  record_kind: chronology-first-contract
  status: draft
  summary: Use GitHub Issues as the canonical breakdown unit for timeline queue work, with deterministic title-level encoding and tag naming classes that keep scope and category readable at a glance.
  governance_area: issue breakdown title encoding and tag naming governance
  applies_to: timeline queue planning, GitHub issue decomposition, issue title structure, and issue tag naming
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
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This preview uses the issue identity directly because that is the clearest readable anchor for the user review standard.
    - The local repo currently has no S0A-1A source log, so this draft must stay explicit about issue-only sourcing.
```

## Contract Statement

- Timeline queue work should be decomposed into GitHub Issues rather than kept only in one prose queue or one operator memory stream.
- GitHub Projects views may help with ad hoc reprioritization during execution, but they do not replace the issue hierarchy as the canonical breakdown surface.
- Issue titles must encode level and category directly in the title key:
  - use `S + No. + capital letter` for the primary level and category, such as `S0A`
  - add `/ + No.` for direct child issues, such as `S0A/1`
  - if a child issue needs sub-category distinction, include a capital letter in that child key
- Issue tags must stay classed by naming role:
  - use `ALL CAPS` for top-level tags such as `EVOLUTION`, `BUG`, or `FEATURE`
  - use lowercase for documentation-hierarchy tags such as `p/0`, `p/1`, or `sub/1`
  - use Capitalized case for module or business-area tags such as `Docs`, `Search`, or `Chronicle`

## Current Reading

- Read this contract when the question is `what problem did S0A-1A solve?`
- The answer is: it fixed how timeline work should be split into issues, how issue titles should expose level and category, and how tags should reveal hierarchy versus business scope without making readers infer the structure from prose.

## Reader Notes

- This is intentionally a one-contract preview, not a broad foundational batch.
- If this shape is accepted, later chronology-first contracts should prefer the same `look once and know the problem` standard instead of broad umbrella summaries.