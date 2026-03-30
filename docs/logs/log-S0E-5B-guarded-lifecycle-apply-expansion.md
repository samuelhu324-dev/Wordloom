# log-S0E-5B (Phase 5B: Guarded Lifecycle Apply Expansion)

---

**id**: `S0E-5B`
**kind**: `log`
**title**: `guarded lifecycle apply expansion v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Issues, PR, Automation, Drills, Evidence, epic/s0, sub/0e5b`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/307`
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_1**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  **reference_log_4**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-30`
**updated**: `2026-03-30`

---

## Decision / Outcome

**Decision**:

- `S0E-5B` exists as the follow-up after `S0E-5A`, focused on expanding guarded pre-gate behavior from one issue-conclusion mutation path to a broader set of real lifecycle apply operations.
- The next step is not another dry-run-only gate. It is a controlled apply expansion that keeps `S0E-5A` audit artifacts as the single precondition layer while widening the set of mutations that must honor that gate.
- The operator-facing goal is one consistent rule: if the lifecycle pre-gate does not allow apply, the tool must stop before mutating issue relationships, PR creation state, or later close-out steps.

**Default choices (phase defaults / v1)**:

- `S0E-5B` should start from the already-validated `S0E-5A` contracts and avoid redefining audit severity or remediation semantics.
- Expansion should proceed one mutation family at a time, with real GitHub validation after each new guarded path rather than a large one-shot orchestration jump.
- Relationship attach and PR-side lifecycle mutations are the first expected guarded apply candidates because `S0E-5A` only proved the issue-conclusion path directly.
- The generic lifecycle pre-gate decision remains the source of truth, but a guarded mutation family may define one narrow continuation rule when the emitted remediation plan contains exactly the mutation family that the command is designed to apply.

## Constraints

- Do not weaken the fail-closed pre-gate policy introduced in `S0E-5A`.
- Do not bypass the explicit remediation-planning output when `warning` or `blocked` findings remain.
- Do not merge multiple new guarded mutation families into one undifferentiated implementation step; each path should leave isolated evidence.

## Scope

- `P0`: define the expansion boundary from guarded issue-conclusion apply to broader guarded lifecycle apply
- `P1`: add one guarded relationship-attach path behind the same pre-gate
- `P2`: evaluate whether PR creation or PR-body mutation should become the next guarded apply family
- `P3`: validate one representative real closed-loop sample that uses more than one guarded mutation family under the same gate policy

## Success Criteria (DoD)

- `S0E-5A` remains the source of truth for audit and decision semantics, while `S0E-5B` only expands guarded apply coverage.
- At least one new mutation family beyond issue conclusion is wired behind the same pre-gate and validated on live GitHub state.
- Evidence clearly shows where apply was allowed, where it stopped, and which remediation artifacts were emitted for blocked paths.

## Current Status

- `S0E-5A` has finished one full real lifecycle on itself: issue `#305`, merged PR `#306`, sidebar relationship attach, and final issue conclusion are all complete.
- `P0` is now fixed: relationship attach is the first mutation family that may continue from a `stop-for-remediation` gate decision, but only when the remediation output contains planned `attach-parent-relationship` steps and nothing outside that family.
- `P1` is now implemented and validated: live issue `#307` was created for `S0E-5B`, the guarded relationship path attached it to parent issue `#248`, and the same command shape stopped on a frozen mixed-remediation sample without applying anything.
- The next remaining gap is now strictly `P2`: deciding which PR-side mutation family should be guarded next behind the same pre-gate.

## P0 (Expansion boundary | v1)

### P0-C1-S1 (Targeted remediation continuation rule | v1)

- `S0E-5A` keeps ownership of the generic lifecycle audit, decision, and remediation-planning semantics.
- `S0E-5B` introduces one mutation-family-specific rule: a guarded relationship-attach command may continue even when the generic gate decision is `stop-for-remediation`, but only if the remediation plan says the requested item is fixable exclusively through planned `attach-parent-relationship` steps.
- If lifecycle remediation includes any other planned action kinds, any manual follow-up, or any ambiguous/multiple downstream relationship manifests, the guarded relationship command must stop before apply.

## P1 (Guarded relationship attach | v1)

### P1-C1-S1 (Guarded apply entrypoint implemented | v1)

- `apply_issue_relationships_with_pre_gate.py` now runs the same lifecycle pre-gate used by guarded issue conclusion, then inspects the remediation output before deciding whether relationship apply is eligible.
- The guarded relationship path derives its relationship manifest from lifecycle remediation output by default instead of requiring the operator to manually splice together a second input.
- The command wrapper now enforces a bounded timeout for `gh` subprocess calls so a stalled GitHub CLI call fails closed instead of hanging indefinitely.

### P1-C1-S2 (Live pass and frozen stop validation | v1)

- The live pass sample uses real issue `#307`, where the generic lifecycle gate returns `stop-for-remediation` because the sidebar parent relationship is still missing, yet the guarded command is allowed to continue because the only planned remediation is `attach-parent-relationship`.
- The guarded pass sample converges by attaching `#307` under parent issue `#248` and recording `applied-after-pre-gate` in the guarded result artifact.
- The frozen stop sample reuses the archived `S0E-5A` fixture audit plan; because that remediation set mixes relationship repair with issue-conclusion refresh, the guarded relationship command stops before apply with `blocked-mixed-remediation`.

## Plan (draft)

- `P0-C1-S1`: fix the exact mutation families that are in-scope for the first guarded apply expansion
- `P1-C1-S1`: connect the lifecycle pre-gate to one relationship-attach apply path
- `P1-C1-S2`: validate one live pass sample and one stop-before-apply sample for the guarded relationship path
- `P2-C1-S1`: decide whether PR creation, PR body rewrite, or another mutation family is the next guarded target

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: expansion boundary fixed
- [x] `P1-C1-S1`: guarded relationship-attach path implemented
- [x] `P1-C1-S2`: pass and stop validation recorded
- [ ] `P2-C1-S1`: next guarded mutation family selected

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the live issue anchor, gate outputs, guarded apply results, and frozen stop evidence for the first guarded relationship path.

### P0-C1-S1 (targeted relationship remediation continuation rule fixed | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `scripts/issues/apply_issue_relationships_with_pre_gate.py`
  - `scripts/issues/gen_issue_draft.py`
  - `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
- expected:
  - relationship attach should be the first guarded mutation family that may continue from `stop-for-remediation` without weakening the generic pre-gate
  - the guarded path should stop when remediation includes any non-relationship action family or manual follow-up
- observed:
  - the new guarded relationship entrypoint now allows apply only when lifecycle remediation is exclusively planned `attach-parent-relationship`, and otherwise fails closed before mutation

### P1-C1-S1S2 (guarded relationship path exercised on live pass and frozen stop samples | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/issue-S0E-5B-guarded-lifecycle-apply-expansion.md`
  - `docs/issues/issue-S0E-5B-guarded-lifecycle-apply-expansion.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p1-pass-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p1-pass-plan.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p1-pass-decision.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-pass-plan.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-pass-relationship-manifest.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-pass-plan.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-pass-parent-248-child-307-apply-result.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p1-stop-decision.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-stop-plan.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-stop-relationship-manifest.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-stop-issue-conclusion-manifest.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-stop-guarded-apply-result.json`
- expected:
  - the live pass sample should continue from `stop-for-remediation` only because relationship attach is the sole planned remediation family
  - the frozen stop sample should refuse to apply because mixed remediation would exceed the guarded relationship command boundary
- observed:
  - live issue `#307` was created and then attached to parent issue `#248` through the guarded relationship path, with `guarded_eligibility = allowed-via-targeted-relationship-remediation`
  - the archived fixture sample stopped before apply with `guarded_eligibility = blocked-mixed-remediation` because the remediation output also contained `plan-issue-conclusion-refresh`

## Recent changes (for traceability, optional)

- 2026-03-30: created `S0E-5B` as the follow-up slice for expanding guarded pre-gate enforcement beyond the issue-conclusion mutation path validated in `S0E-5A`.
- 2026-03-30: created live issue `#307` for `S0E-5B` and wrote the exact GitHub issue link back to this source log.
- 2026-03-30: completed `P0` by fixing the targeted-remediation continuation rule for guarded relationship attach instead of reusing the generic `allow-apply` rule unchanged.
- 2026-03-30: completed `P1` by implementing `apply_issue_relationships_with_pre_gate.py`, attaching `#307` to parent issue `#248` through the guarded pass path, and validating a frozen mixed-remediation stop drill.