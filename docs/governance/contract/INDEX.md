# DOC Contract Index

## Purpose

- This directory is the new family-owned current contract surface for `DOC`.
- It exists so new `DOC` contracts no longer need to default into the older `docs/governance/contracts/` narrow-registry directory.

## Current Model

- Put new stable current `DOC` contract bodies here.
- Keep `docs/governance/views/` for reader summaries, family front doors, and transition explanations.
- Keep `docs/governance/contracts/` for older narrow-registry records, legacy redirects, and related lineage surfaces until later cleanup explicitly changes that standing.

## Filename Model

- The baseline `DOC` contract filename model is:
  - `DOC-<AREA>-<NNNN>-<summary>.md`
- Example shape:
  - `DOC-DRB-0001-document-role-boundaries-writeback-and-disposition.md`
- Under this model:
  - `DOC` identifies the family-owned current contract surface
  - `<AREA>` identifies one stable `DOC` area
  - `<NNNN>` identifies the sequence inside that area
  - `<summary>` keeps the filename human-scannable without overloading `contract_id`

## Area-Code Dictionary

- New `DOC` area codes are not free-form.
- A new `DOC` area code is admitted only when:
  - the code is added here before first use
  - the code names one stable `DOC` governance area rather than one one-off slice
  - the code is not being borrowed mechanically from old `GC` areas unless the semantics are actually the same
- First admitted `DOC` area codes:
  - `DRB`: document role boundaries, write-back protocol, and disposition model
  - `SLC`: source-log compatibility and weak-structure export discipline
  - `TAX`: taxonomy and placement model
  - `FDT`: family front-door transition and `GC-*` demotion model

## Required Fields

- A `DOC` contract record should expose at least:
  - `record_id`
  - `contract_id`
  - `family`
  - `area`
  - `status`
  - `summary`
  - `primary_source_owner`
  - `applies_to`
  - `enforcement_surface`
  - `violation_semantics`
  - `introduced_by`
  - `last_changed_by`
  - `source_refs`

## Template

- Use `docs/governance/contract/_template-doc-contract-record.md` when creating a new `DOC` family-owned current contract.

## Active Records

- `DOC-DRB-0001`:
  - file: `docs/governance/contract/DOC-DRB-0001-document-role-boundaries-writeback-and-disposition.md`
  - status: `active`
  - current role: first active family-owned `DOC` contract body for document role boundaries, write-back order, and disposition separation
  - retained source-owner traceability: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `DOC-SLC-0001`:
  - file: `docs/governance/contract/DOC-SLC-0001-source-log-compatibility-and-weak-structure-export-discipline.md`
  - status: `active`
  - current role: second active family-owned `DOC` contract body for source-log compatibility and weak-structure export discipline
  - retained source-owner traceability: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `DOC-TAX-0001`:
  - file: `docs/governance/contract/DOC-TAX-0001-governance-contract-taxonomy-and-placement-model.md`
  - status: `active`
  - current role: third active family-owned `DOC` contract body for taxonomy and placement model
  - retained source-owner traceability: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `DOC-FDT-0001`:
  - file: `docs/governance/contract/DOC-FDT-0001-family-front-door-transition-and-gc-demotion-model.md`
  - status: `active`
  - current role: fourth active family-owned `DOC` contract body for family front-door transition and `GC-*` demotion model
  - retained source-owner traceability: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`

## Promotion Path

- Future source-owner `DOC` logs may later promote into family-owned `DOC` contracts here when later mapping extensions are admitted.
- The first executed mapped promotion set is:
  - `S0F-4A` -> `DOC-DRB-0001`
  - `S0F-4B` -> `DOC-SLC-0001`
  - `S0F-3I` -> `DOC-TAX-0001`
  - `S0F-4C` -> `DOC-FDT-0001`
- `DOC-DRB-0001`, `DOC-SLC-0001`, `DOC-TAX-0001`, and `DOC-FDT-0001` are now landed and active under this first mapping set.
- If later mapping extensions are admitted, their source-owner logs remain the current primary sources until those later promotions are executed.

## Landing Rule

- A new file belongs here when all of the following are true:
  - it is a `DOC` family contract
  - it is intended to be a stable current rule body rather than a source-owner execution ledger
  - it should be read directly as current family-owned contract text instead of as an old narrow-registry record
  - it can be named under the `DOC-<AREA>-<NNNN>-<summary>.md` family-owned model without pretending to be a `GC-*` record
- A file does not belong here merely because it is documentation.

## Reader Notes

- This directory no longer starts empty: `DOC-DRB-0001`, `DOC-SLC-0001`, `DOC-TAX-0001`, and `DOC-FDT-0001` are now landed family-owned `DOC` contract records.
- This directory now acts as the active landed contract surface for the first mapped `DOC` quartet.
- `DOC-DRB-0001` has now completed stable close-out review and is the first active family-owned `DOC` contract under this landing surface.
- `DOC-SLC-0001` has now completed stable close-out review and is the second active family-owned `DOC` contract under this landing surface.
- `DOC-TAX-0001` has now completed stable close-out review and is the third active family-owned `DOC` contract under this landing surface.
- `DOC-FDT-0001` has now completed stable close-out review and is the fourth active family-owned `DOC` contract under this landing surface.
- The first mapped `DOC` promotion set is now fully landed as active family-owned current contract bodies.
- The retained source-owner logs for `S0F-4A`, `S0F-4B`, `S0F-3I`, and `S0F-4C` remain lineage and traceability surfaces for those rule sets rather than the strongest current reader entry.
- Later `DOC` mapping extensions, if admitted, may still begin in source-owner logs until their own promotion lanes complete.
- The first promoted `DOC` contracts should use the admitted area dictionary above rather than reusing `GC-*` prefixes.

## Source Refs

- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
- `docs/governance/contract/_template-doc-contract-record.md`
- `docs/governance/views/view-doc-contract-promotion-map-v1.md`
- `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`