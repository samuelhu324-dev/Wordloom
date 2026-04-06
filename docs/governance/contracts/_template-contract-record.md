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
- `notes` may clarify operator context, but should never override structured fields.