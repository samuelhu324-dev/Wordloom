# log-S0F-2B (Phase 2B: family patch and ops maintenance model)

---

**id**: `S0F-2B`
**kind**: `log`
**title**: `family patch and ops maintenance model v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Maintenance, Contract, epic/s0, sub/2b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0F-2B-family-patch-and-ops-maintenance-model.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
  **reference_log_1**: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
  **reference_log_2**: `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
  **reference_log_3**: `docs/logs/maintenance/_template-log-maintenance-sweep.md`
  **reference_log_4**: `docs/logs/patch/_template-log-patch-note.md`
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

- `S0F-2B` refines the earlier small-work policy into three sharper lanes: `family patch`, `ops maintenance`, and `tiny direct patch`.
- v1 explicitly stops calling same-source family repair bundles `maintenance`. If the work is a patch that belongs to a family such as `S0F`, it should stay family-owned under `P<n>` patch IDs and live under `docs/logs/patch/`.
- Real maintenance is reserved for recurring or operator-triggered runtime/governance care work that is strongly bound to runbooks, CI/CD, GitHub Actions, environments, evidence bundles, and reportable precheck/postcheck structure.
- The live GitHub top-level label `MAINTENANCE` already exists, but it should not become a generic misc label. v1 reserves it only for true ops-maintenance issues that satisfy explicit admission rules.

**Default choices (phase defaults / v1)**:

- Keep the standard slice lane as the default when work has an independent contract, DoD, replay path, or later full-auto lifecycle value.
- Use `family patch` when the fix is still owned by one family or slice lineage and would be clearer as `S0F-P1-<slug>`, `S4D-P2-<slug>`, or a similar family-bound patch note.
- Use `ops maintenance` only when the work is periodic, operator-facing, buttonable, environment-scoped, and naturally report-oriented.
- Keep `tiny direct patch` as the smallest lane for truly local, obvious, no-log fixes; this lane still requires one ledger row and should never become the default bucket for AI fallout cleanup.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Refine the earlier small-work policy into family patch, ops maintenance, and tiny direct patch.
- Upgrade the maintenance template into a heavier ops-maintenance template with trigger, environment, entrypoint, precheck, postcheck, findings, evidence, and report summary sections.
- Decide and document that GitHub `MAINTENANCE` is a reserved top-level label for true ops-maintenance work, not for ordinary family patches.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

## Constraints

- Do not let `MAINTENANCE` become a misc bucket for ordinary repair work or family-local fallout cleanup.
- Do not hide family-owned patches inside maintenance just because they were discovered during a replay.
- Do not treat CI/CD, GitHub Actions, or runbook-bound recurring care work as if it were a tiny patch lane.
- Do not remove the tiny direct-patch path; only narrow it.

## Scope

- `P0`: create `S0F-2B`, wire it into the `S0F` spine, and define the refinement boundary against `S0F-2A`
- `P1`: refactor the lane model into family patch, ops maintenance, and tiny direct patch
- `P2`: upgrade templates and folder guidance to match the refined model
- `P3`: decide the GitHub `MAINTENANCE` label admission rule and document when it should remain unused
- `P4`: publish the first real ops-maintenance sample so the heavier maintenance template is no longer only a blank form

## Success Criteria (DoD)

- One reader can distinguish family patch from ops maintenance without relying on file count or subjective size language.
- The maintenance template is heavy enough to capture real operator maintenance work with trigger, environment, action, result, evidence, and follow-up.
- The patch template supports family-bound patch IDs such as `S0F-P1-<slug>`.
- The GitHub `MAINTENANCE` label has an explicit admission rule and is no longer an ambiguous missing-or-misc concept.
- The repo contains at least one real ops-maintenance sample log grounded in live workflow and runner evidence, not just a blank maintenance template.

## Current Status

- `S0F-2B` is now opened as the next `S0F` follow-up slice for refining the earlier small-work policy into a sharper family-patch versus ops-maintenance model.
- `P0` is now complete: `S0F-2B` is wired into the spine, and `S0F-2A` is now treated as the earlier baseline rather than the final policy wording.
- `P1` is now complete: the lane model now distinguishes `family patch`, `ops maintenance`, and `tiny direct patch` instead of grouping family-local patch work under generic maintenance.
- `P2` is now complete: the patch template now supports family patch IDs, and the maintenance template is now a heavy ops-maintenance template with report-oriented sections.
- `P3` is now complete: GitHub `MAINTENANCE` is now documented as an already-existing but reserved top-level label for true ops-maintenance work only; ordinary family patches should not use it.
- `P4` is now complete: `docs/logs/maintenance/log-S0F-M1-github-actions-runner-and-dispatch-health-check.md` now publishes the first real ops-maintenance sample using live workflow and runner evidence instead of placeholder text only.
- `S0F-2B` is now stable: the repo now has a more realistic operating model for patch versus maintenance work, and the templates now match that boundary.

## Plan (draft)

### P0 (Refinement boundary and spine wiring)

- P0-C1-S1: create `S0F-2B` and wire it into the `S0F` parent spine as the next follow-up slice
- P0-C1-S2: define `S0F-2B` as the refinement pass over the earlier `S0F-2A` baseline

### P1 (Lane model refinement)

- P1-C1-S1: define `family patch` as the family-owned patch lane
- P1-C1-S2: define `ops maintenance` as the heavier recurring/operator maintenance lane
- P1-C1-S3: keep and narrow `tiny direct patch` as the truly no-log path

### P2 (Template and folder alignment)

- P2-C1-S1: upgrade the patch template to family-patch IDs and origin-family wording
- P2-C1-S2: upgrade the maintenance template to a heavier ops-maintenance report shape

### P3 (GitHub label admission rule)

- P3-C1-S1: decide whether and when the live GitHub `MAINTENANCE` top-level label should be used

### P4 (Real ops-maintenance sample)

- P4-C1-S1: publish the first real ops-maintenance sample log for GitHub Actions runner and workflow-dispatch health

## Execution Checklist (unchecked)

### P0 (Refinement boundary and spine wiring)

- [x] `P0-C1-S1`: `S0F-2B` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: refinement boundary against `S0F-2A` fixed

### P1 (Lane model refinement)

- [x] `P1-C1-S1`: family patch lane defined
- [x] `P1-C1-S2`: ops maintenance lane defined
- [x] `P1-C1-S3`: tiny direct patch lane narrowed and retained

### P2 (Template and folder alignment)

- [x] `P2-C1-S1`: patch template upgraded to family-patch form
- [x] `P2-C1-S2`: maintenance template upgraded to ops-maintenance form

### P3 (GitHub label admission rule)

- [x] `P3-C1-S1`: `MAINTENANCE` label admission rule documented

### P4 (Real ops-maintenance sample)

- [x] `P4-C1-S1`: first real ops-maintenance sample published

## Evidence

- `docs/runbook/run-S0F-2B-family-patch-and-ops-maintenance-model.md` now defines the refined family-patch versus ops-maintenance model and the `MAINTENANCE` label admission rule.
- `docs/logs/patch/_template-log-patch-note.md` now supports family-bound patch IDs such as `S0F-P1-<slug>`.
- `docs/logs/maintenance/_template-log-maintenance-sweep.md` now captures heavy ops-maintenance reporting fields instead of lightweight grouped-cleanup prose only.
- Live GitHub label inventory for `samuelhu324-dev/wordloom-v3` now confirms that `MAINTENANCE` already exists, so the real missing piece was admission policy rather than label creation.
- `docs/logs/maintenance/log-S0F-M1-github-actions-runner-and-dispatch-health-check.md` now provides the first real ops-maintenance sample, showing both healthy comparison evidence and current findings on workflow-run degradation and runner inventory state.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-2B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle.
