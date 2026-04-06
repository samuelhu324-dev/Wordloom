# governance-contract-record: GC-ICT-0001

- `record_id`: `GC-ICT-0001`
- `contract_id`: `ISSUE-CONTEXT-SENTENCE-COUNT-MAIN-VS-CHILD`
- `title`: `issue Context keeps exact main-versus-child sentence counts under one source-log-derived rule`

```yaml
contract_record:
  contract_id: ISSUE-CONTEXT-SENTENCE-COUNT-MAIN-VS-CHILD
  status: active
  summary: Issue Context must use one English sentence per bullet line, with exactly five lines for main-log issues and four lines for child-log issues, under one source-log-derived and fail-closed validation rule.
  governance_area: issue-context-governance
  applies_to: issue body Context sections rendered during issue draft generation and issue conclusion refresh for source-log-owned main and child issues
  enforcement_surface: shared Context renderers and lifecycle or conclusion gates that validate sentence count, one-sentence-per-line shape, and source-log-derived anchors
  violation_semantics: fail
  introduced_by: S0E-6C/P0-C1-S1
  last_changed_by: S0F-3E/P6-C1-S1
  source_refs:
    - docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md
    - docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md
  supersedes: []
  superseded_by: []
  notes:
    - This current record republishes the legacy GC-ISS-0003 contract under the narrower ICT current namespace after the S0F-3E P6 split execution.
```

## Reader Notes

- Current active meaning:
  - Main-log issues keep five Context lines.
  - Child issues keep four Context lines.
  - Every line remains one English sentence and must still belong to the current source log rather than to generic boilerplate.

## Traceability

- Original sentence-count owner:
  - `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
- Current authoring-path owner:
  - `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`