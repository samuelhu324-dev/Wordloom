## Metadata

- Requested ID: `S0F-1E`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-1e`
- Source log: `docs/logs/log-S0F-1E-completeness-classification-buckets-and-audit-output-taxonomy.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #369

## Summary

- Create one explicit taxonomy for lifecycle completeness buckets so audit output can name stage-local failure classes rather than only generic gate states.
- Define how existing read-only planners should expose bucketed completeness findings without breaking the current decision-layer status fields.
- Prepare the next follow-up path for deterministic audit-output consumption by remediation planning or review tooling.

## Execution Checklist

- [x] `P0-C1-S1`: `S0F-1E` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: decision-layer versus diagnosis-layer boundary fixed
- [x] `P1-C1-S1`: creation-stage bucket families fixed
- [x] `P1-C1-S2`: representative creation checks mapped to bucket labels
- [x] `P2-C1-S1`: PR-stage bucket families fixed
- [x] `P2-C1-S2`: representative PR checks mapped to bucket labels
- [x] `P3-C1-S1`: conclusion-stage bucket families fixed
- [x] `P3-C1-S2`: representative conclusion checks mapped to bucket labels
- [x] `P4-C1-S1`: representative bucketed audit-output sample retained

## Links

- Log: `docs/logs/log-S0F-1E-completeness-classification-buckets-and-audit-output-taxonomy.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

Closes #369
