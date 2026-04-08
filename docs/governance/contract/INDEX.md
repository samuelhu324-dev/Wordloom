# DOC Contract Index

## Purpose

- This directory is the new family-owned current contract surface for `DOC`.
- It exists so new `DOC` contracts no longer need to default into the older `docs/governance/contracts/` narrow-registry directory.

## Current Model

- Put new stable current `DOC` contract bodies here.
- Keep `docs/governance/views/` for reader summaries, family front doors, and transition explanations.
- Keep `docs/governance/contracts/` for older narrow-registry records, legacy redirects, and related lineage surfaces until later cleanup explicitly changes that standing.

## Landing Rule

- A new file belongs here when all of the following are true:
  - it is a `DOC` family contract
  - it is intended to be a stable current rule body rather than a source-owner execution ledger
  - it should be read directly as current family-owned contract text instead of as an old narrow-registry record
- A file does not belong here merely because it is documentation.

## Reader Notes

- This directory starts empty on purpose: the first step is to fix the home and entry model before extracting stable rule bodies out of source-owner logs.
- During transition, current `DOC` meaning may still live primarily in source-owner logs such as `S0F-4A`, `S0F-4B`, `S0F-3I`, and `S0F-4C` while this directory becomes the future stable landing surface.

## Source Refs

- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
- `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`