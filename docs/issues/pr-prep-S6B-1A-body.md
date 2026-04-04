## Metadata

- Requested ID: `S6B-1A`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s6b-1a`
- Source log: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
- Labels: `EVOLUTION, s6/evidence & drills, sub/1, drills`
- Development issue: #357

## Summary

- Retain the first repo-level evidence inventory ledger across `human-ledger`, `fact-source`, `retained-summary`, `workflow-derived`, `tmp-scratch`, and `evidence-lite` surfaces.
- Fix the current retention and storage baseline so `artifacts`, `docs/issues`, and `docs/labs/_snapshot` no longer rely on one implicit evidence bucket.
- Record the current generator/emission policy and bounded cutover order so later `S6B` cleanup can reuse one stable owner-and-migration contract.

## Execution Checklist

- [x] `P0-C1-S1`: inventory columns fixed
- [x] `P0-C1-S2`: scale baseline rule fixed
- [x] `P0-C1-S3`: family-level granularity fixed
- [x] `P0-C1-S4`: primary owner discipline fixed
- [x] `P1-C1-S1`: repo evidence total table retained
- [x] `P1-C1-S2`: current scale baseline retained
- [x] `P1-C1-S3`: family owner map retained
- [x] `P2-C1-S1`: class-to-retention baseline fixed
- [x] `P2-C1-S2`: surface-specific retained versus tmp policy fixed
- [x] `P2-C1-S3`: operator storage shortcuts fixed
- [x] `P2-C1-S4`: hotspot list retained
- [x] `P3-C1-S1`: fact-source emission boundary fixed
- [x] `P3-C1-S2`: retained-summary and workflow-derived emission boundary fixed
- [x] `P3-C1-S3`: naming and ownership expectations fixed
- [x] `P4-C1-S1`: bounded rollout order fixed
- [x] `P4-C1-S2`: coexistence rules fixed
- [x] `P4-C1-S3`: stop conditions fixed

## Links

- Log: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
- Parent log: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
- Roadmap: `docs/roadmap/_draft/road-S2-.md`

Closes #357
