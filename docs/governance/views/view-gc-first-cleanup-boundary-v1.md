# GC First Cleanup Boundary v1

## Purpose

- This view fixes the first concrete cleanup boundary for old `GC-*` files after the triage and retention rule was established.
- It exists so later cleanup rounds do not reopen the keep-versus-relocate question for the already-adjudicated first old-`GC-*` subset.

## Boundary Summary

- Keep in `docs/governance/contracts/` root:
  - current narrow-registry records that still appear in `docs/governance/INDEX.md`
  - preserved legacy redirect records whose old root path is still part of the reader contract
- Keep in `docs/governance/contracts/support-only/`:
  - whole-file support-only backtrace notes whose current job is bounded historical traceability rather than root-path redirect reading
- Do not open a new relocation round for old `GC-*` files unless one file has already lost both current-registry standing and root-path redirect duty.

## First Adjudicated Old-GC Subset

### Keep Legacy At Root

- The first preserved legacy redirect set now fixed to remain at the contracts root is:
  - `GC-ISS-0001`
  - `GC-ISS-0002`
  - `GC-ISS-0003`
  - `GC-ISS-0004`
  - `GC-ISS-0005`
  - `GC-PRB-0001`
- Reason:
  - these files still preserve deterministic old-ID lineage and still act as the intended redirect landing surface for readers who arrive through the former namespace

### First Support-Only Exception

- The first old-`GC-*` support-only exception already fixed to remain outside the root is:
  - `docs/governance/contracts/support-only/GC-PRB-0001-backfill-historical-drift-fail-on-findings.md`
- Reason:
  - this file no longer acts as the primary redirect landing path
  - its retained value is bounded backtrace support for the deprecated umbrella `GC-PRB-0001` and its split successors
  - direct discoverability is already preserved through the support-only contracts index and explicit references

## Immediate Consequence

- `GC-ISS-*` and `GC-PRB-0001` should not be proposed again as relocation candidates merely because they are deprecated.
- The existing support-only backfill note should not be pulled back to root merely because it shares the same semantic family as `GC-PRB-0001`.
- Later cleanup should instead look for a new subset where the old root path no longer contributes current reader value.

## Stop Rule

- Stop any future old-`GC-*` relocation proposal if it would:
  - weaken a preserved old-ID redirect path
  - make lineage reading depend on reconstructing history from logs alone
  - mix current registry rows with support-only backtrace handling in the same move round

## Reader Notes

- This is a boundary view, not a new registry.
- It does not replace `docs/governance/INDEX.md`.
- It records the first already-defended answer to `which old GC files stay root-readable and which ones already belong to support-only?`

## Source Refs

- `docs/governance/INDEX.md`
- `docs/governance/contracts/support-only/INDEX.md`
- `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
- `docs/governance/contracts/GC-ISS-0002-issue-conclusion-post-merge-linkage.md`
- `docs/governance/contracts/GC-ISS-0003-issue-context-sentence-count-main-vs-child.md`
- `docs/governance/contracts/GC-ISS-0004-parent-sidebar-ordering-ownership.md`
- `docs/governance/contracts/GC-ISS-0005-issue-title-keyword-controlled-vocabulary.md`
- `docs/governance/contracts/GC-PRB-0001-historical-drift-fail-on-findings.md`
- `docs/governance/contracts/support-only/GC-PRB-0001-backfill-historical-drift-fail-on-findings.md`
- `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
- `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`