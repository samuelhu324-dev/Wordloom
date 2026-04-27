# run-ledger-template-v1

Use this ledger when one stable runbook needs a durable, append-only accounting surface for repeated execution,
evidence admission, review, approval, and downstream consumption.
This ledger owns run-level accounting; it does not replace the runbook, the raw artifacts, or the source log.

## Naming Rule

- Name run ledgers as `ledger-run-<run-sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- `<run-sequence>` is the append-only run number inside one runbook family.
- `<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>` must match the bound runbook suffix exactly.
- Preferred example shape:
  - `ledger-run-001-WORKFLOW-FAMILY-001-operator-surface.md`

## Minimal Header

```yaml
runbook_run_ledger:
  run_ledger_id: <ledger-run-001-RUNBOOK-FAMILY-001-summary>
  ledger_kind: runbook-run-ledger
  status: <draft|active|completed>
  owner_lane: <S0G-2A>
  runbook_family: <RUNBOOK-FAMILY>
  runbook_release: <001>
  runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  runbook_ref: <docs/runbook/run-RUNBOOK-FAMILY-001-summary.md>
  run_sequence: <001>
  governance_area: <workflow|ops-runtime|evidence-pipeline|other>
  functional_domain: <GitHub lifecycle automation>
  environment_class: <local|cloud-dev|ci|mixed>
  target_surface: <what was operated on>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  target_reading_goal: <what later readers should understand after this ledger row is admitted>
```

## Lifecycle Field Rule

- `created_at` records when this run ledger file was created in the repo.
- `reviewed_at` records when the run accounting and admitted evidence first reached defended review state.
- `accepted_at` records when the ledger is accepted as the durable accounting surface for this run.
- `created_at`, `reviewed_at`, and `accepted_at` are required header fields; keep them present even when the defended value is still `unknown` or `pending`.
- These are artifact-lifecycle timestamps only; execution timing belongs in the run-time audit table.

## Run Ledger Table

| run row id | trigger kind | environment | target kind | submitted by | command summary | artifact root | verdict status | review status | approval status | downstream consumption | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001>` | `<workflow_dispatch|manual|task|script|other>` | `<cloud-dev|local|ci|other>` | `<vm|workflow|api|mixed>` | `<unknown|pending|role:operator|name>` | `<stable entrypoint used for this run>` | `<artifacts/...>` | `<pass|fail|pass_after_recovery|partial|not_run>` | `<pending|reviewed|needs-follow-up>` | `<pending|accepted|rejected>` | `<source log or contract that consumed this run>` | `<why this run matters>` |

## Evidence Extraction Table

| evidence item id | run row id | artifact file | evidence type | extraction scope | admitted fields | verification status | used by | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-E01>` | `<RUN-001>` | `<summary.json>` | `<json|log|screenshot|other>` | `<full|partial|excerpt-only>` | `<result; failureClass; runId>` | `<pending|verified|rejected>` | `<S0G-2A/P2 or later consumer>` | `<why these fields were admitted>` |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001>` | `<unknown|pending|role:operator|delegated:workflow-owner|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-artifact-inspection|manual-replay|transcript-comparison|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-ledger|needs-better-evidence|rejected>` | `<why this approval state is currently defended>` | `<why any actor fields remain partial>` |

## Run Time Audit

- This table is required in the template even when one or more values remain `unknown`.

| run row id | run started at | run completed at | source recorded at | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<second|day|unknown>` | `<optional source-local zone note>` | `<why time audit matters for this run>` |

## Run Write-Back Chain Rule

- The auditable run-chain is `run evidence -> run ledger -> source log or contract/runbook consumer`.
- Use a `SUP` packet when later evidence changes the admitted meaning of one run, target, or stage row.
- Use a `PATCH` packet when one bounded repair changes the runbook-owned object under the same stable release; if that repair also changes the admitted reading, pair it with the corresponding `SUP` write-back.
- Readers should be able to tell what changed by comparing the current run row, run-time audit, later SUP or PATCH packets, and any downstream consumer references.

## Required Rules

- One run ledger file should describe one admitted run sequence for one stable runbook family.
- `run row id` is required and should remain stable once admitted.
- `evidence item id` is required for each admitted artifact used by downstream readers.
- Use `unknown`, `pending`, `role:<role-name>`, or `delegated:<role-name>` instead of inventing named actors.
- The ledger may record `partial` or `fail` runs when they are audit-worthy; do not filter them out just because they are not green.
- Raw artifacts remain the source of truth; this ledger records what was admitted, reviewed, and later consumed.

## Completion Rule

- A run ledger may be marked `completed` only when:
  - the run row has one explicit verdict state;
  - every admitted evidence row has one explicit verification status;
  - actor/provenance review state is explicit enough for the packet's claimed audit value.