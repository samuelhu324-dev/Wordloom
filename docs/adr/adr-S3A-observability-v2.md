# ADR-S3A: observability v2（Triage + Evidence Bundle + Automation）

---

**id**: `S3A-observability-v2`
**kind**: `adr`               # log | lab | runbook | adr | note
**title**: `adr/S3A-observability-v2`
**status**: `stable`          # draft | stable | archived
**scope**: `S3A`
**decision_date**: `2026-02-15`
**context_issue**: `#32`
**decision**: `Adopt a three-signal observability model (metrics/tracing/structured logs) with a repeatable triage workflow, and productize failure drills into a one-click GitHub Actions pipeline that outputs evidence-bundle artifacts.`
  **positive**: `"Clear division of responsibilities", "Repeatable incident/audit workflow", "Automated, machine-verifiable drills", "Evidence artifacts for hand-off"`
  **negative**: `"More CI bootstrap complexity", "Need to maintain evidence bundle contract", "Tracing sampling limits trace-only proofs"`
**supersedes**: `null`
**superseded_by**: `null`

---

## Context

We needed observability that is not only usable for day-to-day debugging, but also produces **auditable evidence** during failure drills.
Historically, failure drills required manual steps (trigger/verify/export), and results were hard to reproduce across environments.
We also needed a consistent stance on what each signal is responsible for, to avoid “log-diving” and unstable conclusions.

## Decision

1) Standardize the observability model and triage workflow:
- **Metrics**: fast scoping and health/radius (low-cardinality labels)
- **Tracing**: causal chain and step localization (supporting evidence)
- **Structured logs**: detailed truth and audit-grade evidence

2) Define and enforce an **evidence bundle contract** for each drill run, written to:
- `docs/labs/_snapshot/auto/<lab_id>/<scenario>/<run_id>/`

3) Implement a **one-click automated** workflow in GitHub Actions that:
- bootstraps infra (compose), loads env, runs migrations,
- executes `run → verify → export → clean` (single scenario or `scenario=all`),
- uploads the evidence bundle as an artifact.

## Alternatives Considered

- Manual-only drills (run commands by hand): low setup cost, but non-repeatable and hard to audit.
- Metrics-only validation: fast, but insufficient explanatory power and weak for forensics.
- Trace-only validation: intuitive, but sampling and missing spans make it unreliable as sole evidence.
- Per-scenario ad-hoc scripts without a harness: quick initially, but wrappers drift and CI breaks easily.

## Consequences

- Teams get a predictable incident workflow: **Metrics → Tracing → Logs**, with shared keys/IDs enabling correlation.
- Drill runs become machine-verifiable and produce reviewable evidence artifacts.
- CI becomes heavier (infra + readiness + migrations), but results are reproducible and “buttonized”.
- We must keep the evidence schema stable (e.g., `_recipe.json`, `_result.json`) to preserve long-term usability.

## Implementation Notes

Key files that embody the decision:
- Harness entrypoint: `backend/scripts/cli.py`
- One-click automation: `.github/workflows/drill-failures.yml`
- Contract and troubleshooting history:
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
