# log-S0F-10A (Phase 10A: Book-first access control minimum closure)

---

**id**: `S0F-10A`
**kind**: `log`
**title**: `book-first access control minimum closure and role boundary v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Control, Policy, Drills, Evidence, epic/s0, sub/10a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
  **reference_log_1**: `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
  **reference_log_2**: `docs/roadmap/_draft/road-S2-.md`
**issue_keyword**: `policy`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/10a`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: `M4-P0`
**roadmap_bridge_refs**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4:-Book-first-access-control-minimum-closure-on-the-current-SoT`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-15`
**updated**: `2026-04-15`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this lane.
- Day-level precision is acceptable here because the opening packet is still a policy-and-boundary scaffold rather than a code-side replay ledger.
- `reviewed` should remain `pending` until this minimum access model is explicitly accepted as the first `M4-P0` source packet.

## Decision / Outcome

**Decision**:

- `S0F-10A` opens the first real `M4` child lane as a minimum access-control packet centered on `book` rather than on fine-grained content ACL.
- The first deliverable is not a commercial-plan simulator and not a block-level permission system; it is one bounded policy packet that fixes who may read, edit, share, revoke, and administer one `book`, while separating ordinary user roles from system-admin override.
- The opening lane keeps `block` as inherited content structure under the enclosing `book` standing rather than opening block-level ACL in v1.

**Default choices (phase defaults / v1)**:

- `book` is the first independent authorization container.
- `block` inherits the containing `book` standing and is not an independently shared or independently denied object in v1.
- Ordinary collaboration roles and platform/system admin roles must remain separate concepts.
- `plan` and later `entitlement` remain reserved extension concepts and must not drive the opening packet's core permission logic.
- The opening lane should prefer minimum closure over platform realism: if a permission question cannot be answered without product or commercial speculation, defer it instead of forcing it into v1.

## PR Summary Inputs (optional)

- Use this block because `S0F-10A` is expected to open the first explicit `M4-P0` source packet and may later drive issue/PR automation directly.

**PR summary bullets**:

- Open the first `M4` child lane as a book-first minimum access-control packet.
- Separate ordinary user roles from system-admin override without introducing block-level ACL or early commercial-plan complexity.
- Fix the first bounded `book` action model so later entitlement or billing work can widen from a stable access boundary rather than from guesswork.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
- Previous log: `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `log-retained core + access-model contract-first` lane.
- The expected first landing is a stable minimum access-model contract for `user / membership / book role / system role / book actions / block inheritance`, plus one bounded replay packet later in `M4-P1-A`.

**Outlet ownership**:

- `contract`: define the minimum access vocabulary, role separation, book-first authorization boundary, and block-inheritance rule
- `runbook`: no-op at packet open; operator procedure should wait until the first replay drill exists
- `view`: no-op at packet open; reader-facing access summaries should wait until one real book-role drill exists
- `index/front-door`: no-op at packet open
- `disposition/placement`: no-op at packet open
- `log-retained core`: lane boundary, policy choices, phase plan, execution checklist, and later evidence ledger remain here

## Definitions

- `user`: one ordinary product-facing principal who may belong to a tenant and receive book-level standing through membership or share.
- `membership`: the bounded relation that ties a user to a tenant and lets later authorization reason about ordinary product participation.
- `book_role`: the ordinary collaboration role carried on one book, such as viewer, editor, or owner.
- `system_role`: one platform-level role such as system admin that exists outside normal book collaboration semantics.
- `book`: the first independent authorization container in this lane.
- `block`: one content unit inside a book that inherits the enclosing book standing in v1.

## Constraints

- Do not open block-level ACL in this first lane.
- Do not require `plan`, `entitlement`, or `mock billing` to make the opening packet coherent.
- Do not collapse ordinary product roles and system-admin override into one blended admin concept.
- Do not widen into export monetization, template monetization, or feature gating that the current product policy cannot yet defend.

## Scope

- `P0`: contract
- `P1`: implementation mapping and minimum action matrix
- `P2`: drill and replay
- `P3`: widening decision

## Success Criteria (DoD)

- The lane fixes `book` as the first independent authorization container.
- The lane states explicitly that `block` inherits `book` standing and is not independently authorized in v1.
- The lane distinguishes ordinary user roles from system-admin override.
- The lane names one minimum book action set that later code and drill work can reuse.
- The lane identifies which questions are deferred to later `plan / entitlement / mock billing` widening rather than hiding them inside vague admin wording.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the minimum access vocabulary and object boundary are explicit
  - the first `book` action set is explicit
  - one replayable role flow is named and defended
- `stable` for this opening packet does not require mock billing or feature-plan realism; it requires the access boundary to be explicit enough for later execution.

## P0 (Contract | v1)

### P0-C1-S1 (Principal and role vocabulary)

- Fix the minimum vocabulary for `user`, `membership`, `book_role`, and `system_role`.
- Keep ordinary collaboration roles distinct from platform/system override.

### P0-C1-S2 (Book-first authorization boundary)

- `book` is the first independent authorization container.
- `block` inherits `book` standing and must not open independent ACL in v1.

### P0-C1-S3 (Deferred commercial layer)

- `plan`, `entitlement`, and later `subscription_state` remain reserved extension concepts.
- The first lane must stay coherent even if those concepts are left unimplemented.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-10A/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Implementation mapping and minimum action matrix)

- `P1-C1-S1`: fix one minimum `book` action set such as `read_book`, `edit_book`, `share_book`, `delete_book`, `transfer_book_owner`, and `manage_book_members`
- `P1-C1-S2`: map those actions onto the current SoT without reopening `block` as an independent ACL object

### P2 (Drill / Replay)

- `P2-C1-S1`: prove one owner-to-editor share flow where the editor can edit but cannot re-share or transfer owner standing
- `P2-C1-S2`: prove one bounded system-admin override that does not turn system admin into a normal collaboration role

### P3 (Widening decision)

- `P3-C1-S1`: decide whether `plan / entitlement` should remain deferred or partially enter the lane after the book-first closure is stable
- `P3-C1-S2`: decide whether mock billing deserves its own later packet instead of staying embedded in the same opening lane

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: fix the minimum principal and role vocabulary
- [ ] `P0-C1-S2`: fix the book-first authorization boundary and block-inheritance rule
- [ ] `P0-C1-S3`: make the deferred commercial layer explicit

### P1 (Implementation mapping and minimum action matrix)

- [ ] `P1-C1-S1`: fix one minimum `book` action set
- [ ] `P1-C1-S2`: map the action set onto the current SoT without block-level ACL

## Current Status (recommended)

- `S0F-10A` is now opened as the first real `M4` child log under `road-002`.
- The lane is still in contract-first opening state: the minimum role vocabulary, book-first boundary, and deferred commercial layer are now named, but the first SoT-side action matrix and replay drill still remain open.
- Automation should still read this log as an active source packet rather than as a stable policy artifact.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane begins making real bounded changes.
- This section intentionally remains empty at scaffold time.

## Recent changes (for traceability, optional)

- 2026-04-15: opened `S0F-10A` as the first real `M4` child log so the access-control lane no longer remains only as roadmap prose and draft notes.
- 2026-04-15: fixed the opening lane around book-first minimum closure, user/admin role separation, and explicit block inheritance, while keeping `plan / entitlement / mock billing` as later widening decisions rather than first-packet obligations.