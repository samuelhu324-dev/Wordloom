# Run-S4A-2A: deploy / verify / rollback runtime path (local dev/test)

---

**id**: `S4A-2A-deploy-verify-rollback-runtime-path`
**kind**: `runbook`
**title**: `run/S4A-2A-deploy-verify-rollback-runtime-path`
**status**: `draft`
**scope**: `S4A-2A`
**decision_date**: `2026-03-21`
**context_issue**:
  **DoD**: ``
  **Labs**: `S4A-2A`
**decision**: `Use deploy_app_verify and a minimal env/Git-level rollback pattern as the thin operator entry for local dev/test deploy / post-deploy verification / rollback, so changes are always checked by one gate and can be rolled back with a repeatable path.`
  **positive**: `"Thin post-deploy gate", "Machine-verifiable PASS/FAIL", "Clear minimal rollback path"`
  **negative**: `"Covers only local dev/test", "No automatic DB/data rollback", "Depends on S4A-1A runtime scripts"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one stable post-deploy verification gate for the local dev/test runtime.
- Define a minimal rollback path when that gate fails (config or Git-level), reusing existing S4A-1A runtime scripts.
- Keep the deeper contract, drills, and history in the S4A-2A phase log while exposing only the operator-facing deploy/verify/rollback story here.

## 2) Scope

- Covered:
  - post-deploy verification of DB/API/UI/ES health on local dev/test using `deploy_app_verify`.
  - minimal rollback path when verification fails, by restoring env config or returning to a known-good Git head and re-running the same gate.
  - operator reading and interpreting `POST_DEPLOY_RESULT=PASS|FAIL` and the key status/health summaries.
- Out of scope:
  - production or multi-environment deploy pipelines.
  - DB data-level rollback or backup/restore (owned by future S4A-3A and S5A/S5B work).
  - CI-level hard gates and dashboards (owned by S6A and S3A-2A-4B).
- Primary source materials:
  - `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  - `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  - `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
  - `docs/runbook/run-S4A-1A-ops-scripting-baseline.md`
  - `scripts/ops/deploy_app_verify.sh`
  - `scripts/ops/status.sh`
  - `scripts/ops/health.sh`

## 3) Evidence Bundle

### 3.1 Output roots

- Phase-log evidence:
  - `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md` (P2-C1-S1/S2 evidence blocks).
- Current machine-verifiable checks:
  - exit code and `POST_DEPLOY_RESULT=PASS|FAIL` from `scripts/ops/deploy_app_verify.sh`.
  - `scripts/ops/status.sh` summary lines for `db_container`, `infra_es`, `api_health`, `ui_http`, `es_http`.
  - `scripts/ops/health.sh` summary lines for `db_devtest`, `api_health`, `ui_http`, `es_http`, and optional worker probes.
- Minimum operator proof for this phase:
  - one `deploy_app_verify` run with `POST_DEPLOY_RESULT=PASS` after a change.
  - if rollback is invoked, one failing run (`POST_DEPLOY_RESULT=FAIL`) and one recovered run (`POST_DEPLOY_RESULT=PASS`) recorded in the phase log with `headSha` and a short `rollback_reason`.

### 3.2 Summary or ledger

- The S4A-2A phase log is the current ledger; there is no dedicated JSON ledger file for deploy/verify/rollback yet.
- When in doubt, look at:
  - the `Evidence` section in `log-S4A-2A-deploy-verify-rollback-runtime-path.md`.
  - the terminal proof commands and observed `POST_DEPLOY_RESULT` values.

## 4) One-click Automation

### 4.1 What it does

- `deploy_app_verify`:
  - resolves the env (`dev|test`) and prints `phase=S4A-2A env=<env> target_head_sha=<sha>`.
  - runs `scripts/ops/status.sh <env>` and `scripts/ops/health.sh <env>` in sequence, capturing exit codes without stopping at the first error.
  - emits a low-cardinality result line: `POST_DEPLOY_RESULT=PASS` on full success, or `POST_DEPLOY_RESULT=FAIL status_rc=<rc> health_rc=<rc>` on failure.
  - exits 0 on PASS and non-zero on FAIL, so CI or other tooling can gate on it.

### 4.2 Operator instructions

- After any local deploy or runtime change on dev/test:
  - make sure you have followed the S4A-1A runbook for env prep and startup; at minimum:
    - `./scripts/ops/env_prep.sh dev`
    - `./scripts/ops/start.sh dev app --no-worker` (or `all --no-worker` if you need infra/db too).
  - then run the post-deploy gate:
    - `bash scripts/ops/deploy_app_verify.sh dev`
- Allowed operator knobs:
  - `env_name`: `dev` (default) or `test`.
  - there are no other supported flags yet; the script intentionally keeps the surface small.
- Success criteria:
  - terminal shows `POST_DEPLOY_RESULT=PASS`.
  - `status` summary lines report `db_container healthy`, `infra_es healthy`, `api_health 200`, `ui_http 200`, `es_http 200`.
- Failure criteria:
  - `POST_DEPLOY_RESULT=FAIL` and a non-zero exit code.
  - either `status_rc!=0` or `health_rc!=0` with corresponding DOWN/unexpected HTTP lines.

## 5) Local Operation

### 5.1 Prerequisites

- S4A-1A baseline satisfied for the target env:
  - WSL available (canonical local path) and Docker Desktop running.
  - `.env.<env>` present and consistent (for example `.env.dev` with `API_PORT`, `DATABASE_URL`, `ELASTIC_URL` fields).
  - backend and frontend dependencies installed as described in project docs.
- devtest DB and infra ES can be brought up via S4A-1A scripts (`db_up`, `infra_up`, or `start all`).

### 5.2 Commands

- Canonical "deploy + verify" after changing code or config:
  - `./scripts/ops/env_prep.sh dev`
  - `./scripts/ops/start.sh dev app --no-worker`
  - `bash scripts/ops/deploy_app_verify.sh dev`
- Canonical config-level rollback when verification fails (local example):
  - identify the offending `.env.dev` change (for example a wrong `API_PORT` or backend URL).
  - restore the config to the last known-good values (by editing `.env.dev`, or by aligning it with a committed template).
  - rerun:
    - `./scripts/ops/env_prep.sh dev`
    - `./scripts/ops/start.sh dev app --no-worker`
    - `bash scripts/ops/deploy_app_verify.sh dev`
- Canonical Git-level rollback (pattern):
  - identify the last known-good `headSha` from the S4A-2A log or Git history.
  - perform a Git rollback (for example `git revert` or `git checkout <good_sha>` in your local clone).
  - restart the runtime via S4A-1A scripts and rerun `deploy_app_verify`.

## 6) Troubleshooting

- `deploy_app_verify` exits non-zero with `status_rc!=0`:
  - first run `bash scripts/ops/status.sh <env>` directly and inspect which component is unhealthy.
  - use `scripts/ops/logs.sh` (from S4A-1A) to fetch the relevant container logs (`db`, `es`, or infra).
- `deploy_app_verify` exits non-zero with `health_rc!=0` but `status_rc==0`:
  - treat this as a runtime health failure after startup (for example API or UI not responding as expected).
  - run `bash scripts/ops/health.sh <env>` to see explicit `DOWN` or `unexpected HTTP` lines.
  - check recent code or config changes that would affect the reported endpoint.
- `api_health DOWN` from `health.sh`:
  - confirm the API process is actually running via the S4A-1A runbook (`start app` path and app terminal).
  - inspect `.env.<env>` for incorrect `API_PORT` or backend URLs.
- `ui_http DOWN` from `health.sh`:
  - confirm the frontend was started (for example via `scripts/ui_up.sh` or `start app`).
  - use a browser or `curl`/`curl.exe` against `http://127.0.0.1:30002/` to cross-check availability.
- DB or infra unhealthy:
  - follow the S4A-1A runbook for `env_prep` and `start` troubleshooting first.
  - do not treat S4A-2A deploy/verify as the primary place to repair DB/infra issues.

## 7) Notes and Boundaries

- This runbook is the operator entry for S4A-2A; it does not replace the phase log.
- It assumes the S4A-1A ops scripting baseline is already in place and stable.
- Current operator wording to reuse in production-style materials:
  - `deploy_app_verify`: post-deploy verification gate for the local runtime.
  - `POST_DEPLOY_RESULT`: low-cardinality deployment outcome (PASS/FAIL) for dev/test.
  - "rollback path": minimal env/Git-level pattern for returning to a known-good runtime state when the gate fails.
- Future expansions may add:
  - dedicated `deploy_db_migrations` and `deploy_runtime_bundle` scripts.
  - JSON evidence files and CI workflows that call `deploy_app_verify` as a hard gate.
- Until then, treat this runbook as the thin operator-facing layer on top of the S4A-2A log and S4A-1A runtime scripts.
