# contract-release-ledger-supplement-template-v1

Use this supplement when later evidence needs to sharpen, narrow, revise, or reopen one verdict already admitted in a contract release ledger.

## Naming Rule

- Name contract release SUP ledgers as `ledger-SUP-<sequence>-<CONTRACT-ID>-<summary>.md`.
- Preferred example shape:
  - `ledger-SUP-001-DOC-RUNTIME-OBSERVABILITY-0001-scenario-family-intake.md`

## Minimal Header

```yaml
contract_release_ledger_supplement:
  supplement_series_id: <ledger-SUP-DOC-DOMAIN-SUBDOMAIN-0001>
  supplement_sequence: <001>
  supplement_id: <ledger-SUP-001-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  supplement_kind: contract-release-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_release_ledger_id: <ledger-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  parent_contract_id: <DOC-DOMAIN-SUBDOMAIN-0001>
  parent_row_id: <CRL-01>
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
  supplement_scope: <what later evidence this supplement is admitting>
  target_reading_goal: <what later readers should understand after this supplement is applied>
```

## Lifecycle Field Rule

- New writes should use canonical UTC second timestamps when the repo action time is defendable.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are packet-lifecycle timestamps only; they do not replace source chronology.
- If evidence time precision is weaker than packet-lifecycle precision, preserve that weaker precision in the evidence time audit rather than copying stronger repo timestamps into source fields.

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01-SUP-01>` | `<CRL-01>` | `<log/code/labs/runbook anchor>` | `<md|code|labs|artifact|mixed>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|append-evidence|rewrite-parent-row|reopen-ledger-verdict>` | `<none|rewrite-current-draft|open-new-release|defer-contract-change>` | `<why this evidence matters>` |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01-SUP-01>` | `<unknown|pending|role:contract-maintainer|name>` | `<unknown|pending|role:evidence-owner|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why the approval state is defended>` | `<why any actor fields remain partial>` |

## Optional Evidence Time Audit

| supplement item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01-SUP-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this evidence time audit matters>` |

## Write-Back Chain Rule

- The default release-scoped chain is `evidence -> SUP -> parent release ledger -> contract body`.
- `effect on current verdict` explains how the evidence changes the already-admitted row meaning.
- `proposed parent-ledger action` explains what should move in the parent ledger before the contract body changes.
- `contract impact` explains whether the contract body should stay unchanged, be rewritten, or defer the change to another family or later release.

## Required Rules

- Every SUP row must point to one existing `parent row id` in the parent contract release ledger.
- Use this surface when later evidence is about the current contract release object itself, not just about source-ledger routing.
- Write into the contract body only after the parent contract release ledger is updated or explicitly left unchanged.

## Completion Rule

- A contract release SUP may be marked `completed` only when every admitted evidence row has one explicit `verification status`, one explicit parent-ledger action, and one explicit contract-impact verdict.