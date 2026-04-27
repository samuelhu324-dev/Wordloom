# contract-release-ledger-template-v1

Use this ledger when one stable contract release needs a durable, release-first intake surface for evidence, clause routing, bridge or coverage write-back, and later archaeology.
This ledger is centered on the contract object itself. It complements, and does not replace, source-owned routing ledgers.

## Naming Rule

- Name contract release ledgers as `ledger-<CONTRACT-ID>-<summary>.md`.
- The summary should normally match the bound contract filename suffix exactly.
- Preferred example shape:
  - `ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`

## Minimal Header

```yaml
contract_release_ledger:
  ledger_id: <ledger-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  ledger_kind: contract-release-ledger
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  contract_family: <DOC-DOMAIN-SUBDOMAIN>
  contract_release: <0001>
  contract_id: <DOC-DOMAIN-SUBDOMAIN-0001>
  contract_ref: <docs/governance/contracts/...md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  source_of_authority:
    - <source ledger or source log anchor>
  target_reading_goal: <what later readers should understand after this ledger is applied>
```

## Lifecycle Field Rule

- New writes should use canonical UTC second timestamps such as `2026-04-12T15:18:05Z` whenever the repo action time is actually known.
- Legacy or bounded-precision values such as `2026-04-12` may remain when the defended evidence proves only the day.
- `created_at`, `reviewed_at`, and `accepted_at` are artifact-lifecycle timestamps for this ledger file only; they are not substitutes for source chronology or contract effective time.
- If source chronology is weaker than packet lifecycle, keep the weaker precision in the chronology audit rather than copying stronger repo timestamps into source-facing fields.

## Row Chronology Audit

| row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this row chronology matters>` |

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-E01>` | `<intake-admitted|ledger-writeback-started|ledger-writeback-completed|review-state-changed>` | `<CRL-01|this-ledger>` | `<role:contract-maintainer|pending>` | `<row admitted for later contract write-back>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>` | `<CRL-01|supporting source>` | `<why this governance event matters>` |

## Write-Back Chain Rule

- The full release-scoped chain is:
  - `source or strong-structure evidence -> SUP (optional) -> contract release ledger -> contract body`
- Use `SUP -> contract release ledger -> contract body` when later evidence sharpens, narrows, or reopens an already-admitted intake row.
- Use `PATCH -> contract body` for bounded repair on the contract release object itself; if that repair also changes the admitted reading of one ledger row, pair it with a `SUP` or direct parent-ledger rewrite instead of hiding the semantic delta in the patch packet.
- Readers should be able to tell what changed by comparing:
  - the current intake row verdict,
  - the row chronology audit,
  - the governance event row,
  - and any downstream statement, bridge, or coverage evolution rows written later.

## Intake and Write-Back Table

| row id | evidence anchor | evidence class | semantic area | intended landing surface | current verdict | affected statement ids | affected bridge ids | affected coverage ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01>` | `<log/code/labs/runbook anchor>` | `<source-ledger|source-log|code|labs|runbook|mixed>` | `<clause intake|bridge intake|coverage note|boundary note|other>` | `<statement-table|code-bridge-table|coverage-table|release-change|defer>` | `<applied-current-release|pending-classification|deferred|rejected>` | `<DOC-...-ST-01|none>` | `<DOC-...-CB-01|none>` | `<DOC-...-COV-01|none>` | `<why this intake matters>` |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01>` | `<unknown|pending|role:contract-maintainer|name>` | `<unknown|pending|role:evidence-owner|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-ledger|needs-better-evidence|rejected>` | `<why this state is defended>` | `<why any actor values remain partial>` |

## Required Rules

- Use this ledger when the question is `how should this contract release absorb, defer, or reject new release-scoped evidence?`
- Source-owned ledgers still own source slicing and initial routing; do not bypass them when the unresolved question is still source structure.
- Contract release ledgers are the correct landing surface when the new evidence comes from code, labs, retained runbooks, or other strong-structure channels and the target is an existing contract release.
- Keep clause, bridge, and coverage mutation deferred in the contract body until the ledger verdict is explicit.

## Reader Notes

- Keep one short reader-facing note near the end of live files so later readers can tell:
  - what currently landed in the contract,
  - what remains admitted only in the release ledger,
  - and which changes still await explicit write-back.

## Completion Rule

- A contract release ledger may be marked `completed` only when every intake row has one explicit current verdict and one explicit intended landing surface.