# log-S0F-7C (Phase 7C: old-log decomposition application lane)

---

**id**: `S0F-7C`
**kind**: `log`
**title**: `old-log decomposition application lane`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contracts, Ledger, Migration, Application, epic/s0, sub/7c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7B-release-based-contract-lineage-and-ledger-model.md`
  **reference_log_1**: `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  **reference_log_2**: `docs/logs/log-S0F-7B-release-based-contract-lineage-and-ledger-model.md`
  **reference_log_3**: `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
  **reference_log_4**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_5**: `docs/logs/_template-support-only-contract-release-ledger.md`
**issue_keyword**: `migration`
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
**created**: `2026-04-10`
**updated**: `2026-04-10`

---

## Decision / Outcome

**Decision**:

- `S0F-7C` opens as the first application lane that uses the `7A + 7B` contract standards against additional old `S0` source logs instead of reopening the model layer.
- This lane exists because `7A` and `7B` are now strong enough to guide real decomposition work, and the next useful validation is repeated source-to-contract extraction plus explicit parent-shape synthesis rather than another abstract design pass.
- The first active target is now fixed as `S0B-3A`, which is a real local log plus linked issue context, not an issue-only source.

**Default choices (phase defaults / v1)**:

- Treat `7A` as the active chronology-first and family-boundary baseline.
- Treat `7B` as the active `family + release + ledger` baseline.
- Use `S0F-7C` only to apply, test, and minimally tighten those standards while decomposing old logs and synthesizing broader parent readings from repeated child usage where later evidence justifies that widening.
- Prefer one bounded source target at a time rather than one wide multi-source migration wave.
- When one source mixes contract-worthy rules with support-only transport or chronology material, route that split through one ledger instead of forcing every slice directly into one contract release.
- When one rule surface first appears in one narrow child context but later proves to span multiple document kinds or sibling families, let that rule be extracted narrowly first and widened later through a parent or broader-family release rather than forcing the first extraction to be fully general.

## Problem Statement

- The repo now has a stronger contract model than before, but the model still needs repeated application against older counted sources so the remaining ambiguities surface under real migration pressure.
- Without an application lane, the repo risks over-refining templates while delaying three harder questions:
  - how one mixed old log should actually be sliced into contracts, ledgers, deferred items, or retained-only history
  - how later `parent` contracts should be synthesized from repeated child usage and cross-kind reuse rather than assumed to appear fully formed in the first extraction pass
  - which earlier mixed-source contract packets now need selective ledger backfill because routing ambiguity has become visible only after later contract growth
- `S0B-3A` is a good first target because it is already treated as one structural prerequisite for current `DOC` history reading, yet its body still mixes multiple concerns:
  - logs-facing unified indices and title identity rules
  - front matter metadata rules that may begin in one child surface before widening later
  - lifecycle ownership over legacy taxonomy, freeze, migrate-on-demand, stub, and cutover boundaries
  - dual-use cutover semantics that may feed both lifecycle and logs-oriented contract bodies
- That makes `S0B-3A` the right first proof of whether `7A/7B` can decompose one mixed old source into child contracts, leave a parent partially synthesized, and still preserve later widening paths without losing source accountability.

## Exported Sections / Outlet Ownership

- This slice starts as one `contract + support-only ledger + parent-synthesis` application lane.
- The default expected landing is one bounded `S0B-3A` decomposition packet, one explicit first synthesis rule set for later parents, and any minimal follow-on ledger refinements proven necessary by that real extraction pass.

**Outlet ownership**:

- `contract`: expected landing surface for any release records that emerge from `S0B-3A`
- `support-only ledger`: expected landing surface for source slicing, deferred destinations, and retained-only sections
- `log-retained core`: expected landing surface for the bounded migration rationale, execution notes, and evidence
- `parent synthesis notes`: expected landing surface for the rule that broader parent contracts may be progressively completed from repeated child extraction and cross-kind reuse
- `view`: no-op by default; existing views already narrate `S0B-3A`, but this lane is about contract extraction rather than reader projection
- `runbook`: no-op by default

## Constraints

- Do not reopen `7A` or `7B` as if their core model were still unset.
- Do not assume `S0B-3A` should collapse into one single contract; the source may require multiple destinations or one ledger-first pass.
- Do not treat all `S0B-3A` content as equally contract-worthy; some sections may remain support-only, deferred, or retained-only.
- Do not assume the first extracted child contract already expresses the final generalized parent rule; later widening may be necessary and should be recorded explicitly.
- Do not force the current ledger model to hide real dual-use semantics; when one source slice clearly feeds more than one rule surface, either split the slice more precisely or record the need for a later multi-consumption refinement.
- Do not backfill ledgers for every historical source by default; ledger backfill should stay selective and target only packets where mixed routing, deferred slices, or later overlap now make the missing ledger materially costly.
- Do not force short-name legacy contract ids back into the new chronology-first family grammar.
- Do not ignore the linked issue context just because the local log exists; the issue may still clarify intent and should remain eligible as direct source support where needed.

## Scope

- `P0`: open `S0F-7C`, fix the application-lane boundary, and lock `S0B-3A` as the first decomposition target
- `P1`: reconstruct the bounded source packet for `S0B-3A`, including the local log, issue `44`, and only the bounded upstream context still needed to read the first extraction accurately
- `P2`: record the application-driven decomposition rules learned from `S0B-3A`, especially `child-first extraction`, `later parent synthesis`, and `dual-use slice handling`
- `P3`: emit the first `S0B-3A` decomposition outputs, expected as one ledger plus one or more child-family candidate contract releases such as `LOGS-0001` and `LIFECYCLE-0001`
- `P4`: selectively backfill missing ledgers for earlier mixed-source packets only where later overlap or deferred routing now makes those ledgers operationally necessary
- `P5`: normalize status, release_action, lineage, cumulative-source usage, and future parent-promotion notes so the emitted packet can be reused as the next migration pattern

## Success Criteria (DoD)

- The repo has one live example of using `7A + 7B` to decompose one mixed old log into concrete contract-era outputs.
- `S0B-3A` is no longer only a history/view prerequisite; it also has one explicit contract/ledger judgment packet.
- The lane makes explicit that broader parent contracts may be completed progressively from repeated child extraction and cross-kind reuse rather than assumed complete in one first pass.
- The resulting packet makes clear which `S0B-3A` slices were promoted, deferred, retained-only, or still awaiting another family.
- The lane now distinguishes between `extract now as child`, `widen later into parent`, and `backfill ledger only where routing ambiguity now justifies the cost`.
- Any rule gaps discovered during this pass are recorded as minimal application-driven refinements rather than one fresh abstract redesign.

## P0 (Application-lane boundary | v1)

### P0-C1-S1 (Application lane opened after `7B` | v1)

- `S0F-7C` is now the bounded follow-on lane after `7B` for repeated old-log decomposition work.
- Under this rule, `7C` does not redefine the model; it proves the model by applying it to additional counted old sources.

### P0-C1-S2 (First target fixed as `S0B-3A` | v1)

- The first active source target for this lane is now `S0B-3A`.
- The lane now explicitly records that `S0B-3A` has both:
  - one local source log at `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
  - one linked issue context via issue `44`
- Under this rule, the first decomposition pass should treat `S0B-3A` as `log-first with issue support`, not as `issue-only reconstruction`.

## Plan (draft)

### P1 (Bounded source reconstruction for `S0B-3A`)

- `P1-C1-S1`: read the local `S0B-3A` log as the primary source body
- `P1-C1-S2`: pull in issue `44` only where it sharpens intent, scope, or missing rationale
- `P1-C1-S3`: classify upstream references as either `direct support` or `bounded background` rather than letting all earlier anchors silently become release input

### P1-C1-S1 (Local `S0B-3A` log fixed as the primary source body | v1)

- The local `S0B-3A` log is now fixed as the primary source body for this decomposition pass.
- Under this rule, the first extraction must read the local log as the owning surface for four first-pass slices:
  - logs-facing unified indices and title identity rules
  - front matter fields as they first appear in one logs-facing operational surface
  - legacy taxonomy and explicit `Legacy Refs` handling
  - cutover plus stub policy as historical lifecycle boundary material
- This means the lane should not treat later cross-kind reuse as proof that `S0B-3A` already owns the final generalized parent form of those rules.

### P1-C1-S2 (Issue `44` fixed as sharpening support, not replacement ownership | v1)

- Issue `44` is now fixed as direct support only where it sharpens the local `S0B-3A` log rather than replacing it as the source owner.
- The issue contributes two bounded clarifications that matter for the first extraction pass:
  - from the `S0B-2A` side, it sharpens why legacy taxonomy, cutover, and stub handling became urgent rather than optional cleanup detail
  - from the earlier docs-management side, it sharpens why stable identifiers, decoupled chronology, and front matter were being pursued as one reusable management pattern rather than one isolated file naming tweak
- Under this rule, issue `44` is direct support for intent and scope, but the emitted `S0B-3A` child candidates should still read the local log as the primary historical owner for this target.

### P1-C1-S3 (Upstream references classified as direct support versus bounded background | v1)

- The bounded source packet for `S0B-3A` is now classified in three layers:
  - `primary source`:
    - `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
  - `direct support`:
    - issue `44` as the immediate context that ties `S0B-3A` back to the active docs-management concerns now being reconstructed
  - `bounded background`:
    - `S0B-2A` as near-cause pressure for legacy, cutover, and stub semantics, but not as the replacement owner of `S0B-3A` rule text
    - the earlier docs-management issue context as upstream rationale for identifier decoupling and front matter, but not yet as the direct owner of the first `S0B-3A` child releases
    - older legacy refs and ADR ancestry only when later extraction needs them to justify one specific migrated slice
- Under this rule, `P2` should start from the `S0B-3A` body itself and use the upstream packet only to sharpen scope and provenance, not to silently widen the first extraction into one already-generalized parent contract.

### P2 (Application rules discovered from `S0B-3A`)

- `P2-C1-S1`: define `child-first extraction, later parent synthesis` as the default reading when one broad rule surface is only partially visible in the first source packet
- `P2-C1-S2`: define how broad cross-kind content such as front matter may begin as one child-owned extraction and widen later only after repeated evidence proves the broader parent shape
- `P2-C1-S3`: define how dual-use slices such as cutover should be handled, preferring narrower slice splitting first and reserving explicit multi-consumption refinement for cases that remain irreducibly shared

### P2-C1-S1 (First `S0B-3A` child extraction targets fixed as `LOGS` and `LIFECYCLE` | v1)

- The first `S0B-3A` child extraction targets are now fixed as two narrower workflow families rather than one mixed contract body:
  - `DOC-WORKFLOW-LOGS-0001` for the logs-facing identity and intake body
  - `DOC-WORKFLOW-LIFECYCLE-0001` for legacy, freeze, migrate-on-demand, stub, and lifecycle-boundary ownership
- Under this rule, the `S0B-3A` source packet should no longer be judged as one monolithic contract candidate.
- The default first-pass ownership split is now:
  - `LOGS` owns unified indices as they appear in log-facing title and identity rules, along with the logs-facing front matter body and log identity mechanics
  - `LIFECYCLE` owns legacy taxonomy, explicit `Legacy Refs`, freeze-versus-migrate boundaries, stub preservation, and lifecycle-oriented cutover semantics
- This keeps the first extraction narrow while preserving room for one broader parent reading to emerge later from repeated sibling use.

### P2-C1-S2 (Front matter fixed as child-first extraction with later widening path | v1)

- Front matter is now fixed as `child-first extraction` rather than one already-generalized parent rule at the first `S0B-3A` pass.
- Under this rule:
  - the first emitted front-matter rule body should live in the logs-oriented child candidate because `S0B-3A` owns the earliest explicit operational wording in a logs-facing surface
  - later parent or broader-family widening remains explicitly allowed if repeated evidence later shows that the same front-matter rule body truly spans logs, labs, runbooks, ADRs, and other document kinds as one stable generalized contract surface
- This means `front matter` is not denied a broader future home; it is simply prevented from over-widening the first extraction beyond what the current packet can defend directly.

### P2-C1-S3 (Cutover split into two same-source slices before any multi-consumption model | v1)

- The `cutover` material is now fixed as two narrower same-source slices rather than one unresolved dual-use row.
- The two first-pass slices are:
  - `cutover as logs intake rule`: new structured log content must follow the new identifier, title, and logs-facing metadata discipline from the cutover boundary onward
  - `cutover as lifecycle boundary`: legacy content remains frozen reference material by default, with migration-on-demand and stub preservation controlling how older material re-enters the active system
- Under this rule, both slices still trace back to the same `S0B-3A` source packet, but the first ledger should record them separately so the repo can avoid hiding real dual-use semantics behind one ambiguous single row.
- Explicit multi-consumption refinement remains reserved for later only if a still-narrower split cannot explain future shared usage cleanly.

### P3 (First `S0B-3A` decomposition outputs)

- `P3-C1-S1`: create one `S0B-3A` support-only ledger because the source now clearly spans multiple destinations and deferred widening paths
- `P3-C1-S2`: create one logs-oriented child candidate for the `unified indices / logs-facing front matter / log identity` body, expected as one first `DOC-WORKFLOW-LOGS`-family release candidate
- `P3-C1-S3`: create one lifecycle-oriented child candidate for `legacy taxonomy / freeze / migrate-on-demand / stub / lifecycle cutover` semantics, expected as one first `DOC-WORKFLOW-LIFECYCLE`-family release candidate

### P4 (Selective ledger backfill)

- `P4-C1-S1`: identify earlier `S0A` and `S0B` packets whose routing ambiguity is now materially visible because contracts were emitted before a ledger existed
- `P4-C1-S2`: backfill ledgers only for those earlier mixed-source packets whose missing routing record now blocks later child extraction, parent synthesis, or overlap repair
- `P4-C1-S3`: keep single-family, low-ambiguity packets out of compulsory backfill so ledger growth stays justified rather than mechanical

### P5 (Normalization and reuse)

- `P5-C1-S1`: validate `status` versus `release_action` versus `lineage` across the emitted packet
- `P5-C1-S2`: validate `source_refs` versus `cumulative_source_refs` so carry-forward stays explicit
- `P5-C1-S3`: record future `parent promotion / wider family synthesis` notes explicitly whenever one child extraction is known to be narrower than the eventual generalized rule

## Current Status

- `S0F-7C` is now opened as the first application lane after `7B`.
- The lane now fixes `S0B-3A` as the first bounded decomposition target.
- The lane now also fixes one stronger application reading: extract narrow child bodies first, synthesize broader parent shape later, and backfill ledgers selectively when later overlap proves the missing routing record matters.
- `P1-C1` is now complete in workspace: the source packet now fixes `S0B-3A` as the primary source body, issue `44` as sharpening support, and `S0B-2A` plus earlier docs-management context as bounded upstream background.
- `P2-C1` is now complete in workspace: the first extraction targets are fixed as `DOC-WORKFLOW-LOGS-0001` and `DOC-WORKFLOW-LIFECYCLE-0001`, front matter is fixed as child-first extraction with later widening allowed, and cutover is split into two same-source slices before any later multi-consumption model is considered.
- `P3-C1-S1` is now complete in workspace: the first `S0B-3A` ledger draft now exists and routes the source into `LOGS` and `LIFECYCLE`, with cutover already split into same-source sub-slices.
- `P3-C1-S2S3` are now complete in workspace: the first `DOC-WORKFLOW-LOGS-0001` and `DOC-WORKFLOW-LIFECYCLE-0001` child candidates now exist as reviewed drafts aligned to the completed `S0B-3A` ledger.
- The next execution step is commit/push for the reviewed `LOGS` and `LIFECYCLE` child candidates, then `P4` selective ledger backfill where earlier mixed packets now have routing ambiguity that blocks later reuse.

## Evidence (reserved)

### P0-C1-S1S2 (Application lane scaffolded and first target fixed | 2026-04-10)

- headSha: `6268e6874`
- artifacts:
  - `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should gain one new application lane that treats `7A + 7B` as the active migration standard
  - the first decomposition target should be fixed as `S0B-3A`, with the source type stated correctly as local log plus linked issue support
  - the lane should be ready to carry not only source decomposition but also later parent synthesis and selective ledger backfill decisions
- observed:
  - the repo now has one new `7C` scaffold for repeated old-log decomposition work
  - `S0B-3A` is now fixed as the first active target under a `log-first with issue support` reading
  - the lane now explicitly reserves child-first extraction, later parent synthesis, and selective ledger backfill as part of the same application workflow

### P1-C1-S1S2S3 (Bounded `S0B-3A` source packet reconstructed | 2026-04-10)

- headSha: `6268e6874`
- artifacts:
  - `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  - `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
  - `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
- expected:
  - the lane should identify one bounded source packet for `S0B-3A` without letting every upstream ancestor silently become direct release input
  - the packet should distinguish the local log from the immediate issue support and from broader upstream rationale
- observed:
  - the local `S0B-3A` log is now fixed as the primary source body for the first decomposition pass
  - issue `44` is now fixed as direct sharpening support rather than replacement ownership
  - `S0B-2A` and earlier docs-management context are now treated as bounded background that may sharpen later extraction without automatically widening the first child releases

### P2-C1-S1S2S3 (First `S0B-3A` extraction rules fixed | 2026-04-10)

- headSha: `302e587f9`
- artifacts:
  - `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the first `S0B-3A` extraction pass should fix the child-family targets before any ledger or contract bodies are emitted
  - front matter should stay narrow enough for the first extraction while preserving a later widening path
  - cutover should be split into narrower same-source slices before the lane resorts to one explicit multi-consumption model
- observed:
  - the first child extraction targets are now fixed as `DOC-WORKFLOW-LOGS-0001` and `DOC-WORKFLOW-LIFECYCLE-0001`
  - front matter is now fixed as child-first extraction in the logs-oriented child with later parent or broader-family widening explicitly reserved
  - cutover is now split into one logs-intake slice and one lifecycle-boundary slice, both still tied back to the same `S0B-3A` source packet

### P3-C1-S1 (First `S0B-3A` routing ledger drafted | 2026-04-10)

- headSha: `672ac2d16`
- artifacts:
  - `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`
  - `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
- expected:
  - the first concrete `S0B-3A` output should be one source-owned ledger that preserves the fixed `LOGS/LIFECYCLE` split before any child contract body is drafted
  - the ledger should separate the two cutover meanings into same-source sub-slices rather than leave one ambiguous dual-use row
- observed:
  - the first `S0B-3A` ledger draft now exists under source-owned naming and routes the source into the two approved child-family candidates
  - cutover is now represented as two same-source rows in the ledger, one for logs intake and one for lifecycle boundary ownership

### P3-C1-S2S3 (First `LOGS` and `LIFECYCLE` child candidates drafted | 2026-04-10)

- headSha: `<workspace not committed yet for S0F-7C/P3-C1-S2S3>`
- artifacts:
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  - `docs/governance/contracts/workflow/lifecycle/DOC-WORKFLOW-LIFECYCLE-0001-legacy-taxonomy-cutover-and-stub-preservation.md`
  - `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`
- expected:
  - the first child contract drafts should match the fixed ledger split without silently recombining `LOGS` and `LIFECYCLE`
  - `LOGS-0001` should stay narrow around log identity, log-facing front matter, and logs-intake cutover
  - `LIFECYCLE-0001` should stay narrow around legacy taxonomy, lifecycle cutover, migration-on-demand, and stub preservation
- observed:
  - `DOC-WORKFLOW-LOGS-0001` now exists as one first draft child release for log identity, logs-facing front matter, and logs-intake cutover
  - `DOC-WORKFLOW-LIFECYCLE-0001` now exists as one first draft child release for legacy taxonomy, lifecycle cutover, and stub preservation without collapsing those rules back into the logs child