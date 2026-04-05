## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: `road-002: projection runtime platformization and evidence governance`
- Parent issue: #363

## Context

- The issue packages the stable PR body completeness check behind a repo-owned local task and a workflow-dispatch CI gate without changing existing wrapper semantics.
- The packaging strictly reuses existing scripts and avoids duplicating logic by delegating execution to the PowerShell entrypoint.
- The runbook has been validated by successfully running the packaged local task and CI gate, with evidence retained from both executions.
- The CI gate can fail on findings but is designed as a secondary enforcement surface that does not replace the local reviewer-owned boundary.

## Definition of Done (DoD)

- #383

## Links

- Log: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- Runbook: `docs/runbook/run-S0F-1H-pr-body-completeness-review.md`
- Roadmap: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Previous log: `docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md`

