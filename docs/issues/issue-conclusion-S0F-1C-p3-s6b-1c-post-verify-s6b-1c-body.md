## Metadata

- Labels: `sub/1`, `EVOLUTION`, `s6/evidence & drills`, `drills`
- Projects: `wordloom Board`
- Milestone: `road-002: projection runtime platformization and evidence governance`
- Parent issue: #356

## Context



- This issue continues the migration for the tracked retained-summary coexistence, focusing specifically on the write_gate data family's transition from legacy aliases to a new primary path.
- The new primary path has been designated as artifacts/s2b.write-gate.runs.latest.json, while the legacy alias remains at artifacts/write_gate_runs.latest.json for now.
- A detailed inventory of high-value lookup surfaces has been created to prioritize which entries must migrate immediately and which legacy references can remain temporarily.
- Explicit dual-write and fallback policies are maintained to ensure compatibility during the coexistence period, along with clear stop conditions for retiring the legacy alias.



## Definition of Done (DoD)

- #362

## Links

- Log: `docs/logs/log-S6B-1C-tracked-retained-summary-coexistence-migration.md`
- Roadmap: `docs/roadmap/_draft/road-S2-.md`
- Parent log: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
- Previous log: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
- Roadmap: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`

