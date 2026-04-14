# governance-contract-record: GC-ATTR-0001

- `record_id`: `GC-ATTR-0001`
- `contract_id`: `PR-EVENT-SOURCE-LOG-ATTRIBUTION-PRECEDENCE`
- `title`: `pr-event source-log attribution must resolve through ordered precedence, fail-closed ambiguity policy, and explicit consume-or-stop handoff`

```yaml
contract_record:
  contract_id: PR-EVENT-SOURCE-LOG-ATTRIBUTION-PRECEDENCE
  status: active
  summary: PR-event source-log attribution must resolve through one ordered precedence rule, stop fail-closed on missing or ambiguous ownership, and emit an explicit consume-or-stop handoff before any downstream mirror verification begins.
  governance_area: attribution-and-provenance-resolution-governance
  applies_to: docs and GitHub automation surfaces that derive one contract-owning source log from a live PR or PR-event payload before downstream contract verification or secondary enforcement proceeds
  enforcement_surface: S0E-4E attribution contract surfaces and later implementation or workflow consumers that replay the same ordered ownership rule without owning a separate front-door contract
  violation_semantics: fail
  introduced_by: S0E-4E/P0-C1-S1
  last_changed_by: S0F-3F/P4-C3-S2
  source_refs:
    - docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md
  supersedes: []
  superseded_by: []
  notes:
    - S0E-4E owns the stable attribution precedence, ambiguity-stop taxonomy, and consume-or-stop handoff contract concentrated here.
    - S0E-7B remains support-only implementation and workflow wiring that emits and consumes this contract without becoming a parallel current record.
    - GC-PRA-0001 and GC-PRG-0001 remain adjacent but narrower: they own PR creation and gate behavior, not PR-event source-log attribution ownership.
```

## Reader Notes

- Current active meaning:
  - attribution may resolve only from the allowed ordered ownership surfaces
  - missing, conflicting, multi-candidate, and invalid-shape ownership all remain fail-closed stop outcomes
  - downstream mirror verification may continue only after one exact repo-relative `source_log_path` has resolved through the explicit consume-or-stop handoff

## Traceability

- Stable attribution owner:
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`