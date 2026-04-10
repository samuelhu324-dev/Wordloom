# docs/governance/contracts support-only historical contracts

- This directory is the relocation surface for `docs/governance/contracts/` files whose whole-file standing has already been reduced to support-only historical or backtrace value by a bounded cleanup decision.
- `docs/governance/contracts/` root remains the current and preserved-legacy contract surface.
- Whole-file support-only backtrace notes may move here once a cleanup round proves that discoverability is preserved through direct reference rewrites and explicit local navigation rather than through root-level co-location.
- `current narrow-registry` files do not move here.
- `legacy redirect` files also do not move here by default, because their main value is that the old root path itself remains readable as a redirect surface.
- Only files whose standing is already reduced to `support-only history or backtrace` should be considered relocation candidates for this directory.

## Current Members

- `GC-ISS-0001-issue-creation-metadata-english-body.md`
- `GC-PRB-0001-backfill-historical-drift-fail-on-findings.md`

## Navigation Rule

- When a relocated support-only contract backtrace is still cited by governance views, cleanup ledgers, or registry-model logs, those references should point here directly rather than relying on implied historical root paths.
- If a reader still needs the old root path as the primary redirect entrypoint, the file should remain in `docs/governance/contracts/` instead of moving here.