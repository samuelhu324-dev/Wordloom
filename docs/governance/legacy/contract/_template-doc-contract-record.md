# doc-contract-record-template

```yaml
doc_contract:
  record_id: DOC-<AREA>-<NNNN>
  contract_id: <stable-doc-contract-id>
  family: DOC
  area: <doc-governance-area>
  status: <draft|active|deprecated|superseded|retired>
  summary: <current effective rule meaning>
  primary_source_owner: <current source-owner log or contract>
  applies_to: <targets governed by this doc-first contract>
  enforcement_surface: <template|log|runbook|view|index|automation>
  violation_semantics: <fail|warning|report-only|neutral>
  introduced_by: <first source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <minimal current traceability source>
  supersedes:
    - <optional replaced contract id>
  superseded_by:
    - <optional replacement contract id>
  notes:
    - <optional clarification>
```

## Guidance

- Use the filename model `DOC-<AREA>-<NNNN>-<summary>.md`.
- `record_id` is the short family-owned contract identifier; keep it stable after publication.
- `contract_id` should stay semantic and stable; do not encode slice IDs into it.
- `primary_source_owner` should name the current source-owner log or already-promoted contract from which this rule was stabilized.
- Keep `source_refs` minimal and current; use source-owner logs for traceability, not as the long-term primary reader surface once promotion is complete.

## Optional Legacy Redirect

- Use this only when a promoted `DOC` contract later becomes historical and readers still need a deterministic path to the newer current interpretation.
- Keep the same shape used by other contract surfaces:

```md
## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `superseded by DOC-NEW-0001`
- Read now:
  - `DOC-NEW-0001`
```