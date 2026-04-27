# contract-release-ledger-patch-template-v1

Use this patch ledger when one stable contract release needs a bounded repair packet that should remain under the same release instead of forcing a new release.

## Naming Rule

- Name contract release patch ledgers as `ledger-PATCH-<sequence>-<CONTRACT-ID>-<summary>.md`.
- Preferred example shape:
  - `ledger-PATCH-001-DOC-RUNTIME-OBSERVABILITY-0001-release-ledger-bootstrap.md`

## Minimal Header

```yaml
contract_release_patch_ledger:
  patch_ledger_id: <ledger-PATCH-001-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  patch_kind: contract-release-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_contract_id: <DOC-DOMAIN-SUBDOMAIN-0001>
  parent_contract_ref: <docs/governance/contracts/...md>
  parent_release_ledger_id: <ledger-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  parent_row_id: <CRL-01|pending|not-applicable>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_statement_ids:
    - <DOC-...-ST-01|none>
  affected_bridge_ids:
    - <DOC-...-CB-01|none>
  affected_coverage_ids:
    - <DOC-...-COV-01|none>
  patch_scope: <what bounded repair this packet admits>
  patch_reason_class: <docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>
  target_reading_goal: <what later readers should understand after this patch ledger is applied>
```

## Lifecycle Field Rule

- New writes should use canonical UTC second timestamps when the repo action time is defendable.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are packet-lifecycle timestamps only; they do not replace source chronology or the historical-effective range of the repaired meaning.
- If the repair cites evidence whose chronology is weaker than the packet lifecycle, keep that weaker precision in the patch time audit.

## Patch Change Table

| patch item id | parent row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current contract release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<CRL-01|pending|not-applicable>` | `<docs/governance/contracts/...>` | `<docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>` | `<diff|log|other>` | `<pending|verified|rejected>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<no-release-bump|candidate-release-bump-needs-log>` | `<no-change|append-patch-ref|rewrite-parent-row|open-sup-ledger>` | `<none|rewrite-current-draft|open-new-release|defer>` | `<why this patch matters>` |

## Actor and Provenance Review Table

| patch item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<unknown|pending|role:contract-maintainer|name>` | `<unknown|pending|role:evidence-owner|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<why the approval state is defended>` | `<why any actor fields remain partial>` |

## Optional Patch Time Audit

| patch item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this patch time audit matters>` |

## Write-Back Chain Rule

- The default repair chain is `repair evidence -> PATCH -> contract body`.
- If the repair also changes the admitted meaning of one release-ledger row, pair the patch with `SUP -> parent release ledger -> contract body` rather than hiding that semantic change inside the patch packet alone.
- Readers should be able to tell what changed by comparing the patch row, its time audit, the parent ledger verdict, and any later contract statement, bridge, or coverage evolution rows.

## Required Rules

- Use a contract release patch only for bounded repair on the contract release object itself.
- Do not use this surface to bypass a new release when semantic contract meaning materially changes.

## Completion Rule

- A contract release patch may be marked `completed` only when every admitted patch item has one explicit `verification status`, one explicit `approval status`, and one explicit parent-ledger or downstream write-back action.