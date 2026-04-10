# log-S0F-5G (Phase 5G: remaining old-S0 history-line expansion and manual screening)

---

**id**: `S0F-5G`
**kind**: `log`
**title**: `remaining old-S0 history-line expansion and manual screening v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Views, History, Migration, Review, epic/s0, sub/5g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-5F-remaining-s0e-standing-adjudication-and-packeted-review.md`
  **reference_log_1**: `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
  **reference_log_2**: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  **reference_log_3**: `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
  **reference_log_4**: `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`
  **reference_log_5**: `docs/governance/views/view-doc-history-and-lineage-v1.md`
**issue_keyword**: `migration`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/5`
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
**created**: `2026-04-10`
**updated**: `2026-04-10`

---

## Decision / Outcome

**Decision**:

- `S0F-5G` opens as the bounded follow-up after `S0F-5F` to expand the remaining old-`S0` history/view line before any further manual contract screening or six-outlet adjustment is attempted.
- This lane exists because the repo now has:
  - one stable current `DOC` front door
  - one bounded `DOC` history view
  - one bounded promotion map
  - one aggregate old-`S0` coverage view
  - bounded series standing pilots for `S0B`, `S0E`, and `S0F`
  - but it still does not have one sufficiently expanded history/view layer across the remaining old-`S0` population for human contract screening without replaying source logs row by row.
- The lane is intentionally history/view-first rather than contract-first:
  - do not auto-admit new `DOC` contracts just because a row looks structurally important
  - first widen the reader-facing history/view layer so one human reviewer can inspect the full remaining old-`S0` line more safely
  - then use that widened surface to decide which rows should stay as retained history, which should become explicit current reader surfaces, and which six-outlet assignments need manual adjustment

**Default choices (phase defaults / v1)**:

- Treat remaining old-`S0` history expansion and later contract admission as two different jobs.
- Do not use `S0F-5G` to auto-promote source-log or template contracts into `DOC` current contracts without an explicit later human screening result.
- Prefer widening one explicit view layer over hiding judgments inside the support-only working ledger.
- Preserve the already-landed standing vocabulary from `S0F-6B` and the already-executed standing results from `S0F-5C`, `S0F-5E`, and `S0F-5F`; this lane widens routing and manual screening surfaces rather than reopening those settled row outcomes by default.

## Problem Statement

- After `S0F-5F`, `S0E` no longer carries generic unresolved remainder, and the earlier small-series work has already removed the generic unresolved remainder from `S0B`, `S0C`, and `S0D`.
- The repo can now explain per-series standing for several bounded pilots, but it still cannot show one expanded history/view line for the full remaining old-`S0` population in a way that supports low-risk manual contract screening.
- Without one widened history/view layer, later contract admission review risks:
  - filtering candidate contracts too early from partial source-log archaeology
  - undercounting source-log and template contracts that are still real governance surfaces but not yet published as family-owned `DOC` bodies
  - conflating `current contract`, `retained history`, `lineage`, `manual review candidate`, and `non-DOC` rows inside one support-only working ledger that is not meant to be a reader-facing review surface

## PR Summary Inputs (optional)

- Use this block because `S0F-5G` is expected to publish a widened history/view line first and to hand back one clearer manual screening surface rather than to auto-land one new contract by default.

**PR summary bullets**:

- Open the bounded lane for remaining old-`S0` history-line expansion.
- Fix one explicit rule that history/view widening happens before manual contract screening.
- Keep later six-outlet adjustment and contract admission human-guided instead of auto-filtered from partial row review.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the history-line expansion lane.

**PR links**:

- Log: `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
- Previous log: `docs/logs/log-S0F-5F-remaining-s0e-standing-adjudication-and-packeted-review.md`

## Exported Sections / Outlet Ownership

- This slice starts as a reader-surface widening lane, not as a new `DOC` contract landing lane.
- The default expected landing is in `view` and possibly in the existing standing surfaces, not in new current-rule records.

**Outlet ownership**:

- `contract`: no-op by default; any new contract landing should happen only after explicit manual screening on top of the widened history/view layer
- `runbook`: no-op by default; this lane explains reading and review routing, not stable operator procedure
- `view`: expected landing surface for remaining old-`S0` history-line expansion, widened reader routing, and manual screening support
- `index/front-door`: possible later update only if the widened history/view layer changes first-open routing materially enough to justify it
- `disposition/placement`: possible later write-back only when a row's widened history line proves a placement consequence directly
- `log-retained core`: keep this source log for boundary, phase order, evidence ledger, and the explicit human-screening handoff rule

## Definitions (optional)

- **remaining old-`S0` history-line expansion**: widening reader-facing history/view coverage for old-`S0` rows that are still not concentrated into one clear current history line, even when their standing has already been adjudicated elsewhere
- **manual screening surface**: one widened `view` layer that lets a human reviewer decide whether a row should stay history-only, become one current contract candidate, or require a six-outlet reassignment
- **history/view-first lane**: one lane that improves reader routing and historical concentration before any later contract landing or outlet adjustment is attempted

## Constraints

- Do not reopen already-defended standing results just to force them into current contracts.
- Do not treat the support-only working ledger as the final human review surface.
- Do not assume every structurally important source-log or template rule should become one family-owned `DOC` current contract.
- Do not widen this lane into support-only relocation execution or whole-repo cleanup movement.

## Scope

- `P0`: open `S0F-5G`, wire it into the parent spine, and fix the history/view-first manual-screening boundary
- `P1`: fix the exact remaining old-`S0` population that still needs widened history/view routing after the existing coverage, standing, and history-chain pilots
- `P2`: land one widened history/view routing surface for the remaining old-`S0` population so readers can see the still-unconcentrated line without replaying the working ledger alone
- `P3`: expand the series and/or chain surfaces needed so the remaining `S0F` backlog and the already-adjudicated non-surfaced rows become human-reviewable as one explicit history line
- `P4`: publish one manual screening view or equivalent reader-facing packet that separates `candidate current contract`, `retain as history`, `lineage only`, `non-DOC`, and `needs six-outlet adjustment`
- `P5`: determine whether any bounded first write-back subset should follow immediately, or whether the lane should stop at human-screening publication and wait for manual review feedback
- `P6`: fix the next owner after manual screening, including whether later follow-up should be contract-admission-first, six-outlet-adjustment-first, or no-op on most rows

## Success Criteria (DoD)

- One reader can inspect the remaining old-`S0` history line without relying on the support-only working ledger as the only global review surface.
- The repo has one explicit manual screening surface for later human review of contract candidacy and six-outlet adjustments.
- The lane leaves later contract-admission decisions more visible and less auto-filtered than the current partial history/view layer allows.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the remaining old-`S0` history/view expansion boundary is explicit enough to reuse
  - the widened history/view layer exists and is sufficient for manual review of the remaining line
  - the next post-screening owner is explicit enough that later contract admission or outlet-adjustment work does not need to reopen the same history-line boundary first

## P0 (Contract | v1)

### P0-C1-S1 (History/view-first screening boundary fixed | v1)

- `S0F-5G` is now opened as the remaining old-`S0` history-line expansion and manual-screening lane.
- This slice does not decide that one new `DOC` contract packet already exists.
- It first fixes that the next job is to widen reader-facing history/view coverage before one human reviewer filters contract candidates or outlet changes manually.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now fixed as:
  - first inventory the remaining old-`S0` line that still lacks widened history/view routing
  - then publish one widened history/view surface for that line
  - then publish one manual screening packet on top of that widened surface
- This keeps reader routing and human review ahead of any later contract landing pressure.

## Plan (draft)

### P1 (Remaining old-`S0` history-line inventory)

- `P1-C1-S1`: fix the exact remaining old-`S0` row population that still lacks widened history/view routing after the current pilots
- `P1-C1-S2`: fix the minimum routing classes that the later manual screening surface must expose

### P1-C1-S1 (Remaining old-`S0` history-line population fixed | v1)

- The remaining old-`S0` line that still lacks widened history/view routing is now fixed as the full non-surfaced remainder after the current `DOC` surfaced set, not just as the still-`unreviewed` subset.
- The exact current remaining history-line population is now `63` rows, matching the current non-surfaced remainder in `view-old-s0-absorption-coverage-overview-v1.md`.
- That `63`-row remainder is now split into two review classes:
  - `45` already-adjudicated but still non-surfaced rows whose standing is already known, but whose wider history/view routing is still not concentrated enough for low-risk manual contract screening
  - `18` still-unresolved `S0F` rows whose standing and wider history/view routing are both still missing
- The `45` already-adjudicated but still non-surfaced rows are now fixed as:
  - `S0B`: `S0B-2A`
  - `S0C`: `S0C-2A`, `S0C-3A`, `S0C-3A-1A`, `S0C-3A-2A`, `S0C-3A-3A`, `S0C-4A`, `S0C-4A-1A`, `S0C-5A`
  - `S0D`: `S0D-2A`, `S0D-3A`, `S0D-4A`, `S0D-5A`, `S0D-6A`
  - `S0E`: `S0E-1A`, `S0E-1B`, `S0E-2A`, `S0E-2B`, `S0E-2C`, `S0E-3B`, `S0E-4A`, `S0E-4B`, `S0E-4C`, `S0E-4D`, `S0E-4E`, `S0E-4F`, `S0E-5A`, `S0E-5B`, `S0E-5C`, `S0E-5D`, `S0E-5E`, `S0E-6B`, `S0E-6D`, `S0E-6E`, `S0E-6F`, `S0E-7A`, `S0E-7B`, `S0E-7C`, `S0E-7D`, `S0E-7E`, `S0E-7F`, `S0E-7G`
  - `S0F`: `S0F-1H`, `S0F-1I`, `S0F-1J`
- The `18` still-unresolved `S0F` rows are now fixed as:
  - `S0F-1C`, `S0F-1K`
  - `S0F-2A`, `S0F-2B`
  - `S0F-3A`, `S0F-3B`, `S0F-3C`, `S0F-3D`, `S0F-3E`, `S0F-3F`, `S0F-3G`, `S0F-3H`, `S0F-3J`, `S0F-3K`, `S0F-3L`, `S0F-3M`
  - `S0F-4H`, `S0F-5A`
- Under this `P1` boundary, later widened history/view routing should cover the whole remaining `63`-row line, but `P3` should enter the still-unresolved `18`-row `S0F` subset separately from the already-adjudicated `45`-row retained-history population.

### P1-C1-S2 (Screening routing classes fixed | v1)

- The minimum routing classes for the later manual screening surface are now fixed as six distinct reader-facing buckets:
  - `standing-first unresolved`: the row still lacks defended standing and must not be screened for contract admission yet
  - `candidate current-contract`: the row looks structurally current enough that later human review may consider one current contract concentration write
  - `candidate current-view`: the row looks more like one possible current reader-surface concentration point than like one rule-body landing
  - `retain as history`: the row should stay directly readable as retained historical evidence even after screening
  - `lineage only`: the row is historically relevant, but current reading should open some later or stronger surface first rather than the row itself
  - `non-DOC / external current-home`: the row's strongest current meaning already lives outside the current `DOC` surface or outside one reader-facing write target for this lane
- These routing classes intentionally sit above the earlier standing vocabulary rather than replacing it:
  - `retained-evidence`, `history-lineage`, `retired-lineage`, and `non-doc` remain valid standing answers
  - the new routing classes decide how the later manual screening surface should present those standing answers for human contract and outlet review
- The routing classes also intentionally preserve one explicit `needs six-outlet adjustment` consequence, but not as a first-pass population bucket:
  - first the manual screening surface should show the six routing classes above
  - then human review may mark a row inside one of those classes as a later `needs six-outlet adjustment` follow-up if its current outlet still looks wrong after the widened history line is visible
- Under this rule, `P4` should publish one human-reviewable surface that separates unresolved rows from contract/view candidates and from rows that should remain retained, lineage-only, or outside `DOC`.

### P2 (Widened history/view routing surface)

- `P2-C1-S1`: land one widened history/view routing surface for the remaining old-`S0` line
- `P2-C1-S2`: wire that surface into the existing old-`S0` reader routing set without collapsing it back into the working ledger

### P2-C1-S1 (Widened history/view routing surface landed | v1)

- The first widened remainder-routing surface now exists at `docs/governance/views/view-old-s0-remaining-history-line-routing-v1.md`.
- This first widened surface intentionally answers one reader-facing question only:
  - `what is the full remaining old-S0 line after the current surfaced DOC set, and how should I route into it?`
- The landed surface now makes three points explicit without dropping readers into the support-only working ledger first:
  - the remaining line is the full `63`-row non-surfaced remainder
  - that remainder splits into `45` already-adjudicated rows plus `18` still-unresolved `S0F` rows
  - current first-open routing differs by series because `S0B`/`S0C`/`S0D`/`S0E` now have only adjudicated remainder while `S0F` still mixes adjudicated and unresolved remainder

### P2-C1-S2 (Widened routing wired into the old-`S0` reader set | v1)

- The old-`S0` reader-routing set now explicitly includes the new remainder-routing surface.
- `view-old-s0-absorption-coverage-overview-v1.md` now points readers to `view-old-s0-remaining-history-line-routing-v1.md` when the question is the non-surfaced remainder itself rather than the surfaced set or the aggregate counts.
- This keeps the new routing answer reader-facing while leaving the support-only working ledger in its intended working-only role.

### P3 (Remaining old-`S0` history-line expansion)

- `P3-C1-S1`: expand the remaining `S0F` series and adjacent retained-history line into explicit reader-facing history routing
- `P3-C1-S2`: widen the already-adjudicated retained-history population enough that manual review no longer depends on row-by-row archaeology

### P4 (Manual screening packet)

- `P4-C1-S1`: publish one manual screening view or equivalent packet for candidate current-contract, retained-history, lineage-only, non-DOC, and outlet-adjustment rows
- `P4-C1-S2`: fix the first human-review sequence for filtering that packet without auto-admitting a contract set

### P5 (Post-screening consequence)

- `P5-C1-S1`: determine whether any bounded first write-back subset is immediately safe after the screening surface lands
- `P5-C1-S2`: determine whether the lane should stop at human-screening publication and wait for manual review feedback instead of auto-executing

### P6 (Next-owner decision)

- `P6-C1-S1`: fix whether the next bounded follow-up is contract-admission-first, six-outlet-adjustment-first, or no-op on most rows
- `P6-C1-S2`: fix the next owner and stop boundary without reopening the same widened history-line inventory

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: history/view-first screening boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Remaining old-`S0` history-line inventory)

- [x] `P1-C1-S1`: remaining old-`S0` history-line population fixed
- [x] `P1-C1-S2`: screening routing classes fixed

### P2 (Widened history/view routing surface)

- [x] `P2-C1-S1`: widened history/view routing surface landed
- [x] `P2-C1-S2`: widened routing wired into the old-`S0` reader set

### P3 (Remaining old-`S0` history-line expansion)

- [ ] `P3-C1-S1`: remaining `S0F` history line expanded
- [ ] `P3-C1-S2`: adjudicated retained-history line widened for manual review

### P4 (Manual screening packet)

- [ ] `P4-C1-S1`: manual screening packet published
- [ ] `P4-C1-S2`: human-review sequence fixed

### P5 (Post-screening consequence)

- [ ] `P5-C1-S1`: first write-back consequence determined
- [ ] `P5-C1-S2`: stop-at-screening versus auto-execute consequence determined

### P6 (Next-owner decision)

- [ ] `P6-C1-S1`: next bounded follow-up type fixed
- [ ] `P6-C1-S2`: next owner and stop boundary fixed

## Current Status

- `S0F-5G` is now opened as the bounded remaining old-`S0` history-line expansion lane after `S0F-5F` removed the last generic unresolved remainder from `S0E`.
- `P0` is now complete: the lane is fixed as history/view-first and manual-screening-first rather than as another auto-admission lane.
- `P1` is now complete: the remaining non-surfaced old-`S0` history line is now fixed as one explicit `63`-row remainder split into `45` already-adjudicated rows plus `18` still-unresolved `S0F` rows, and the later manual screening surface now has one defended six-class routing model.
- `P2` is now complete: the repo now has one reader-facing remainder-routing surface for the full `63`-row non-surfaced old-`S0` line, and aggregate coverage routing now points readers there before they fall back to the support-only working ledger.
- The immediate next step is now `P3`: widen that routing answer into one readable detail/history line for the remaining `63` rows, with separate entry for the unresolved `18`-row `S0F` subset.

## Evidence (reserved)

### P0-C1-S1S2 (Remaining old-`S0` history-line expansion lane opened | 2026-04-10)

- headSha: `<pending commit for S0F-5G/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should have one explicit next lane for widening the old-`S0` history/view layer before later human contract screening
  - the lane should not assume one automatic contract-admission packet from scaffold alone
- observed:
  - `S0F-5G` now fixes the boundary, sequencing, and manual-screening-first rule for remaining old-`S0` history/view expansion
  - the parent spine now routes the next follow-up through this lane rather than through ad hoc remaining-row review

### P1-C1-S1S2 (Remaining old-`S0` history-line inventory and screening classes fixed | 2026-04-10)

- headSha: `<pending commit for S0F-5G/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the remaining old-`S0` line should stop reading as one vague `outside surfaced set` bucket and instead become one explicit remainder population for widened history/view routing
  - the later manual screening surface should have one explicit routing-class model before any human contract filtering begins
- observed:
  - the remaining old-`S0` line is now fixed as the full `63`-row non-surfaced remainder, split into `45` already-adjudicated rows plus `18` still-unresolved `S0F` rows
  - the later manual screening surface now has one defended six-class routing model that keeps unresolved rows separate from candidate current-contract/current-view, retained-history, lineage-only, and non-DOC rows

### P2-C1-S1S2 (Remaining old-`S0` routing surface landed and wired | 2026-04-10)

- headSha: `<pending commit for S0F-5G/P2-C1-S1S2>`
- artifacts:
  - `docs/governance/views/view-old-s0-remaining-history-line-routing-v1.md`
  - `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
  - `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - readers should gain one first-open remainder-routing answer for the full non-surfaced old-`S0` line
  - the aggregate coverage layer should now route non-surfaced questions to that new view rather than leaving readers to infer the remainder from counts alone
- observed:
  - `view-old-s0-remaining-history-line-routing-v1.md` now exposes the full `63`-row remainder split and the current first-open routing by series
  - `view-old-s0-absorption-coverage-overview-v1.md` now routes the non-surfaced-remainder question into that new reader-facing surface

## Recent changes (for traceability, optional)

- 2026-04-10: opened `S0F-5G` as the bounded remaining old-`S0` history-line expansion and manual-screening lane after `S0F-5F` completed the remaining `S0E` standing adjudication.
- 2026-04-10: completed `P1` by fixing the full remaining old-`S0` non-surfaced population and the minimum routing classes for later manual screening.
- 2026-04-10: completed `P2` by landing the first remainder-routing view for the full non-surfaced old-`S0` line and wiring aggregate coverage routing to that new surface.