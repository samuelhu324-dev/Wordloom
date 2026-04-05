# log-S0F-2A (Phase 2A: maintenance lanes and direct patch ledger)

---

**id**: `S0F-2A`
**kind**: `log`
**title**: `maintenance lanes and direct patch ledger v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Packaging, Contract, epic/s0, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
  **reference_log_1**: `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
  **reference_log_2**: `docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md`
  **reference_log_3**: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
  **reference_log_4**: `docs/logs/ledger-direct-patch-commits.md`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/2`
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
**created**: `2026-04-05`
**updated**: `2026-04-05`

---

## Decision / Outcome

**Decision**:

- `S0F-2A` institutionalizes one explicit three-lane model for work that does not fit cleanly into the existing full slice log lifecycle: standard slice work, maintenance sweep work, and tiny direct patch work.
- `S0F-2A` institutionalizes one explicit three-lane model for work that does not fit cleanly into the existing full slice log lifecycle: standard slice work, maintenance sweep work, and tiny direct patch or patch-log work.
- v1 should not weaken the existing log-driven system. Instead, it adds two bounded escape hatches so mixed small fixes can be shipped without inventing fake slice names or polluting formal phase logs.
- The new model should stay operationally simple: one thin policy runbook defines when each lane is allowed, and one shared direct-patch ledger gives tiny no-log commits a deterministic place to be remembered.

**Default choices (phase defaults / v1)**:

- Keep the existing slice log system as the default lane for any work that has an independent contract, DoD, or replayable evidence surface.
- Introduce one new maintenance-log lane for grouped same-source cleanup, fallout repair, or mixed small fixes that are worth one bounded narrative but not worth several formal child slices.
- Introduce one direct-patch lane only for tiny local fixes that do not add a contract, do not need retained evidence, and do not widen system ownership; when a tiny patch still needs one short note, keep that note under `docs/logs/patch/` rather than in the main log root.
- Treat lane choice as a semantics decision, not a file-count decision: if a change has its own independent meaning, it should not hide inside a patch bundle.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Define a three-lane policy for standard slice work, maintenance sweep bundles, and direct patch commits.
- Add one thin operator-facing runbook so lane selection, naming, and escalation rules do not need to be reinvented during mixed cleanup work.
- Publish one shared direct-patch ledger and one minimal maintenance-log template so small work can remain traceable without forcing every fix into the full issue/log lifecycle.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

**PR links**:

- Log: `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

## Definitions (optional)

- `standard slice lane`: the current full log-driven path used when work owns a real contract, success criteria, and often a live issue/PR lifecycle.
- `maintenance sweep lane`: one bounded log used to group related small fixes discovered through the same replay, cleanup pass, or operator session.
- `direct patch lane`: a tiny patch path used only when the change is local, obvious, low-risk, and not worth a standalone narrative; the smallest version uses only the shared ledger, while the narrated version keeps one short patch note under `docs/logs/patch/`.

## Constraints

- Do not use the maintenance lane to hide contract changes, new automation surfaces, or multi-step behavioral work that deserves its own slice.
- Do not use the direct patch lane for anything that needs retained evidence, introduces a new boundary, or spans multiple unrelated problem areas.
- Do not let direct patch commits silently become the default workflow for mixed AI-generated cleanup; once the fix set needs a why/exclusion/validation paragraph, it should escalate to a maintenance log.
- Do not redefine the existing `S0F-1*` lineage. `S0F-2A` only adds bounded side lanes around it.

## Scope

- `P0`: create `S0F-2A`, wire it into the `S0F` spine, and define the lane boundary problem explicitly
- `P1`: define the three-lane decision model and escalation rules
- `P2`: standardize maintenance-log naming, patch-log location, and direct-patch commit boundaries
- `P3`: publish one thin runbook, one shared direct-patch ledger, and one minimal template under both `maintenance/` and `patch/`

## Success Criteria (DoD)

- One reader can determine in under a minute whether a change belongs in the standard slice lane, maintenance sweep lane, or direct patch lane.
- One stable home exists for future maintenance logs and patch logs so grouped cleanup does not need fake slice titles or ad hoc placement.
- One explicit direct-patch boundary exists so tiny fixes can land without pretending to be full slices.
- One shared ledger exists for direct patch commits, and one minimal template exists under both `docs/logs/maintenance/` and `docs/logs/patch/`.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the three-lane model is documented in one thin procedural surface;
  - the maintenance-log naming rule and direct-patch boundary are explicit;
  - one shared direct-patch ledger and one minimal maintenance template are published for immediate reuse.

## Current Status

- `S0F-2A` is now opened as the next `S0F` follow-up slice for institutionalizing how this repo handles small grouped fixes and tiny direct patches that do not fit naturally into the full slice lifecycle.
- `P0` is now complete: `S0F-2A` is wired into the spine, the problem is scoped as lane governance rather than as an ad hoc naming complaint, and the next step is explicit lane selection policy.
- `P1` is now complete: the repo now has one three-lane model that keeps full slice logs as the default path while adding bounded maintenance and direct-patch escapes.
- `P2` is now complete: future grouped cleanup now belongs under `docs/logs/maintenance/`, future patch notes now belong under `docs/logs/patch/`, and tiny no-log fixes still have explicit commit-boundary rules instead of being squeezed into fake slice titles.
- `P3` is now complete: the thin runbook/policy, shared direct-patch ledger, and concrete maintenance/patch templates are all published for immediate reuse.
- `S0F-2A` is now stable: the repo has a concrete, documented answer for work that is too small or too mixed for the standard slice lifecycle without allowing untracked patch drift.

## Plan (draft)

### P0 (Lane boundary and spine wiring)

- P0-C1-S1: create `S0F-2A` and wire it into the `S0F` parent spine as the next follow-up slice
- P0-C1-S2: define the problem as lane governance for mixed small fixes rather than as one-off naming friction

### P1 (Three-lane policy)

- P1-C1-S1: define the standard slice lane, maintenance sweep lane, and direct patch lane
- P1-C1-S2: define the escalation rule from direct patch to maintenance log to full slice

### P2 (Naming and commit boundary)

- P2-C1-S1: standardize future maintenance-log naming as `family-M<n>-<slug>`
- P2-C1-S2: standardize patch-log placement under `docs/logs/patch/` and direct-patch commit boundaries

### P3 (Published surfaces)

- P3-C1-S1: publish one thin runbook/policy for lane choice and escalation
- P3-C1-S2: publish one shared direct-patch ledger plus one minimal maintenance template and one minimal patch template

## Execution Checklist (unchecked)

### P0 (Lane boundary and spine wiring)

- [x] `P0-C1-S1`: `S0F-2A` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: lane-governance boundary fixed

### P1 (Three-lane policy)

- [x] `P1-C1-S1`: standard slice, maintenance sweep, and direct patch lanes defined
- [x] `P1-C1-S2`: lane escalation rule defined

### P2 (Naming and commit boundary)

- [x] `P2-C1-S1`: future maintenance-log naming standardized
- [x] `P2-C1-S2`: patch-log placement and direct-patch boundary standardized

### P3 (Published surfaces)

- [x] `P3-C1-S1`: thin lane-policy runbook published
- [x] `P3-C1-S2`: shared direct-patch ledger plus maintenance/patch templates published

## Evidence

- `docs/runbook/run-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md` now defines the three-lane model, folder placement rules, escalation rules, maintenance-log naming rule, and direct-patch boundary in one operator-facing procedural surface.
- `docs/logs/ledger-direct-patch-commits.md` now exists as the shared repository ledger for tiny no-log patch commits.
- `docs/logs/maintenance/_template-log-maintenance-sweep.md` and `docs/logs/patch/_template-log-patch-note.md` now publish concrete templates at the canonical homes for maintenance and patch notes.
- `docs/logs/log-S0F-docs-management-v6.md` now points to `S0F-2A` as the next institutional follow-up under the `S0F` spine.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-2A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
