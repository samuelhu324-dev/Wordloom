# ISS Split Package v1

## Purpose

- This view explains the executed first bounded migration that split the coarse `ISS` governance area into narrower current areas.
- It exists so readers can inspect the concrete executed mapping and preservation result without treating `INDEX.md` as a mixed current-plus-history ledger.

## Current Model

- The current front door now shows four narrower current issue areas:
  - `ICL`
  - `ICR`
  - `ICT`
  - `IID`
- The old `ISS` namespace no longer acts as a current growth area.
- Old `GC-ISS-*` files remain preserved as deprecated legacy records with deterministic redirects.

## Executed Mapping

- Executed package:
  - `ISS split package v1`
- Descendant current areas:
  - `ICR`: issue creation governance
  - `ICL`: issue conclusion governance
  - `ICT`: issue Context governance
  - `IID`: issue identity governance
- Record mapping:
  - `GC-ISS-0001` -> `GC-ICR-0001`
  - `GC-ISS-0002` -> `GC-ICL-0001`
  - `GC-ISS-0003` -> `GC-ICT-0001`
  - `GC-ISS-0004` -> `GC-IID-0001`
  - `GC-ISS-0005` -> `GC-IID-0002`

## Preservation Status

- Keep all old `GC-ISS-*` file paths in place.
- Keep all old `GC-ISS-*` record IDs valid for historical references.
- Old `GC-ISS-*` files are now preserved historical records with `Legacy Redirect` notes.
- `ISS` is now a frozen legacy area rather than a live current namespace.
- `contract_id` values remain stable across the move so semantic identity is preserved while area-level namespace changes.

## Reader Notes

- This view is a migration and lineage aid, not the current front door.
- `INDEX.md` remains the source of current-state truth for active governance areas.
- Use old `GC-ISS-*` files or this view when you need lineage from the former coarse area to the narrower current areas.

## Source Refs

- `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
- `docs/logs/log-S0F-3D-first-governance-contract-landing-batch.md`
- `docs/governance/contracts/GC-ICR-0001-issue-creation-metadata-english-body.md`
- `docs/governance/contracts/GC-ICL-0001-issue-conclusion-post-merge-linkage.md`
- `docs/governance/contracts/GC-ICT-0001-issue-context-sentence-count-main-vs-child.md`
- `docs/governance/contracts/GC-IID-0001-parent-sidebar-ordering-ownership.md`
- `docs/governance/contracts/GC-IID-0002-issue-title-keyword-controlled-vocabulary.md`
- `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
- `docs/governance/contracts/GC-ISS-0002-issue-conclusion-post-merge-linkage.md`
- `docs/governance/contracts/GC-ISS-0003-issue-context-sentence-count-main-vs-child.md`
- `docs/governance/contracts/GC-ISS-0004-parent-sidebar-ordering-ownership.md`
- `docs/governance/contracts/GC-ISS-0005-issue-title-keyword-controlled-vocabulary.md`