# doc-contract-record: DOC-ICL-0001

- `record_id`: `DOC-ICL-0001`
- `contract_id`: `ISSUE-CONCLUSION-POST-MERGE-LINKAGE`
- `title`: `issue conclusion post-merge linkage stays explicit across current DOC issue-governance surfaces`

```yaml
doc_contract:
  record_id: DOC-ICL-0001
  contract_id: ISSUE-CONCLUSION-POST-MERGE-LINKAGE
  family: DOC
  area: ICL
  status: active
  summary: Issue conclusion is a post-merge lifecycle step that must materialize exact-ID merged PR linkage into the final issue body instead of treating GitHub close state as sufficient completion.
  primary_source_owner: docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md
  applies_to: source-log-owned GitHub issues that move from open or merged-open state into final concluded state after the delivery PR set has merged
  enforcement_surface: issue conclusion planners and apply surfaces that require merged PR evidence and write the final DoD-led conclusion body back to the issue
  violation_semantics: fail
  introduced_by: S0E-2E/P0-C1-S1
  last_changed_by: S0F-4I/P2-C1-S1S2
  source_refs:
    - docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
    - docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the issue-conclusion DOC contract body landed from the S0F-4I replacement packet.
    - The corresponding GC row remains in place during transition until matching demotion and reader-transition writes complete.
```

## Current Rule

- Final issue conclusion activates only after the exact delivery PR set is merged.
- The final body must carry short merged-PR refs in DoD and deterministic PR URLs in Links.

## Compact History

- `Current source-owner origin`:
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
- `Why this current contract exists`:
  - issue-conclusion governance now reads as family-owned DOC current meaning rather than as GC-registry-only admission vocabulary
- `Major evolution chain`:
  - `S0E-2E` fixed the post-merge linkage rule
  - `S0F-1D` concentrated lifecycle completeness around the same rule
  - `S0F-4I` landed the family-owned DOC replacement body

## Reader Notes

- `GC-ICL-0001` remains a lineage-safe narrow-registry row during transition, but current family-owned reading may now start here.

## Traceability

- Source-owner logs:
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
- Promotion lane:
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`