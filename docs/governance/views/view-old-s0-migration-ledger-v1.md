# Old S0 Migration Ledger v1

## Purpose

- This view is the reader-facing migration ledger for old-`S0` source surfaces under the `7 families + 6 outlets` model.
- It exists so readers can see the current migration shape without replaying the support-only working ledger row by row.

## Current Model

- Use this view when the question is `what is the current migration standing of the old-S0 backlog?`
- Read each row in this order:
  - `source surface`
  - `current standing`
  - `target family`
  - `target outlet`
  - `target surface`
  - `follow-up owner`
- This view may show:
  - stable current standing
  - the best admitted family and outlet answer
  - the bounded next owner for later execution
- This view must intentionally omit:
  - fast-moving blocker prose
  - provisional alternative target debates
  - long package-local execution notes
  - evidence ledgers that remain owned by source logs

## Migration Summary

- Current state after `S0F-5B/P1-P3`:
  - the repo now has one explicit split between a support-only working ledger and this reader-facing migration view
  - the working-ledger row contract and the reader-facing projection contract are now fixed
- Current state after `S0F-5B/P4`:
  - the first bounded seed set is now admitted as the already-executed first `DOC` migration chain
  - the reader-facing view now exposes real seeded rows rather than only the model shell
  - the next widening step remains a later bounded follow-up, not a whole-series backlog flood into this view
- Current state after `S0F-5B/P4-C2`:
  - the second bounded seed set is now admitted as the first supporting source-owner packet already absorbed by the executed issue-governance `DOC` contracts
  - the migration ledger now distinguishes retained source-owner rows from supporting absorbed rows without reopening the ledger contract itself
- Current state after `S0F-5B/P4-C3`:
  - the third bounded seed set is now admitted as the first source-owner packet already absorbed by the current `DOC` history reader surface
  - the migration ledger now distinguishes supporting rows absorbed by `contract` targets from supporting rows absorbed by `view` targets

## Current Migration Rows

| source surface | current standing | target family | target outlet | target surface | follow-up owner |
| --- | --- | --- | --- | --- | --- |
| `S0F-4A` | `done` | `DOC` | `contract` | `DOC-DRB-0001` | `none (executed)` |
| `S0F-4B` | `done` | `DOC` | `contract` | `DOC-SLC-0001` | `none (executed)` |
| `S0F-3I` | `done` | `DOC` | `contract` | `DOC-TAX-0001` | `none (executed)` |
| `S0F-4C` | `done` | `DOC` | `contract` | `DOC-FDT-0001` | `none (executed)` |
| `S0E-2D` | `done` | `DOC` | `contract` | `DOC-ICR-0001` | `none (executed)` |
| `S0E-2E` | `done` | `DOC` | `contract` | `DOC-ICL-0001` | `none (executed)` |
| `S0E-6C` | `done` | `DOC` | `contract` | `DOC-ICT-0001` | `none (executed)` |
| `S0F-1G` | `done` | `DOC` | `contract` | `DOC-IID-0001` and `DOC-IID-0002` | `none (executed)` |
| `S0F-1A` | `done` | `DOC` | `contract` | `DOC-ICR-0001` | `none (executed)` |
| `S0F-1B` | `done` | `DOC` | `contract` | `DOC-ICT-0001` | `none (executed)` |
| `S0F-1D` | `done` | `DOC` | `contract` | `DOC-ICR-0001` and `DOC-ICL-0001` | `none (executed)` |
| `S0F-4D` | `done` | `DOC` | `view` | `view-doc-history-and-lineage-v1` | `none (executed)` |
| `S0F-4E` | `done` | `DOC` | `view` | `view-doc-history-and-lineage-v1` | `none (executed)` |
| `S0F-4F` | `done` | `DOC` | `view` | `view-doc-history-and-lineage-v1` | `none (executed)` |

## Reader Notes

- This is a current migration view, not the support-only working ledger.
- For blockers, provisional judgments, and row-by-row working notes, use `docs/governance/views/support-only/inventory-old-s0-migration-working-ledger-v1.md`.
- For slice-local reasoning, execution boundaries, and evidence, use `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md` and the later source-owner execution logs.

## Source Refs

- `docs/logs/log-S0F-5B-old-s0-migration-ledger-view-and-support-only-inventory-model.md`
- `docs/governance/views/support-only/inventory-old-s0-migration-working-ledger-v1.md`
- `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`