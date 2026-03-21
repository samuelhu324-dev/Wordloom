# Run-S4A-1A: ops scripting baseline（runtime support entry + health triage）

---

**id**: `S4A-1A-ops-scripting-baseline`
**kind**: `runbook`
**title**: `run/S4A-1A-ops-scripting-baseline`
**status**: `draft`
**scope**: `S4A-1A`
**decision_date**: `2026-03-21`
**context_issue**:
  **DoD**: ``
  **Labs**: `S4A-1A`
**decision**: `Use scripts/ops as the thin operator entry for local runtime support so environment preparation, cold start, warm start, status summary, health checks, and first-line log inspection all follow one stable path.`
  **positive**: `"Stable operator entry", "Cold-start and warm-start paths are separated", "Status and health checks are machine-verifiable"`
  **negative**: `"Still depends on WSL + Docker + Windows npm fallback for the current frontend path", "Full all-start path is not yet idempotent when devtest db is already running"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one thin runtime-support entry for preparing, starting, checking, and triaging the local dev/test runtime.
- Make the first-response path explicit: `env_prep -> start -> status -> health -> logs -> stop`.
- Keep the deeper evolution history in the `S4A-1A` log while exposing only the stable operator-facing path here.

## 2) Scope

- Covered:
  - environment readiness checks for the local runtime
  - cold start of infra/db and warm start of the app layer
  - status summary and health-gate checks for DB, API, UI, and ES
  - first-line log access for docker-managed services
- Out of scope:
  - deploy/rollback workflow owned by future `S4A-2A`
  - backup/recovery operator path owned by future `S4A-3A`
  - hybrid runtime expansion owned by future `S4A-4A`
- Primary source materials:
  - `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  - `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
  - `scripts/ops/env_prep.sh`
  - `scripts/ops/start.sh`
  - `scripts/ops/stop.sh`
  - `scripts/ops/status.sh`
  - `scripts/ops/health.sh`
  - `scripts/ops/logs.sh`
  - `scripts/ui_up.sh`

## 3) Evidence Bundle

### 3.1 Output roots

- Current first-pass evidence root:
  - terminal proof recorded in `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
- Current machine-verifiable checks:
  - `scripts/ops/status.sh` output
  - `scripts/ops/health.sh` exit code and summary lines
  - optional raw probe proof such as `curl.exe -I http://127.0.0.1:30002/`
- Minimum operator proof for this phase:
  - one successful `status` summary
  - one successful `health` check
  - the corresponding `headSha` recorded in the phase log evidence section

### 3.2 Summary or ledger

- `docs/logs/log-S4A-1A-ops-scripting-baseline.md` is currently the operator ledger.
- There is no dedicated `artifacts/` JSON ledger for `S4A-1A` yet; do not search for a separate `s4a-runs.json` file.

## 4) One-click Automation

### 4.1 What it does

- `env_prep` checks whether the runtime can be operated safely in the current shell and host environment.
- `start all` performs a cold-start path for infra, devtest DB, migrations, and the app layer.
- `start app` performs a warm-start path when infra and DB are already healthy.
- `status` gives a low-cardinality runtime summary suitable for first-line inspection.
- `health` provides PASS/FAIL operator checks for DB, API, UI, and ES.

### 4.2 Operator instructions

- Cold start:
  - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/env_prep.sh dev"`
  - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/start.sh dev all --no-worker"`
- Warm start when infra/db are already up:
  - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/start.sh dev app --no-worker"`
- Summary and health:
  - `bash scripts/ops/status.sh dev`
  - `bash scripts/ops/health.sh dev`
- First-line logs:
  - `bash scripts/ops/logs.sh db`
  - `bash scripts/ops/logs.sh es`
  - `bash scripts/ops/logs.sh infra`
- Stop docker-managed runtime:
  - `bash scripts/ops/stop.sh all`
- Allowed operator knobs:
  - env: `dev | test`
  - start target: `env_prep | infra | db | app | all`
  - app modifiers: `--no-worker`, `--no-ui`

## 5) Local Operation

### 5.1 Prerequisites

- WSL available for the canonical local path
- Docker Desktop or equivalent Docker engine available
- backend Python environment available for API and migration paths
- frontend dependencies installed; current WSL path may fall back to Windows `npm.cmd` through `scripts/ui_up.sh`

### 5.2 Commands

- Canonical cold-start path:
  - `./scripts/ops/env_prep.sh dev`
  - `./scripts/ops/start.sh dev all --no-worker`
- Canonical warm-start path:
  - `./scripts/ops/start.sh dev app --no-worker`
- Canonical inspection path:
  - `./scripts/ops/status.sh dev`
  - `./scripts/ops/health.sh dev`
- Canonical log path:
  - `./scripts/ops/logs.sh db`
  - `./scripts/ops/logs.sh es`
- Canonical stop path:
  - `./scripts/ops/stop.sh all`

## 6) Troubleshooting

- `env_prep` fails on port occupancy before cold start:
  - treat that as a runtime-state conflict first
  - inspect whether `db` or app ports are already in use before retrying `start all`
- `start all` fails while devtest DB is already running:
  - current behavior is non-idempotent for the cold-start path
  - use `start app` as the warm-start path instead of rerunning `all`
- `api_health=000`:
  - inspect the app terminal or rerun `./scripts/ops/start.sh <env> app --no-worker`
  - then re-check `./scripts/ops/health.sh <env>`
- `ui_http=000` from WSL while the frontend is expected to be up:
  - confirm whether the frontend was launched through `scripts/ui_up.sh`
  - inspect `curl.exe -I http://127.0.0.1:30002/` from Windows to confirm the UI is actually listening
- `worker_healthz/readyz=000`:
  - first confirm whether this was an intentional `--no-worker` path or `SEARCH_OUTBOX_WORKER_ENABLED=0`
  - do not classify that as runtime failure until the worker path is intentionally enabled
- ES is up but UI or API is failing:
  - separate infra health from app health
  - treat `status` as the summary and `health` as the gate before going deeper into logs

## 7) Notes and Boundaries

- This runbook is the operator entry for `S4A-1A`, not a replacement for the phase log.
- The phase log remains the source of truth for P/C/S history and evidence bookkeeping.
- Current operator wording to reuse in production-style materials:
  - `env_prep`: environment readiness check
  - `start all`: cold-start runtime path
  - `start app`: warm-start application recovery path
  - `status`: runtime summary / first-line operational visibility
  - `health`: post-start verification gate
  - `logs`: first-line incident triage entry
  - `stop`: controlled docker-managed runtime shutdown
- The next likely operator-facing expansion is not more script proliferation; it is making the cold-start path idempotent and then extending the same wording to deploy/verify/rollback in `S4A-2A`.