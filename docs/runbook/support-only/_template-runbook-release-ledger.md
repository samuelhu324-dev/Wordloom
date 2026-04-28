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

## Lifecycle Field Rule

- New writes should use canonical UTC second timestamps such as `2026-04-12T15:18:05Z` for artifact-lifecycle fields whenever the repo action time is actually known.
- Legacy or bounded-precision values such as `2026-04-12` may remain when the defended evidence proves only the day.
- `created_at`, `reviewed_at`, and `accepted_at` are artifact-lifecycle timestamps for this ledger file only; they are not substitutes for source execution or historical-effective time.
- If the source chronology is weaker than the current repo action time, keep the weaker source precision in the chronology audit rather than copying the stronger artifact timestamp into source-facing fields.

## Row Chronology Audit

- Keep this section present whenever one row is expected to survive as a reusable intake or staged write-back surface.

| row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this row chronology matters>` |

- `source observed at` is the best known time the underlying evidence event, code state, lab run, or reader-facing signal was observed.
- `source recorded at` is the best known time that evidence was written down, exported, committed, or otherwise admitted as one usable source.
- `source effective from` and `source effective until` describe the best known historical-effective range for the semantic signal carried by that intake row.
- `time precision` must reflect the strongest defended precision only; do not fabricate seconds when the source proves only a date.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-E01>` | `<intake-admitted|ledger-writeback-started|ledger-writeback-completed|review-state-changed>` | `<RBL-01|this-ledger>` | `<role:runbook-maintainer|pending>` | `<row admitted for later runbook write-back>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>` | `<RBL-01|supporting source>` | `<why this governance event matters>` |

## Write-Back Chain Rule

- The full release-scoped chain is:
  - `source or strong-structure evidence -> SUP (optional) -> runbook release ledger -> runbook body`
- Use `SUP -> runbook release ledger -> runbook body` when later evidence sharpens, narrows, or reopens an already-admitted intake row.
- Use `PATCH -> runbook body` for bounded repair on the runbook release object itself; if that repair also changes the admitted reading of one ledger row, pair it with a `SUP` or direct parent-ledger rewrite instead of hiding the semantic delta in the patch packet.
- Readers should be able to tell what changed by comparing:
  - the current intake row verdict,
  - the row chronology audit,
  - the governance event row,
  - and any downstream runbook bridge or coverage evolution rows written later.

## Intake and Write-Back Table

| row id | evidence anchor | evidence class | semantic area | intended landing surface | current verdict | affected bridge ids | affected coverage ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01>` | `<log/contract/code/labs anchor>` | `<source-log|code|labs|runbook|contract|mixed>` | `<scenario inventory|boundary note|evidence contract|other>` | `<runbook-body|code-bridge-table|scenario-registry|notes-and-boundaries|defer>` | `<applied-current-release|pending-classification|deferred|rejected>` | `<RB-01; RB-02|none>` | `<SC-01; SC-02|none>` | `<why this intake matters>` |

## Scenario Routing Registry

- Add this section whenever one parent intake row carries many scenario-level standing or routing outcomes.

| scenario row id | parent row id | scenario name | classified standing | current runbook status | current owner surface | route status | destination kind | destination ref | last routing event id | source supplement item ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-02-SC-01>` | `<RBL-02>` | `<es_timeout>` | `<current-family|support-only|sibling-family>` | `<already-in-runbook|release-ledger-only|not-owned-here>` | `<runbook-body|release-ledger|source-log|sibling-lane>` | `<no-change-needed|awaiting-writeback|retained-here|routed-out|rejected>` | `<runbook-body|release-ledger-only|source-log-only|sibling-ledger|pending-p3>` | `<SC-01|docs/...|pending>` | `<RBL-02-SC-E01>` | `<RBL-02-SUP-01; RBL-02-SUP-03|none>` | `<why this scenario is currently routed this way>` |

## Scenario Routing Chronology Audit

| scenario row id | first observed at | first recorded at | classified at | last routed at | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-02-SC-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|pending|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this scenario chronology matters>` |

## Scenario Routing Event Table

| routing event id | scenario row id | change action | from surface | to surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-02-SC-E01>` | `<RBL-02-SC-01>` | `<classified-current-family|classified-support-only|classified-sibling-family|written-into-runbook|rerouted-to-sibling|retained-in-ledger>` | `<release-ledger-intake>` | `<runbook-body|release-ledger|source-log|sibling-lane|pending-p3>` | `<role:runbook-maintainer|pending>` | `<what changed for this scenario>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>` | `<RBL-02; RBL-02-SUP-03>` | `<why this routing event matters>` |

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
- When a parent row carries many scenarios, each scenario should get one stable `scenario row id` before downstream write-back starts.
- `destination ref` must become explicit once a scenario is actually written into a runbook body row or routed into a sibling lane.

## Reader Notes

- Keep one short reader-facing note near the end of live files so later readers can tell:
  - what currently landed in the runbook,
  - what remains admitted only in the release ledger,
  - and which changes still await explicit write-back.

## Completion Rule

- A runbook release ledger may be marked `completed` only when every intake row has one explicit current verdict and one explicit intended landing surface.