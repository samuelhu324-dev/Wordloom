# road-00x-<summary> (Structured roadmap | v1)

---

**id**: `road-00x-<summary>`
**kind**: `roadmap`          # roadmap | note
**title**: `<One-line title: scope + audience + v1>`
**status**: `draft`          # draft | stable | archived
**scope**: `<Sx or cross-scope>`
**tags**: `ROADMAP, systems/platform, planning, v5-adapted`
**links**: ``
  **source**: `docs/roadmap/legacy/ROADMAP v5.md`
  **parent_log**: ``
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `YYYY-MM-DD`
**updated**: `YYYY-MM-DD`

---

## Positioning

**Context / role targeting**

- <One paragraph: what role this roadmap is optimised for>

**One-sentence goal**

- `<Systems/platform reliability + automation + operational support + documented runtime>`

## Scope & Audience

- **Primary audience**: <e.g. systems/platform operations roles>
- **Time horizon**: <e.g. 3–6 months>
- **Code base**: `wordloom-v3`

## Milestone overview (M1–M5)

- **M1. Systems / platform operations language**
- **M2. IaC / scripting / automation**
- **M3. Runtime packaging & deploy / verify / rollback**
- **M4. Backup / recovery / operational support narrative**
- **M5. Cloud fundamentals with hybrid awareness**

## Milestones (M1–M5)

For each milestone, keep结构和 phase-log 类似：有 Contract（P0）、Implementation（P1）、Drills/Verification（P2–P3）。

### M1: Systems administration / operational support language

**Goal**

- <Be able to describe wordloom-v3 in systems/platform operations language: installation, configuration, maintenance, monitoring, backup/recovery, operational support, lifecycle management>

**Plan (P0–P3)**

- `P0` Contract: define minimal vocabulary, example phrases, and mapping to existing assets.
- `P1` Implementation: notes, cheat-sheets, and 1–2 small samples wired to real logs/runbooks.
- `P2` Drill: dry-run 1–2 interview-style explanations using this language.
- `P3` Drill: refine based on feedback; record stable examples.

**Execution Checklist**

- [ ] `M1-P0`: vocabulary + mapping note drafted.
- [ ] `M1-P1`: 1–2 concrete samples (e.g. S4A/S5A stories) written.
- [ ] `M1-P2`: at least one mock interview answer rehearsed/recorded.
- [ ] `M1-P3`: examples stabilised and linked from logs/runbooks.

### M2: Bash + automation scripts (runtime operations)

**Goal**

- <Have a small but real set of Bash scripts covering start/stop/health/backup/logs that match ROADMAP v5 priorities>

**Plan (P0–P3)**

- `P0` Contract: decide script naming, locations, and evidence style.
- `P1` Implementation: add/align scripts under `scripts/` and `scripts/ops/`.
- `P2` Drill: run from-zero-to-dev/test path and record FAIL→PASS evidence.
- `P3` Drill: operator-facing runbook + interview wording.

**Execution Checklist**

- [ ] `M2-P0`: contract written and linked to S4B-1A/S4A logs.
- [ ] `M2-P1`: scripts aligned and minimally cleaned.
- [ ] `M2-P2`: from-zero drill executed with evidence JSON/text.
- [ ] `M2-P3`: runbook and interview story in place.

### M3: Terraform / IaC minimal sample

**Goal**

- <Deliver a minimal, runnable Terraform/IaC sample that defines dev/test infrastructure in a repeatable way>

**Plan (P0–P3)**

- `P0` Contract: scope (dev/test only), resources, and evidence contract.
- `P1` Implementation: Terraform skeleton modules under `infra/terraform/*`.
- `P2` Drill: `terraform init/validate/plan` drills with evidence.
- `P3` Drill: operator-facing wording and interview narrative.

**Execution Checklist**

- [ ] `M3-P0`: contract recorded (e.g. S4B-2A log).
- [ ] `M3-P1`: at least one module implemented (e.g. devtest DB).
- [ ] `M3-P2`: drills executed with headSha + artifact paths.
- [ ] `M3-P3`: narrative wired into logs/runbooks/interview notes.

### M4: Docker + deployable runtime & post-change verification

**Goal**

- <Show a deployable, documented runtime with post-change verification and rollback awareness>

**Plan (P0–P3)**

- `P0` Contract: define what “deployable runtime” means for dev/test.
- `P1` Implementation: Dockerfile/compose/env/health wiring.
- `P2` Drill: deploy + smoke-verify drill with evidence.
- `P3` Drill: rollback/fallback narrative and operator wording.

**Execution Checklist**

- [ ] `M4-P0`: contract exists and references S4A/S4B logs.
- [ ] `M4-P1`: runtime packaging aligned and documented.
- [ ] `M4-P2`: deploy+verify drill with artifacts.
- [ ] `M4-P3`: rollback/fallback story captured.

### M5: Backup / recovery + hybrid/cloud fundamentals framing

**Goal**

- <Stabilise backup/recovery narrative and add a thin layer of cloud/hybrid awareness>

**Plan (P0–P3)**

- `P0` Contract: define minimal cloud/hybrid scope and terms.
- `P1` Implementation: notes and mapping from existing S5A-3B assets.
- `P2` Drill: backup/restore drill + one cloud/hybrid interpretation.
- `P3` Drill: interview story that connects on-prem/devtest with cloud basics.

**Execution Checklist**

- [ ] `M5-P0`: contract written.
- [ ] `M5-P1`: mapping note and examples.
- [ ] `M5-P2`: drill evidence (S5A-3B + cloud framing).
- [ ] `M5-P3`: stable interview paragraph recorded.

## Evidence Pointers (cross-log)

- <Link to S4A/S4B/S5A logs, drills, and artifacts that back each milestone>

## Recent Changes (optional)

- YYYY-MM-DD: <What changed and why>
