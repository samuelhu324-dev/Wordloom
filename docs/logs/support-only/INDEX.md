# docs/logs support-only historical logs

- This directory is the relocation surface for `docs/logs/` files whose whole-file standing has already been reduced to support-only historical value by a bounded cleanup decision.
- `docs/logs/` root remains the current-log and parent-spine surface.
- Mixed-standing logs stay at the root until a later cleanup round proves that whole-file relocation would not collapse current-adjacent meaning or break reader discoverability.

## Scope Buckets

- `s0/`
  - `log-S0F-1E-completeness-classification-buckets-and-audit-output-taxonomy.md`
  - `log-S0F-1F-bucketed-audit-output-materialization.md`

## Navigation Rule

- When a relocated support-only log is still cited by parent spines, sweep views, or adjacent historical child logs, those references should point here directly rather than relying on implied legacy paths.