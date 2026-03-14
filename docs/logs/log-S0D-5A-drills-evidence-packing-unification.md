# log-S0D-5A (Phase 5: Drills Evidence Packing Unification)

---

**id**: `S0D-5A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `drills evidence packing unification and optimization v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Tooling, Drills, Evidence, Automation, Artifacts, Packing, epic/s0, sub/5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0D-1A-log-entries-orchestration.md`
  **previous_log**: `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
  **reference_log_1**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  **reference_log_2**: `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
  **reference_log_3**: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
  **reference_log_4**: `.github/workflows/reusable-labs-scenario-runner.yml`
  **reference_log_5**: `.github/workflows/drill-failures.yml`
**created**: `2026-03-14`
**updated**: `2026-03-14`

---

## Decision / Outcome

**Decision**:

- Unify reusable drills evidence packing around one simple rule: single-scenario success uploads only the minimal result summary, while failures still upload a large evidence bundle.
- Keep `drill-failures` matrix mode (`scenario_id=fault/obs_infra/all`) as the explicit escape hatch for broader per-run evidence bundles, instead of making every single-scenario dispatch carry unrelated snapshot directories.

**Default choices (phase defaults / v1)** (optional, but recommended):

- Success-first artifact contract for single-scenario workflows: upload `summary.json` only.
- Failure-first artifact contract for single-scenario workflows: upload one zipped evidence bundle rooted at the current run evidence, not the whole shared snapshot tree unless the run directory cannot be resolved.
- Reuse the existing `workflow_artifacts.py` helper and artifact-safe scenario naming rather than introducing another workflow-local packing script.

## Definitions (optional)

- **minimal evidence mode**: upload only `artifacts/summary.json` on success, and `artifacts.zip` on failure.
- **full evidence mode**: upload the full run evidence directory for the current run.
- **single-scenario dispatch**: a workflow invocation where one scenario id maps to one runner job.
- **matrix-all dispatch**: a workflow invocation where `fault/obs_infra/all` expands into multiple scenario jobs.

## Constraints

- Do not mix unrelated scenario directories into a single-scenario success artifact.
- Preserve failure forensics: a failed run must still leave a downloadable evidence bundle.
- Reuse the repo-wide workflow artifact helper where practical instead of re-implementing packaging logic inline in YAML.
- Keep artifact names stable and artifact-safe for catalog ids containing `/`.

## Scope

- `P0`: contract (packing modes, naming, success/failure artifact rules)
- `P1`: implementation / helper updates in reusable workflow code
- `P2`: drill / verify adoption for `drill-failures` and other reusable-labs callers
- `P3`: follow-up cleanup / broader convergence across older workflows

## Success Criteria (DoD)

- Single-scenario `drill-failures` runs no longer upload unrelated scenario directories on success.
- Success artifacts for minimal mode contain only the result summary.
- Failure artifacts for minimal mode still provide one downloadable evidence bundle for triage.
- `fault/obs_infra/all` remains available as the broad-evidence path when operators intentionally want the larger bundle behavior.
- The packing behavior is expressed as reusable workflow contract, not as ad hoc per-workflow shell logic.

## Stability (what stable means)

- This log can move to `stable` when the reusable packing contract is implemented, adopted by the main reusable labs runner, and validated on at least one single-scenario drill plus one matrix-style drill path.

## P0 (Contract | v1)

### P0-C1-S1 (Packing modes)

- `minimal`: upload `summary.json` on success and `artifacts.zip` on failure.
- `full`: upload the full evidence directory for the current run.
- Workflow callers should choose the mode explicitly when broad evidence is still desired; otherwise the reusable runner should default to the minimal operator-friendly contract.

### P0-C1-S2 (Artifact scope boundary)

- A single-scenario artifact must describe one run only.
- `fault/obs_infra/all` is the only intended path where operators should expect many scenario jobs from one dispatch.
- Even in `full` mode, the artifact boundary should be the current run evidence, not the entire shared snapshot root when the run directory is known.

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - scenario id / run id context
  - current run result path or copied summary path
  - PASS/FAIL decision fields from `_result.json`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- For logs tied to a specific scope/index (for example, `S5B-3A` belongs to `S5B`, and `S0D-2A` belongs to `S0D`), prefer making P* code and documentation changes on a working branch with the same prefix.
- `S0D-5A` style packaging and workflow-governance changes should normally land on an `S0D-*` branch.

**Commit discipline (recommended)**:

- Record packing-contract changes and workflow adoption changes in separate `P*-C*-S*` commits when practical so later evidence work can point to a narrow landing change.

## Plan (draft)

### P1 (Implementation)

- P1-C1-S1: extend `workflow_artifacts.py` with a helper for summary-only packing from `_result.json`
- P1-C1-S2: add `minimal/full` evidence upload modes to `reusable-labs-scenario-runner.yml`

### P2 (Drill / Verify)

- P2-C1-S1: adopt the new packing contract in `drill-failures.yml`, with single-scenario dispatches using minimal mode
- P2-C1-S2: let other callers of `reusable-labs-scenario-runner.yml` inherit the new default without reopening each workflow contract

### P3 (Cleanup / Convergence)

- P3-C1-S1: audit older workflow docs and examples that still describe root-level snapshot uploads instead of run-scoped packing

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: packing modes defined
- [x] `P0-C1-S2`: artifact scope boundary defined
- [x] `P0-C1-S3`: evidence contract defined

### P1 (Implementation)

- [x] `P1-C1-S1`: summary-only packing helper added
- [x] `P1-C1-S2`: reusable labs runner upload modes added

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: `drill-failures` adopts minimal mode for non-`all` dispatches
- [x] `P2-C1-S2`: reusable labs callers inherit the new default contract

### P3 (Cleanup / Convergence)

- [x] `P3-C1-S1`: older docs/examples audited against the new packing contract

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P1-C1-S1S2 / P2-C1-S1S2 (Reusable labs packing convergence | 2026-03-14)

- headSha: `ce6b99498de4b66daf14bb053deeec6de01cdd9d` (validated on `main`; contract originally landed via `ffcb622086debc38c111e435f94f2baea8d3b515`)
- ci_run_url: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23088974971`
- dispatch:
  - workflow: `drill-failures`
  - scenario_id: `fault/obs_infra/es_429_inject`
  - job: `drills (fault/obs_infra/es_429_inject)`
- artifacts:
  - `.github/workflows/reusable-labs-scenario-runner.yml`
  - `.github/workflows/drill-failures.yml`
  - `backend/scripts/ci/workflow_artifacts.py`
  - `docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
- expected:
  - single-scenario drill dispatches upload only `summary.json` on success
  - failures still upload one large evidence bundle
  - `fault/obs_infra/all` remains the explicit broad-evidence path
- observed:
  - GitHub Actions page reports `Status=Success`, `1 job completed`, `Artifacts=1`, total duration `5m 28s`
  - the only produced artifact is `labs-evidence-fault_obs_infra_es_429_inject-23088974971-1-fault_obs_infra_es_429_inject` with size `1.04 KB`
  - the tiny single artifact size is consistent with the minimal success contract (`summary.json` only), not a bundled multi-directory snapshot upload

### P3-C1-S1 (Legacy docs/examples audit | 2026-03-14)

- headSha: `ffcb622086debc38c111e435f94f2baea8d3b515`
- artifacts:
  - `docs/runbook/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
- expected:
  - operator-facing docs stop implying that single-scenario success always uploads the whole `docs/labs/_snapshot/auto/` root
  - historical logs preserve the original fact pattern but label it as a legacy full-bundle baseline
- observed:
  - the operator runbook now documents minimal-success / failure-bundle behavior as the default reusable labs contract
  - older historical references that mentioned root-level uploads are retained only as explicit historical baseline notes

## Recent changes (for traceability, optional)

- 2026-03-14: scaffolded `S0D-5A` to unify and optimize drills evidence packing, with `drill-failures` included in the same `P*-C*-S*` contract.
- 2026-03-14: recorded first successful single-scenario CI validation for the minimal packing contract and completed the initial legacy-doc wording audit.