# Contract Sweep Workflow v1

## Purpose

- This view concentrates the first reusable workflow for sweeping one bounded source family into governance-contract decisions without turning the front door into a mixed current-plus-history ledger.

## Current Model

- The workflow now treats contract sweeping as a declared review path rather than as ad hoc file creation.
- Each bounded family sweep must produce:
  - one sweep packet
  - one candidate worksheet
  - one resolved outcome per row
  - one bounded action package

## Decision Outcomes

- `already covered`
- `refine existing`
- `split current`
- `supersede current`
- `absorb into current`
- `retire surface`
- `admit new current`
- `support-only history`
- `defer adjudication`

## Allowed Actions

- Create or modify current contracts only after every row resolves to one explicit outcome.
- Update `INDEX.md` only when the sweep changes current-state reading.
- Preserve old records through `deprecated`, `superseded`, or `retired` handling instead of deleting them.
- Use one governance view when lineage or current-vs-history reading would otherwise become noisy.

## Reader Notes

- This workflow does not guarantee that every sweep will create new current contracts.
- The workflow is meant to reduce judgment drift: human reviewers still declare the semantic outcome, while mechanics validate closure and consistency.

## Source Refs

- `docs/logs/log-S0F-3C-governance-contract-series-audit-and-admission.md`
- `docs/logs/log-S0F-3E-governance-registry-lineage-and-legacy-handling.md`
- `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`