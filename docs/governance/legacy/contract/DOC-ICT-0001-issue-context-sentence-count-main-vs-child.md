# doc-contract-record: DOC-ICT-0001

- `record_id`: `DOC-ICT-0001`
- `contract_id`: `ISSUE-CONTEXT-SENTENCE-COUNT-MAIN-VS-CHILD`
- `title`: `issue Context sentence-count and shape stay explicit across current DOC issue-governance surfaces`

```yaml
doc_contract:
  record_id: DOC-ICT-0001
  contract_id: ISSUE-CONTEXT-SENTENCE-COUNT-MAIN-VS-CHILD
  family: DOC
  area: ICT
  status: active
  summary: Issue Context must use one English sentence per bullet line, with exactly five lines for main-log issues and four lines for child-log issues, under one source-log-derived and fail-closed validation rule.
  primary_source_owner: docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md
  applies_to: issue body Context sections rendered during issue draft generation and issue conclusion refresh for source-log-owned main and child issues
  enforcement_surface: shared Context renderers and lifecycle or conclusion gates that validate sentence count, one-sentence-per-line shape, and source-log-derived anchors
  violation_semantics: fail
  introduced_by: S0E-6C/P0-C1-S1
  last_changed_by: S0F-4I/P2-C1-S1S2
  source_refs:
    - docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md
    - docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md
    - docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the issue-context DOC contract body landed from the S0F-4I replacement packet.
    - The corresponding GC row remains in place during transition until matching demotion and reader-transition writes complete.
```

## Current Rule

- Main-log issues keep five Context lines.
- Child issues keep four Context lines.
- Every line remains one English sentence and must still belong to the current source log rather than to generic boilerplate.

## Compact History

- `Current source-owner origin`:
  - `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
- `Why this current contract exists`:
  - issue-context governance now reads as family-owned DOC current meaning rather than as GC-registry-only admission vocabulary
- `Major evolution chain`:
  - `S0E-6C` fixed the sentence-count and shape rule
  - `S0F-1B` added the current authoring-path owner for the same boundary
  - `S0F-4I` landed the family-owned DOC replacement body

## Reader Notes

- `GC-ICT-0001` remains occupied as a lineage-safe legacy redirect surface during transition, but current family-owned reading now starts here.

## Traceability

- Source-owner logs:
  - `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
  - `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
- Promotion lane:
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`