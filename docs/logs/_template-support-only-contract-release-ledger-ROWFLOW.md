# support-only-contract-release-ledger-row-flow-template

## Purpose

- Use this attached ledger when one already-routed parent-ledger row must be split into multiple derived rows, absorbed with adjacent parent rows, or forwarded into different downstream outlets before current write-back is reviewable.
- This ledger owns `derived-row accounting, split-or-absorption tracking, parent-ledger write-back recommendation, and downstream consumption tracking`.
- This ledger is attached to one source-owned parent ledger and sits at the same review level as a `SUP` ledger, but it is not a supplement round: it records row decomposition and flow rather than later evidence admission.
- Do not use the control log as the durable place for this accounting; the control log should keep decision and evolution notes only.

## Naming Rule

- Name row-flow ledgers as `ledger-<source-id>-<row-scope>-<summary>.md`.
- `<source-id>` must match the attached parent ledger source id.
- `<row-scope>` must render the exact parent row scope being decomposed, for example `R01` or `R01-R04`.
- The `<summary>` should describe the decomposition purpose, not the reviewing lane.
- Preferred example shapes:
  - `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`
  - `ledger-S0B-2A-R03-R04-labs-and-runbook-split-accounting.md`

## Minimal Header

```yaml
support_only_contract_release_row_flow_ledger:
  row_flow_ledger_id: <ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption>
  ledger_kind: support-only-contract-release-row-flow-ledger
  status: <draft|active|completed>
  owner_lane: <S4G-1B>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  parent_ledger_id: <ledger-S3A-2A-combo-observability-triage>
  parent_source_id: <S3A-2A>
  parent_row_scope: <S3A-2A-R01>
  parent_row_ref: <docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md>
  source_scope: <what row split or absorption problem this ledger covers>
  target_reading_goal: <what readers should understand after this decomposition is applied>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, and `accepted_at` are artifact-lifecycle fields for this attached ledger only.
- `writeback_started_at` records when parent-ledger, contract, or adjacent-surface write-back begins.
- `writeback_completed_at` records when the accepted write-back is complete in the repo.
- These timestamps do not replace parent-row source chronology or contract chronology.

## Recommended Decision Frame

- State clearly whether this attached ledger is:
  - the first decomposition draft
  - a completed split-and-consumption record
  - or a partial decomposition that still leaves some parent meaning unresolved
- State clearly which surfaces remain authoritative after the split:
  - the parent ledger for original row identity
  - the attached row-flow ledger for derived-row accounting
  - any downstream contract or runbook for current reader ownership

## Recommended Current Governance State

- Record current ownership, steward, review, and approval state for:
  - the attached row-flow ledger itself
  - the attached parent ledger
  - any current control log that still explains the decision sequence
  - any downstream current reader already resolved from this split

## Derived Row And Consumption Table

| derived row id | parent row ids | derivation kind | meaning owned here | downstream owner | target release action | derivation status | applied-to surface | resolution status | resolved by surface | resolved by contract id | consumed scope | parent write-back state | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<S3A-2A-R01-D01>` | `<S3A-2A-R01>` | `<semantic-claim|boundary-bridge|entrypoint-bridge|proof-binding|runbook-boundary|support-guard>` | `<what this derived row now means>` | `<contract|runbook|support-only|log-retained core|other>` | `<new-family|new-release|revise-release|no-contract>` | `<split-from-parent|split-from-parent-plus-absorbs-adjacent|forwarded-without-consumption|retained-local-only>` | `<bounded code surface or n/a>` | `<draft|applied|partially-applied|deferred|retained-support-only|re-routed|rejected>` | `<path to ledger/log/contract/runbook now owning the reader>` | `<DOC-...|none>` | `<full|partial|none>` | `<queued|written-back|not-required>` | `<why this decomposition and current result are correct>` |

## Parent Write-Back Table

| parent row id | attached-ledger effect | derived row ids | parent-ledger action | downstream impact | write-back status | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<S3A-2A-R01>` | `<split|split-plus-adjacent-absorption|forward-only>` | `<S3A-2A-R01-D01; S3A-2A-R01-D02>` | `<rewrite-parent-row|add-parent-note|no-parent-change-yet>` | `<contract-opened|runbook-deferred|support-only-only|mixed>` | `<pending|applied|deferred>` | `<what the parent ledger should now say>` |

## Row Chronology Audit

| derived row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<S3A-2A-R01-D01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone note>` | `<why this derived row time audit matters>` |

- Use this audit when the source chronology of one derived row depends on a mixture of one parent row and one or more absorbed adjacent rows.
- Keep source chronology here separate from later write-back or release chronology.

## Recommended Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<S3A-2A-R01-GOV-01>` | `<contribution-event|derived-row-accounting-opened|parent-writeback-event|contract-source-rewrite-event|runbook-deferred-event>` | `<surface name>` | `<unknown|pending|role:...>` | `<what current state changed>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<rows or surfaces used as basis>` | `<why this event matters>` |

## Recommended Reader Notes

- Explain briefly:
  - what the parent row was
  - why it could no longer remain one undivided routed slice
  - where the current reader now lives for each major derived row cluster

## Completion Rule

- A row-flow ledger may be marked `completed` only when every derived row has one explicit `resolution status` and every required parent write-back row has one explicit `write-back status`.
- Leaving the parent row split informal in the control log is not completion.

## Optional Rollup

- `current reader handoff`:
  - list which derived rows now read through contract, runbook, support-only, or retained log surfaces
- `unconsumed derived rows`:
  - list derived rows intentionally left deferred or support-only
- `adjacent absorbed rows`:
  - list any parent rows outside the main row scope that materially sharpened one derived row in this ledger