# DOC-WORKFLOW-RUNBOOK-0001 projection operator rebuild replay and failure recovery

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-RUNBOOK
  contract_release: 0001
  contract_id: DOC-WORKFLOW-RUNBOOK-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first runbook-family release from S0A-2A by isolating the earliest projection SOPs as durable operator guidance for rebuildability, replay, runtime verification, observability, and failure recovery.
  summary: Projection runbooks should convert post-labs operational learning into durable operator SOPs for rebuild, replay, health and readiness verification, observability, and bounded failure recovery.
  governance_area: workflow runbook operator recovery and runtime verification governance
  applies_to: operator runbooks for long-lived projection systems, including rebuild procedures, replay procedures, readiness and health checks, observability checks, and failure-recovery handling
  enforcement_surface: runbook
  violation_semantics: warning
  recorded_at: 2026-04-12
  reviewed_at: 2026-04-12
  effective_from: unknown
  effective_until: ongoing
  introduced_by: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  last_changed_by: docs/logs/support-only/ledger-SUP-S0A-2A-tools-workflow-log-lab-runbook-adr.md
  source_refs:
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-tools-workflow-log-lab-runbook-adr.md
  cumulative_source_refs:
    - GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-tools-workflow-log-lab-runbook-adr.md
  supporting_evidence_refs:
    - legacy/from_structured_docs/from-runbook/run-001-search-projection.md
    - legacy/from_structured_docs/from-runbook/run-003-chronicle-projection.md
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
    - This first runbook draft stays narrow to projection operator SOP governance rather than restating the whole broader workflow pipeline.
    - The local repo currently has no S0A-2A source log, so this draft stays explicit about issue-only origin plus later direct-evidence supplementation.
    - The decisive child-opening packet is justified by the accepted runbook SUP row on S0A-2A-R04 rather than by the broad issue packet alone.
```

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-RUNBOOK-0001-ST-01` | `Runbooks as durable operator SOPs` | `active` | `introduced` | `S0A-2A-R04` | `DOC-WORKFLOW-RUNBOOK-0001` | `unknown` | `DOC-WORKFLOW-RUNBOOK-0001` | `2026-04-12` | `unknown` | `ongoing` | `in-force` | Runbooks should convert operational learning from projection implementation and labs into durable operator-facing SOPs rather than leaving that knowledge only in experiments or broad issue text. | Opening clause for the runbook family itself. |
| `DOC-WORKFLOW-RUNBOOK-0001-ST-02` | `Rebuild from source of truth` | `active` | `introduced` | `S0A-2A-R04-SUP-01; S0A-2A-R04-SUP-02` | `DOC-WORKFLOW-RUNBOOK-0001` | `unknown` | `DOC-WORKFLOW-RUNBOOK-0001` | `2026-04-12` | `unknown` | `ongoing` | `in-force` | Projection runbooks should document how the read model can be rebuilt from its source-of-truth path rather than treating the projection state as unrecoverable operational history. | Both earliest runbooks treat rebuildability as a durable operator concern after projection success. |
| `DOC-WORKFLOW-RUNBOOK-0001-ST-03` | `Runtime verification and readiness` | `active` | `introduced` | `S0A-2A-R04-SUP-01; S0A-2A-R04-SUP-02` | `DOC-WORKFLOW-RUNBOOK-0001` | `unknown` | `DOC-WORKFLOW-RUNBOOK-0001` | `2026-04-12` | `unknown` | `ongoing` | `in-force` | Runbooks should expose one minimum runtime-verification path through health or readiness checks, metrics, and direct state inspection before and during operator intervention. | Search and chronicle both elevate readiness, health, metrics, and DB-state verification into durable SOP shape. |
| `DOC-WORKFLOW-RUNBOOK-0001-ST-04` | `Auditable replay after terminal failure` | `active` | `introduced` | `S0A-2A-R04-SUP-01; S0A-2A-R04-SUP-02` | `DOC-WORKFLOW-RUNBOOK-0001` | `unknown` | `DOC-WORKFLOW-RUNBOOK-0001` | `2026-04-12` | `unknown` | `ongoing` | `in-force` | Failed projection work should move through explicit replay-controlled recovery with audit fields and operator intent rather than through silent automatic resurrection. | The runbooks make replay and failure handling part of operator governance, not just implementation detail. |
| `DOC-WORKFLOW-RUNBOOK-0001-ST-05` | `Bounded observability and recovery actions` | `active` | `introduced` | `S0A-2A-R04-SUP-01; S0A-2A-R04-SUP-02` | `DOC-WORKFLOW-RUNBOOK-0001` | `unknown` | `DOC-WORKFLOW-RUNBOOK-0001` | `2026-04-12` | `unknown` | `ongoing` | `in-force` | Runbooks should pair backlog or failure observability with bounded recovery actions for transient dependency failures, deterministic data problems, and draining or restart decisions. | This keeps runbook ownership on operator recovery semantics rather than on domain-specific projection design. |

## Release Change

- This release opens the first dedicated `DOC-WORKFLOW-RUNBOOK` family from the already accepted `S0A-2A-R04` runbook child-candidate review.
- The decisive evidence is the earliest durable projection SOP pair:
  - `run-001-search-projection.md`
  - `run-003-chronicle-projection.md`
- Those sources show the same post-projection pattern twice:
  - projection success is not the endpoint
  - the next long-lived operator need becomes rebuildability, replay, readiness, observability, and failure recovery
  - that operator guidance becomes durable enough to live as runbook governance rather than only as labs or issue-level notes
- This release intentionally does not absorb the broader workflow pipeline, logs child, labs child, or ADR child boundaries; it owns only the runbook-family operator SOP layer.

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-RUNBOOK-0001-ST-01`: Runbooks should convert projection-operation learning into durable operator SOPs.
- `DOC-WORKFLOW-RUNBOOK-0001-ST-02`: Projection systems should remain rebuildable from source-of-truth state, and runbooks should document that rebuild path.
- `DOC-WORKFLOW-RUNBOOK-0001-ST-03`: Runbooks should expose a minimum operator verification path through readiness, health, metrics, and direct state inspection.
- `DOC-WORKFLOW-RUNBOOK-0001-ST-04`: Terminal failure handling should require explicit, auditable replay rather than silent automatic recovery.
- `DOC-WORKFLOW-RUNBOOK-0001-ST-05`: Runbooks should pair observability with bounded recovery actions for transient failure, deterministic failure, and runtime draining or restart situations.

## Current Reading

- Read this release when the question is `what runbook-layer rule first governed projection rebuild, replay, runtime verification, and failure recovery as durable operator SOPs?`
- Read `DOC-WORKFLOW-0001` first only when the reader still needs the broader `log -> lab -> runbook -> adr` refinement boundary rather than the narrower runbook family itself.

## Reader Notes

- This draft is sourced from issue `S0A-2A`, but its child-opening decision depends on later direct-evidence supplementation through the accepted runbook SUP packet.
- The opening release intentionally stays narrow to projection operator governance because the current defended evidence comes from search and chronicle projection SOPs rather than from every possible runbook shape in the repo.
- Later releases may widen or refine this family if additional archaeology proves broader runbook governance beyond the projection-rebuild and recovery pattern captured here.