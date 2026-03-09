# log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI（Phase 3：S2D hard gate entrypoint & CI wiring）

---

**id**: `S2D-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection onboarding hard gate entrypoint + CI (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S2D`
**tags**: `EVOLUTION, Projection, HardGate, Drills, Evidence, epic/s2d, sub/3`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S2D-projection-onboarding-hard-gates.md`
  **parent_log**: `docs/logs/log-S2D-projection-onboarding-hard-gates.md`
  **previous_log**: `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
  **reference_log_1**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_2**: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
**created**: `2026-03-09`
**updated**: `2026-03-09`

---

## Decision / Outcome（结论区）

**Decision**:

- Provide a first-class S2D hard gate entrypoint that runs projection onboarding suites (starting with the S2D-1A sample projection) and interprets their JSON artifacts as a CI-enforceable PASS/FAIL signal.
- Reuse the existing S2D-1A onboarding runner + labs as the first hard gate target, then generalize the pattern so additional projections can be plugged into the same CI workflow without bespoke scripts.

**Default choices（本 phase 默认决策 / v1）**:

- Scope v1 to dev/test only: the hard gate workflow talks only to the devtest Postgres instance and projection harness, never to production data or infra.
- Start with a single projection (`chronicle_daily_stats`) wired via S2D-1A; new projections will join once they have S2D-style labs/onboarding runners.
- Treat `artifacts/s2d-runs.json` and scenario-level `_result.json` as the single source of truth; the CI layer only interprets PASS/FAIL and key metadata, it does not re-implement business logic.
- Prefer additive wiring: keep existing S2C/S2B workflows stable, add new S2D hard gate jobs rather than retrofitting everything at once.

## Definitions（概念定义）

- **S2D hard gate entrypoint**: A script or workflow entry that runs one or more projection onboarding suites and exits with non-zero status when any required suite fails.
- **Onboarding suite**: A bundle of S2D labs and orchestration scripts for a given projection, such as the S2D-1A sample (`chronicle_daily_stats`) runner that appends to `artifacts/s2d-runs.json`.
- **Evidence JSON**: The combination of scenario-level `_result.json` files and aggregated `artifacts/s2d-runs.json` records, compatible with the S6A-4A contract and mechanically interpretable by CI.
- **Required vs optional suites**: A configuration layer that distinguishes which projections/suites are mandatory for a given repo/branch (hard gate) and which are best-effort or experimental.

## Constraints（约束）

- Do not break existing S2B/S2C stable workflows: new S2D jobs must be introduced in a way that can be guarded/opt-in (e.g. behind labels/branches) before being promoted to mandatory.
- Do not change the failure taxonomy of labs: CI should read `ok` and structured `reason` fields, not introduce new high-cardinality error categories.
- The hard gate must be mechanically evaluable: given a set of JSON artifacts, CI can determine PASS/FAIL without reading free-form logs.
- Workflow and script names should remain stable and explicit (e.g. `s2d_*` prefix), to be easily referenced from S0D/S6A automation logs.

## Scope（本 log 范围）

- `P0`: contract（define S2D hard gate entrypoint semantics, evidence contract, and naming conventions for scripts/workflows）
- `P1`: implementation（add/extend local hard gate runner(s) around the S2D-1A onboarding package, plus minimal configuration for multiple suites）
- `P2`: CI wiring（add a GitHub Actions workflow that runs the S2D hard gate entrypoint against devtest DB and fails PRs when required suites fail）
- `P3`: adoption & guardrails（make the S2D hard gate visible in docs/runbooks, tighten default protections, and provide escape hatches for legacy projections）

## Success Criteria（DoD）

- There is a clearly documented S2D hard gate contract: what scripts/workflows run, what JSON artifacts they must produce, and how CI interprets PASS/FAIL.
- At least one onboarding suite (S2D-1A sample projection) is wired into a single local hard gate runner that can be invoked both by humans and CI.
- A GitHub Actions workflow exists that runs the S2D hard gate entrypoint against a devtest DB and:
  - fails when S2D-1A onboarding runs with `ok=false`,
  - passes when the latest onboarding run is green.
- The workflow publishes or preserves artifacts (e.g. `_result.json` snapshots and `artifacts/s2d-runs.json`) for inspection.
- The Evidence section of this log contains at least one local dry run and one CI run (with headSha + run_id + run_dir or CI URL) showing both a red and a green case.

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0-P2 的 hard gate contract + 本地/CI 入口脚本 + 至少 1 条示范 onboarding suite（S2D-1A）已在 CI 中反复跑通；
  - Evidence 区记录了至少 1 次 red run 与 1 次 green run（含 headSha + artifacts 路径或 CI run URL），可作为后续扩展到多投影时的基线样板；
  - P3 的 adoption 规则（哪些 projection/suites 属于 hard gate 的 required 集）已经在 catalog 或配置中落地，并在文档中稳定描述。

## P0（Contract｜v1）

### P0-C1-S1（Hard gate entrypoint contract）

- 定义 S2D hard gate entrypoint 的最小语义：
  - 输入：环境（dev/test）、数据库 URL、需要执行的 onboarding suite 列表；
  - 行为：顺序或并行执行 suites，聚合 `ok` 状态与错误信息；
  - 输出：统一的 exit code（0 表示所有 required suites `ok=true`，非 0 表示至少 1 条 required suite 失败）。

### P0-C1-S2（Evidence contract for CI）

- 约定 CI 需要依赖的 evidence 字段：
  - `artifacts/s2d-runs.json` 中每条记录至少包含：`log_id/phase/cycle/step/head_sha/run_id/ok/scenarios[]`；
  - 每个 scenario 的 `_result.json` 至少包含：`ok`、关键 counters 和 `reason`/`failure` 字段；
  - hard gate entrypoint 在 CI 上运行时，必须能够从这些 JSON 中机械计算出整体 PASS/FAIL。

### P0-C1-S3（Workflow & naming contract）

- Workflow 与脚本命名：
  - GitHub Actions workflow 建议命名为 `s2d-hard-gate.yml` 或类似显式前缀；
  - 本地入口脚本统一使用 `scripts/s2d_*` 或 `scripts/projections/s2d_*` 前缀；
  - 所有新增文件需在 S2D spine 与 S0D/S6A 相关 runbook 中登记。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2D-3A/P<phase>-C<cycle>-S<steps>: <summary>`，例如：`S2D-3A/P0-C1-S1: scaffold S2D hard gate contract`。

**Branch 约定**:

- S2D-3A 相关改动优先落在 `S2D-*` 前缀的工作分支（例如 `S2D-projection-onboarding-hard-gates`），便于与 S2D-1A 的演进串联。
- 若一次 PR 同时涉及多个 scope/index（如 S2C 与 S2D），建议拆成多条 PR，每条 PR 聚焦一个 scope/index 与对应分支。

## Plan（draft）

### P1（Implementation：local hard gate runner）

- P1-C1-S1：提炼/包装 `scripts/projections/s2d_1a_p3c1s1_sample_onboarding.py`，形成可接受 suite 配置的本地 hard gate runner（例如 `scripts/s2d_hard_gate.py`）。
- P1-C1-S2：确保 runner 在 devtest DB 下可重复执行，并对 `artifacts/s2d-runs.json`/`_result.json` 的缺失或损坏做出合理错误处理。

### P2（CI wiring：GitHub Actions workflow）

- P2-C1-S1：新增 GitHub Actions workflow（例如 `.github/workflows/s2d-hard-gate.yml`），在 CI 中启动 devtest DB、运行 S2D hard gate runner，并根据 exit code 决定 job 成功与否。
- P2-C1-S2：为 workflow 增加必要的缓存/超时时间与 artifact 上传规则（如 `_snapshot/auto` 与 `artifacts/s2d-runs.json`）。

### P3（Adoption：catalog & guardrails）

- P3-C1-S1：在 docs/logs 与 runbook 中记录哪些 projection/onboarding suites 已纳入 S2D hard gate required 集，哪些仍处于 optional/experimental 状态。
- P3-C1-S2：为 legacy projection 设计合理的 skip/waiver 机制（例如基于标签或配置），并约定升级路径。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 hard gate entrypoint 语义与 exit code 约定
- [x] `P0-C1-S2`：定义 CI 所需 evidence JSON 字段
- [x] `P0-C1-S3`：定义 workflow/script 命名与登记约定

### P1（Implementation：local hard gate runner）

- [x] `P1-C1-S1`：抽象并实现本地 S2D hard gate runner（基于 S2D-1A onboarding）
- [x] `P1-C1-S2`：完善错误处理与重复运行语义

### P2（CI wiring：GitHub Actions）

- [x] `P2-C1-S1`：新增 S2D hard gate GitHub Actions workflow
- [x] `P2-C1-S2`：为 workflow 补充 artifact 上传与超时/重试策略

### P3（Adoption & guardrails）

- [ ] `P3-C1-S1`：在文档中记录 required/optional suites 与升级路径
- [ ] `P3-C1-S2`：实现并记录 skip/waiver 机制

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P1-C1-S1（local hard gate dry run｜YYYY-MM-DD）

- headSha：`2fd5d5e8bfb92c2ca92c12bcdc2d27ac0058badf`
- artifacts：
  - 汇总记录：`artifacts/s2d-runs.json`（追加记录，`log_id="S2D-1A"`，`run_id="20260309-194740"`，`ok=true`）
  - backfill smoke：`docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_backfill_smoke/20260309-194740`
  - harness drill：`docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_harness_drill/20260309-194740`
- env：
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test`
- 期望（expected）：
  - 本地 hard gate runner 通过调用 S2D-1A onboarding 套餐脚本产出一条新的 S2D run 记录；
  - 当该记录 `ok=true` 时，hard gate runner 以 `exit_code=0` 结束；当 `ok=false` 或记录缺失时，以非 0 结束。
- 观测（observed）：
  - 2026-03-09 在 devtest DB 下执行 `python scripts/s2d_hard_gate.py --database-url $DATABASE_URL`，runner 触发一次新的 onboarding run：`run_id=20260309-194740`，backfill/harness 两个 scenario 均 `ok=true`；
  - hard gate runner 从 `artifacts/s2d-runs.json` 中成功找到该记录，生成 S2D-3A summary JSON，整体 `overall_ok=true` 并以 `exit_code=0` 结束，完成首个 green dry run。

### P2-C1-S1（CI hard gate workflow run｜YYYY-MM-DD）

- headSha：`5ccf5bb96fd6669282ddc46079414b3e942d8c88`
- CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22852965555`
- artifacts：
  - 预期：`artifacts/s2d-runs.json` 中追加一条 `log_id="S2D-1A"` 的记录，并在 `_snapshot/auto` 下生成对应 backfill/harness 目录；
  - 实际：本次 run 结束时，Actions 报告 `No files were found with the provided path ... artifacts/s2d-runs.json`，说明 S2D onboarding 套餐在 CI 环境中尚未成功产出预期 artifacts。
- 期望（expected）：
  - `.github/workflows/s2d-hard-gate.yml` 在 CI 中启动 devtest DB、运行 `python scripts/s2d_hard_gate.py --database-url $DATABASE_URL`；
  - 当 S2D-1A onboarding suite `ok=false` 时，workflow 失败并标记 PR；当 `ok=true` 时，workflow 成功通过。
- 观测（observed）：
  - 2026-03-09，由 PR `#196 (S2D-projection-onboarding-hard-gates)` 触发的首轮 `s2d-hard-gate` workflow 运行（Run 1）以 `hard_gate` job `exit_code=2` 结束，整体状态为 Failure；
  - 上传 artifacts 步骤未找到任何匹配路径（包括 `_snapshot/auto/...` 和 `artifacts/s2d-runs.json`），这次 run 作为 S2D-3A 的首个 red CI 例子，后续需要在本地复现并修复，使下一轮 run 成为 green baseline。

## Recent changes（for traceability，可选）

- 2026-03-09：scaffold S2D-3A log，定义 S2D hard gate entrypoint & CI wiring 的 contract/plan，等待后续 P1/P2/P3 实现。
