# road-template-branch-roadmap (Branch roadmap template | v1)

---

**id**: `road-template-branch-roadmap`
**kind**: `roadmap`
**title**: `branch roadmap template: focused detour + parent contribution rules v1`
**status**: `draft`
**scope**: `cross-scope`
**tags**: `ROADMAP, template, branch-road, planning, bridge-ledger`
**links**: ``
  **source**: `docs/roadmap/legacy/ROADMAP v5.md`
  **parent_road**: `docs/roadmap/road-<parent>.md`
  **reference_log_1**: `docs/logs/_template-log-parent-epic-spine.md`
  **reference_log_2**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_3**: `docs/roadmap/road-template-main-roadmap.md`
**created**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown`
**updated**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown`
**reviewed**: `YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for roadmap frontmatter.
- Prefer canonical UTC-second timestamps such as `2026-04-13T08:15:30Z` when exact repo-side lifecycle audit matters.
- Legacy day-only values may remain when branch-road maintenance does not yet require second-level precision.
- `reviewed` should be used only when a branch roadmap enters bounded review rather than ordinary iterative editing.

## Positioning

**Context / role targeting**

- Use this template when a focused detour is needed inside a larger mainline, but the extra detail should not flood the mainline body.
- A branch roadmap is not a separate strategic backbone; it is a concentrated problem-solving track that still contributes back to the parent roadmap.

**One-sentence goal**

- `<Solve a focused sub-problem and record exactly how its child logs contribute back to the parent mainline>`

## Parent / Branch Rules

- A branch roadmap must declare its `parent_road`.
- Branch-road completion still counts toward the parent when the parent milestone-phase alignment is explicit.
- The branch ledger remains child-log-first: list child logs, not prose paragraphs, as the canonical rows.
- The branch roadmap may contain concentrated narrative and constraints that the parent should not absorb verbatim.
- If a branch slot is still unmapped, say `unmapped` explicitly instead of leaving the parent contribution implicit.

## Scope & Audience

- **Primary audience**: <focused role / problem / interview / transition path>
- **Relation to parent road**: <which parent milestones this branch concentrates>
- **Time horizon**: <short focused window, e.g. 4-8 weeks>

## Roadmap / Log Bridge Contract

- The branch roadmap owns focused selection, concentration, and parent-alignment rules.
- Child logs still own the implementation and evidence.
- Both the branch and the parent should record the same child-log mapping when the branch output counts toward the mainline.

## Parent Contribution Ledger

- Record which parent roadmap slots this branch helps satisfy.
- Preferred format:
  - `parent M2-P1 <- docs/logs/log-<...>.md`
  - `parent M4-P0 <- docs/logs/log-<...>.md`

## Milestone overview

- List only the milestones this branch actively concentrates.

## Milestones

### Mx: <Milestone title>

**Goal**

- <What this branch milestone means>

**Bridge Ledger (child logs only)**

- `Mx-P0`:
  - `docs/logs/log-<...>.md`
- `Mx-P1`:
  - `docs/logs/log-<...>.md`
- `Mx-P2`:
  - `docs/logs/log-<...>.md`
- `Mx-P3`:
  - `docs/logs/log-<...>.md`

**Parent alignment**

- `parent Mx-P0 <- docs/logs/log-<...>.md`
- `parent Mx-P1 <- docs/logs/log-<...>.md`

**Plan (P0-P3)**

- `P0` Contract: ...
- `P1` Implementation: ...
- `P2` Drill: ...
- `P3` Drill: ...

Repeat for each focused milestone this branch handles.

## Evidence Pointers (cross-log)

- <Supporting pointers only; the canonical rows should stay inside each milestone's Bridge Ledger and Parent alignment blocks>

## Recent Changes (optional)

- YYYY-MM-DD: <What changed and why>