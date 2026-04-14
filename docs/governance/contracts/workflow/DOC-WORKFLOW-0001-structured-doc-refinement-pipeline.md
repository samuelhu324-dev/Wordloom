# DOC-WORKFLOW-0001 structured doc refinement pipeline

```yaml
contract_record:
  contract_family: DOC-WORKFLOW
  contract_release: 0001
  contract_id: DOC-WORKFLOW-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Preserve the first broad workflow release from S0A-2A as the parent boundary for one-way refinement from log to lab to runbook to ADR, while aligning the file to the current chronology-first contract structure.
  summary: Manage structured documentation as a one-way refinement pipeline from log to lab to runbook to ADR, where links point back to source artifacts and evidence rather than forward to a guessed next step.
  governance_area: workflow documentation refinement pipeline governance
  applies_to: structured logs, labs, runbooks, adrs, source-linking semantics, and workflow handoff boundaries across documentation refinement
  enforcement_surface: manual
  violation_semantics: warning
  recorded_at: 2026-04-10
  reviewed_at: pending
  effective_from: unknown
  effective_until: ongoing
  introduced_by: GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  last_changed_by: GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  source_refs:
    - GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  cumulative_source_refs:
    - GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
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
    - This contract is intentionally placed at the broader WORKFLOW layer rather than inside one narrower GitHub-issues subpath.
    - Narrower workflow families such as `DOC-WORKFLOW-LABS` may sit beneath this broader workflow family path, but that hierarchy is not itself a release split event.
    - The local repo currently has no S0A/2A source log, so this draft stays explicit about issue-only sourcing.
```

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-0001-ST-01` | `One-way refinement pipeline` | `active` | `introduced` | `S0A-2A-R01` | `DOC-WORKFLOW-0001` | `unknown` | `DOC-WORKFLOW-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Structured documentation should move through one one-way refinement pipeline from log to lab to runbook to ADR. | Broad workflow boundary clause retained as the primary owner for the S0A-2A parent packet. |
| `DOC-WORKFLOW-0001-ST-02` | `Back-link to source evidence` | `active` | `introduced` | `S0A-2A-R01` | `DOC-WORKFLOW-0001` | `unknown` | `DOC-WORKFLOW-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Links in that pipeline should point back to source artifacts and evidence rather than forward to a guessed next step. | The back-link rule is kept explicit so later child contracts do not have to restate the parent navigation principle. |
| `DOC-WORKFLOW-0001-ST-03` | `Logs plan layer` | `active` | `introduced` | `S0A-2A-R01` | `DOC-WORKFLOW-0001` | `unknown` | `DOC-WORKFLOW-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Logs should convert raw materials into one structured plan layer covering status, what, how, and links. | This release keeps the broad workflow reading even though later child families may own narrower logs-specific rule bodies. |
| `DOC-WORKFLOW-0001-ST-04` | `Labs proof layer` | `active` | `introduced` | `S0A-2A-R01` | `DOC-WORKFLOW-0001` | `unknown` | `DOC-WORKFLOW-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Labs should act as the most granular execution and proof layer through repeatable checks plus result backfills. | The contract keeps the broad refinement role without claiming direct ownership of later labs-family historical backfill work. |
| `DOC-WORKFLOW-0001-ST-05` | `Runbook operational layer` | `active` | `introduced` | `S0A-2A-R01` | `DOC-WORKFLOW-0001` | `unknown` | `DOC-WORKFLOW-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | Runbooks should distill the operational invariants learned from labs into one operator-facing troubleshooting and recovery guide. | This parent clause remains the broad boundary even though `DOC-WORKFLOW-RUNBOOK-0001` now owns one narrower runbook packet. |
| `DOC-WORKFLOW-0001-ST-06` | `ADR decision layer` | `active` | `introduced` | `S0A-2A-R01` | `DOC-WORKFLOW-0001` | `unknown` | `DOC-WORKFLOW-0001` | `unknown` | `unknown` | `ongoing` | `in-force` | ADRs should summarize the decision layer of the chain through context, decision, alternatives considered, and consequences rather than embedding the full lab execution narrative. | The ADR layer remains broad background at this parent level until stronger direct child evidence is admitted. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-0001-CH-01` | `DOC-WORKFLOW-0001` | `introduced` | `none` | `DOC-WORKFLOW-0001-ST-01; DOC-WORKFLOW-0001-ST-02; DOC-WORKFLOW-0001-ST-03; DOC-WORKFLOW-0001-ST-04; DOC-WORKFLOW-0001-ST-05; DOC-WORKFLOW-0001-ST-06` | `unknown` | `2026-04-10` | The first broad workflow parent release is being retained as a chronology-first contract with explicit clause identity so later narrower child packets do not erase the original pipeline boundary. | `S0A-2A-R01` | One initial release row is sufficient because this repair aligns the existing release to the current table model without changing the owned meaning. |

## Release Change

- This release preserves the first broad workflow parent boundary extracted from `S0A-2A`.
- The current repair does not rewrite the owned meaning; it aligns the file to the current chronology-first contract structure by making clause identity, chronology fields, and source-basis anchors explicit.
- This release remains the parent workflow boundary for:
  - one-way refinement from log to lab to runbook to ADR
  - back-linking to source artifacts and evidence
  - broad role assignment across logs, labs, runbooks, and ADRs
- Narrower workflow families may continue to exist beneath this parent path without turning that family hierarchy into a split-release lineage event.

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-0001-ST-01`: Structured documentation should move through one one-way refinement pipeline:
  - `log -> lab -> runbook -> adr`
- `DOC-WORKFLOW-0001-ST-02`: Links in that pipeline should point back to source artifacts such as inputs and evidence rather than acting as loose `where to go next` hints.
- `DOC-WORKFLOW-0001-ST-03`: Logs should convert raw materials into one structured plan layer covering status, what, how, and links.
- `DOC-WORKFLOW-0001-ST-04`: Labs should act as the most granular execution and proof layer through repeatable checks plus result backfills.
- `DOC-WORKFLOW-0001-ST-05`: Runbooks should distill the operational invariants learned from labs into one operator-facing troubleshooting and recovery guide.
- `DOC-WORKFLOW-0001-ST-06`: ADRs should summarize the decision layer of the chain through context, decision, alternatives considered, and consequences rather than embedding the full lab execution narrative.

## Current Reading

- Read this contract when the question is `what workflow-layer rule originally governed how structured docs should refine from raw material into stable decisions?`
- This contract owns the workflow-layer boundary only; narrower mechanism-specific contracts may sit beneath the same broader workflow domain later.

## Reader Notes

- This is a workflow-layer contract preview sourced from issue `S0A/2A`, not from a local source log.
- It intentionally captures the historical contract at the broader `WORKFLOW` layer without rewriting it to match later workflow replacements.
- `DOC-WORKFLOW-LABS` now reads as one narrower family beneath the broader workflow path, not as a release split from this record.
- The file now uses the current chronology-first clause registry model, but it still remains the same first broad release rather than a new later family state.