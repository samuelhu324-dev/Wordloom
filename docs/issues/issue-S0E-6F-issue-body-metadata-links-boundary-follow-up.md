## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Projects: `wordloom Board`
- Milestone: `road-002-projection-runtime-platformization-and-evidence-governance`
- Parent issue: #248

## Context

- The issue body still treated Source log as metadata even though it behaves as a navigation link rather than issue state.
- This slice kept Metadata limited to issue state fields and moved deterministic navigation rows into Links, including optional previous-log references.
- Top-level parent issues and child issues now follow separate body rules so parent ledgers do not inherit child-oriented fields by accident.
- Lifecycle audit was updated around that split so historical S0E issues can be checked against one explicit Metadata-versus-Links contract.

## Definition of Done (DoD)


## Links

- Log: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
