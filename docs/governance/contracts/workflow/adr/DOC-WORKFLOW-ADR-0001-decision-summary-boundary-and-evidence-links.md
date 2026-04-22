# DOC-WORKFLOW-ADR-0001 decision summary boundary and evidence links

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-ADR
  contract_release: 0001
  contract_id: DOC-WORKFLOW-ADR-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first ADR-family release from S0A-2A by isolating retained decision records that summarize context, decision, alternatives, consequences, and links back to labs and runbooks without absorbing their execution detail.
  summary: ADRs should act as durable decision summaries that preserve context, decision, alternatives considered, consequences, and links back to the source evidence surfaces rather than replaying full labs or runbook execution detail.
  governance_area: workflow adr decision-summary governance
  applies_to: ADRs that summarize architecture and workflow decisions, including context, decision, alternatives considered, consequences, and links back to source evidence and operator surfaces
  enforcement_surface: manual
  violation_semantics: warning
  owner_team: docs-governance
  current_steward: delegated:workflow-adr-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  recorded_at: 2026-04-22
  reviewed_at: pending
  effective_from: unknown
  effective_until: ongoing
  introduced_by: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  last_changed_by: docs/logs/support-only/ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape.md
  source_refs:
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape.md
  cumulative_source_refs:
    - GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape.md
  supporting_evidence_refs:
    - legacy/from_structured_docs/from-adrs/adr-001-chronicle-projection-chronicle-events-to-entries.md
    - legacy/from_structured_docs/from-adrs/adr-002-evolution-worker-to-daemon.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This first ADR draft stays narrow to decision-summary governance rather than restating the whole broader workflow pipeline.
    - The local repo currently has no S0A-2A source log, so this draft stays explicit about issue-only origin plus later direct-evidence supplementation.
    - The decisive child-opening packet is justified by the accepted ADR SUP row on S0A-2A-R05 rather than by the broad issue packet alone.
    - Current-state governance now reads through owner_team/current_steward/approval_state/reviewed_by/approved_by, while the parent ledger and supplement remain the event and evidence chain that explain how this state was reached.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the narrow current-state governance surface for the `S0A-2A-R05` ADR slice, while the parent ledger and `SUP-003` preserve the route and evidence-history chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day ADR maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-ADR-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-ADR-0001` | `unknown` | `family-introduced` | `2026-04-22` | `GitHub issue S0A-2A (#24)` | The issue-only source introduced the ADR slice, but it does not by itself defend a named current steward or approver for the current contract state. |
| `DOC-WORKFLOW-ADR-0001-GOV-02` | `current-draft-sharpened` | `DOC-WORKFLOW-ADR-0001` | `role:packet-reviewer` | `statement-surface-sharpened` | `2026-04-22` | `ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape.md` | The accepted ADR SUP round sharpened the child-opening reading from broad background into direct decision-summary governance without changing durable owner-team identity. |
| `DOC-WORKFLOW-ADR-0001-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-ADR-0001` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-22` | `S0G-4A/P4 adr sample round` | Stewardship for the current ADR child is now explicitly delegated to the narrower ADR contract maintainer role while final approval remains with the broader docs-governance approver role. |
| `DOC-WORKFLOW-ADR-0001-GOV-04` | `review-approval-separation-event` | `DOC-WORKFLOW-ADR-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-22` | `S0G-4A/P4 adr sample round` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit or collapsed into one reviewer identity. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-ADR-0001-ST-01` | `ADRs as durable decision summaries` | `active` | `introduced` | `S0A-2A-R05` | `DOC-WORKFLOW-ADR-0001` | `unknown` | `DOC-WORKFLOW-ADR-0001` | `2026-04-22` | `unknown` | `ongoing` | `in-force` | ADRs should convert already-stabilized workflow learning into durable decision summaries rather than leaving the decision layer only in broad issue text, labs, or runbooks. | Opening clause for the ADR family itself. |
| `DOC-WORKFLOW-ADR-0001-ST-02` | `Canonical decision skeleton` | `active` | `introduced` | `S0A-2A-R05-SUP-01; S0A-2A-R05-SUP-02` | `DOC-WORKFLOW-ADR-0001` | `unknown` | `DOC-WORKFLOW-ADR-0001` | `2026-04-22` | `unknown` | `ongoing` | `in-force` | ADRs should preserve at least the decision-summary skeleton of `Context`, `Decision`, `Alternatives considered`, and `Consequences` so the reader can recover the durable decision without replaying the whole implementation history. | Both retained ADRs use the same durable skeleton. |
| `DOC-WORKFLOW-ADR-0001-ST-03` | `Link back to source evidence` | `active` | `introduced` | `S0A-2A-R05-SUP-01; S0A-2A-R05-SUP-02` | `DOC-WORKFLOW-ADR-0001` | `unknown` | `DOC-WORKFLOW-ADR-0001` | `2026-04-22` | `unknown` | `ongoing` | `in-force` | ADRs should link back to the labs, runbooks, or other source evidence that justify the decision rather than absorbing the full execution narrative into the ADR body itself. | This keeps ADRs decision-facing while preserving traceability. |
| `DOC-WORKFLOW-ADR-0001-ST-04` | `Cross-surface boundary` | `active` | `introduced` | `S0A-2A-R05-SUP-01; S0A-2A-R05-SUP-02` | `DOC-WORKFLOW-ADR-0001` | `unknown` | `DOC-WORKFLOW-ADR-0001` | `2026-04-22` | `unknown` | `ongoing` | `in-force` | ADRs may summarize reusable architecture or workflow decisions across projections, but they should still leave operator steps to runbooks and experimentation detail to labs. | This clause keeps ADR ownership on decision meaning rather than SOP or drill detail. |

## Release Change

- This release opens the first dedicated `DOC-WORKFLOW-ADR` family from the accepted `S0A-2A-R05` ADR child-candidate review.
- The decisive evidence is the retained ADR pair:
  - `adr-001-chronicle-projection-chronicle-events-to-entries.md`
  - `adr-002-evolution-worker-to-daemon.md`
- Those sources show the same durable ADR pattern twice:
  - the decision layer is separated from the underlying labs and runbooks
  - the ADR keeps context, decision, alternatives considered, and consequences readable as the stable summary
  - links point back to labs, runbooks, and operator evidence instead of copying their whole execution narrative into the ADR body
- This release intentionally does not absorb the broader workflow pipeline, logs child, labs child, or runbook child boundaries; it owns only the ADR-family decision-summary layer.

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-ADR-0001-ST-01`: ADRs should convert already-stabilized workflow learning into durable decision summaries.
- `DOC-WORKFLOW-ADR-0001-ST-02`: ADRs should preserve a minimum decision-summary skeleton through `Context`, `Decision`, `Alternatives considered`, and `Consequences`.
- `DOC-WORKFLOW-ADR-0001-ST-03`: ADRs should link back to the source labs, runbooks, or other evidence that justify the decision rather than replaying that full execution detail inline.
- `DOC-WORKFLOW-ADR-0001-ST-04`: ADRs may summarize reusable architecture or workflow decisions across projections, but they should still leave operator steps to runbooks and experimentation detail to labs.

## Current Reading

- Read this release when the question is `what adr-layer rule first governed decision summaries as durable workflow readers rather than only broad background beneath the parent pipeline?`
- Read `DOC-WORKFLOW-0001` first only when the reader still needs the broader `log -> lab -> runbook -> adr` refinement boundary rather than the narrower ADR family itself.

## Reader Notes

- This draft is sourced from issue `S0A-2A`, but its child-opening decision depends on later direct-evidence supplementation through the accepted ADR SUP packet.
- The opening release intentionally stays narrow to decision-summary governance because the current defended evidence comes from the retained Chronicle and worker-to-daemon ADR pair rather than from every possible ADR shape in the repo.
- Later releases may widen or refine this family if additional archaeology proves broader ADR governance beyond the decision-summary boundary captured here.
- Under `S0G-4A/P4`, this contract now also acts as the current-state governance surface for the ADR child while the supplement remains the packet-level evidence and accountability surface.