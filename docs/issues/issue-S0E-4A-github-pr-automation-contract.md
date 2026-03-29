# S0E-4A: contract/GitHub pull request automation contract

## Metadata

- Title: `S0E-4A: contract/GitHub pull request automation contract`
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Milestone: ``
- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Parent issue: ``

## Context

- `S0E-4A` defines PR automation as a separate contract instead of hiding it inside issue automation.
- v1 treats PR creation as its own object model: commit selection, PR metadata, project assignment, milestone assignment, development linking, and human-readable PR description.
- The stable workflow preserves day-to-day work on mixed branches while still allowing ID-scoped PRs to be created safely.

## Definition of Done (DoD)

- The contract explicitly defines a stable commit-selection strategy for ID-scoped PRs.
- Log templates expose enough PR metadata for automation to extract labels, projects, milestone, base branch, and development issue.
- PR descriptions have one simple, repeatable structure that can be generated from child-log execution checklists.
- The contract explains how PR automation coexists with a constantly updated working branch without losing unrelated scope work.

## Links

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Parent Log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous Log: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
- Reference Log 1: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Reference Log 2: `docs/logs/_template-log-parent-epic-spine.md`
- Reference Log 3: `docs/logs/_template-log-phase-drills-evidence.md`
