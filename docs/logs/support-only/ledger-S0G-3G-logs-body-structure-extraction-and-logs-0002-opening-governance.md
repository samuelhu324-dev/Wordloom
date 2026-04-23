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
| `S0G-3G-R01` | `docs/logs/log-S0C-1A-log-extensions.md` | `extracted` | `Structured logs should expose one top-level Decision / Outcome block as the first reader-facing conclusion surface rather than forcing readers to reconstruct the current decision state from later prose.` | `first-sample-only` | `candidate-introduced-clause-for-LOGS-0002` | `cluster with later samples under P2-C1` | This is the strongest candidate clause in `S0C-1A`: it is framed as a reusable rule and not only as local style preference. |
| `S0G-3G-R02` | `docs/logs/log-S0C-1A-log-extensions.md` | `extracted` | `The Decision / Outcome block should keep a stable minimum field set: Decision, Drivers, Non-goals, and Success criteria.` | `first-sample-only` | `candidate-amend-or-introduce-clause-for-LOGS-0002` | `cluster with later samples under P2-C1` | This row is narrower than `R01`: it may become a child clause beneath a broader conclusion-block rule if corroborated. |
| `S0G-3G-R03` | `docs/logs/log-S0C-1A-log-extensions.md` | `extracted` | `Log state should be owned by top-level front matter status rather than repeated per-section draft/stable/archived timelines in the body.` | `first-sample-only` | `candidate-amended-boundary-note-for-LOGS-0002` | `test against LOGS-0001 carry-forward plus later samples` | This looks like a body-structure rule that also touches the current front-matter/body boundary, so later clustering must decide whether it is a new clause or a note-level amendment to existing logs-family scope. |
| `S0G-3G-R04` | `docs/logs/log-S0C-1A-log-extensions.md` | `extracted` | `The body should preserve current effective content only, while historical drift and failed routes should normally leave through git history, legacy, or stub paths instead of remaining as multi-timeline prose.` | `first-sample-only` | `candidate-introduced-clause-for-LOGS-0002` | `cluster with later samples under P2-C1` | This is the clearest long-lived structure-maintenance rule in the sample and may later interact with lifecycle/legacy routing contracts. |
| `S0G-3G-R05` | `docs/logs/log-S0C-1A-log-extensions.md` | `extracted-supporting-evidence` | `Applied examples and copyable template snippets support the rule set, but they currently read as evidence/supporting pattern rather than primary contract meaning.` | `evidence-only-until-corroborated` | `supporting-evidence-only` | `retain in ledger unless later samples make template-level language contract-worthy` | `Applied` and `Example` sections help prove operational usability, but they should not become primary clause text by default. |

## Boundary Test Register

| test id | question | current verdict | trigger to advance | notes |
| --- | --- | --- | --- | --- |
| `S0G-3G-B01` | `Does the repo now have enough repeated modern evidence to open LOGS-0002 as the next DOC-WORKFLOW-LOGS release?` | `not-yet` | `at least one extracted first sample plus additional corroborating sample rows` | `S0C-1A` alone is intentionally insufficient for contract mutation.` |
| `S0G-3G-B02` | `Should LOGS-0001 absorb body-structure rules directly?` | `default-no` | `only revisit if later evidence proves these rules are inseparable from log identity/front matter` | `Current standing keeps LOGS-0001 narrow.` |
| `S0G-3G-B03` | `Would opening LOGS-0002 require a DOC-WORKFLOW-LOGS family register?` | `likely-yes-if-opened` | `explicit verdict that 0002 becomes first-open current reader and 0001 stays reader-relevant in some standing` | `Follow the transition-register template only if family-level reader standing changes.` |

## Next Actions

- Complete `P1-C2-S1`: admit one additional post-cutover log sample so `R01` through `R04` can move from `first-sample-only` toward a repeatability verdict.
- Complete `P2-C1-S1`: cluster `R01` through `R05` into provisional `LOGS-0002` rule buckets and separate likely clauses from support-only evidence.
- Open `P1-C2` only after one more post-cutover modern log sample is selected.