# governance-contract-record: GC-ICL-0001

- `record_id`: `GC-ICL-0001`
- `contract_id`: `ISSUE-CONCLUSION-POST-MERGE-LINKAGE`
- `title`: `issue conclusion happens only after merge and must record exact delivery PR linkage`

```yaml
contract_record:
  contract_id: ISSUE-CONCLUSION-POST-MERGE-LINKAGE
  status: deprecated
  summary: Issue conclusion is a post-merge lifecycle step that must materialize exact-ID merged PR linkage into the final issue body instead of treating GitHub close state as sufficient completion.
  governance_area: issue-conclusion-governance
  applies_to: source-log-owned GitHub issues that move from open or merged-open state into final concluded state after the delivery PR set has merged
  enforcement_surface: issue conclusion planners and apply surfaces that require merged PR evidence and write the final DoD-led conclusion body back to the issue
  violation_semantics: fail
  introduced_by: S0E-2E/P0-C1-S1
  last_changed_by: S0F-4I/P3-C1-S1S2
  source_refs:
    - docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md
    - docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md
  supersedes: []
  superseded_by:
    - DOC-ICL-0001
  notes:
    - This preserved GC registry record now redirects readers to DOC-ICL-0001 after the S0F-4I family-owned promotion-extension packet.
    - The root path remains occupied as a lineage-safe redirect surface during family-first transition.
```

## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `re-homed into DOC as DOC-ICL-0001`
- Read now:
  - `DOC-ICL-0001`

## Reader Notes

- Historical meaning preserved:
  - Final issue conclusion activates only after the exact delivery PR set is merged.
  - The final body must carry short merged-PR refs in DoD and deterministic PR URLs in Links.
- Current family-owned successor:
  - `DOC-ICL-0001`

## Traceability

- Stable semantic owner:
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
- Current completeness concentration:
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`