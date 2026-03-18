# log-<ID> (Phase <n>: <Slice Title>)

---

**id**: `<ID>`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `<One-line title: deliverable + drills/evidence + v1>`
**status**: `draft`           # draft | stable | archived
**scope**: `<Sx>`
**tags**: `EVOLUTION, <domain>, Drills, Evidence, epic/<sx>, sub/<phase>`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-<PARENT>.md`
  **previous_log**: ``
  **reference_log_1**: ``
**created**: `YYYY-MM-DD`
**updated**: `YYYY-MM-DD`

---

## Decision / Outcome

**Decision**:

- <What this phase delivers>
- <Default behavior / default semantics>

**Default choices (phase defaults / v1)** (optional, but recommended):

- <For example: dev/test first; avoid production-grade complexity; do not commit generated artifacts; required evidence JSON fields>

## Definitions (optional)

- <3-10 key terms so readers do not need to infer meaning>

## Constraints

- <For example: dumps are not committed to git; least privilege; low-cardinality reasons; machine-verifiable evidence>

## Scope

- `P0`: contract (default decisions, naming/fields, evidence contract)
- `P1`: <implementation / infra / scripts>
- `P2`: <drill / verify>
- `P3`: <drill / verify>
- (optional) `P4`: <single-command pipeline / hard gate>

## Success Criteria (DoD)

- <List 4-10 acceptance checks, ideally verifiable from evidence JSON / SQL / metrics>

## Stability (what stable means)

- This log can be marked `stable` when:
  - <The P0-Pn contract, entry scripts, and drills have all been exercised successfully>
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (<Contract item 1>)

- <Naming / fields / semantics / constraints>

### P0-C1-S2 (<Contract item 2>)

- <Naming / fields / semantics / constraints>

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - <Input parameters>
  - <Output artifact paths>
  - <PASS/FAIL decision fields>

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- For logs tied to a specific scope/index (for example, `S5B-3A` belongs to `S5B`, and `S0D-2A` belongs to `S0D`), prefer making P* code and documentation changes on a working branch with the same prefix:
  - For example, `S5B-3A` changes should usually land on an `S5B-*` branch such as `S5B-security-governance-hard-gates`.
  - `S0D-2A` style meta/docs/automation changes should usually land on an `S0D-*` branch such as `S0D-docs-management-v4`.
- If a single PR touches multiple scopes/indexes (for example both `S5B-3A` and `S0D-2A`), prefer splitting it into multiple PRs so each PR stays focused on one scope/index and its corresponding branch for easier aggregation and traceability.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch:
  - For example, `S5B-4A` changes should normally land on an `S5B-*` top-level branch such as `S5B-security-governance-hard-gates`.
  - If a phase is unusually large or involves multiple contributors, you may open a short-lived child branch under the `S5B-*` branch, but the default is still not to create a separate branch for every log.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (<Implementation>)

- P1-C1-S1: ...
- P1-C1-S2: ...

### P2 (<Drill / Verify>)

- P2-C1-S1: ...
- P2-C1-S2: ...

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: ...
- [ ] `P0-C1-S2`: ...
- [ ] `P0-C1-S3`: ...

### P1 (...)

- [ ] `P1-C1-S1`: ...
- [ ] `P1-C1-S2`: ...

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### <Pn-Cx-Sy> (<Drill name> | YYYY-MM-DD)

- headSha: `<git sha>`
- artifacts: `artifacts/_tmp_<...>/drills_<ts>.json`
- env (example, optional):
  - `<ENV>=<...>`
- expected:
  - ...
- observed:
  - ...

## Recent changes (for traceability, optional)

- YYYY-MM-DD: <What changed, why it is recorded, and how to trace it>
