# DOC-CONTROL-PLANE-0001 current-state event-history and authorization boundary

```yaml
contract_record:
  contract_family: DOC-CONTROL-PLANE
  contract_release: 0001
  contract_id: DOC-CONTROL-PLANE-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first DOC-first governance-control contract by fixing the minimum current-state vocabulary, event-history placement rule, and boundary against authorization/product-access semantics after two bounded sample rounds under S0F-9A.
  summary: Govern DOC-first control-plane semantics through explicit current-state fields for ownership, stewardship, review, and approval; explicit event-history surfaces for contribution and handoff; and an explicit boundary that keeps authorization, entitlement, and billing semantics out of this contract family.
  governance_area: DOC-first governance control-plane vocabulary and current-state versus event-history boundary
  applies_to: current-state governance fields on logs, ledgers, and contracts; event-history surfaces for contribution and handoff; and the boundary between governance control and authorization/product access
  enforcement_surface: manual
  violation_semantics: warning
  recorded_at: 2026-04-15
  reviewed_at: pending
  effective_from: 2026-04-15
  effective_until: ongoing
  introduced_by: docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md
  last_changed_by: docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md
  source_refs:
    - docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md
  cumulative_source_refs:
    - docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md
    - docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md
    - docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md
    - docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr.md
    - docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md
  supporting_evidence_refs:
    - docs/governance/views/support-only/view-s0a-1a-governance-current-state-v1.md
    - docs/governance/views/support-only/view-s0a-1a-governance-history-and-contribution-v1.md
    - docs/governance/views/support-only/view-s0a-2a-runbook-governance-current-state-v1.md
    - docs/governance/views/support-only/view-s0a-2a-runbook-governance-history-and-contribution-v1.md
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
    - This first control-plane contract is DOC-first by design and should be treated as the vocabulary-and-boundary owner for M3-P0 rather than as a repo-wide runtime authorization model.
    - The contract is justified by one screenshot-backed narrow-child sample and one markdown-evidence-backed broad-parent to narrow-child sample under S0F-9A.
    - Later runbook, evidence, drill, tenant, entitlement, and billing rollouts should reuse this vocabulary rather than overloading it with authorization semantics.
```

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-CONTROL-PLANE-0001-ST-01` | `Current-state governance fields` | `active` | `introduced` | `S0F-9A/P0-C1-S1; S0F-9A/P3-C1-S1S2; S0F-9A/P3-C2-S1S2` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `2026-04-15` | `ongoing` | `in-force` | Current effective governance state should be carried through explicit current-state fields such as `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by` rather than being inferred from chronology or evidence metadata. | The two S0F-9A sample rounds now prove that this field set can be carried on both narrow-child and broad-parent to narrow-child packets. |
| `DOC-CONTROL-PLANE-0001-ST-02` | `Verification stays packet-level` | `active` | `introduced` | `S0F-9A/P0-C1-S1; S0F-9A/P2-C1-S1S2; S0F-9A/P3-C2-S1S2` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `2026-04-15` | `ongoing` | `in-force` | `verified_by` is a packet-level evidence-accountability field and should remain on supplements or other event/accountability surfaces rather than being flattened into current-state frontmatter by default. | This keeps evidence verification distinct from current ownership and current approval identity. |
| `DOC-CONTROL-PLANE-0001-ST-03` | `Event-history owns contribution and handoff` | `active` | `introduced` | `S0F-9A/P0-C1-S2; S0F-9A/P3-C1-S1S2; S0F-9A/P3-C2-S1S2` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `2026-04-15` | `ongoing` | `in-force` | Contribution credits, direct-evidence review, delegated stewardship, review-versus-approval separation, and ownership handoff must live in ledgers, supplements, or explicit event tables rather than in current-state frontmatter. | This is the core current-state versus event-history placement rule for M3-P0. |
| `DOC-CONTROL-PLANE-0001-ST-04` | `Actor is not a catch-all` | `active` | `introduced` | `S0F-9A/P0-C1-S1; S0F-9A/P2-C1-S1S2` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `2026-04-15` | `ongoing` | `in-force` | Governance records must not collapse ownership, stewardship, review, approval, verification, contribution, and handoff into one overloaded `actor` field. | The first two sample rounds already prove at least one delegated stewardship case and at least one clean review versus verify versus approve split. |
| `DOC-CONTROL-PLANE-0001-ST-05` | `Minimum event vocabulary` | `active` | `introduced` | `S0F-9A/P0-C1-S1; S0F-9A/P3-C1-S1S2; S0F-9A/P3-C2-S1S2` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `2026-04-15` | `ongoing` | `in-force` | The minimum reusable event vocabulary for this lane includes `contribution_event` plus ownership or stewardship movement such as `ownership_handoff_event` or a narrower delegated-stewardship event, with room for review and approval separation events when the sample justifies them. | This clause fixes the vocabulary floor without pretending the repo already has one frozen global event enum. |
| `DOC-CONTROL-PLANE-0001-ST-06` | `Authorization boundary` | `active` | `introduced` | `S0F-9A/P0-C1-S3` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `DOC-CONTROL-PLANE-0001` | `2026-04-15` | `2026-04-15` | `ongoing` | `in-force` | This DOC-first control-plane contract governs ownership, stewardship, approval, review, verification, contribution, and handoff semantics only; it does not govern tenant permission, system privilege, plan state, entitlement, billing, or broader product-access closure. | The authorization and commercial boundary remains reserved for M4. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-CONTROL-PLANE-0001-CH-01` | `DOC-CONTROL-PLANE-0001` | `introduced` | `none` | `DOC-CONTROL-PLANE-0001-ST-01; DOC-CONTROL-PLANE-0001-ST-02; DOC-CONTROL-PLANE-0001-ST-03; DOC-CONTROL-PLANE-0001-ST-04; DOC-CONTROL-PLANE-0001-ST-05; DOC-CONTROL-PLANE-0001-ST-06` | `2026-04-15` | `2026-04-15` | The first DOC-first control-plane contract is now explicit enough to own the shared vocabulary, current-state versus event-history placement rule, and authorization boundary after two bounded sample rounds proved the shape locally. | `S0F-9A/P0-C1-S1S2S3; S0F-9A/P3-C1-S1S2; S0F-9A/P3-C2-S1S2` | The release is intentionally narrow: it fixes reusable control-plane semantics without yet opening a broader runtime authorization model. |

## Release Change

- This release establishes the first DOC-first governance-control contract from `S0F-9A`.
- The release fixes three reusable rule surfaces that were previously carried only in the source log and in local sample write-backs:
  - one minimum current-state vocabulary for ownership, stewardship, review, approval, and packet-level verification
  - one explicit placement rule that keeps current state in frontmatter and contribution or handoff in event-history surfaces
  - one explicit boundary that keeps authorization, entitlement, and billing semantics outside this family
- This release intentionally does not absorb tenant-access, product privilege, or billing state modeling; those remain reserved for `M4`.

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-CONTROL-PLANE-0001-ST-01`: Current effective governance state should read through explicit current-state fields such as `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- `DOC-CONTROL-PLANE-0001-ST-02`: `verified_by` should remain a packet-level evidence-accountability field unless later evidence proves a narrower current-state use that should be owned by a different contract.
- `DOC-CONTROL-PLANE-0001-ST-03`: Contribution, direct-evidence review, stewardship movement, and handoff history should be recorded in event tables, supplements, or comparable historical-accountability surfaces rather than in current-state frontmatter.
- `DOC-CONTROL-PLANE-0001-ST-04`: Governance records must not overload one generic `actor` field to carry distinct meanings that belong to owner, steward, reviewer, approver, verifier, contributor, or handoff actor roles.
- `DOC-CONTROL-PLANE-0001-ST-05`: The minimum reusable event vocabulary for this lane includes contribution and handoff semantics, with narrower delegated-stewardship or role-separation events admitted when samples justify them.
- `DOC-CONTROL-PLANE-0001-ST-06`: Authorization, entitlement, billing, and broader product-access semantics remain out of scope for this contract family.

## Current Reading

- Read this release when the question is `what is the shared DOC-first control-plane rule for current-state fields, event-history placement, and the boundary against authorization semantics?`
- Read `S0F-9A` when the question is `how was this rule family staged, sampled, and proven locally?`
- Read the `S0A-1A` and `S0A-2A/R04` sample families when the question is `how does this contract behave on real bounded ledger and child-contract surfaces?`

## Reader Notes

- This contract is intentionally family-owning and boundary-owning rather than sample-owning.
- The two bounded `P3` rounds justify the contract because they prove the same shape across two different sample styles:
  - one screenshot-backed narrow-child packet
  - one markdown-evidence-backed broad-parent to narrow-child packet
- Later runbook, evidence, and drill families should reuse this control-plane contract instead of redefining the same ownership and event-history split ad hoc.