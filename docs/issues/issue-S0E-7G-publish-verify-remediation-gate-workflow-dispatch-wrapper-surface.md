## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: `road-002-projection-runtime-platformization-and-evidence-governance`
- Parent issue: #248

## Context

- The read-only wrapper worked locally, but operators still could not trigger the same verification flow from a GitHub-side manual workflow.
- This slice exposed a workflow_dispatch entrypoint that calls the shared wrapper with explicit family selection, run-specific artifact roots, and uploaded summaries.
- The workflow keeps delegate_apply disabled and preserves the secondary-enforcement wording so GitHub-side runs stay read-only.
- Representative dispatch runs demonstrated that the Actions surface can coordinate verification artifacts without reopening publish ownership or family-specific semantics.

## Definition of Done (DoD)


## Links

- Log: `docs/logs/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-7F-publish-verify-remediation-gate-read-only-wrapper-adoption.md`
