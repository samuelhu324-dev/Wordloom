# GC Dual-Reading Transition v1

## Purpose

- This view explains how old `GC-*` identifiers should be read during the family-first transition.
- It exists so readers can keep historical lineage and stored record IDs without continuing to treat `GC-*` as the name of the whole contract universe.

## Current Model

- Read `GC-*` in two layers:
  - `storage or lineage layer`: old or current registry record identifiers that remain useful for traceability, redirects, and stable file references
  - `reader layer`: family-first current meaning that should now be read through `DOC`, `OPS`, or other family front doors when those exist
- Under this model:
  - `GC-*` may remain on disk
  - `GC-*` may remain in historical references
  - `GC-*` no longer needs to be the first reader vocabulary for every important contract

## Dual-Reading Rule

- If the question is `what family is this contract?`, answer with `DOC / OPS / DOM / PRO / INT / SEC / EVD`.
- If the question is `what is the stored registry record or historical redirect path?`, answer with the relevant `GC-*` identifier when one exists.
- If the question is `where should I read current meaning first?`, prefer the family current front door over the old registry prefix whenever a family front door has already been published.

## Current Examples

- `DOC` current reading:
  - start at `docs/governance/views/view-doc-current-front-door-v1.md`
  - do not ask first whether `S0F-4A`, `S0F-4B`, or `S0F-3I` already have a `GC-*` record
- `OPS` current reading:
  - start at `docs/governance/views/view-ops-current-front-door-v1.md`
  - do not compress `S4A`, `S4D`, and `S4E` into one narrow governance-registry question before reading their active meaning
- narrow governance registry reading:
  - use `docs/governance/INDEX.md` when the question is specifically about current governance-registry records that still live inside that registry model

## Reader Notes

- This is a transition rule, not a mass-renaming command.
- A contract may have no `GC-*` record and still be a current contract if its family front door and source-owner SoT are already explicit.
- Later cleanup may still rename or repackage some storage identifiers, but that is not required for family-first current reading to begin now.

## Source Refs

- `docs/governance/INDEX.md`
- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-ops-current-front-door-v1.md`
- `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`