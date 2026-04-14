# doc-contract-record: DOC-FDT-0001

- `record_id`: `DOC-FDT-0001`
- `contract_id`: `FAMILY-FRONT-DOOR-TRANSITION-AND-GC-DEMOTION-MODEL`
- `title`: `family-first front-door transition and GC demotion stay explicit across current DOC governance surfaces`

```yaml
doc_contract:
  record_id: DOC-FDT-0001
  contract_id: FAMILY-FRONT-DOOR-TRANSITION-AND-GC-DEMOTION-MODEL
  family: DOC
  area: FDT
  status: active
  summary: Current reader-facing governance meaning must be family-first, keep family versus front door versus disposition separate, and demote `GC-*` to legacy-registry lineage vocabulary instead of the umbrella contract universe.
  primary_source_owner: docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md
  applies_to: DOC-family current reading, front-door transition decisions, GC demotion and dual-reading policy, DOC and OPS front-door interpretation, and later legacy-registry cleanup decisions derived from the same rule set
  enforcement_surface: governance front-door views, transition views, source-owner promotion work, and later family-first contract landing decisions
  violation_semantics: warning
  introduced_by: S0F-4C/P0-P4
  last_changed_by: S0F-4E/P3-C4-S1S2
  source_refs:
    - docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md
    - docs/governance/views/view-doc-current-front-door-v1.md
    - docs/governance/views/view-ops-current-front-door-v1.md
    - docs/governance/views/view-gc-dual-reading-transition-v1.md
    - docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md
  supersedes: []
  superseded_by: []
  notes:
    - This file is the fourth family-owned DOC contract body promoted out of a source-owner log.
    - S0F-4C remains the retained source-owner traceability log for this rule set after fourth-lane stable close-out review completed under S0F-5A.
    - The published DOC front door, OPS front door, and GC dual-reading view remain supporting reader surfaces; this record owns the stable transition rule, not every future summary variant.
```

## Current Rule

- Family answers what kind of contract a surface is.
- Front door answers where a current reader should look first.
- Disposition answers current standing such as `current`, `legacy`, or `support-only`.
- These are three different questions and must not be collapsed into one registry-first label.

## GC Demotion Rule

- `GC-*` is no longer the umbrella name for the whole contract universe.
- During transition, `GC-*` remains valid as one narrow legacy-registry and lineage vocabulary.
- Old storage identifiers may remain on disk while current reader-facing interpretation moves to family-first front doors.

## Family-First Reading Rule

- A contract may remain family-owned and current without first becoming a legacy-style registry record.
- Current reading should start from the family front door where one already exists.
- `DOC` and `OPS` are the first families to receive explicit front-door treatment because they are the most reader-facing and the most easily distorted by old registry-first wording.

## Dual-Reading Transition Rule

- During the transition period, preserve lineage-safe storage identifiers and family-first current reading together.
- Under this model:
  - family front doors become the first reader vocabulary for current meaning
  - `docs/governance/INDEX.md` remains a valid narrow registry landing surface
  - supporting views may explain current versus legacy interpretation without replacing the stable contract rule
- The goal is to change reader behavior before any later mass rename or cleanup decision.

## Disposition Boundary

- Disposition may say `legacy`, `support-only`, `deprecated`, or `current family-owned`.
- Disposition helps standing and cleanup decisions.
- Disposition does not replace family classification or current front-door ownership.

## Compact History

- `Current source-owner origin`:
  - `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- `Why this current contract exists`:
  - the repo needed one stable current rule surface for family-first reading so `GC-*` could stop acting like the umbrella contract universe while lineage-safe storage and transition notes remained explicit
- `Major evolution chain`:
  - `S0F-4C` fixed the family versus front-door versus disposition split and the first `GC-*` demotion rule
  - `S0F-4D` fixed the current `DOC` contract home that could hold this transition rule directly
  - `S0F-4E` promoted that transition rule into `DOC-FDT-0001`
  - `S0F-4F` consolidated the steady-state `DOC` front door and promotion-map split that this contract now governs
- `Read history in full`:
  - start at `docs/governance/views/view-doc-history-and-lineage-v1.md`
  - then open `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md` for detailed chronology and evidence
- `Cleanup dependency`:
  - the retained source-owner log stays protected as detailed chronology until a later history-aware cleanup review confirms that this compact block plus the lineage view are sufficient for first-pass historical reading

## Reader Notes

- This file is the fourth active family-owned current contract body mapped from `S0F-4C`.
- `S0F-4C` remains the retained source-owner traceability log for lineage, evidence, and concentrated historical source context, but current reader-facing rule ownership now reads here.
- The published front-door and transition views remain supporting reader surfaces:
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-ops-current-front-door-v1.md`
  - `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- This record owns the stable family-front-door transition and `GC-*` demotion rule, not every later front-door inventory detail.
- Stable close-out review for the fourth promotion lane has completed under `S0F-5A`, and no bounded post-stable export tail was required.

## Traceability

- Source-owner log:
  - `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- Supporting front doors and transition view:
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-ops-current-front-door-v1.md`
  - `docs/governance/views/view-gc-dual-reading-transition-v1.md`
- Promotion lane:
  - `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`