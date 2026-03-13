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
  **Labs**: `S5B-1A, S5B-2A, S5B-3A, S5B-4A`
**decision**: `Provide one concrete operator entry for S5B security and governance hard gates so policy, entrypoint, audit, and search-authorization suites can be run, verified, and triaged from a single top-level runbook.`
  **positive**: `"Single operator entry for security hard gates", "Evidence and ledgers stay machine-verifiable", "Keeps phase logs focused on evolution rather than step-by-step operation"`
  **negative**: `"Must keep workflow and script references stable", "Still depends on multiple phase-specific suites underneath"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one top-level entry for S5B policy, policy-entrypoint, audit, and search-authorization hard gates.
- Make it clear which suite to run for each security/governance concern, where evidence lands, and what to inspect first when deny reasons or audit contracts drift.

## 2) Scope

- Covered:
  - policy/audit contract drills (`S5B-1A`)
  - policy entrypoint consolidation drills (`S5B-2A`)
  - policy and audit hard-gate drills
  - audit coverage operator workflow
  - search authorization and tenant-isolation drills
- Out of scope:
  - full implementation history of each chain
  - broader S5A design history and identity-provider expansion
- Primary source materials:
  - `docs/logs/log-S5B-security-governance-hard-gates.md`
  - `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  - `docs/logs/log-S5B-2A-policy-entrypoint-consolidation.md`
  - `docs/logs/log-S5B-3A-audit-coverage-operator-workflow.md`
  - `docs/logs/log-S5B-4A-search-query-authorization-drills.md`

## 3) Evidence Bundle

### 3.1 Output roots

- Phase evidence roots:
  - `docs/labs/_snapshot/auto/S5B-1A/`
  - `docs/labs/_snapshot/auto/S5B-2A/`
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
- Current phase-to-ledger reality:
  - `S5B-1A`: no dedicated runs ledger; use phase log + run directory + CI artifact name
  - `S5B-2A`: no dedicated runs ledger; use phase log + run directory + CI artifact name
  - `S5B-3A`: `artifacts/s5b3a-runs.json`
  - `S5B-4A`: `artifacts/s5b4a-runs.json`

## 4) One-click Automation

### 4.1 What it does

- Runs the phase-specific hard gate in CI.
- Uses the verifier and `_result.json.ok` as the pass/fail signal.
- Uploads or records the run directory and summary artifacts for later triage.

### 4.2 Operator instructions

- Primary workflows:
  - `.github/workflows/hard-gate-s5b1a-policy-audit.yml`
  - `.github/workflows/hard-gate-s5b2a-policy-entrypoint.yml`
  - `.github/workflows/hard-gate-s5b3a-membership-audit.yml`
  - `.github/workflows/hard-gate-s5b4a-search-query-authorization.yml`
- Suggested operator mapping:
  - `S5B-1A`: contract regression for tenant boundary, deny reasons, audit traceability
  - `S5B-2A`: policy entrypoint consolidation for `bookshelf.delete`
  - `S5B-3A`: membership audit coverage and replay/forensics workflow
  - `S5B-4A`: search query authorization and tenant isolation
- Use CI first when you need a repeatable gate result tied to a head SHA.
- Use local commands first when you need rapid iteration before pushing or when narrowing one failing suite.

## 5) Local Operation

### 5.1 Prerequisites

- backend Python environment available
- dev or test Postgres reachable
- backend API running locally when the suite exercises HTTP routes
- baseline env vars configured for the phase-specific suite:
  - `WORDLOOM_API_BASE_URL=http://127.0.0.1:31001`
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@127.0.0.1:5435/wordloom_test`
  - `WORDLOOM_JWT_SECRET_KEY=dev-secret-key-change-in-production`
  - `WORDLOOM_JWT_ALG=HS256`
- additional suite-specific env when needed:
  - `S5B_1A_ACTOR_USER_ID=<uuid>` for the S5B-1A hard gate

### 5.2 Commands

- Verify any existing S5B artifacts directory:
  - `python scripts/drills/s5b1a_verify_artifacts.py --run-dir <run_dir>`
- Run S5B-1A hard gate locally:
  - `python scripts/drills/s5b1a_p4_hard_gate.py`
- Run S5B-2A hard gate locally:
  - `python scripts/drills/s5b2a_p3_hard_gate.py`
- Run S5B-3A hard gate locally:
  - `python scripts/drills/s5b3a_p4_hard_gate.py`
- Run S5B-4A hard gate locally:
  - `python scripts/drills/s5b4a_p3c1s1_hard_gate.py`
- Useful suite overrides when narrowing scope:
  - `S5B_1A_SUITES=tenant_escape_read,tenant_escape_write,audit_completeness`
  - `S5B_2A_SUITES=bookshelf_delete_entrypoint`
  - `S5B_3A_SUITE_ID=membership_audit_coverage`
  - `S5B_4A_SUITE_ID=search_query_authorization`
- Minimal local execution order:
  - start devtest DB
  - migrate backend DB
  - start local backend on `127.0.0.1:31001`
  - export env vars above
  - run the selected hard gate

## 6) Troubleshooting

- verifier passes contract but `_result.json.ok=false`:
  - inspect the case-level `failure_reason` in `_result.json` before looking at raw logs
- a phase artifact exists but no ledger was updated:
  - for `S5B-1A` and `S5B-2A`, that is expected; use the run directory and CI artifact as the fact source
- deny reason drift or unexpected result mapping:
  - compare `action/result/reason` against the S5B-1A contract first
- `bookshelf.delete` gate is failing unexpectedly:
  - inspect `S5B-2A` first, because tenant mismatch versus not_found classification is intentionally concentrated there
- audit rows missing or not traceable by `request_id`:
  - use the S5B-3A operator workflow and query path before debugging implementation details
- search authorization failures:
  - inspect `S5B-4A` `_result.json` and confirm `library_id` / tenant expectations before reviewing backend code

### 6.1 Validated Decision Paths

- happy path, existing green artifact:
  - `S5B-2A` sample run dir `docs/labs/_snapshot/auto/S5B-2A/bookshelf_delete_entrypoint/7e464272-8352-41b6-b655-b5077597edfe`
  - expected first check: verify the artifact contract, then confirm `_result.json.ok=true`
- happy path, ledger-backed green artifact:
  - `S5B-3A` sample run dir `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/332361bc-3bb1-4d99-862c-a40d586190db`
  - expected first check: inspect `_result.json.summary` and confirm all five membership audit cases passed
- known failure, contract-ok red artifact:
  - `S5B-3A` sample run dir `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/9d3cdfc1-2fb0-43c8-8364-a00b5db4e87e`
  - expected first check: verifier may still return contract OK, so classify by case-level `failure_reason` before suspecting missing evidence
- ambiguity, stale evidence path:
  - historical run dir `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/16b34278-d370-4be4-9e8f-29a455e25111`
  - expected first check: if verifier reports `missing_run_dir`, treat it as stale or unavailable evidence and reroute to a current local run dir or CI artifact instead of treating it as suite failure
- cross-phase routing example:
  - when the symptom is unexpected `bookshelf.delete` classification, go to `S5B-2A` first even if it surfaced during broader policy triage, because that boundary is intentionally concentrated there

## 7) Notes and Boundaries

- This runbook is intentionally thin and top-level; implementation consolidation and phase closure stay in the S5B logs.
- `S5B-1A` through `S5B-4A` stay as phase logs and suites, not separate runbooks, because the operator should enter from one top-level gate family rather than four competing documents.
- `S5B-2A` remains a reference-heavy consolidation slice; it is included in this runbook because it has a real hard gate, but it still does not justify a standalone long-lived runbook.