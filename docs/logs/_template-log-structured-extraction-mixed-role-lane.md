# log-<owner-id>-run-<n>-<mixed-role-slug> (structured extraction mixed-role lane)

---

**id**: `<owner-id>-run-<n>`
**kind**: `log`
**title**: `structured extraction mixed-role lane <short purpose> v1`
**status**: `draft`
**scope**: `<owner-family>`
**links**: ``
  **parent_log**: `<parent spine or active family log path>`
  **origin_log**: `<origin control slice or source-owner log path>`
  **reference_log_1**: `docs/logs/log-S0F-3H-recurring-governance-run-model-and-ledger-split.md`
  **reference_log_2**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  **reference_log_3**: `<current mixed-role source log path>`
  **reference_log_4**: `<current blocker manifest or dependency inventory path>`

---

## Why This Mixed-Role Lane Exists

- `<one bounded reason this source cannot be cleaned up safely without export-first discipline>`

## Mixed-Role Symptoms

- the retained source still mixes one or more of:
  - stable current rule ownership
  - stable operator procedure
  - reader-facing family summary
  - historical repair or convergence ledger
  - exact-path discoverability needed by lifecycle artifacts

## Package Boundary

- target owner:
  - `<owner-id>`
- package type:
  - `mixed-role structured extraction`
- explicit goal:
  - export stable responsibilities first, then thin the retained log, then judge disposition only after remaining blockers are explicit
- explicit non-goal:
  - do not force relocation merely because the source looks old

## Current Blockers

- exact-path consumers:
  - `<runbook | contract | lineage | issue | pr-prep | other>`
- unresolved outlet identities:
  - `<missing stable runbook | missing current contract | missing summary surface | none>`
- current disposition standing:
  - `<defer cleanup | keep current | ...>`

## Export-First Plan

- `contract`:
  - `<what stable current rule must leave first>`
- `runbook`:
  - `<what stable procedure must leave first>`
- `index/front-door`:
  - `<what current navigation change is required>`
- `view`:
  - `<what summary is justified, or why no view should be created>`
- `log rewrite`:
  - `<what content remains as slice-local ledger plus minimum bridge notes only>`
- `disposition/placement`:
  - `<what later file-state decision becomes eligible only after blocker reduction>`

## Stop Rules

- stop if the supposed target outlet still lacks stable identity
- stop if the remaining blockers are still current exact-path consumers rather than cleanup-local residue
- stop if the package starts acting like a new policy slice instead of one bounded extraction run

## Allowed Writes

- allowed:
  - `<export current rule>`
  - `<export stable procedure>`
  - `<thin retained log>`
  - `<record blocker reduction in manifest>`
- non-writes:
  - `<no relocation before blocker set is reduced>`
  - `<no archive-first solution>`
  - `<no duplicate summary surface unless a real reader need exists>`

## Residual Blocker Ledger

- keep after close-out:
  - `<remaining exact-path consumers>`
  - `<remaining lifecycle artifacts>`
  - `<what still keeps disposition at defer cleanup if applicable>`

## Naming Samples

- bounded execution log:
  - `log-<owner-id>-run-<n>-<mixed-role-slug>.md`
- likely mixed-role sample shape:
  - `log-S0F-1I-run-1-lifecycle-exact-path-successor-package.md`
- possible support-only destination after later success:
  - `docs/logs/support-only/<scope>/log-<slice-id>-<summary>.md`

## Validation

- `<current rule no longer depends on the retained log as the live owner>`
- `<stable procedure no longer depends on the retained log as the live owner>`
- `<retained log now reads as slice-local ledger>`
- `<remaining blockers, if any, are explicit rather than implied>`

## Evidence

- headSha:
  - `<git sha>`
- artifacts:
  - `<blocker manifest path>`
  - `<dependency inventory path>`
