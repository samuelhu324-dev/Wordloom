# DOC Contract Promotion Map v1

## Purpose

- This view explains how current source-owner `DOC` logs promote into family-owned `DOC` contract records.
- It exists so later extraction work can reuse one explicit mapping rule instead of improvising a new contract ID every time.

## Promotion Rule

- A source-owner `DOC` log remains the current primary SoT until its rule text is stable enough to stand alone as a family-owned current contract.
- When promotion happens:
  - the contract body lands under `docs/governance/contract/`
  - the promoted file uses the `DOC-<AREA>-<NNNN>-<summary>.md` model
  - the source-owner log remains the execution and traceability ledger rather than the long-term primary current rule body

## First Mapping Set

| source-owner log | promoted contract target | meaning |
| --- | --- | --- |
| `S0F-4A` | `DOC-DRB-0001` | document role boundaries, write-back protocol, and disposition model |
| `S0F-4B` | `DOC-SLC-0001` | source-log compatibility and weak-structure export discipline |
| `S0F-3I` | `DOC-TAX-0001` | governance contract taxonomy and placement model |
| `S0F-4C` | `DOC-FDT-0001` | family front-door transition and `GC-*` demotion model |

## Reader Notes

- This remains a promotion map first: it owns deterministic source-owner-to-contract mapping, not the full directory-inventory job or the family front-door job.
- The first mapping set above is now fully executed: `DOC-DRB-0001`, `DOC-SLC-0001`, `DOC-TAX-0001`, and `DOC-FDT-0001` are all landed as active family-owned current contracts.
- For later mapping extensions that are not yet executed, the source-owner log remains the current primary source until the corresponding promoted file exists.
- The map therefore remains meaningful after the first quartet completed because it still fixes naming, area ownership, and future extension semantics deterministically.

## Source Refs

- `docs/governance/contract/INDEX.md`
- `docs/governance/contract/_template-doc-contract-record.md`
- `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`