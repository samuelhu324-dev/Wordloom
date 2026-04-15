# S0B-3A Governance Current State v1

## Purpose

- This view is the second bounded current-state reader surface under `S0F-9A/P5`, focused on the `S0B-3A` no-supplement family.
- It exists so readers can answer `who owns this now, who stewards it now, who reviewed it, and who approves it` without replaying the mixed parent ledger and both child contracts end to end.
- It is a reader surface only; it does not replace the parent ledger or child contracts as the underlying governance truth.

## Current Model

- Read this surface only for current effective governance state across the bounded `S0B-3A` family.
- Under this second `P5` cycle:
  - current family routing, stewardship standing, and family-level governance events live on the parent ledger
  - narrow current-governance state for logs and lifecycle lives on the two child contracts
  - no supplement packet currently exists, so packet-level accountability has not been split into a separate evidence surface
- This keeps the no-supplement family readable without inventing one supplement-backed governance layer that the repo does not actually have.

## Current Governance Reading

| governed surface | current reading home | owner team | current steward | reviewed by | approved by | why this is the current-state source |
| --- | --- | --- | --- | --- | --- | --- |
| `S0B-3A` mixed packet routing | `ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter` | `docs-governance` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The parent ledger carries the current routing state for the mixed `S0B-3A` family and also acts as the current-state governance surface while no supplement packet exists. |
| `DOC-WORKFLOW-LOGS-0001` current child contract | `DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter` | `docs-governance` | `delegated:workflow-logs-contract-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The logs child contract carries the current effective state for the logs-facing slices, including delegated stewardship and review-versus-approval separation. |
| `DOC-WORKFLOW-LIFECYCLE-0001` current child contract | `DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation` | `docs-governance` | `delegated:workflow-lifecycle-contract-maintainer` | `role:workflow-reviewer` | `role:docs-governance-approver` | The lifecycle child contract carries the current effective state for the lifecycle-facing slices, including delegated stewardship and review-versus-approval separation. |

## Reader Notes

- Start here when the question is `what is true now for the S0B-3A family?`
- Then open the parent ledger when the question is `what is the current routing state for the mixed source family?`
- Then open the logs or lifecycle child contract when the question becomes `what is the current governed meaning for that narrower child body?`
- Do not infer current ownership from `introduced_by`, `last_changed_by`, or other chronology fields.
- Use `view-s0b-3a-governance-history-and-contribution-v1.md` when the question shifts from current state to contribution, routing write-back, delegation, or role-separation explanation.

## Source Refs

- `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
- `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`
- `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
- `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation.md`
- `docs/governance/views/support-only/view-s0b-3a-governance-history-and-contribution-v1.md`