# log-S0E-5D (Phase 5D: Body Contract and Gate Shape Normalization)

---

**id**: `S0E-5D`
**kind**: `log`
**title**: `body contract and gate shape normalization v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Issues, PR, Automation, Contract, Formatting, Evidence, epic/s0, sub/0e5d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_5**: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
  **reference_log_6**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-31`
**updated**: `2026-03-31`

---

## Decision / Outcome

**Decision**:

- `S0E-5D` exists to fix a problem that is now clearly separate from guarded `PR create`: the system still lacks one explicit body contract that keeps issue creation, issue conclusion, PR body rendering, Evidence Footer shape, and hard-gate formatting checks aligned.
- The immediate goal of this slice is not to change GitHub Actions policy or widen mutation automation. It is to define one canonical rendering contract and one canonical gate surface so formatting drift stops being treated as an acceptable side effect.
- This slice is intentionally separate from `S0E-5C` because `S0E-5C` is already occupied by guarded `PR create` stage decomposition. Mixing the two would blur whether a failure came from create orchestration or from body-shape contract drift.

**Default choices (phase defaults / v1)**:

- One object type should have one canonical body renderer at a time:
  - issue creation body;
  - issue conclusion body;
  - PR body.
- Evidence Footer should have one low-cardinality shape contract, not one style for commit-derived footer lines and another style for phase-heading-derived footer lines.
- Hard gate should evolve from a section-presence gate to a body-shape gate that also checks section order, blank-line discipline, footer shape, and allowed link-line types.
- GitHub Actions discussion stays deferred until this contract is fixed; otherwise Actions would only amplify drift that is already present.

## Constraints

- Do not silently normalize live GitHub history in this slice; first fix the contract, then decide which historical bodies deserve reconciliation.
- Do not keep two equally valid Evidence Footer styles in v1.
- Do not let formatter choices stay implicit inside multiple scripts once the canonical contract is fixed.

## Scope

- `P0`: define one canonical body contract for issue creation, issue conclusion, and PR body
- `P1`: define one canonical Evidence Footer rule set with explicit presence/omission/fallback policy
- `P2`: define the hard-gate shape checks that must be enforced beyond mere section existence
- `P3`: decide whether to repair generators first, gate first, or both together after the contract is fixed
- `P4`: execute the selective historical rewrite batch under the fixed body contract

## Success Criteria (DoD)

- The repo has one explicit contract for:
  - issue creation body shape;
  - issue conclusion body shape;
  - PR body shape;
  - Evidence Footer semantics.
- The contract clearly says when Evidence Footer is required, when it may be omitted, and whether fallback to commit-derived lines is allowed.
- The contract clearly says what hard gate must inspect: section order, body shape, blank-line rules, footer style, and allowed link categories.
- The result is concrete enough that generator scripts can be refactored toward one source of truth instead of preserving multiple implicit templates.

## Current Status

- The current system has multiple implicit renderers instead of one explicit body contract:
  - issue creation body rendering in `gen_issue_draft.py`;
  - issue conclusion body rendering in `plan_issue_conclusion.py`;
  - PR preview/create rendering in `plan_pr_prep.py`;
  - PR rewrite partial rendering in `rewrite_pr_body_scope_from_log.py`.
- Live GitHub objects now show the drift clearly: `#299`, `#302`, `#306`, `#308`, and closed issue `#293` are not uniformly shaped even though they all belong to the same automation family.
- The current hard gate is still closer to a lifecycle structural gate than to a full body-shape gate; it catches missing sections and structural lifecycle defects, but it does not yet enforce canonical formatting shape.
- `S0E-5D` is the dedicated place to fix that contract before any further GitHub Actions rollout is considered.
- `P0` is now completed: one first-cut canonical body spec has been fixed for issue creation, issue conclusion, and PR body shape, including contiguous metadata rows, explicit section order, backtick rules, and the rule that Evidence Footer is drills/evidence-only with no commit-footer fallback.
- `P1` is now completed: Evidence Footer now has one fixed extraction source, one fixed rendered line shape, explicit omission semantics, and an explicit rule that both the stage token and artifact path must be wrapped in inline code.
- `P2` is now completed: hard gate now checks canonical section order, metadata blank-gap discipline, allowed link categories, issue conclusion Context retention, and PR-side Evidence Footer presence/shape against one explicit source block; both PR prep preview and PR rewrite now consume `Evidence Footer Source` only.
- `P3` is now completed: rewrite execution is fixed as a new `P4` under `S0E-5D`, while the later post-apply gate is explicitly deferred to `S0E-5C`; the minimal inspected rewrite set has been identified and the boundary between contract normalization and publish-time orchestration is now clearer.

## P0 (Canonical body families | v1)

### P0-C1-S1 (Canonical body families drafted from operator rules | v1)

- The canonical spec is now recorded in `docs/issues/body-contract-S0E-5D-p0-canonical-spec.md`.
- Issue Creation body is now fixed as:
  - `Metadata -> Context -> Definition of Done (DoD) -> Links`;
  - empty `Context` and empty `Definition of Done (DoD)` are both preserved at creation time.
- Issue Conclusion body is now fixed as:
  - `Metadata -> Context -> Definition of Done (DoD) -> Links`;
  - `Context` remains present and must contain substantive conclusion-stage content;
  - `Definition of Done (DoD)` contains short PR refs such as `#299` and `#300`;
  - `Links` does not add issue or PR lines in the conclusion contract.
- PR body is now fixed as:
  - `Metadata -> Summary -> Execution Checklist -> Links -> Evidence Footer (when applicable) -> Development Link (only when an issue exists)`.
- Metadata-like bullet rows across creation / conclusion / PR bodies must be contiguous with no blank paragraphs between adjacent bullets.
- Inline code is now fixed as:
  - metadata values use backticks by default;
  - GitHub short refs such as parent issue or development issue refs remain plain refs without backticks;
  - links path/url refs use backticks.
- Evidence Footer applicability is now pre-locked for the next step:
  - drills/evidence-only;
  - omitted entirely when not applicable;
  - no commit-footer fallback.

## P1 (Evidence Footer contract | v1)

### P1-C1-S1 (Evidence Footer source and rendered shape fixed | v1)

- The canonical Evidence Footer spec is now recorded in `docs/issues/evidence-footer-S0E-5D-p1-canonical-spec.md`.
- Evidence Footer now has one explicit log-owned extraction source:
  - block name: `Evidence Footer Source`;
  - location: under `PR Summary Inputs (optional)`.
- The canonical source line shape is now fixed as:
  - ``- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json```.
- The stage token and artifact path must both use inline code.
- The rendered PR `Evidence Footer` section must preserve the exact same line shape and source order.
- If the source block is absent, the entire `Evidence Footer` section must be omitted.
- Commit-footer fallback, phase-heading fallback, and mixed inferred footer styles are all forbidden.

## P2 (Hard gate body-shape checks | v1)

### P2-C1-S1 (Canonical hard-gate body-shape checks implemented | v1)

- The hard-gate shape spec is now recorded in `docs/issues/hard-gate-shape-S0E-5D-p2-canonical-spec.md`.
- Shared contract helpers now live in `scripts/issues/body_contract.py`.
- PR preview/create rendering in `plan_pr_prep.py` now:
  - reads `PR links` and `Evidence Footer Source` separately;
  - omits `Evidence Footer` when no source rows exist;
  - forbids commit-footer fallback.
- PR rewrite in `rewrite_pr_body_scope_from_log.py` now:
  - reads `Evidence Footer Source` only;
  - removes stale `Evidence Footer` when the source block is absent;
  - validates the rewritten body against the canonical PR contract before writing output.
- Create-time hard gate in `plan_pr_create_preflight_with_gate.py` now validates preview bodies against the canonical PR body contract.
- Lifecycle audit in `plan_lifecycle_audit.py` now additionally checks:
  - issue section order;
  - metadata bullet contiguity;
  - allowed issue-link categories;
  - closed-issue substantive `Context` retention.
- Issue conclusion rendering in `plan_issue_conclusion.py` is now aligned to the canonical contract by:
  - always keeping the `Context` section;
  - using a canonical conclusion line when create-time `Context` remained blank;
  - omitting issue/PR rows from issue `Links`.
- Standalone PR body contract checks are now available through `scripts/issues/check_pr_body_contract.py`.

## P3 (Repair order and post-apply audit chain | v1)

### P3-C1-S1 (Repair order and post-apply audit chain fixed | v1)

- The rollout and post-audit decision is now recorded in `docs/issues/rollout-and-post-audit-S0E-5D-p3-decision.md`.
- The chosen rollout order is now fixed as:
  - `gate-first` to stop new drift;
  - `selective historical rewrite` to repair only the minimal representative backlog under `S0E-5D/P4`.
- Historical rewrite is now explicitly attached to a new `P4`, not to another `C` inside `P3`.
- The later post-apply live-verify chain is now explicitly deferred to `S0E-5C`, where live publish and post-publish ownership already belong.
- The minimal inspected issue rewrite set is now fixed as:
  - `#293`, `#295`, `#297`, `#300`, `#303`, `#305`, `#307`.
- The minimal representative PR rewrite set is now fixed as:
  - `#299`, `#302`, `#306`, `#308`.
- A new post-apply PR verifier now exists in `scripts/issues/verify_live_pr_body_contract.py`.
- `body_contract.py` now also rejects `Evidence Footer` when the source log is not drills/evidence eligible.
- `S0E-5D` keeps ownership only of pre-apply contract enforcement and historical normalization; GitHub Actions post-apply ownership is deferred.

## P2-Locked Inputs For P3

- The repo now has one machine-checkable PR body contract gate that can emit pass/fail results on local fixtures before live GitHub mutation.
- The repo now has one canonical source-log path for Evidence Footer lines and one canonical rendered row shape.

## P3-Locked Outputs

- The next remaining work is no longer contract definition.
- The next work inside `S0E-5D` is operational rewrite rollout:
  - representative historical PR rewrites;
  - representative historical issue rewrites.
- The later post-apply verification chain and GitHub Actions wiring are now intentionally deferred to `S0E-5C`.

## Plan (draft)

- `P4-C1-S1`: execute the first representative historical PR rewrite batch under the fixed contract
- `P4-C1-S2`: execute the first representative historical closed-issue rewrite batch under the fixed contract

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: canonical issue-creation / issue-conclusion / PR body families drafted
- [x] `P1-C1-S1`: Evidence Footer contract fixed
- [x] `P2-C1-S1`: hard-gate body-shape check scope fixed
- [x] `P3-C1-S1`: repair order fixed
- [ ] `P4-C1-S1`: representative historical PR rewrite batch executed
- [ ] `P4-C1-S2`: representative historical closed-issue rewrite batch executed

## Evidence (reserved)

- This slice will compare current script renderers and representative live GitHub objects until the canonical body contract is fixed.

### P0-C1-S1 (canonical body families drafted from operator rules | 2026-03-31)

- artifacts:
  - `docs/issues/body-contract-S0E-5D-p0-canonical-spec.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
- expected:
  - one explicit canonical spec should fix issue creation, issue conclusion, and PR body section order and row-shape rules
  - metadata-like bullets should forbid blank paragraphs between adjacent rows
  - Evidence Footer applicability should be constrained before formatter/gate implementation work continues
- observed:
  - the canonical spec now fixes contiguous metadata rows, creation/conclusion/PR body section order, inline-code rules, and the operator rule that Evidence Footer is drills/evidence-only with no commit-footer fallback
  - one carry-forward source-extraction direction is now documented for the next step so the footer can move toward one low-cardinality source instead of mixed inference rules

### P1-C1-S1 (canonical evidence footer source and line shape fixed | 2026-03-31)

- artifacts:
  - `docs/issues/evidence-footer-S0E-5D-p1-canonical-spec.md`
  - `docs/issues/body-contract-S0E-5D-p0-canonical-spec.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
- expected:
  - one explicit source block should become the only allowed Evidence Footer input for PR create and PR rewrite
  - one exact line shape should remove ambiguity between stage token formatting and artifact-path formatting
  - omitted footer and rendered footer should both become mechanically checkable by a later hard gate
- observed:
  - the contract now fixes `Evidence Footer Source` under `PR Summary Inputs (optional)` as the only extraction source
  - the contract now fixes one exact line shape where both the stage token and artifact path are inline-code wrapped
  - omission semantics are now explicit when the source block is absent, and all fallback styles are forbidden

### P2-C1-S1 (hard-gate body-shape checks implemented and sampled | 2026-03-31)

- artifacts:
  - `docs/issues/hard-gate-shape-S0E-5D-p2-canonical-spec.md`
  - `scripts/issues/body_contract.py`
  - `scripts/issues/check_pr_body_contract.py`
  - `scripts/issues/plan_pr_prep.py`
  - `scripts/issues/rewrite_pr_body_scope_from_log.py`
  - `scripts/issues/plan_pr_create_preflight_with_gate.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/issues/pr-prep-S0E-5D-p2-pass-manifest.json`
  - `docs/issues/pr-prep-S0E-5D-p2-render-plan.json`
  - `docs/issues/pr-body-contract-S0E-5D-p2-pass-body.md`
  - `docs/issues/pr-body-contract-S0E-5D-p2-pass-check.json`
  - `docs/issues/pr-body-contract-S0E-5D-p2-stop-unquoted-footer-body.md`
  - `docs/issues/pr-body-contract-S0E-5D-p2-stop-unquoted-footer-check.json`
  - `docs/issues/pr-body-contract-S0E-5D-p2-stop-wrong-source-log.md`
  - `docs/issues/pr-body-contract-S0E-5D-p2-stop-wrong-source-check.json`
  - `docs/issues/pr-body-contract-S0E-5D-p2-rewrite-body.md`
  - `docs/issues/pr-body-contract-S0E-5D-p2-rewrite-check.json`
- expected:
  - hard gate should reject PR bodies with malformed footer rows or footer sections sourced from the wrong block
  - PR prep preview and PR rewrite should stop inferring footer rows from commit or `Evidence` sections
  - issue-side audit should move from section presence to canonical section order and link-category checks
- observed:
  - PR prep preview now renders from `Evidence Footer Source` only and produced a pass sample on `S0E-5B`
  - standalone contract checks now pass on canonical preview/rewrite bodies and fail on both unquoted footer rows and wrong-source-block fixtures
  - lifecycle audit and issue conclusion rendering are now aligned with the newer issue body contract instead of the older transient-context rule

### P3-C1-S1 (rollout order and post-apply audit chain fixed | 2026-03-31)

- artifacts:
  - `docs/issues/rollout-and-post-audit-S0E-5D-p3-decision.md`
  - `docs/issues/pr-live-contract-check-308-result.json`
  - `docs/issues/pr-live-contract-check-302-result.json`
  - `scripts/issues/verify_live_pr_body_contract.py`
  - `scripts/issues/body_contract.py`
- expected:
  - rollout order should stop new drift first instead of starting with a broad historical rewrite
  - historical rewrite execution should become a new phase step rather than being buried inside another `C`
  - post-apply verification should remain available as a later chain without forcing `S0E-5D` to own live-publish orchestration
- observed:
  - representative live PR `#308` fails the post-apply verifier on metadata blank-gap drift and old footer rows
  - representative live PR `#302` fails the post-apply verifier on invalid `Links` prose rows, ineligible footer presence, and non-canonical footer rows
  - the resulting ownership split is now fixed as `S0E-5D/P4 = historical rewrite execution` and `S0E-5C future phase = post-apply live verify / Actions wiring`

## Recent changes (for traceability, optional)

- 2026-03-31: created `S0E-5D` as a dedicated follow-up for body contract normalization, Evidence Footer unification, and hard-gate shape checks after live object drift was confirmed across representative issues and PRs.
- 2026-03-31: completed `P0` by converting operator-supplied formatting rules into one canonical body spec for issue creation, issue conclusion, and PR body shape, and by pre-locking Evidence Footer to drills/evidence-only with no commit-footer fallback.
- 2026-03-31: completed `P1` by fixing one explicit `Evidence Footer Source` block, one exact footer line shape, and the rule that both the stage token and artifact path must use inline code while all fallback footer styles remain forbidden.
- 2026-03-31: completed `P2` by wiring one shared body-contract gate into PR preview/rewrite paths, aligning issue-side audit/rendering to the new contract, and recording pass/stop samples for canonical footer rows, unquoted footer rows, and wrong-source-block failure cases.
- 2026-03-31: completed `P3` by fixing the rewrite rollout order, attaching historical rewrite execution to new `P4`, deferring post-apply gate ownership to `S0E-5C`, and identifying the minimal inspected historical rewrite set.