# governance-contract-record-template

```yaml
contract_record:
  contract_id: <stable-governance-contract-id>
  status: <draft|active|deprecated|superseded|retired>
  summary: <current effective contract meaning>
  governance_area: <governed area>
  applies_to: <targets governed by this contract>
  enforcement_surface: <workflow|script|runbook|adapter|manual>
  violation_semantics: <fail|warning|report-only|neutral>
  introduced_by: <first source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <minimal source-log reference>
  supersedes:
    - <optional replaced contract id>
  superseded_by:
    - <optional replacement contract id>
  notes:
    - <optional clarification>
```

## Guidance

- Keep `contract_id` semantic and stable; do not encode slice IDs, run IDs, or implementation filenames into it.
- `summary` should describe the current effective rule, not the change history.
- `source_refs` should stay minimal and point only to the most relevant current traceability sources.
- Use `superseded_by` only for one-to-one successor replacement; do not overload it to represent `split into` or `absorbed into` cases.
- `notes` may clarify operator context, but should never override structured fields.

## Optional Legacy Redirect

- Use this only when the record is intentionally stored as non-active history and readers still need a deterministic path to the current interpretation.
- Keep this section near the top of the file, immediately after the YAML block.
- The section should state:
  - current standing such as `deprecated`, `superseded`, or `retired`
  - the lineage verb such as `absorbed into`, `split into`, or `superseded by`
  - the current record or records a reader should consult now, if any
- Example shape:

```md
## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `absorbed into GC-NEW-0001`
- Read now:
  - `GC-NEW-0001`
```