# log-S0F-4C (Phase 4C: doc and ops front-door transition and GC demotion model)

---

**id**: `S0F-4C`
**kind**: `log`
**title**: `doc and ops front-door transition and GC demotion model v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Taxonomy, epic/s0, sub/4c`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/397`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/405`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
  **reference_log_1**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  **reference_log_2**: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  **reference_log_3**: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
  **reference_log_4**: `docs/governance/INDEX.md`
  **reference_log_5**: `docs/governance/views/view-contract-family-inventory-v1.md`
  **reference_log_6**: `docs/governance/views/view-contract-family-placement-map-v1.md`
  **reference_log_7**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_8**: `docs/governance/views/view-ops-current-front-door-v1.md`
  **reference_log_9**: `docs/governance/views/view-gc-dual-reading-transition-v1.md`
  **reference_log_10**: `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
**issue_keyword**: `taxonomy`
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
**created**: `2026-04-08`
**updated**: `2026-04-14`

---

## Decision / Outcome

**Decision**:

- `S0F-4C` opens the next bounded follow-up because `S0F-3I` already fixed the seven-family taxonomy, but the repo still lacks one explicit transition model for how readers should move from the old `GC-*` front-door language to family-first `DOC/OPS/...` reading.
- v1 fixes one transition principle:
  - family answers `what kind of contract is this?`
  - front door answers `where should a reader go first for current meaning?`
  - disposition answers `what is the current standing of this surface?`
- Under this model, `GC-*` should no longer be treated as the umbrella name for the whole contract universe.
- `GC-*` survives first as a narrow legacy registry prefix and storage lineage surface while new family-first current reading is introduced gradually, starting with `DOC` and `OPS`.

**Default choices (phase defaults / v1)** (optional, but recommended):

- Do not mass-rename existing `GC-*` files first; reader language and front-door ownership should change before storage identifiers are reconsidered.
- `disposition/placement` remains important, but it cannot replace family classification or current front-door ownership.
- A contract may remain family-owned and current without first becoming a legacy-style registry record.
- `DOC` and `OPS` are the first families that should receive explicit front-door treatment because they are the most reader-facing and the most easily distorted by old registry-first wording.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-4C` fixes the transition language for how the repo should talk about family front doors versus legacy registry prefixes.
- `PR Summary Inputs` remains the automation-facing source block; later view or index work should not reconstruct this transition model from scattered narrative.

**PR summary bullets**:

- Separate `family`, `front door`, and `disposition` so `GC-*` stops acting like the name of the whole contract universe.
- Start the transition with `DOC` and `OPS` rather than mass-renaming old registry files first.
- Fix how `S0F-4A`, `S0F-4B`, and `S0F-3I` should be read as `DOC` contracts even before any later admission or file-renaming work.

**PR checklist source**:

- Default source: reuse this log's execution checklist for any later front-door transition PR.

**PR links**:

- Log: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Previous log: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`

## Exported Sections / Outlet Ownership (optional)

- This slice is expected to end in family-first reader surfaces rather than one more overloaded source log.
- Strong-structure transition decisions remain owned here until later contract, view, or front-door surfaces are explicitly published.

**Outlet ownership**:

- `contract`: stable `DOC/OPS` front-door and transition rules
- `runbook`: none by default; only add if a repeatable operator path is actually needed
- `view`: family-first reader summary comparing old registry wording versus new family wording
- `index/front-door`: current `DOC` and `OPS` entry surfaces plus any narrowed legacy-registry landing note
- `disposition/placement`: legacy `GC-*`, support-only helper views, and later relocation standing
- `log-retained core`: decision, checklist, current status, evidence, and phase sequencing for this transition lane

## Definitions (optional)

- **family front door**: the current reader-facing surface that tells a human where a family's active meaning should be read first
- **legacy registry prefix**: an older storage or record identifier such as `GC-*` that may remain on disk for lineage without remaining the primary reader vocabulary
- **dual-reading transition**: a bounded period where the repo keeps old storage identifiers but asks readers to interpret current meaning through the new family-first front door
- **disposition**: standing such as `current`, `legacy`, `support-only`, `deprecated`, or `superseded`

## Constraints

- Do not let `GC-*` continue to imply the whole contract universe once the seven-family taxonomy already exists.
- Do not use `disposition/placement` as a substitute for family ownership.
- Do not mass-rename current files until the new family-first front doors actually exist.
- Do not force `DOC` and `OPS` into one generic governance bucket once their reader-facing meaning can already be separated cleanly.

## Scope

- `P0`: fix the transition model among family, front door, legacy registry prefix, and disposition
- `P1`: define the first `DOC` current front-door model
- `P2`: define the first `OPS` current front-door model
- `P3`: define the `GC-*` demotion and dual-reading transition rule
- `P4`: define how `disposition/placement` helps migration without replacing family or front-door ownership

## Success Criteria (DoD)

- One reader can explain why `S0F-4A`, `S0F-4B`, and `S0F-3I` are `DOC` contracts even before any later registry admission work.
- One reader can explain why `GC-*` should survive first as legacy registry lineage rather than as the name of the whole contract universe.
- The repo has one explicit transition answer for how to move from registry-first wording to family-first wording without immediate mass rename.
- The repo has one explicit statement that `disposition` helps standing and cleanup, but does not replace family classification or front-door ownership.
- `DOC` and `OPS` have one bounded next-step lane for family-first front-door work instead of remaining hidden behind the old `GC-*` vocabulary.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the `DOC` and `OPS` front-door transition model is explicit enough that future slices stop asking whether every important rule must first become a `GC-*` record
  - the repo has one clear dual-reading transition rule for old registry identifiers versus new family-first reading

## P0 (Contract | v1)

### P0-C1-S1 (Family versus front-door rule | v1)

- A family says what kind of contract a surface is.
- A front door says where a current reader should look first.
- One family may have a current front door without requiring every supporting or legacy surface to live under the same directory or prefix.

### P0-C1-S2 (GC demotion rule | v1)

- `GC-*` should now be read as a legacy or narrow registry prefix, not as the name of the whole contract universe.
- During transition, old `GC-*` storage identifiers may remain on disk while reader-facing current interpretation moves to family-first front doors.

### P0-C1-S3 (Disposition role rule | v1)

- `disposition/placement` answers standing and cleanup state.
- It may say `legacy`, `support-only`, `deprecated`, or `current family-owned`, but it does not answer the first question of family ownership by itself.

## P1 (DOC front door | v1)

### P1-C1-S1 (First DOC current front-door shape | v1)

- The repo now keeps one current `DOC` family reader entry at:
  - `docs/governance/views/view-doc-current-front-door-v1.md`
- That surface is intentionally family-first rather than registry-first:
  - it tells the reader how to start reading current `DOC` meaning
  - it does not require creating or reusing a `GC-*` record just to make `DOC` legible

### P1-C1-S2 (DOC source-owner mapping | v1)

- The first `DOC` front door currently maps these source-owner contracts directly:
  - `S0F-4A`: document role boundaries, write-back protocol, and disposition model
  - `S0F-4B`: source-log compatibility and weak-structure export discipline
  - `S0F-3I`: governance contract taxonomy and placement model
  - `S0F-4C`: family-front-door transition and `GC-*` demotion model
- Under this model, those surfaces are already current `DOC` contracts even before any later admission or naming reform work.

## P2 (OPS front door | v1)

### P2-C1-S1 (First OPS current front-door shape | v1)

- The repo now keeps one current `OPS` family reader entry at:
  - `docs/governance/views/view-ops-current-front-door-v1.md`
- That surface is family-first rather than registry-first:
  - it tells the reader how to start reading current `OPS` meaning
  - it does not require turning active runtime spines or runbooks into registry records just to make the family legible

### P2-C1-S2 (OPS source-owner mapping | v1)

- The first `OPS` front door currently maps these source-owner surfaces directly:
  - `S4A`: systems/platform operations runtime foundation
  - `S4D`: cloud runtime deploy/verify/rollback
  - `S4E`: release operating model and governance boundary
  - `run-S4D-cloud-runtime-release-operations`: stable operator-facing release path
- Under this model, current `OPS` reading stays anchored in runtime spines, runbooks, workflows, and scripts rather than being compressed into one narrow registry surface.

## P3 (GC demotion and dual-reading transition | v1)

### P3-C1-S1 (Legacy-registry versus family-first dual-reading rule | v1)

- The repo now keeps one explicit transition surface at:
  - `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- Under this rule:
  - `GC-*` remains valid as storage and lineage vocabulary
  - family current front doors become the first reader vocabulary where they already exist
  - `docs/governance/INDEX.md` remains valid, but only as the narrow registry front door rather than the universal contract front door

  ## P4 (Disposition role in migration | v1)

  ### P4-C1-S1 (Disposition supports standing and cleanup, not family ownership | v1)

  - The repo now keeps one explicit disposition-role surface at:
    - `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
  - Under this rule:
    - disposition answers current versus legacy/support-only/deprecated standing
    - disposition may guide placement and cleanup decisions
    - disposition does not replace family classification or current front-door ownership

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

**Branch convention**:

- For logs tied to a specific scope/index, prefer making P* code and documentation changes on a working branch with the same prefix.
- If a single PR touches multiple scopes/indexes, prefer splitting it into multiple PRs so each PR stays focused on one scope/index and its corresponding branch for easier aggregation and traceability.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (DOC front door)

- P1-C1-S1: define the first `DOC` current front-door shape
- P1-C1-S2: map `S0F-4A`, `S0F-4B`, and `S0F-3I` into that `DOC` reading model

### P2 (OPS front door)

- P2-C1-S1: define the first `OPS` current front-door shape
- P2-C1-S2: separate `OPS` current reading from old governance-registry wording

### P3 (GC demotion and dual-reading transition)

- P3-C1-S1: define how old `GC-*` terms remain usable as lineage/storage identifiers without remaining the primary reader vocabulary

### P4 (Disposition role in migration)

- P4-C1-S1: define how `disposition/placement` supports transition without replacing family or front-door ownership

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: family versus front-door rule fixed
- [x] `P0-C1-S2`: `GC-*` demotion rule fixed
- [x] `P0-C1-S3`: disposition role rule fixed

### P1 (DOC front door)

- [x] `P1-C1-S1`: first `DOC` current front-door shape defined
- [x] `P1-C1-S2`: `S0F-4A`, `S0F-4B`, and `S0F-3I` mapped into `DOC` reading model

### P2 (OPS front door)

- [x] `P2-C1-S1`: first `OPS` current front-door shape defined
- [x] `P2-C1-S2`: `OPS` current reading separated from old governance-registry wording

### P3 (GC demotion and dual-reading transition)

- [x] `P3-C1-S1`: legacy-registry versus family-first dual-reading transition fixed

### P4 (Disposition role in migration)

- [x] `P4-C1-S1`: disposition role fixed for transition without replacing family ownership

## Current Status (recommended)

- `S0F-4C` is now opened as the next bounded transition lane after `S0F-3I/P5`: the repo has a family taxonomy and placement map, but it still needs one explicit reader-facing migration model away from registry-first `GC-*` language.
- `P0` is now fixed: family, front door, legacy registry prefix, and disposition are now separated conceptually enough to guide later `DOC` and `OPS` front-door work.
- `P1` is now complete: the repo now has one first `DOC` current front door at `docs/governance/views/view-doc-current-front-door-v1.md`, and `S0F-4A`, `S0F-4B`, `S0F-3I`, and `S0F-4C` are now explicitly readable as current `DOC` contracts without first passing through `GC-*` vocabulary.
- `P2` is now complete: the repo now has one first `OPS` current front door at `docs/governance/views/view-ops-current-front-door-v1.md`, and current operational meaning now reads through `S4A`, `S4D`, `S4E`, and the stable runbook layer rather than through old governance-registry wording.
- `P3` is now complete: the repo now has one explicit dual-reading rule, so `GC-*` may remain as lineage/storage vocabulary while current reading moves to family front doors where those already exist.
- `P4` is now complete: the repo now has one explicit rule for what `disposition` owns during transition, so standing and cleanup can be clarified without blurring family ownership or current front-door reading.
- `S0F-4C` is now stable: `DOC` and `OPS` current front doors exist, the `GC-*` dual-reading rule is explicit, and `disposition` is now bounded to standing and cleanup rather than to family meaning.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1 through P0-C1-S3 (transition model opened and fixed at contract level | 2026-04-08)

- headSha: `25e294734db8c6828c9746164507b292709e9d4b`
- artifacts: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to explain why `GC-*` can no longer serve as the umbrella term once the seven-family taxonomy already exists
- observed:
  - `S0F-4C` now fixes the first transition boundary and opens the next bounded follow-up around `DOC` and `OPS` family-first front doors

### P1-C1-S1 through P1-C1-S2 (DOC current front door defined and mapped | 2026-04-08)

- headSha: `455724f6aa70aa6a5e554221bee8a13b0610d9dc`
- artifacts: `docs/governance/views/view-doc-current-front-door-v1.md`
- artifacts: `docs/governance/views/view-contract-family-inventory-v1.md`
- artifacts: `docs/governance/views/view-contract-family-placement-map-v1.md`
- artifacts: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- expected:
  - one reader should be able to find the current `DOC` family entry and read `S0F-4A`, `S0F-4B`, and `S0F-3I` as `DOC` contracts without first translating them into legacy registry language
- observed:
  - the repo now has one explicit `DOC` family front door and one direct mapping from that front door to the current source-owner `DOC` contracts

### P2-C1-S1 through P2-C1-S2 (OPS current front door defined and mapped | 2026-04-08)

- headSha: `81bc3dbf426adf2c84c3cdf5a7d77d8c83b0cd14`
- artifacts: `docs/governance/views/view-ops-current-front-door-v1.md`
- artifacts: `docs/governance/views/view-contract-family-inventory-v1.md`
- artifacts: `docs/governance/views/view-contract-family-placement-map-v1.md`
- artifacts: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- expected:
  - one reader should be able to find the current `OPS` family entry and read runtime-operational meaning without first translating it into narrow governance-registry wording
- observed:
  - the repo now has one explicit `OPS` family front door and one direct mapping from that front door to the current runtime spines and runbook-owned operational surfaces

### P3-C1-S1 (legacy-registry versus family-first dual-reading rule fixed | 2026-04-08)

- headSha: `f1a28ceaf81a41344d2d555f32b2d98c1aa6c73e`
- artifacts: `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- artifacts: `docs/governance/INDEX.md`
- artifacts: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- expected:
  - one reader should be able to preserve old `GC-*` lineage while switching current reading to family-first front doors where they already exist
- observed:
  - the repo now has one explicit dual-reading rule, and `docs/governance/INDEX.md` now reads as the narrow registry front door rather than as the universal front door for every contract family

### P4-C1-S1 (disposition role fixed for family-first transition | 2026-04-08)

- headSha: `bbff10fa1ac0d8d37d0ca6f4b23ed2c8e791bb95`
- artifacts: `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
- artifacts: `docs/governance/views/view-contract-family-placement-map-v1.md`
- artifacts: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to explain how disposition supports standing and cleanup during transition without treating it as a substitute for family or front-door ownership
- observed:
  - the repo now has one explicit disposition-role surface, and `S0F-4C` now closes with family, front door, lineage vocabulary, and standing all separated clearly enough for later transition work

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-4C` to separate family, front door, legacy registry prefix, and disposition so the repo can move toward `DOC/OPS/...` current reading without immediate mass rename.
- 2026-04-08: completed `P1` by publishing the first `DOC` current front door and by mapping `S0F-4A`, `S0F-4B`, `S0F-3I`, and `S0F-4C` into one family-first reading model.
- 2026-04-08: completed `P2` by publishing the first `OPS` current front door and by mapping `S4A`, `S4D`, `S4E`, and the stable release-operations runbook into one family-first reading model.
- 2026-04-08: completed `P3` by publishing the first dual-reading transition rule, so old `GC-*` identifiers remain valid for lineage and storage while current reading shifts to family front doors where available.
- 2026-04-08: completed `P4` by publishing the disposition-role rule, so standing and cleanup now support family-first transition without replacing family ownership or current front-door reading.