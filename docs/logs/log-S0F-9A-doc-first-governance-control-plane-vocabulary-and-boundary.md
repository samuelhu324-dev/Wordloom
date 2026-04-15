# log-S0F-9A (Phase 9A: DOC-first governance control-plane vocabulary and boundary)

---

**id**: `S0F-9A`
**kind**: `log`
**title**: `DOC-first governance control-plane vocabulary and boundary packet v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Records, epic/s0, sub/9a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`
  **reference_log_1**: `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
  **reference_log_2**: `docs/logs/log-S0F-7H-actor-and-provenance-fields-for-evidence-review-governance.md`
  **reference_log_3**: `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`
  **reference_log_4**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M3`
**roadmap_phase**: `M3-P0`
**roadmap_bridge_refs**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M3-P0`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-15`
**updated**: `2026-04-15`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this log.
- Day-level precision is acceptable for this opening packet because the lane is starting as one bounded vocabulary-and-boundary scaffold rather than one fine-grained operational replay.
- If this lane later becomes the active source log for issue/PR automation, subsequent updates should preserve deterministic `issue_*`, `pr_*`, and roadmap bridge fields rather than inferring them from downstream artifacts.

## Decision / Outcome

**Decision**:

- `S0F-9A` opens as the first real `M3` child log for `road-002`, turning the earlier `S0F-7G/7H/7I` precursor packet into one explicit `DOC`-first governance-control opening lane.
- The first deliverable is not a repo-wide schema migration; it is one bounded vocabulary-and-boundary packet that fixes how ownership, stewardship, approval, verification, contribution, and handoff should be separated on `log -> ledger -> contract` surfaces.
- This lane keeps the first execution surface inside docs/governance records and contracts; it does not yet widen into tenant authorization, billing, or product-runtime permission semantics.

**Default choices (phase defaults / v1)**:

- Keep `M3-P0-A` `DOC`-first: the first mutable surfaces are source logs, ledgers, and contracts under docs governance.
- Treat `S0F-7G`, `S0F-7H`, and `S0F-7I` as precursor evidence only; `S0F-9A` is the first log that should speak in explicit `M3` control-plane language.
- Frontmatter should carry current effective governance state only; event/history detail should stay in ledgers, tables, or explicit event blocks.
- Do not let approval, verification, contribution, and ownership collapse into one overloaded `actor` field.
- Do not pull `tenant`, `membership`, `role`, `plan`, `entitlement`, or billing semantics into this lane; those belong to `M4`.

## PR Summary Inputs (optional)

- Use this block because `S0F-9A` is expected to open the first real `M3` child packet and may later drive issue/PR automation directly.

**PR summary bullets**:

- Open the first real `M3` child log as a `DOC`-first governance-control vocabulary-and-boundary packet.
- Separate current ownership, stewardship, approval, verification, contribution, and handoff semantics instead of overloading one generic actor field.
- Fix the first execution boundary on `log -> ledger -> contract` before any later widening into runbook, evidence, drills, or tenant authorization.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
- Previous log: `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `log-retained core + contract-first governance vocabulary` lane.
- The expected first landing is a stable vocabulary-and-boundary contract for current-state governance fields, plus one bounded application packet later in `M3-P1-A`.
- This opening scaffold should not export runbook, view, or index/front-door surfaces yet because the first task is still to stabilize vocabulary and field placement.

**Outlet ownership**:

- `contract`: define the minimum governance-control vocabulary and field-placement rules for current state versus event history
- `runbook`: no-op at packet open; repeatable operator procedure should wait until field placement survives a real application packet
- `view`: no-op at packet open; reader-facing summaries should wait until there is at least one real current-state sample and one real handoff sample
- `index/front-door`: no-op at packet open
- `disposition/placement`: no-op at packet open; no relocation or cleanup decision is needed yet
- `log-retained core`: lane boundary, field semantics, phase plan, execution checklist, and later evidence ledger remain here

## Definitions (optional)

- `owner_team`: the durable team-level responsibility anchor for the governed surface.
- `current_steward`: the current named or role-based maintainer accountable for day-to-day state and bounded updates.
- `approved_by`: the actor or role that accepted the current effective state.
- `reviewed_by`: the actor or role that reviewed the current packet or state without necessarily carrying final approval authority.
- `verified_by`: the actor or role that verified evidence or implementation claims closely enough to support packet-level judgment.
- `contribution_event`: a bounded historical record that credits meaningful work without implying current ownership.
- `ownership_handoff_event`: a bounded historical record that explains when and why current stewardship or ownership changed.

## Constraints

- Do not treat `actor` as a sufficient catch-all field.
- Do not place historical event rows in frontmatter when the value is only true for one earlier moment rather than the current effective state.
- Do not widen into tenant authorization, product permissions, org-chart simulation, or billing semantics.
- Do not force every existing docs-family file to adopt the new fields before the first vocabulary-and-boundary packet is explicitly reviewed.

## Scope

- `P0`: open the `M3-P0-A` vocabulary-and-boundary lane and fix minimum control-plane terms plus field-placement rules
- `P1`: apply the first minimal governance block to one bounded `log -> ledger -> contract` packet in docs/governance
- `P2`: prove handoff, steward replacement, approver separation, and verifier accountability on representative docs-family samples
- `P3`: define the first reader-facing current-state versus history surfaces without turning views into false sources of governance truth

## Success Criteria (DoD)

- The repo has one explicit minimum vocabulary for ownership, stewardship, approval, review, verification, contribution, and handoff.
- The lane records which fields belong in current-state frontmatter versus historical event surfaces.
- The lane keeps `M3` distinct from `M4` by excluding tenant/access/billing semantics from the first packet.
- The lane identifies one bounded first application packet for `M3-P1-A` rather than leaving the next step abstract.
- The first handoff drill and the first reader-facing surface are both named explicitly, even if still deferred to later phases.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the minimum governance-control vocabulary is explicit
  - the frontmatter-versus-event-history placement rule is explicit
  - one bounded `M3-P1-A` application packet is chosen and defended
- `stable` for this opening packet does not require full repo-wide rollout; it requires the vocabulary-and-boundary contract to be explicit enough for later execution.

## P0 (Contract | v1)

### P0-C1-S1 (Minimum governance-control vocabulary)

- Fix the minimum shared vocabulary for `owner_team`, `current_steward`, `approved_by`, `reviewed_by`, `verified_by`, `contribution_event`, and `ownership_handoff_event`.
- Make the vocabulary answer different questions cleanly instead of overloading one generic actor field.

### P0-C1-S2 (Current-state versus event-history placement)

- Frontmatter should carry current effective governance state only.
- Historical changes, contributor credits, and stewardship transitions should live in ledgers, tables, or explicit event blocks rather than being flattened into current-state metadata.

### P0-C1-S3 (Boundary against authorization and product access)

- `M3` in this opening packet is governance-control only.
- Tenant permissions, plan state, entitlement, and billing remain out of scope and reserved for `M4`.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-9A/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (First DOC-surface application packet)

- `P1-C1-S1`: choose one bounded `log -> ledger -> contract` sample family that can carry the first governance-control field application
- `P1-C1-S2`: apply the current-state versus event-history split to that sample without widening into unrelated schema churn

### P1 Execution Decision (v1)

- The first bounded sample family is now fixed as `S0A-1A` parent ledger + `ledger-SUP-S0A-1A-001` + `DOC-WORKFLOW-GITHUB-PROJECTS-0001`.
- This family is preferred because it already has a parent-ledger routing decision, one screenshot-backed supplement with packet-level actor/provenance rows, and one child contract whose current-reading surface is narrow enough to absorb governance state without a repo-wide schema jump.
- The `P1` application rule in this sample is:
  - current effective governance state belongs on the parent-ledger and child-contract reading surfaces
  - packet-level actor/provenance and write-back history remain in the supplement as event/accountability evidence
  - the source log records the boundary and the defended sample choice rather than replaying the sample's full local tables

### P2 (Handoff and separation drill)

- `P2-C1-S1`: prove one steward replacement or delegated stewardship case
- `P2-C1-S2`: prove that approver, reviewer, and verifier can be separated without ambiguity on the chosen docs-family sample

### P2 Drill Decision (v1)

- The same `S0A-1A` sample family remains the `P2` drill surface so the lane can prove governance movement without introducing a second family too early.
- The bounded drill now uses one delegated stewardship case on `DOC-WORKFLOW-GITHUB-PROJECTS-0001` and one role-separation case across the same family.
- The `P2` success rule in this sample is:
  - current stewardship may be delegated without changing the durable `owner_team`
  - `reviewed_by`, `verified_by`, and `approved_by` must point to distinguishable governance roles rather than collapsing back into one actor value
  - the delegation and separation should be explicit in current-state blocks and in event/accountability surfaces at the same time

### P3 (Reader-facing surface)

- `P3-C1-S1`: define one current-state reader surface answering who owns and approves the current state
- `P3-C1-S2`: define one history surface answering who contributed and when stewardship changed

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: fix the minimum governance-control vocabulary
- [ ] `P0-C1-S2`: fix the current-state versus event-history placement rule
- [ ] `P0-C1-S3`: fix the boundary against authorization and product-access semantics

### P1 (First DOC-surface application packet)

- [x] `P1-C1-S1`: choose the first bounded `log -> ledger -> contract` sample family
- [x] `P1-C1-S2`: apply the field split to the chosen sample without widening into unrelated schema churn

### P2 (Handoff and separation drill)

- [x] `P2-C1-S1`: prove one steward replacement or delegated stewardship case
- [x] `P2-C1-S2`: prove one clean approver versus reviewer versus verifier separation case

### P3 (Reader-facing surface)

- [ ] `P3-C1-S1`: define one current-state reader surface
- [ ] `P3-C1-S2`: define one history/contribution reader surface

## Current Status (recommended)

- `S0F-9A` is now opened as the first real `M3` child log under `road-002`.
- `P1` is now complete on one bounded sample family: `S0A-1A` parent ledger + `SUP-001` + `DOC-WORKFLOW-GITHUB-PROJECTS-0001`.
- The first application now makes one practical split explicit: current effective governance state is carried on the parent-ledger and child-contract reading surfaces, while packet-level actor/provenance and write-back chain stay in the supplement as event/history evidence.
- `P2` is now also complete on the same family: the Projects child now carries an explicit delegated stewardship state under the same durable `owner_team`, and the sample now separates reviewer, verifier, and approver roles instead of collapsing them into one packet reviewer.
- The next step is `P3`: define one reader-facing current-state view and one history/contribution view that read across the same family without turning those views into false governance sources of truth.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane begins making real bounded changes.
- This section intentionally remains empty at scaffold time.

### P1-C1-S1S2 (First governance-control field split applied to `S0A-1A` sample family | 2026-04-15)

- headSha: `1b1bc8917`
- artifacts:
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
- expected:
  - the first `M3` application should prove a bounded current-state versus event-history split without forcing repo-wide schema churn
  - the chosen sample should keep current ownership/stewardship/approval reading on the parent-ledger and child-contract surfaces
  - packet-level actor/provenance rows should remain historical/accountability evidence rather than becoming false current-state ownership markers
- observed:
  - `S0A-1A` is now fixed as the first `P1` sample family because it already exposed the needed `log -> ledger -> contract` seams in one small docs-governance packet
  - the parent ledger and the Projects child contract now carry explicit current-state governance blocks, while the supplement now states its actor/provenance table as event/accountability evidence rather than current ownership
  - the lane still avoids tenant/access/billing semantics and therefore remains inside the intended `M3` boundary

### P2-C1-S1S2 (Delegated stewardship and governance-role separation proved on `S0A-1A` sample family | 2026-04-15)

- headSha: `2f2f89b36`
- artifacts:
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
- expected:
  - the sample family should prove one delegated stewardship case without changing the durable owner team
  - the sample family should prove that reviewer, verifier, and approver can be read as distinct governance roles
  - the proof should remain local to the chosen family rather than forcing broader repo-wide field expansion
- observed:
  - the Projects child now carries one explicit delegated stewardship state while the owner team remains `docs-governance`
  - the supplement now separates evidence verification from packet review and approval, so `verified_by`, `reviewed_by`, and `approved_by` no longer collapse into one actor value
  - the parent ledger and child contract now preserve both the current-state reading and the event trail that explains why the delegated and separated governance state is currently defended

## Recent changes (for traceability, optional)

- 2026-04-15: opened `S0F-9A` as the first real `M3` child log so the governance-control lane no longer depends only on `S0F-7G/7H/7I` precursor material.
- 2026-04-15: completed `P1-C1-S1S2` by selecting the `S0A-1A` sample family and applying the first current-state versus event-history split across the parent ledger, supplement, and Projects child contract.
- 2026-04-15: completed `P2-C1-S1S2` on the same `S0A-1A` sample family by proving one delegated stewardship state and one clean reviewer/verifier/approver separation case.