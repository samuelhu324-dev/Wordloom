# log-S0E-7B (Phase 7B: attribution handoff implementation and automatic mirroring integration)

---

**id**: `S0E-7B`
**kind**: `log`
**title**: `workflow/attribution handoff implementation and automatic mirroring integration v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Actions, Automation, Workflow, PR, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  **reference_log_1**: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  **reference_log_3**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **reference_log_4**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
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
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-01`
**updated**: `2026-04-01`

---

## Decision / Outcome

**Decision**:

- `S0E-7B` is now the implementation follow-up after `S0E-4E/P3`: it owns how the attribution result payload is actually produced and then consumed by `S0E-7A` in a future automatic PR-event path.
- `S0E-4E` remains the contract owner for attribution semantics, stop taxonomy, and handoff payload shape.
- `S0E-7B` owns implementation only: planner/result JSON emission, workflow-side consume-or-stop wiring, and end-to-end validation that distinguishes `attribution stop` from later `mirror verification drift`.

**Default choices (phase defaults / v1)**:

- The first implementation should stay as narrow as the current `S0E-7A` workflow contract: produce one attribution result payload, then either continue into the existing mirror verifier or stop before verification begins.
- The implementation should reuse existing field names already common in repo JSON outputs where practical, especially `source_log_path`, `pr_ref`, `pr_url`, and repo-relative artifact paths.
- Automatic rollout should stay fail-closed until the implementation proves both a resolved handoff sample and an attribution-stop sample with retained evidence.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Implement the attribution result payload defined by `S0E-4E/P3`.
- Wire `S0E-7A` to consume that payload and stop before verifier execution when attribution does not resolve.
- Validate one resolved handoff sample and one attribution-stop sample with retained evidence that distinguishes attribution stop from later verifier drift.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0` is reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
- `P1-C1-S1S2` | artifact: `scripts/issues/resolve_pr_source_log_attribution.py`

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` and `Development Link` as separate sections.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Definitions (optional)

- `attribution result payload`: the machine-readable JSON result that says whether source-log attribution resolved cleanly or stopped before verification.
- `consume-or-stop`: the workflow boundary where `S0E-7A` either consumes a resolved attribution payload and proceeds, or stops before verifier execution.
- `attribution stop`: a stop outcome caused by missing/conflicting/multi-candidate/invalid-shape ownership, distinct from later verifier failure.

## Constraints

- Do not re-argue attribution semantics here; `S0E-4E` already owns the contract.
- Do not collapse attribution-stop and verifier-failure into one undifferentiated workflow outcome.
- Do not widen directly to broad `pull_request` coverage before the narrow implementation path proves it can preserve attribution evidence cleanly.

## Scope

- `P0`: fix the implementation ownership boundary between `S0E-4E` contract and `S0E-7B` execution wiring
- `P1`: implement the attribution planner/result JSON entrypoint
- `P2`: wire `S0E-7A` to consume the attribution result and stop or continue deterministically
- `P3`: validate one resolved handoff sample and one attribution-stop sample with retained evidence

## Success Criteria (DoD)

- The repo has one implementation slice that owns emission of the attribution result payload without moving the ownership contract back out of `S0E-4E`.
- `S0E-7A` can later consume a resolved attribution payload without needing an extra operator-supplied `source_log_path` in automatic mode.
- A stop sample can halt before verifier execution while preserving retained evidence that clearly says the run stopped in attribution rather than failed in mirror verification.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the implementation boundary, attribution result entrypoint, consume-or-stop wiring, and representative handoff samples
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-7B` is now opened as the implementation follow-up after `S0E-4E` finished the attribution contract.
- `P0` is now completed: implementation ownership is now explicitly separated from `S0E-4E` contract ownership.
- `P1` is now completed: the repo now has one attribution resolver entrypoint that emits the `S0E-4E/P3` handoff payload and one normalized PR payload snapshot that future `S0E-7A` workflow wiring can consume directly.
- `P2-P3` remain open: workflow consume-or-stop wiring and resolved/stop evidence samples are not yet implemented.

## P0 (Implementation boundary | v1)

### P0-C1-S1 (Implementation ownership boundary fixed | v1)

- `S0E-4E` already fixed what attribution means, which surfaces are allowed, which ambiguity classes must stop, and what payload shape `S0E-7A` may consume.
- `S0E-7B` now fixes the next boundary directly:
  - `S0E-4E` owns attribution contract semantics;
  - `S0E-7B` owns the code path that emits the attribution result JSON and wires it into the GitHub Actions path;
  - `S0E-7A` continues to own mirror verification, retained artifacts, and failure surfacing once attribution has already resolved.
- This prevents the next implementation pass from leaking back into contract churn: future work should implement the payload and workflow behavior, not reopen the attribution rules themselves.

## P1 (Attribution result entrypoint | v1)

### P1-C1-S1 (Attribution result JSON entrypoint implemented | v1)

- `scripts/issues/resolve_pr_source_log_attribution.py` now owns the first implementation entrypoint for `PR event -> source_log_path` attribution.
- The entrypoint resolves attribution only from the allowed `S0E-4E/P1` surfaces:
  - trusted explicit provenance supplied as `--trusted-source-log-path` or through a structured PR payload file;
  - the canonical PR-body `Links` row `Log: <repo-relative-path>`;
  - exact-ID head-branch fallback that resolves one exact log ID from the PR head ref.
- The script emits the `S0E-4E/P3` consume-or-stop payload directly, including:
  - `mode`, `result`, `repository`, `pr_ref`, `pr_url`, `source_log_path`, `winning_surface`, `consulted_surfaces`, `stop_reason`, and `eligible_for_secondary_enforcement`;
  - fail-closed stop results for `missing-attribution`, `conflicting-attribution`, `multi-candidate-attribution`, and `invalid-attribution-shape`.
- The implementation stays intentionally narrow:
  - it fetches a live PR via `gh pr view` or accepts a local PR payload JSON for offline replay;
  - it does not wire GitHub Actions behavior yet;
  - it does not reopen attribution semantics that already belong to `S0E-4E`.

### P1-C1-S2 (Retained attribution artifact paths fixed | v1)

- `P1` now fixes the first retained artifact pair for attribution output:
  - one normalized PR payload snapshot JSON;
  - one attribution result JSON.
- The resolver now writes repo-relative paths for both artifacts so later workflow wiring can pass them forward without introducing a second path convention:
  - default local result path: `docs/issues/pr-source-log-attribution-<pr-ref>-result.json`;
  - default local payload snapshot path: `docs/issues/pr-source-log-attribution-<pr-ref>-pr-payload.json`;
  - future workflow runs may override both paths into workflow artifact directories while keeping the same payload fields and repo-relative path reporting.
- This fixes the `P1` artifact boundary directly: later `S0E-7A` wiring can consume the emitted `source_log_path` when resolved, while attribution evidence remains independently inspectable when the resolver stops before verification.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-7B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0E-7B/P0-P3: attribution handoff implementation and automatic mirroring integration`
  - discontinuous phases: `S0E-7B/P0+P3: attribution handoff implementation and automatic mirroring integration`
  - mixed discontinuous + consecutive phases: `S0E-7B/P0+P3-P4: attribution handoff implementation and automatic mirroring integration`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `S0E-7B/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- `S0E-7B` changes should usually stay on the existing `S0E-*` working branch because this slice is still part of the docs-management / GitHub automation spine.

## Plan (draft)

### P1 (Attribution result entrypoint)

- [x] `P1-C1-S1`: implement the attribution planner/result JSON entrypoint with the `S0E-4E/P3` payload shape
- [x] `P1-C1-S2`: define retained artifact paths for attribution output in a way that `S0E-7A` can consume directly

### P2 (Workflow consume-or-stop wiring)

- `P2-C1-S1`: wire the GitHub Actions path so resolved attribution continues into mirror verification
- `P2-C1-S2`: wire stop outcomes so attribution halts before verifier execution and retains independent stop evidence

### P3 (Representative end-to-end samples)

- `P3-C1-S1`: validate one resolved handoff sample
- `P3-C1-S2`: validate one attribution-stop sample distinct from later verifier drift

## Execution Checklist (unchecked)

### P0 (Implementation boundary)

- [x] `P0-C1-S1`: implementation ownership boundary fixed

### P1 (Attribution result entrypoint)

- [x] `P1-C1-S1`: implement attribution result JSON entrypoint
- [x] `P1-C1-S2`: define retained attribution artifact paths

### P2 (Workflow consume-or-stop wiring)

- [ ] `P2-C1-S1`: wire resolved attribution into mirror verification
- [ ] `P2-C1-S2`: wire attribution-stop before verifier execution

### P3 (Representative end-to-end samples)

- [ ] `P3-C1-S1`: validate resolved handoff sample
- [ ] `P3-C1-S2`: validate attribution-stop sample

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1 (implementation ownership boundary fixed | 2026-04-01)

- headSha: `d31fd453`
- artifacts:
  - `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
- expected:
  - the repo should open one follow-up slice that owns implementation of the attribution payload and the GitHub-side consume-or-stop wiring without reopening `S0E-4E` contract decisions
- observed:
  - `S0E-7B` now fixes that split directly: contract ownership remains in `S0E-4E`, while implementation and integration work is explicitly deferred into this new GitHub-side follow-up

### P1-C1-S1S2 (attribution result entrypoint and artifact paths fixed | 2026-04-01)

- headSha: `d31fd453`
- artifacts:
  - `scripts/issues/resolve_pr_source_log_attribution.py`
  - `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
- expected:
  - the repo should gain one implementation entrypoint that emits the exact `4E -> 7A` attribution handoff payload and one stable retained-artifact pair that later workflow wiring can consume without inventing a second path convention
- observed:
  - the new resolver now emits `resolved` or fail-closed stop payloads from the allowed attribution surfaces only, writes a normalized PR payload snapshot beside the result JSON by default, and reports both artifact paths in repo-relative form

## Recent changes (for traceability, optional)

- 2026-04-01: opened `S0E-7B` as the implementation follow-up for attribution payload emission and automatic mirroring integration after `S0E-4E` completed the handoff contract.
- 2026-04-01: completed `P0` by fixing the ownership split between attribution contract (`S0E-4E`) and attribution implementation / workflow wiring (`S0E-7B`).
- 2026-04-01: completed `P1` by adding `scripts/issues/resolve_pr_source_log_attribution.py`, which emits the `4E -> 7A` handoff payload plus a normalized PR payload snapshot using stable repo-relative artifact paths.