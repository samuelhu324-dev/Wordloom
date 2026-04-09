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
- Current state after `S0F-5B/P4-C4`:
  - the fourth bounded seed set is now admitted as the second source-owner packet already absorbed by that same `DOC` history reader surface
  - the migration ledger now proves that one executed reader-facing `view` target may accumulate multiple defended source-owner subpackets without collapsing them into one generic history bucket
- Current state after `S0F-5B/P4-C5`:
  - the fifth bounded seed set is now admitted as the first source-owner execution lane already absorbed by the current `DOC` promotion-map reader surface
  - the migration ledger now shows two distinct `DOC` reader-facing `view` targets participating in old-`S0` absorption: one history surface and one promotion-map surface
- Current state after `S0F-5B/P4-C6`:
  - the sixth bounded seed set is now admitted as the third source-owner packet already absorbed by the current `DOC` history reader surface
  - the migration ledger now shows that the `DOC` history reader surface absorbs both lineage milestones and its own history-publication gate, while remaining separated from the promotion-map surface

## DOC Absorption Snapshot

- Current `S0 -> DOC` absorption rows tracked here: `18`
- Rows absorbed into current `DOC` contract targets: `11`
- Rows absorbed into current `DOC` reader-facing `view` targets: `7`
- Current `DOC` `view` targets now represented here:
  - `view-doc-history-and-lineage-v1`: `6` rows (`S0F-4D`, `S0F-4E`, `S0F-4F`, `S0E-3A`, `S0E-6A`, `S0F-4G`)
  - `view-doc-contract-promotion-map-v1`: `1` row (`S0F-4I`)
- Read this view as the current migration answer to `which old S0 surfaces are already absorbed into DOC, and through which current outlet do they now read?`

## Grouped DOC Reading

- Use this section when the question is not `what are all the rows?` but `which DOC reading surface should I open first?`
- The row table below remains the canonical bounded projection.

## Reader Decision Block

- Start here when you have a concrete question and want one first-open surface immediately.
- `what is true now?`
  - open first: `view-doc-current-front-door-v1`
  - why: this is the current family-first `DOC` entrypoint for active rule reading
- `how did this DOC surface emerge?`
  - open first: `view-doc-history-and-lineage-v1`
  - why: this is the bounded family history surface for lineage, evolution chain, and history-publication context
- `which lane or packet landed this DOC result?`
  - open first: `view-doc-contract-promotion-map-v1`
  - why: this is the current promotion-map surface for bounded landing packets and source-owner-to-contract mapping
- `where is the full migration inventory?`
  - open first: `view-old-s0-migration-ledger-v1` row table below
  - why: this remains the canonical bounded projection of already-admitted old-`S0 -> DOC` absorption rows

### Contract-First DOC Reading

- Count: `11`
- Use this group when the question is `what is true now for this rule set under DOC?`
- Open first:
  - `view-doc-current-front-door-v1`
- Then open:
  - the listed `DOC-*` contract body for the exact area you need
  - the retained source-owner log only if you need detailed chronology or evidence
- Open the active `DOC` contract body first when the old `S0` surface now reads as current rule meaning:
  - `S0F-4A` -> `DOC-DRB-0001`
  - `S0F-4B` -> `DOC-SLC-0001`
  - `S0F-3I` -> `DOC-TAX-0001`
  - `S0F-4C` -> `DOC-FDT-0001`
  - `S0E-2D` -> `DOC-ICR-0001`
  - `S0E-2E` -> `DOC-ICL-0001`
  - `S0E-6C` -> `DOC-ICT-0001`
  - `S0F-1G` -> `DOC-IID-0001` and `DOC-IID-0002`
  - `S0F-1A` -> `DOC-ICR-0001`
  - `S0F-1B` -> `DOC-ICT-0001`
  - `S0F-1D` -> `DOC-ICR-0001` and `DOC-ICL-0001`

### History-View DOC Reading

- Count: `6`
- Use this group when the question is `how did this current DOC surface emerge or why does it read this way now?`
- Open first:
  - `view-doc-history-and-lineage-v1`
- Then open:
  - the retained source-owner log only if you need full chronology, detailed evidence, or the exact publication gate rationale
- Open `view-doc-history-and-lineage-v1` first when the old `S0` surface now reads as lineage, history, or history-publication context:
  - `S0F-4D`
  - `S0F-4E`
  - `S0F-4F`
  - `S0E-3A`
  - `S0E-6A`
  - `S0F-4G`

### Promotion-Map DOC Reading

- Count: `1`
- Use this group when the question is `which bounded source-owner lane or cluster landed into which DOC packet or contract target?`
- Open first:
  - `view-doc-contract-promotion-map-v1`
- Then open:
  - the landed current `DOC` contract body or `view-doc-current-front-door-v1` if you need the current reading surface after the mapping answer
- Open `view-doc-contract-promotion-map-v1` first when the old `S0` surface now reads as a bounded promotion packet or landing map:
  - `S0F-4I`

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
| `S0E-3A` | `done` | `DOC` | `view` | `view-doc-history-and-lineage-v1` | `none (executed)` |
| `S0E-6A` | `done` | `DOC` | `view` | `view-doc-history-and-lineage-v1` | `none (executed)` |
| `S0F-4I` | `done` | `DOC` | `view` | `view-doc-contract-promotion-map-v1` | `none (executed)` |
| `S0F-4G` | `done` | `DOC` | `view` | `view-doc-history-and-lineage-v1` | `none (executed)` |

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