# log-S0F-6A (Phase 6A: view-old-S0 migration ledger reader summary and grouped DOC reading)

---

**id**: `S0F-6A`
**kind**: `log`
**title**: `view-old-S0 migration ledger reader summary and grouped DOC reading v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Views, Reader, Summary, epic/s0, sub/6a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/388`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/391`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_1**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_2**: `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  **reference_log_3**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_4**: `docs/governance/views/view-doc-history-and-lineage-v1.md`
  **reference_log_5**: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
**issue_keyword**: `records`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M2`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-09`
**updated**: `2026-04-14`

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
- `P3`: define per-group reader-path notes and handoff order so each grouped class tells readers what to open next
- `P4`: add one question-first reader decision block so readers can route by intent before scanning the grouped classes
- `P5`: run the publish close-out review and answer the six outlets explicitly before holding the lane as a released `view` enhancement

## Success Criteria (DoD)

- One reader can identify the current `DOC` reading path class without scanning the whole row table manually.
- The grouped summary stays consistent with the canonical row table instead of becoming a second competing ledger.
- `contract`, `history view`, and `promotion-map view` remain visibly distinct reading groups.
- One reader can tell what to open first and what to open next for each grouped reading class without inferring the handoff from other files.
- One reader can start from a concrete question and jump to the right current `DOC` surface without first translating that question into one of the grouped classes.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the grouped reader-summary contract is explicit enough to reuse
  - the first grouped `DOC` reading summary is landed in the migration view
  - the grouped classes carry enough reader-path guidance that later readers do not need to improvise the next hop
  - the view also exposes one compact question-first decision layer for readers who think in questions rather than class names
  - the six-outlet publish close-out review is explicit, with justified `no-op` answers where no further export is warranted
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

## P3 (Reader-path notes and handoffs)

### P3-C1-S1 (Per-group reader-path notes fixed | v1)

- Each grouped `DOC` reading class may now carry one short note answering:
  - when to use this group
  - what to open first
- These notes stay reader-facing and must not duplicate source-log evidence or support-only row commentary.

### P3-C1-S2 (Per-group handoff order fixed | v1)

- The grouped summary may now state one bounded `open first -> then open` sequence for each reading class.
- The first fixed handoff order is now:
  - `contract` group: current `DOC` front door or the listed contract body first, then retained source-owner trace only if needed
  - `history view` group: `view-doc-history-and-lineage-v1` first, then retained source-owner chronology if needed
  - `promotion-map view` group: `view-doc-contract-promotion-map-v1` first, then the landed current contract or front door if needed
- This keeps the migration view self-sufficient for fast reader routing while preserving the row table as the canonical projection.

## P4 (Question-first reader decision block)

### P4-C1-S1 (Decision-block contract fixed | v1)

- The migration view may now carry one compact decision block above the grouped classes.
- The block should start from natural reader questions, not from migration-row fields.
- The first decision-block questions are now fixed as:
  - `what is true now?`
  - `how did this DOC surface emerge?`
  - `which lane or packet landed this DOC result?`
  - `where is the full migration inventory?`
- Each question should point to one first-open surface only, with one short reason.

### P4-C1-S2 (Decision-block landed | v1)

- `view-old-s0-migration-ledger-v1.md` now carries one question-first reader decision block above the grouped classes.
- This block does not replace the grouped classes.
- It exists so a reader can route from intent first, then use the grouped classes and row table only if more detail is needed.

### P4-C2-S1 (Completion-summary contract fixed | v1)

- The migration view may now carry one compact completion summary near the `DOC Absorption Snapshot`.
- This summary should answer three bounded reader questions directly:
  - `how far has current DOC contract absorption completed on the currently surfaced set?`
  - `how far has current DOC view absorption completed on the currently surfaced set?`
  - `what rough backlog classes remain outside the current surfaced set?`
- The completion summary stays reader-facing:
  - it summarizes the already-admitted row set
  - it does not replace the canonical row table
  - it does not claim whole-repo migration completion beyond the current `DOC` surfaced set

### P4-C2-S2 (Completion summary landed | v1)

- `view-old-s0-migration-ledger-v1.md` now carries one completion summary that answers current `contract` absorption, current `view` absorption, and the rough remaining backlog classes directly.
- This summary is intentionally framed as `current DOC surfaced coverage`, not as whole-repo old-`S0` migration completion.
- Readers can now see, in one place, both:
  - where current `DOC` absorption is already complete on the surfaced set
  - and why some remaining backlog is still outside this view until one later lane creates a new current-surface concentration point

## P5 (Publish close-out review)

### P5-C1-S1 (Six-outlet close-out review completed | v1)

- `S0F-6A` now completes its publish close-out review by answering the six outlets explicitly:
  - `contract`: no-op; this slice does not change current `DOC` rule text, contract shape, or contract history blocks
  - `runbook`: no-op; this slice does not define a stable operator procedure
  - `view`: keep the landed enhancement in `view-old-s0-migration-ledger-v1.md` as the released reader-facing result
  - `index/front-door`: no-op; the migration view remains reachable through existing lineage and does not require a broader navigation mutation in this slice
  - `disposition/placement`: no-op; this slice does not change row standing, support-only placement, or cleanup status
  - `log-retained core`: keep this source log for the grouped-summary contract, release rationale, and the boundary explaining why this lane publishes a `view` enhancement rather than a contract change
- This makes the release boundary explicit: `S0F-6A` publishes reader routing, not new `DOC` rule content.

### P5-C1-S2 (Post-release boundary fixed | v1)

- After `P5`, `S0F-6A` should be held as one released `view` enhancement lane rather than widened indefinitely.
- Any later work should reopen only for one clearly different question, such as:
  - additional reader question classes
  - a new front-door export need
  - or a downstream contract/history-lane change that genuinely alters the right first-open routing
- This prevents the lane from drifting from `reader routing release` into open-ended migration or contract evolution work.

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

### P3 (Reader-path notes and handoffs)

- [x] `P3-C1-S1`: per-group reader-path notes fixed
- [x] `P3-C1-S2`: per-group handoff order fixed

### P4 (Question-first reader decision block)

- [x] `P4-C1-S1`: decision-block contract fixed
- [x] `P4-C1-S2`: decision block landed
- [x] `P4-C2-S1`: completion-summary contract fixed
- [x] `P4-C2-S2`: completion summary landed

### P5 (Publish close-out review)

- [x] `P5-C1-S1`: six-outlet close-out review completed
- [x] `P5-C1-S2`: post-release boundary fixed

## Current Status (recommended)

- `S0F-6A` is now opened as the bounded follow-up for migration-view reader summary enhancement.
- `P0` is now complete: the slice is fixed as reader-summary work rather than row-widening work.
- `P1` is now complete: the grouped reader-summary contract and first group boundary are explicit enough to reuse.
- `P2` is now complete: the first grouped `DOC` reading summary is landed in the migration view.
- `P3` is now complete: each grouped reading class now carries one bounded reader-path note and one fixed handoff order, so the migration view can route readers directly instead of only grouping rows.
- `P4` is now complete: the migration view now also carries one question-first decision block plus one completion summary, so readers can route by intent and also see current `contract` versus `view` absorption completion on the surfaced set before choosing a grouped reading class.
- `P5` is now complete: the six-outlet publish close-out review is explicit, the released result is fixed as one `view` enhancement, and all other outlets are justified `no-op`.
- `S0F-6A` is now `stable`.
- The next step is no longer whether grouped reading belongs in the view; it is whether a later bounded lane should add more question classes, refine the surfaced completion summary further, publish a broader front-door export, or return to migration-row widening itself.

## Evidence (reserved)

### P0-P5-C1-S1S2 (S0F-6A scaffold, grouped summary, handoffs, decision block, and publish close-out landed | 2026-04-09)

- headSha: `<pending commit for S0F-6A/P0-P5-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`
  - `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the migration view gains one reader-speed layer without reopening migration-row admission
  - grouped `DOC` reading classes remain visibly distinct and reconcilable with the canonical row table
  - each grouped class tells readers what to open first and what to open next
  - one compact question-first block routes readers who start from intent rather than grouped class names
  - the six outlets are explicitly closed so the lane can publish as a `view` enhancement without pretending to be a contract or runbook change
- observed:
  - `S0F-6A` now owns the grouped reader-summary contract and execution notes
  - the migration view now groups current `DOC` absorption by `contract`, `history view`, and `promotion-map view`
  - the grouped classes now also carry explicit reader-path notes and handoff order
  - the view now also exposes one question-first decision block for direct routing by reader intent
  - the publish close-out review now fixes `view` as the only landed outlet and records justified `no-op` for the other five outlets
  - the canonical row table remains intact under the grouped reader summary

### P4-C2-S1S2 (Surfaced completion summary landed | 2026-04-09)

- headSha: `<pending commit for S0F-6A/P4-C2-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`
  - `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the migration view should answer not only `which surface should I open first?` but also `how complete is current DOC absorption on the surfaced set?`
  - the answer should separate current `contract` absorption, current `view` absorption, and rough remaining backlog classes without pretending the whole old-`S0` repo-wide migration is finished
- observed:
  - the migration view now states the completed `contract`-absorbed set, the completed `view`-absorbed set, and the rough remaining backlog classes explicitly
  - the summary stays bounded to the current surfaced set and does not replace the canonical row table or support-only ledger
  - readers can now distinguish `current surfaced coverage complete for v1` from `whole old-S0 migration complete`, which the view still does not claim

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-6A` as the bounded follow-up for migration-view reader summary enhancement rather than further migration-row widening.
- 2026-04-09: completed `P1` by fixing the grouped reader-summary contract and the first `DOC` reader-surface group boundary.
- 2026-04-09: completed `P2` by landing the first grouped `DOC` reading summary in `view-old-s0-migration-ledger-v1.md`.
- 2026-04-09: completed `P3` by fixing per-group reader-path notes and handoff order so the grouped summary now routes readers to the right next surface directly.
- 2026-04-09: completed `P4` by landing one question-first decision block so readers can route by intent before using the grouped classes or canonical row table.
- 2026-04-09: completed `P5` by fixing the six-outlet publish close-out review and holding `S0F-6A` as one released `view` enhancement lane.
- 2026-04-09: completed `P4-C2` by landing one surfaced completion summary that states current `contract` absorption, current `view` absorption, and the rough remaining backlog classes directly inside the migration view.