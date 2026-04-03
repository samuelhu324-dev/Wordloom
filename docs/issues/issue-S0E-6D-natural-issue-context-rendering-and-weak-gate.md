## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Projects: `wordloom Board`
- Milestone: ``
- Parent issue: #248

## Context

- S0E-6C made Context deterministic, but the renderer still produced prose that looked like the same template with nouns swapped.
- This slice replaced rigid sentence slots with source-log-derived summaries so different issues can sound specific without losing contract shape.
- The gate was narrowed to prose-integrity checks such as line counts, readable English, and placeholder hygiene rather than rhetorical pattern matching.
- Replayed closed-issue samples showed the new renderer can pass audit while reading like manual project notes instead of machine scaffolding.

## Definition of Done (DoD)


## Links

- Log: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
