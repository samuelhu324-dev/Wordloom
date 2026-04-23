# ledger-S0G-3G: logs body-structure extraction and LOGS-0002 opening governance

## Purpose

- This support-only ledger is the mandatory accumulation surface for `S0G-3G`.
- It records sample-by-sample extracted body-structure rules before any `DOC-WORKFLOW-LOGS-*` contract mutation is attempted.
- One new sample should normally add or sharpen rows here rather than opening a sibling source log immediately.

## Operating Rule

- Flow for this lane: `source log -> this ledger -> contract decision`.
- `DOC-WORKFLOW-LOGS-0001` should not be widened from one sample directly.
- `DOC-WORKFLOW-LOGS-0002` should open only if repeated rows here justify the next release in the same `DOC-WORKFLOW-LOGS` family.

## Sample Intake Table

| row id | source sample | sample status | extracted candidate rule | repeatability verdict | contract impact verdict | next write-back target | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0G-3G-R01` | `docs/logs/log-S0C-1A-log-extensions.md` | `selected-not-yet-extracted` | `Decision / Outcome block plus single top-level status ownership may be a reusable post-cutover logs body rule` | `pending-more-samples` | `candidate-next-release-LOGS-0002-not-direct-LOGS-0001-patch` | `P1-C1 extraction write-back in S0G-3G, then later `LOGS-0002` boundary test` | First concrete sample selected because it states the rule set clearly, but the lane still needs extraction details and additional corroborating samples before the family can advance from `0001` to `0002`. |

## Boundary Test Register

| test id | question | current verdict | trigger to advance | notes |
| --- | --- | --- | --- | --- |
| `S0G-3G-B01` | `Does the repo now have enough repeated modern evidence to open LOGS-0002 as the next DOC-WORKFLOW-LOGS release?` | `not-yet` | `at least one extracted first sample plus additional corroborating sample rows` | `S0C-1A` alone is intentionally insufficient for contract mutation.` |
| `S0G-3G-B02` | `Should LOGS-0001 absorb body-structure rules directly?` | `default-no` | `only revisit if later evidence proves these rules are inseparable from log identity/front matter` | `Current standing keeps LOGS-0001 narrow.` |
| `S0G-3G-B03` | `Would opening LOGS-0002 require a DOC-WORKFLOW-LOGS family register?` | `likely-yes-if-opened` | `explicit verdict that 0002 becomes first-open current reader and 0001 stays reader-relevant in some standing` | `Follow the transition-register template only if family-level reader standing changes.` |

## Next Actions

- Complete `P1-C1-S1`: extract the concrete body-structure rules from `S0C-1A` into finer-grained notes.
- Complete `P1-C1-S2`: sharpen `S0G-3G-R01` from `selected-not-yet-extracted` to explicit extracted-rule rows if needed.
- Open `P1-C2` only after one more post-cutover modern log sample is selected.