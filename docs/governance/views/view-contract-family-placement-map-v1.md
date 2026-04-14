# Contract Family Placement Map v1

## Purpose

- This view answers the concrete placement question left open after `S0F-3I/P4`: where the seven contract families currently live in the repo, and which of those placements are deliberate versus merely unfinished.
- It exists so later cleanup slices do not treat `distributed SoT` as a documentation bug by default.

## Current Model

- Read each row in this order:
  - `family`: what kind of contract it is
  - `current primary directories or surfaces`: where a reader should look first for the strongest current SoT
  - `supporting surfaces`: where the same family currently exposes explanation, operator packaging, tests, workflows, or retained evidence
  - `concentration status`: whether the family is already concentrated enough, partially concentrated, or mixed by design
  - `cleanup reading`: whether a future slice should prefer better indexing or real relocation
- This is a current-state scan, not a rule that all future families must keep the exact same paths.

## Placement Map

| family | current primary directories or surfaces | supporting surfaces | concentration status | cleanup reading |
| --- | --- | --- | --- | --- |
| `DOC` | `docs/logs/`, `docs/governance/`, `docs/runbook/`, `docs/roadmap/` | `docs/governance/views/view-doc-current-front-door-v1.md` plus documentation-facing automation surfaces and templates that read or write these docs | `partially concentrated under docs/ by role` | `Do not build one extra universal DOC folder. Strengthen cross-links and front doors only when navigation gets noisy.` |
| `DOM` | `backend/api/app/modules/`, `backend/api/app/migrations/`, `backend/api/app/tests/` | slice logs under `docs/logs/` that explain bounded domain changes | `code-first and coherent, but not docs-concentrated` | `Only create a stronger family hub if cross-module business rules become hard to discover. Today, forcing DOM into docs/ would weaken SoT clarity.` |
| `PRO` | `backend/api/app/modules/search/`, `backend/api/app/modules/chronicle/`, `backend/scripts/search_outbox_*.py`, `backend/scripts/ops/` replay or rebuild surfaces | `docs/logs/`, `docs/runbook/`, `.github/workflows/`, `artifacts/` | `mixed by design` | `Prefer one family index or placement note before any physical move. Projection semantics currently live across code, worker runtime, drills, and evidence.` |
| `INT` | `backend/api/app/main.py`, `backend/api/app/shared/`, `backend/scripts/cli_app/` | `docs/logs/`, verification tests under `backend/api/app/tests/`, workflow and artifact surfaces where interface shape is checked | `mixed by design` | `Reorganize only if API, CLI, or artifact contracts start drifting into duplicate front doors. For now, interface meaning stays closest to entrypoint code plus checks.` |
| `OPS` | `docs/runbook/`, `backend/scripts/ops/`, `.github/workflows/`, top-level runtime surfaces such as `docker-compose*.yml` and `Procfile*` | `docs/governance/views/view-ops-current-front-door-v1.md`, `docs/logs/`, `infra/`, retained operational artifacts under `artifacts/` | `already concentrated enough across operator-owned surfaces` | `Needs clearer indexing more than relocation. Ops already has a readable home split among runbook, scripts, and workflow entrypoints.` |
| `SEC` | `backend/api/app/policy/`, security-focused tests under `backend/api/app/tests/`, hard-gate workflows under `.github/workflows/` | `docs/logs/`, `docs/runbook/`, retained gate artifacts under `artifacts/` | `mixed by design` | `Do not force a single folder yet. First let later auth, tenant, and policy slices mature under `SEC-IDN/TEN/AUT/AUD/DAT`; add a family front door only after the subfamilies stabilize.` |
| `EVD` | `artifacts/`, `.github/workflows/`, `docs/runbook/`, gate and drill entrypoints under `backend/scripts/cli_app/` and `backend/scripts/ops/` | `docs/logs/` and retained JSON or text bundles that explain or summarize evidence runs | `already concentrated enough around evidence execution` | `Needs retention discipline and indexing, not a universal relocation. EVD is valuable precisely because artifacts and gate code stay close together.` |

## Consolidation Threshold

- A later slice should prefer stronger indexing over physical relocation when:
  - one family already has a clear primary SoT and readers mostly struggle with navigation
  - the family is inherently mixed because enforcement lives in code, tests, workflows, and artifacts together
  - relocation would create a second weaker copy instead of clarifying ownership
- A later slice should consider a real family hub or directory reorganization only when:
  - readers repeatedly fail to find the authoritative surface for the same family
  - one family grows too many parallel front doors to scan cheaply
  - multiple files begin restating the same rule without one clear primary owner

## Registry Note

- The narrow `GC-*` governance registry remains concentrated under `docs/governance/contracts/` with current front-door reading at `docs/governance/INDEX.md`.
- Preserved legacy redirects such as `GC-ISS-*` and `GC-PRB-0001` remain on disk for lineage, but they do not mean the seven family taxonomy has failed or that every family should migrate into the governance registry.

## Reader Notes

- This view is descriptive, not prescriptive: it tells you where the repo currently keeps meaning, not where an imaginary perfect repository would place every file.
- The most fragmented-looking families are not automatically the most broken ones. `PRO`, `INT`, `SEC`, and `EVD` are mixed because their enforceable semantics already span code, workflows, tests, and retained artifacts.
- The family most likely to justify later concentration work is `DOM`, but only if you decide the business-rule reading path now needs a reader-facing front door beyond module code plus tests.
- If the question is about current versus legacy or support-only standing, use `docs/governance/views/view-disposition-role-in-family-transition-v1.md`; placement and disposition are related, but they are not the same question.

## Source Refs

- `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `docs/governance/views/view-contract-family-inventory-v1.md`
- `docs/governance/INDEX.md`