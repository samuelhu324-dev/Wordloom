# DOC-WORKFLOW-0001 structured doc refinement pipeline

```yaml
contract_record:
  contract_id: DOC-WORKFLOW-0001
  record_kind: chronology-first-contract
  status: draft
  summary: Manage structured documentation as a one-way refinement pipeline from log to lab to runbook to ADR, where links point back to source artifacts and evidence rather than forward to a guessed next step.
  governance_area: workflow documentation refinement pipeline governance
  applies_to: structured logs, labs, runbooks, adrs, source-linking semantics, and workflow handoff boundaries across documentation refinement
  enforcement_surface: manual
  violation_semantics: warning
  introduced_by: GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  last_changed_by: GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  source_refs:
    - GitHub issue S0A/2A (#24) (issue-only source; no local log exists in workspace)
  supporting_evidence_refs: []
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
    - The local repo currently has no S0A/2A source log, so this draft stays explicit about issue-only sourcing.
```

## Contract Statement

- Structured documentation should move through one one-way refinement pipeline:
  - `log -> lab -> runbook -> adr`
- Links in that pipeline should point back to source artifacts such as inputs and evidence rather than acting as loose `where to go next` hints.
- Logs should convert raw materials into one structured plan layer covering status, what, how, and links.
- Labs should act as the most granular execution and proof layer through repeatable checks plus result backfills.
- Runbooks should distill the operational invariants learned from labs into one operator-facing troubleshooting and recovery guide.
- ADRs should summarize the decision layer of the chain through context, decision, alternatives considered, and consequences rather than embedding the full lab execution narrative.

## Current Reading

- Read this contract when the question is `what workflow-layer rule originally governed how structured docs should refine from raw material into stable decisions?`
- This contract owns the workflow-layer boundary only; narrower mechanism-specific contracts may sit beneath the same broader workflow domain later.

## Reader Notes

- This is a workflow-layer contract preview sourced from issue `S0A/2A`, not from a local source log.
- It intentionally captures the historical contract at the broader `WORKFLOW` layer without rewriting it to match later workflow replacements.