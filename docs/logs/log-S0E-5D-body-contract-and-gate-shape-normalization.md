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

## Carry-Forward Questions For P1/P2

- `P1` still needs one canonical low-cardinality Evidence Footer line shape and one canonical extraction source from the log.
- `P2` still needs the hard-gate body-shape check list derived from this canonical spec.

## Suggested Direction For Evidence Footer Source (not fixed yet)

- The cleanest next-step design is to extract Evidence Footer from one explicit log-owned source instead of inferring it from mixed evidence sections or commit subjects.
- A practical direction is:
  - keep one dedicated machine-facing subsection in the log, such as a reserved `Evidence Footer Source` block under `PR Summary Inputs` or under `Evidence`;
  - make every source line already match the one canonical footer shape;
  - let PR create and PR rewrite consume only that source block;
  - if the source block is absent and the log is not drills/evidence class, omit the entire footer section.
- This keeps cardinality low because the renderer no longer chooses between phase-heading-style and commit-style; it always consumes one source shape and either renders it or omits the footer entirely.

## Plan (draft)

- `P1-C1-S1`: fix Evidence Footer presence/omission/fallback contract
- `P2-C1-S1`: fix hard-gate body-shape checks beyond simple section presence
- `P3-C1-S1`: decide repair order across generators, rewriters, and gate checks

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: canonical issue-creation / issue-conclusion / PR body families drafted
- [ ] `P1-C1-S1`: Evidence Footer contract fixed
- [ ] `P2-C1-S1`: hard-gate body-shape check scope fixed
- [ ] `P3-C1-S1`: repair order fixed

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

## Recent changes (for traceability, optional)

- 2026-03-31: created `S0E-5D` as a dedicated follow-up for body contract normalization, Evidence Footer unification, and hard-gate shape checks after live object drift was confirmed across representative issues and PRs.
- 2026-03-31: completed `P0` by converting operator-supplied formatting rules into one canonical body spec for issue creation, issue conclusion, and PR body shape, and by pre-locking Evidence Footer to drills/evidence-only with no commit-footer fallback.