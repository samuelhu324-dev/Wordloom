# runbook-release-ledger-supplement-template-v1

Use this supplement when later evidence needs to sharpen, narrow, revise, or reopen one verdict already admitted in a runbook release ledger.
This SUP surface is release-scoped; it does not replace source logs and it does not replace run-level `ledger-run-SUP-*` packets.

## Naming Rule

- Name runbook release SUP ledgers as `ledger-runbook-SUP-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- Preferred example shape:
  - `ledger-runbook-SUP-001-RUNTIME-OBSERVABILITY-001-scenario-family-intake.md`

## Minimal Header

```yaml
runbook_release_ledger_supplement:
  supplement_series_id: <ledger-runbook-SUP-RUNBOOK-FAMILY-001>
  supplement_sequence: <001>
  supplement_id: <ledger-runbook-SUP-001-RUNBOOK-FAMILY-001-summary>
  supplement_kind: runbook-release-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_release_ledger_id: <ledger-runbook-RUNBOOK-FAMILY-001-summary>
  parent_runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  parent_row_id: <RBL-01>
  parent_scenario_row_ids:
    - <RBL-01-SC-01|none>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_bridge_ids:
    - <RB-01|none>
  affected_coverage_ids:
    - <SC-01|none>
  supplement_scope: <what later evidence this supplement is admitting>
  target_reading_goal: <what later readers should understand after this supplement is applied>
```

## Lifecycle Field Rule

- New writes should use canonical UTC second timestamps when the repo action time is defendable.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are packet-lifecycle timestamps only; they do not replace source chronology.
- If evidence time precision is weaker than packet-lifecycle precision, preserve that weaker precision in the evidence time audit rather than copying stronger repo timestamps into source fields.

## Evidence Table

| supplement item id | parent row id | parent scenario row ids | evidence ref | evidence type | verification status | effect on current verdict | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01-SUP-01>` | `<RBL-01>` | `<RBL-01-SC-01; RBL-01-SC-02|none>` | `<log/code/labs/runbook anchor>` | `<md|code|labs|artifact|mixed>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|append-evidence|rewrite-parent-row|rewrite-scenario-route|reopen-ledger-verdict>` | `<none|rewrite-runbook|rewrite-contract-bridge|defer>` | `<why this evidence matters>` |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01-SUP-01>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why the approval state is defended>` | `<why any actor fields remain partial>` |

## Optional Evidence Time Audit

| supplement item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01-SUP-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this evidence time audit matters>` |

## Write-Back Chain Rule

- The default release-scoped chain is `evidence -> SUP -> parent release ledger -> runbook body`.
- `effect on current verdict` explains how the evidence changes the already-admitted row meaning.
- `proposed parent-ledger action` explains what should move in the parent ledger before the runbook body changes.
- `downstream impact` explains whether the runbook body should stay unchanged, be rewritten, or defer the change to another family.
- `parent_scenario_row_ids` should be populated whenever the evidence sharpens, reroutes, or confirms one scenario-level standing beneath the parent row.

## Required Rules

- Every SUP row must point to one existing `parent row id` in the parent runbook release ledger.
- Scenario-specific SUP rows should also point to one or more existing `parent scenario row ids`.
- Use this surface when the follow-up changes release-scoped meaning or admission standing, not when it only sharpens one admitted run.
- Write into the runbook body only after the parent runbook release ledger is updated or explicitly left unchanged.

## Completion Rule

- A runbook release SUP may be marked `completed` only when every admitted evidence row has one explicit `verification status`, one explicit parent-ledger action, and one explicit downstream impact verdict.