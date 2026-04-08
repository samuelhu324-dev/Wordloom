# doc-contract-record: DOC-TAX-0001

- `record_id`: `DOC-TAX-0001`
- `contract_id`: `GOVERNANCE-CONTRACT-TAXONOMY-AND-PLACEMENT-MODEL`
- `title`: `governance contract taxonomy and placement model stay explicit across current DOC governance surfaces`

```yaml
doc_contract:
  record_id: DOC-TAX-0001
  contract_id: GOVERNANCE-CONTRACT-TAXONOMY-AND-PLACEMENT-MODEL
  family: DOC
  area: TAX
  status: active
  summary: Documentation-governance taxonomy must keep contract family separate from system level, narrow `GC-*` to the registry-admitted governance subset, and prefer primary-SoT-first distributed placement over one fake universal contracts folder.
  primary_source_owner: docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md
  applies_to: documentation-governance taxonomy, family placement reading, family-versus-level interpretation, cross-family inventory reading, and later DOC family contract landing decisions derived from the same taxonomy rule set
  enforcement_surface: taxonomy-facing governance views, source-owner promotion work, and later family front-door or placement decisions
  violation_semantics: warning
  introduced_by: S0F-3I/P0-P5
  last_changed_by: S0F-4E/P3-C3-S1S2
  source_refs:
    - docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md
    - docs/governance/views/view-contract-family-placement-map-v1.md
    - docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the third family-owned DOC contract body promoted out of a source-owner log.
    - S0F-3I remains the retained source-owner traceability log for this rule set after stable close-out review completed under S0F-5A.
    - The placement map remains a supporting view for concrete current-state scanning; this record owns the stable taxonomy and placement rule, not every future directory choice.
```

## Current Rule

- Contract family answers `what kind of contract is this?`
- System level answers `which surface or layer does it affect?`
- These are two different axes and must not collapse into one taxonomy.
- The current seven contract families are:
  - `DOM`
  - `PRO`
  - `INT`
  - `OPS`
  - `SEC`
  - `EVD`
  - `DOC`
- `GC-*` is a narrow current governance-registry vocabulary, not the umbrella name for every important contract in the repo.

## Family And Level Relation

- `S0-S6` remains the affected-level or system-surface map.
- Family answers kind of rule; level answers affected surface.
- Typical affinities are useful, but not one-to-one taxonomy:
  - `DOC` often aligns with `S0`
  - `DOM` often aligns with `S1`
  - `PRO` often aligns with `S2`
  - `OPS` often aligns with `S4`
  - `SEC` often aligns with `S5`
  - `EVD` often aligns with `S6`
  - `INT` commonly spans multiple levels at once

## Primary SoT Placement Rule

- The seven families do not need to collapse into one physical folder.
- The repo should prefer `primary SoT first, cross-link second`.
- Code-first families stay closest to code, schema, tests, workflows, and runtime surfaces.
- Doc-first families stay closest to logs, runbooks, templates, governance docs, and documentation-specific automation.
- A central taxonomy index may point to those surfaces, but must not replace their real primary SoT.

## Placement Guidance

- `DOM` primary SoT normally lives in code, schema, migrations, and domain tests.
- `PRO` primary SoT normally lives in projection code, runtime behavior, replay or rebuild surfaces, tests, and drills.
- `INT` primary SoT normally lives in API, CLI, event, or adapter code plus verification artifacts and tests.
- `OPS` primary SoT normally lives in runbooks, operator scripts, workflow entrypoints, and bounded runtime docs.
- `SEC` primary SoT is often mixed but must still name one lead enforceable surface plus related docs and runbooks.
- `EVD` primary SoT normally lives in evidence schemas, gate scripts, CI workflows, runbooks, and retained artifacts.
- `DOC` primary SoT normally lives in templates, governance docs, runbooks, or documentation-specific automation surfaces.

## Consolidation Threshold

- Do not create one universal contracts folder for all seven families.
- Prefer stronger indexing over physical relocation when:
  - one family already has a clear primary SoT and readers mostly struggle with navigation
  - the family is inherently mixed because enforceable meaning spans code, tests, workflows, and artifacts together
  - relocation would create a weaker second copy instead of clarifying ownership
- Consider a real family hub or reorganization only when:
  - readers repeatedly fail to find the authoritative surface for the same family
  - one family grows too many parallel front doors to scan cheaply
  - multiple files begin restating the same rule without one clear primary owner

## Reader Notes

- This file is the third active family-owned current contract body mapped from `S0F-3I`.
- `S0F-3I` remains the retained source-owner traceability log for lineage, evidence, and concentrated historical source context, but current reader-facing rule ownership now reads here.
- The placement map at `docs/governance/views/view-contract-family-placement-map-v1.md` remains the descriptive current-state scan that helps readers answer where families live today.
- Stable close-out review for the third promotion lane has completed under `S0F-5A`, and no bounded post-stable export tail was required.

## Traceability

- Source-owner log:
  - `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- Supporting placement view:
  - `docs/governance/views/view-contract-family-placement-map-v1.md`
- Promotion lane:
  - `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`