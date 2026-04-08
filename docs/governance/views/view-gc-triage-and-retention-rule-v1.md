# GC Triage And Retention Rule v1

## Purpose

- This view explains how old `GC-*` files should be triaged after the family-first transition.
- It exists so readers can decide whether an old governance-contract file stays in the contracts root, stays there as a redirect, or becomes eligible for later support-only relocation without collapsing all old files into one archive bucket.

## Three Buckets

- `current narrow-registry`:
  - a record still admitted by `docs/governance/INDEX.md` as part of the current governance-registry reading surface
  - these files still solve a current governance question directly and therefore remain in `docs/governance/contracts/`
- `legacy redirect`:
  - a preserved old record whose main current value is stable lineage, old-ID continuity, or redirecting the reader to a newer current record
  - these files also remain in `docs/governance/contracts/` because the old root path is part of their value
- `support-only history or backtrace`:
  - a file kept only for bounded historical explanation, cleanup traceability, or backtrace value after current reading and redirect needs already moved elsewhere
  - these files may later relocate into `docs/governance/contracts/support-only/` once direct references are rewritten and local discoverability remains explicit

## Retention Rule

- Do not decide by age alone.
- Keep a file in `docs/governance/contracts/` root when either of these is still true:
  - it is listed as a current row in `docs/governance/INDEX.md`
  - the old root path is still the intended first redirect landing surface for lineage-safe reading
- Consider support-only relocation only when all of these are true:
  - the file is no longer a current registry-admitted row
  - the file is no longer needed as the primary redirect landing path
  - direct references can point to the new support-only location without weakening reader discoverability
  - the move is executed by a bounded cleanup decision rather than by opportunistic folder tidying

## Practical Examples

- `current narrow-registry`:
  - active records such as `GC-ICR-0001`, `GC-ICT-0001`, and `GC-PRG-0001` remain current registry rows and stay in the contracts root
- `legacy redirect`:
  - preserved old split-package records such as `GC-ISS-0001` through `GC-ISS-0005` remain readable at the old root path because they redirect readers toward the later `ICR`, `ICL`, `ICT`, and `IID` surfaces
- `support-only history or backtrace`:
  - bounded historical backtrace notes such as the already relocated `GC-PRB-0001-backfill-historical-drift-fail-on-findings.md` can live under `docs/governance/contracts/support-only/` once the redirect need is gone and direct references are explicit

## Reader Notes

- `legacy redirect` is not the same as `support-only history`.
- A deprecated file may still deserve the root path if its redirect value is still active.
- A file should not move to support-only merely because a newer contract exists somewhere else.
- The first question is not `is this old?`; it is `what standing does this file still serve for current readers?`
- For the first concrete old-`GC-*` cleanup boundary already fixed under this rule, read `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`.

## Source Refs

- `docs/governance/INDEX.md`
- `docs/governance/contracts/support-only/INDEX.md`
- `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
- `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- `docs/governance/views/view-disposition-role-in-family-transition-v1.md`
- `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`