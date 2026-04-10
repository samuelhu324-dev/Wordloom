# Chronology-First Contracts Index v1

## Purpose

- This index is the canonical root for chronology-first governance-contract rebuild.
- It exists so rebuilt contracts can start from the earliest defended history and grow forward through explicit lineage, instead of continuing the older current-first contract extraction model.

## Current Standing

- `docs/governance/contracts/` is now the canonical root for rebuilt contracts.
- `docs/governance/legacy/contract/` and `docs/governance/legacy/contracts/` are retained legacy reference sets.
- The chronology-first rebuild is not yet populated beyond the template and scaffold phase.

## Current Rebuild Model

- A chronology-first contract is now defined as one rule-owning or boundary-owning state in the historical contract chain.
- Validation rows, migration mechanics, wrapper/transport shells, and similar retained chronology now stay outside the canonical contract chain unless they become the clearest owner of one governance rule.
- The canonical template now supports distinct lineage verbs for:
  - one-to-one supersession
  - split relationships
  - absorbed relationships
  - retirement relationships

## Current Rebuild Order

- First foundational packet: `S0A + S0B`
- Follow-on rebuild order: `S0C -> S0D -> S0E -> S0F`
- This order is chronology-first rather than projection-first:
  - `S0A + S0B` establishes the earliest decision spine
  - `S0C` and `S0D` extend the structural and operator grammar that later automation depends on
  - `S0E` then carries the first large mixed automation and lifecycle contract line
  - `S0F` remains last because it is the latest and still the densest mixed series

## Read Now

- Open `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md` for the rebuild boundary, order, and next steps.
- Use `docs/governance/contracts/_template-contract-record.md` as the temporary record template during the reset phase.
- Use the moved legacy trees only as retained reference material while the new canonical chain is rebuilt:
  - `docs/governance/legacy/contract/`
  - `docs/governance/legacy/contracts/`

## Reader Notes

- This index intentionally does not treat the moved legacy trees as canonical.
- Existing `view` surfaces may remain clearer than the current contract folders during the reset; that is the reason this rebuild lane exists.
- The next intended population step is foundational contract generation from `S0A + S0B`, not another late-stage current-first extraction packet.