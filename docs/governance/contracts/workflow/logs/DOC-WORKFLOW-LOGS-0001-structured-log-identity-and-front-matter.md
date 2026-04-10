# DOC-WORKFLOW-LOGS-0001 structured log identity and front matter

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LOGS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-LOGS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first logs-oriented child release from S0B-3A by extracting the narrow workflow rule for stable structured log identity, log-facing front matter, and cutover-based intake discipline.
  summary: Govern structured logs through stable workflow identifiers, logs-facing front matter, and one cutover rule that requires new log content to enter the managed system under the new identifier and metadata discipline.
  governance_area: workflow structured log identity and front matter governance
  applies_to: structured log ids, log titles, log-facing front matter fields, index-facing log identity, and new structured log intake after the cutover boundary
  enforcement_surface: manual
  violation_semantics: warning
  introduced_by: docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
  last_changed_by: docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
  source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - GitHub issue #44 (direct support for S0B-3A context; issue-only source)
  cumulative_source_refs:
    - docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md
    - GitHub issue #44 (direct support for S0B-3A context; issue-only source)
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md
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
    - This draft is the first narrow logs-oriented extraction from the mixed S0B-3A source packet rather than one already-generalized workflow parent release.
    - The broader DOC-WORKFLOW family path remains taxonomy only; this record does not claim split lineage from DOC-WORKFLOW-0001.
    - Front matter is intentionally kept narrow here on first extraction, while later parent or sibling-spanning widening remains explicitly reserved if repeated evidence justifies it.
```

## Release Change

- This release establishes the first logs-oriented child family extracted from `S0B-3A`.
- The release isolates three rule surfaces that were previously mixed together inside the broader source packet:
  - stable workflow identifiers as they appear in structured log titles and index-facing log identity
  - logs-facing front matter as the mechanically managed metadata surface for logs
  - the logs-intake half of cutover, which requires new structured log content to enter the managed system under the new identifier and metadata discipline
- This release intentionally does not absorb legacy taxonomy, stub preservation, or lifecycle-boundary cutover semantics; those remain reserved for `DOC-WORKFLOW-LIFECYCLE-0001`.

## Contract Statement

- Structured logs must use one stable workflow identifier pattern that expresses delivery/topic identity without binding that identity to directory layout or chronology.
- Log titles and index-facing log references should expose that stable identity clearly enough that readers can recognize the governed topic without reconstructing meaning from file placement alone.
- Structured logs should carry one mechanically managed front matter surface rather than scattering status, scope, links, and audit metadata through freeform prose.
- The logs-facing front matter should at least keep the fields that make structured logs navigable and mechanically readable, such as:
  - stable `id`
  - `kind`
  - human-readable `title`
  - `status`
  - `scope`
  - low-cardinality `tags`
  - link fields that preserve issue, PR, ADR, runbook, or nearby context anchors
  - `created` and `updated` audit fields
- From the cutover boundary onward, new structured log content must enter the system under the new identifier and front matter discipline rather than continuing the older unmanaged intake habits.
- This contract governs the logs-facing intake and identity body only; it does not by itself decide how legacy material is frozen, migrated on demand, or preserved through stubs.

## Current Reading

- Read this release when the question is `what is the first narrow workflow rule for structured log identity, log-facing front matter, and post-cutover logs intake?`
- Read the `S0B-3A` ledger when the question is `which parts of S0B-3A entered this logs family and which parts were routed elsewhere?`
- Read the broader workflow family only when the question is about the higher-level workflow path rather than this specific logs-facing rule body.

## Reader Notes

- This draft is intentionally narrower than any eventual generalized parent surface that might later synthesize identifier or front-matter meaning across logs, labs, runbooks, ADRs, or other workflow children.
- It is the first candidate owner of the earliest explicit logs-facing wording, not the final owner of every later cross-kind reuse of the same concepts.