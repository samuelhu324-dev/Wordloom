# governance-contract-record: GC-ISS-0001

- `record_id`: `GC-ISS-0001`
- `contract_id`: `ISSUE-CREATION-METADATA-ENGLISH-BODY`
- `title`: `issue creation must resolve metadata deterministically and render an English-only scaffold`

```yaml
contract_record:
  contract_id: ISSUE-CREATION-METADATA-ENGLISH-BODY
  status: deprecated
  summary: Issue creation must resolve milestone, relationship, project, and deterministic links before live creation while rendering an English-only body scaffold that keeps Context and child DoD intentionally unexpanded.
  governance_area: issue-creation-governance
  applies_to: source-log-owned GitHub issue creation for child and top-level logs within the docs-GitHub lifecycle
  enforcement_surface: issue draft and create surfaces that derive metadata from frontmatter or exact controlled bridges and stop when required creation metadata is ambiguous
  violation_semantics: fail
  introduced_by: S0E-2D/P0-C1-S1
  last_changed_by: S0F-3E/P6-C1-S2
  source_refs:
    - docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
  supersedes: []
  superseded_by: []
  notes:
    - This retained historical body moved from the old GC root path during S0F-3M/P2 while the root path stayed occupied by a stub for old-ID landing.
    - This preserved legacy ISS-area record now redirects readers to GC-ICR-0001 after the S0F-3E P6 namespace split.
```

## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `split into ICR as GC-ICR-0001`
- Read now:
  - `GC-ICR-0001`

## Reader Notes

- Historical meaning preserved:
  - Creation may derive only deterministic metadata such as milestone, parent issue, project, and stable navigation links.
  - Creation must not auto-author final Context or child issue DoD prose.
- Historical boundary preserved:
  - Missing or ambiguous creation metadata remains blank or stops the mutation path rather than being guessed from prose.
- Current successor:
  - `GC-ICR-0001`

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Current completeness concentration:
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`