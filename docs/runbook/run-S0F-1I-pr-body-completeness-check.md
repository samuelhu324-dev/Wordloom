# Run-S0F-1I: standard PR body completeness check

---

**id**: `S0F-1I-pr-body-completeness-check`
**kind**: `runbook`
**title**: `run/S0F-1I-pr-body-completeness-check`
**status**: `stable`
**scope**: `S0F-1I`
**decision_date**: `2026-04-05`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `Standardize one repeatable local read-only check path for PR body completeness that delegates to the canonical reviewer and retains an operator-facing evidence bundle.`
  **positive**: `"Primary local check boundary", "Single-sourced reviewer semantics", "Retained pass or stop artifacts under one operator-facing root"`
  **negative**: `"Extra wrapper artifacts per run", "Need to preserve wrapper and reviewer output shapes together", "Operators still need source-log ownership to be converged first"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Provide one operator-facing path for running the stable PR body completeness check after `S0F-1I` convergence.
- Keep the workflow read-only and single-sourced:
  - the standard wrapper owns pass or stop semantics
  - the canonical reviewer still owns exact-match, formatting-only, substantive, stop, and skip classification
  - one retained artifact bundle proves what the check saw on that run

## 2) Scope

- Covered:
  - local operator invocation of the standard PR body completeness check
  - retained result, summary, manifest, and fetched review files under one operator-facing artifact root
  - stable pass or stop semantics derived from the canonical reviewer without introducing a second classifier
- Out of scope:
  - live PR body mutation or formatting-only convergence itself
  - CI wiring or task wiring beyond the current local entrypoint
  - source-log ownership repair for missing `links.pr` or live PR lifecycle creation for in-progress slices
- Source materials:
  - `docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md`
  - `docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `scripts/issues/review_pr_body_completeness.py`
  - `scripts/issues/plan_pr_body_completeness_check_wrapper.py`
  - `scripts/issues/invoke_pr_body_completeness_check.ps1`

## 3) Evidence Bundle

### 3.1 Output roots

- Operator-facing root:
  - `artifacts/operator-facing/pr-body-completeness-check/<run-id>-<slug>/`
- Minimum evidence files:
  - `wrapper-result.json`
  - `workflow-summary.md`
  - `artifact-manifest.json`
  - `review-result.json`
  - `review-files/`

### 3.2 Summary or ledger

- There is no append-only ledger for this workflow.
- Operators should inspect:
  - `wrapper-result.json` for pass or stop outcome
  - `workflow-summary.md` for the human-readable run summary
  - `review-result.json` for exact reviewer classification details

## 4) One-click Automation

### 4.1 What it does

- Runs the canonical PR body completeness reviewer for one or more requested-ID prefixes.
- Publishes one operator-facing artifact bundle under `artifacts/operator-facing/pr-body-completeness-check/`.
- Converts reviewer output into one standard local check result:
  - `pass` when there is no substantive drift and no stop-state ownership gap
  - `stop` when substantive drift or stop-state ownership gaps exist
  - `error` when wrapper inputs are invalid or the retained reviewer result cannot be produced
- Preserves `skip-no-live-pr-owned` as a bounded non-failing state for slices that do not yet own a live issue or PR.

### 4.2 Operator instructions

- Stable entrypoint:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/issues/invoke_pr_body_completeness_check.ps1 -RequestedIdPrefix S0F- -PythonExe c:/python314/python.exe
```

- Allowed inputs:
  - `-RequestedIdPrefix` for the scope family to review
  - `-Repo` if the repository slug must be overridden
  - `-LogsDir` if the default `docs/logs` root must be overridden
  - `-WrapperNotes` for retained operator notes
  - `-RunId` or `-ArtifactRoot` only when the output root must be fixed explicitly
- Success looks like:
  - PowerShell exits `0`
  - `wrapper-result.json` records `result=pass`
  - `review-result.json` records zero `substantive_drift_ids` and zero `stop_ids`
- Failure looks like:
  - PowerShell exits `1` for a real completeness failure or `2` for wrapper-input/runtime failure
  - `wrapper-result.json` records `result=stop` or `result=error`

## 5) Local Operation

### 5.1 Prerequisites

- GitHub CLI authenticated for the target repository.
- Python environment able to run `scripts/issues/*.py`.
- Source-log ownership already converged enough that the targeted live slice set has canonical `links.pr` where required.

### 5.2 Commands

- Canonical local command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/issues/invoke_pr_body_completeness_check.ps1 -RequestedIdPrefix S0F- -PythonExe c:/python314/python.exe
```

- If the wrapper itself needs to be invoked directly for debugging, use the stable Python surface rather than calling the reviewer with ad hoc paths:

```powershell
c:/python314/python.exe scripts/issues/plan_pr_body_completeness_check_wrapper.py --requested-id-prefix S0F- --review-result-path artifacts/operator-facing/pr-body-completeness-check/manual-s0f/review-result.json --review-artifact-dir artifacts/operator-facing/pr-body-completeness-check/manual-s0f/review-files --wrapper-result-path artifacts/operator-facing/pr-body-completeness-check/manual-s0f/wrapper-result.json --wrapper-summary-path artifacts/operator-facing/pr-body-completeness-check/manual-s0f/workflow-summary.md --artifact-manifest-path artifacts/operator-facing/pr-body-completeness-check/manual-s0f/artifact-manifest.json --trigger-surface local-cli
```

## 6) Troubleshooting

- Symptom: wrapper exits with `result=stop` and `stop_reason=findings-present`.
  - Inspect: `review-result.json`
  - Action: check `substantive_drift_ids` and `stop_ids`; do not treat `skip_ids` as failure.

- Symptom: wrapper exits with `result=error` and `stop_reason=wrapper-input-invalid`.
  - Inspect: `wrapper-result.json` and the terminal output
  - Action: verify requested prefixes, logs root, Python path, and GitHub auth.

- Symptom: an expected live slice appears under `stop-missing-pr-link`.
  - Inspect: the slice source log under `docs/logs/`
  - Action: converge `links.pr` in source before rerunning the check.

- Symptom: a current in-progress slice appears under `skip-no-live-pr-owned`.
  - Inspect: `review-result.json`
  - Action: no repair is needed unless that slice should already own a live issue or PR.

- Symptom: the operator-facing artifact bundle is missing `review-files/` or `review-result.json`.
  - Inspect: `artifact-manifest.json` and `wrapper-result.json`
  - Action: rerun through `invoke_pr_body_completeness_check.ps1`; do not rely on a partial artifact root.

## 7) Notes and Boundaries

- This runbook is procedural only; the owning contract still lives in `S0F-1I` and `S0F-1H`.
- Do not use this runbook as the source of truth for reviewer semantics; the wrapper and canonical reviewer own those definitions.
- If operators need to repair formatting-only drift, leave this runbook and follow the bounded live convergence surfaces retained by `S0F-1I`.
- The next likely expansion point is wiring this same standard check surface into a repo task or CI gate once operator expectations no longer change.