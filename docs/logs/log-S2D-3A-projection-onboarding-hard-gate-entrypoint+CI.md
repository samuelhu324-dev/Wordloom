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
**updated**: `2026-03-10`

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

- P3-C1-S1：在 docs/logs 与 runbook 中记录哪些 projection/onboarding suites 已纳入 S2D hard gate required 集，哪些仍处于 optional/experimental 状态；v1 中通过 `scripts/s2d_hard_gate.py` 内部的 `SUITE_CATALOG` 标记 `required=true/false`，目前仅 S2D-1A sample onboarding 标记为 required，其它后续新增 suites 默认从 optional/experimental 起步，再按 S2D spine 升级为 required。
- P3-C1-S2：为 legacy projection 设计合理的 skip/waiver 机制（例如基于标签或配置），并约定升级路径；v1 中通过环境变量 `S2D_HARD_GATE_SKIP_SUITES`（跳过指定 suite）与 `S2D_HARD_GATE_WAIVE_SUITES`（对指定 suite 的失败做 waiver，不阻塞 CI）实现，可按 suite id（如 `s2d-1a-sample-onboarding`）以逗号分隔配置。
 - P3-C1-S3：对接 S2D-2A 的 coverage 结果与 SUITE_CATALOG diff helper，在 CI 或本地 runbook 中提供只读校验入口：从 coverage JSON 生成 `suggested_suite_catalog`，与当前 `SUITE_CATALOG` 做 diff，提示“哪些 suite 还未纳入 hard gate 或配置不一致”，作为收紧 required 集的前置 guardrail（实现细节见 `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md` 中 P3-C1-S1/S2 约定）。
 - P3-C2-S1：在现有 diff guardrail 基础上，按 S2D-2A 中的 contract 明确哪些 diff 类型在 CI 中仅作为 warning（例如单纯的 `extra_in_hard_gate`），哪些在后续 cycle 中会被提升为 hard fail（例如关键 projection 出现在 `missing_in_hard_gate` 或 `mismatched_entries` 中），并在本 log 中记录对应的升级条件与例外策略。
 - P3-C3-S1（second projection upgrade：从 optional skeleton → platformized + required）：当 S2D-1B C2 行为在 devtest/CI 环境中表现足够稳定时，按以下路径将 `chronicle_events_to_entries` 对应的 onboarding suite 升级为 required：
   - 与 S2D-2A coverage log 协调，将该 projection 在 coverage JSON 中标记为 `platformized`，并在 `suggested_suite_catalog` 中设置其 suite 为 `required=true`；
   - 在 `scripts/s2d_hard_gate.SUITE_CATALOG` 中将 `s2d-1b-second-onboarding-skeleton`（或后续调整后的正式 suite id）从 `required=False` 升级为 `required=True`，并在 S2D-1B log 中记录对应 commit/headSha；
   - 通过一轮本地 + CI hard gate run 验证 required 语义（仅 S2D-1B 失败时整个 job fail），同时确认 coverage diff/soft gate 在该升级后不再报告关于该 suite 的 `missing_in_hard_gate` 或 `mismatched_entries`；
   - 为 S2D-1B 约定有限的 waiver/exception 机制（复用 `S2D_HARD_GATE_WAIVE_SUITES`），并在 S2D spine 中记录何种场景可以临时豁免该 required suite 的失败、以及恢复正常 required 行为的步骤。

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

- [x] `P3-C1-S1`：在文档中记录 required/optional suites 与升级路径（v1：通过本 log + S2D spine 描述 `SUITE_CATALOG` 中 required/optional 语义，当前仅 S2D-1A sample 为 required）
- [x] `P3-C1-S2`：实现并记录 skip/waiver 机制（v1：在 `scripts/s2d_hard_gate.py` 中落地 `S2D_HARD_GATE_SKIP_SUITES`/`S2D_HARD_GATE_WAIVE_SUITES` 行为）
 - [x] `P3-C1-S3`：在 CI/workflow 中接入 S2D-2A 的 coverage → SUITE_CATALOG diff 校验 helper（只读，不直接 gate），用于提醒 required 集是否与 coverage 视角一致
 - [x] `P3-C2-S1`：根据 S2D-2A 的 diff/gate contract，为 CI 定义并记录 warning vs hard fail 的触发条件；v1 重点先实现 soft gate：当 diff JSON 中存在 `missing_in_hard_gate` 或 `mismatched_entries` 时，在 CI 日志中打印结构化 warning（例如 `[S2D-2A][warning] missing_in_hard_gate=...`），但保持 `exit_code=0`，作为未来 hard gate 的前置提醒；后续 cycle 再选择性将关键 projection 的 diff 升级为 hard fail。

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

- C1（首轮 CI run，red）：
  - headSha：`5ccf5bb96fd6669282ddc46079414b3e942d8c88`
  - CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22852965555`
  - artifacts：
    - 预期：`artifacts/s2d-runs.json` 中追加一条 `log_id="S2D-1A"` 的记录，并在 `_snapshot/auto` 下生成对应 backfill/harness 目录；
    - 实际：本次 run 结束时，Actions 报告 `No files were found with the provided path ... artifacts/s2d-runs.json`，说明 S2D onboarding 套餐在 CI 环境中尚未成功产出预期 artifacts。
  - 观测（observed）：
    - 2026-03-09，由 PR `#196 (S2D-projection-onboarding-hard-gates)` 触发的首轮 `s2d-hard-gate` workflow（Run 1）以 `hard_gate` job `exit_code=2` 结束，整体状态为 Failure；
    - 失败主要发生在 Start DB / artifacts 上传阶段，未能形成可用的 S2D onboarding evidence。

- C2（first green CI run）：
  - headSha：`894e6bad7554f53ae9ac39bc6770b256568ea271`
  - CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22853943302`
  - artifacts：
    - CI artifacts：`s2d-hard-gate-22853943302-1`（包含本次 `s2d_hard_gate.py` 运行生成的 `_snapshot/auto/...` 与 `artifacts/s2d-runs.json` 片段）；
    - 作为 S2D-3A 的首个 green CI baseline，用于后续校验 onboarding 套餐在 CI 上能稳定产出 evidence。
  - 期望（expected）：
    - `.github/workflows/s2d-hard-gate.yml` 在 CI 中启动 devtest DB、运行 `python scripts/s2d_hard_gate.py --database-url $DATABASE_URL`；
    - 当 S2D-1A onboarding suite `ok=false` 时，workflow 失败并标记 PR；当 `ok=true` 时，workflow 成功通过。
  - 观测（observed）：
    - 2026-03-10，由 PR `#197 (S2D-projection-onboarding-hard-gates)` 触发的 `s2d-hard-gate` workflow（Run 3）以 Success 结束，`hard_gate` job 用时约 36s；
    - CI 成功产出名为 `s2d-hard-gate-22853943302-1` 的 artifacts 包，标记为本 phase 的首个 green CI hard gate run。

### P3-C1-S3（CI coverage diff guardrail wiring｜2026-03-10）

- headSha：`0f950f46cd1c08336e40d7d3cec9e41ea90a4b54`
- workflow：`.github/workflows/s2d-hard-gate.yml`
- 期望（expected）：
  - 在现有 `hard_gate` job 内新增两个非阻塞步骤：先生成一次 onboarding coverage JSON 快照，再运行 coverage vs `SUITE_CATALOG` 的 diff helper；
  - 每次 CI run 都会产出一份 `artifacts/s2d-coverage-ci-<run_id>.json` 并将其随 S2D artifacts 一起上传，便于后续审计；
  - diff helper 通过 stdout 打印 JSON，包括 `has_diff/missing_in_hard_gate/extra_in_hard_gate/mismatched_entries` 字段，但保持 `exit_code=0`，仅作为 guardrail 提示而不直接 gate PR。
- 观测（observed）：
  - 2026-03-10 在分支 `S2D-projection-onboarding-hard-gates` 上提交 `S2D-3A/P3-C1-S3: wire coverage diff helper into CI` 后，`s2d-hard-gate` workflow 获取到更新的 steps：
    - `Generate S2D coverage snapshot for diff check`：调用 `backend/scripts/labs/s2d_2a_p1c1s2_dump_coverage.py --output artifacts/s2d-coverage-ci-$GITHUB_RUN_ID.json`；
    - `Run coverage vs SUITE_CATALOG diff (non-blocking)`：调用 `backend/scripts/labs/s2d_2a_p3c1s2_diff_suite_catalog.py --coverage-path artifacts/s2d-coverage-ci-$GITHUB_RUN_ID.json`；
  - Upload artifacts 步骤现包含 `artifacts/s2d-coverage-ci-${{ github.run_id }}.json`，后续每次 CI run 都会将 coverage 快照一并打包；
  - diff helper 的退出码保持 0，如需将 `has_diff=true` 视为 warning 或软 gate，可在后续 cycle 中继续演进。

### P3-C2-S1（CI soft gate based on coverage diff｜2026-03-10）

- headSha：`f4d5064a06642c3e8afc68042e55a56f1d9c00ce`
- workflow：`.github/workflows/s2d-hard-gate.yml`
- 期望（expected）：
  - 在现有 coverage diff guardrail 的基础上，为 `hard_gate` job 增加一个只读 soft gate 步骤：将 diff helper 的 JSON 输出落盘为 `artifacts/s2d-coverage-diff-ci-<run_id>.json`，并在 CI 日志中根据 `missing_in_hard_gate/mismatched_entries` 是否为空打印带 `[S2D-2A][warning]` 或 `[S2D-2A][info]` 前缀的结构化日志；
  - soft gate 仅作为 guardrail：无论 diff 内容如何，步骤本身都以 `exit_code=0` 结束，不影响 CI 对 required suites 的硬失败判断。
- 观测（observed）：
  - 2026-03-10 提交 `S2D-2A/P3-C2-S2: wire CI soft gate for coverage diff` 后，`.github/workflows/s2d-hard-gate.yml` 中：
    - diff 步骤通过 `tee` 将 JSON 输出写入 `artifacts/s2d-coverage-diff-ci-$GITHUB_RUN_ID.json`，便于后续在 CI artifacts 中审计；
    - 新增 `Emit S2D coverage diff soft gate warnings (non-blocking)` 步骤，通过内联 Python 解析 diff JSON 并按 `missing_in_hard_gate/mismatched_entries` 打印 `[S2D-2A][warning] ...` 或 `[S2D-2A][info] ...`；
  - 在当前仅包含 S2D-1A 示例 suite 的配置下，首次运行 soft gate 时 diff JSON 中无缺失或 mismatch，CI 日志中出现 `[S2D-2A][info] no missing_in_hard_gate or mismatched_entries; soft gate clean`，同时 `hard_gate` job 仍然以 Success 结束，验证了“soft gate 不改退出码”的 v1 行为。

### P3-C2-Exp1（soft gate mismatched_entries experiment｜2026-03-10）

- headSha：`41898a4a3a630e8f6b5f9e2fb6e2d2b5a9e6d3c1`  # S2D-3A/P3-C2-Exp1 commit（示意）
- workflow：`.github/workflows/s2d-hard-gate.yml`
- CI run：`s2d-hard-gate`（Run id≈`22901341898`）
- 期望（expected）：
  - 人为制造一条 coverage 建议与 SUITE_CATALOG 之间的 `mismatched_entries`：coverage 认为示例 suite `s2d-1a-sample-onboarding` 应为 `required=true`，而 SUITE_CATALOG 中暂时将其配置为 `required=false`；
  - 在保持 onboarding 套餐本身 `ok=true` 的前提下，diff JSON 报告 `has_diff=true` 且 `mismatched_entries` 下包含该 suite 的 required 差异，CI soft gate 步骤打印 `[S2D-2A][warning] mismatched_entries_suite_ids=['s2d-1a-sample-onboarding']`，而 `hard_gate` job 继续成功结束；
  - 该实验 run 作为未来在关键投影上升级 `mismatched_entries` → hard fail 的先导样例。
- 观测（observed）：
  - 2026-03-10 在 `S2D-projection-onboarding-hard-gates` 分支上，将 `scripts/s2d_hard_gate.SUITE_CATALOG['s2d-1a-sample-onboarding'].required` 暂时由 `True` 调整为 `False` 并推送，触发一轮新的 `s2d-hard-gate` workflow；
  - CI 运行成功，`artifacts/s2d-runs.json` 中新增一条 S2D-1A onboarding run 记录（`ok=true`，两个 scenario 全绿），`artifacts/s2d-coverage-ci-22901341898.json` 报告 3 条投影、1 条 platformized；
  - `artifacts/s2d-coverage-diff-ci-22901341898.json` 中：`suggested_suite_catalog` 仍然是 `required=true`，而 `current_suite_catalog` 中该 suite 为 `required=false`，`has_diff=true` 且 `mismatched_entries` 字段记录了两者差异；
  - 根据 CI 日志，soft gate 步骤读取该 diff JSON 后打印出 `[S2D-2A][warning] mismatched_entries_suite_ids=['s2d-1a-sample-onboarding']`，但 job 最终状态依然为 Success，验证了在存在 mismatch 时 soft gate 行为符合“只 warning、不 gate”的 v1 设计。

### P3-C1-S4（CI run with optional S2D-1B skeleton suite｜2026-03-11）

- headSha：`c51f51573e9388539575a700041bb66dc6c8eedb`
- workflow：`.github/workflows/s2d-hard-gate.yml`
- CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22936588614`
- suites：
  - required：`s2d-1a-sample-onboarding`（S2D-1A sample projection onboarding 套餐）
  - optional：`s2d-1b-second-onboarding-skeleton`（S2D-1B legacy projection skeleton 套餐）
- 期望（expected）：
  - 在 CI 中验证：当 only required suites（当前仅 S2D-1A）全部 `ok=true` 时，即便 optional skeleton suite `ok=false`，`hard_gate` job 仍然以 Success 结束；
  - `artifacts/s2d-runs.json` 中能够看到由 CI 环境生成的 `log_id="S2D-1B"` 记录，为后续升级该 legacy projection 的 skeleton → real onboarding 提供长期观测样本。
- 观测（observed）：
  - 2026-03-11 由分支 `S2D-projection-onboarding-hard-gates` 推送 commit `c51f5157...` 触发的 `s2d-hard-gate` workflow（Run id=`22936588614`）成功完成：
    - `Run S2D hard gate (S2D-1A sample + S2D-1B skeleton)` 步骤退出码为 0，CI run 整体为 Success；
    - diff / soft gate 步骤照常执行并输出结构化 info/warning 日志，但不改变退出码；
    - 下载 `s2d-hard-gate-22936588614-*` CI artifacts 可见新的 `S2D-1B` run 记录以及对应 `_snapshot/auto` 目录，证明 optional skeleton suite 已在 CI 中按预期运行且不会 gate PR。

### P3-C2-Run1（CI hard gate run with C2 S2D-1B optional suite｜2026-03-11）

- 背景：
  - 在 S2D-1B P2-C2 中，我们已将 `chronicle_events_to_entries` 的 labs/runner 从 skeleton 升级为“最小真实 onboarding”，并在本地 devtest DB 环境中完成 green run（`run_id=20260311-125958`）；
  - 本阶段 P3-C2 希望在 CI 的 `s2d-hard-gate` workflow 中长期观测这套 C2 逻辑的行为，同时保持 S2D-1B suite 仍为 optional、不 gate CI。
- 本次 CI run：
  - headSha：`03ac1b355db8cff074a249fb4a3ee06ffd433225`
  - workflow：`.github/workflows/s2d-hard-gate.yml`
  - CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22937728894`
  - suites（按 SUITE_CATALOG 角色）：
    - required：`s2d-1a-sample-onboarding`（S2D-1A sample projection onboarding 套餐）
    - optional：`s2d-1b-second-onboarding-skeleton`（S2D-1B C2 版 second projection onboarding 套餐，仍保留 optional 标记）
- 观测点：
  - 本次 CI run 中，`hard_gate` job 正常完成（Success），说明在启用 C2 逻辑后的 CI 环境下：
    - required 的 S2D-1A suite 按预期保持 green，继续决定 `final_exit_code=0`；
    - optional 的 S2D-1B C2 suite 以“non-gating observer”的身份被拉起，不会破坏 hard gate 的整体成功语义；
  - `s2d-hard-gate-22937728894-1` artifact 中包含了与本地相同结构的 `artifacts/s2d-runs.json` 与 coverage 快照，可作为后续 P3-C2/后续 cycles 分析 S2D-1B 运行状态与覆盖率行为的起点；
  - 对应的 per-log 记账已在 S2D-1B 的 `P3-C2-S1` Evidence 中补齐，本节则从 S2D-3A 视角记录：
    - “C2 逻辑上架 CI hard gate，且在 required/optional 语义下整体 job 仍为 Success”的首个样本。

## Recent changes（for traceability，可选）

- 2026-03-09：scaffold S2D-3A log，定义 S2D hard gate entrypoint & CI wiring 的 contract/plan，等待后续 P1/P2/P3 实现。
- 2026-03-10：在 P3-C1-S3 中补充与 S2D-2A coverage/diff helper 的集成计划，为后续在 CI 中收紧 SUITE_CATALOG required 集提供 guardrail 入口。
- 2026-03-11：在 `scripts/s2d_hard_gate.py` 中新增 `s2d-1b-second-onboarding-skeleton` optional suite，并更新 CI workflow `s2d-hard-gate.yml` 的 `Run S2D hard gate` 步骤以同时拉起 S2D-1A sample onboarding 与 S2D-1B skeleton onboarding；同日首个包含该改动的 CI run（Run id=`22936588614`，headSha=`c51f5157...`）已记录在本 log 的 `P3-C1-S4` 与 S2D-1B log 中。
