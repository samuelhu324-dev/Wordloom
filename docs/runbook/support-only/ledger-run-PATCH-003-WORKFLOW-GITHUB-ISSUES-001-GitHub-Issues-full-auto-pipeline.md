# ledger-run-PATCH-003-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: ledger-run-PATCH-003-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  patch_kind: runbook-run-ledger-patch
  status: active
  owner_lane: S0G-3E
  parent_runbook_id: run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  parent_runbook_ref: docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_ledger_id: ledger-run-002-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  parent_run_ledger_ref: docs/runbook/support-only/ledger-run-002-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_row_id: RUN-002
  parent_target_row_id: RUN-002-T01
  parent_target_stage_row_id: RUN-002-T01-STG-CREATION
  parent_target_stage_attempt_id: RUN-002-T01-STG-CREATION-A01
  target_ref_key: S0G-1B
  target_ref_path: docs/logs/log-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.md
  patch_sequence: 003
  created_at: 2026-04-24
  reviewed_at: 2026-04-24
  accepted_at: pending
  writeback_started_at: 2026-04-24
  writeback_completed_at: 2026-04-24
  patch_scope: record the bounded create-surface repair that removed unsafe default project fallback when source-log issue_projects is blank for live issue creation.
  patch_reason_class: script-fix
  approval_boundary: runbook-bound create-surface repairs must remain reviewable before they are treated as stable support-only evidence for later target execution under the same release.
  target_reading_goal: show that the first RUN-002 target exposed one bounded gen_issue_draft.py failure mode, that the repair preserved fail-closed semantics for blank issue_projects, and that the repaired surface was immediately validated by successful live issue creation for S0G-1B.
```

## Decision Frame

- This patch packet is bound to `RUN-002`, because the defect was exposed by the first admitted target in the new remaining-`S0G` run rather than by any earlier `RUN-001` batch surface.
- The repair is intentionally narrow: blank `issue_projects` on `docs/logs/*` should remain blank, not default to a workspace project name that may not exist in the target GitHub repo.
- No release bump is justified because the repair restores the defended fail-closed blank-field contract instead of widening feature scope or changing the admitted lifecycle model.

## Patch Packet Summary

| patch ledger id | patch sequence | parent run row id | repair scope | packet verdict | current release effect | admitted chronology effect | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-003` | `003` | `RUN-002` | `blank issue_projects fail-closed repair in issue draft generation` | `completed` | `no-release-bump` | `no-direct-chronology-change` | `The repair was validated immediately by re-running S0G-1B live issue creation to issue #526 with issue_projects preserved as an empty list.` |

## Repair Delta Table

| patch item id | target artifact or path | repair class | prior defect reading | new defended repair reading | effect on admitted chronology | requires paired SUP? | paired SUP ref | parent-ledger writeback | primary evidence ref | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-003-I01` | `scripts/issues/gen_issue_draft.py` | `script-fix` | `blank issue_projects on docs/logs fell through to a default workspace project, causing live gh issue create to fail closed when that project did not exist in the repo` | `blank issue_projects now remains blank, preserving the source-log contract and allowing live create to proceed only without unintended project mutation` | `no-direct-chronology-change` | `no` | `not-required` | `append-patch-ref` | `docs/issues/issue-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.json` | `The repaired create path returned issue_projects as [] and produced live issue #526 after the fallback removal.` |

## Patch Change Table

| patch item id | parent run row id | target row id | target stage row id | target stage attempt id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-003-I01` | `RUN-002` | `RUN-002-T01` | `RUN-002-T01-STG-CREATION` | `RUN-002-T01-STG-CREATION-A01` | `scripts/issues/gen_issue_draft.py` | `script-fix` | `docs/issues/issue-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-run-002-creation-for-blank-project-targets` | `The fix keeps blank issue_* fields fail-closed instead of silently mutating live create inputs with repo-specific defaults.` |

## Attachment Review Table

| attachment id | patch item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `PATCH-003-I01-ATT-01` | `PATCH-003-I01` | `docs/issues/issue-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.json` | `accepted-for-packet` | `The successful post-repair create artifact records issue_projects as an empty list and shows issue #526 was created live under the defended metadata set.` | `Checked the repaired live create output for S0G-1B after the default-project fallback was removed.` |

## Actor and Provenance Review Table

| patch item id | run row id | target row id | target stage row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-003-I01` | `RUN-002` | `RUN-002-T01` | `RUN-002-T01-STG-CREATION` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `live-create-replay-after-default-project-fallback-removal` | `pending` | `pending` | `The repair is bounded to issue-draft input derivation and was validated by the immediate successful live create replay for S0G-1B.` | `This row was opened when the first S0G-1B create attempt failed closed on nonexistent project 'wordloom Board' despite the source log leaving issue_projects blank by contract.` |

## Reader Notes

- `PATCH-003` stays repair-first: it explains why `RUN-002-T01-STG-CREATION-A01` reads as `pass_after_recovery`, but it does not become its own chronology round.
- If a later run-level reading needs sharpening because of this repair, that later admission should still land through a `SUP` packet rather than by overloading this patch ledger.
- The defended contract outcome is narrow and reusable for later remaining `S0G` child targets: blank `issue_projects` should stay blank unless the source log names an explicit live project target.