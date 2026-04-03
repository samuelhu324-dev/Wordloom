## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Parent issue: #248

## Context

- The system had separate body templates for issue creation, issue conclusion, and PR bodies, so the same automation family produced visibly different shapes in live GitHub objects.
- This slice fixed one canonical contract for metadata layout, section order, Evidence Footer shape, and inline-code rules across those bodies.
- The hard gate now checks body shape rather than section presence alone, including blank-line discipline and allowed link categories.
- Representative merged PRs and closed issues were rewritten under that contract to prove the normalized body can survive live verification.

## Definition of Done (DoD)


## Links

- Log: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
