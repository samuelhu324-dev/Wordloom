# S0A-1A Governance Current State v1

## Purpose

- This view is the first bounded current-state reader surface for the `S0A-1A` governance-control sample family.
- It exists so readers can answer `who owns this now, who stewards it now, who reviewed it, and who approves it` without replaying the parent ledger, supplement, and child contract end to end.
- It is a reader surface only; it does not replace the parent ledger or child contract as the underlying governance truth.

## Current Model

- Read this surface only for current effective governance state across the bounded `S0A-1A` family.
- Under the `S0F-9A/P1` and `P2` split:
  - current ownership, stewardship, review, and approval state live on the parent-ledger and child-contract surfaces
  - packet-level evidence maintenance, verification, and screenshot review stay in the supplement as event/accountability history
- This means the supplement can defend evidence-chain accountability without being mistaken for the current owner or current steward surface.

## Current Governance Reading

| governed surface | current reading home | owner team | current steward | reviewed by | approved by | why this is the current-state source |
| --- | --- | --- | --- | --- | --- | --- |
| `S0A-1A` mixed packet routing | `ledger-S0A-1A-tools-github-issues-projects-and-tags` | `docs-governance` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The parent ledger carries the current routing and governance state for the mixed packet rather than only its historical intake. |
| `DOC-WORKFLOW-GITHUB-PROJECTS-0001` current child contract | `DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority` | `docs-governance` | `delegated:workflow-projects-contract-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The child contract carries the current effective state for the bounded Projects surface, including the delegated steward and review-versus-approval split. |
| `SUP-001` screenshot packet | `ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags` | `not-current-state-surface` | `not-current-state-surface` | `role:workflow-reviewer` | `role:docs-governance-approver` | The supplement records packet review and evidence accountability only; it should not be read as the current ownership or stewardship surface. |

## Reader Notes

- Start here when the question is `what is true now?`
- Then open the parent ledger when the question is `what is the current routing state for the mixed S0A-1A packet?`
- Then open the Projects child contract when the question is `what is the current governed meaning for GitHub Projects usage inside this family?`
- Do not infer current ownership from `submitted by`, `evidence owner`, `introduced_by`, or other chronology fields.
- Use `view-s0a-1a-governance-history-and-contribution-v1.md` when the question shifts from current state to contribution, delegation, handoff, or evidence-history explanation.

## Source Refs

- `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
- `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
- `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
- `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
- `docs/governance/views/support-only/view-s0a-1a-governance-history-and-contribution-v1.md`