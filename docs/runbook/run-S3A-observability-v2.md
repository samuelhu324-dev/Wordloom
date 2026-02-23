# Run-S3A: observability v2（Triage + Evidence Bundle + One-click Automation）

---

**id**: `S3A-observability-v2`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S3A-observability-v2`
**status**: `stable`          # draft | stable | archived
**scope**: `S3A`
**decision_date**: `2026-02-15`
**context_issue**: 
   **DoD**: `#33, #37, #41, #45, #48, #49, #51`
   **Labs**: `#34, #35, #38, #39, #40, #46, #47`
**decision**: `Standardize observability triage (metrics/tracing/structured logs) and automate failure drills into an evidence-bundle producing workflow (local + GitHub Actions).`
  **positive**: `"Repeatable triage workflow", "Machine-verifiable drills", "Evidence bundle artifacts for audit/hand-off"`
  **negative**: `"More infra in CI (compose + migrations)", "Need to keep evidence schema stable", "Tracing sampling means traces are supporting evidence"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Provide a repeatable incident/debug/audit workflow using **Metrics → Tracing → Structured Logs**.
- Ensure every failure drill run can output an **evidence bundle** (metrics/logs/traces + recipe/result) that is reviewable and hand-off friendly.
- Provide a **one-click** (GitHub Actions) automation entry that runs `run → verify → export → clean` and uploads the evidence artifact.

## 2) Scope

- Applies to API + worker processes that expose:
  - Metrics (`/metrics` on API; embedded Prometheus exporter on workers)
  - Tracing (OTLP → collector/Jaeger)
  - Structured logs (JSON lines)
- Applies to failure drills harnessed by `backend/scripts/cli.py`.

## 3) Triage Roles (3 Signals)

### 3.1 Metrics (Radar)

Answer: “Is the system healthy? Where is it burning? How big is the blast radius?”

Use for:
- Trend/threshold/alerting/capacity
- Fast scoping by low-cardinality labels (env/projection/op/result/reason)

Not ideal for:
- Single-event forensic details (payload, stack traces)

### 3.2 Tracing (Dashcam)

Answer: “How did this request/batch flow across steps? Where time was spent? Where it broke?”

Use for:
- Causal chain across modules/components
- Pinpoint the slow/failing step in a pipeline

Notes:
- Sampling may apply; treat as **supporting evidence**, not the only source of truth.

### 3.3 Structured Logs (Recorder)

Answer: “What exactly happened? What parameters, branch decisions, and error stacks?”

Use for:
- Auditable details: errors, stack traces, payload summaries
- Correlation via IDs/keys (e.g., correlation_id, trace_id/span_id, entity/outbox IDs)

## 4) Evidence Bundle Standard

### 4.1 Output root

- Automated evidence bundle root:
  - `docs/labs/_snapshot/auto/<lab_id>/<scenario>/<run_id>/`

### 4.2 Minimal bundle contract

Each run directory should include at least:
- `_recipe.json`: the “what we did” (scenario + parameters)
- `_result.json`: the “did it pass” (pass/why/checks[])
- `_logs/`: representative worker/API logs (structured)
- `_metrics/`: before/after scrape (or extracted snippets)
- `_exports/`: trace exports when available

## 5) One-click Automation (GitHub Actions)

### 5.1 What it does

The workflow runs the same harness as local execution:
- Start infra (DB/ES/Jaeger) via docker compose
- Generate + load `.env.test`
- Migrate DB (alembic)
- For each scenario (or `all`):
  - `labs run` → `labs verify` → `labs export` → `labs clean`
- Upload evidence bundle artifact from `docs/labs/_snapshot/auto/`

### 5.2 Operator instructions

- Open GitHub Actions: `drill-failures`（原 `failure-drills`）
- Choose input:
  - `scenario`: single scenario or `all`
  - `duration`: seconds
  - `lookback`: Jaeger lookback (e.g., `30m`)
  - `keep_last`: snapshot retention
- Run the workflow and download the artifact.

## 6) Local Operation

### 6.1 Prerequisites

- Docker engine running
- Python environment for backend dependencies
- Infra available (DB/ES/Jaeger) via compose

### 6.2 Run a single scenario (example)

- Run:
  - `python backend/scripts/cli.py labs run <scenario> --env-file .env.test --duration 25 --run-id <run_id>`
- Verify:
  - `python backend/scripts/cli.py labs verify <scenario> --run-id <run_id>`
- Export:
  - `python backend/scripts/cli.py labs export <scenario> --run-id <run_id> --lookback 30m`
- Clean:
  - `python backend/scripts/cli.py labs clean <scenario> --env-file .env.test --keep-last 20`

## 7) Troubleshooting Checklist

### 7.1 “Local works, Actions fails”

- Confirm env loading in CI (workflow sources `.env.test`).
- Confirm working directory assumptions (workflow runs from repo root).
- Confirm infra readiness (ES/DB reachable before labs).
- Confirm migrations ran (alembic upgrade head).

### 7.2 Verify flakiness

- If the assertion relies on metric deltas, ensure “before” scrape happens **before** injection/trigger.
- For scenarios sensitive to scrape timing (e.g., collector down), prefer additional ground-truth checks (DB/logs) as a fallback.

## 8) References

- Logs:
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
- Workflow:
  - `.github/workflows/drill-failures.yml`
- Harness:
  - `backend/scripts/cli.py`
