## Metadata

- Requested ID: `S6B-1C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s6b-1c`
- Source log: `docs/logs/log-S6B-1C-tracked-retained-summary-coexistence-migration.md`
- Labels: `EVOLUTION, s6/evidence & drills, sub/1, drills`
- Development issue: #359

## Summary

- Fix the coexistence contract for the tracked `write_gate` retained-summary family by separating the new primary path from the legacy alias.
- Inventory the high-value lookup surfaces and split immediate primary-path migrations from bounded historical legacy references.
- Retain explicit dual-write, manual fallback, and alias-retirement gates so the tracked rename path can progress without a breaking cutover.

## Execution Checklist

- [x] `P0-C1-S1`: primary and alias boundary fixed
- [x] `P0-C1-S2`: migration unit fixed
- [x] `P1-C1-S1`: high-value lookup surfaces identified
- [x] `P1-C1-S2`: must-migrate versus bounded-legacy references separated
- [x] `P2-C1-S1`: generator write priority fixed
- [x] `P2-C1-S2`: consumer read priority and fallback fixed
- [x] `P3-C1-S1`: dual-write stop conditions fixed
- [x] `P3-C1-S2`: dual-read / alias-reference stop conditions fixed
- [x] `P3-C1-S3`: observation window and rollback boundary fixed

## Links

- Log: `docs/logs/log-S6B-1C-tracked-retained-summary-coexistence-migration.md`
- Parent log: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
- Roadmap: `docs/roadmap/_draft/road-S2-.md`

Closes #359
