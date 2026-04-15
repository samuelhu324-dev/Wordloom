# log-S0F-10A (Phase 10A: Book-first access control minimum closure)

---

**id**: `S0F-10A`
**kind**: `log`
**title**: `book-first access control minimum closure and role boundary v1`
**status**: `stable`
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
**roadmap_bridge_refs**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4:-Book-first-access-control-minimum-closure-on-the-current-SoT, docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4:-Book-first-access-control-minimum-closure-on-the-current-SoT, docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4:-Book-first-access-control-minimum-closure-on-the-current-SoT`
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

### P1 Minimum Action Matrix Decision (v1)

- `P1` is now fixed as one minimum action packet around `book` rather than as one full tenant-plan-entitlement system.
- The first independent authorization object remains `book`.
- The minimum ordinary collaboration roles are now fixed as:
  - `viewer`
  - `editor`
  - `owner`
- The minimum platform/system role is now fixed as:
  - `system_admin`
- The first minimum action set is now fixed as:
  - `read_book`
  - `edit_book`
  - `share_book`
  - `delete_book`
  - `transfer_book_owner`
  - `manage_book_members`
- The `P1` success rule in this packet is:
  - one reader should be able to answer ordinary collaboration rights from one small role matrix rather than from prose-only interpretation
  - `block` should remain inherited content structure and must not require its own ACL row
  - `system_admin` should be legible as platform override rather than as one stronger ordinary collaborator

#### P1 Role And Action Matrix (v1)

| role | read_book | edit_book | share_book | delete_book | transfer_book_owner | manage_book_members | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `viewer` | `allow` | `deny` | `deny` | `deny` | `deny` | `deny` | Viewers can read one shared book but cannot mutate content or permissions. |
| `editor` | `allow` | `allow` | `deny` | `deny` | `deny` | `deny` | Editors may change book content but cannot change sharing, ownership, or membership standing. |
| `owner` | `allow` | `allow` | `allow` | `allow` | `allow` | `allow` | Owners are the ordinary collaboration authority surface for book lifecycle and membership control. |
| `system_admin` | `bounded-override-only` | `bounded-override-only` | `bounded-override-only` | `bounded-override-only` | `bounded-override-only` | `bounded-override-only` | System admin is not a normal collaboration role and should act only through explicit platform override paths. |

#### P1 SoT Mapping Notes (v1)

- `tenant` remains the broader identity and containment surface for later widening, but it is not the first independent authorization object in this packet.
- `membership` remains the bounded relation that allows one user to appear inside the tenant and later receive book-level standing.
- `library` and `bookshelf` remain organization or navigation surfaces in this packet rather than first-class ACL containers.
- `book` is the first independent authorization object.
- `block` inherits `book` standing and should be interpreted as follows in v1:
  - if one user may `read_book`, that user may read the blocks inside that book
  - if one user may `edit_book`, that user may edit the blocks inside that book
  - block movement, export filtering, and block-specific sharing remain deferred until a later widening packet explicitly proves that those problems need an independent policy surface

### P2 (Drill / Replay)

- `P2-C1-S1`: prove one owner-to-editor share flow where the editor can edit but cannot re-share or transfer owner standing
- `P2-C1-S2`: prove one bounded system-admin override that does not turn system admin into a normal collaboration role

### P2 Drill Decision (v1)

- `P2` now stays on the same `book`-first packet and proves one replayable minimum flow instead of widening into plan or billing realism.
- The first ordinary collaboration drill is now fixed as:
  - owner creates or holds one book
  - owner grants `editor` standing to one second user
  - editor can read and edit but cannot re-share, delete, transfer owner, or manage members
  - owner revokes the editor standing cleanly
- The first platform override drill is now fixed as:
  - one `system_admin` may perform a bounded break-glass recovery action when normal owner control is unavailable or must be corrected
  - that recovery action should be legible as platform override rather than as ordinary collaboration standing
- The `P2` success rule in this packet is:
  - one reader should be able to replay one owner/editor/share-revoke flow without guessing hidden role semantics
  - one reader should be able to explain what `system_admin` may do without treating system admin as a default owner or editor
  - the lane should still avoid `plan / entitlement / mock billing` dependence

#### P2 Replay Drill A (Owner / Editor / Revoke)

| drill step | actor | intended action | expected result | why it matters |
| --- | --- | --- | --- | --- |
| `A1` | `owner` | grant `editor` standing on one book to one second user | `allow` | The lane must prove ordinary collaboration can be delegated without changing book ownership. |
| `A2` | `editor` | read and edit that book | `allow` | Editors need one clear productive role in the first closure. |
| `A3` | `editor` | re-share the book, delete the book, transfer owner, or manage members | `deny` | The lane must prove content-edit rights do not silently become authority over collaboration or lifecycle control. |
| `A4` | `owner` | revoke the editor standing | `allow` | The lane must prove ordinary collaboration rights remain revocable by the current owner. |

#### P2 Replay Drill B (System-Admin Override Boundary)

| drill step | actor | intended action | expected result | why it matters |
| --- | --- | --- | --- | --- |
| `B1` | `system_admin` | inspect book standing for support or recovery purposes | `allow-via-override` | The platform needs one bounded support path that is not confused with ordinary collaboration. |
| `B2` | `system_admin` | repair or reset book access when ownership is stuck, orphaned, or administratively invalid | `allow-via-override` | The lane must prove one platform-side recovery seam exists. |
| `B3` | `system_admin` | remain as long-lived ordinary collaborator on the book by default | `deny` | System admin should not become a disguised owner or editor role. |
| `B4` | `system_admin` | bypass the entire role model for everyday use | `deny` | The override seam must stay bounded or the first lane loses all role separation value. |

### P3 (Widening decision)

- `P3-C1-S1`: decide whether `plan / entitlement` should remain deferred or partially enter the lane after the book-first closure is stable
- `P3-C1-S2`: decide whether mock billing deserves its own later packet instead of staying embedded in the same opening lane

### P3 Widening Decision (v1)

- `P3` is now fixed as a boundary decision rather than as the start of a second hidden implementation stream inside `S0F-10A`.
- The minimum closure fixed by `P0-P2` is now considered stable enough to stand on its own without introducing commercial realism.
- `plan` and `entitlement` remain deferred from this lane's core rules in the following sense:
  - they are valid later extension concepts
  - they must not rewrite the `book`-first authorization boundary already fixed here
  - they must not turn `system_admin` into a commercial-plan alias or broaden `book_role` semantics by accident
- `mock billing` is now explicitly kept out of `S0F-10A` and should open only as its own later packet once the repo can defend why subscription state changes must alter entitlement state.
- The `P3` success rule in this packet is:
  - one reader should be able to explain which access questions are already answered by `S0F-10A`
  - one reader should be able to explain which commercial or entitlement questions are intentionally not answered here
  - later widening should have to prove a new need instead of silently accreting into the minimum closure lane

#### P3 Deferred-vs-Later-Packet Decision Table (v1)

| topic | decision in `S0F-10A` | reason |
| --- | --- | --- |
| `book` collaboration rights | `keep-in-lane` | The lane already fixes the minimum ordinary collaboration and override boundary around one `book`. |
| `plan` | `defer` | Commercial packaging is not required to explain who may read, edit, share, revoke, or recover one book. |
| `entitlement` | `defer` | A later entitlement model may widen resource-action control, but it should layer on top of the current `book`-first closure rather than replace it. |
| `mock billing` | `split-to-later-packet` | Billing state changes are an external trigger surface and would add product-policy complexity that this minimum access packet does not need. |
| block-level gating or monetized export/copy rules | `defer` | Those questions should only enter after a later packet proves that book-level standing is insufficient. |

#### P3 Later-Packet Entry Conditions (v1)

- A later widening packet may open only when at least one of these conditions becomes concrete:
  - the product must gate actions that cannot be defended by `viewer / editor / owner / system_admin` alone
  - subscription or trial state must change effective access outcomes in a way the current lane cannot express cleanly
  - one resource beyond `book` requires an independent authorization or entitlement surface backed by concrete drills rather than speculation
- Until one of those conditions is real, later work should treat `S0F-10A` as the stable minimum access baseline and should not reopen this lane just to host speculative commerce design.

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: fix the minimum principal and role vocabulary
- [ ] `P0-C1-S2`: fix the book-first authorization boundary and block-inheritance rule
- [ ] `P0-C1-S3`: make the deferred commercial layer explicit

### P1 (Implementation mapping and minimum action matrix)

- [x] `P1-C1-S1`: fix one minimum `book` action set
- [x] `P1-C1-S2`: map the action set onto the current SoT without block-level ACL

### P2 (Drill / Replay)

- [x] `P2-C1-S1`: prove one owner-to-editor share flow where the editor can edit but cannot re-share or transfer owner standing
- [x] `P2-C1-S2`: prove one bounded system-admin override that does not turn system admin into a normal collaboration role

## P3 (Widening decision)

- [x] `P3-C1-S1`: decide whether `plan / entitlement` should remain deferred or partially enter the lane after the book-first closure is stable
- [x] `P3-C1-S2`: decide whether mock billing deserves its own later packet instead of staying embedded in the same opening lane

## Current Status (recommended)

- `S0F-10A` is now opened as the first real `M4` child log under `road-002`.
- `P0` is now complete: the lane explicitly fixes the minimum principal vocabulary, the book-first authorization boundary, and the deferred commercial layer instead of leaving those choices only in roadmap prose.
- `P1` is now complete: the lane now carries one concrete first role-and-action matrix for `viewer`, `editor`, `owner`, and `system_admin`, plus one explicit SoT mapping that keeps `block` under inherited `book` standing.
- `P2` is now complete: the lane now carries one replayable owner/editor/share-revoke flow and one bounded system-admin override flow, so ordinary collaboration and platform override are no longer only implied design intent.
- `P3` is now complete: `plan` and `entitlement` remain deferred from this minimum closure lane, while `mock billing` is explicitly split to a later packet instead of being embedded into `S0F-10A`.
- `S0F-10A` now stands as the stable minimum access baseline for `M4-P0` through `M4-P3`: later widening must layer on top of this packet instead of quietly rewriting it.
- Automation may now read this log as the stable minimum-closure source packet for the first `M4` lane, while treating later entitlement or billing work as separate widening work rather than as unfinished content inside this packet.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane begins making real bounded changes.
- This section intentionally begins as a policy-evidence ledger because the first packet is fixing contract and replay semantics rather than shipping code paths.

### P1-C1-S1S2 (Minimum book role and action matrix fixed for the first closure | 2026-04-15)

- headSha: `c4990a149`
- artifacts:
  - `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
- expected:
  - the lane should name one minimum ordinary collaboration matrix instead of leaving role semantics only in roadmap prose
  - the packet should keep `book` as the first independent authorization object and keep `block` under inherited standing
  - the packet should distinguish ordinary user roles from system-admin override without requiring plan or billing realism
- observed:
  - the lane now fixes one first role matrix for `viewer`, `editor`, `owner`, and `system_admin`, with ordinary collaboration rights and platform override separated explicitly
  - the SoT mapping now states that `tenant`, `membership`, `library`, and `bookshelf` remain broader context surfaces while `book` is the first independent authorization object
  - the packet now explicitly states that `block` inherits `book` standing for both read and edit interpretation in v1 and does not open block-level ACL

### P2-C1-S1S2 (Replayable owner/editor and system-admin boundary drills fixed for the first closure | 2026-04-15)

- headSha: `c4990a149`
- artifacts:
  - `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
- expected:
  - the lane should prove one ordinary collaboration share-revoke flow that can be replayed without guessing hidden semantics
  - the lane should prove one bounded system-admin override seam without turning system admin into a disguised ordinary collaborator
  - the drills should still avoid dependence on `plan / entitlement / mock billing`
- observed:
  - the lane now fixes one owner-to-editor flow where editors can read and edit but cannot re-share, delete, transfer owner, or manage members
  - the lane now fixes one bounded system-admin override seam for inspection and recovery without default long-lived collaboration standing
  - the first packet therefore now answers both ordinary collaboration and platform override questions at minimum-closure level while still deferring commercial widening

### P3-C1-S1S2 (Commercial widening explicitly deferred and split beyond the minimum closure packet | 2026-04-15)

- headSha: `4c3c84104`
- artifacts:
  - `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  - `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
- expected:
  - the lane should stop leaving `plan / entitlement / mock billing` as an open ambiguity after the minimum closure is already fixed
  - the packet should decide whether commercial widening belongs inside `S0F-10A` or in a later dedicated packet
  - the result should preserve the `book`-first role boundary rather than diluting it with speculative plan design
- observed:
  - `S0F-10A` now explicitly keeps `plan` and `entitlement` deferred from the minimum closure packet and states that later widening must layer on top of the current access baseline
  - `mock billing` is now explicitly split to a later packet instead of being embedded into the opening `book`-first lane
  - the first `M4` lane can now be treated as a stable minimum closure rather than as a partially finished commercial-access hybrid

## Recent changes (for traceability, optional)

- 2026-04-15: opened `S0F-10A` as the first real `M4` child log so the access-control lane no longer remains only as roadmap prose and draft notes.
- 2026-04-15: fixed the opening lane around book-first minimum closure, user/admin role separation, and explicit block inheritance, while keeping `plan / entitlement / mock billing` as later widening decisions rather than first-packet obligations.
- 2026-04-15: completed `P1-C1-S1S2` by fixing the first minimum role-and-action matrix around `book`, plus the first SoT mapping that keeps `block` under inherited standing.
- 2026-04-15: completed `P2-C1-S1S2` by fixing one replayable owner/editor/share-revoke flow and one bounded system-admin override flow for the same minimum closure packet.
- 2026-04-15: completed `P3-C1-S1S2` by explicitly deferring `plan / entitlement`, splitting `mock billing` to a later packet, and declaring `S0F-10A` the stable minimum access baseline for the first `M4` lane.