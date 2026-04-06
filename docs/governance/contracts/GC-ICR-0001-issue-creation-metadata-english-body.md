# governance-contract-record: GC-ICR-0001

- `record_id`: `GC-ICR-0001`
- `contract_id`: `ISSUE-CREATION-METADATA-ENGLISH-BODY`
- `title`: `issue creation must resolve metadata deterministically and render an English-only scaffold`

```yaml
contract_record:
  contract_id: ISSUE-CREATION-METADATA-ENGLISH-BODY
  status: active
  summary: Issue creation must resolve milestone, relationship, project, and deterministic links before live creation while rendering an English-only body scaffold that keeps Context and child DoD intentionally unexpanded.
  governance_area: issue-creation-governance
  applies_to: source-log-owned GitHub issue creation for child and top-level logs within the docs-GitHub lifecycle
  enforcement_surface: issue draft and create surfaces that derive metadata from frontmatter or exact controlled bridges and stop when required creation metadata is ambiguous
  violation_semantics: fail
  introduced_by: S0E-2D/P0-C1-S1
  last_changed_by: S0F-3F/P4-C1-S1
  source_refs:
    - docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
    - docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
  supersedes: []
  superseded_by: []
  notes:
    - This current record republishes the legacy GC-ISS-0001 contract under the narrower ICR current namespace after the S0F-3E P6 split execution.
    - S0F-3F/P4 adds S0F-1A as the current fail-closed entrypoint clarification for real issue-create stop conditions without changing the front-door contract boundary.
```

## Reader Notes

- Current active meaning:
  - Creation may derive only deterministic metadata such as milestone, parent issue, project, and stable navigation links.
  - Creation must not auto-author final Context or child issue DoD prose.
- Current active boundary:
  - Missing or ambiguous creation metadata remains blank or stops the mutation path rather than being guessed from prose.

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Current fail-closed boundary clarification:
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- Current completeness concentration:
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`