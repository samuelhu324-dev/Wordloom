# log-S0F-4F (Phase 4F: DOC reader-surface consolidation after first promotion quartet)

---

**id**: `S0F-4F`
**kind**: `log`
**title**: `DOC reader-surface consolidation after first promotion quartet v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Consolidation, epic/s0, sub/4f`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
  **reference_log_1**: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
  **reference_log_2**: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
  **reference_log_3**: `docs/governance/contract/INDEX.md`
  **reference_log_4**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_5**: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
  **reference_log_6**: `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`
  **reference_log_7**: `docs/governance/contract/DOC-DRB-0001-document-role-boundaries-writeback-and-disposition.md`
  **reference_log_8**: `docs/governance/contract/DOC-SLC-0001-source-log-compatibility-and-weak-structure-export-discipline.md`
  **reference_log_9**: `docs/governance/contract/DOC-TAX-0001-governance-contract-taxonomy-and-placement-model.md`
  **reference_log_10**: `docs/governance/contract/DOC-FDT-0001-family-front-door-transition-and-gc-demotion-model.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/4`
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
**created**: `2026-04-08`
**updated**: `2026-04-08`

---

## Decision / Outcome

**Decision**:

- `S0F-4F` opens the next bounded follow-up because `S0F-4E` has already completed the first mapped `DOC` promotion quartet, but the three main `DOC` reader surfaces still carry transitional wording that was correct during staged landing and is now slightly looser than the repo's new steady state.
- v1 fixes one consolidation principle:
  - `docs/governance/contract/INDEX.md` should now read as the active landed contract surface for the first `DOC` quartet
  - `docs/governance/views/view-doc-current-front-door-v1.md` should now read as the stable family-first reader entry after quartet activation rather than as a mixed-state landing note
  - `docs/governance/views/view-doc-contract-promotion-map-v1.md` should now clearly distinguish between `promotion map as naming/admission map` and `this first mapping set is already fully executed`
- Under this model, `S0F-4F` is not one more promotion lane and not old-`GC-*` cleanup yet; it is the bounded consolidation lane that turns post-promotion reader surfaces from transition-safe wording into steady-state wording.

**Default choices (phase defaults / v1)**:

- Do not reopen any `DOC-...` contract body semantics in this slice unless a reader-surface contradiction forces it.
- Prefer wording convergence and reader-role clarification over structural churn or new file creation.
- Keep `contract/INDEX.md`, the `DOC` front door, and the promotion map separate:
  - `INDEX.md` owns landed contract inventory and directory-level reading
  - the `DOC` front door owns family-first current reading
  - the promotion map owns deterministic source-owner-to-contract mapping and promotion history framing
- Do not start old `GC-*` cleanup inside this slice; this lane only prepares the reader surfaces so later cleanup can rely on a steadier `DOC` contract story.
- Reuse `S0F-5A` discipline implicitly for no-proliferation: if consolidation does not justify a new `view` or `runbook`, do not invent one.

## PR Summary Inputs (optional)

- Use this block because `S0F-4F` exists to converge the public reader story after the first `DOC` promotion quartet reached stable active state.

**PR summary bullets**:

- Consolidate the three main `DOC` reader surfaces after the first mapped promotion quartet became fully active.
- Remove residual mixed-transition wording where the repo now has a stronger steady-state answer.
- Keep promotion-map, directory-index, and family-front-door roles explicit instead of letting them drift into partial duplication.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the first `DOC` post-quartet consolidation PR.

**PR links**:

- Log: `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
- Previous log: `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
- Contract index: `docs/governance/contract/INDEX.md`
- DOC front door: `docs/governance/views/view-doc-current-front-door-v1.md`
- Promotion map: `docs/governance/views/view-doc-contract-promotion-map-v1.md`

## Exported Sections / Outlet Ownership (optional)

- This slice should primarily end in converged reader surfaces rather than in new contract extraction.

**Outlet ownership**:

- `contract`: none by default beyond directory-level index wording convergence
- `view`: the `DOC` family front door and the promotion map if reader wording needs consolidation
- `index/front-door`: `docs/governance/contract/INDEX.md` plus any minimal `DOC` landing-surface write-back needed to express the fully active quartet state
- `disposition/placement`: none by default; old-`GC-*` cleanup remains later work
- `log-retained core`: consolidation boundary, wording-drift inventory, execution checklist, and evidence for the post-quartet reader-surface package

## Definitions (optional)

- **reader-surface consolidation**: bounded convergence work that makes already-correct files read as one consistent steady-state story after a transition phase completes
- **mixed-transition wording**: text that was accurate while some promoted files were still draft or still absent, but becomes loose or redundant once the whole mapped set is active
- **steady-state quartet**: the first mapped `DOC` promotion set after `DOC-DRB-0001`, `DOC-SLC-0001`, `DOC-TAX-0001`, and `DOC-FDT-0001` are all active

## Constraints

- Do not reopen the `DOC` area-code dictionary, filename model, or source-owner promotion map semantics already fixed in `S0F-4D` and executed in `S0F-4E`.
- Do not treat the promotion map as obsolete merely because the first mapping set is now complete; it still owns deterministic mapping vocabulary.
- Do not collapse the contract index and the `DOC` front door into one file.
- Do not expand this slice into old-`GC-*` cleanup or non-`DOC` family strategy work.

## Scope

- `P0`: open `S0F-4F`, fix the post-quartet consolidation boundary, and wire the new slice into the parent spine
- `P1`: inventory residual mixed-transition wording and role overlap across `INDEX.md`, `view-doc-current-front-door-v1.md`, and `view-doc-contract-promotion-map-v1.md`
- `P2`: converge those reader surfaces onto one steady-state quartet-active story without collapsing their distinct roles
- `P3`: fix the post-consolidation reader notes, next-step boundary, and retained-source-owner framing so later old-`GC-*` cleanup can proceed from a stable `DOC` reader surface

## Success Criteria (DoD)

- One reader can explain the difference among the `DOC` contract index, the `DOC` family front door, and the `DOC` promotion map without reading them as competing summaries.
- One reader can tell that the first mapped `DOC` promotion quartet is fully active without having to infer that from multiple separate files.
- One reader can tell that the promotion map is still meaningful even though the first mapping set has already been executed.
- The repo has one bounded follow-up lane for reader-surface convergence before old-`GC-*` cleanup begins.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the `DOC` contract index, `DOC` front door, and promotion map all read coherently as the steady-state post-quartet surface
  - their distinct reader jobs remain explicit
  - the next follow-up boundary after consolidation is explicit enough that later cleanup does not need to reopen the same wording debate

## P0 (Contract | v1)

### P0-C1-S1 (Post-quartet consolidation boundary fixed | v1)

- `S0F-4F` is now opened as the bounded follow-up after `S0F-4E` completed the first mapped `DOC` promotion quartet.
- This slice does not extract one more contract body.
- It consolidates the already-landed reader surfaces so they stop carrying transitional wording that belonged to the staged promotion period.

### P0-C1-S2 (Primary target surfaces fixed | v1)

- The primary consolidation targets are now fixed as:
  - `docs/governance/contract/INDEX.md`
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-doc-contract-promotion-map-v1.md`
- These three files now form the minimum reader-surface set that should tell one coherent post-quartet story.

### P0-C1-S3 (Immediate sequencing fixed | v1)

- The immediate next step after scaffold is:
  - first inventory residual mixed-transition wording and role overlap across the three target files
  - then converge wording only where steady-state quartet activation makes the stronger answer explicit
- Old-`GC-*` triage and non-`DOC` family evaluation remain later work after this consolidation lane.

## P1 (Residual wording inventory | v1)

### P1-C1-S1 (Residual mixed-transition wording inventoried in `docs/governance/contract/INDEX.md` | v1)

- The `DOC` contract index is already materially correct, but `P1` now fixes three residual wording gaps that still read as if the first mapped quartet were only mid-transition:
  - the `Promotion Path` block still says current source-owner `DOC` logs may later promote into family-owned contracts here, even though the first mapped set is already fully executed
  - the line `Until those files are actually created, the source-owner logs remain the current primary sources` is now too broad because it no longer applies to the first mapped quartet and should be narrowed to future mapping extensions only
  - the `Reader Notes` line `During transition, current DOC meaning may still live primarily in source-owner logs such as S0F-4A, S0F-4B, S0F-3I, and S0F-4C` is now historically true but no longer the strongest current reading for the active quartet
- Role-overlap note:
  - the index should keep directory-level landed-contract inventory and landing rules, but it should stop sounding like a temporary landing pad for the four already-active mapped contracts

### P1-C1-S2 (Residual mixed-transition wording inventoried in `docs/governance/views/view-doc-current-front-door-v1.md` | v1)

- The `DOC` front door is already close to steady-state, but `P1` now fixes three wording issues that still understate the current reader position:
  - the opening sentence `This view is the first current front door` still sounds like an initial transitional surface rather than the standing family-first reader entry after quartet activation
  - the `Current Model` still uses `when one exists` / `otherwise open the stable or bounded source-owner log` language that was correct during staged promotion but now needs tighter wording for the fully active first mapped quartet
  - the line `The current planned promotion map lives at ...` now overstates the map as merely planned when the first mapped set is already executed
- Role-overlap note:
  - the front door should keep family-first reading guidance and quartet-readable current entry behavior, but it should not try to restate the directory-inventory job already owned by the contract index in the same level of detail

### P1-C1-S3 (Residual mixed-transition wording and role ambiguity inventoried in `docs/governance/views/view-doc-contract-promotion-map-v1.md` | v1)

- The promotion map now has the largest wording drift because it still reads almost entirely as a pre-execution planning surface:
  - `This is a promotion map, not a proof that all four contracts have already been extracted` is no longer the best top-level reader note once the first mapping set is already fully executed
  - `Until a promoted file actually exists, the source-owner log remains the current primary source` is now false for the first mapped set as written and needs narrowing to future not-yet-executed mapping extensions
  - the map lacks one explicit statement that the first mapped set is already executed while the mapping surface still remains valid for naming, admission, and future extension semantics
- Role-overlap note:
  - the promotion map should remain the deterministic source-owner-to-contract mapping surface and light historical framing surface, not a duplicate of the contract index or the family front door

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `<ID>/P0-P3: <log title>`
  - discontinuous phases: `<ID>/P0+P3: <log title>`
  - mixed discontinuous + consecutive phases: `<ID>/P0+P3-P4: <log title>`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `<ID>/P*-C*-S*: <one-sentence summary>`.

## Plan (draft)

### P1 (Residual wording inventory)

- P1-C1-S1: inventory residual mixed-transition wording in `docs/governance/contract/INDEX.md`
- P1-C1-S2: inventory residual mixed-transition wording in `docs/governance/views/view-doc-current-front-door-v1.md`
- P1-C1-S3: inventory residual mixed-transition wording and role ambiguity in `docs/governance/views/view-doc-contract-promotion-map-v1.md`

### P2 (Reader-surface convergence)

- P2-C1-S1: converge `INDEX.md` onto steady-state quartet-active directory language
- P2-C1-S2: converge the `DOC` front door onto steady-state quartet-active family-reading language
- P2-C1-S3: converge the promotion map onto `executed first mapping set + still-valid deterministic mapping model` language

### P3 (Post-consolidation boundary)

- P3-C1-S1: fix post-consolidation reader notes and next-step boundary for later `DOC`-adjacent cleanup work
- P3-C1-S2: decide whether any additional bounded export or follow-up is warranted after the reader surfaces converge

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: post-quartet consolidation boundary fixed
- [x] `P0-C1-S2`: primary target surfaces fixed
- [x] `P0-C1-S3`: immediate sequencing fixed

### P1 (Residual wording inventory)

- [x] `P1-C1-S1`: residual mixed-transition wording inventoried in `docs/governance/contract/INDEX.md`
- [x] `P1-C1-S2`: residual mixed-transition wording inventoried in `docs/governance/views/view-doc-current-front-door-v1.md`
- [x] `P1-C1-S3`: residual mixed-transition wording and role ambiguity inventoried in `docs/governance/views/view-doc-contract-promotion-map-v1.md`

### P2 (Reader-surface convergence)

- [ ] `P2-C1-S1`: `INDEX.md` converged onto steady-state quartet-active language
- [ ] `P2-C1-S2`: `DOC` front door converged onto steady-state quartet-active language
- [ ] `P2-C1-S3`: promotion map converged onto executed-first-set plus still-valid mapping language

### P3 (Post-consolidation boundary)

- [ ] `P3-C1-S1`: post-consolidation reader notes and next-step boundary fixed
- [ ] `P3-C1-S2`: bounded follow-up decision fixed

## Current Status

- `S0F-4F` is now opened as the next bounded follow-up after `S0F-4E`: the first mapped `DOC` promotion quartet is active, but the three main `DOC` reader surfaces still need one consolidation pass so they read as one steady-state story instead of as leftover staged landing notes.
- `P0` is now complete: the problem boundary is fixed as reader-surface consolidation rather than one more contract extraction or old-`GC-*` cleanup lane.
- `P1` is now complete: the residual wording inventory is explicit for all three target surfaces, and the remaining work is now tightly bounded to wording convergence rather than additional discovery.
- The immediate next step is `P2`: converge `INDEX.md`, the `DOC` front door, and the promotion map onto one steady-state quartet-active story while keeping their reader jobs distinct.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1 through P0-C1-S3 (post-quartet consolidation lane opened | 2026-04-08)

- headSha: `52117863613f878398446a8c370c370c34a131f9`
- artifacts:
  - `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to explain why the next `DOC` follow-up is a bounded consolidation lane rather than one more promotion lane or immediate old-`GC-*` cleanup
- observed:
  - `S0F-4F` now fixes the post-quartet consolidation boundary, the three primary target surfaces, and the immediate sequencing that keeps reader-surface convergence ahead of later cleanup work

### P1-C1-S1 through P1-C1-S3 (residual wording inventory completed across the three DOC reader surfaces | 2026-04-08)

- headSha: `8a7442cab82032bca32c22ba662f951048e17e7f`
- artifacts:
  - `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/governance/contract/INDEX.md`
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-doc-contract-promotion-map-v1.md`
- expected:
  - one reader should be able to point to the exact residual mixed-transition wording and role-overlap set before any convergence edits are made
- observed:
  - the residual drift set is now bounded: the contract index still carries some future-promotion and source-owner-primary language that is too broad for the active quartet, the DOC front door still carries some first-surface and planned-map wording that understates the steady state, and the promotion map now needs the strongest reframing because it still reads mostly as a pre-execution plan instead of as an executed-first-set mapping surface

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-4F` as the post-quartet `DOC` reader-surface consolidation lane, fixed the three target reader surfaces, and fixed `P1` residual-wording inventory as the immediate next step.
- 2026-04-08: completed `P1` by inventorying the exact residual mixed-transition wording and role-overlap set across the `DOC` contract index, the `DOC` front door, and the promotion map so `P2` can now converge wording without reopening discovery.