# log-S0G-4A (Phase 4A: contract boundary map and parent-child clause-flow governance)

---

**id**: `S0G-4A`
**kind**: `log`
**title**: `contract boundary map and parent-child clause-flow governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Contract, Evidence, epic/s0, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-3E-workflow-github-issues-round-attempt-chronology-and-family-template-governance.md`
  **reference_log_1**: `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  **reference_log_2**: `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`
  **reference_log_3**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_4**: `docs/logs/_template-support-only-contract-release-ledger.md`
  **reference_log_5**: `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  **reference_log_6**: `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
  **reference_log_7**: `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0002-labs-snapshot-evidence-package-governance.md`
  **reference_log_8**: `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  **reference_log_9**: `docs/logs/support-only/ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/4a`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-22`
**updated**: `2026-04-22`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while this lane is still fixing the reader model and template scope rather than executing one final write-back batch.
- `reviewed` should remain `pending` until the repo fixes one defended contract-facing rule for current boundary reading versus statement-flow history and confirms whether ledger / SUP template changes are required.

## Decision / Outcome

**Decision**:

- `S0G-4A` opens as the next bounded follow-up after `S0G-3E`: the current chronology-first contract model already separates `current statement state` from `statement evolution`, but parent contracts still lack one explicit reader-facing surface that tells readers whether a broad clause is parent-owned, delegated to a child, backfilled into the current reader, or unrelated to any child family.
- This lane first treats the problem as a template and rule question, not as an `ADR` sample-writing question. The immediate deliverable is one defended contract-template usage rule plus, if justified, one optional parent-only table such as `Current Boundary Map` or equivalent naming that makes parent/child reading boundaries explicit.
- The lane must evaluate the full write path in the existing repo order:
  - `SUP -> parent ledger -> child contract -> parent contract`
  - Any new boundary-flow rule that materially changes how contracts are read must be checked against parent-ledger and SUP-ledger responsibilities before it is treated as contract-only policy.
- The first experimental application in this lane is now fixed:
  - first on `DOC-WORKFLOW-0001`
  - then on `DOC-WORKFLOW-LABS-0002`
  - and only after those experiments are coherent should the repo open `S0A-2A` ADR evidence as the next fresh sample for a new child-contract scenario.

**Default choices (phase defaults / v1)**:

- Treat `statement label` as the short label for the clause's current meaning only; it must not become the place where split, return, re-absorb, or child-ownership history is encoded.
- Treat `Statement Evolution Table` as the default home for `go / come back / split again / absorbed / history-backfilled / replaced` chronology.
- Treat any new `Current Boundary Map` as parent-facing and reader-facing only:
  - it explains the current reading boundary
  - it does not replace release lineage in frontmatter
  - it does not replace statement evolution history
  - it does not replace source routing in ledgers
- Default starting assumption for this lane: no mandatory new routing column should be added to the parent-ledger or SUP templates unless the experiments prove that contract-only surfaces still leave the `SUP -> LEDGER -> child -> parent` path ambiguous.
- If the experiments show that ledgers must preview downstream boundary standing, prefer one narrow optional field or rollup note rather than duplicating full contract-boundary tables into ledgers.
- Draft-stage source logs remain the concentrated surface while template wording and experimental write-back order are still moving; do not export a new stable contract or view prematurely just to shorten the source log.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.

## PR Summary Inputs (optional)

- This packet is expected to drive template and sample rewrites, so the review summary should focus on reader clarity, parent/child boundary semantics, and whether ledger-class templates need one bounded follow-on adjustment.

**PR summary bullets**:

- Fix one explicit reader model for parent contracts so current clause meaning is no longer mixed with clause-flow history.
- Test the model on `DOC-WORKFLOW-0001` and `DOC-WORKFLOW-LABS-0002` before opening a new `ADR` child sample.
- Decide whether the existing `SUP -> parent ledger -> child contract -> parent contract` chain needs any bounded ledger or SUP template addition after the contract experiments.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-4A-contract-boundary-map-and-parent-child-clause-flow-governance.md`
- Runbook: ``
- Evidence artifact: ``

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/governance/contracts/_template-contract-record.md`
- `P0-C1-S2` | artifact: `docs/logs/_template-support-only-contract-release-ledger.md`
- `P1-C1-S1` | artifact: `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `contract-template + ledger/SUP integration audit + log-retained core` lane.
- The expected first landing is one defended template rule and one bounded experiment packet; whether any stable contract-template rewrite or support-only template rewrite should leave this log depends on the experiment results rather than being assumed up front.

**Outlet ownership**:

- `contract`: expected landing surface for the contract-template usage rule and any optional parent-only boundary-map section once the experiment is stable
- `runbook`: no-op by default
- `view`: no-op by default; a separate reader summary should wait until the experiment proves one reusable view need beyond the source log
- `index/front-door`: no-op by default
- `disposition/placement`: support-only ledger and SUP template impact assessment remains here until the experiments show whether any template rewrite is justified
- `log-retained core`: the lane boundary, experiment order, findings, and evidence ledger remain here

## Definitions (optional)

- **current boundary map**: one reader-facing parent-contract table that says how each broad clause should currently be read relative to child families, for example `parent-owned`, `delegated-summary`, `child-owned`, `shared-reader`, `backfilled-history-only`, or `no-child-relation`.
- **statement-flow history**: the chronology of clause split, carry-forward, amendment, absorption, historical backfill, return flow, or replacement recorded through statement-evolution rows rather than packed into statement labels.
- **parent reading boundary**: the current rule for what the broader parent still owns directly versus what it now only summarizes or points toward.
- **return flow**: a later state where meaning that was once narrowed into child or sibling surfaces becomes visible again in a broader current reader without erasing the earlier split history.
- **full write path**: the existing repo order `SUP -> parent ledger -> child contract -> parent contract`.
- **reader guesswork**: any situation where a reader must infer from prose notes alone whether a clause is still parent-owned, now child-owned, or merely retained as historical background.

## Constraints

- Do not overload `statement label` with lineage, routing, or ownership-handoff prose.
- Do not use a new parent-only boundary table to replace statement evolution, release lineage, or source-routing ledgers.
- Do not jump directly to the `S0A-2A ADR` sample before the template and experiment rules are stable enough to judge that sample consistently.
- Do not widen ledger or SUP templates by default if the experiments can be explained cleanly at contract level only.
- Do not let `DOC-WORKFLOW-0001` and `DOC-WORKFLOW-LABS-0002` drift into incompatible experiment shapes; the point of the lane is one reusable reader model, not two local exceptions.

## Scope

- `P0`: contract-template rule and evaluation criteria for current boundary reading versus statement-flow history
- `P1`: experiment on `DOC-WORKFLOW-0001`, including one candidate parent-facing boundary-map section and one explicit reading rule for broad workflow clauses
- `P2`: experiment on `DOC-WORKFLOW-LABS-0002`, including whether `history-backfilled` clause rows and carried-forward clauses still read clearly without a parent-only boundary map
- `P3`: decide whether parent-ledger and SUP templates need any bounded follow-up fields or notes after the two experiments
- `P4`: only if `P0-P3` stabilize, open the next fresh `S0A-2A ADR` sample lane
- `P5`: assess remaining contracts and ledgers against the now-written-back reader-model rule before any repo-wide normalization batch opens

## Success Criteria (DoD)

- One explicit rule states that `statement label` names current clause meaning only.
- One explicit rule states that `go / return / split again / absorbed / history-backfilled` chronology belongs in `Statement Evolution Table` rather than in labels.
- One explicit reader model exists for parent contracts when broad clauses and narrower child families coexist.
- `DOC-WORKFLOW-0001` can show broad workflow clauses without forcing readers to guess whether a child now owns the narrow rule body.
- `DOC-WORKFLOW-LABS-0002` can show `history-backfilled`, `carried-forward`, `amended`, and `introduced` rows without confusing current clause meaning with clause chronology.
- The lane records one explicit verdict on whether the existing parent-ledger and SUP templates are already sufficient, need only note-level clarification, or need one bounded structural addition.
- The next sample order is explicit: `ADR` sample work does not begin until the template and experiment verdicts are fixed.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the parent-contract reader model is explicit;
  - the `WORKFLOW-0001` and `LABS-0002` experiments are complete enough to test it;
  - the ledger / SUP impact verdict is explicit;
  - the repo knows whether the next step is template write-back only or a new `ADR` sample lane.
- `stable` for this lane does not require the `ADR` sample itself to be finished; it requires the template and experiment rules to be fixed enough that the `ADR` sample will not reopen the same structural question immediately.

## P0 (Contract rule | v1)

### P0-C1-S1 (Fix statement-label responsibility)

- `statement label` should describe the current clause identity only.
- Under this rule, parent/child routing state, split history, absorbed history, or return-flow history must not be encoded as pseudo-lineage inside the label.

### P0-C1-S2 (Fix statement-flow history placement)

- `Statement Evolution Table` is the default surface for clause-flow history such as `introduced`, `carried-forward`, `amended`, `split`, `merged`, `history-backfilled`, `replaced`, `retired`, and any later return-flow pattern.
- Under this rule, readers should be able to reconstruct clause history from evolution rows without forcing the current statement table to double as a chronology ledger.

### P0-C1-S3 (Fix the parent-reader gap and evaluation rule)

- Parent contracts may use one optional parent-only section such as `Current Boundary Map` when the current statement table plus statement evolution table still leaves parent/child ownership unclear to a bounded reader.
- This lane must evaluate that section first on `WORKFLOW-0001`, then against `LABS-0002`, before deciding whether the contract template should recommend it and whether ledgers need any downstream clarification.

### P0-C1-S4 (Fix the full write-path evaluation order)

- Any template change in this lane must be reviewed against the current repo order:
  - `SUP -> parent ledger -> child contract -> parent contract`
- Under this rule, `P3` must answer whether the new contract-reader model remains contract-local or whether parent ledgers / SUP ledgers need one bounded addition to preserve handoff clarity.

### P0-C2-S1 (Write verified reader-model rule back into the contract template)

- The contract template should explicitly distinguish two different optional reader-facing aids:
  - `Current Boundary Map` for broader parent contracts that need one current ownership or delegation summary across child readers
  - `Current Reader Shape` for narrow current readers that need one explanation of mixed clause origins inside the same current release

### P0-C2-S2 (Write section-order and statement-label limits back into the contract template)

- The contract template should explicitly say that `statement label` names current clause meaning only and must not carry lineage or routing semantics.
- The recommended body order should place any optional boundary or reader-shape surface ahead of `Statement Evolution Table`, `Release Change`, and the readable current statement so readers see the current reading rule before scanning chronology details.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0G-4A/P0-C1-S1S4: fix clause-flow and boundary-map evaluation rule`
- `S0G-4A/P0-C2-S1S2: write verified reader model back into contract template`
- `S0G-4A/P1-C1-S1: apply parent-boundary experiment to workflow-0001`
- `S0G-4A/P2-C1-S1: test labs-0002 backfill reading against new rule`
- `S0G-4A/P3-C1-S1: decide ledger and sup template impact`

**Branch convention**:

- Prefer one `S0G-*` branch if this lane stays coupled to the current `S0G` docs-management sequence.
- If the actual execution packet becomes a narrower contract-template-only rewrite separated from other `S0G` work, a short-lived child branch under the active `S0G-*` lane is acceptable.

## Plan (draft)

### P1 (WORKFLOW parent experiment)

- `P1-C1-S1`: draft one candidate parent-only `Current Boundary Map` for `DOC-WORKFLOW-0001`
- `P1-C1-S2`: rewrite `WORKFLOW-0001` statement notes and current reading so broad clauses and child-boundary meaning no longer require guesswork

### P2 (LABS current-reader experiment)

- `P2-C1-S1`: test whether `DOC-WORKFLOW-LABS-0002` already reads clearly with current statement/evolution separation
- `P2-C1-S2`: if needed, add the minimum reader clarification without turning `LABS-0002` into a second parent-boundary table sample

### P3 (Ledger and SUP impact verdict)

- `P3-C1-S1`: review whether the parent-ledger template needs one optional downstream-boundary note or rollup after the contract experiments
- `P3-C1-S2`: review whether the SUP template needs one optional downstream-reading clarification or whether current `contract impact` guidance is sufficient

### P4 (Next sample gate)

- `P4-C1-S1`: open or explicitly defer the `S0A-2A ADR` sample only after `P0-P3` are stable enough to avoid reopening the same reader-model question

### P5 (Repo-wide assessment gate)

- `P5-C1-S1`: classify remaining contracts as `Current Boundary Map`, `Current Reader Shape`, `no change`, or `defer until a new family opens`
- `P5-C1-S2`: classify remaining ledgers as `note/rollup candidate`, `no change`, or `defer with future family opening`
- `P5-C1-S3`: produce one prioritized execution list so later normalization can run in bounded groups rather than one repo-wide sweep
- `P5-C2-S1`: execute Batch A by adding one explicit parent-boundary surface to `DOC-WORKFLOW-GITHUB-ISSUES-0001`
- `P5-C2-S2`: decide whether Batch A alone is sufficient or whether `S0A-1A` also needs one later bounded ledger note batch
- `P5-C3-S1`: execute Batch B by adding one explicit downstream-reading handoff note to `ledger-S0A-1A-tools-github-issues-projects-and-tags`
- `P5-C3-S2`: record whether the instance-level ledger candidate is now closed without widening parent-ledger core tables

## Execution Checklist (unchecked)

### P0 (Contract rule)

- [x] `P0-C1-S1`: fix statement-label responsibility
- [x] `P0-C1-S2`: fix statement-flow history placement
- [x] `P0-C1-S3`: fix the parent-reader gap and evaluation rule
- [x] `P0-C1-S4`: fix the full write-path evaluation order
- [x] `P0-C2-S1`: write verified reader-model rule back into the contract template
- [x] `P0-C2-S2`: write section-order and statement-label limits back into the contract template

### P1 (WORKFLOW parent experiment)

- [x] `P1-C1-S1`: draft one candidate parent-only `Current Boundary Map` for `DOC-WORKFLOW-0001`
- [x] `P1-C1-S2`: rewrite `WORKFLOW-0001` reading surfaces so child-boundary meaning no longer depends on reader guesswork

### P2 (LABS current-reader experiment)

- [x] `P2-C1-S1`: test `DOC-WORKFLOW-LABS-0002` against the new rule
- [x] `P2-C1-S2`: apply only the minimum reader clarification if the experiment shows a real ambiguity

### P3 (Ledger and SUP impact verdict)

- [x] `P3-C1-S1`: review parent-ledger template impact
- [x] `P3-C1-S2`: review SUP template impact

### P4 (Next sample gate)

- [x] `P4-C1-S1`: open or defer the `S0A-2A ADR` sample after the experiment verdict

### P5 (Repo-wide assessment gate)

- [x] `P5-C1-S1`: classify remaining contracts by reader-surface need
- [x] `P5-C1-S2`: classify remaining ledgers by note/rollup or no-change standing
- [x] `P5-C1-S3`: produce one prioritized execution list for later normalization batches
- [x] `P5-C2-S1`: execute Batch A on `DOC-WORKFLOW-GITHUB-ISSUES-0001`
- [x] `P5-C2-S2`: record whether ledger follow-up is still needed after Batch A
- [x] `P5-C3-S1`: execute Batch B on `ledger-S0A-1A-tools-github-issues-projects-and-tags`
- [x] `P5-C3-S2`: record whether the ledger-instance note candidate is now closed

## Current Status (recommended)

- `S0G-4A` is now opened as a draft template-and-experiment lane.
- `P0-C2` is now complete: the contract template now explicitly distinguishes `Current Boundary Map` from `Current Reader Shape` and writes the verified statement-label and section-order limits back into the reusable template.
- `P1` is now complete: `DOC-WORKFLOW-0001` has one bounded `Current Boundary Map` experiment so the parent current-reading split is no longer left to statement notes alone.
- `P2` is now complete: `DOC-WORKFLOW-LABS-0002` does not need a parent-style boundary map; the bounded ambiguity was resolved by clarifying the current reader shape and reaffirming that chronology stays in `Statement Evolution Table`.
- `P3` is now complete: the parent-ledger and SUP templates do not need new routing columns; they only need one explicit note-level rule that downstream reader shape should be explained through optional rollups rather than through widened core tables.
- `P4` is now complete: the repo now has one full `SUP -> parent ledger -> child contract -> parent contract` ADR sample chain on `S0A-2A-R05`.
- `P5` is now complete as assessment-only work: the repo-wide scan finds one clear remaining parent-contract `Current Boundary Map` candidate, no new clear `Current Reader Shape` candidate beyond `LABS-0002`, and only bounded ledger-instance note/rollup candidates rather than one broad ledger rewrite need.
- `P5-C2` is now complete: `DOC-WORKFLOW-GITHUB-ISSUES-0001` now carries one explicit parent-boundary map, and the result does not yet force a same-commit ledger rewrite on `S0A-1A`.
- `P5-C3` is now complete: `ledger-S0A-1A-tools-github-issues-projects-and-tags` now carries one explicit downstream-reading handoff note, and the earlier ledger-instance candidate is closed without adding new parent-ledger routing columns or contract-boundary tables.
- The active work is no longer deciding whether Batch B should be tried; the bounded ledger follow-up is now executed.
- The next concrete execution step is user review of whether to stop here with the GitHub-Issues family normalized or to open a new deferred-family assessment batch.

## P5 Assessment Verdict (recommended)

- `Current Boundary Map` high-priority candidate:
  - `DOC-WORKFLOW-GITHUB-ISSUES-0001`
- `Current Reader Shape` high-priority candidate:
  - none currently stronger than the already-updated `DOC-WORKFLOW-LABS-0002`
- `no change` contract group for now:
  - `DOC-WORKFLOW-GITHUB-PROJECTS-0001`
  - `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001`
  - `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001`
  - `DOC-WORKFLOW-RUNBOOK-0001`
  - `DOC-WORKFLOW-ADR-0001`
  - `DOC-WORKFLOW-LOGS-0001`
  - `DOC-WORKFLOW-LIFECYCLE-0001`
  - `DOC-WORKFLOW-LABS-0001`
  - `DOC-CONTROL-PLANE-0001`
- `defer until new family opens` contract group:
  - no existing file yet for `DOC-WORKFLOW-SCRIPTS`
  - no existing file yet for `DOC-OPS-RUNBOOK-EVIDENCE`
- ledger-instance note or rollup candidates only when the matching contract batch opens:
  - `ledger-S0A-1A-tools-github-issues-projects-and-tags`
  - `ledger-S0B-2A-tools-scripts-and-snapshots-management`
  - `ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter`
- ledger-instance `no change` for now:
  - `ledger-S0A-2A-tools-workflow-log-lab-runbook-adr`
  - already-aligned supplement packets used in the earlier `P3/P4` sample chain

## P5 Prioritized Execution List (recommended)

- Batch A: add one `Current Boundary Map` to `DOC-WORKFLOW-GITHUB-ISSUES-0001` and align its current-reading text to explicit parent-versus-child ownership.
- Batch A status: completed.
- Batch B: if Batch A lands, add only one bounded parent-ledger note or rollup clarification to `ledger-S0A-1A-tools-github-issues-projects-and-tags` if the contract change shows the current handoff still reads too implicitly.
- Batch B status: completed.
- Batch C: open a fresh assessment lane for `DOC-WORKFLOW-SCRIPTS` and `DOC-OPS-RUNBOOK-EVIDENCE` only if the user wants to convert the currently deferred `S0B-2A` slices into real families rather than leaving them deferred.
- Batch D: revisit `ledger-S0B-3A` and `ledger-S0B-2A` only after Batch C or another new-family opening proves that a real downstream handoff note is missing at the instance level.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S4 (scaffold lane opened | 2026-04-22)

- headSha: ``
- artifacts: ``
- expected:
  - open `S0G-4A` as the bounded lane for contract-boundary-map and clause-flow governance
  - fix the default execution order as `template rule -> WORKFLOW-0001 experiment -> LABS-0002 experiment -> ledger/SUP impact verdict -> ADR sample gate`
- observed:
  - scaffold opened
  - execution order recorded in the source log

### P0-C2-S1S2 (contract template write-back landed | 2026-04-22)

- headSha: ``
- artifacts: `docs/governance/contracts/_template-contract-record.md`
- expected:
  - write the verified reader-model rule back into the reusable contract template
  - distinguish when to use `Current Boundary Map` versus `Current Reader Shape`
  - tighten the template wording so `statement label` remains current-meaning-only and section order exposes the reader surface before chronology detail
- observed:
  - the contract template now distinguishes parent-boundary versus narrow-current-reader surfaces explicitly
  - the template now recommends `Current Boundary Map` and `Current Reader Shape` at the right insertion points
  - the statement-label rule and body-order rule are now written back into the reusable template rather than living only in sample contracts and the source log

### P1-C1-S1S2 (workflow parent boundary-map experiment | 2026-04-22)

- headSha: ``
- artifacts: `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
- expected:
  - add one parent-only boundary surface that tells readers which broad workflow clauses are still parent-owned versus delegated-summary readings
  - rewrite `WORKFLOW-0001` notes and current-reading text so labs and runbook child readers no longer have to be inferred indirectly
- observed:
  - `Current Boundary Map` added to `WORKFLOW-0001`
  - current-reading and reader-note text now state explicitly that labs and runbook are narrower current readers while logs and ADR remain broad parent readings in this packet

### P2-C1-S1S2 (labs current-reader experiment | 2026-04-22)

- headSha: ``
- artifacts: `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-0002-labs-snapshot-evidence-package-governance.md`
- expected:
  - decide whether `LABS-0002` needs the same parent-style boundary map used in `WORKFLOW-0001`
  - if not, add only the minimum reader clarification needed to explain why `history-backfilled`, `carried-forward`, `amended`, and `introduced` clauses coexist in one current reader
- observed:
  - `LABS-0002` judged to be a narrow current reader rather than a parent-boundary surface
  - one `Current Reader Shape` section now explains that the mixed clause set should be read as chronology inside one current reader, not as unresolved ownership routing

### P3-C1-S1S2 (ledger and sup template impact verdict | 2026-04-22)

- headSha: ``
- artifacts: `docs/logs/_template-support-only-contract-release-ledger.md`; `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
- expected:
  - decide whether the two contract experiments require new parent-ledger or SUP table columns
  - if not, land only the minimum template guidance needed to explain downstream reader shape after write-back
- observed:
  - no new parent-ledger routing column was needed
  - no new SUP evidence-table column was needed
  - both templates now direct downstream reader-shape clarification into optional rollups or reader notes rather than widened core tables

### P4-C1-S1 (adr sample chain executed | 2026-04-22)

- headSha: ``
- artifacts: `docs/logs/support-only/ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape.md`; `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`; `docs/governance/contracts/workflow/adr/DOC-WORKFLOW-ADR-0001-decision-summary-boundary-and-evidence-links.md`; `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
- expected:
  - open one ADR-direct-evidence SUP for `S0A-2A-R05`
  - rewrite the parent ledger row from deferred background to an applied ADR child outcome
  - open one first ADR child contract
  - bridge the broad parent ADR boundary back to that new narrow child reader without widening the ledgers into contract-reader tables
- observed:
  - `ledger-SUP-S0A-2A-003` now carries the ADR-direct-evidence packet for `R05`
  - the parent ledger now resolves `R05` to `DOC-WORKFLOW-ADR-0001`
  - `DOC-WORKFLOW-ADR-0001` now acts as the narrow current-state governance surface for the ADR slice
  - `DOC-WORKFLOW-0001` now reads the ADR clause as `delegated-summary` through the new child rather than as broad parent background only

### P5-C1-S1S3 (remaining-contract and ledger assessment recorded | 2026-04-22)

- headSha: ``
- artifacts: `docs/logs/log-S0G-4A-contract-boundary-map-and-parent-child-clause-flow-governance.md`
- expected:
  - classify remaining contracts by reader-surface need after the template write-back
  - classify remaining ledgers by note/rollup need versus no-change standing
  - produce one bounded execution order for later normalization batches
- observed:
  - only `DOC-WORKFLOW-GITHUB-ISSUES-0001` stands out as one clear remaining `Current Boundary Map` candidate
  - no new contract shows the same narrow-reader ambiguity that justified `Current Reader Shape` on `DOC-WORKFLOW-LABS-0002`
  - current ledgers mostly remain sufficient as current-state routing surfaces, with only bounded note/rollup candidates worth revisiting if the matching contract batch opens
  - later `S0B-2A` deferred slices still depend on new-family decisions rather than on one global ledger rewrite

### P5-C2-S1S2 (batch a executed on github-issues parent | 2026-04-22)

- headSha: ``
- artifacts: `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
- expected:
  - add one explicit `Current Boundary Map` to the remaining high-priority parent-contract candidate
  - make Projects, title, and tag child standing readable without relying on statement notes alone
  - decide whether that contract-only change already resolves the reader ambiguity or whether a same-cycle ledger note is immediately required
- observed:
  - `DOC-WORKFLOW-GITHUB-ISSUES-0001` now exposes one explicit boundary map across mechanism, Projects, title, and tag clauses
  - the parent contract now distinguishes one `shared-reader` Projects boundary from delegated title and tag boundaries
  - current-reading and reader-note text now direct readers to the boundary map rather than to prose-only inference
  - no immediate `S0A-1A` ledger rewrite was required to make the contract-level handoff readable in this first batch

### P5-C3-S1S2 (batch b executed on s0a-1a parent ledger | 2026-04-22)

- headSha: ``
- artifacts: `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
- expected:
  - add one bounded downstream-reading handoff note to the `S0A-1A` parent ledger after Batch A
  - make the parent-ledger reader path explicit without widening routing tables or duplicating the GitHub-Issues contract boundary map into the ledger
  - record whether the earlier ledger-instance note candidate is now closed
- observed:
  - the `S0A-1A` parent ledger now tells readers explicitly to use `DOC-WORKFLOW-GITHUB-ISSUES-0001` for parent-versus-child boundary reading
  - the ledger now names the exact child follow-on reading for Projects, title, and tag slices while keeping routing ownership in the ledger itself
  - the Batch B change stayed at note/rollup level only and did not widen parent-ledger core tables
  - the earlier ledger-instance handoff candidate is now closed for the GitHub-Issues family

## Recent changes (for traceability, optional)

- 2026-04-22: opened `S0G-4A` to separate the contract reader-model question from the later `ADR` sample application and to make the `SUP -> LEDGER -> child contract -> parent contract` evaluation order explicit.
- 2026-04-22: completed `P1` by adding a bounded `Current Boundary Map` experiment to `WORKFLOW-0001` and writing the first explicit parent-owned versus delegated-summary reading split into the parent contract surface.
- 2026-04-22: completed `P2` by deciding that `LABS-0002` should keep chronology clarification inside one narrow current reader instead of receiving a second parent-style boundary map.
- 2026-04-22: completed `P3` by deciding that parent-ledger and SUP templates need note-level downstream-reading guidance, not new structural columns.
- 2026-04-22: completed `P4` by running the first ADR sample chain end to end: `SUP-003`, parent-ledger write-back, `DOC-WORKFLOW-ADR-0001`, and parent-contract ADR boundary bridge.
- 2026-04-22: completed `P0-C2` by writing the verified reader-model rule back into the reusable contract template instead of leaving it only in sample files.
- 2026-04-22: completed `P5` assessment by classifying remaining contracts and ledgers into one clear parent-boundary candidate, one no-new-reader-shape verdict, and a bounded deferred-new-family group.
- 2026-04-22: completed `P5-C2` by executing Batch A on `DOC-WORKFLOW-GITHUB-ISSUES-0001` and confirming that the first remaining parent-boundary gap can be closed at contract level before any ledger-instance follow-up is forced.
- 2026-04-22: completed `P5-C3` by executing Batch B on `ledger-S0A-1A-tools-github-issues-projects-and-tags` and closing the remaining GitHub-Issues-family ledger handoff note candidate without widening the parent-ledger structure.