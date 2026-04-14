# governance-contract-record: GC-ICR-0001

- `record_id`: `GC-ICR-0001`
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
  last_changed_by: S0F-4I/P3-C1-S1S2
  source_refs:
    - docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
    - docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
  supersedes: []
  superseded_by:
    - DOC-ICR-0001
  notes:
    - This preserved GC registry record now redirects readers to DOC-ICR-0001 after the S0F-4I family-owned promotion-extension packet.
    - The root path remains occupied as a lineage-safe redirect surface during family-first transition.
```

## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `re-homed into DOC as DOC-ICR-0001`
- Read now:
  - `DOC-ICR-0001`

## Reader Notes

- Historical meaning preserved:
  - Creation may derive only deterministic metadata such as milestone, parent issue, project, and stable navigation links.
  - Creation must not auto-author final Context or child issue DoD prose.
- Historical boundary preserved:
  - Missing or ambiguous creation metadata remains blank or stops the mutation path rather than being guessed from prose.
- Current family-owned successor:
  - `DOC-ICR-0001`

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Current fail-closed boundary clarification:
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- Current completeness concentration:
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`