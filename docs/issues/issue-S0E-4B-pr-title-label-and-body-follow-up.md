## Metadata

- Title: `S0E-4B: contract/PR title compression, structural label inheritance, and body footer follow-up`
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Source log: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
- Parent issue: ``

## Context

- `S0E-4B` exists as the narrow follow-up to `S0E-4A`, focused only on PR title naming, PR label inheritance, and PR body section formatting.
- Structural PR labels should no longer rely only on `pr_labels`; they should inherit explicit issue-side structural labels from the same log.
- PR body generation should match the newer log template shape, especially flat execution checklist parsing plus separate `Evidence Footer` and `Development Link` sections.
- Stacked PRs should be interpreted by their compare base and `Files changed` delta, not by GitHub's full head-branch commit ancestry list.

## Definition of Done (DoD)

- Generated PR titles can distinguish whole-phase aggregate PRs from incremental `P*-C*-S*` follow-ups.
- Generated PR labels inherit at least the explicit top/scope/module labels from the same source log.
- Body generation can parse `Execution Checklist` sections even when the heading variant changes.
- `Evidence Footer` and `Development Link` remain separate sections in the generated PR body.
- Issue creation for logs under `docs/logs/` defaults to project `wordloom Board` unless an explicit project override is supplied.
- Live issue creation and project assignment are validated by issue `#295` on `wordloom Board`.
- PR creation stays project-empty by default unless `pr_projects` is explicitly populated.
- Logs with substantive evidence/drill execution derive the `drills` label.
- Stacked PR review guidance makes clear that `Files changed` and compare-base semantics are authoritative, while full commit ancestry is only traceability context.
- Parent/spine logs and child phase logs have a clear branch-lifecycle policy instead of creating ad hoc permanent top-level branches for every PR.

## Links

- Log: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
- Parent Log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Reference Log 1: `docs/logs/_template-log-parent-epic-spine.md`
- Reference Log 2: `docs/logs/_template-log-phase-drills-evidence.md`
- Reference Log 3: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
