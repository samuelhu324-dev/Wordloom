# ledger-S3A-1A-third-leg-tracing-with-jaegar

```yaml
support_only_contract_release_ledger:
  ledger_id: ledger-S3A-1A-third-leg-tracing-with-jaegar
  ledger_kind: support-only-contract-release-ledger
  status: draft
  owner_lane: S0G-3G
  created_at: 2026-04-24
  reviewed_at: 2026-04-24
  accepted_at: pending
  source_id: S3A-1A
  source_ref: GitHub issue S3A-1A (#33) plus child issues #34 and #35 (issue-only source; no local structured source log exists in workspace)
  source_scope: mixed issue-only archaeology packet covering third-leg tracing introduction, child Jaeger-oriented labs or manual-drill slices, and later retained legacy log, runbook, and ADR evidence surfaces
  target_reading_goal: show how the S3A-1A packet should first split into reviewable tracing, labs or manual-drill, runbook, and ADR rows before any screenshot-backed SUP or downstream contract mutation is considered
```

## Decision Frame

- This ledger is a first routing and archaeology draft, not a completed write-back.
- The current draft default is:
  - keep `#33` as the issue-only parent tracing-boundary row
  - keep `#34` and `#35` as child labs or manual-drill rows under the same parent packet instead of inventing child source logs
  - keep the later legacy `run-S3A` and `adr-S3A` surfaces visible as separate rows because they preserve durable operator and decision meaning beyond the issue hierarchy alone
  - treat the legacy `log-S2A-observability-tracing.md` body as direct tracing evidence for the parent packet, but do not pretend it is the missing `S3A-1A` source log itself
  - defer screenshot-backed SUP admission and all contract mutation until this row split is reviewed
- The purpose of this draft is to make the missing-log archaeology packet reviewable under the current parent-ledger model rather than leaving it as one prose-only exception.

## Routing And Consumption Table

| row id | source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-1A-R01` | `GitHub issue S3A-1A (#33)` plus `legacy/from_structured_docs/from-logs/v2-logs/log-S2A-observability-tracing.md` | tracing becomes the missing third observability leg, including API to outbox to worker propagation, trace context carry-forward, and logs-to-traces correlation | `DOC-WORKFLOW-LOGS` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | hold as the parent tracing row until direct-markdown sharpening and later family-boundary review decide whether the durable meaning belongs in the logs family, a legacy logs surface, or a still-mixed parent read | The issue hierarchy establishes the packet root, while the retained tracing markdown supplies the strongest surviving technical body. |
| `S3A-1A-R02` | `GitHub child issue #34` (`S3A/1A/1A`) plus the same tracing packet context | preserve the earliest Jaeger-facing experiment or manual-drill slice without claiming it was already a durable contract or stable runbook | `DOC-WORKFLOW-LABS` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as a child labs or manual-drill row until screenshot or markdown SUP evidence proves whether this slice should remain historical review only or become one narrow labs reader | The current evidence is strong enough to keep the row visible, but not strong enough to promote it directly. |
| `S3A-1A-R03` | `GitHub child issue #35` (`S3A/1A/1B`) plus the same tracing packet context | preserve the earliest new-spans or worker-side trace-visibility slice without claiming it was already one complete structured-log packet | `DOC-WORKFLOW-LABS` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as a second child labs or manual-drill row until later SUP evidence proves whether it should stay attached to the parent review only or move into one narrow labs reader | This row remains distinct from `R02` because the surviving child issue title suggests a separate bounded experiment focus. |
| `S3A-1A-R04` | `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | failure-drill automation, evidence-bundle packaging, and stable operator run/verify/export/clean workflow form a durable runbook layer beyond the issue-only parent | `DOC-WORKFLOW-RUNBOOK` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep this row draft-only until a later direct-markdown SUP packet decides whether the runbook layer should stay background, become historical review, or justify one narrower child-opening packet | The retained runbook is clearly later and broader than `#33`, so it stays separate from the issue-only parent row instead of replacing it. |
| `S3A-1A-R05` | `legacy/from_structured_docs/from-adrs/adr-S3A-observability-v2.md` | the observability packet already had one durable decision-summary layer that separates metrics, tracing, structured logs, and evidence-bundle automation from execution details | `DOC-WORKFLOW-ADR` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep this row draft-only until a later direct-markdown SUP packet decides whether the ADR layer should remain supporting context or justify one narrow child-opening packet | The retained ADR is clearly decision-summary material and therefore should not be flattened into the runbook or parent tracing rows. |

## Row Id Map

- `S3A-1A-R01`: parent tracing-boundary packet
- `S3A-1A-R02`: child Jaeger electrification labs or manual-drill row
- `S3A-1A-R03`: child new-spans labs or manual-drill row
- `S3A-1A-R04`: later failure-drills runbook row
- `S3A-1A-R05`: later observability ADR row

## Deferred Slices

- screenshot-backed SUP admission for the `#33/#34/#35` hierarchy and titles
- direct-markdown SUP review for the retained tracing markdown body
- later decision on whether `R02` and `R03` should remain historical labs review, become one merged labs packet, or stay attached only as parent-ledger child rows
- later decision on whether `R04` and `R05` justify narrow child-opening packets or remain parent-level supporting surfaces

## Row Chronology Audit

| row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-1A-R01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the screenshot-backed issue hierarchy proves existence, but the surviving packet does not yet defend one stable creation timestamp for #33` | The parent tracing row is evidence-rich enough for routing, but chronology still needs later screenshot or issue export sharpening. |
| `S3A-1A-R02` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `child issue #34 is currently preserved only through screenshot-backed hierarchy evidence` | The child labs or manual-drill row remains chronology-deferred until a later screenshot or markdown SUP reconstructs its narrower timing. |
| `S3A-1A-R03` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `child issue #35 is currently preserved only through screenshot-backed hierarchy evidence` | The second child labs or manual-drill row remains chronology-deferred for the same reason as `R02`. |
| `S3A-1A-R04` | `unknown` | `2026-02-15` | `2026-02-15` | `ongoing` | `day` | `the retained runbook preserves a defended day-level decision date only` | The later runbook row already preserves one stable recorded date, but that date does not replace the earlier issue-only parent chronology. |
| `S3A-1A-R05` | `unknown` | `2026-02-15` | `2026-02-15` | `ongoing` | `day` | `the retained ADR preserves a defended day-level decision date only` | The later ADR row already preserves one stable recorded date, but that date does not replace the earlier issue-only parent chronology. |

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-1A-GOV-01` | `contribution-event` | `S3A-1A mixed source` | `unknown` | `none-current-state` | `2026-04-24` | `GitHub issue S3A-1A (#33) plus child issues #34/#35` | The original packet remains defended only through issue hierarchy and retained legacy evidence; current routing review therefore stays on this parent ledger. |
| `S3A-1A-GOV-02` | `routing-writeback-event` | `ledger-S3A-1A-third-leg-tracing-with-jaegar` | `role:packet-reviewer` | `current-routing-draft-fixed` | `2026-04-24` | `S0G-3G/P1-C3-S1; S0G-3G/P2-C3-S1` | The parent ledger now fixes one explicit row split for the missing-log archaeology packet instead of leaving the packet as one unstructured exception. |
| `S3A-1A-GOV-03` | `evidence-deferral-event` | `S3A-1A screenshot and markdown sharpening rounds` | `role:packet-reviewer` | `sup-and-contract-work-deferred` | `2026-04-24` | `current draft rule under S0G-3G` | The row split is admitted now, but later screenshot-backed and direct-markdown sharpening still remain separate follow-up work rather than being collapsed into the initial parent draft. |

## Reader Notes

- This ledger now makes the `S3A-1A` exception reviewable without inventing missing structured source logs.
- The current reading is deliberately two-step: first read this parent ledger for the draft split, then use later SUP packets if and when screenshot-backed or direct-markdown sharpening is admitted.
- `R02` and `R03` remain child labs or manual-drill rows under the same parent packet; `R04` and `R05` remain later runbook and ADR rows that should sharpen the packet without replacing the issue-only parent source.