# Run-S5B: security governance hard gates（policy/audit drills + operator entry）

---

**id**: `S5B-security-governance-hard-gates`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S5B-security-governance-hard-gates`
**status**: `draft`          # draft | stable | archived
**scope**: `S5B`
**decision_date**: `2026-03-13`
**context_issue**:
  **DoD**: ``
  **Labs**: `S5B-1A, S5B-3A, S5B-4A`
**decision**: `Provide one thin operator entry for S5B security and governance hard gates so policy, audit, and search-authorization drills can be run, verified, and triaged from a single top-level runbook.`
  **positive**: `"Single operator entry for security hard gates", "Evidence and ledgers stay machine-verifiable", "Keeps phase logs focused on evolution rather than step-by-step operation"`
  **negative**: `"Must keep workflow and script references stable", "Still depends on multiple phase-specific suites underneath"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one top-level entry for S5B policy, audit, and search-authorization hard gates.
- Make it clear where to run the suites, where evidence lands, and how to triage deny-reason or audit-contract drift.

## 2) Scope

- Covered:
  - policy and audit hard-gate drills
  - audit coverage operator workflow
  - search authorization and tenant-isolation drills
- Out of scope:
  - full implementation history of each chain
  - broader S5A design history and identity-provider expansion
- Primary source materials:
  - `docs/logs/log-S5B-security-governance-hard-gates.md`
  - `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  - `docs/logs/log-S5B-3A-audit-coverage-operator-workflow.md`
  - `docs/logs/log-S5B-4A-search-query-authorization-drills.md`

## 3) Evidence Bundle

### 3.1 Output roots

- Phase evidence roots:
  - `docs/labs/_snapshot/auto/S5B-1A/`
  - `docs/labs/_snapshot/auto/S5B-3A/`
  - `docs/labs/_snapshot/auto/S5B-4A/`
- Minimum artifacts contract follows the S5B-1A verifier shape:
  - `_recipe.json`
  - `_result.json`
  - `_logs/`
  - `_metrics/`

### 3.2 Summary or ledger

- Current operator-facing ledgers:
  - `artifacts/s5b3a-runs.json`
  - `artifacts/s5b4a-runs.json`
- For suites without a dedicated ledger yet, the phase log plus run directory remains the fact source.

## 4) One-click Automation

### 4.1 What it does

- Runs the phase-specific hard gate in CI.
- Uses the verifier and `_result.json.ok` as the pass/fail signal.
- Uploads or records the run directory and summary artifacts for later triage.

### 4.2 Operator instructions

- Primary workflows:
  - `.github/workflows/hard-gate-s5b1a-policy-audit.yml`
  - `.github/workflows/hard-gate-s5b3a-membership-audit.yml`
  - `.github/workflows/hard-gate-s5b4a-search-query-authorization.yml`
- Use CI first when you need a repeatable gate result tied to a head SHA.
- Use local commands first when you need rapid iteration before pushing.

## 5) Local Operation

### 5.1 Prerequisites

- backend Python environment available
- dev or test Postgres reachable
- API base URL and DB URL configured for the phase-specific suite

### 5.2 Commands

- Verify an existing S5B artifacts directory:
  - `python scripts/drills/s5b1a_verify_artifacts.py --run-dir <run_dir>`
- Run the membership-audit hard gate locally:
  - `python scripts/drills/s5b3a_p4_hard_gate.py`
- For policy-audit or search-authorization local drills, use the stable runner or hard-gate entry documented in the corresponding phase log before escalating to CI.

## 6) Troubleshooting

- verifier passes contract but `_result.json.ok=false`:
  - inspect the case-level `failure_reason` in `_result.json` before looking at raw logs
- deny reason drift or unexpected result mapping:
  - compare `action/result/reason` against the S5B-1A contract first
- audit rows missing or not traceable by `request_id`:
  - use the S5B-3A operator workflow and query path before debugging implementation details

## 7) Notes and Boundaries

- This runbook is intentionally thin and top-level; implementation consolidation and phase closure stay in the S5B logs.
- `S5B-2A` remains a reference log, not a separate runbook, because it is mainly a consolidation slice rather than a standalone long-lived operator entry.