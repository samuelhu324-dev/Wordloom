# ISS Split Package v1

## Purpose

- This view explains the first bounded migration package that will later split the coarse `ISS` governance area into narrower current areas.
- It exists so readers can inspect the concrete target mapping and preservation rules without treating `INDEX.md` as a mixed current-plus-history ledger.

## Current Model

- The current front door still shows one active `ISS` area containing five active records.
- Those five records already span multiple narrower governance surfaces:
  - issue creation
  - issue conclusion
  - issue Context
  - issue identity
- The migration package keeps current semantics intact while changing the namespace shape used for future current growth.

## Migration Package

- Package name:
  - `ISS split package v1`
- Target descendant areas:
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

## Preservation Rules

- Keep all old `GC-ISS-*` file paths in place.
- Keep all old `GC-ISS-*` record IDs valid for historical references.
- Mark old `GC-ISS-*` files as preserved historical records with `Legacy Redirect` notes after successor records are published.
- Keep `contract_id` values stable across the move so semantic identity is preserved while area-level namespace changes.

## Reader Notes

- This view is a migration and lineage aid, not the current front door.
- Until the package is actually executed, `INDEX.md` remains the source of current-state truth.
- After execution, `ISS` should become a frozen legacy area rather than continue as a live current namespace.

## Source Refs

- `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
- `docs/logs/log-S0F-3D-first-governance-contract-landing-batch.md`
- `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
- `docs/governance/contracts/GC-ISS-0002-issue-conclusion-post-merge-linkage.md`
- `docs/governance/contracts/GC-ISS-0003-issue-context-sentence-count-main-vs-child.md`
- `docs/governance/contracts/GC-ISS-0004-parent-sidebar-ordering-ownership.md`
- `docs/governance/contracts/GC-ISS-0005-issue-title-keyword-controlled-vocabulary.md`