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
  - `docs/labs/_snapshot/auto/`
  - `artifacts/`
- Minimum evidence contract:
  - `_result.json`
  - `_recipe.json`
  - `_logs/`
  - `_metrics/`
  - optional `summary.json`, `logs.txt`, `traces.json`, or CI zip bundles

### 3.2 Summary or ledger

- `_result.json` is the primary fact source for run success or failure.
- When a phase-specific ledger exists, use that ledger plus the run directory together.
- When no ledger exists, the phase log and the uploaded CI artifact are the authoritative operator trail.

## 4) One-click Automation

### 4.1 What it does

- Runs the selected drill suite or hard-gate workflow.
- Verifies contract and result using `_result.json` and related evidence.
- Uploads self-explaining artifacts so failures can be triaged without rerunning immediately.

### 4.2 Operator instructions

- Use the suite workflows documented by the selected scenario family, starting from the S6A-4A hard-gate guidance.
- For fault drills, the stable operator path remains the `labs run -> verify -> export -> clean` flow already used by S3A and extended by S6A.
- When a hard gate fails, inspect `_result.json` first, then logs or metrics, then the phase-specific contract details.

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

## 6) Troubleshooting

- `_result.json` missing:
  - treat that as a contract failure before debugging deeper behavior
- worker path or env wiring drift:
  - check the S6A-1A stable-entry expectations before inspecting scenario-specific code
- supply inserted into the wrong table or not visible to the consumer:
  - check the S6A-2A supply fields and DB-side supply check first
- reason distribution does not match expected family:
  - inspect the S6A-3A reason contract output before reviewing raw metrics dumps

## 7) Notes and Boundaries

- This runbook is the execution entry for S6A, not a replacement for the spine log.
- The S6A spine log remains the index and evolution record; this runbook only collects the operator path and first-line triage.