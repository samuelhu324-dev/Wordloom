# Run-S3A: failure drills & gitactions & dashboard（Triage + Evidence Bundle + One-click Automation）

---

**id**: `S3A-failure-drills-&-gitactions-&-dashboard`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S3A-failure-drills-&-gitactions-&-dashboard`
**status**: `stable`          # draft | stable | archived
**scope**: `S3A`
**decision_date**: `2026-02-15`
**context_issue**:
  **DoD**: `#33, #37, #41, #45, #48, #49, #51`
  **Labs**: `#34, #35, #38, #39, #40, #46, #47`
**decision**: `Standardize failure-drill triage and evidence-bundle automation so operators can run, verify, export, and clean with stable local and GitHub Actions entrypoints.`
  **positive**: `"Repeatable triage workflow", "Machine-verifiable drills", "Evidence bundle artifacts for audit and hand-off"`
  **negative**: `"More infra in CI", "Need to keep evidence schema stable", "Tracing remains supporting evidence"`
**supersedes**: `docs/runbook/run-S3A-observability-v2.md`
**superseded_by**: `null`

---

## 1) Purpose

- Provide a repeatable incident, debug, and audit workflow using metrics, tracing, and structured logs.
- Ensure every failure drill run emits an evidence bundle that can be reviewed and handed off.
- Keep one stable operator path for `run -> verify -> export -> clean`.

## 2) Scope

- Covered:
  - failure drills executed through `backend/scripts/cli.py`
  - local triage and GitHub Actions automation
  - evidence bundles under `docs/labs/_snapshot/auto/`
- Out of scope:
  - domain-specific semantics of each individual fault scenario
  - deeper failure-contract evolution already owned by S2B and S6A logs
- Primary source materials:
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
  - `docs/adr/adr-S3A-observability-v2.md`

## 3) Evidence Bundle

### 3.1 Output roots

- Automated evidence root:
  - `docs/labs/_snapshot/auto/<lab_id>/<scenario>/<run_id>/`
- Minimum bundle:
  - `_recipe.json`
  - `_result.json`
  - `_logs/`
  - `_metrics/`
  - `_exports/` when traces are available

### 3.2 Summary or ledger

- GitHub Actions uploads artifacts from `docs/labs/_snapshot/auto/`.
- `_result.json` remains the primary fact source for pass/fail and supporting checks.

## 4) One-click Automation

### 4.1 What it does

- Starts required infra for the selected drill suite.
- Runs `labs run`, `labs verify`, `labs export`, and `labs clean`.
- Uploads the resulting evidence bundle as an artifact.

### 4.2 Operator instructions

- Open GitHub Actions workflow `drill-failures`.
- Choose:
  - `scenario`
  - `duration`
  - `lookback`
  - `keep_last`
- Run the workflow and inspect the downloaded artifact if verification fails.

## 5) Local Operation

### 5.1 Prerequisites

- Docker engine running
- backend Python environment installed
- infra available through compose when required by the chosen scenario

### 5.2 Commands

- Run:
  - `python backend/scripts/cli.py labs run <scenario> --env-file .env.test --duration 25 --run-id <run_id>`
- Verify:
  - `python backend/scripts/cli.py labs verify <scenario> --run-id <run_id>`
- Export:
  - `python backend/scripts/cli.py labs export <scenario> --run-id <run_id> --lookback 30m`
- Clean:
  - `python backend/scripts/cli.py labs clean <scenario> --env-file .env.test --keep-last 20`

## 6) Troubleshooting

- local run works but Actions fails:
  - check env loading, repo-root working directory, infra readiness, and migrations first
- verify looks flaky on metric deltas:
  - confirm the before scrape happened before injection or trigger
- traces are missing:
  - treat traces as supporting evidence and fall back to `_result.json`, logs, and metrics

## 7) Notes and Boundaries

- This runbook is the operator entry; the malfunction history and design rationale stay in the S3A logs and ADR.
- The previous filename `run-S3A-observability-v2.md` is superseded so the runbook suffix now matches the parent log name `failure-drills-&-gitactions-&-dashboard`.