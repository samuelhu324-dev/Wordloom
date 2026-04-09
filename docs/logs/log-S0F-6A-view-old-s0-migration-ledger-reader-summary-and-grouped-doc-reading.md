# log-S0F-6A (Phase 6A: view-old-S0 migration ledger reader summary and grouped DOC reading)

---

**id**: `S0F-6A`
**kind**: `log`
**title**: `view-old-S0 migration ledger reader summary and grouped DOC reading v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Views, Reader, Summary, epic/s0, sub/6a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_1**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_2**: `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  **reference_log_3**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_4**: `docs/governance/views/view-doc-history-and-lineage-v1.md`
  **reference_log_5**: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
**issue_keyword**: `view`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/6`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-09`
**updated**: `2026-04-09`

---

## Decision / Outcome

**Decision**:

- `S0F-6A` opens as the bounded follow-up after `S0F-5B/P4-C6` because the repo now has one real old-`S0 -> DOC` migration ledger, but its reader-facing surface is still stronger at row inventory than at fast human orientation.
- This slice does not widen migration coverage.
- It strengthens how readers consume the already-admitted `DOC` absorption state by adding one grouped reader summary to `view-old-s0-migration-ledger-v1.md`.
- The grouped summary is now fixed around current `DOC` reading classes rather than around source chronology alone:
  - `contract` reading
  - `history` view reading
  - `promotion-map` view reading

**Default choices (phase defaults / v1)**:

- Keep the migration ledger row table as the canonical bounded projection.
- Add grouped reader summaries above the row table instead of replacing the row table.
- Group by current reader-facing `DOC` surface class first, because that is the shortest path for human readers asking `where should this old S0 meaning be read now?`
- Do not duplicate support-only blocker prose or source-log evidence into the grouped summary.
- Keep `contract`, `history view`, and `promotion-map view` as separate reading groups even when they all belong to `DOC`.

## Problem Statement

- `S0F-5B` already solved the ledger-model problem and admitted real migration rows.
- The remaining weakness is reader speed, not ledger shape.
- A human reader can now answer the migration question by scanning the row table, but the view still makes readers do their own grouping work when the real question is:
  - which old `S0` surfaces now read through current `DOC` contracts?
  - which ones now read through the `DOC` history surface?
  - which ones now read through the `DOC` promotion map?
- Without one grouped reader summary, the migration view is correct but still slower than it should be for repeated governance reading.

## PR Summary Inputs (optional)

- Use this block because `S0F-6A` is expected to enhance the reader-facing migration view rather than reopen migration-row admission.

**PR summary bullets**:

- Define one grouped reader-summary contract for `view-old-s0-migration-ledger-v1.md`.
- Group current `DOC` absorption by reading class rather than leaving readers to infer the grouping from the row table.
- Land the first grouped summary without widening migration coverage or changing support-only ledger ownership.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the migration-view enhancement lane.

**PR links**:

- Log: `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`
- Previous log: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`

## Exported Sections / Outlet Ownership

- This slice enhances one existing reader-facing view and does not reopen migration-row admission.

**Outlet ownership**:

- `contract`: no-op; this slice does not create or revise current `DOC` contracts
- `runbook`: no-op; this slice fixes reader summary shape rather than operator procedure
- `view`: landed as an enhanced grouped reader summary in `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `index/front-door`: no-op; the migration ledger remains discoverable through its existing path and parent lineage
- `disposition/placement`: no-op; no row standing or placement outcome changes in this slice
- `log-retained core`: keep this source log for grouped-summary contract, execution notes, and next-step boundary

## Definitions (optional)

- **grouped reader summary**: a bounded summary layer above the migration-row table that groups already-admitted rows by the current `DOC` reading surface a human should open first
- **reader-surface class**: one stable reading bucket such as `contract`, `history view`, or `promotion-map view`

## Constraints

- Do not widen migration coverage in this slice.
- Do not mutate support-only row semantics or standing values in this slice.
- Do not replace the canonical row table with grouped prose.
- Do not collapse different `DOC` reader surfaces into one generic `view` bucket.

## Scope

- `P0`: open `S0F-6A`, wire it into the parent spine, and fix the problem as `reader summary enhancement` work rather than migration widening
- `P1`: define the grouped reader-summary contract for the migration view
- `P2`: land the first grouped `DOC` reading summary in `view-old-s0-migration-ledger-v1.md`

## Success Criteria (DoD)

- One reader can identify the current `DOC` reading path class without scanning the whole row table manually.
- The grouped summary stays consistent with the canonical row table instead of becoming a second competing ledger.
- `contract`, `history view`, and `promotion-map view` remain visibly distinct reading groups.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the grouped reader-summary contract is explicit enough to reuse
  - the first grouped `DOC` reading summary is landed in the migration view
  - later enhancement work no longer needs to reopen whether grouped reading belongs in the migration view at all

## P0 (Contract | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-6A` is now opened as the migration-view reader-summary enhancement lane.
- This slice does not admit new migration rows.
- It fixes how already-admitted rows should be grouped for faster human reading.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now:
  - define the grouped reader-summary contract
  - land one first grouped `DOC` reading summary in the migration view

## P1 (Grouped summary contract)

### P1-C1-S1 (Grouped reader-summary contract fixed | v1)

- The migration view now may carry one grouped reader summary above the canonical row table.
- The grouped summary should answer:
  - which rows now read through current `DOC` contracts
  - which rows now read through the `DOC` history view
  - which rows now read through the `DOC` promotion-map view
- The grouped summary remains a reader layer only:
  - no blocker prose
  - no alternate-candidate debate
  - no replacement for the row table

### P1-C1-S2 (Group boundary fixed | v1)

- The first grouped summary boundary is fixed as:
  - `contract-first DOC reading`
  - `history-view DOC reading`
  - `promotion-map-view DOC reading`
- Within each group, list only the already-admitted source surfaces and the current reader-facing target that now owns the reading job.
- Keep counts visible so readers can reconcile the grouped summary against the row table quickly.

## P2 (First grouped DOC reading summary)

### P2-C1-S1 (Grouped DOC reader summary landed | v1)

- `view-old-s0-migration-ledger-v1.md` now carries a grouped `DOC` reading summary above the canonical row table.
- The grouped summary now exposes:
  - one `contract` group for current rule reading
  - one `history view` group for lineage and history reading
  - one `promotion-map view` group for landed promotion-packet reading

### P2-C1-S2 (Reader-speed boundary fixed | v1)

- After `P2`, a reader no longer needs to infer all major `DOC` grouping from the row table alone.
- The row table remains the canonical bounded projection.
- The new grouped summary is now the fastest entrypoint for `which DOC reading surface should I open first?`

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Grouped summary contract)

- [x] `P1-C1-S1`: grouped reader-summary contract fixed
- [x] `P1-C1-S2`: group boundary fixed

### P2 (First grouped DOC reading summary)

- [x] `P2-C1-S1`: grouped DOC reader summary landed
- [x] `P2-C1-S2`: reader-speed boundary fixed

## Current Status (recommended)

- `S0F-6A` is now opened as the bounded follow-up for migration-view reader summary enhancement.
- `P0` is now complete: the slice is fixed as reader-summary work rather than row-widening work.
- `P1` is now complete: the grouped reader-summary contract and first group boundary are explicit enough to reuse.
- `P2` is now complete: the first grouped `DOC` reading summary is landed in the migration view.
- `S0F-6A` is now `stable`.
- The next step is no longer whether grouped reading belongs in the view; it is whether later follow-up should add more grouped reader classes or keep widening migration coverage itself.

## Evidence (reserved)

### P0-P2-C1-S1S2 (S0F-6A scaffold and first grouped reader summary landed | 2026-04-09)

- headSha: `<pending commit for S0F-6A/P0-P2-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`
  - `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the migration view gains one reader-speed layer without reopening migration-row admission
  - grouped `DOC` reading classes remain visibly distinct and reconcilable with the canonical row table
- observed:
  - `S0F-6A` now owns the grouped reader-summary contract and execution notes
  - the migration view now groups current `DOC` absorption by `contract`, `history view`, and `promotion-map view`
  - the canonical row table remains intact under the grouped reader summary

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-6A` as the bounded follow-up for migration-view reader summary enhancement rather than further migration-row widening.
- 2026-04-09: completed `P1` by fixing the grouped reader-summary contract and the first `DOC` reader-surface group boundary.
- 2026-04-09: completed `P2` by landing the first grouped `DOC` reading summary in `view-old-s0-migration-ledger-v1.md`.