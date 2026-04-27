# runbook-release-ledger-template-v1

Use this ledger when one stable runbook release needs a durable, release-first intake surface for evidence, scenario additions, boundary clarifications, and staged write-back.
This ledger is about the runbook release object itself; it does not replace source logs and it does not replace per-run accounting.

## Naming Rule

- Name runbook release ledgers as `ledger-runbook-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- `<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>` should match the bound runbook suffix exactly.
- Preferred example shape:
  - `ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`

## Minimal Header

```yaml
runbook_release_ledger:
  ledger_id: <ledger-runbook-RUNBOOK-FAMILY-001-summary>
  ledger_kind: runbook-release-ledger
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  runbook_family: <RUNBOOK-FAMILY>
  runbook_release: <001>
  runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  runbook_ref: <docs/runbook/run-RUNBOOK-FAMILY-001-summary.md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  source_of_authority:
    - <source log or contract anchor>
  target_reading_goal: <what later readers should understand after this ledger is applied>
```

## Intake and Write-Back Table

| row id | evidence anchor | evidence class | semantic area | intended landing surface | current verdict | affected bridge ids | affected coverage ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01>` | `<log/contract/code/labs anchor>` | `<source-log|code|labs|runbook|contract|mixed>` | `<scenario inventory|boundary note|evidence contract|other>` | `<runbook-body|code-bridge-table|scenario-registry|notes-and-boundaries|defer>` | `<applied-current-release|pending-classification|deferred|rejected>` | `<RB-01; RB-02|none>` | `<SC-01; SC-02|none>` | `<why this intake matters>` |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-ledger|needs-better-evidence|rejected>` | `<why this state is defended>` | `<why any actor values remain partial>` |

## Required Rules

- Use this ledger when the question is `how should this runbook release absorb, defer, or reject new release-scoped evidence?`
- Do not use this ledger to replace source-owned ledgers when the unresolved problem is still source slicing.
- Do not use this ledger to replace `ledger-run-*` execution accounting when the evidence belongs to one concrete run.
- `affected bridge ids` and `affected coverage ids` may stay `none` until a later write-back is explicit; do not invent ids only to fill the table.
- Keep object-level evidence here first when the runbook body should not widen yet.

## Completion Rule

- A runbook release ledger may be marked `completed` only when every intake row has one explicit current verdict and one explicit intended landing surface.