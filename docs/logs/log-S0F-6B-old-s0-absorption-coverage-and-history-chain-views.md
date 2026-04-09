# log-S0F-6B (Phase 6B: old-S0 absorption coverage and history-chain views)

---

**id**: `S0F-6B`
**kind**: `log`
**title**: `old-S0 absorption coverage and history-chain views v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Views, History, Lineage, Inventory, epic/s0, sub/6b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`
  **reference_log_1**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_2**: `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`
  **reference_log_3**: `docs/governance/views/view-old-s0-migration-ledger-v1.md`
  **reference_log_4**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_5**: `docs/governance/views/view-doc-history-and-lineage-v1.md`
  **reference_log_6**: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
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

- `S0F-6B` opens as the bounded follow-up after `S0F-6A` because the repo now has one reader-facing old-`S0 -> DOC` migration ledger, but it still lacks one layered reader surface for these larger questions:
  - how much of old `S0` is absorbed at all
  - how absorption status distributes by series such as `S0B`, `S0C`, `S0D`, `S0E`, and `S0F`
  - how each old `S0` log currently reads: current contract, current view, retained evidence, history lineage, retired lineage, no-op, or unreviewed
  - how one current `DOC` surface evolved through older source-owner logs rather than existing as a static current body only
- This slice does not reopen current `DOC` contract text first.
- It fixes the next missing reader layer as one bounded `view` problem: coverage overview, series drill-down, and contract-history-chain reading.
- This same slice now reopens in `C2` to execute the second bounded contract-history-chain pilot instead of opening one more near-duplicate follow-up slice:
  - current `DOC` surface: `DOC-SLC-0001`
  - second bounded history-chain target: `docs/governance/views/view-old-s0-contract-history-chain-doc-slc-0001-v1.md`
- The second bounded contract-history-chain pilot is now complete and remains inside the already-stabilized `S0F-6B` row contract and routing model.
- This same slice now reopens in `C3` to execute the third bounded contract-history-chain pilot instead of opening one more near-duplicate follow-up slice:
  - current `DOC` surface: `DOC-TAX-0001`
  - third bounded history-chain target: `docs/governance/views/view-old-s0-contract-history-chain-doc-tax-0001-v1.md`
- The third bounded contract-history-chain pilot is now complete and remains inside the already-stabilized `S0F-6B` row contract and routing model.

**Default choices (phase defaults / v1)**:

- Do not overload `view-old-s0-migration-ledger-v1.md` with every reader job.
- Prefer layered reader-facing `view` surfaces over one giant mixed table.
- Keep current-rule reading in current `DOC` contracts and `view-doc-current-front-door-v1.md`.
- Keep mutable working judgment in the support-only migration inventory.
- Use new reader-facing `view` surfaces to explain coverage, per-series standing, and historical chain meaning for old `S0` material that is no longer the current rule SoT.

## Problem Statement

- `S0F-5B` fixed the migration-ledger model and `S0F-6A` improved reader routing for the already-admitted surfaced set.
- The remaining gap is no longer `which current DOC surface should I open first?`
- The remaining gap is deeper historical readability:
  - what is the total old-`S0` coverage picture
  - how much of each series has been absorbed or remains outside the current surfaced set
  - what is the current standing of each individual old log
  - how one current `DOC` contract or reader surface evolved through older logs, promotions, consolidations, retirements, and lineage transitions
- Without this layer, readers can see the current surfaced set but still cannot read old-`S0` history as one coherent absorption-and-evolution story.

## PR Summary Inputs (optional)

- Use this block because `S0F-6B` is expected to define the next reader-facing `view` layer for old-`S0` absorption coverage and history-chain reading.

**PR summary bullets**:

- Define the layered `view` split for old-`S0` absorption coverage, series drill-down, and contract-history-chain reading.
- Fix the minimum reader-facing standing vocabulary for per-log absorption status.
- Sequence the next work so coverage overview, series drill-down, and history-chain reading land as separate bounded reader surfaces rather than one giant mixed ledger.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the `view` layering lane.

**PR links**:

- Log: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- Previous log: `docs/logs/log-S0F-6A-view-old-s0-migration-ledger-reader-summary-and-grouped-doc-reading.md`

## Exported Sections / Outlet Ownership

- This slice is expected to define additional reader-facing `view` surfaces and does not reopen current `DOC` contract text directly.

**Outlet ownership**:

- `contract`: no-op; this slice does not directly create or revise current `DOC` contract bodies
- `runbook`: no-op; this slice fixes reader-facing historical navigation rather than operator procedure
- `view`: landed as `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`, `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`, `docs/governance/views/view-old-s0-contract-history-chain-doc-drb-0001-v1.md`, `docs/governance/views/view-old-s0-contract-history-chain-doc-slc-0001-v1.md`, and now `docs/governance/views/view-old-s0-contract-history-chain-doc-tax-0001-v1.md`; later bounded follow-up views may widen series coverage and current-surface history-chain coverage
- `index/front-door`: no-op for now; broader navigation changes should occur only if later reader routing proves they are warranted
- `disposition/placement`: no-op for now; mutable review standing remains owned by the support-only migration inventory
- `log-retained core`: keep this source log for the layered-view contract, standing vocabulary, reader-boundary rationale, and stop conditions

## Definitions (optional)

- **coverage overview**: one reader-facing summary that answers total old-`S0` absorption counts and series-level distribution without replaying per-log detail
- **series drill-down**: one reader-facing view that shows per-log standing inside one series such as `S0B` or `S0C`
- **contract-history chain**: one reader-facing chain that lets a reader start from a current `DOC` surface and trace back its older source-owner, promotion, lineage, and retirement history
- **reader-facing standing**: one bounded current-reading classification for an old log such as `current-contract`, `current-view`, `retained-evidence`, `history-lineage`, `retired-lineage`, `no-op`, `non-doc`, or `unreviewed`

## Constraints

- Do not turn one reader-facing view into a second support-only working ledger.
- Do not claim whole-repo old-`S0` completion before per-series standing and review state are explicit.
- Do not collapse `current contract`, `history lineage`, and `retired past-state meaning` into one generic `absorbed` label.
- Do not use current `DOC` contract bodies as the only place where historical evolution must be reconstructed.

## Scope

- `P0`: open `S0F-6B`, wire it into the parent spine, and fix the problem as one layered `view` lane for old-`S0` coverage and history-chain reading
- `P1`: define the layered `view` split and the minimum reader-facing standing vocabulary
- `P2`: land one coverage-overview `view` for old-`S0` total counts and series distribution
- `P3`: land one series drill-down `view` family or bounded equivalent for per-series and per-log standing
- `P4`: land one contract-history-chain `view` that lets readers start from current `DOC` surfaces and read backward through source-owner evolution
- `P5`: fix reader routing among those views and complete stable close-out review

## Success Criteria (DoD)

- One reader can answer how much of old `S0` has been absorbed without replaying the source logs manually.
- One reader can answer how much of one series such as `S0B` has been absorbed and what remains outside the current surfaced set.
- One reader can inspect one individual old log and see its current standing in bounded reader-facing vocabulary.
- One reader can start from a current `DOC` surface and read its historical chain without reconstructing the full sequence from raw source logs alone.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the layered `view` split is explicit enough to reuse
  - the minimum reader-facing standing vocabulary is explicit enough to apply consistently
  - at least one bounded coverage overview, one series drill-down shape, and one contract-history-chain shape are landed or explicitly held as the defended minimal publish set
  - later old-`S0` review work no longer needs to improvise whether coverage, per-log standing, or historical-chain reading belongs in one migration ledger, one contract body, or one retained source log

## P0 (Contract | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-6B` is now opened as the old-`S0` absorption coverage and history-chain `view` lane.
- This slice does not start by widening the current migration ledger row set.
- It starts by fixing the missing reader-facing layer above the current surfaced set.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now:
  - define the layered `view` split
  - define the reader-facing standing vocabulary
  - decide the minimum first publish set among coverage overview, series drill-down, and contract-history-chain reading

## Plan (draft)

### P1 (Layered view split and standing vocabulary)

- `P1-C1-S1`: fix the layered `view` split for coverage overview, series drill-down, and contract-history-chain reading
- `P1-C1-S2`: fix the minimum reader-facing standing vocabulary for old-`S0` per-log reading

### P1-C1-S1 (Layered view split fixed | v1)

- The layered `view` split is now fixed as three distinct reader-facing jobs rather than one giant mixed ledger:
  - `coverage overview`:
    - answers `how much old S0 has been reviewed or absorbed at all?`
    - answers `how does that coverage distribute by series such as S0B/S0C/S0D/S0E/S0F?`
    - must stay aggregate-first rather than row-by-row
  - `series drill-down`:
    - answers `for one series, what is the standing of each individual old log now?`
    - answers `what is the current reading home for this specific old log?`
    - must stay per-log and series-bounded rather than whole-repo giant-table first
  - `contract-history chain`:
    - answers `starting from one current DOC surface, how did this current meaning emerge?`
    - answers `which old logs are primary predecessors, which are supporting lineage, and which are retired or superseded predecessors?`
    - must stay current-surface-first rather than source-log-first
- The three reader jobs are intentionally separate because they optimize for different reading questions:
  - coverage asks for counts and distribution
  - drill-down asks for per-log standing
  - history chain asks for evolution path from current meaning backward
- `view-old-s0-migration-ledger-v1.md` remains the bounded surfaced-coverage ledger and should not absorb all three jobs directly.

### P1-C1-S2 (Reader-facing standing vocabulary fixed | v1)

- The minimum reader-facing standing vocabulary for old-`S0` per-log reading is now fixed as:
  - `current-contract`:
    - the old log's current reading home is one active current `DOC` contract body
  - `current-view`:
    - the old log's current reading home is one active current `DOC` reader-facing `view`
  - `retained-evidence`:
    - the old log is still retained mainly for detailed chronology, rationale, or evidence after the current reading home has moved elsewhere
  - `history-lineage`:
    - the old log survives primarily as one historical link in the evolution chain of a current surface
  - `retired-lineage`:
    - the old log represents a prior or superseded state whose meaning remains historically relevant but is no longer current reading
  - `no-op`:
    - the old log has been reviewed and does not warrant one separate current absorption surface
  - `non-doc`:
    - the old log has been reviewed and does not primarily land under the current `DOC` family
  - `unreviewed`:
    - no defended reader-facing classification has been fixed yet
- This vocabulary is intentionally reader-facing rather than support-only:
  - it tells readers where the old log stands now
  - it does not replace support-only mutable states such as `provisional`, `blocked`, or `deferred`
- When later views show per-log standing, they should use this vocabulary for reader-facing classification and link back to support-only inventory only when mutable working status is needed.

### P2 (Coverage overview)

- `P2-C1-S1`: define the minimum field set for old-`S0` total and series-level coverage reading
- `P2-C1-S2`: land the first bounded coverage overview surface

### P2-C1-S1 (Coverage-overview field set fixed | v1)

- The minimum field set for the first bounded old-`S0` coverage-overview surface is now fixed as:
  - `series`
  - `in-scope old logs`
  - `currently surfaced`
  - `current-contract`
  - `current-view`
  - `remaining outside surfaced set`
- The first aggregate overview must also show repo-level totals for the same measures.
- The first coverage-overview population boundary is now fixed as:
  - top-level root `docs/logs/log-S0*.md` source logs under `S0B` through `S0F`
  - excluding parent spines such as `S0E-docs-management-v5` and `S0F-docs-management-v6`
  - excluding the current absorption-tracking lanes `S0F-5B`, `S0F-6A`, and `S0F-6B`
- `remaining outside surfaced set` is intentionally narrower than `unreviewed`:
  - it means `not currently admitted into the surfaced old-S0 -> DOC set`
  - it does not by itself decide whether the remainder is unreviewed, retained-only, non-`DOC`, or later-history material

### P2-C1-S2 (First bounded coverage overview landed | v1)

- The first bounded aggregate coverage-overview surface now exists at `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`.
- This first view answers:
  - how many old-`S0` logs are currently in the root review-scope population
  - how many are already absorbed into the current surfaced `DOC` set
  - how that surfaced absorption distributes by series
- This first view intentionally stops at aggregate coverage and series distribution.
- It does not yet try to answer per-log standing or current-surface historical chains; those remain sequenced into `P3` and `P4`.

### P3 (Series drill-down)

- `P3-C1-S1`: define the per-series and per-log standing field set
- `P3-C1-S2`: land the first bounded series drill-down surface or equivalent grouped shape

### P3-C1-S1 (Per-series drill-down field set fixed | v1)

- The minimum field set for the first bounded series drill-down surface is now fixed as:
  - `source log`
  - `series`
  - `currently surfaced`
  - `reader-facing standing`
  - `current family`
  - `current reading home`
  - `history role`
  - `notes`
- Field intent is now fixed as:
  - `currently surfaced`:
    - answers whether the log is already admitted into the current old-`S0 -> DOC` surfaced set
  - `reader-facing standing`:
    - uses the fixed vocabulary from `P1`
  - `current family`:
    - answers which current family presently owns the best defended reading home when such a home is known
  - `current reading home`:
    - names the current contract body, current `view`, or unresolved state rather than restating generic standing only
  - `history role`:
    - explains whether the log acts as structural prerequisite, lineage milestone, retained evidence, retired predecessor, or another bounded historical role
  - `notes`:
    - stays short and reader-facing; it must not become support-only blocker prose
- The first drill-down surface may leave some fields unresolved when a log is still `unreviewed`, but it must do so explicitly rather than silently omitting the row.

### P3-C1-S2 (First bounded series drill-down surface landed | v1)

- The first bounded series drill-down surface now exists at `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`.
- `S0B` is used as the first bounded pilot because it is the smallest current review-scope series and already shows two different states at once:
  - one row already surfaced into the current `DOC` history view
  - one row still outside the current surfaced set
- This first drill-down therefore proves that the per-log standing view can show both `current-view` and `unreviewed` without collapsing them into one generic `not yet absorbed` bucket.

### P4 (Contract-history chain)

- `P4-C1-S1`: define the current-surface-to-history-chain field set
- `P4-C1-S2`: land the first bounded contract-history-chain reading surface

### P4-C1-S1 (Current-surface-to-history-chain field set fixed | v1)

- The minimum field set for the first bounded contract-history-chain surface is now fixed as:
  - `current DOC surface`
  - `current outlet`
  - `history step`
  - `source surface`
  - `current standing now`
  - `relationship to current surface`
  - `why it matters now`
  - `deep chronology home`
- Field intent is now fixed as:
  - `current DOC surface`:
    - keeps the view current-surface-first rather than source-log-first
    - names the exact active `DOC` contract or current reader surface whose history is being traced
  - `current outlet`:
    - answers whether the current surface being traced is a `contract` or one reader-facing `view`
    - prevents the chain from silently mixing current contract history with current view history
  - `history step`:
    - gives one short bounded chain role such as `current rule`, `primary source-owner origin`, `promotion-home decision`, `promotion event`, `reader consolidation`, `history publication gate`, or `structural prerequisite`
  - `source surface`:
    - names the old-`S0` log or current `DOC` surface that occupies that chain step
  - `current standing now`:
    - uses the fixed reader-facing standing vocabulary from `P1`
    - makes it explicit whether the source now reads as `current-contract`, `current-view`, `retained-evidence`, or another defended standing
  - `relationship to current surface`:
    - states how that row connects to the named current surface rather than leaving readers to infer the role from chronology alone
  - `why it matters now`:
    - keeps one concise explanation of the present-day consequence of that predecessor or milestone
  - `deep chronology home`:
    - points readers to the retained source-owner log or current reader surface that should be opened for fuller chronology after the bounded chain has oriented them
- The first bounded contract-history-chain surface must stay current-surface-first and compressed:
  - include the direct source-owner and promotion chain first
  - include only the strongest supporting prerequisite or lineage rows needed to explain the current surface coherently
  - do not replay every intermediate edit or whole-family inventory row

### P4-C1-S2 (First bounded contract-history-chain surface landed | v1)

- The first bounded contract-history-chain surface now exists at `docs/governance/views/view-old-s0-contract-history-chain-doc-drb-0001-v1.md`.
- `DOC-DRB-0001` is used as the first pilot because it is the clearest current-surface-first case in the current `DOC` set:
  - it is the first promoted current `DOC` contract body
  - its retained source-owner origin is explicit at `S0F-4A`
  - its surrounding promotion-home, promotion-event, reader-consolidation, and history-publication nodes are already separately surfaced in the current `DOC` history layer
- This first bounded surface proves that one reader can start from one active current `DOC` contract, read backward through the direct source-owner and promotion chain, and then widen only as far as the strongest prerequisite and lineage milestones actually needed for comprehension.
- This first surface intentionally does not yet widen to the rest of the active `DOC` quartet or the issue-governance extension packet; later `P4` follow-up, if needed, should add additional current-surface pilots rather than turning the first chain into one giant family table.

### P4-C2-S1 (Second bounded contract-history-chain pilot admitted inside the same slice | v1)

- `S0F-6B` is now explicitly reopened in `C2` rather than in a new slice.
- The second active current-surface history-chain pilot is now fixed as:
  - current `DOC` surface: `DOC-SLC-0001`
  - retained source-owner origin: `S0F-4B`
  - bounded second chain target: `docs/governance/views/view-old-s0-contract-history-chain-doc-slc-0001-v1.md`
- Rationale:
  - `DOC-SLC-0001` is the cleanest second pilot because it shares the same promotion-home, promotion-event, reader-consolidation, and history-publication chain shape as `DOC-DRB-0001` while carrying a different current-rule concentration under `S0F-4B`
  - this makes it the strongest immediate test that `P4-C1` fixed one reusable current-surface-first row contract rather than one contract-specific one-off surface

### P4-C2-S2 (Second bounded contract-history-chain surface landed | v1)

- The second bounded contract-history-chain surface now exists at `docs/governance/views/view-old-s0-contract-history-chain-doc-slc-0001-v1.md`.
- This second surface proves that the same bounded chain model can be replayed on a second active `DOC` contract without reopening row shape, routing logic, or whole-family history design.
- The second surface intentionally remains current-contract-first and bounded:
  - it reuses the defended prerequisite and lineage packet already surfaced by the `DOC` family history view
  - it changes only the direct source-owner and current-rule concentration from `S0F-4A` / `DOC-DRB-0001` to `S0F-4B` / `DOC-SLC-0001`
  - it still does not widen to a whole quartet matrix inside one view

### P4-C3-S1 (Third bounded contract-history-chain pilot admitted inside the same slice | v1)

- `S0F-6B` is now explicitly reopened in `C3` rather than in a new slice.
- The third active current-surface history-chain pilot is now fixed as:
  - current `DOC` surface: `DOC-TAX-0001`
  - retained source-owner origin: `S0F-3I`
  - bounded third chain target: `docs/governance/views/view-old-s0-contract-history-chain-doc-tax-0001-v1.md`
- Rationale:
  - `DOC-TAX-0001` is the strongest third pilot because it keeps the same direct promotion skeleton while testing a different kind of current rule: family taxonomy, placement, and family-versus-level interpretation
  - this widens the history-chain sample set beyond role-boundary and source-log-compatibility rules without yet pulling in the extra transition-surface complexity around `DOC-FDT-0001`

### P4-C3-S2 (Third bounded contract-history-chain surface landed | v1)

- The third bounded contract-history-chain surface now exists at `docs/governance/views/view-old-s0-contract-history-chain-doc-tax-0001-v1.md`.
- This third surface proves that the same bounded chain model can also carry the taxonomy-and-placement rule set under `DOC-TAX-0001` without reopening field shape, routing logic, or whole-family history design.
- The third surface intentionally remains current-contract-first and bounded:
  - it reuses the defended prerequisite and lineage packet already surfaced by the `DOC` family history view
  - it changes only the direct source-owner and current-rule concentration from `S0F-4B` / `DOC-SLC-0001` to `S0F-3I` / `DOC-TAX-0001`
  - it still does not widen to a whole quartet matrix inside one view

### P5 (Reader routing and close-out)

- `P5-C1-S1`: fix reader routing among coverage, drill-down, and history-chain views
- `P5-C1-S2`: complete stable close-out review for the layered `view` lane

### P5-C1-S1 (Reader routing among layered views fixed | v1)

- The three landed reader-facing surfaces now have one explicit first-open split:
  - `coverage overview` answers aggregate scope and series distribution first
  - `series drill-down` answers per-log standing inside one series first
  - `contract-history chain` answers current-surface-first evolution for one current `DOC` surface first
- The routing rule is now:
  - if the reader asks `how much is absorbed overall?`, start at `view-old-s0-absorption-coverage-overview-v1.md`
  - if the reader asks `inside one series, what is the standing of each log?`, start at the matching series drill-down view such as `view-old-s0-series-s0b-standing-v1.md`
  - if the reader asks `how did one current DOC surface emerge?`, start at the matching contract-history-chain view such as `view-old-s0-contract-history-chain-doc-drb-0001-v1.md`
  - if the reader asks `which exact old-S0 rows are already admitted into the surfaced DOC set?`, start at `view-old-s0-migration-ledger-v1.md`
- This routing is intentionally view-layer-specific:
  - aggregate totals should not be reconstructed from one series drill-down
  - per-log standing should not be reconstructed from one current-surface chain
  - one current-surface chain should not be stretched into a whole-family or whole-backlog answer

### P5-C1-S2 (Six-outlet stable close-out review fixed | v1)

- The layered old-`S0` absorption view lane is now execution-complete in this slice.
- `P5` does not open one further expansion tail before close-out.
- It fixes the stable close-out answer across the six outlets as follows:
  - `contract`: no-op because this lane only adds reader-facing historical and standing views; current `DOC` contract bodies remain unchanged here
  - `runbook`: no-op because no reusable operator procedure was introduced beyond the slice-local reading contract
  - `view`: complete because the defended minimal publish set is now landed as one coverage overview, one bounded series drill-down surface, and one bounded contract-history-chain surface with explicit routing among them
  - `index/front-door`: no-op because the current minimal publish set does not require broader directory-entry mutation to remain readable
  - `disposition/placement`: no-op because mutable review and placement standing remain owned by the support-only migration inventory rather than by this reader-facing lane
  - `log-retained core`: keep, because this source log remains the right owner for the layered-view contract, standing vocabulary, routing rationale, close-out boundary, and evidence
- This means `S0F-6B` closes as `stable retained-log close-out`, not as another widening or routing-expansion lane.

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Layered view split and standing vocabulary)

- [x] `P1-C1-S1`: layered `view` split fixed
- [x] `P1-C1-S2`: reader-facing standing vocabulary fixed

### P2 (Coverage overview)

- [x] `P2-C1-S1`: coverage-overview field set fixed
- [x] `P2-C1-S2`: first bounded coverage overview landed

### P3 (Series drill-down)

- [x] `P3-C1-S1`: per-series drill-down field set fixed
- [x] `P3-C1-S2`: first bounded series drill-down surface landed

### P4 (Contract-history chain)

- [x] `P4-C1-S1`: contract-history-chain field set fixed
- [x] `P4-C1-S2`: first bounded contract-history-chain surface landed
- [x] `P4-C2-S1`: second bounded contract-history-chain pilot admitted inside the same slice
- [x] `P4-C2-S2`: second bounded contract-history-chain surface landed
- [x] `P4-C3-S1`: third bounded contract-history-chain pilot admitted inside the same slice
- [x] `P4-C3-S2`: third bounded contract-history-chain surface landed

### P5 (Reader routing and close-out)

- [x] `P5-C1-S1`: reader routing fixed among layered views
- [x] `P5-C1-S2`: stable close-out review completed

## Current Status (recommended)

- `S0F-6B` is now opened as the bounded follow-up for old-`S0` absorption coverage and history-chain `view` layering.
- `P0` is now complete: the problem is fixed as one reader-facing `view` layering gap above the current surfaced migration set, not as immediate contract mutation or ad hoc row widening.
- `P1` is now complete: the layered `view` split and the minimum reader-facing standing vocabulary are now explicit enough to reuse.
- `P2` is now complete: the minimum field set for one bounded aggregate coverage-overview surface is fixed, and the first aggregate old-`S0` absorption coverage view is now landed.
- `P3` is now complete: the per-series and per-log standing field set is fixed, and the first bounded `S0B` series drill-down surface is now landed.
- `P4` is now complete: the current-surface-to-history-chain field set is fixed, and the first bounded `DOC-DRB-0001` contract-history-chain surface is now landed.
- `S0F-6B` is now reopened in `C2` rather than in a new slice: the second bounded current-surface history-chain pilot is fixed as `DOC-SLC-0001` and is now landed under the already-stable `P4` row contract.
- `S0F-6B` is now reopened in `C3` rather than in a new slice: the third bounded current-surface history-chain pilot is fixed as `DOC-TAX-0001` and is now landed under the already-stable `P4` row contract.
- `P5` is now complete: reader routing among the coverage overview, series drill-down, and contract-history-chain layers is now explicit, and the stable close-out review is now answered across the six outlets.
- `S0F-6B` is now `stable`.
- No further implementation tail is required inside this lane before later widening by additional series drill-down views or additional current-surface history-chain pilots.

## Evidence (reserved)

### P0-C1-S1S2 (S0F-6B scaffold and immediate sequencing landed | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one explicit lane for the missing reader-facing layer above the current old-`S0 -> DOC` surfaced set
  - later work no longer needs to improvise whether old-`S0` coverage, per-series standing, and historical-chain reading belong in one migration ledger, one contract body, or one retained source log
- observed:
  - `S0F-6B` is now opened as the layered `view` lane for old-`S0` coverage and historical-chain reading
  - the immediate next work is now the layered `view` split and standing vocabulary rather than direct per-series file proliferation

### P1-C1-S1S2 (Layered view split and reader-facing standing vocabulary fixed | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - later coverage, series drill-down, and contract-history-chain surfaces should inherit one fixed split of reader jobs rather than improvising mixed tables
  - later per-log reader-facing standing should use one consistent bounded vocabulary instead of ad hoc prose labels
- observed:
  - `coverage overview`, `series drill-down`, and `contract-history chain` are now fixed as three separate reader-facing jobs with explicit question boundaries
  - the minimum reader-facing standing vocabulary is now fixed as `current-contract`, `current-view`, `retained-evidence`, `history-lineage`, `retired-lineage`, `no-op`, `non-doc`, and `unreviewed`
  - later view landing work can now define fields and concrete files without reopening these boundary questions first

### P2-C1-S1S2 (Coverage-overview field set fixed and first aggregate view landed | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P2-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - readers should be able to see one bounded aggregate answer for how much old-`S0` is in scope and how much of that scope is already absorbed into the current surfaced `DOC` set
  - the aggregate answer should distribute by series without pretending to answer per-log standing already
- observed:
  - the minimum field set for aggregate old-`S0` coverage reading is now fixed as `series`, `in-scope old logs`, `currently surfaced`, `current-contract`, `current-view`, and `remaining outside surfaced set`
  - the first aggregate old-`S0` absorption coverage view is now landed and shows both repo-level totals and per-series distribution across `S0B` through `S0F`
  - the first aggregate view now answers coverage and distribution while explicitly holding per-log standing and current-surface historical chains for later phases

### P3-C1-S1S2 (Per-series drill-down field set fixed and first bounded S0B surface landed | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P3-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - later series drill-down surfaces should inherit one fixed per-log field set rather than improvising row shape per series
  - the first bounded drill-down surface should prove that the reader-facing standing vocabulary can show mixed states inside one real series
- observed:
  - the minimum per-series/per-log field set is now fixed as `source log`, `series`, `currently surfaced`, `reader-facing standing`, `current family`, `current reading home`, `history role`, and `notes`
  - the first bounded `S0B` drill-down surface is now landed and shows one surfaced `current-view` row plus one row still outside the surfaced set as explicit `unreviewed`
  - later series drill-down work can now widen by series without reopening row-shape or standing-display questions first

### P4-C1-S1S2 (Contract-history-chain field set fixed and first bounded DOC-DRB-0001 surface landed | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P4-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/governance/views/view-old-s0-contract-history-chain-doc-drb-0001-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - later contract-history-chain surfaces should inherit one fixed current-surface-first row contract rather than improvising one new chain shape per current `DOC` surface
  - the first bounded history-chain pilot should prove that readers can start from one current `DOC` contract and trace back through direct origin, promotion, consolidation, and strongest prerequisite context without replaying the whole family history view first
- observed:
  - the minimum current-surface-to-history-chain field set is now fixed as `current DOC surface`, `current outlet`, `history step`, `source surface`, `current standing now`, `relationship to current surface`, `why it matters now`, and `deep chronology home`
  - the first bounded `DOC-DRB-0001` history-chain surface is now landed and compresses direct source-owner origin, promotion-home, promotion-event, reader-consolidation, history-publication, and prerequisite context into one current-surface-first chain
  - later history-chain work can now widen by additional current `DOC` surfaces without reopening whether the chain should be source-log-first, promotion-map-first, or whole-family-history-first

### P5-C1-S1S2 (Reader routing fixed and stable close-out review completed | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P5-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
  - `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`
  - `docs/governance/views/view-old-s0-contract-history-chain-doc-drb-0001-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - readers should be able to choose the right layered old-`S0` view without replaying the whole migration ledger or inferring which question belongs to which surface
  - the lane should close with one explicit six-outlet answer and no hidden requirement for one more export tail
- observed:
  - the three landed layered views now carry one explicit first-open routing split across aggregate coverage, per-series standing, and current-surface history-chain reading
  - the stable close-out review now resolves to justified `no-op` for `contract`, `runbook`, `index/front-door`, and `disposition/placement`, with the defended minimal publish set retained under `view`
  - `S0F-6B` is now ready to close as `stable`

### P4-C2-S1S2 (Second bounded DOC-SLC-0001 history-chain pilot landed inside the stable row contract | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P4-C2-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/governance/views/view-old-s0-contract-history-chain-doc-slc-0001-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the lane should be able to widen by a second current-surface pilot without reopening `P4-C1` field design, `P5` routing design, or a brand-new slice
  - the second pilot should prove that the same current-surface-first chain model also works for the source-log compatibility rule set under `DOC-SLC-0001`
- observed:
  - `S0F-6B` is now explicitly reopened in `C2` rather than in a new slice, and the second pilot is fixed as `DOC-SLC-0001`
  - the second bounded history-chain surface is now landed for `DOC-SLC-0001`, reusing the same promotion-home, promotion-event, consolidation, publication, and prerequisite packet while swapping in `S0F-4B` as the direct source-owner origin
  - later history-chain widening can now continue by additional current-surface pilots without weakening the defended stable close-out already fixed for the lane

### P4-C3-S1S2 (Third bounded DOC-TAX-0001 history-chain pilot landed inside the stable row contract | 2026-04-09)

- headSha: `<pending commit for S0F-6B/P4-C3-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  - `docs/governance/views/view-old-s0-contract-history-chain-doc-tax-0001-v1.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the lane should be able to widen by a third current-surface pilot without reopening `P4-C1` field design, `P5` routing design, or a brand-new slice
  - the third pilot should prove that the same current-surface-first chain model also works for the taxonomy-and-placement rule set under `DOC-TAX-0001`
- observed:
  - `S0F-6B` is now explicitly reopened in `C3` rather than in a new slice, and the third pilot is fixed as `DOC-TAX-0001`
  - the third bounded history-chain surface is now landed for `DOC-TAX-0001`, reusing the same promotion-home, promotion-event, consolidation, publication, and prerequisite packet while swapping in `S0F-3I` as the direct source-owner origin
  - later history-chain widening can now continue by additional current-surface pilots without weakening the defended stable close-out already fixed for the lane

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-6B` as the bounded follow-up for old-`S0` absorption coverage, per-series standing, and contract-history-chain `view` layering.
- 2026-04-09: completed `P1` by fixing the layered `view` split and the minimum reader-facing standing vocabulary for old-`S0` per-log reading.
- 2026-04-09: completed `P2` by fixing the aggregate coverage-overview field set and landing the first bounded old-`S0` absorption coverage overview view.
- 2026-04-09: completed `P3` by fixing the per-series/per-log field set and landing the first bounded `S0B` series drill-down surface.
- 2026-04-09: completed `P4` by fixing the current-surface-to-history-chain field set and landing the first bounded `DOC-DRB-0001` contract-history-chain surface.
- 2026-04-09: completed `P5` by fixing reader routing among the layered views, answering the six-outlet stable close-out review, and marking `S0F-6B` stable.
- 2026-04-09: reopened `S0F-6B` in `C2` so the second bounded current-surface history-chain pilot (`DOC-SLC-0001`) could land inside the same stable row contract instead of opening a near-duplicate follow-up slice.
- 2026-04-09: reopened `S0F-6B` in `C3` so the third bounded current-surface history-chain pilot (`DOC-TAX-0001`) could land inside the same stable row contract instead of opening a near-duplicate follow-up slice.