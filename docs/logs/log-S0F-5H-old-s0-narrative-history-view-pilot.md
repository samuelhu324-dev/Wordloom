# log-S0F-5H (Phase 5H: old-S0 narrative history view pilot)

---

**id**: `S0F-5H`
**kind**: `log`
**title**: `old-S0 narrative history view pilot v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Views, History, Narrative, Reader, epic/s0, sub/5h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
  **reference_log_1**: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  **reference_log_2**: `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
  **reference_log_3**: `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md`
  **reference_log_4**: `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md`
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

- `S0F-5H` opens as the bounded follow-up after `S0F-5G` to pilot one reader-facing narrative-history view layer for old-`S0`.
- This lane exists because the repo now has:
  - one aggregate old-`S0` coverage overview
  - per-series standing views
  - one remaining-line routing/detail/manual-screening stack
  - one supplemental ancestry branch for early `S0A` / `S0B`
  - but it still does not have one reader-facing surface that answers, per log, `why did this appear?`, `what problem did it try to solve?`, and `what result or decision did it leave behind?`
- The first pilot should prove that a stable view can carry old-`S0` narrative change-reading without forcing readers to replay many source logs or ask ad hoc AI summaries each time.

**Default choices (phase defaults / v1)**:

- Treat `narrative history view` as different from `standing view` and different from `current contract`.
- Prefer extracting stable narrative fields from source-log-owned blocks such as `Decision / Outcome`, `Problem Statement`, `Current Status`, and defended consequence notes rather than inventing freeform summaries.
- Do not replace the existing standing/routing views; add one complementary reader layer that explains emergence, boundary, and result.
- Use `S0A + S0B` as the first pilot because the repo now has both counted `S0B` mainline reading and supplemental `S0A / S0B` ancestry reading, which is the hardest useful mixed case.

## Problem Statement

- Current old-`S0` views are already strong at answering `where does this row read now?`, `is it surfaced?`, and `what is its current standing?`
- They are weaker at answering the reader-facing historical questions that arise before outlet or current-home judgment:
  - why was this log opened at all?
  - what concrete boundary or problem was under repair?
  - what decision, result, or stabilized outcome did the work leave behind?
  - what later row, view, contract, or retained-history surface inherited that result?
- Without one explicit narrative-history layer, readers still have to reconstruct change meaning by scanning many logs or by asking an assistant to compress them repeatedly.

## PR Summary Inputs (optional)

- Use this block because `S0F-5H` is expected to define the narrative-history reader contract first, then publish one pilot surface rather than to change standing or contract admission directly.

**PR summary bullets**:

- Open one bounded lane for old-`S0` narrative-history reading.
- Separate `narrative history view` from existing standing and current-home views.
- Pilot the model on mixed `S0A + S0B` ancestry before widening to the other series.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the narrative-history pilot lane.

**PR links**:

- Log: `docs/logs/log-S0F-5H-old-s0-narrative-history-view-pilot.md`
- Previous log: `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`

## Exported Sections / Outlet Ownership

- This slice starts as a reader-surface pilot lane, not as a new contract landing or a standing re-adjudication lane.
- The default expected landing is in `view` only.

**Outlet ownership**:

- `contract`: no-op by default; the lane explains historical change-reading rather than landing new current rules
- `runbook`: no-op by default; this lane is for reader interpretation, not operator procedure
- `view`: expected landing surface for one bounded old-`S0` narrative-history pilot
- `index/front-door`: possible later update only if the pilot materially changes first-open reading order
- `disposition/placement`: no-op by default; the lane does not move files or alter placement on scaffold
- `log-retained core`: keep this source log for boundary, field model, pilot sequence, and evidence ledger

## Definitions (optional)

- **narrative history view**: one reader-facing surface that explains why a log existed, what problem it addressed, what result it left behind, and where that result later reads now
- **standing view**: one reader-facing surface that classifies current standing, current home, and surfaced-versus-non-surfaced state
- **narrative field model**: one bounded field set that lets readers understand change meaning without replaying full source logs

## Constraints

- Do not reopen old-`S0` standing results merely to make the narrative view look cleaner.
- Do not collapse `why it existed` and `where it reads now` into one field.
- Do not ask the narrative view to become a second current-contract index.
- Do not fabricate historical motives or results that are not defensible from source-owned text.
- Do not require the pilot to cover all old-`S0` series before it proves the field model on one bounded mixed case.

## Scope

- `P0`: open `S0F-5H`, wire it into the parent spine, and fix the narrative-history-view boundary
- `P1`: define the minimum narrative field model for reader-facing old-`S0` change-reading
- `P2`: select and defend the first pilot population, expected as `S0A + S0B`
- `P3`: publish one bounded narrative-history pilot view for that population
- `P4`: decide whether the pilot is strong enough to widen to `S0C` / `S0D` / `S0E` / `S0F`, or whether the field model still needs revision first

## Success Criteria (DoD)

- One reader can understand why the pilot logs existed, what they changed, and what they left behind without replaying the full source logs.
- The pilot stays clearly separate from standing classification and current-contract concentration.
- The repo gains one reusable narrative field model that can later be widened to the rest of old-`S0` if the pilot proves useful.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the narrative-history reader contract is explicit enough to reuse
  - one bounded pilot surface exists and is readable without source-log replay
  - the next widening or stop boundary is explicit enough that later work does not need to reopen the same scaffold decision first

## P0 (Contract | v1)

### P0-C1-S1 (Narrative-history-view boundary fixed | v1)

- `S0F-5H` is now opened as the old-`S0` narrative-history-view pilot lane.
- This slice does not decide standing, contract admission, or cleanup consequence.
- It fixes only that the next job is to create one reader-facing historical change-reading layer above the existing standing/routing stack.

### P0-C1-S2 (Immediate pilot sequence fixed | v1)

- The immediate next work after scaffold is now fixed as:
  - first define one stable narrative field model
  - then choose one bounded pilot population
  - then land one narrative-history pilot view on top of that model
- Under the current boundary, `S0A + S0B` is the preferred first pilot because it combines counted and supplemental ancestry reading in one small package.

## Plan (draft)

### P1 (Narrative field model)

- `P1-C1-S1`: define the minimum reader-facing narrative fields for why / problem / result / inheritance
- `P1-C1-S2`: define which source-owned blocks are allowed to feed those fields

### P1-C1-S1 (Minimum narrative field model fixed | v1)

- The minimum reader-facing field model for the pilot is now fixed as eight bounded fields:
  - `source log`: the exact historical source under review
  - `why it appeared`: the trigger, pressure, or emergence reason that justified opening the log
  - `scoped problem`: the concrete boundary or problem the log tried to repair, separate from the trigger
  - `decision / result`: the stabilized outcome, decision, or result the log left behind
  - `what changed after it`: the later surface, inheritance path, or downstream consequence that absorbed or replaced the result
  - `current historical role`: the present reader-facing role of the log in history reading, such as direct history, lineage support, structural prerequisite, retained evidence, or unresolved ancestry
  - `current first-open home`: the current first-open surface for readers after the historical row is understood
  - `reader note`: one compact note for ambiguity, exclusion, or bounded caution when needed
- This field model intentionally separates historical narrative from standing classification:
  - `why it appeared`, `scoped problem`, and `decision / result` explain why the log mattered at the time
  - `current historical role` and `current first-open home` explain how readers should interpret it now
- The pilot should not require every field to be equally long; short defended phrases are preferred over verbose restatement.

### P1-C1-S2 (Allowed source-owned feed blocks fixed | v1)

- The pilot may now derive the narrative field model only from bounded source-owned blocks or defended current reader surfaces.
- Allowed primary source blocks are now fixed as:
  - source-log or ADR `Decision / Outcome` and explicit decision text
  - source-log or ADR `Background` / `Context`
  - source-log `Problem Statement`
  - source-log `Current Status` only when it records defended outcome or later inheritance rather than transient execution chatter
  - stable retained decision bullets such as `stable`, `adopted`, `archived`, or defended implementation/consequence notes that clearly belong to the source body
- Allowed secondary bridge surfaces are now fixed as:
  - existing standing views, but only for `current historical role` and `current first-open home`
  - existing supplemental ancestry views, but only for counted-scope status and defended ancestry gap wording
- Disallowed feed sources are now fixed as:
  - ad hoc AI-only compression that cannot be traced back to one bounded source-owned block
  - support-only mutable ledgers as the sole source of why/problem/result wording
  - speculative synthesis that upgrades one unresolved placeholder into a stronger historical result than the current source text can defend
- Under this rule, `P3` should publish a narrative pilot surface that is compact, traceable, and repeatable rather than one prose-heavy retrospective essay.

### P2 (Pilot population selection)

- `P2-C1-S1`: fix the first pilot population and why it is a valid narrative-history test
- `P2-C1-S2`: fix what remains intentionally outside the pilot

### P2-C1-S1 (First pilot population fixed | v1)

- The first narrative-history pilot population is now fixed as one five-item mixed `S0A + S0B` set:
  - `S0A` legacy carry-forward anchor
  - `S0B` parent ADR anchor
  - `S0B-2A`
  - `S0B-3A`
  - `S0B-1A` unresolved issue-only placeholder
- This is now the defended first pilot because it combines all three reading states the narrative model needs to prove:
  - supplemental direct history outside counted scope
  - supplemental lineage-support ancestry outside counted scope
  - counted-series rows already inside the main old-`S0` review scope
  - one explicit unresolved placeholder that prevents the pilot from pretending historical completeness where evidence still does not exist
- This makes the pilot small enough to read in one pass while still hard enough to prove that counted mainline and supplemental ancestry can coexist in one narrative surface without collapsing into standing-only tables.

### P2-C1-S2 (Intentional non-pilot boundary fixed | v1)

- Everything outside the five-item `S0A + S0B` set remains intentionally outside the first pilot.
- The non-pilot boundary is now fixed as:
  - all `S0C`, `S0D`, `S0E`, and `S0F` rows
  - any future issue-only `S0B-1A` evidence packet that is not yet materialized locally
  - any attempt to widen the pilot into counted-scope changes or current-contract admission consequences
- Under this rule, `P3` should prove the narrative field model on one bounded mixed set first.
- If the pilot succeeds, later widening can reuse the same field model on larger series without reopening the scaffold boundary.

### P3 (Pilot narrative-history surface)

- `P3-C1-S1`: publish one narrative-history pilot view for the bounded pilot population
- `P3-C1-S2`: wire that pilot into the existing old-`S0` reader-routing set without confusing it with standing views

### P4 (Post-pilot decision)

- `P4-C1-S1`: determine whether the pilot should widen to the other series
- `P4-C1-S2`: determine whether the field model needs revision before widening

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: narrative-history-view boundary fixed
- [x] `P0-C1-S2`: immediate pilot sequence fixed

### P1 (Narrative field model)

- [x] `P1-C1-S1`: minimum reader-facing narrative fields fixed
- [x] `P1-C1-S2`: allowed source-owned feed blocks fixed

### P2 (Pilot population selection)

- [x] `P2-C1-S1`: first pilot population fixed
- [x] `P2-C1-S2`: non-pilot boundary fixed

### P3 (Pilot narrative-history surface)

- [ ] `P3-C1-S1`: pilot narrative-history view published
- [ ] `P3-C1-S2`: pilot routing wired into the old-`S0` reader set

### P4 (Post-pilot decision)

- [ ] `P4-C1-S1`: widening decision fixed
- [ ] `P4-C1-S2`: field-model revision decision fixed

## Current Status

- `S0F-5H` is now opened as the bounded follow-up lane for old-`S0` narrative-history reading after `S0F-5G` widened standing/routing/manual-screening surfaces.
- `P0` is now complete: the lane boundary is fixed and the immediate next step is to define the narrative field model rather than to improvise summary prose ad hoc.
- `P1` is now complete: the minimum narrative field model and its allowed source-owned feed blocks are now fixed, so the pilot can extract `why / problem / result / inheritance` without drifting into ad hoc AI compression.
- The preferred first pilot is now `S0A + S0B`, because that mixed set is small and already spans both counted mainline reading and supplemental ancestry reading.
- `P2` is now complete: the first pilot population is fixed as the five-item mixed `S0A + S0B` set, and everything outside that bounded packet now stays intentionally outside the pilot.
- The immediate next step is now `P3`: publish the first narrative-history pilot view and wire it into the old-`S0` reader set.

## Evidence (reserved)

### P0-C1-S1S2 (Narrative-history pilot lane opened | 2026-04-10)

- headSha: `<pending local changes for S0F-5H/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5H-old-s0-narrative-history-view-pilot.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should have one explicit next lane for narrative-history reading that sits beside, not inside, the standing-view stack
  - the first pilot should be bounded enough that the reader contract can be proved before widening to all old-`S0` series
- observed:
  - `S0F-5H` now fixes the reader-facing narrative-history-view boundary, pilot sequence, and preferred `S0A + S0B` first-population direction
  - the parent spine now carries the new lane as the next old-`S0` reader-surface follow-up after `S0F-5G`

### P1-C1-S1S2 (Narrative field model and source-feed rules fixed | 2026-04-10)

- headSha: `<pending local changes for S0F-5H/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5H-old-s0-narrative-history-view-pilot.md`
- expected:
  - the pilot should have one stable narrative field model that can explain historical emergence and result without collapsing back into current standing tables
  - the pilot should have explicit source-feed rules so later narrative rows remain traceable to defended source-owned blocks
- observed:
  - the minimum reader-facing field model is now fixed across `source log`, `why it appeared`, `scoped problem`, `decision / result`, `what changed after it`, `current historical role`, `current first-open home`, and `reader note`
  - the pilot now also has explicit allowed primary and secondary source feeds, plus disallowed AI-only and speculative synthesis paths

### P2-C1-S1S2 (Pilot population and non-pilot boundary fixed | 2026-04-10)

- headSha: `<pending local changes for S0F-5H/P2-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-5H-old-s0-narrative-history-view-pilot.md`
- expected:
  - the pilot should have one exact bounded population that is small enough to read but rich enough to prove counted mainline plus supplemental ancestry coexistence
  - the pilot should also have an explicit non-pilot boundary so `P3` does not widen opportunistically while building the first view
- observed:
  - the first pilot population is now fixed as `S0A`, `S0B` parent ADR, `S0B-2A`, `S0B-3A`, and the unresolved `S0B-1A` placeholder
  - all other old-`S0` series and any not-yet-materialized `S0B-1A` issue packet now remain intentionally outside the pilot until the first view proves the field model

## Recent changes (for traceability, optional)

- 2026-04-10: opened `S0F-5H` as the bounded old-`S0` narrative-history-view pilot lane after `S0F-5G` landed standing, routing, screening, and supplemental ancestry reader surfaces.
- 2026-04-10: completed `P1` by fixing the minimum narrative field model and explicit source-feed rules for the first old-`S0` narrative-history pilot.
- 2026-04-10: completed `P2` by fixing the first five-item `S0A + S0B` pilot population and explicit non-pilot boundary for the first narrative-history view.