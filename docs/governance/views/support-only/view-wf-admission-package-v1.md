# WF Admission Package v1

## Purpose

- This view explains why the `A2` lane under `S0F-3F` admits one new current workflow-failure area and one current record instead of treating the whole `S0E-7D` through `S0E-7G` family as a multi-record workflow landing.
- It exists so readers can distinguish the admitted `WF` taxonomy contract from the later thin-gate, wrapper, and `workflow_dispatch` transport surfaces that replay the same semantics.

## Area Choice

- Chosen area code:
  - `WF`
- Chosen current record:
  - `GC-WF-0001`
- Chosen contract id:
  - `PUBLISH-VERIFY-REMEDIATION-FAILURE-TAXONOMY-AND-HANDLING`
- Why `WF` was admitted as-is:
  - the current surface is broader than one single remediation-stage boundary, but narrower than a generic workflow-orchestration bucket
  - the admitted surface owns the stable failure taxonomy, ordered replay/backfill contract, and explicit handling semantics reused by later thin-gate and wrapper surfaces
  - the later `S0E-7E` through `S0E-7G` records remain implementation, wrapper, and transport layers rather than independent front-door rules

## Current Boundary

- `GC-WF-0001` owns:
  - strong-structure versus weak-structure failure taxonomy
  - ordered replay/backfill contract
  - explicit block, replayable, manual, and reconciliation handling semantics
- `GC-WF-0001` does not own:
  - thin gate normalization as a separate current record
  - read-only wrapper adoption or GitHub-side `workflow_dispatch` packaging as separate current records
  - the narrower multi-item remediation-stage boundary already concentrated in `GC-REMED-0001`

## Executed Admission Writes

- Add `WF` to the front-door glossary and controlled area-code dictionary in `INDEX.md`
- Add one current front-door row for `GC-WF-0001`
- Create the current record file `GC-WF-0001-publish-verify-remediation-failure-taxonomy-and-handling.md`
- Update the `WF` family sweep surfaces so `A2` reads as executed instead of only packaged

## Reader Notes

- This view is an admission explanation surface, not the current registry itself.
- `INDEX.md` remains the front door for current-state reading.
- `GC-WF-0001` is the current contract body.
- `S0E-7D` remains the primary semantic source log behind this admitted current record.

## Source Refs

- `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
- `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
- `docs/logs/log-S0F-3C-governance-contract-series-audit-and-admission.md`
- `docs/governance/contracts/GC-WF-0001-publish-verify-remediation-failure-taxonomy-and-handling.md`