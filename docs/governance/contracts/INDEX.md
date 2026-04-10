# Chronology-First Contracts Index v1

## Purpose

- This index is the canonical root for chronology-first governance-contract rebuild.
- It exists so rebuilt contracts can start from the earliest defended history and grow forward through explicit lineage, instead of continuing the older current-first contract extraction model.

## Current Standing

- `docs/governance/contracts/` is now the canonical root for rebuilt contracts.
- `docs/governance/legacy/contract/` and `docs/governance/legacy/contracts/` are retained legacy reference sets.
- The chronology-first rebuild now keeps one issue-first preview contract for `S0A-1A` after the earlier broad foundational batch was rejected in review.

## Current Rebuild Model

- A chronology-first contract is now defined as one rule-owning or boundary-owning state in the historical contract chain.
- Validation rows, migration mechanics, wrapper/transport shells, and similar retained chronology now stay outside the canonical contract chain unless they become the clearest owner of one governance rule.
- The canonical template now supports distinct lineage verbs for:
  - one-to-one supersession
  - split relationships
  - absorbed relationships
  - retirement relationships
- Canonical naming now uses one long-path readable id grammar rather than short opaque abbreviations:
  - `DOC-<DOMAIN>-<SUBDOMAIN>-...-<CATEGORY>-<NNNN>`
- The rebuild model now also distinguishes:
  - `parent contracts` for mechanism introduction, `why`, and boundary
  - `child contracts` for independently judgeable narrow rule bodies beneath that parent

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
- Open the current preview contract when the question is `can one issue-first contract make the problem readable at a glance?`
  - `docs/governance/contracts/S0A-1A-github-issue-breakdown-title-and-tag-governance.md`
- The next intended generation packet is now one parent-and-child rewrite rather than another one-file mixed preview:
  - parent: workflow/GitHub/issues mechanism introduction
  - child: issue-title rules
  - child: issue-tag rules
- Use the moved legacy trees only as retained reference material while the new canonical chain is rebuilt:
  - `docs/governance/legacy/contract/`
  - `docs/governance/legacy/contracts/`

## Foundational Contracts

| contract id | standing now | role in rebuild |
| --- | --- | --- |
| `S0A-1A` | `draft` | issue-first preview contract for issue breakdown, title encoding, and tag naming governance |

## Reader Notes

- This index intentionally does not treat the moved legacy trees as canonical.
- Existing `view` surfaces may remain clearer than the current contract folders during the reset; that is the reason this rebuild lane exists.
- The current preview intentionally uses the issue identity directly because the earlier broad four-contract synthesis failed the user review standard.
- The next intended step is not another mixed preview: it is to replace that preview with one parent contract and two child contracts under the new long-path naming grammar.