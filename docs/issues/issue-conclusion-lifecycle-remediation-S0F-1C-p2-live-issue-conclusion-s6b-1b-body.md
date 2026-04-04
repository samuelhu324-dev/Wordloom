## Metadata

- Labels: `sub/1`, `EVOLUTION`, `s6/evidence & drills`, `drills`
- Projects: `wordloom Board`
- Milestone: `road-002: projection runtime platformization and evidence governance`
- Parent issue: #356

## Context



- This issue builds on the previous baseline established in S6B-1A to improve evidence naming clarity for key categories like retained-summary, tmp-scratch, and snapshot run identity files.
- The main goal is to establish a naming baseline that enables operators to infer the file's family, owner, usage, and retention status directly from its name without inspecting file contents.
- Key naming updates include explicit fields in retained-summary files under artifacts/, clear tmp identity in _tmp_ and _local_ scratch outputs, and directory-focused run identities in docs/labs/_snapshot/**.
- A bounded rename sample set was created to anchor current-to-target name mappings, providing concrete examples to guide future name standardization and avoid ambiguous or generic file names.



## Definition of Done (DoD)

- #361

## Links

- Log: `docs/logs/log-S6B-1B-evidence-naming-baseline.md`
- Roadmap: `docs/roadmap/_draft/road-S2-.md`
- Parent log: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
- Previous log: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
- Roadmap: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`

