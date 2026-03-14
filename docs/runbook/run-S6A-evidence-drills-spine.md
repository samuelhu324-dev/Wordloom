# Run-S6A: evidence drills spine（hard-gate operations + evidence triage）

---

**id**: `S6A-evidence-drills-spine`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S6A-evidence-drills-spine`
**status**: `draft`          # draft | stable | archived
**scope**: `S6A`
**decision_date**: `2026-03-13`
**context_issue**:
  **DoD**: ``
  **Labs**: `S6A-1A, S6A-2A, S6A-3A, S6A-4A`
**decision**: `Provide one top-level operator entry for evidence and drills hard gates so stable entry, supply creation, reason contract, and CI evidence JSON can be operated as one workflow.`
  **positive**: `"Single top-level entry for fault-suite operations", "Evidence JSON remains the fact source", "Clarifies what to inspect first when a hard gate fails"`
  **negative**: `"Still depends on multiple underlying scenarios and workflows", "Needs ongoing discipline to avoid duplicating the spine log"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one thin entry for running and triaging evidence and drills hard gates.
- Make the main execution path explicit: stable entry, supply creation, run, verify, export, inspect evidence.

## 2) Scope

- Covered:
  - stable worker entry expectations
  - unified supply creation expectations
  - reason-contract verification expectations
  - hard-gate evidence JSON and CI artifact expectations
  - `fault/obs_infra/*` suite operation across local runs and CI hard gates
- Out of scope:
  - full history of all prior drill systems
  - non-S6A domain logic owned by S2B, S3A, or S0C
- Primary source materials:
  - `docs/logs/log-S6A-evidence-drills-spine.md`
  - `docs/logs/log-S6A-1A-stable-entry-contract.md`
  - `docs/logs/log-S6A-2A-unify-supply-creation.md`
  - `docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md`
  - `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`

## 3) Evidence Bundle

### 3.1 Output roots

- Snapshot roots:
  - local snapshot: `docs/labs/_snapshot/auto/S3A-2A-3A/<scenario>/<run_id>/`
  - CI artifact bundle: `artifacts/_tmp_ci_run_<run>/labs-evidence-*/S3A-2A-3A/<scenario>/<run_id>/`
  - auxiliary artifacts: `artifacts/_tmp_s6a*/`
- Minimum evidence contract:
  - `_result.json`
  - `_recipe.json`
  - `_logs/`
  - `_metrics/`
  - optional `summary.json`, `logs.txt`, `traces.json`, or CI zip bundles

### 3.2 Summary or ledger

- `_result.json` is the primary fact source for run success or failure.
- `S6A` currently has no dedicated runs ledger under `artifacts/`; do not waste time searching for `s6a-runs.json`.
- Use the phase log, run directory, and CI artifact name or run URL together as the authoritative operator trail.

## 4) One-click Automation

### 4.1 What it does

- Runs the selected drill suite or hard-gate workflow.
- Verifies contract and result using `_result.json` and related evidence.
- Uploads self-explaining artifacts so failures can be triaged without rerunning immediately.

### 4.2 Operator instructions

- Primary CI workflows:
  - `.github/workflows/hard-gate-fault-es-timeout.yml`
  - `.github/workflows/hard-gate-fault-es-down-connect.yml`
  - `.github/workflows/hard-gate-fault-es-429-inject.yml`
  - `.github/workflows/hard-gate-fault-es-bulk-partial.yml`
  - `.github/workflows/hard-gate-fault-es-write-block-4xx.yml`
  - `.github/workflows/hard-gate-fault-db-claim-contention.yml`
  - `.github/workflows/hard-gate-fault-collector-down.yml`
  - `.github/workflows/hard-gate-fault-duplicate-delivery.yml`
  - `.github/workflows/hard-gate-fault-projection-version.yml`
  - `.github/workflows/hard-gate-fault-stuck-reclaim.yml`
- For fault drills, the stable operator path remains the `labs run -> verify -> export -> clean` flow already used by S3A and extended by S6A.
- When a hard gate fails, inspect `_result.json` first, then logs or metrics, then the phase-specific contract details.
- `require_min_artifacts=true` is part of the CI contract; a green verify without `_recipe/_logs/_metrics` is not a valid S6A hard-gate result.

## 5) Local Operation

### 5.1 Prerequisites

- backend Python environment available
- required infra available for the chosen scenario
- environment variables prepared for DB, ES, and related services when needed

### 5.2 Commands

- Run:
  - `python backend/scripts/cli.py labs run <scenario> --env-file .env.test --run-id <run_id>`
- Verify:
  - `python backend/scripts/cli.py labs verify <scenario> --run-id <run_id>`
- Export:
  - `python backend/scripts/cli.py labs export <scenario> --run-id <run_id> --lookback 30m`
- Clean:
  - `python backend/scripts/cli.py labs clean <scenario> --env-file .env.test --keep-last 20`
- Common scenario mapping:
  - `es_down_connect`: supply path + transport-family reason checks
  - `es_timeout`: timeout-family reason checks
  - `es_429_inject`: rate-limit path and early stable-entry regressions
  - `es_bulk_partial`: partial-success/partial-failure mixed evidence

## 6) Troubleshooting

- `_result.json` missing:
  - treat that as a contract failure before debugging deeper behavior
- worker path or env wiring drift:
  - check the S6A-1A stable-entry expectations before inspecting scenario-specific code
- supply inserted into the wrong table or not visible to the consumer:
  - check the S6A-2A supply fields and DB-side supply check first
- reason distribution does not match expected family:
  - inspect the S6A-3A reason contract output before reviewing raw metrics dumps
- `_result.json.ok=false` and all observed deltas stay `0`:
  - treat that as an entry or trigger-path problem first; the `es_429_inject/20260304T195127` sample shows this shape
- `supply_db_check.ok=false`:
  - stop at S6A-2A and fix supply visibility before reviewing worker behavior
- `reason_contract.db_reason_check.ok=false` or reason family drifts:
  - stop at S6A-3A and compare DB `error_reason` with metrics `reason` before reading raw logs
- local snapshot path is missing but a CI run URL or artifact name exists:
  - treat that as `CI-only evidence`, then inspect `artifacts/_tmp_ci_run_<run>/labs-evidence-*/S3A-2A-3A/<scenario>/<run_id>/` instead of classifying it as suite failure

### 6.1 Validated Decision Paths

- happy path, local green supply + verify sample:
  - `docs/labs/_snapshot/auto/S3A-2A-3A/es_down_connect/S6A-2A-P1-C2-S1`
  - expected first check: confirm `supply_db_check.ok=true`, then confirm `_result.json.ok=true`
- happy path, local green reason-contract sample:
  - `docs/labs/_snapshot/auto/S3A-2A-3A/es_timeout/s6a3a-p3c5s4-20260305-211200`
  - expected first check: confirm `reason_contract.observed.db_reasons=["es_timeout"]` and `_result.json.ok=true`
- known failure, stable-entry or trigger-path regression:
  - `docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/20260304T195127`
  - expected first check: classify the run by `ok=false` plus zero metric deltas before suspecting reason-contract drift
- ambiguity, CI-only evidence bundle:
  - local path `docs/labs/_snapshot/auto/S3A-2A-3A/es_timeout/22746408022-1-fault_obs_infra_es_timeout-r1` does not exist in this workspace
  - CI artifact bundle exists at `artifacts/_tmp_ci_run_22746408022/labs-evidence-fault_obs_infra_es_timeout-22746408022-1-fault_obs_infra_es_timeout-r1/S3A-2A-3A/es_timeout/22746408022-1-fault_obs_infra_es_timeout-r1`
  - expected first check: reroute to the CI bundle and inspect `_result.json.ok` there rather than treating the missing local snapshot as a failed run

## 7) Notes and Boundaries

- This runbook is the execution entry for S6A, not a replacement for the spine log.
- The S6A spine log remains the index and evolution record; this runbook only collects the operator path and first-line triage.