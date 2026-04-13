# log-S0F-7G (Phase 7G: approval-facing screenshot evidence review and attachment protocol)

---

**id**: `S0F-7G`
**kind**: `log`
**title**: `approval-facing screenshot evidence review and attachment protocol`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Evidence, Records, epic/s0, sub/7g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
  **reference_log_1**: `docs/logs/log-S0F-7F-log-and-roadmap-frontmatter-minimum-time-fields.md`
  **reference_log_2**: `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  **reference_log_3**: `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  **reference_log_4**: `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
**issue_keyword**: `evidence`
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

- `S0F-7G` opens as the bounded follow-up after `S0F-7F` for one narrower evidence-governance problem: screenshot-backed supplement packets are now structurally traceable, but approval and review still remain awkward when the reviewer cannot directly open, inspect, and judge the attached evidence from the packet itself.
- This lane will first define one approval-facing attachment and screenshot review protocol for supplement-ledger packets; it will not yet widen into a repo-wide actor/authority/provenance control plane.

**Default choices (phase defaults / v1)**:

- Keep the first landing surface inside supplement-ledger packets rather than trying to retrofit every log, roadmap, and contract immediately.
- Prefer stable attachment ids plus clickable repo-local asset refs over embedding full screenshots directly into the main evidence tables.
- Add review-facing structure only where it materially improves packet readability: attachment access, concise reviewer notes, approval state, and defended basis for acceptance or rejection.
- Keep asset review separate from historical-effective time: screenshot visibility solves evidence readability, not chronology semantics.
- Defer actor-rich provenance fields such as `submitted_by`, `verified_by`, and `approved_by` unless the attachment-review pilot proves that review usability alone is still insufficient.

## Problem Statement

- `S0F-7D` and `S0F-7F` now let the repo admit screenshot evidence through one parent-ledger plus SUP chain, but the current packet shape still assumes that attachment ids and file paths alone are enough for approval-facing review.
- In practice, that leaves one missing governance surface:
  - reviewers need one consistent way to open the image evidence quickly from the packet
  - reviewers need one bounded place to record what was actually checked or why one screenshot was accepted, rejected, or left pending
  - the repo still needs to avoid bloating the main evidence tables into image galleries or mixing screenshot review with broader provenance-actor governance too early
- The repo therefore needs one narrow follow-up lane that answers three questions before any broader approval model is attempted:
  - what minimum supplement-ledger structure makes screenshot evidence directly reviewable
  - how attachment ids and repo-local asset refs should be rendered so reviewers can click through without ambiguity
  - which smallest live packet should prove the protocol before any repo-wide adoption rule is declared

## Exported Sections / Outlet Ownership

- This slice starts as one `support-only ledger + template + log-retained core` governance-design lane.
- The expected first landing is one supplement-ledger review protocol and one sample packet update that proves approval-facing readability without changing contract ownership.

**Outlet ownership**:

- `contract`: no-op by default; contract packets should consume improved approved evidence, not become the first image-review surface
- `runbook`: no-op by default
- `view`: no-op by default; a future reviewer-facing evidence index may emerge later, but it is not assumed here
- `index/front-door`: no-op by default
- `disposition/placement`: supplement-ledger template and pilot packets are the first mutable landing surfaces
- `log-retained core`: lane boundary, review protocol, pilot verdicts, and any deferred provenance expansion stay here

## Definitions (optional)

- `approval-facing screenshot review`: the minimum structure that lets a reviewer open an image asset, understand what claim it is supposed to prove, and record a bounded judgment.
- `click-through attachment ref`: one repo-local asset path or equivalent stable ref presented so the reviewer can open the evidence directly from the packet.
- `attachment review note`: one compact reviewer-facing note that records what was checked, what was visible, or why the evidence was accepted, rejected, or deferred.
- `approval basis`: the concise rationale connecting the visible attachment evidence to the packet verdict.

## Constraints

- Do not embed full screenshots directly into the main supplement evidence table by default.
- Do not reopen the chronology model; this lane is about reviewability of attachments, not new time semantics.
- Do not widen immediately into full actor / authority / organization provenance fields unless the first attachment-review pilot proves that narrower review structure is insufficient.
- Do not break existing supplement naming, attachment-id, or parent-ledger binding rules.

## Scope

- `P0`: open `S0F-7G` and bound the problem to approval-facing screenshot evidence review inside supplement-ledger packets
- `P1`: define the minimum attachment review protocol, including clickable asset refs, review-note shape, and approval-state semantics
- `P2`: apply the protocol to one first live sample, expected first on `ledger-SUP-S0A-1A-001`
- `P3`: decide whether reviewer/approver actor fields are truly needed next or should remain deferred to a later provenance-governance lane

## Success Criteria (DoD)

- The repo has one explicit minimum rule for making screenshot evidence directly reviewable from a supplement packet.
- The repo has one explicit rule for how attachment refs should appear so reviewers can click through to the source asset without ambiguity.
- The repo has one bounded reviewer-facing note or approval-basis surface that records what was actually checked without turning supplement packets into image galleries.
- The repo proves the protocol on one live packet before declaring wider adoption.
- Any broader actor/provenance governance expansion is either explicitly deferred or opened as a separate bounded lane.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the minimum attachment-review protocol is explicitly written
  - one live supplement packet demonstrates the protocol cleanly
  - the lane records whether actor-rich provenance or approval-role fields are still needed next or should remain deferred
- `stable` does not require repo-wide migration; one accepted sample-first protocol is sufficient.

## P0 (Lane boundary | v1)

### P0-C1-S1 (Open `S0F-7G` as the screenshot-review follow-up)

- Open one bounded follow-up lane after `S0F-7F` for approval-facing screenshot evidence review and attachment readability.

### P0-C1-S2 (Fix the first landing surface before wider governance expansion)

- The first mutable landing surface is the supplement-ledger template plus one first live packet rather than a repo-wide frontmatter rewrite.

## Plan (draft)

### P1 (Minimum attachment review protocol)

- `P1-C1-S1`: define how attachment refs should be rendered for click-through review
- `P1-C1-S2`: define one minimum review-note and approval-basis surface for screenshot evidence rows

### P2 (First live packet pilot)

- `P2-C1-S1`: patch the supplement-ledger template with the approved review protocol
- `P2-C1-S2`: apply the protocol to `ledger-SUP-S0A-1A-001` as the first live screenshot-review sample

### P3 (Deferred provenance decision)

- `P3-C1-S1`: decide whether actor-rich provenance or approval-role fields are actually required next

## Execution Checklist (unchecked)

### P0 (Lane boundary)

- [x] `P0-C1-S1`: open `S0F-7G` as the screenshot-review follow-up
- [x] `P0-C1-S2`: fix the first landing surface before wider governance expansion

### P1 (Minimum attachment review protocol)

- [x] `P1-C1-S1`: define how attachment refs should be rendered for click-through review
- [x] `P1-C1-S2`: define one minimum review-note and approval-basis surface for screenshot evidence rows

### P2 (First live packet pilot)

- [x] `P2-C1-S1`: patch the supplement-ledger template with the approved review protocol
- [x] `P2-C1-S2`: apply the protocol to `ledger-SUP-S0A-1A-001` as the first live screenshot-review sample

### P3 (Deferred provenance decision)

- [x] `P3-C1-S1`: decide whether actor-rich provenance or approval-role fields are actually required next

## Current Status (recommended)

- `S0F-7G` is now opened as the bounded follow-up after `S0F-7F` for approval-facing screenshot evidence review and attachment click-through structure.
- The lane is intentionally scoped to supplement-ledger readability first; it does not yet commit the repo to a broader provenance / actor / authority model.
- `P1-C1-S1` is now complete: the SUP protocol now requires click-through markdown links for stable repo-local assets instead of relying on bare path prose only.
- `P1-C1-S2` is now complete: the SUP protocol now defines one minimum `Attachment Review Table` with `review status`, `approval basis`, and `review note` as the approval-facing review surface.
- `P2-C1-S1` is now complete: the SUP template now exposes the attachment-review protocol without disturbing the existing routing-focused evidence table.
- `P2-C1-S2` is now complete: `ledger-SUP-S0A-1A-001` now proves the protocol on three live screenshot rows, each with one direct click-through link and one bounded approval-facing review record.
- `P3-C1-S1` is now complete: actor-rich reviewer / approver provenance fields remain deferred because the narrower reviewability problem is now handled by the attachment-review protocol plus one table-external quick-review surface.
- The next step is to judge whether this narrower screenshot-review protocol is now stable enough to retain as-is or whether a later separate lane should open specifically for provenance / authority actors.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths when the lane starts mutating templates or live supplement packets.
- This section stays empty until the first template or pilot patch is actually landed.

### P1-C1-S1S2 + P2-C1-S1S2 (Minimum screenshot-review protocol and first live packet pilot fixed | 2026-04-13)

- headSha: `e4671f222`

- artifacts:
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
- expected:
  - screenshot-backed SUP packets should expose one direct click-through path to stable repo-local image assets instead of forcing reviewers to copy bare file paths manually
  - approval-facing review should stay compact and packet-local, using one bounded review surface rather than turning the main evidence table into an embedded image gallery
  - the first live packet should prove that screenshot evidence can carry `review status`, `approval basis`, and `review note` without reopening broader actor or provenance modeling
- observed:
  - the SUP template now requires clickable markdown links for stable repo-local attachments and defines one dedicated `Attachment Review Table` for approval-facing review
  - `ledger-SUP-S0A-1A-001` now exposes direct click-through links for all three screenshot assets and records one bounded review row for each attachment
  - the live pilot proves that packet-level screenshot review can be made directly readable without changing the chronology model or introducing actor-rich provenance fields yet

### P3-C1-S1 (Actor-rich provenance decision deferred; quick-review surface added | 2026-04-13)

- artifacts:
  - `docs/logs/_template-support-only-contract-release-ledger-SUP.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
- expected:
  - the lane should decide whether actor-rich provenance fields are truly needed now or whether the narrower reviewability problem is already solved by better attachment access and review ergonomics
  - if table-cell link rendering proves too weak, the packet should expose one table-external review surface rather than forcing a bigger provenance-field expansion
- observed:
  - the current attachment-review protocol is sufficient for the bounded screenshot-review problem, so actor-rich provenance fields remain deferred for now
  - the SUP template and live pilot now also expose one `Attachment Quick Review` section with standalone links and inline previews, making the screenshots directly visible and easier to open from the packet outside the tables