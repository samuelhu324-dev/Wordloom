# Old S0 Migration Working Ledger v1

## Purpose

- This support-only inventory is the continuously revisable working ledger for old-`S0` migration review under the `7 families + 6 outlets` model.
- It exists so later migration lanes can update one shared row set for blockers, provisional judgments, and follow-up ownership without rewriting those fast-moving details into source-owner logs or reader-facing views.

## Working-Ledger Model

- Use this inventory when the question is `what is the current working state of this migration row?`
- A row may change many times before execution closes.
- This file is allowed to carry:
  - provisional family guesses
  - candidate outlet choices
  - blocker notes
  - deferred follow-up ownership
  - execution status churn across later bounded lanes
- This file must not be treated as the current rule SoT, current family front door, or the replacement for source-owner execution logs.

## Row Contract

| field | job |
| --- | --- |
| `source surface` | exact source-owner log or bounded source cluster under review |
| `current standing` | working-ledger state for this row |
| `candidate family` | best current family answer under the seven-family model |
| `candidate outlet` | best current outlet answer under the six-outlet model |
| `action type` | `add`, `update`, `merge`, `split`, `retain`, or `no-op` |
| `target surface` | candidate current contract, view, runbook, front-door, or retained-log target |
| `blocker` | lowest-cardinality reason the row cannot advance yet |
| `follow-up owner` | bounded lane or current owner expected to advance the row |
| `notes` | short working note needed to understand the current row state |

## Standing Values

- `unreviewed`:
  - no bounded migration judgment has been written yet
- `provisional`:
  - one first-pass answer exists, but family, outlet, or action still remains open enough that readers should not treat the row as settled
- `admitted`:
  - the row is admitted into one bounded action shape, but execution has not yet landed
- `blocked`:
  - the row cannot advance because one explicit blocker still prevents defended execution or no-op close-out
- `deferred`:
  - the row is not wrong, but it is intentionally held for a later bounded lane instead of advancing now
- `done`:
  - the migration result is executed or the no-op result is fully defended

## Row Semantics

- `provisional` does not mean `nearly done`; it means the working answer is still too unstable for reader-facing projection.
- `blocked` should name the missing condition, not retell the whole slice history.
- `deferred` should point to one bounded next owner instead of becoming an orphan backlog bucket.
- `done` may still mean `retain source log` or `no-op` when that outcome is the defended result.

## Current Ledger State

- `S0F-5B/P4` now admits the first bounded seed set as the already-executed first `DOC` migration chain.
- The first seed set is intentionally narrow:
  - first `DOC` source-owner quartet promoted under `S0F-4E`
  - first issue-governance source-owner packet promoted under `S0F-4I`
- Wider old-`S0` population remains a later bounded follow-up after this initial seed packet proves the shared ledger shape on real rows.

## Working Rows

| source surface | current standing | candidate family | candidate outlet | action type | target surface | blocker | follow-up owner | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0F-4A` | `done` | `DOC` | `contract` | `add` | `DOC-DRB-0001` | `` | `none (executed)` | `first source-owner quartet row; active rule now reads through DOC current contract while the log remains retained traceability` |
| `S0F-4B` | `done` | `DOC` | `contract` | `add` | `DOC-SLC-0001` | `` | `none (executed)` | `source-log compatibility rule now reads through DOC current contract while the log remains retained traceability` |
| `S0F-3I` | `done` | `DOC` | `contract` | `add` | `DOC-TAX-0001` | `` | `none (executed)` | `taxonomy and placement rule now reads through DOC current contract while the log remains retained traceability` |
| `S0F-4C` | `done` | `DOC` | `contract` | `add` | `DOC-FDT-0001` | `` | `none (executed)` | `family-front-door transition rule now reads through DOC current contract while the log remains retained traceability` |
| `S0E-2D` | `done` | `DOC` | `contract` | `add` | `DOC-ICR-0001` | `` | `none (executed)` | `issue-creation source-owner row admitted through the first executed issue-governance packet` |
| `S0E-2E` | `done` | `DOC` | `contract` | `add` | `DOC-ICL-0001` | `` | `none (executed)` | `issue-conclusion source-owner row admitted through the first executed issue-governance packet` |
| `S0E-6C` | `done` | `DOC` | `contract` | `add` | `DOC-ICT-0001` | `` | `none (executed)` | `issue-context source-owner row admitted through the first executed issue-governance packet` |
| `S0F-1G` | `done` | `DOC` | `contract` | `split` | `DOC-IID-0001` and `DOC-IID-0002` | `` | `none (executed)` | `one source-owner log now reads through two DOC issue-identity contracts under one shared execution packet` |

## Source Refs

- `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
- `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`