# log-S0F-6B (Phase 6B: old-S0 absorption coverage and history-chain views)

---

**id**: `S0F-6B`
**kind**: `log`
**title**: `old-S0 absorption coverage and history-chain views v1`
**status**: `draft`
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
- `view`: landed first as `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`; later bounded follow-up views may add series drill-down and contract-history-chain reading
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

### P4 (Contract-history chain)

- `P4-C1-S1`: define the current-surface-to-history-chain field set
- `P4-C1-S2`: land the first bounded contract-history-chain reading surface

### P5 (Reader routing and close-out)

- `P5-C1-S1`: fix reader routing among coverage, drill-down, and history-chain views
- `P5-C1-S2`: complete stable close-out review for the layered `view` lane

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

- [ ] `P3-C1-S1`: per-series drill-down field set fixed
- [ ] `P3-C1-S2`: first bounded series drill-down surface landed

### P4 (Contract-history chain)

- [ ] `P4-C1-S1`: contract-history-chain field set fixed
- [ ] `P4-C1-S2`: first bounded contract-history-chain surface landed

### P5 (Reader routing and close-out)

- [ ] `P5-C1-S1`: reader routing fixed among layered views
- [ ] `P5-C1-S2`: stable close-out review completed

## Current Status (recommended)

- `S0F-6B` is now opened as the bounded follow-up for old-`S0` absorption coverage and history-chain `view` layering.
- `P0` is now complete: the problem is fixed as one reader-facing `view` layering gap above the current surfaced migration set, not as immediate contract mutation or ad hoc row widening.
- `P1` is now complete: the layered `view` split and the minimum reader-facing standing vocabulary are now explicit enough to reuse.
- `P2` is now complete: the minimum field set for one bounded aggregate coverage-overview surface is fixed, and the first aggregate old-`S0` absorption coverage view is now landed.
- The next step is `P3`: define the per-series and per-log standing field set before landing the first bounded series drill-down surface.

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

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-6B` as the bounded follow-up for old-`S0` absorption coverage, per-series standing, and contract-history-chain `view` layering.
- 2026-04-09: completed `P1` by fixing the layered `view` split and the minimum reader-facing standing vocabulary for old-`S0` per-log reading.
- 2026-04-09: completed `P2` by fixing the aggregate coverage-overview field set and landing the first bounded old-`S0` absorption coverage overview view.