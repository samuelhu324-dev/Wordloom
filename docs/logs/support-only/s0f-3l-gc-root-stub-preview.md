# S0F-3L root-stub preview for preserved old GC redirect records

- status: `preview-only`
- package owner: `S0F-3L`
- candidate family: `GC-ISS-*` and `GC-PRB-0001`
- root surface under test: `docs/governance/contracts/`
- future replacement target surface: `docs/governance/contracts/support-only/`
- purpose:
  - retain one executable draft of the root-stub body and bounded execution checks before any later cleanup-execution round reopens a real move package

## Proposed Root Stub Body Pattern

- The stub keeps the old root path occupied.
- The full retained body would move to the support-only contracts surface using the same basename.
- The stub preserves old-ID landing and deterministic redirect without pretending to be the full retained historical body.

### Single-successor example (`GC-ISS-0001`)

```md
# governance-contract-stub: GC-ISS-0001

- `record_id`: `GC-ISS-0001`
- `contract_id`: `ISSUE-CREATION-METADATA-ENGLISH-BODY`
- `status`: `archived`
- `moved_from`: `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
- `moved_to`: `docs/governance/contracts/support-only/GC-ISS-0001-issue-creation-metadata-english-body.md`
- `moved_at`: `<set-at-execution-time>`

## This file moved

- Current active successor:
  - `GC-ICR-0001`
- Retained historical body:
  - `docs/governance/contracts/support-only/GC-ISS-0001-issue-creation-metadata-english-body.md`

## Reader Notes

- This root path remains occupied so old-ID links and legacy citations can still land here first.
- Read `GC-ICR-0001` for current rule meaning.
- Open the moved support-only body only when the retained historical wording itself is needed.
- Do not edit here.
```

### Multi-successor example (`GC-PRB-0001`)

```md
# governance-contract-stub: GC-PRB-0001

- `record_id`: `GC-PRB-0001`
- `contract_id`: `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS`
- `status`: `archived`
- `moved_from`: `docs/governance/contracts/GC-PRB-0001-historical-drift-fail-on-findings.md`
- `moved_to`: `docs/governance/contracts/support-only/GC-PRB-0001-historical-drift-fail-on-findings.md`
- `moved_at`: `<set-at-execution-time>`

## This file moved

- Current active successors:
  - `GC-PRR-0001`
  - `GC-PRG-0001`
- Retained historical body:
  - `docs/governance/contracts/support-only/GC-PRB-0001-historical-drift-fail-on-findings.md`

## Reader Notes

- This root path remains occupied so old umbrella-ID links and legacy lineage citations can still land here first.
- Read `GC-PRR-0001` and `GC-PRG-0001` for current rule meaning.
- Open the moved support-only body only when the retained umbrella wording itself is needed.
- Do not edit here.
```

## Navigation Support Contract

- Keep the root-path citation unchanged when a reader surface is intentionally preserving:
  - old-ID landing
  - split-package lineage
  - cleanup-boundary enumeration of the preserved legacy set
- Rewrite direct references to the support-only target only when the reader surface is supposed to open the full retained body rather than just land on the old ID and follow successor guidance.
- `docs/governance/contracts/support-only/INDEX.md` must list any moved full-body target so support-only navigation does not depend on directory browsing.
- A later cleanup manifest must record which references stay on the root stub and which references are retargeted to the moved full body.

## Execution Checklist

- [ ] reopen cleanup execution under one explicit owner before touching any preserved old root-level `GC-*` file
- [ ] confirm `docs/governance/contracts/support-only/INDEX.md` remains the stable local navigation surface for moved full-body targets
- [ ] copy the retained full body to `docs/governance/contracts/support-only/` using the same basename before replacing the root file
- [ ] replace the old root file with the appropriate stub form, setting `moved_at` to the real execution date
- [ ] validate that split-package and cleanup-boundary readers remain acceptable when they land on the root stub rather than the old full body
- [ ] rewrite only the bounded direct-navigation references that should now open the moved support-only body
- [ ] retain one cleanup manifest that lists stub-kept citations versus retargeted full-body citations

## Stop Rules

- stop if the root stub cannot preserve readable old-ID landing for one or more preserved legacy readers
- stop if execution requires broad reader-surface rewrites instead of bounded direct-navigation rewrites
- stop if the model would force `docs/governance/contracts/support-only/` to act like a second front door instead of a support-only retained-body surface