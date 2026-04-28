# runbook-release-ledger-patch-template-v1

Use this patch ledger when one stable runbook release needs a bounded repair packet that should remain under the same release instead of forcing a release bump.
This surface is release-scoped and support-only.

## Naming Rule

- Name runbook release patch ledgers as `ledger-runbook-PATCH-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- Preferred example shape:
  - `ledger-runbook-PATCH-001-RUNTIME-OBSERVABILITY-001-release-ledger-bootstrap.md`

## Minimal Header

```yaml
runbook_release_patch_ledger:
  patch_ledger_id: <ledger-runbook-PATCH-001-RUNBOOK-FAMILY-001-summary>
  patch_kind: runbook-release-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  parent_runbook_ref: <docs/runbook/run-RUNBOOK-FAMILY-001-summary.md>
  parent_release_ledger_id: <ledger-runbook-RUNBOOK-FAMILY-001-summary>
  parent_row_id: <RBL-01|pending|not-applicable>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_bridge_ids:
    - <RB-01|none>
  affected_coverage_ids:
    - <SC-01|none>
  patch_scope: <what bounded repair this packet admits>
  patch_reason_class: <docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>
  target_reading_goal: <what later readers should understand after this patch ledger is applied>
```

## Lifecycle Field Rule

- New writes should use canonical UTC second timestamps when the repo action time is defendable.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are packet-lifecycle timestamps only; they do not replace source chronology or the historical-effective range of the repaired meaning.
- If the repair cites evidence whose chronology is weaker than the packet lifecycle, keep that weaker precision in the patch time audit.

## Patch Change Table

| patch item id | parent row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RBL-01|pending|not-applicable>` | `<docs/runbook/...>` | `<docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>` | `<diff|log|other>` | `<pending|verified|rejected>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<no-release-bump|candidate-release-bump-needs-log>` | `<no-change|append-patch-ref|rewrite-parent-row|open-sup-ledger>` | `<none|rewrite-runbook|rewrite-contract-bridge|defer>` | `<why this patch matters>` |

## Actor and Provenance Review Table

| patch item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<why the approval state is defended>` | `<why any actor fields remain partial>` |

## Optional Patch Time Audit

| patch item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this patch time audit matters>` |

## Write-Back Chain Rule

- The default repair chain is `repair evidence -> PATCH -> runbook body`.
- If the repair also changes the admitted meaning of one release-ledger row, pair the patch with `SUP -> parent release ledger -> runbook body` rather than hiding that semantic change inside the patch packet alone.
- Readers should be able to tell what changed by comparing the patch row, its time audit, the parent ledger verdict, and any later runbook bridge or coverage evolution rows.

## Required Rules

- Use a runbook release patch only for bounded repair on the runbook release object itself.
- Do not use this surface for per-run execution repairs; those belong to `ledger-run-PATCH-*`.
- If the repair materially changes runbook semantics, stop and open a new source log plus a new runbook release instead of continuing under the same patch series.

## Completion Rule

- A runbook release patch may be marked `completed` only when every admitted patch item has one explicit `verification status`, one explicit `approval status`, and one explicit parent-ledger or downstream write-back action.