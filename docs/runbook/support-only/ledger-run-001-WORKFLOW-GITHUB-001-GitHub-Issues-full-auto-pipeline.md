# ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline

```yaml
runbook_run_ledger:
  run_ledger_id: ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  ledger_kind: runbook-run-ledger
  status: active
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
  reviewed_at: 2026-04-21
  accepted_at: pending
  target_reading_goal: show the first admitted accounting surface for the WORKFLOW-GITHUB-001 family after one real four-sample full-auto pilot run completed through issue conclusion.
```

## Decision Frame

- This ledger now remains `active` instead of `draft` because the first real admitted full-auto sample batch has executed across issue creation, PR creation, human merge, and post-merge issue conclusion refresh.
- The purpose of this ledger is now twofold: preserve the durable accounting surface for the first live run, and admit the concrete evidence rows that tie `RUN-001` to the four S4F samples and the bounded repairs consumed during that run.

## Run Ledger Table

| run row id | trigger kind | environment | target kind | submitted by | command summary | artifact root | verdict status | review status | approval status | downstream consumption | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `manual-plus-guarded-scripts` | `local-plus-github` | `issue-pr-conclusion-lifecycle` | `role:workflow-operator` | `Execute the first real WORKFLOW-GITHUB-001 sample batch across issue create -> PR create -> human merge -> guarded issue conclusion refresh.` | `artifacts/` | `pass_after_recovery` | `reviewed` | `pending` | `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md` | Four S4F samples now landed as live issue/PR/conclusion packets; bounded repairs in `PATCH-001-I02` and `PATCH-001-I03` were required but stayed inside the defended release. |

## Evidence Extraction Table

| evidence item id | run row id | artifact file | evidence type | extraction scope | admitted fields | verification status | used by | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001-E01` | `RUN-001` | `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` | `md` | `full` | `runbook family, release, ledger binding, minimum admitted fields` | `verified` | `S0G-2A/P2` | The bound runbook release remains the root contract evidence for the first admitted live run. |
| `RUN-001-E02` | `RUN-001` | `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` | `md` | `partial` | `parent run row binding, bounded repair refs, patch-ledger placement` | `verified` | `RUN-001 patch binding` | The first admitted run consumed two bounded repairs and now binds the reserved patch ledger back to `RUN-001`. |
| `RUN-001-E03` | `RUN-001` | `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md` | `md` | `partial` | `requested_id, issue link, PR link, sample lineage` | `verified` | `RUN-001 live sample set` | `S4F-1A` is admitted as part of the first live four-sample batch. |
| `RUN-001-E04` | `RUN-001` | `docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md` | `md` | `partial` | `requested_id, issue link, PR link, sample lineage` | `verified` | `RUN-001 live sample set` | `S4F-2A` is admitted as part of the first live four-sample batch. |
| `RUN-001-E05` | `RUN-001` | `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md` | `md` | `partial` | `requested_id, issue link, PR link, sample lineage` | `verified` | `RUN-001 live sample set` | `S4F-2B` is admitted as part of the first live four-sample batch. |
| `RUN-001-E06` | `RUN-001` | `docs/logs/log-S4F-2C-deployed-identity-admission-membership-truth-hardening.md` | `md` | `partial` | `requested_id, issue link, PR link, sample lineage` | `verified` | `RUN-001 live sample set` | `S4F-2C` is admitted as part of the first live four-sample batch. |
| `RUN-001-E07` | `RUN-001` | `artifacts/_tmp_s4f_1a_issue_conclusion_apply_result.json` | `json` | `full` | `requested_id, issue_number, final_issue_state, issue_url` | `verified` | `RUN-001 conclusion admission` | The guarded post-merge conclusion refresh for `S4F-1A` completed with final issue state `CLOSED`. |
| `RUN-001-E08` | `RUN-001` | `artifacts/_tmp_s4f_2a_issue_conclusion_apply_result_retry.json` | `json` | `full` | `requested_id, issue_number, final_issue_state, issue_url` | `verified` | `RUN-001 conclusion admission` | The guarded post-merge conclusion refresh for `S4F-2A` completed with final issue state `CLOSED`. |
| `RUN-001-E09` | `RUN-001` | `artifacts/_tmp_s4f_2b_issue_conclusion_apply_result.json` | `json` | `full` | `requested_id, issue_number, final_issue_state, issue_url` | `verified` | `RUN-001 conclusion admission` | The guarded post-merge conclusion refresh for `S4F-2B` completed with final issue state `CLOSED`. |
| `RUN-001-E10` | `RUN-001` | `artifacts/_tmp_s4f_2c_issue_conclusion_apply_result_retry2.json` | `json` | `full` | `requested_id, issue_number, final_issue_state, issue_url` | `verified` | `RUN-001 conclusion admission` | The guarded post-merge conclusion refresh for `S4F-2C` completed with final issue state `CLOSED`. |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `role:workflow-operator` | `role:runbook-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-artifact-inspection and live-github-state-check` | `pending` | `pending` | The four-sample run completed with concrete issue, PR, patch, and conclusion evidence rows admitted into the parent ledger, but explicit human approval is still left pending. | GitHub-side issue states for `#507` through `#510` were checked live after conclusion apply, and the local apply-result artifacts preserve the exact post-merge write-back evidence. |

## Optional Run Time Audit

| run row id | run started at | run completed at | source recorded at | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `RUN-001` | `2026-04-21` | `2026-04-21` | `2026-04-21` | `day` | `GitHub merged-at timestamps were recorded in UTC; run-ledger write-back was completed from the local operator session on the same date.` | The first admitted run spanned four S4F samples through issue creation, PR creation, human merge, and guarded issue-conclusion refresh. |

## Reader Notes

- This file is now the durable accounting surface for the first admitted `WORKFLOW-GITHUB-001` live sample batch.
- Future sample rounds should either append a new run ledger row or open the next run ledger file instead of rewriting the admitted evidence for `RUN-001`.