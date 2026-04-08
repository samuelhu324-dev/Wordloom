# Disposition Role In Family Transition v1

## Purpose

- This view explains what `disposition/placement` does during the family-first transition.
- It exists so readers stop asking disposition to answer family ownership or current front-door questions that it does not actually own.

## Current Model

- Read `disposition` as the standing and placement layer.
- It answers questions such as:
  - is this surface current, legacy, support-only, deprecated, superseded, or retired?
  - should this file stay in place, move to support-only, or remain as a redirect?
- It does not answer the first-order questions:
  - what family does this contract belong to?
  - where should a reader go first for current meaning?

## Standing Examples

- `current family-owned`:
  - `S0F-4A`, `S0F-4B`, `S0F-3I`, and `S0F-4C` currently read this way inside the `DOC` family
- `legacy redirect`:
  - preserved `GC-ISS-*` records and `GC-PRB-0001` remain useful as redirect or lineage surfaces
- `support-only history`:
  - helper views under `docs/governance/views/support-only/` and contract backtraces under `docs/governance/contracts/support-only/`
- `current registry-admitted`:
  - active rows still listed in `docs/governance/INDEX.md`

## Reader Notes

- If you need family meaning, use the family front door first.
- If you need standing or cleanup state, use disposition.
- If a surface is `legacy` or `support-only`, that does not by itself mean it stopped belonging to its family; it only means the reader should not treat that file as the primary current front door.

## Source Refs

- `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-ops-current-front-door-v1.md`
- `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`