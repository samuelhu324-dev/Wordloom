# DOC Current Front Door v1

## Purpose

- This view is the first current front door for the `DOC` contract family.
- It exists so readers can find current documentation-governance meaning without first translating that question into the older `GC-*` registry vocabulary.

## Current Model

- Read `DOC` as the family for doc-first control-plane contracts.
- The `DOC` family includes current rule surfaces about document roles, source-log compatibility, taxonomy, placement, and later family-first front-door transition.
- The current `DOC` front door is family-first rather than registry-first:
  - start here for current reading
  - then open the landed family-owned contract body when one exists
  - otherwise open the stable or bounded source-owner log that currently holds the authoritative rule text
- Under this model, `DOC` current reading does not require first creating a `GC-*` registry record.

## Active Contracts

- `DOCUMENT-ROLE-BOUNDARIES-WRITEBACK-PROTOCOL-AND-DISPOSITION-MODEL`:
  - promoted current contract draft: `docs/governance/contract/DOC-DRB-0001-document-role-boundaries-writeback-and-disposition.md`
  - retained source-owner SoT during draft stage: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  - current role: fixes the six-outlet role model, write-back order, and disposition separation, with the first family-owned contract body now landed but not yet fully closed out
- `SOURCE-LOG-COMPATIBILITY-AND-WEAK-STRUCTURE-EXPORT-DISCIPLINE`:
  - current primary source: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  - current role: keeps the old two source-log templates canonical and narrows outlet ownership to weak-structure export
- `GOVERNANCE-CONTRACT-TAXONOMY-AND-PLACEMENT-MODEL`:
  - current primary source: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
  - current role: fixes the seven-family taxonomy, placement model, and family-versus-level split
- `DOC-AND-OPS-FRONT-DOOR-TRANSITION-AND-GC-DEMOTION-MODEL`:
  - current primary source: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
  - current role: fixes how readers should transition from registry-first wording to family-first reading

## Reader Notes

- This front door is intentionally a `view` rather than a new `GC-*` record.
- The `DOC` family is now in a mixed landing state:
  - `DOC-DRB-0001` already exists as a family-owned current contract draft
  - `S0F-4A` still remains the retained source-owner SoT for that rule set until later stable close-out review completes
- Other `DOC` areas still keep their strongest rule text in source-owner logs because those promotions have not landed yet.
- Promoted contract bodies should land under `docs/governance/contract/` with the family-owned filename model `DOC-<AREA>-<NNNN>-<summary>.md`.
- The current planned promotion map lives at `docs/governance/views/view-doc-contract-promotion-map-v1.md`.

## Source Refs

- `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `docs/governance/contract/DOC-DRB-0001-document-role-boundaries-writeback-and-disposition.md`
- `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- `docs/governance/contract/INDEX.md`
- `docs/governance/views/view-doc-contract-promotion-map-v1.md`