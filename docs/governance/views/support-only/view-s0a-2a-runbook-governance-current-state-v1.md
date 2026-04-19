# S0A-2A Runbook Governance Current State v1

## Purpose

- This view is the second bounded current-state reader surface under `S0F-9A/P3`, focused on the `S0A-2A/R04` runbook slice.
- It exists so readers can answer `who owns this now, who stewards it now, who reviewed it, and who approves it` without replaying the broad parent ledger, the runbook supplement, and the child contract end to end.
- It is a reader surface only; it does not replace the parent ledger or runbook child contract as the underlying governance truth.

## Current Model

- Read this surface only for current effective governance state across the bounded `S0A-2A/R04` sample slice.
- Under this second `P3` round:
  - current ownership, stewardship, review, and approval state live on the parent-ledger and runbook-child surfaces
  - packet-level direct-markdown review, verification, and write-back history stay in the supplement as event and accountability history
- This keeps the broad `S0A-2A` parent packet readable while still letting one narrow runbook slice expose current governance state explicitly.

## Current Governance Reading

| governed surface | current reading home | owner team | current steward | reviewed by | approved by | why this is the current-state source |
| --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A` broad packet routing | `ledger-S0A-2A-tools-workflow-log-lab-runbook-adr` | `docs-governance` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The parent ledger carries the current routing state for the mixed `S0A-2A` packet even though final parent acceptance is still pending. |
| `DOC-WORKFLOW-RUNBOOK-0001` current child contract | `DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery` | `docs-governance` | `delegated:workflow-runbook-contract-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The child contract carries the current effective state for the narrow runbook slice, including delegated stewardship and review-versus-approval separation. |
| `SUP-001` direct-evidence packet | `ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr` | `not-current-state-surface` | `not-current-state-surface` | `role:workflow-reviewer` | `role:docs-governance-approver` | The supplement records packet review and evidence accountability only; it should not be read as the current ownership or stewardship surface. |

## Reader Notes

- Start here when the question is `what is true now for the runbook slice?`
- Then open the parent ledger when the question is `what is the current routing state for the broad S0A-2A packet?`
- Then open the runbook child contract when the question is `what is the current governed meaning for the projection-runbook layer?`
- Do not infer current ownership from `introduced_by`, `last_changed_by`, or other chronology fields.
- Use `view-s0a-2a-runbook-governance-history-and-contribution-v1.md` when the question shifts from current state to contribution, direct evidence, delegation, or role-separation explanation.

## Source Refs

- `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
- `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
- `docs/logs/support-only/ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr.md`
- `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md`
- `docs/governance/views/support-only/view-s0a-2a-runbook-governance-history-and-contribution-v1.md`