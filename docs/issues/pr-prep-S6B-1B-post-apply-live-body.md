## Metadata

- Requested ID: `S6B-1B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s6b-1b`
- Source log: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
- Labels: `EVOLUTION, s6/evidence & drills, sub/1, drills`
- Development issue: #358

## Summary

- Fix the first naming baseline for retained-summary, tmp-scratch, and snapshot run identity so operators can infer surface role before opening file contents.
- Retain a bounded current-to-target rename sample set for `artifacts/`, `_tmp_` / `_local_`, and `docs/labs/_snapshot/**` surfaces instead of leaving naming cleanup at abstract rules only.
- Start the first tracked retained-summary coexistence path by selecting `write_gate` as the candidate family, enabling dual-write, and migrating the first primary lookup surfaces.

## Execution Checklist

- [x] `P0-C1-S1`: naming fields fixed
- [x] `P0-C1-S2`: per-surface grammar split fixed
- [x] `P1-C1-S1`: stable retained-summary grammar fixed
- [x] `P1-C1-S2`: retained-summary anti-patterns fixed
- [x] `P1-C1-S3`: retained-summary examples retained
- [x] `P2-C1-S1`: tmp identity kept visible
- [x] `P2-C1-S2`: tmp anti-confusion rule fixed
- [x] `P2-C1-S3`: tmp examples retained
- [x] `P3-C1-S1`: run identity belongs to directory first
- [x] `P3-C1-S2`: key file role names fixed
- [x] `P3-C1-S3`: snapshot naming anti-patterns fixed
- [x] `P4-C1-S1`: retained-summary sample mappings retained
- [x] `P4-C1-S2`: tmp-scratch sample mappings retained
- [x] `P4-C1-S3`: snapshot run-identity sample mappings retained
- [x] `P4-C1-S4`: bounded sample usage rules fixed
- [x] `P4-C2-S1`: first local bounded rename sample executed
- [x] `P4-C2-S2`: ignored-surface execution boundary fixed
- [x] `P4-C3-S1`: first repo-tracked coexistence candidate selected
- [x] `P4-C3-S2`: tracked coexistence prerequisites fixed
- [x] `P4-C3-S3`: deferred execution boundary fixed
- [x] `P4-C4-S1`: tracked alias/fallback coexistence enabled
- [x] `P4-C4-S2`: primary lookup migration started
- [x] `P4-C4-S3`: tracked coexistence stop-condition boundary retained

## Links

- Log: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
- Parent log: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
- Roadmap: `docs/roadmap/_draft/road-S2-.md`

Closes #358
