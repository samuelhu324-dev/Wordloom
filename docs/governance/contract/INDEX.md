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

## Landing Rule

- A new file belongs here when all of the following are true:
  - it is a `DOC` family contract
  - it is intended to be a stable current rule body rather than a source-owner execution ledger
  - it should be read directly as current family-owned contract text instead of as an old narrow-registry record
  - it can be named under the `DOC-<AREA>-<NNNN>-<summary>.md` family-owned model without pretending to be a `GC-*` record
- A file does not belong here merely because it is documentation.

## Reader Notes

- This directory starts empty on purpose: the first step is to fix the home and entry model before extracting stable rule bodies out of source-owner logs.
- During transition, current `DOC` meaning may still live primarily in source-owner logs such as `S0F-4A`, `S0F-4B`, `S0F-3I`, and `S0F-4C` while this directory becomes the future stable landing surface.
- The first promoted `DOC` contracts should use the admitted area dictionary above rather than reusing `GC-*` prefixes.

## Source Refs

- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
- `docs/governance/contract/_template-doc-contract-record.md`
- `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`