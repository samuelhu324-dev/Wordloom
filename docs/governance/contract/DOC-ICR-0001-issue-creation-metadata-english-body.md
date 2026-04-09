# doc-contract-record: DOC-ICR-0001

- `record_id`: `DOC-ICR-0001`
- `contract_id`: `ISSUE-CREATION-METADATA-ENGLISH-BODY`
- `title`: `issue creation metadata and English body stay explicit across current DOC issue-governance surfaces`

```yaml
doc_contract:
  record_id: DOC-ICR-0001
  contract_id: ISSUE-CREATION-METADATA-ENGLISH-BODY
  family: DOC
  area: ICR
  status: active
  summary: Issue creation must resolve milestone, relationship, project, and deterministic links before live creation while rendering an English-only body scaffold that keeps Context and child DoD intentionally unexpanded.
  primary_source_owner: docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
  applies_to: source-log-owned GitHub issue creation for child and top-level logs within the docs-GitHub lifecycle
  enforcement_surface: issue draft and create surfaces that derive metadata from frontmatter or exact controlled bridges and stop when required creation metadata is ambiguous
  violation_semantics: fail
  introduced_by: S0E-2D/P0-C1-S1
  last_changed_by: S0F-4I/P2-C1-S1S2
  source_refs:
    - docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
    - docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
    - docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the first issue-governance DOC contract body landed from the S0F-4I replacement packet.
    - The corresponding GC row remains in place during transition until matching demotion and reader-transition writes complete.
```

## Current Rule

- Creation may derive only deterministic metadata such as milestone, parent issue, project, and stable navigation links.
- Creation must not auto-author final Context or child issue DoD prose.
- Missing or ambiguous creation metadata remains blank or stops the mutation path rather than being guessed from prose.

## Compact History

- `Current source-owner origin`:
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- `Why this current contract exists`:
  - issue-creation governance now reads as family-owned DOC current meaning rather than as GC-registry-only admission vocabulary
- `Major evolution chain`:
  - `S0E-2D` fixed the creation metadata and English-body rule
  - `S0F-1A` clarified the fail-closed entrypoint boundary
  - `S0F-1D` concentrated lifecycle completeness around the same rule
  - `S0F-4I` landed the family-owned DOC replacement body

## Reader Notes

- `GC-ICR-0001` remains a lineage-safe narrow-registry row during transition, but current family-owned reading may now start here.
- The retained source-owner logs remain detailed chronology and evidence surfaces for the rule set.

## Traceability

- Source-owner logs:
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
- Promotion lane:
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`