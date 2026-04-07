# docs/governance/contracts support-only historical contracts

- This directory is the relocation surface for `docs/governance/contracts/` files whose whole-file standing has already been reduced to support-only historical or backtrace value by a bounded cleanup decision.
- `docs/governance/contracts/` root remains the current and preserved-legacy contract surface.
- Whole-file support-only backtrace notes may move here once a cleanup round proves that discoverability is preserved through direct reference rewrites and explicit local navigation rather than through root-level co-location.

## Current Members

- `GC-PRB-0001-backfill-historical-drift-fail-on-findings.md`

## Navigation Rule

- When a relocated support-only contract backtrace is still cited by governance views, cleanup ledgers, or registry-model logs, those references should point here directly rather than relying on implied historical root paths.