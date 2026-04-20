# ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline

```yaml
runbook_run_ledger:
  run_ledger_id: ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  ledger_kind: runbook-run-ledger
  status: draft
  owner_lane: S0G-2A
  runbook_family: WORKFLOW-GITHUB
  runbook_release: 001
  runbook_id: run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  runbook_ref: docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
  run_sequence: 001
  governance_area: workflow
  functional_domain: GitHub lifecycle automation
  environment_class: local-plus-github
  target_surface: issue creation, PR creation, merge follow-through, and issue conclusion
  created_at: 2026-04-20
  reviewed_at: pending
  accepted_at: pending
  target_reading_goal: show the first admitted accounting surface for the WORKFLOW-GITHUB-001 family and preserve a stable place for the first real full-auto pilot run.
```

## Decision Frame

- This first run ledger opens in `draft` because the family-level runbook has now been published, but the first real admitted full-auto sample run has not yet been executed.
- The purpose of this ledger is to fix the durable accounting surface before the first live sample, so the initial real run can land in one explicit place instead of being scattered across source-log evidence rows and raw artifacts only.

## Run Ledger Table

| run row id | trigger kind | environment | target kind | submitted by | command summary | artifact root | verdict status | review status | approval status | downstream consumption | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `planned-full-auto-sample` | `local-plus-github` | `issue-pr-conclusion-lifecycle` | `role:workflow-operator` | `Open the first real WORKFLOW-GITHUB-001 sample across issue creation -> PR creation -> human merge -> issue conclusion.` | `docs/issues/` | `not_run` | `pending` | `pending` | `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md` | This row is intentionally opened before execution so the first admitted sample has a fixed accounting home. |

## Evidence Extraction Table

| evidence item id | run row id | artifact file | evidence type | extraction scope | admitted fields | verification status | used by | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001-E01` | `RUN-001` | `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` | `md` | `full` | `runbook family, release, ledger binding, minimum admitted fields` | `verified` | `S0G-2A/P2` | The first admitted evidence item is the bound runbook release itself, because the run-ledger surface is being opened before the first live run. |
| `RUN-001-E02` | `RUN-001` | `docs/issues/` | `artifact-root` | `root-only` | `planned future issue/pr/conclusion artifacts` | `pending` | `future live sample packet` | This placeholder row records the defended artifact root that the first real sample run is expected to populate. |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `role:workflow-operator` | `role:runbook-maintainer` | `pending` | `role:evidence-verifier` | `direct-doc-inspection` | `pending` | `pending` | The ledger surface is opened and bound to the first real sample family, but the live full-auto run has not yet been executed. | The current packet can defend the family binding and planned run surface, but not yet a real execution or GitHub-side result. |

## Optional Run Time Audit

| run row id | run started at | run completed at | source recorded at | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `unknown` | `unknown` | `2026-04-20` | `day` | `planning-only scaffold round` | The first real execution has not started yet; this row currently audits only the scaffold date for the accounting surface. |

## Reader Notes

- This file is the first durable accounting surface for `WORKFLOW-GITHUB-001`; it is not yet proof that a live full-auto sample has succeeded.
- The next bounded packet should execute the first real sample and then update `RUN-001` with admitted issue/PR/conclusion artifacts, verdict state, review state, and any required downstream write-back.