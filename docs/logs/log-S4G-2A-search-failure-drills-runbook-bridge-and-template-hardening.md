# log-S4G-2A-search-failure-drills-runbook-bridge-and-template-hardening

---

**id**: `S4G-2A`
**kind**: `log`
**title**: `search failure-drills runbook bridge and template hardening v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, FailureDrills, Runbook, Template, epic/s4, epic/s4g, sub/2`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4G-fallback-cells-and-failure-drills-asset-governance.md`
  **previous_log**: `docs/logs/log-S4G-1E-runtime-observability-contract-code-bridge-hardening.md`
  **reference_log_1**: `docs/logs/log-S4G-1C-runtime-runbook-bridge-gate-and-code-coupled-contract-reader-surfaces.md`
  **reference_log_2**: `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  **reference_log_4**: `docs/logs/log-S0D-3A-runbook-stub.md`
**issue_keyword**: `runtime`
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
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-27`
**updated**: `2026-04-27`
**source_reader_model**: `mixed-source-v1`
**extraction_surface_version**: `extractable-rules-v1`

---

## Decision / Outcome

**Decision**:

- Open `S4G-2A` as the bounded packet for the first runtime-owned Search failure-drills runbook bridge and the template hardening needed to support it.
- Treat Search as the first child candidate because the repo already defends one bounded worker chain, one defended proof path, and a concrete failure-drill scenario set there.
- Keep Chronicle below the shared runbook contract and projection-specific SOP layer for now; it does not yet have the same defended runtime-owned proof surface.
- Harden the runbook template family now so later runbooks can carry `governance state`, `code bridge binding`, and `scenario coverage` explicitly instead of only through prose.

**Default choices (phase defaults / v1)**:

- Prefer one shared `failure-drills spine` plus one Search-specific child runbook candidate rather than opening separate Search and Chronicle child contracts immediately.
- Treat `es_429`, `es_down_connect`, `es_timeout`, `es_bulk_partial`, `db_claim_contention`, `stuck_reclaim`, and `duplicate_delivery` as the initial Search scenario registry for evaluation.
- Keep `fallback switch procedure`, `coexistence window`, and `who may cut over or reverse` outside positive runbook meaning unless the repo can already defend those procedures.
- If a runbook can name a switch or fallback surface in code but cannot yet defend operator procedure, classify that standing explicitly as `code-anchor-only` or `gap-owned` rather than implying full procedure coverage.

## Extractable Rule Surface

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `Search worker + S4G-1D gap` | `runbook-candidate` | A runtime-owned Search failure-drills runbook should name the stable entrypoint, admitted scenario registry, default system behavior, manual intervention class, recovery proof, and evidence minimum for each defended failure family. | `runbook` | `ready` | `RG-01` | `backend/scripts/search_outbox_worker.py`; `backend/scripts/search_outbox_worker_impl.py`; `backend/scripts/cli_app/scenarios/*.py`; `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md` | This is the first child runbook candidate, not yet the released runbook itself. |
| `R02` | `runbook template gap` | `contract-candidate` | Generic runbook templates need current governance fields so `owner team`, `current steward`, `approval state`, `reviewed by`, and `approved by` are carried on live runbook surfaces rather than only on neighboring contracts or ledgers. | `contract` | `ready` | `RG-02` | `docs/runbook/_template-runbook.md`; `docs/governance/contracts/workflow/runbook/DOC-WORKFLOW-RUNBOOK-0001-projection-operator-rebuild-replay-and-failure-recovery.md` | This is template hardening, not a Search-only rule. |
| `R03` | `ISSUES-001 comparison + Search need` | `contract-candidate` | Runbook templates need one explicit `code bridge binding` surface so stable entrypoints, operator surfaces, fallback anchors, scenario registry refs, and minimum supported failure classes can be defended structurally rather than inferred from prose. | `contract` | `ready` | `RG-02` | `docs/runbook/_template-runbook.md`; `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md`; `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md` | This is the missing field family the current ISSUES runbook also lacks. |
| `R04` | `Search scenario review` | `runbook-candidate` | Search should classify each admitted failure scenario by `default system behavior`, `operator action class`, `prod relevance`, `cadence class`, `evidence minimum`, and `coverage class` instead of treating all drills as one flat showcase menu. | `runbook` | `ready` | `RG-01` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; `backend/scripts/cli_app/scenarios/*.py` | This is the minimum structure needed to stop the runbook from reading like a demo index. |
| `R05` | `shared spine boundary` | `support-only` | The retained shared failure-drills runbook should remain the family-level shared operator spine for `run -> verify -> export -> clean`, GitHub Actions, and evidence bundle handling, while the Search child runbook later owns Search-specific failure semantics. | `log-retained` | `ready` | `RG-03` | `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | Avoid replacing the shared spine with the Search child. |
| `R06` | `Chronicle standing` | `support-only` | Chronicle should remain under the shared runbook contract and projection SOP layer until it has one defended runtime-owned failure-drill proof path and a stable scenario registry of its own. | `log-retained` | `ready` | `RG-03` | `legacy/from_structured_docs/from-runbook/run-003-chronicle-projection.md`; `backend/scripts/chronicle_outbox_worker.py` | Do not open a Chronicle child runbook by symmetry alone. |

### Shared Reason Groups

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R04` | Search already has enough defended code and drill evidence to justify a child runbook candidate, but only if the scenario surface is made explicit and bounded. | `search_outbox_worker.py`; `search_outbox_worker_impl.py`; `cli_app/scenarios`; `S4G-1D` | This is the Search child-opening rationale. |
| `RG-02` | `R02; R03` | Existing runbook templates are too thin for code-coupled operator surfaces because they do not currently carry explicit governance state or code-bridge binding fields. | `runbook templates`; `ISSUES-001` runbook | This is the template-hardening rationale. |
| `RG-03` | `R05; R06` | Shared-spine retention and Chronicle deferral prevent over-splitting before multiple runtime-owned children are actually defendable. | `legacy runbook`; `Chronicle SOP`; `S4G-1D` | This is the boundary-preservation rationale. |

## Source Reader Model / Versioning

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v1` | This packet reads current worker code, drill scenario definitions, the retained shared runbook, and the stronger runbook-template model together. |
| extraction surface version | `extractable-rules-v1` | The packet exposes template-hardening and child-runbook-opening rules in one table. |
| compatibility expectation | `forward-readable` | Later Search or Chronicle child packets can extend this structure without reopening the retained shared spine. |
| migration note | `Keep the shared spine retained until at least one Search child runbook is actually opened and bounded.` | Prevents premature replacement of the current shared runbook reader. |

## PR Summary Inputs

- This packet both opens the Search runbook candidate and hardens the runbook-template field set needed to support it.

**PR summary bullets**:

- Open `S4G-2A` as the bounded packet for Search failure-drills runbook completion and runbook-template hardening.
- Record the first Search scenario registry and the rule that runbooks need explicit governance and code-bridge surfaces.
- Keep Chronicle deferred and keep the shared legacy runbook as the cross-projection spine for now.

**PR checklist source**:

- Default source: reuse this packet's execution checklist.

**PR links**:

- Log: `docs/logs/log-S4G-2A-search-failure-drills-runbook-bridge-and-template-hardening.md`
- Runbook: `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
- Evidence artifact: ``

## Exported Sections / Outlet Ownership

**Outlet ownership**:

- `contract`: later landing should update the runbook-template family fields and, if accepted, write the stronger field model into current runbook-family templates.
- `runbook`: later landing should be one Search-specific runtime-owned failure-drills child runbook, not the shared spine and not Chronicle yet.
- `view`: no-op for now.
- `index/front-door`: update the S4G spine and roadmap to register the new packet.
- `disposition/placement`: keep Chronicle in shared-contract plus projection-SOP standing until a separate child-opening packet is justified.
- `log-retained core`: keep the Search-versus-Chronicle decision, template-hardening rationale, and runbook-boundary rules here.

## Constraints

- Do not claim full Search runbook completeness merely because drills exist; the packet must separate defended procedure from code-anchor-only and gap-owned semantics.
- Do not open a Chronicle child runbook until the repo can defend Chronicle-specific failure semantics beyond shared framework behavior.
- Template hardening must stay generic enough to support code-coupled operator surfaces beyond Search alone.

## Gap Closure / Write-Back

| gap id | current status | closure target | current write-back standing | reopen proof expectation | notes |
| --- | --- | --- | --- | --- | --- |
| `G01` | `open` | `docs/runbook/_template-runbook.md` | `write-back required now` | A later runbook can survive as a live operator surface without needing explicit governance fields. | Generic runbook templates currently lack current-state governance fields. |
| `G02` | `open` | `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md` | `write-back required now` | The family-specific template can already carry stable entrypoints, fail-closed surfaces, and artifact contracts without an explicit code bridge. | The current family-specific template also lacks bridge fields. |
| `G03` | `partially-closed` | `future Search child runbook` | `conditional` | Search fallback and cutover procedures become fully defendable rather than only code-anchored. | Search has enough code and drills for a child candidate, but not yet complete fallback procedure. |
| `G04` | `open` | `future Chronicle child packet or explicit no-child verdict` | `not-required-now` | Chronicle receives one defended runtime-owned failure-drill proof path and scenario registry. | Chronicle remains deferred. |

| write-back target | target kind | when required | current verdict | notes |
| --- | --- | --- | --- | --- |
| `docs/runbook/_template-runbook.md` | `runbook reader` | `required when the generic template cannot carry governance or code bridge fields` | `required-now` | This packet already fixes the missing field family. |
| `docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md` | `runbook reader` | `required when family-specific templates also need the same field family` | `required-now` | ISSUES family should not stay structurally weaker than the new rule. |
| `future Search child runbook` | `runbook reader` | `required when the Search child is actually opened` | `conditional` | This packet fixes the opening criteria and field grammar first. |

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `source log` | `Has Search runbook incompleteness been reduced to explicit field and scenario gaps?` | `R01-R06 plus reason groups` | Entry step for this packet. |
| `SUP` | `not-required` | `n/a` | `Is this packet later evidence against one existing source-owned row?` | `explicit no-SUP verdict` | This is a new bounded packet, not later evidence against one existing row. |
| `parent ledger` | `conditional` | `S3A parent/support-only ledgers` | `Does this packet later change one existing S3A row verdict?` | `later write-back only if a Search child runbook actually opens` | The packet is primarily forward-opening, not immediate parent-ledger rewrite. |
| `contract impact decision` | `required` | `source log` | `Is the packet template-hardening only, Search child-opening only, or both?` | `explicit mixed verdict in Decision / Outcome` | This packet is both template-hardening and Search child-opening. |
| `contract mutation` | `required` | `runbook templates` | `Do live runbook templates need new fields now?` | `template write-back applied` | Required now. |
| `bridged contract reconciliation` | `conditional` | `runbook contract or shared spine` | `Do current runbook readers need redirect or coverage notes after the child opens?` | `later bridge note or explicit no-change verdict` | Not required until the child runbook exists. |

## Scope

- `P0`: fix the Search child-opening decision and the runbook-template hardening target.
- `P1`: normalize the Search scenario registry and coverage classes needed for a real runbook.
- `P2`: decide what is already defendable operator procedure, what is only code-anchor support, and what remains gap-owned.
- `P3`: route template write-back now and defer the Search child runbook body until the stronger field set exists.

## Success Criteria (DoD)

- The packet explicitly states why Search can open a child runbook candidate and why Chronicle cannot yet.
- The packet explicitly lists the first Search failure scenario registry rather than only naming drills in prose.
- The packet explicitly defines the missing runbook-template field family needed for code-coupled operator surfaces.
- The packet explicitly states which template surfaces need write-back now.
- The packet keeps shared-spine retention and Chronicle deferral explicit.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the Search child-opening rule is reviewable;
  - the template-hardening write-back target set is explicit;
  - the retained shared-spine and Chronicle deferral boundaries are explicit.

## P0 (Contract | v1)

### P0-C1-S1 (Search child-opening rule)

- Search can act as the first runtime-owned failure-drills runbook child only because the repo already has one defended worker entrypoint, one defended proof path, and a non-trivial scenario/drill surface on Search.
- Chronicle does not inherit the same child-opening standing merely because it shares framework code.

### P0-C1-S2 (Runbook template hardening target)

- Generic and family-specific runbook templates must both carry:
  - current governance fields;
  - code bridge binding fields;
  - scenario registry / coverage tables for code-coupled operator surfaces.

### P0-C1-S3 (Coverage classes | v1)

- `defended-now`: the runbook can instruct operators to use the procedure now.
- `partial-code-support`: code and drills support part of the scenario, but full operator procedure is not yet defended.
- `gap-owned`: missing procedure stays owned by a gap packet or deferred owner surface.
- `not-owned-here`: the runbook should route the reader elsewhere rather than pretending coverage.

## Plan (draft)

### P1 (Scenario registry)

- P1-C1-S1: enumerate the first Search scenario registry (`es_429`, `es_down_connect`, `es_timeout`, `es_bulk_partial`, `db_claim_contention`, `stuck_reclaim`, `duplicate_delivery`, `projection_version`).
- P1-C1-S2: classify each scenario by default system behavior, operator action class, prod relevance, cadence class, evidence minimum, and coverage class.

### P2 (Boundary classification)

- P2-C1-S1: separate defended operator procedure from code-anchor-only fallback and cutover semantics.
- P2-C1-S2: keep shared-spine retention and Chronicle deferral explicit.

### P3 (Write-back routing)

- P3-C1-S1: write back runbook-template hardening now.
- P3-C1-S2: defer the Search child runbook body until the stronger template field set exists.

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: Search child-opening rule fixed.
- [ ] `P0-C1-S2`: runbook template hardening target fixed.
- [ ] `P0-C1-S3`: runbook coverage classes fixed.

### P1 (Scenario registry)

- [ ] `P1-C1-S1`: Search scenario registry enumerated.
- [ ] `P1-C1-S2`: Search scenario coverage classified.

### P2 (Boundary classification)

- [ ] `P2-C1-S1`: defended procedure vs code-anchor-only vs gap-owned separated.
- [ ] `P2-C1-S2`: shared-spine retention and Chronicle deferral fixed.

### P3 (Write-back routing)

- [ ] `P3-C1-S1`: template write-back completed.
- [ ] `P3-C1-S2`: Search child runbook opening deferred cleanly until template hardening lands.

## Current Status

- Search already has enough real failure handling and drill surfaces to justify a child runbook candidate, but not enough defended operator procedure to claim a complete runbook yet.
- The shared legacy runbook remains the current cross-projection operator spine.
- Chronicle remains below the shared contract and projection-SOP layer.
- The immediate downstream task is to harden runbook templates so the later Search child runbook can be maintained with explicit governance, code bridge, and coverage surfaces.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA and key write-back targets when execution is later performed.

## Recent changes (for traceability, optional)

- 2026-04-27: opened `S4G-2A` as the bounded packet for Search failure-drills runbook hardening and runbook-template field expansion.