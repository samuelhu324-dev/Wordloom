## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: `road-002-projection-runtime-platformization-and-evidence-governance`
- Parent issue: #248

## Context

- Recent PR and issue fixes exposed repeated drift, but the repo still lacked a shared language for which failures block, replay, reconcile, or stay manual.
- This slice defined the publish-to-verify-to-remediation taxonomy, separating strong-structure failures from weaker prose and summary problems.
- It also fixed the ordered replay pipeline so repairs move through source log, derivation, audit, manifest, apply, and verify instead of ad hoc edits.
- Representative manifests and audits now record each handling semantic explicitly, which gives later automation a stable classification surface.

## Definition of Done (DoD)


## Links

- Log: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
