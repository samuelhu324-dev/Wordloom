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

## Canonical Questions To Fix

- Issue Creation body:
  - exact section set and order;
  - whether empty `Context` / `Definition of Done (DoD)` should still render at creation time;
  - how `Metadata` lines must be formatted.
- Issue Conclusion body:
  - whether `Context` must disappear entirely or may remain as an empty section;
  - exact DoD line format for merged PR refs;
  - exact `Links` line set allowed after closure.
- PR body:
  - exact section set and order;
  - whether `Metadata` bullets may contain blank lines between items;
  - whether rewrite paths must fully re-render or may only patch selected sections.
- Evidence Footer:
  - when it is mandatory;
  - when it may be omitted;
  - whether non-drill logs may fallback to commit-derived footer lines;
  - whether the canonical line style is phase-heading-style or commit-style;
  - how to keep the output low-cardinality so humans and machines do not infer accidental semantic differences.
- Hard gate shape checks:
  - section presence;
  - section order;
  - blank-line discipline;
  - allowed footer style;
  - allowed link categories and line shape.

## Operator Input Needed

- You do **not** need to hand-write a full final template before work can begin, but the contract does need decisions on a small set of style levers.
- The highest-value operator decisions are:
  - whether inline code markers such as backticks are mandatory, optional, or forbidden for each body family;
  - whether empty sections should render explicitly or disappear until substantive content exists;
  - whether Evidence Footer should be mandatory only for drill/evidence-carrying logs or for every PR body;
  - if Evidence Footer fallback is allowed, whether fallback lines should keep the same canonical shape as primary footer lines instead of switching style.
- If you want, you can provide these as rule bullets rather than full markdown mockups.

## Proposed First Cut (for review, not fixed yet)

- Issue Creation canonical body:
  - `Metadata -> Context -> Definition of Done (DoD) -> Links`
  - empty `Context` and `Definition of Done (DoD)` may remain visible at creation time if that is the chosen contract.
- Issue Conclusion canonical body:
  - `Metadata -> Definition of Done (DoD) -> Links`
  - no `Context` section once concluded.
- PR canonical body:
  - `Metadata -> Summary -> Execution Checklist -> Links -> Evidence Footer -> Development Link`
  - no blank lines between `Metadata` bullet items.
- Evidence Footer canonical direction:
  - one canonical line shape only;
  - fallback, if allowed, must still render in that same shape rather than inventing a second style.

## Plan (draft)

- `P0-C1-S1`: inventory current renderers and draft the three canonical body families
- `P1-C1-S1`: fix Evidence Footer presence/omission/fallback contract
- `P2-C1-S1`: fix hard-gate body-shape checks beyond simple section presence
- `P3-C1-S1`: decide repair order across generators, rewriters, and gate checks

## Execution Checklist (unchecked)

- [ ] `P0-C1-S1`: canonical issue-creation / issue-conclusion / PR body families drafted
- [ ] `P1-C1-S1`: Evidence Footer contract fixed
- [ ] `P2-C1-S1`: hard-gate body-shape check scope fixed
- [ ] `P3-C1-S1`: repair order fixed

## Evidence (reserved)

- This slice will compare current script renderers and representative live GitHub objects until the canonical body contract is fixed.

## Recent changes (for traceability, optional)

- 2026-03-31: created `S0E-5D` as a dedicated follow-up for body contract normalization, Evidence Footer unification, and hard-gate shape checks after live object drift was confirmed across representative issues and PRs.