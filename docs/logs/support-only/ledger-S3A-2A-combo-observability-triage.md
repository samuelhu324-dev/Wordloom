# ledger-S3A-2A-combo-observability-triage

```yaml
support_only_contract_release_ledger:
  ledger_id: ledger-S3A-2A-combo-observability-triage
  ledger_kind: support-only-contract-release-ledger
  status: draft
  owner_lane: S4G-1A
  created_at: 2026-04-25
  reviewed_at: 2026-04-25
  accepted_at: pending
  source_id: S3A-2A
  source_ref: GitHub issue S3A-2A (#37) plus child issues #38, #39, #40, #41, #45, #46, #47, #48, #49, and #51 (issue-first mixed source; only part of the packet survives as local logs, labs, and runbook material)
  source_scope: mixed issue-first packet covering observability triage, shared-key evidence, replayable failure drills, daemon-ready worker migration, automation harnessing, GitHub Actions parity, and the later retained failure-drills runbook surface
  target_reading_goal: show whether the S3A-2A packet can be consolidated under one parent ledger with explicit child rows, no new SUP round, and one bounded S4G-1A assessment path before any later downstream contract mutation is considered
```

## Decision Frame

- This ledger is a first consolidation and routing draft for `S3A-2A`, not a completed write-back.
- The current draft default is:
  - treat `#37` as the issue-first parent packet instead of recreating missing source logs for each child issue
  - keep `#38`, `#39`, `#40`, `#41`, `#45`, `#46`, `#47`, `#48`, `#49`, and `#51` as explicit child rows under the same parent packet
  - use surviving local logs, the surviving lab, and the retained runbook as row evidence where they exist, but do not let those later files replace the parent issue packet
  - record an explicit `no-SUP-for-now` verdict because the issue bodies plus surviving repo-local sources are already strong enough to make the row split reviewable
  - defer direct `DOC-WORKFLOW-*` mutation until `S4G-1A` decides which row is the first bounded downstream candidate
- The purpose of this ledger is to make the blurred old `logs/labs/runbook` packet reviewable as one parent-owned mixed source under the current `S4G-1A` lane.

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `ledger-S3A-2A-combo-observability-triage` | `docs-governance` | `role:workflow-ledger-maintainer` | `parent-review-pending-final-acceptance` | `role:workflow-reviewer` | `role:docs-governance-approver` | This ledger is the current parent routing surface for the mixed `S3A-2A` packet under `S4G-1A`. |
| `S4G-1A` | `S4 runtime governance` | `role:s4-history-packet-maintainer` | `packet-review-in-progress` | `role:workflow-reviewer` | `role:docs-governance-approver` | `S4G-1A` owns the current packet-selection and verdict step, but not yet any downstream contract mutation from this packet. |

## Routing And Consumption Table

| row id | source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R01` | `GitHub issue S3A-2A (#37)` | observability triage fixes the operating chain `metrics -> tracing -> structured logs`, keeps shared pivots explicit, and treats logs or audit events as the primary truth surface | `S4 runtime observability governance` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as the parent packet boundary until a narrower downstream row is selected under `S4G-1A` | This row is the packet root and should not be replaced by any later child file. |
| `S3A-2A-R02` | `GitHub issue #38` (`S3A/2A/1A`) | shared keys align metrics, traces, and structured logs tightly enough for repeatable triage | `DOC-WORKFLOW-LABS` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep attached to the parent packet as the first bounded proof surface for the triage loop | This is strong evidence, but it still reads as packet support rather than one standalone current contract mutation. |
| `S3A-2A-R03` | `GitHub issue #39` (`S3A/2A/2A(3A)`) plus surviving manual evidence in `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | transient ES-outage drill proves the triage path can move from metrics to batch trace to single-event diagnosis with stable pivots and retained evidence | `DOC-WORKFLOW-LABS` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as one explicit lab row under the parent packet rather than as one separate source packet | The issue body and surviving lab text together are sufficient for review without a separate SUP. |
| `S3A-2A-R04` | `GitHub issue #40` (`S3A/2A/3A`) plus surviving manual and automated evidence in `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | deterministic ES-429 injection turns observability failure handling into one queryable, repeatable packet with stable event ids, startup traces, and retry classification | `DOC-WORKFLOW-LABS` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as the main `expB` row and do not split manual versus automated variants into separate parents | This row preserves one bounded experiment packet with both issue-only and surviving lab support. |
| `S3A-2A-R05` | `GitHub issue #41` (`S3A/2A/1B`) | the missing source-log slice still fixes one durable bridge rule: move from ad-hoc manual testing into replayable `run/verify/export/clean` shape without pretending the old source log survived | `S4 runtime drill automation` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as issue-only evidence and do not fabricate a replacement source log | This row exists specifically because the issue text survived while the local source log did not. |
| `S3A-2A-R06` | `GitHub issue #45` plus `docs/logs/log-S3A-2A-2B-daemon-ready-worker-migration.md` | daemon-ready worker migration fixes the stable operator entrypoint problem and separates current runnable entrypoints from legacy implementation reuse | `DOC-WORKFLOW-RUNBOOK` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | hold as one operator-entrypoint row until `S4G-1A` decides whether this is only lineage support or one later runbook-sharpening packet | This row is operationally important and should stay visible even though it is not the first promotion candidate yet. |
| `S3A-2A-R07` | `GitHub issue #46` | the ES-429 stress-test packet acts as one negative-control row showing why unstable stress reproduction should not replace deterministic fault injection as the primary proof path | `support-only` | `no-contract` | `none-source-only` | `support-only` | `draft` | `none` | `none` | keep attached as supporting contrast for `R04` and `R08` rather than one standalone downstream promotion target | This row matters for judgment, but not as the first current contract candidate. |
| `S3A-2A-R08` | `GitHub issue #47` plus `docs/logs/log-S3A-2A-3B-automated-failure-drills.md` | failure drills become a repeatable automation harness with machine-verifiable `run/verify/export/clean` entrypoints and structured evidence bundles | `S4 runtime drill automation` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as a parent-owned automation row; later verdict may classify it as runbook-sharpening or contract-sharpening | This row is one of the strongest downstream candidates because it already names stable operator paths and audit outputs. |
| `S3A-2A-R09` | `GitHub issue #48` plus `docs/logs/log-S3A-2A-3B-automated-failure-drills.md` | the automation log layer productizes the drills packet and records the explicit `no-human-clickflow` operating shape for retained evidence | `S4 runtime drill automation` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep distinct from `R08` because the DoD issue sharpens the governance intent while the local log preserves the longer reader-facing body | This row is not redundant with `R08`; it fixes the governed productization claim. |
| `S3A-2A-R10` | `GitHub issue #49` plus `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md` | local and CI failure-drills execution converge behind one harness, one evidence bundle shape, and one end-to-end `scenario=all` regression path | `S4 runtime drill automation` candidate | `new-family` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as the broad integration row and do not split dashboard, harness, and CI parity into separate parents | This row is one likely bridge from old observability triage into current runtime-owned drill governance. |
| `S3A-2A-R11` | `GitHub issue #51` plus `docs/logs/log-S3A-2A-4B-1A-git-actions.md` | GitHub Actions parity fixes repo-root execution, env loading, compose-based dependency bootstrapping, and repeatable CI evidence for the same drills packet | `S4 runtime drill automation` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as a narrower CI-parity row under the same parent packet instead of reopening it as one independent family | This row is narrower than `R10` and may later sharpen one CI-facing operator contract, but not yet. |
| `S3A-2A-R12` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | the surviving lab now acts as the packet-level evidence spine for the classic A-H drills, manual proofs, automated snapshots, and later scenario expansion | `DOC-WORKFLOW-LABS` candidate | `revise-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as one retained evidence surface that supports `R03`, `R04`, `R07`, `R08`, and `R11` rather than replacing them | This file is evidence-rich, but it is not the parent packet by itself. |
| `S3A-2A-R13` | `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | the retained runbook fixes one stable operator path for `run -> verify -> export -> clean`, evidence-bundle handling, and local versus CI troubleshooting | `DOC-WORKFLOW-RUNBOOK` candidate | `new-release` | `none-source-only` | `keep-in-issue` | `draft` | `none` | `none` | keep as the strongest downstream operator surface and the first likely later narrow packet under `S4G-1A` | This is currently the clearest candidate for a later `runbook-sharpening` verdict. |

## Row Id Map

- `S3A-2A-R01`: parent observability triage packet
- `S3A-2A-R02`: shared-key proof row
- `S3A-2A-R03`: transient ES outage drill row
- `S3A-2A-R04`: deterministic ES-429 experiment row
- `S3A-2A-R05`: missing-source replayable-test bridge row
- `S3A-2A-R06`: daemon-ready worker migration row
- `S3A-2A-R07`: ES-429 stress negative-control row
- `S3A-2A-R08`: automation harness row
- `S3A-2A-R09`: automated failure-drills governance row
- `S3A-2A-R10`: failure-drills plus dashboard plus CI integration row
- `S3A-2A-R11`: GitHub Actions parity row
- `S3A-2A-R12`: surviving lab evidence spine row
- `S3A-2A-R13`: retained operator runbook row

## Row Chronology Audit

| row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the surviving parent issue text proves packet shape, but this ledger does not yet defend one stable creation timestamp for #37` | The parent row is good enough for routing, but not yet for precise chronology claims. |
| `S3A-2A-R02` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `issue-only row preserved through #38 only` | The shared-key row is strong on content and weak on defended timestamps. |
| `S3A-2A-R03` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `issue-only row sharpened by later surviving lab text` | The outage drill row is supported by the lab body, but its issue-level chronology still remains indirect. |
| `S3A-2A-R04` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `issue-only row sharpened by later surviving lab text` | The deterministic injection row is content-defended first and chronology-defended later if needed. |
| `S3A-2A-R05` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the row survives only through issue #41` | This is the clearest issue-only row in the packet. |
| `S3A-2A-R06` | `unknown` | `2026-02-13` | `2026-02-13` | `ongoing` | `day` | `the surviving log preserves a defended day-level creation date` | The local log gives this row stronger chronology than most of the issue-only rows. |
| `S3A-2A-R07` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `stress-test row survives through issue text only` | This row should not be over-read as a chronology anchor. |
| `S3A-2A-R08` | `unknown` | `2026-02-14` | `2026-02-14` | `ongoing` | `day` | `the surviving automation log preserves a defended day-level creation date` | The automation row is one of the first stable local chronology anchors in the packet. |
| `S3A-2A-R09` | `unknown` | `2026-02-14` | `2026-02-14` | `ongoing` | `day` | `the surviving automation log preserves the same day-level chronology as the DoD child issue` | This row shares chronology with `R08` but not the same packet meaning. |
| `S3A-2A-R10` | `unknown` | `2026-02-15` | `2026-02-15` | `ongoing` | `day` | `the surviving 4B log preserves a defended day-level update window` | This row is one stable chronology anchor for the integrated drill packet. |
| `S3A-2A-R11` | `unknown` | `2026-02-15` | `2026-02-15` | `ongoing` | `day` | `the surviving 4B-1A log preserves a defended day-level update window` | This row is narrower than `R10` but keeps the same broad era. |
| `S3A-2A-R12` | `unknown` | `2026-02-13` | `2026-02-13` | `ongoing` | `day` | `the surviving lab preserves a defended day-level creation date` | The lab evidence spine now serves as a local chronology anchor for several child rows. |
| `S3A-2A-R13` | `unknown` | `2026-02-15` | `2026-02-15` | `ongoing` | `day` | `the retained runbook preserves a defended day-level decision date only` | The operator runbook row is the clearest downstream chronology anchor in the packet. |

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-GOV-01` | `contribution-event` | `S3A-2A mixed source` | `unknown` | `none-current-state` | `2026-04-25` | `GitHub issue #37 plus child issues #38/#39/#40/#41/#45/#46/#47/#48/#49/#51` | The original packet remains issue-first even though several local logs and one local runbook survive. |
| `S3A-2A-GOV-02` | `routing-writeback-event` | `ledger-S3A-2A-combo-observability-triage` | `role:packet-reviewer` | `current-routing-draft-fixed` | `2026-04-25` | `S4G-1A/P1-C1-S1S2` | This ledger now fixes one explicit row split for the old mixed `logs/labs/runbook` packet instead of leaving the packet dispersed across child files only. |
| `S3A-2A-GOV-03` | `routing-writeback-event` | `S3A-2A sharpening strategy` | `role:packet-reviewer` | `no-sup-verdict-fixed` | `2026-04-25` | `issue bodies plus surviving repo-local logs/lab/runbook are sufficient for current row review` | The current packet verdict is `no-SUP-for-now`; later work should select narrower downstream packets rather than reopen supplement staging by default. |

## Deferred Slices

- decide whether `R13` is the first bounded downstream `runbook-sharpening` packet under `S4G-1A`
- decide whether `R06` should remain lineage support only or become a second operator-path candidate after `R13`
- decide whether `R08` through `R11` should remain one consolidated drill-automation cluster or later split into one narrower CI-parity packet and one broader drill-harness packet
- decide whether `R02` through `R05` should remain parent-level issue support or later condense into one historical labs packet

## Reader Notes

- This ledger treats `S3A-2A` as one issue-first mixed packet whose child issues and surviving local files should be read together rather than as independent replacement source logs.
- The current reading path is: parent issue `#37` fixes the packet boundary, child issues and surviving logs fill the row map, and `S4G-1A` owns the next bounded verdict instead of sending these rows directly into existing `DOC-WORKFLOW-*` contracts.
- Under the current draft, `R13` is the strongest later downstream candidate, while `R06`, `R08`, `R09`, `R10`, and `R11` remain the main adjacent operator-path and automation cluster under the same parent packet.