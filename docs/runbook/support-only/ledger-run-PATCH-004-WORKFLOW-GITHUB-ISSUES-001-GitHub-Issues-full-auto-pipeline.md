# ledger-run-PATCH-004-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: ledger-run-PATCH-004-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  patch_kind: runbook-run-ledger-patch
  status: active
  owner_lane: S4G-1A
  parent_runbook_id: run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  parent_runbook_ref: docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_ledger_id: ledger-run-004-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  parent_run_ledger_ref: docs/runbook/support-only/ledger-run-004-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_row_id: RUN-004
  parent_target_row_id: RUN-004-T02
  parent_target_stage_row_id: RUN-004-T02-STG-CREATION
  parent_target_stage_attempt_id: RUN-004-T02-STG-CREATION-A01
  target_ref_key: S4G-1A
  target_ref_path: docs/logs/log-S4G-1A-s4-history-extraction-and-code-first-fallback-cells-assessment.md
  patch_sequence: 004
  created_at: 2026-04-28
  reviewed_at: 2026-04-28
  accepted_at: pending
  writeback_started_at: 2026-04-28
  writeback_completed_at: 2026-04-28
  patch_scope: record the bounded create-surface repair that resolves exact roadmap-bridge milestone tokens to the live GitHub milestone title before create-time validation.
  patch_reason_class: script-fix
  approval_boundary: runbook-bound create-surface repairs must remain reviewable before they are treated as stable support-only evidence for later child-target execution under the same release.
  target_reading_goal: show that the first RUN-004 child target exposed one bounded gen_issue_draft.py failure mode, that the repair preserved fail-closed milestone validation semantics, and that the repaired surface was immediately validated by successful live issue creation for S4G-1A.
```

## Decision Frame

- This patch packet is bound to `RUN-004`, because the defect was first exposed by `S4G-1A` during the active `S4G` child execution sequence.
- The repair is intentionally narrow: exact roadmap bridge metadata such as `roadmap_milestone: M1` should resolve to the one live GitHub milestone title governed by the roadmap id prefix rather than failing closed on the shorthand token itself.
- No release bump is justified because the repair restores the defended milestone-resolution contract instead of widening feature scope or changing the admitted lifecycle model.

## Patch Packet Summary

| patch ledger id | patch sequence | parent run row id | repair scope | packet verdict | current release effect | admitted chronology effect | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-004` | `004` | `RUN-004` | `roadmap bridge milestone resolution repair in issue draft generation` | `completed` | `no-release-bump` | `no-direct-chronology-change` | `The repair was validated immediately by re-running S4G-1A live issue creation to issue #560 with the milestone normalized to the live GitHub title.` |

## Repair Delta Table

| patch item id | target artifact or path | repair class | prior defect reading | new defended repair reading | effect on admitted chronology | requires paired SUP? | paired SUP ref | parent-ledger writeback | primary evidence ref | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-004-I01` | `scripts/issues/gen_issue_draft.py` | `script-fix` | `exact roadmap bridge milestone tokens such as M1 were passed directly into create-time milestone validation, causing live issue creation to fail closed even when the repo contained the intended roadmap milestone under its canonical live title` | `derived roadmap bridge milestone tokens now resolve through roadmap_path metadata to the one live milestone title before validation, while still failing closed when no unique live title exists` | `no-direct-chronology-change` | `no` | `not-required` | `append-patch-ref` | `docs/issues/issue-S4G-1A-s4-history-extraction-and-code-first-fallback-cells-assessment.json` | `The repaired create path normalized the roadmap bridge token to the live milestone title and produced live issue #560 after the initial fail-closed attempt.` |

## Patch Change Table

| patch item id | parent run row id | target row id | target stage row id | target stage attempt id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-004-I01` | `RUN-004` | `RUN-004-T02` | `RUN-004-T02-STG-CREATION` | `RUN-004-T02-STG-CREATION-A01` | `scripts/issues/gen_issue_draft.py` | `script-fix` | `docs/issues/issue-S4G-1A-s4-history-extraction-and-code-first-fallback-cells-assessment.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-run-004-creation-for-roadmap-bridge-milestone-targets` | `The fix keeps live milestone validation fail-closed while allowing exact roadmap bridge shorthand to resolve to the canonical GitHub milestone title.` |

## Attachment Review Table

| attachment id | patch item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `PATCH-004-I01-ATT-01` | `PATCH-004-I01` | `docs/issues/issue-S4G-1A-s4-history-extraction-and-code-first-fallback-cells-assessment.json` | `accepted-for-packet` | `The successful post-repair create artifact records the normalized live milestone title and shows issue #560 was created live under the defended metadata set.` | `Checked the repaired live create output for S4G-1A after roadmap bridge milestone resolution was restored.` |

## Actor and Provenance Review Table

| patch item id | run row id | target row id | target stage row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-004-I01` | `RUN-004` | `RUN-004-T02` | `RUN-004-T02-STG-CREATION` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `live-create-replay-after-roadmap-bridge-milestone-resolution-repair` | `pending` | `pending` | `The repair is bounded to issue-draft milestone derivation and was validated by the immediate successful live create replay for S4G-1A.` | `This row was opened when the first S4G-1A create attempt failed closed on shorthand milestone M1 even though the repo already contained the canonical roadmap milestone title.` |

## Reader Notes

- `PATCH-004` stays repair-first: it explains why `RUN-004-T02-STG-CREATION-A01` should read as `pass_after_recovery`, but it does not become its own chronology round.
- If a later run-level reading needs sharpening because of this repair, that later admission should still land through a `SUP` packet rather than by overloading this patch ledger.
- The defended contract outcome is narrow and reusable for later `S4G` child targets that derive milestones from the same roadmap bridge metadata family.