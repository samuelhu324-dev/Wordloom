# road-template-main-roadmap (Mainline roadmap template | v1)

---

**id**: `road-template-main-roadmap`
**kind**: `roadmap`
**title**: `mainline roadmap template: long-running backbone + branch absorption rules v1`
**status**: `draft`
**scope**: `cross-scope`
**tags**: `ROADMAP, template, mainline, planning, bridge-ledger`
**links**: ``
  **source**: `docs/roadmap/legacy/ROADMAP v5.md`
  **reference_log_1**: `docs/logs/_template-log-parent-epic-spine.md`
  **reference_log_2**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_3**: `docs/roadmap/road-template-branch-roadmap.md`
**created**: `2026-03-29`
**updated**: `2026-03-29`

---

## Positioning

**Context / role targeting**

- Use this template for a long-running mainline roadmap such as `road-S1`.
- The mainline owns the backbone narrative, broad milestone language, and the stable list of direct/absorbed child-log outcomes.
- Branch roads may appear later to solve a focused problem without forcing the mainline body to absorb all branch-only narrative detail.

**One-sentence goal**

- `<Define the long-running backbone and absorb focused branch-road outputs without polluting the mainline narrative>`

## Mainline / Branch Rules

- A mainline roadmap owns the durable capability axis and milestone language.
- A branch roadmap may complete part of the mainline when a focused detour is needed.
- Mainline bridge ledgers must still point to child logs, not to branch-road files as the canonical implementation rows.
- When a child log is completed inside a branch roadmap but also counts toward the mainline, the mainline ledger should list that child log and mark it as `via <branch road>`.
- Branch roads are for containment, not for creating a second competing mainline.

## Scope & Audience

- **Primary audience**: <broad role family or long-term capability owner>
- **Time horizon**: <6 months to multiple years>
- **Code base**: `wordloom-v3`

## Roadmap / Log Bridge Contract

- The mainline roadmap owns `M* / M*-P*` capability language.
- Child logs own implementation, drill, and evidence detail.
- The canonical machine-readable bridge is `M*-P* -> child log`.
- A branch roadmap may add focus and concentrated narrative, but should not replace the mainline ledger.
- `Evidence Pointers` and `Recent Changes` remain supporting narrative only.

## Branch Road Register

- `child_road_1`: `docs/roadmap/road-<...>.md`
- `child_road_2`: `docs/roadmap/road-<...>.md`
- For each branch road, record:
  - why it exists;
  - which parent milestones it helps complete;
  - which child logs it concentrates.

## Milestone overview (M1-M5)

- **M1. <language / framing>**
- **M2. <runtime baseline / automation>**
- **M3. <IaC / infrastructure primitives>**
- **M4. <deploy / verify / rollback / release operations>**
- **M5. <recovery / governance / hybrid-cloud / second-layer capabilities>**

## Future capabilities & trigger conditions

- Keep future capability notes parallel to M1-M5 so the mainline can record what may appear next without forcing it into the active path too early.

## Milestones (M1-M5)

### M1: <Milestone title>

**Goal**

- <What this mainline milestone means>

**Bridge Ledger (child logs only)**

- `M1-P0`:
  - `docs/logs/log-<...>.md`
- `M1-P1`:
  - `docs/logs/log-<...>.md`
- `M1-P2`:
  - `docs/logs/log-<...>.md`
- `M1-P3`:
  - `docs/logs/log-<...>.md`

**Branch absorption notes (optional)**

- `<child log> via docs/roadmap/road-<branch>.md`

**Plan (P0-P3)**

- `P0` Contract: ...
- `P1` Implementation: ...
- `P2` Drill: ...
- `P3` Drill: ...

Repeat the same milestone structure for `M2` through `M5`.

## Evidence Pointers (cross-log)

- <Supporting pointers only; do not treat this section as the canonical bridge ledger>

## Recent Changes (optional)

- YYYY-MM-DD: <What changed and why>