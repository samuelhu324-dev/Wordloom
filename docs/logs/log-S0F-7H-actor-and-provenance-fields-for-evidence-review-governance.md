# log-S0F-7H (Phase 7H: actor and provenance fields for evidence review governance)

---

**id**: `S0F-7H`
**kind**: `log`
**title**: `actor and provenance fields for evidence review governance`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Evidence, Records, epic/s0, sub/7h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
  **reference_log_1**: `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
  **reference_log_2**: `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  **reference_log_3**: `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  **reference_log_4**: `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
**issue_keyword**: `records`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/7`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-13`
**updated**: `2026-04-13`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this log.
- Day-level values remain acceptable for this scaffold because the lane is being opened as one bounded governance design packet rather than one second-precision operational run.

## Decision / Outcome

**Decision**:

- `S0F-7H` opens as the bounded follow-up after `S0F-7G` for one narrower governance problem: once screenshot and attachment review is readable, the next missing boundary is who submitted evidence, who verified it, who approved it, and what provenance chain currently defends that judgment.
- This lane will define a minimum actor/provenance field set for evidence-review packets first; it will not widen into a full org-role or permissions model yet.

**Default choices (phase defaults / v1)**:

- Keep the first landing surface inside supplement-ledger packets rather than retrofitting every document class at once.
- Separate review ergonomics from authority/provenance semantics: `7G` already solved readable attachment review, while `7H` should solve actor and provenance accountability.
- Prefer a minimum field set first, such as `submitted_by`, `evidence_owner`, `verified_by`, `verification_method`, `approved_by`, `approval_state`, and `approval_basis`, before considering wider org-interface fields.
- Avoid guessing real-world actors when the historical packet cannot yet defend them; `unknown`, `pending`, or bounded notes remain valid.
- Keep role/authority escalation explicit and deferred until the minimum field set proves insufficient.

## Minimum Actor / Provenance Contract

- Supplement-ledger evidence review may add one minimal accountability surface using `submitted by`, `evidence owner`, `verified by`, `verification method`, `approved by`, `approval state`, and `approval basis`.
- These fields describe packet-level submission, verification, and approval only; they do not by themselves establish a full permissions or org-authority model.
- The packet may add one short `provenance note` when the current accountability chain is only partially defended.
- This lane treats role-based or delegated values as valid intermediate states when the historical packet cannot yet defend one named actor.

## Problem Statement

- `S0F-7G` solved the narrower screenshot-reviewability problem, but it intentionally deferred one next governance question: approval-facing packets still need a consistent way to name who submitted evidence, who verified it, how it was verified, who approved it, and what provenance chain currently supports that approval state.
- Without one minimum actor/provenance protocol, the repo still risks mixing several different concerns:
  - evidence readability
  - evidence accountability
  - approval authority
  - provenance traceability
- The repo therefore needs one bounded lane that answers three questions before broader governance expansion:
  - what the minimum actor/provenance field set should be for supplement-ledger evidence review
  - how those fields should be recorded when historical packets cannot fully defend named actors yet
  - which smallest live packet should prove the protocol before any wider rollout is declared

## Exported Sections / Outlet Ownership

- This slice starts as one `support-only ledger + template + log-retained core` governance-design lane.
- The expected first landing is one minimum actor/provenance field contract for evidence-review packets plus one live pilot.

**Outlet ownership**:

- `contract`: the minimum actor/provenance field contract remains written here in `S0F-7H` until the repo actually needs a separate evidence-governance contract surface
- `runbook`: no-op by default
- `view`: no-op by default
- `index/front-door`: no-op by default
- `disposition/placement`: supplement-ledger template and pilot packets are the first mutable landing surfaces
- `log-retained core`: lane boundary, field contract, pilot verdicts, and deferred authority questions stay here

## Definitions (optional)

- `submitted_by`: the actor or source channel that first supplied the evidence into the review packet.
- `evidence_owner`: the actor or role currently accountable for the evidence item being maintained or defended.
- `verified_by`: the actor or role that checked the evidence closely enough for packet-level judgment.
- `verification_method`: the bounded method used for verification, such as direct screenshot inspection, source-path check, transcript comparison, or manual replay.
- `approved_by`: the actor or role that accepted the evidence for packet-level use.
- `approval_state`: the current packet-level judgment state for the evidence row.
- `approval_basis`: the concise rationale that explains why the approval state is currently defended.

## Constraints

- Do not collapse actor/provenance fields back into attachment ergonomics; `7G` already owns the narrower screenshot-review surface.
- Do not invent named people or authority chains when the packet cannot defend them.
- Do not widen immediately into permissions, org charts, or enterprise approval workflow modeling.
- Do not break existing supplement naming, attachment-id, or parent-ledger binding rules.

## Scope

- `P0`: open `S0F-7H` and bound the problem to minimum actor/provenance fields for evidence-review packets
- `P1`: define the minimum actor/provenance field set and its semantics for supplement-ledger packets
- `P2`: decide how unknown, pending, delegated, or role-based values should be represented when evidence history is incomplete
- `P3`: apply the protocol to one first live sample, expected first on `ledger-SUP-S0A-1A-001`

## Success Criteria (DoD)

- The repo has one explicit minimum actor/provenance field contract for evidence-review packets.
- The repo has one explicit representation rule for incomplete or historically under-defended actor/provenance data.
- The repo proves the protocol on one bounded live packet before wider rollout.
- Broader authority or permissions modeling remains explicitly deferred unless the minimum field set proves insufficient.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the minimum actor/provenance field contract is explicitly written
  - one live packet demonstrates the protocol cleanly
  - the lane records whether broader authority modeling is still needed next or remains deferred
- `stable` does not require repo-wide rollout; one accepted sample-first protocol is sufficient.

## P0 (Lane boundary | v1)

### P0-C1-S1 (Open `S0F-7H` as the actor/provenance follow-up)

- Open one bounded follow-up lane after `S0F-7G` for actor/provenance fields around evidence submission, verification, and approval.

### P0-C1-S2 (Keep the first landing surface inside SUP packets)

- The first mutable landing surface remains the supplement-ledger template plus one live packet rather than a repo-wide frontmatter rewrite.

## Plan (draft)

### P1 (Minimum actor/provenance field contract)

- `P1-C1-S1`: define the minimum actor/provenance field set for evidence-review packets
- `P1-C1-S2`: define the semantics for each field without assuming a full org-role model

### P2 (Incomplete-history representation rule)

- `P2-C1-S1`: define how `unknown`, `pending`, role-based, or delegated values should be represented
- `P2-C1-S2`: define when the packet may stay partial rather than fabricating actor certainty

### P3 (First live packet pilot)

- `P3-C1-S1`: patch the supplement-ledger template with the approved actor/provenance protocol
- `P3-C1-S2`: apply the protocol to `ledger-SUP-S0A-1A-001` as the first live sample

## Execution Checklist (unchecked)

### P0 (Lane boundary)

- [x] `P0-C1-S1`: open `S0F-7H` as the actor/provenance follow-up
- [x] `P0-C1-S2`: keep the first landing surface inside SUP packets

### P1 (Minimum actor/provenance field contract)

- [x] `P1-C1-S1`: define the minimum actor/provenance field set for evidence-review packets
- [x] `P1-C1-S2`: define the semantics for each field without assuming a full org-role model

### P2 (Incomplete-history representation rule)

- [x] `P2-C1-S1`: define how `unknown`, `pending`, role-based, or delegated values should be represented
- [x] `P2-C1-S2`: define when the packet may stay partial rather than fabricating actor certainty

### P3 (First live packet pilot)

- [x] `P3-C1-S1`: patch the supplement-ledger template with the approved actor/provenance protocol
- [x] `P3-C1-S2`: apply the protocol to `ledger-SUP-S0A-1A-001` as the first live sample

## Current Status (recommended)

- `S0F-7H` is now opened as the bounded follow-up after `S0F-7G` for actor/provenance fields around evidence submission, verification, and approval.
- The lane is intentionally scoped to supplement-ledger accountability first; it does not yet commit the repo to a broader org-role or permissions model.
- `P1-C1-S1` is now complete: the lane now defines the minimum actor/provenance field set for evidence-review packets as `submitted by`, `evidence owner`, `verified by`, `verification method`, `approved by`, `approval state`, and `approval basis`.
- `P1-C1-S2` is now complete: the lane now states that these fields record packet-level accountability only and do not yet establish a full permissions or org-authority model.
- `P2-C1-S1` is now complete: the lane now defines `unknown`, `pending`, `role:<role-name>`, and `delegated:<role-name>` as the bounded representation grammar for incomplete actor history.
- `P2-C1-S2` is now complete: the lane now permits partial actor/provenance rows when the packet stays useful and the missing detail is stated explicitly in one `provenance note`.
- `P3-C1-S1` is now complete in workspace: the SUP template now exposes the actor/provenance protocol as one dedicated accountability surface separate from attachment-review ergonomics.
- `P3-C1-S2` is now complete in workspace: `ledger-SUP-S0A-1A-001` now proves the protocol on three live supplement items using defended partial actor values rather than invented named submitters.
- The next step is to review whether this minimum packet-level accountability chain is already sufficient or whether a later lane should widen into stronger authority-role or org-level provenance modeling.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane starts mutating templates or live supplement packets.
- This section stays empty until the first template or pilot patch is actually landed.

### P1-C1-S1S2 + P2-C1-S1S2 (Minimum actor/provenance contract and incomplete-history rule fixed in workspace | 2026-04-13)

- headSha: `92c223458`

- artifacts:
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  - `docs/logs/log-S0F-7H-actor-and-provenance-fields-for-evidence-review-governance.md`
- expected:
  - the repo should define one minimum actor/provenance field set for evidence-review packets without dragging in a full permissions or org-model rewrite
  - the protocol should state how to represent incomplete actor history using explicit bounded values instead of fabricated named actors
- observed:
  - the SUP template now defines one `Actor and Provenance Review Table` with the minimum packet-level accountability fields
  - the lane now records `unknown`, `pending`, `role:<role-name>`, and `delegated:<role-name>` as the approved grammar for incomplete actor history, plus one `provenance note` when the chain remains partial but still usable

### P3-C1-S1S2 (First live actor/provenance pilot fixed in workspace | 2026-04-13)

- headSha: `aa4bf42d8`

- artifacts:
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/logs/log-S0F-7H-actor-and-provenance-fields-for-evidence-review-governance.md`
- expected:
  - the live pilot should prove that the minimum actor/provenance protocol can be applied without inventing named actors the historical packet cannot actually defend
  - the sample should show one bounded accountability chain per supplement item while staying separate from the narrower screenshot-review ergonomics already solved in `7G`
- observed:
  - `ledger-SUP-S0A-1A-001` now exposes one `Actor and Provenance Review Table` for all three supplement items
  - the pilot uses defended partial values such as `unknown` and `role:packet-reviewer` rather than fabricating historical named submitters, while still recording one explicit packet-level approval state and provenance note for each item