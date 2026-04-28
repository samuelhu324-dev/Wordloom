# log-S4G-2A-search-failure-drills-runbook-bridge-and-template-hardening

---

**id**: `S4G-2A`
**kind**: `log`
**title**: `issues code-bridge first sample and runbook template hardening v2`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, Workflow, GitHubIssues, Runbook, Template, epic/s4, epic/s4g, sub/2`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/572`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/573`
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4G-fallback-cells-and-failure-drills-asset-governance.md`
  **previous_log**: `docs/logs/log-S4G-1E-runtime-observability-contract-code-bridge-hardening.md`
  **reference_log_1**: `docs/logs/log-S4G-1C-runtime-runbook-bridge-gate-and-code-coupled-contract-reader-surfaces.md`
  **reference_log_2**: `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  **reference_log_4**: `docs/logs/log-S0D-3A-runbook-stub.md`
**issue_keyword**: `workflow`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
**roadmap_milestone**: `M2`
**roadmap_phase**: `M2-P3`
**roadmap_bridge_refs**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md#M2-P3`
**pr_labels**: `workflow`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-27`
**updated**: `2026-04-28`
**source_reader_model**: `mixed-source-v2`
**extraction_surface_version**: `extractable-rules-v2`

---

## Decision / Outcome

**Decision**:

- Keep `S4G-2A` open, but retarget the first defended sample to the GitHub Issues automation family because it already exposes stable scripts, fail-closed preflight gates, contract validators, retained artifact contracts, and secondary-enforcement workflow wrappers.
- Treat `run-WORKFLOW-GITHUB-ISSUES-001` as the first code-coupled sample because its code-facing fields differ materially from runtime failure-drills: it is script-heavy, artifact-contract-heavy, and wrapper-aware rather than worker-and-scenario heavy.
- Defer the Search child runbook opening until after the Issues sample proves the field model on one stable non-runtime family.
- Harden the runbook template family now so later runbooks can carry `governance state`, `code bridge binding`, and `scenario coverage` explicitly instead of only through prose.

**Default choices (phase defaults / v1)**:

- Prefer the Issues family as the first sample because its entrypoints and fail-closed validators are already bounded and easier to keep current than the still-open Search fallback/cutover semantics.
- Treat `missing-metadata`, `preflight-rejected`, `review-hold`, `merge-state-missing`, `pr-body-contract-fail`, and `workflow-wrapper-stop` as the initial Issues coverage registry for evaluation.
- Keep `secondary-enforcement wrapper` semantics distinct from `primary mutation or review boundary` semantics.
- If a runbook can name an override or wrapper in code but cannot yet defend the full approval policy around it, classify that standing explicitly as `partial-code-support` rather than implying complete operator governance.

## Extractable Rule Surface

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `ISSUES-001 runbook + scripts/issues/*` | `runbook-candidate` | The GitHub Issues lifecycle runbook should carry current governance fields, a stable entrypoint table, a coverage table for fail-closed lifecycle checks, and an explicit boundary note for secondary-enforcement wrappers. | `runbook` | `ready` | `RG-01` | `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`; `scripts/issues/*.py`; `.github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml`; `.github/workflows/s0f-pr-body-completeness-standard-check-dispatch.yml` | This is the first defended code-coupled runbook sample under S4G-2A. |
| `R02` | `runbook template gap` | `contract-candidate` | Generic runbook templates need current governance fields so `owner team`, `current steward`, `approval state`, `reviewed by`, and `approved by` are carried on live runbook surfaces rather than only on neighboring contracts or ledgers. | `contract` | `ready` | `RG-02` | `docs/runbook/_template-runbook.md`; `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md` | This is template hardening, not a Search-only rule. |
| `R03` | `ISSUES template and validator surface` | `contract-candidate` | Runbook templates need one explicit `code bridge binding` surface so stable scripts, wrapper workflows, artifact contracts, and minimum supported failure classes can be defended structurally rather than inferred from prose. | `contract` | `ready` | `RG-02` | `docs/runbook/_template-runbook.md`; `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md`; `scripts/issues/body_contract.py`; `scripts/issues/check_pr_body_contract.py`; `scripts/issues/verify_live_pr_body_contract.py` | This is the missing field family the current ISSUES runbook lacked before this sample. |
| `R04` | `Issues lifecycle coverage review` | `runbook-candidate` | The Issues sample should classify admitted lifecycle failures by `default system behavior`, `operator action class`, `prod relevance`, `cadence class`, `evidence minimum`, and `coverage class` instead of treating fail-closed gates as implicit prose behavior. | `runbook` | `ready` | `RG-01` | `scripts/issues/create_pr_from_plan.py`; `scripts/issues/body_contract.py`; `.github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml`; `.github/workflows/s0f-pr-body-completeness-standard-check-dispatch.yml` | This is the minimum structure needed to stop the runbook from reading as a script index only. |
| `R05` | `Issues contract boundary` | `support-only` | The existing GitHub-Issues parent contract remains a manual mechanism and hierarchy boundary; it should not be repurposed as the automation code-bridge contract for this sample. | `log-retained` | `ready` | `RG-03` | `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`; `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md` | Prevents the mechanism parent from being overloaded with automation semantics. |
| `R06` | `Search standing after issues sample` | `support-only` | Search remains the next realistic runtime-owned child candidate, but its fallback and cutover semantics should wait until after the Issues sample proves the field model on one defended non-runtime family. | `log-retained` | `ready` | `RG-03` | `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md`; `backend/scripts/search_outbox_worker.py`; `backend/scripts/search_outbox_worker_impl.py` | Search is deferred, not rejected. |

### Shared Reason Groups

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R04` | The Issues family already has enough stable scripts, fail-closed gates, retained artifacts, and wrapper semantics to justify the first code-coupled runbook sample. | `run-WORKFLOW-GITHUB-ISSUES-001`; `scripts/issues/*`; `s0e/s0f workflows` | This is the Issues-first-sample rationale. |
| `RG-02` | `R02; R03` | Existing runbook templates were too thin for code-coupled operator surfaces because they did not carry explicit governance state or code-bridge binding fields. | `runbook templates`; `ISSUES-001` runbook | This is the template-hardening rationale. |
| `RG-03` | `R05; R06` | The manual GitHub-Issues parent should stay a mechanism boundary, and Search should stay deferred until the first non-runtime sample proves the field model cleanly. | `GitHub-Issues parent contract`; `S4G-1D`; `search worker` | This is the boundary-preservation rationale. |

## Source Reader Model / Versioning

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v2` | This packet now reads the Issues runbook, Issues script validators, secondary-enforcement workflows, and the stronger runbook-template model together. |
| extraction surface version | `extractable-rules-v2` | The packet now exposes template-hardening plus the first Issues code-bridge sample in one table. |
| compatibility expectation | `forward-readable` | Later Search child work can extend this structure after the Issues sample proves stable. |
| migration note | `Keep the broad GitHub-Issues mechanism parent separate from the Issues lifecycle automation sample.` | Prevents the parent mechanism contract from being overloaded with automation semantics. |

## PR Summary Inputs

- This packet now hardens the runbook-template field set and applies the first defended sample to the GitHub Issues lifecycle runbook.

**PR summary bullets**:

- Retarget `S4G-2A` to the first Issues code-bridge sample while preserving the broader template-hardening purpose.
- Record the first Issues coverage registry and the rule that runbooks need explicit governance and code-bridge surfaces.
- Keep the GitHub-Issues parent contract manual, and defer Search child-opening until after this sample stabilizes.

**PR checklist source**:

- Default source: reuse this packet's execution checklist.

**PR links**:

- Log: `docs/logs/log-S4G-2A-search-failure-drills-runbook-bridge-and-template-hardening.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: ``

## Exported Sections / Outlet Ownership

**Outlet ownership**:

- `contract`: later landing should keep the runbook-template family fields and the shared runbook-family contract separate from the manual GitHub-Issues mechanism parent.
- `runbook`: the first landing is now the Issues lifecycle runbook sample, not the Search child runbook.
- `view`: no-op for now.
- `index/front-door`: update the S4G spine and roadmap to register the new packet.
- `disposition/placement`: keep the GitHub-Issues parent contract as manual mechanism governance and keep Search in deferred runtime-owned standing.
- `log-retained core`: keep the Issues-first-sample decision, template-hardening rationale, and Search deferral rule here.

## Constraints

- Do not mutate the GitHub-Issues mechanism parent into an automation code-bridge contract; it remains manual and hierarchy-oriented.
- Do not treat GitHub Actions wrappers as the primary publish or review authorization boundary.
- Template hardening must stay generic enough to support code-coupled operator surfaces beyond Search alone.

## Gap Closure / Write-Back

| gap id | current status | closure target | current write-back standing | reopen proof expectation | notes |
| --- | --- | --- | --- | --- | --- |
| `G01` | `open` | `docs/runbook/_template-runbook.md` | `write-back required now` | A later runbook can survive as a live operator surface without needing explicit governance fields. | Generic runbook templates currently lack current-state governance fields. |
| `G02` | `open` | `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md` | `write-back required now` | The family-specific template can already carry stable entrypoints, fail-closed surfaces, and artifact contracts without an explicit code bridge. | The current family-specific template also lacks bridge fields. |
| `G03` | `closed-now` | `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md` | `write-back required now` | The Issues runbook can act as the first code-bridge sample without governance fields, bridge bindings, or explicit coverage tables. | This packet now applies the first sample directly to ISSUES-001. |
| `G04` | `open` | `future Search child runbook` | `conditional` | Search fallback and cutover procedures become fully defendable rather than only code-anchored. | Search remains deferred to a later round. |

| write-back target | target kind | when required | current verdict | notes |
| --- | --- | --- | --- | --- |
| `docs/runbook/_template-runbook.md` | `runbook reader` | `required when the generic template cannot carry governance or code bridge fields` | `required-now` | This packet already fixes the missing field family. |
| `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md` | `runbook reader` | `required when family-specific templates also need the same field family` | `required-now` | ISSUES family should not stay structurally weaker than the new rule. |
| `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md` | `runbook reader` | `required when the first code-bridge sample is applied` | `required-now` | This packet now uses ISSUES-001 as the first applied sample. |
| `future Search child runbook` | `runbook reader` | `required when the deferred runtime child is actually opened` | `conditional` | Search stays as the next candidate after the Issues sample. |

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `source log` | `Has the Issues lifecycle sample been reduced to explicit field, validator, and wrapper boundaries?` | `R01-R06 plus reason groups` | Entry step for this packet. |
| `SUP` | `not-required` | `n/a` | `Is this packet later evidence against one existing source-owned row?` | `explicit no-SUP verdict` | This is a new bounded packet, not later evidence against one existing row. |
| `parent ledger` | `not-required` | `n/a` | `Does this packet need to rewrite one older S3A or S0A parent row now?` | `explicit no-parent-writeback verdict` | The packet is a forward sample and template hardening round, not a parent-ledger rewrite. |
| `contract impact decision` | `required` | `source log` | `Is the packet template-hardening only, Issues-sample only, or both?` | `explicit mixed verdict in Decision / Outcome` | This packet is both template-hardening and Issues-sample application. |
| `contract mutation` | `required` | `runbook templates` | `Do live runbook templates need new fields now?` | `template write-back applied` | Required now. |
| `bridged contract reconciliation` | `conditional` | `runbook contract or GitHub-Issues parent contract` | `Do current readers need a boundary note so the manual parent is not confused with the automation sample?` | `runbook boundary note or explicit no-change verdict` | Addressed on the runbook sample here; no parent-contract mutation is required now. |

## Scope

- `P0`: fix the Issues-first-sample decision and the runbook-template hardening target.
- `P1`: normalize the Issues coverage registry and boundary classes needed for a real code-coupled runbook sample.
- `P2`: decide what is already defendable operator procedure, what is only partial-code support, and what remains outside the manual parent contract.
- `P3`: route template write-back now, apply the Issues sample now, and defer Search child-opening until later.

## Success Criteria (DoD)

- The packet explicitly states why the Issues lifecycle runbook is the first sample and why the GitHub-Issues parent contract should remain manual.
- The packet explicitly lists the first Issues lifecycle coverage registry rather than only naming fail-closed behavior in prose.
- The packet explicitly defines the missing runbook-template field family needed for code-coupled operator surfaces.
- The packet explicitly states which template and runbook surfaces need write-back now.
- The packet keeps Search deferral explicit after the Issues sample.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the Issues-first-sample rule is reviewable;
  - the template-hardening write-back target set is explicit;
  - the manual-parent-versus-automation-sample boundary and Search deferral are explicit.

## P0 (Contract | v1)

### P0-C1-S1 (Issues first-sample rule)

- The Issues lifecycle runbook can act as the first code-coupled sample because the repo already has stable scripts, fail-closed preflight gates, contract validators, retained artifact contracts, and secondary-enforcement wrappers there.
- The broad GitHub-Issues parent contract does not inherit this automation standing merely because it already governs issue hierarchy and decomposition.

### P0-C1-S2 (Runbook template hardening target)

- Generic and family-specific runbook templates must both carry:
  - current governance fields;
  - code bridge binding fields;
  - scenario registry / coverage tables for code-coupled operator surfaces.

### P0-C1-S3 (Coverage classes | v1)

- `defended-now`: the runbook can instruct operators to use the procedure now.
- `partial-code-support`: code and retained artifacts support part of the scenario, but full approval or escalation policy is not yet defended.
- `gap-owned`: missing procedure stays owned by a later packet or deferred owner surface.
- `not-owned-here`: the runbook should route the reader elsewhere rather than pretending coverage.

## Plan (draft)

### P1 (Coverage registry)

- P1-C1-S1: enumerate the first Issues coverage registry (`missing-metadata`, `preflight-rejected`, `review-hold`, `merge-state-missing`, `pr-body-contract-fail`, `workflow-wrapper-stop`).
- P1-C1-S2: classify each scenario by default system behavior, operator action class, prod relevance, cadence class, evidence minimum, and coverage class.

### P2 (Boundary classification)

- P2-C1-S1: separate defended operator procedure from partial-code-support overrides and wrapper-only surfaces.
- P2-C1-S2: keep the GitHub-Issues mechanism parent manual and keep Search deferral explicit.

### P3 (Write-back routing)

- P3-C1-S1: write back runbook-template hardening now.
- P3-C1-S2: apply the Issues sample now and defer the Search child runbook body until later.

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: Issues first-sample rule fixed.
- [ ] `P0-C1-S2`: runbook template hardening target fixed.
- [ ] `P0-C1-S3`: runbook coverage classes fixed.

### P1 (Coverage registry)

- [ ] `P1-C1-S1`: Issues coverage registry enumerated.
- [ ] `P1-C1-S2`: Issues coverage classified.

### P2 (Boundary classification)

- [ ] `P2-C1-S1`: defended procedure vs partial-code-support vs gap-owned separated.
- [ ] `P2-C1-S2`: manual-parent boundary and Search deferral fixed.

### P3 (Write-back routing)

- [ ] `P3-C1-S1`: template write-back completed.
- [ ] `P3-C1-S2`: Issues sample applied and Search child runbook opening deferred cleanly.

## Current Status

- The Issues lifecycle runbook is now the first applied code-bridge sample under `S4G-2A` because its scripts, validators, artifacts, and wrapper workflows are already bounded enough to read structurally.
- The broad GitHub-Issues parent contract remains a manual mechanism and hierarchy surface, not the automation code-bridge contract.
- Search remains the next realistic runtime-owned sample, but it stays deferred until after the Issues sample stabilizes.
- The immediate downstream task is to verify that the Issues sample stays readable and then decide whether a later Search child runbook needs any additional runtime-only field shapes.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA and key write-back targets when execution is later performed.

## Recent changes (for traceability, optional)

- 2026-04-27: opened `S4G-2A` as the bounded packet for runbook-template field expansion and later Search runbook work.
- 2026-04-27: retargeted `S4G-2A` so `run-WORKFLOW-GITHUB-ISSUES-001` becomes the first defended code-bridge sample while Search stays deferred to a later round.
