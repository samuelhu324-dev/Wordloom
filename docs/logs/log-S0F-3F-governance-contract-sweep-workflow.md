# log-S0F-3F (Phase 3F: governance contract sweep workflow)

---

**id**: `S0F-3F`
**kind**: `log`
**title**: `governance contract sweep workflow v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Contract, Registry, Sweep, Audit, epic/s0, sub/3f`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
  **reference_log_1**: `docs/logs/log-S0F-3C-governance-contract-series-audit-and-admission.md`
  **reference_log_2**: `docs/logs/log-S0F-3D-first-governance-contract-landing-batch.md`
  **reference_log_3**: `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
  **reference_log_4**: `docs/governance/views/view-contract-sweep-workflow-v1.md`
  **reference_log_5**: `docs/governance/views/view-s0f-1-family-sweep-v1.md`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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
**created**: `2026-04-06`
**updated**: `2026-04-06`

---

## Decision / Outcome

**Decision**:

- `S0F-3F` opens the next follow-up slice for a repeatable governance-contract sweep workflow.
- This slice exists because the repo now has enough registry structure to sweep remaining source families one bounded series at a time, but it does not yet have one fixed worksheet for how each candidate must be judged before contracts are created, split, refined, absorbed, or left as history only.
- v1 therefore turns `contract sweep` into a declared workflow with three explicit parts:
  - one required candidate worksheet for each bounded source family
  - one fixed decision table of allowed sweep outcomes
  - one fixed action matrix that says what writes are allowed for each outcome and what writes remain forbidden

**Default choices (phase defaults / v1)**:

- Sweep one bounded family at a time; do not reopen whole-repo discovery during each execution pass.
- Every candidate row must end in one explicit outcome before any current-state contract write is allowed.
- Humans declare semantic outcomes; mechanics validate closure, redirects, successor existence, and front-door consistency.
- Old contracts are not deleted merely because a later sweep reclassifies them.
- `INDEX.md` remains current-state-only; sweep history, lineage, and packaging details belong in slice logs, legacy files, and views.
- A sweep may end with `no new current contract` for some or all rows; the workflow exists to prevent forced admission, not to guarantee growth.

## Scope

- `P0`: open `S0F-3F`, wire it into the `S0F` spine, and publish the first reusable contract-sweep workflow skeleton
- `P1`: fix the required sweep packet and candidate worksheet fields for one bounded source family
- `P2`: fix the decision table that every worksheet row must resolve through
- `P3`: fix the allowed-action matrix for each sweep outcome
- `P4`: fix the mandatory write targets, preservation notes, and stop rules that keep current-state surfaces readable
- `P5`: run the first bounded family through the worksheet and use the workflow to decide the next execution package

## Current Status

- `S0F-3F` is now opened as the next `S0F` follow-up slice for repeatable governance-contract sweeping after the registry-lineage baseline fixed by `S0F-3E`.
- `P0` is now complete: the repo now has a first `contract sweep workflow v1` scaffold with one required worksheet shape, one decision table, and one allowed-action matrix.
- `P1` is now complete for the first bounded source family: `S0F-1A` through `S0F-1J` now have one explicit sweep packet and one candidate worksheet instead of being treated as ten unrelated future admissions.
- `P2` is now complete for that same bounded family: the first `S0F-1` worksheet outcomes are now formally adjudicated, no row remains in an unresolved defer queue, and the family now exits `P2` with one clear admission candidate plus one small refinement package.
- `P3` is now complete for that same bounded family: the accepted `S0F-1` outcomes are now translated into one split action-package model, with `R1` reserved for bounded traceability refinement and `A1` reserved for remediation-governance admission work.
- `P4` is now complete for the justified first write stage: `R1` has been executed on `GC-ICR-0001` and `GC-PRA-0001`, front-door state remains unchanged, and `A1` remains blocked until remediation-governance naming and scope are explicit enough for admission work.
- The first `S0F-1` worksheet shows a mixed result by design: most stable semantic surfaces are already covered by current contracts, several later slices remain support-only history, and one bounded remediation surface still looks like a real current-admission candidate.
- The workflow is intentionally conservative: it exists to reduce ad hoc judgment drift before future family sweeps scale out.
- The immediate next follow-up is `P5`: close the first pilot run by recording what this family sweep proved, while carrying `A1` forward as the next bounded admission-design package rather than silently auto-executing it.

## Problem Statement

- `S0F-3C` established which source families can yield governance contracts.
- `S0F-3D` and `S0F-3E` proved that admission, split, and legacy handling can be executed safely.
- The remaining problem is operational scale: many retained logs can now be reviewed family by family, but the repo still lacks one fixed worksheet that says:
  - what evidence must be collected before judgment,
  - what outcomes are valid,
  - and what writes are permitted for each outcome.
- Without this workflow, future sweeps risk mixing semantic judgment, file-writing, and historical cleanup in inconsistent ways.

## Contract Sweep Workflow v1

### Sweep Unit

- One sweep run covers one bounded source family or one tightly related family subset.
- A bounded sweep unit should usually share at least one of these properties:
  - same lifecycle surface
  - same contract area or candidate area
  - same enforcement owner
  - same current-state reading question
- Do not mix unrelated families just because they are all still unswept.

### Required Sweep Packet

- Every sweep run should begin with one packet that records:
  - bounded source family
  - included logs or existing contracts under review
  - already-active current contracts that may overlap
  - any known frozen legacy area or legacy umbrella records
  - the exact question being answered by this sweep
  - the stop condition for this run
- If the sweep packet is incomplete, the run should stop before contract writes begin.

## P1 Baseline (Candidate worksheet)

### Required Row Fields

- Every candidate row should record at least:
  - `candidate surface`
  - `source owner`
  - `current semantic owner, if any`
  - `overlap type`
  - `proposed outcome`
  - `reason for outcome`
  - `allowed action package`
  - `front-door effect`
  - `legacy effect`

### Overlap Type Rules

- `none`:
  - no current contract appears to own the same governed surface
- `same-surface versional`:
  - one current contract already owns the same surface, but the candidate may require one newer same-surface version
- `same-surface refinement`:
  - one current contract owns the surface and the candidate only sharpens its current explanation or source support
- `partial decomposition`:
  - one current surface appears too coarse and the candidate indicates a narrower split is needed
- `support-only`:
  - the candidate provides evidence, packaging, or historical support without owning the live rule itself
- `unclear`:
  - the sweep has not yet justified any stronger classification

## P1 First Bounded Family Execution (`S0F-1A` through `S0F-1J`)

### Sweep Packet

- bounded source family:
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  - `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
  - `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
  - `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
  - `docs/logs/log-S0F-1E-completeness-classification-buckets-and-audit-output-taxonomy.md`
  - `docs/logs/log-S0F-1F-bucketed-audit-output-materialization.md`
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
  - `docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md`
  - `docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md`
  - `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- already-active current contracts reviewed for overlap:
  - `GC-ICR-0001`
  - `GC-ICT-0001`
  - `GC-IID-0001`
  - `GC-IID-0002`
  - `GC-PRA-0001`
  - `GC-COMPL-0001`
  - `GC-PRR-0001`
  - `GC-PRG-0001`
- known legacy surfaces under this family context:
  - legacy `GC-ISS-*` records preserved after the `ISS` split
  - legacy `GC-PRB-0001` umbrella preserved after the `PRB` split
- exact question answered by this sweep:
  - which `S0F-1` semantic surfaces are already concentrated into current governance contracts,
  - which `S0F-1` surfaces are only support, repair, or packaging history,
  - and whether one bounded not-yet-landed current-admission candidate still remains inside the family
- stop condition for this run:
  - stop before current-state writes if any worksheet row cannot defend one primary current owner or one non-current classification

### Candidate Worksheet

| candidate surface | source owner | current semantic owner | overlap type | proposed outcome | reason for outcome | allowed action package | front-door effect | legacy effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| issue-create fail-closed boundary | `S0F-1A` | `GC-ICR-0001` | `same-surface refinement` | `refine existing` | current issue-create contract already owns deterministic metadata and create-time scaffold boundaries, but `S0F-1A` remains the first stable fail-closed entrypoint clarification | later add `S0F-1A` traceability to `GC-ICR-0001` | none in `INDEX.md` | no legacy change |
| PR-create front-half preflight boundary | `S0F-1A` | `GC-PRA-0001` | `same-surface refinement` | `refine existing` | current PR-create contract already owns exact commit scoping and bounded create-time staging, but `S0F-1A` still clarifies the fail-closed publish boundary | later add `S0F-1A` traceability to `GC-PRA-0001` | none in `INDEX.md` | no legacy change |
| issue Context LLM-authored exact-count rule | `S0F-1B` | `GC-ICT-0001` | `same-surface refinement` | `already covered` | current issue-Context contract already treats `S0F-1B` as the current authoring-path owner inside the same sentence-count rule | no current-state write required | none | no legacy change |
| guarded multi-item remediation stages | `S0F-1C` | `` | `none` | `admit new current` | stable batch-stage vocabulary, wrapper-owned live mutation boundary, and per-target failure semantics remain unrepresented at the front door even after `S0F-3D` and `S0F-3E` | later admit one bounded current remediation contract and area code | later add one new area only if `P2/P3` confirm | no legacy change required yet |
| lifecycle three-stage completeness matrix | `S0F-1D` | `GC-COMPL-0001` | `same-surface refinement` | `already covered` | `GC-COMPL-0001` is already the concentrated current contract for this exact semantic surface | no current-state write required | none | no legacy change |
| completeness diagnosis bucket taxonomy | `S0F-1E` | `` | `support-only` | `support-only history` | bucket taxonomy sharpens audit reading, but it does not own an independent front-door governance rule beyond the current completeness matrix | keep as supporting history only | none | retain log and artifacts only |
| bucketed audit output materialization | `S0F-1F` | `` | `support-only` | `support-only history` | emitted diagnosis-layer fields are runtime and retained-output packaging, not a separate current governance surface | keep as supporting history only | none | retain log and artifacts only |
| parent sidebar ordering ownership | `S0F-1G` | `GC-IID-0001` | `same-surface refinement` | `already covered` | current issue-identity contract already owns this exact source-log-versus-GitHub ordering rule | no current-state write required | none | no legacy change |
| title keyword controlled vocabulary | `S0F-1G` | `GC-IID-0002` | `same-surface refinement` | `already covered` | current issue-identity contract already concentrates create-time and audit-time title keyword governance | no current-state write required | none | no legacy change |
| PR body canonical review classification | `S0F-1H` | `GC-PRR-0001` | `same-surface refinement` | `already covered` | current PR-review contract already concentrates the read-only reviewer classification semantics directly from `S0F-1H` | no current-state write required | none | no legacy change |
| formatting-only merged-PR convergence lane | `S0F-1I/P1-P3` | `` | `support-only` | `support-only history` | this lane consumes reviewer results and performs bounded repair, but it does not own a new enduring current rule after convergence is complete | keep as supporting repair history only | none | retain log and artifacts only |
| packaged PR-body standard-check gate | `S0F-1I/P4 + S0F-1J/P1-P3` | `GC-PRG-0001` | `same-surface refinement` | `already covered` | current PR-gate contract already concentrates fail-on-substantive-drift semantics and packaged local or CI replay surfaces | no current-state write required | none | no legacy change |

### P1 Result

- The first bounded `S0F-1` worksheet does not justify a bulk registry expansion.
- Current result by row class:
  - `already covered`: `S0F-1B`, `S0F-1D`, `S0F-1G` sidebar ordering, `S0F-1G` title keyword governance, `S0F-1H`, and `S0F-1I/P4 + S0F-1J/P1-P3`
  - `refine existing`: `S0F-1A` issue-create and PR-create boundary clarifications
  - `support-only history`: `S0F-1E`, `S0F-1F`, and `S0F-1I/P1-P3`
  - `candidate new current`: `S0F-1C`
- The first worksheet therefore suggests one narrow next package rather than another broad sweep:
  - if `P2` accepts the provisional outcomes, the most likely next current-admission work is one bounded remediation-governance contract derived from `S0F-1C`
  - before that, the lighter-weight refinement package is to add `S0F-1A` traceability to `GC-ICR-0001` and `GC-PRA-0001`

## P2 Baseline (Decision table)

### Allowed Outcomes

- `already covered`:
  - no new current contract is needed because an existing current contract already owns the active semantics
- `refine existing`:
  - keep the current contract, but sharpen its wording, source refs, or reader guidance
- `split current`:
  - decompose one coarse current contract or area into multiple narrower current contracts or areas
- `supersede current`:
  - replace one current contract with one newer current contract for the same governed surface
- `absorb into current`:
  - stop treating one older or candidate surface as independently active because its semantics now live fully inside one current contract
- `retire surface`:
  - keep the historical record only; no current successor is required
- `admit new current`:
  - create one new current contract because no existing current contract owns this surface
- `support-only history`:
  - keep the source only as history, evidence, packaging, or backfill support
- `defer adjudication`:
  - stop without writing current-state changes because the sweep cannot yet defend a stronger result

### Required Decision Discipline

- Each row must resolve to exactly one outcome.
- Do not write contracts from an `unclear` row.
- Do not use `admit new current` merely because a candidate is recent or well written.
- Do not use `support-only history` as a vague discard bucket when the real outcome is `split current`, `absorb into current`, or `retire surface`.

## P2 First Bounded Family Adjudication (`S0F-1A` through `S0F-1J`)

### Accepted Outcomes

- `refine existing`:
  - `S0F-1A` issue-create fail-closed boundary -> `GC-ICR-0001`
  - `S0F-1A` PR-create front-half preflight boundary -> `GC-PRA-0001`
- `already covered`:
  - `S0F-1B` issue Context LLM-authored exact-count rule -> `GC-ICT-0001`
  - `S0F-1D` lifecycle three-stage completeness matrix -> `GC-COMPL-0001`
  - `S0F-1G` parent sidebar ordering ownership -> `GC-IID-0001`
  - `S0F-1G` title keyword controlled vocabulary -> `GC-IID-0002`
  - `S0F-1H` PR body canonical review classification -> `GC-PRR-0001`
  - `S0F-1I/P4 + S0F-1J/P1-P3` packaged PR-body standard-check gate -> `GC-PRG-0001`
- `support-only history`:
  - `S0F-1E` completeness diagnosis bucket taxonomy
  - `S0F-1F` bucketed audit output materialization
  - `S0F-1I/P1-P3` formatting-only merged-PR convergence lane
- `admit new current`:
  - `S0F-1C` guarded multi-item remediation stages

### Defer Queue

- No row remains in `defer adjudication` for the first bounded `S0F-1` family pass.
- This does not mean every row will cause front-door writes.
- It means every row now has one defended primary outcome, so later packaging can proceed without reopening classification.

### P2 Adjudication Result

- The first bounded `S0F-1` family now exits `P2` with two intentionally separate downstream lanes:
  - one small refinement lane:
    - add `S0F-1A` traceability to `GC-ICR-0001`
    - add `S0F-1A` traceability to `GC-PRA-0001`
  - one bounded current-admission lane:
    - evaluate one remediation-governance contract derived from `S0F-1C`
- The first bounded family does not justify any further current admission for:
  - `S0F-1E`
  - `S0F-1F`
  - `S0F-1I/P1-P3`
- The first bounded family also does not justify reopening current front-door ownership for:
  - `S0F-1B`
  - `S0F-1D`
  - `S0F-1G`
  - `S0F-1H`
  - `S0F-1I/P4 + S0F-1J/P1-P3`

## P3 First Bounded Family Action Package (`S0F-1A` through `S0F-1J`)

### Package Split Rule

- The first bounded `S0F-1` family does not collapse into one mixed execution bundle.
- `P3` fixes two separate packages and treats their separation as part of the governance contract:
  - `R1`: bounded current-refinement package
  - `A1`: bounded current-admission package
- Any attempt to merge those two packages into one write pass is out of scope for the first pilot run because it would mix low-risk traceability refinement with front-door area-admission change.

### `R1` Bounded Current-Refinement Package

- target writes:
  - update `GC-ICR-0001` to add `S0F-1A` as current boundary clarification for fail-closed issue-create entrypoints
  - update `GC-PRA-0001` to add `S0F-1A` as current boundary clarification for fail-closed PR-create front-half preflight
- explicit non-writes:
  - no `INDEX.md` change
  - no new area code
  - no legacy redirect change
- rationale:
  - these two rows were adjudicated as `refine existing`, so the justified write is traceability and reader-guidance concentration only

### `A1` Bounded Current-Admission Package

- target work:
  - derive one current remediation-governance contract from `S0F-1C`
  - decide whether that contract should revive the earlier `REMED` shortlist area from `S0F-3C` or land under a narrower newly defended area name
  - prepare the minimal front-door package only after that area and contract boundary are explicit
- explicit non-writes at `P3`:
  - do not yet update `INDEX.md`
  - do not yet create a new contract file
  - do not yet admit any second remediation-adjacent record
- rationale:
  - `S0F-1C` is the only adjudicated `admit new current` row in the first bounded family, so it remains the only candidate admission lane for the next write stage

### Explicit Exclusion Set

- `P3` excludes these surfaces from the current action package entirely:
  - `S0F-1E`
  - `S0F-1F`
  - `S0F-1I/P1-P3`
  - all rows already adjudicated as `already covered` with no further refinement need
- `P3` also excludes package mixing such as:
  - adding `S0F-1A` traceability and a new remediation area in one commit unit
  - sweeping `ATTR`, `WF`, or any non-`S0F-1` family while this pilot family is still being executed

### P3 Result

- The first bounded family now has one execution order rather than only one classification result:
  - execute `R1` first
  - hold `A1` until the remediation-governance contract boundary and area-code choice are explicit enough for front-door mutation
- This means the first pilot family can advance under `P4` without reopening `P2` and without silently widening scope.

## P4 First Bounded Family Write Stage (`S0F-1A` through `S0F-1J`)

### Executed Writes

- `R1` is now executed.
- Applied writes:
  - `GC-ICR-0001` now cites `S0F-1A` as the current fail-closed issue-create boundary clarification
  - `GC-PRA-0001` now cites `S0F-1A` as the current fail-closed PR-create front-half clarification

### Validated Non-Writes

- `INDEX.md` remains unchanged.
- No new area code is admitted during this stage.
- No legacy redirect or frozen-area state changes are introduced during this stage.

### Blocked Package Carry-Forward

- `A1` remains blocked by design after `P4`.
- The blocker is not execution capacity; the blocker is missing front-door precision:
  - remediation-governance current scope is not yet compressed into one explicit contract shape
  - area naming is not yet fixed tightly enough to decide whether `REMED` should be reactivated or narrowed further

### P4 Result

- The first bounded family now proves that the workflow can execute refinement-only writes without accidentally dragging admission work across the boundary.
- The pilot family therefore exits `P4` in a clean intermediate state:
  - `R1` executed and validated
  - `A1` intentionally held for later admission design

## P3 Baseline (Allowed-action matrix)

### Outcome-to-Action Mapping

- `already covered`:
  - allowed actions:
    - update the sweep log or view to state current ownership
    - add source refs to the existing contract if they materially clarify current meaning
  - forbidden actions:
    - create a duplicate current contract
    - add a new area code only to preserve one extra source file
- `refine existing`:
  - allowed actions:
    - modify one current contract
    - update one view or lineage note if the refinement changes reader guidance
  - forbidden actions:
    - create a parallel current record for the same surface without a defended split or supersede reason
- `split current`:
  - allowed actions:
    - create narrower successor current contracts
    - freeze the old area if area-level decomposition is happening
    - deprecate the old umbrella contract with deterministic redirects
    - update `INDEX.md`, one lineage view, and the sweep slice log
  - forbidden actions:
    - keep admitting new records into the old coarse area after freeze
- `supersede current`:
  - allowed actions:
    - create one successor current contract
    - mark the old record as `superseded`
    - update the front door to point to the new current record
  - forbidden actions:
    - keep both old and new records active for the same surface without explicit versional justification
- `absorb into current`:
  - allowed actions:
    - modify the absorbing current contract if needed
    - deprecate the absorbed record or keep the candidate as non-current support
    - update reader notes or legacy redirects
  - forbidden actions:
    - preserve the absorbed record as a parallel active rule
- `retire surface`:
  - allowed actions:
    - mark the old record as `retired`
    - remove it from current-state reading surfaces
    - keep historical notes explaining why no successor exists
  - forbidden actions:
    - invent a fake current successor purely to avoid an empty redirect
- `admit new current`:
  - allowed actions:
    - create one new current contract
    - update `INDEX.md`
    - add one view only if the new contract needs concentrated reader help
  - forbidden actions:
    - bulk-admit adjacent candidates that have not been adjudicated
- `support-only history`:
  - allowed actions:
    - keep the source in logs, backfill notes, or support-only historical files
    - mention it in the sweep result as non-current support
  - forbidden actions:
    - surface it in `INDEX.md` as if it were a current contract
- `defer adjudication`:
  - allowed actions:
    - record the unresolved question and explicit blocker
    - stop the sweep at the bounded queue
  - forbidden actions:
    - half-admit or half-retire the row without a defended outcome

## P4 Baseline (Write targets and stop rules)

### Mandatory Write Targets by Sweep Type

- Every completed sweep should update:
  - the active slice log
  - the `S0F` parent spine status when the slice materially advances
- A sweep that changes current-state contracts should also update:
  - `docs/governance/contracts/`
  - `docs/governance/INDEX.md`
  - one governance view when lineage or current-vs-history reading would otherwise become noisy
- A sweep that changes only historical classification may stop short of `INDEX.md` if current-state meaning does not change.

### Stop Rules

- Stop if the sweep packet is incomplete.
- Stop if one candidate row still requires more than one possible outcome.
- Stop if the proposed action package would change `INDEX.md` but no defended current-state owner exists.
- Stop if an old current record would lose active standing without a deterministic legacy note.
- Stop if the sweep tries to mix current-state concentration with unrelated implementation cleanup.

## P5 Next Execution Boundary

- The first execution under this slice should pick one bounded unswept family and run the full worksheet before any new contract admission.
- That run should end in one of three package-level results:
  - `no-op current-state`: everything is already covered or support-only
  - `bounded current refinement`: existing current contracts need refinement, split, absorption, supersede, or retirement work
  - `bounded new admission`: one or more defended new current contracts should be landed next
- The first execution run should remain small enough that one reviewer can still read the full decision table without losing current-state meaning.

## Plan (draft)

### P0 (Slice opening and workflow scaffold)

- P0-C1-S1: create `S0F-3F` and wire it into the `S0F` parent spine
- P0-C1-S2: publish the first `contract sweep workflow v1` scaffold and supporting governance view

### P1 (Sweep packet and worksheet)

- P1-C1-S1: choose the first bounded source family for execution
- P1-C1-S2: fill the candidate worksheet for that family without writing current-state contracts yet

### P2 (Decision table)

- P2-C1-S1: resolve every worksheet row to one allowed outcome
- P2-C1-S2: isolate unresolved rows into one explicit defer queue instead of forcing admission

### P3 (Allowed-action package)

- P3-C1-S1: translate resolved outcomes into one bounded action package
- P3-C1-S2: reject any action package that mixes unrelated cleanup with current-state concentration

### P4 (Write targets and stop rules)

- P4-C1-S1: apply only the write targets justified by the chosen outcomes
- P4-C1-S2: validate redirects, successor existence, and front-door cleanliness

### P5 (First pilot run)

- P5-C1-S1: complete one first bounded family sweep through the v1 worksheet
- P5-C1-S2: record whether the workflow needs another refinement pass before wider reuse

## Execution Checklist (unchecked)

### P0 (Slice opening and workflow scaffold)

- [x] `P0-C1-S1`: `S0F-3F` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: first `contract sweep workflow v1` scaffold and supporting view published

### P1 (Sweep packet and worksheet)

- [x] `P1-C1-S1`: first bounded source family chosen for execution
- [x] `P1-C1-S2`: candidate worksheet filled before current-state writes begin

### P2 (Decision table)

- [x] `P2-C1-S1`: all worksheet rows resolved to one allowed outcome
- [x] `P2-C1-S2`: unresolved rows isolated into one explicit defer queue

### P3 (Allowed-action package)

- [x] `P3-C1-S1`: one bounded action package derived from the resolved outcomes
- [x] `P3-C1-S2`: unrelated cleanup excluded from the current-state action package

### P4 (Write targets and stop rules)

- [x] `P4-C1-S1`: only justified write targets updated
- [x] `P4-C1-S2`: redirects, successor existence, and front-door cleanliness validated

### P5 (First pilot run)

- [ ] `P5-C1-S1`: first bounded family sweep completed through the v1 workflow
- [ ] `P5-C1-S2`: workflow refinement needs recorded after the pilot run