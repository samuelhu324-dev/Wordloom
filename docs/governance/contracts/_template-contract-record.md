# governance-contract-record-template

```yaml
contract_record:
  contract_id: <stable-governance-contract-id>
  record_kind: chronology-first-contract
  status: <draft|active|deprecated|superseded|retired>
  summary: <effective contract meaning at this contract state>
  governance_area: <governed area>
  applies_to: <targets governed by this contract>
  enforcement_surface: <workflow|script|runbook|adapter|manual>
  violation_semantics: <fail|warning|report-only|neutral>
  introduced_by: <first source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <minimal decisive source reference>
  supporting_evidence_refs:
    - <optional retained chronology or validation evidence>
  lineage:
    supersedes:
      - <optional one-to-one replaced contract id>
    superseded_by:
      - <optional one-to-one replacement contract id>
    split_from:
      - <optional parent contract id if this record is a split child>
    split_into:
      - <optional child contract id if this record later splits>
    absorbed_from:
      - <optional earlier contract id whose meaning is partly absorbed here>
    absorbed_into:
      - <optional later contract id that absorbs meaning from this record>
    retires:
      - <optional earlier contract id explicitly ended by this record>
    retired_by:
      - <optional later contract id or decision that retires this record>
  notes:
    - <optional clarification>
```

## Guidance

- Keep `contract_id` semantic and stable; do not encode slice IDs, run IDs, or implementation filenames into it.
- Canonical chronology-first `contract_id` values should use one long-path grammar rather than opaque short abbreviations:
  - `DOC-<DOMAIN>-<SUBDOMAIN>-...-<CATEGORY>-<NNNN>`
  - Example family shapes: `DOC-WORKFLOW-GITHUB-ISSUES-0001`, `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001`, `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001`
- The category path inside `contract_id` should stay human-readable enough that readers can understand the contract family without opening a separate glossary.
- Keep the file title or filename summary readable, but treat `contract_id` as the stable identity rather than the path or summary slug.
- Use this template only when the record is the clearest owner of one governance rule or boundary state in chronology-first rebuild.
- Do not use this template for rows that are only validation evidence, migration mechanics, wrapper transport, or chronology support without primary rule ownership.
- `summary` should describe the effective rule meaning at this contract state, not the full change history.
- `source_refs` should stay minimal and point only to the decisive sources that justify the contract state itself.
- `supporting_evidence_refs` may capture retained evidence that helps verify chronology without promoting every evidence row into a contract.
- Use `notes` or a nearby prose section to make the human-readable distinction explicit when a contract is functioning as either:
  - one `parent contract` that owns mechanism introduction, `why`, and boundary
  - one `child contract` that owns one independently judgeable narrow rule body beneath that parent
- Use `supersedes` / `superseded_by` only for one-to-one successor replacement.
- Use `split_from` / `split_into` when one broader contract decomposes into narrower children.
- Use `absorbed_from` / `absorbed_into` when rule meaning is carried forward into another contract without a pure one-to-one replacement.
- Use `retires` / `retired_by` when a contract state ends explicitly without one clean direct successor.
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

## Qualification Rule

- Treat a source-owned item as a chronology-first contract only when its primary historical result is one of these:
  - it introduces a new governance rule or decision state
  - it materially changes an existing governance rule or decision state
  - it stabilizes one governance boundary strongly enough that later history should read it as a named contract state
- Treat a source-owned item as evidence-only or lineage-support history when it mainly validates, packages, transports, audits, or narrates a rule whose clearest meaning lives elsewhere.