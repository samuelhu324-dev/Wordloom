# log-S0D-2A-drills-evidence-automation（Phase 2：Drills/Evidence 自动化结构 v1）

---

**id**: `S0D-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `drills/evidence 自动化结构（目录约定 + run_dir 发现 + write_gate 汇总） v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Tooling, Drills, Evidence, Automation, HardGate, epic/s0, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: ``
  **previous_log**: ``
  **reference_log_1**: `docs/logs/log-S5B-1A-policy-audit-hard-gate-drills.md`
  **reference_log_2**: `docs/logs/log-S5B-3A-audit-coverage-operator-workflow.md`
**created**: `2026-03-07`
**updated**: `2026-03-07`

---

## Decision / Outcome（结论区）

**Decision**:

- 为 drills/evidence 建立一套可复用的 **自动化结构**：固定 run_dir 布局、runner 输出约定、hard gate/工具自动发现 run_dir，并把关键信息写入 artifacts 汇总 JSON。
- 统一 "log ↔ artifacts ↔ write_gate" 的证据链：log 只记录 `headSha + run_dir (+ ci_url)`，真实 JSON artifacts 落在 `docs/labs/_snapshot/auto/...`，而 `artifacts/*.json` 负责聚合/索引，供 CI/dashboard/后续阶段使用。

**Default choices（本 phase 默认决策 / v1）**:

- 所有 Phase SxY-ZA drills/evidence 优先复用：
  - `docs/labs/_snapshot/auto/<LOG_ID>/<suite_id>/<run_id>/` 作为事实源目录；
  - `s5b-1a.recipe.v1 / s5b-1a.result.v1 / s5b-1a.metrics.v1` 作为默认 schema；
  - `scripts/drills/s5b1a_verify_artifacts.py` 作为默认 verifier（可选）。
- write_gate 汇总文件一律放在 `artifacts/` 根目录下，命名约定：
  - `<log_id>-runs.json`（完整历史）；
  - `<log_id>-runs.final.json`（对外展示用的稳定视图）；
  - `write_gate_runs.latest.json` 作为所有 hard gate 的轻量索引。

## Definitions（概念定义）

- **run_dir**：一次 drills/hard gate run 的唯一目录，包含 `_recipe.json/_result.json/_logs/_metrics`，可单独作为证据包归档。
- **suite_id**：runner 内部的场景/套件标识（如 `tenant_escape_read`、`membership_audit_coverage`）。
- **write_gate run**：一次完整的 hard gate 入口执行，包含：所有 suite 的 run_dir、git sha、整体 PASS/FAIL 结果以及环境参数快照。
- **contract_ok/result_ok**：verifier 对 run_dir 的两层判定：contract_ok 代表 artifacts 结构/schema 正确，result_ok 代表业务 case 全部 PASS。

## Constraints（约束）

- drills 输出目录必须 **只增不改**：同一个 run_id 目录内的 JSON 禁止被 in-place 改写（只允许新增新的 run_id 目录）。
- log 只记录 **引用信息**（sha + run_dir + ci_url），不直接粘贴大 JSON；证据以 artifacts 为事实源。
- write_gate 汇总 JSON 必须低基数、机器可解析：禁止塞入大体积自由文本（如完整 stdout），只保留路径/枚举型状态。

## Scope（本 log 范围）

- `P0`：contract（目录/命名约定、run_dir 发现规则、汇总 JSON schema）。
- `P1`：实现（通用 helper + S5B-1A/S5B-2A/S5B-3A 适配）。
- `P2`：drill/verify（为 S5B-3A 等日志提供自动化 run + verify + 入账流水线）。
- `P3`：hard gate（可选）：统一入口脚本 + CI workflow；或显式记录不接入原因。

## Success Criteria（DoD）

- 任意一个基于本 contract 的 log（如 S5B-3A）满足：
  - 从 log 中最新一条 Evidence 记录能 **机械解析** 出 `log_id/headSha/run_dir`；
  - 在 repo 根执行一次 hard gate 入口脚本即可：
    - 自动发现/创建 run_dir；
    - 自动调用 verifier；
    - 自动更新 `artifacts/<log_id>-runs.json`；
    - 正确以 exit code 表示 PASS/FAIL。
- CI 能通过 `artifacts/*runs*.json` 和 run_dir 结构，构建最小 dashboard 或做回归检查，而不用额外人工输入。
- 本 log 标记为 `stable` 时，S5B-1A/S5B-2A/S5B-3A 至少有 1 条完整 run 是通过 S0D-2A 的自动化入口完成并写入汇总。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0 contract（目录约定 + run_dir 发现 + 汇总 JSON schema）已实现并在至少 1 个 log 上跑通；
  - 至少一个 hard gate/runner 已经接入 S0D-2A 的自动化入口（可在 CI 或本地 repeat）；
  - Evidence 区有可追溯的 `headSha` + `run_dir` + 对应 `artifacts/<log_id>-runs.json` 条目。

## P0（Contract｜v1）

### P0-C1-S1（Artifacts 目录与 runner 输出约定）

- 目录布局：
  - 每次 run 输出到：`docs/labs/_snapshot/auto/<LOG_ID>/<suite_id>/<run_id>/`。
  - 目录内至少包含：`_recipe.json`、`_result.json`、`_logs/run.log`、`_metrics/summary.json`。
- runner 输出：
  - stdout 中必须打印一行：`[OK] Wrote artifacts to <run_dir>`；
  - `<run_dir>` 为上述相对路径，便于 hard gate/higher-level 工具通过正则自动捕获。
- fallback 规则：
  - 若 stdout 未包含 run_dir，自动工具应回退到：
    - 在 `docs/labs/_snapshot/auto/<LOG_ID>/<suite_id>/` 下按 mtime 选择最近的子目录作为 run_dir（与 S5B-1A hard gate 现有逻辑一致）。

### P0-C1-S2（Evidence & 汇总 JSON schema）

- 每条 Evidence（写在各自业务 log 的 Evidence 区）至少包含：
  - `headSha=<git sha>`（必填）；
  - `run_dir=docs/labs/_snapshot/auto/<LOG_ID>/<suite_id>/<run_id>/`（必填）；
  - （可选）`ci_url=<workflow_run_url>`；
  - 可选附加信息：`summary={total, passed, failed}` / `error_type=...`。
- S0D-2A 负责维护的汇总 JSON（以 S5B-3A 为例）：
  - 路径约定：`artifacts/s5b3a-runs.json`（全部历史） + `artifacts/s5b3a-runs.final.json`（对外暴露用）；
  - 条目结构（v1 draft）：
    - `log_id`: string（如 `S5B-3A`）
    - `phase`: string（如 `P2`）
    - `cycle`: string（如 `C1`）
    - `step`: string（如 `S1`）
    - `head_sha`: string
    - `run_dir`: string（相对路径）
    - `suite_id`: string
    - `ok`: bool（来自 `_result.json.ok`）
    - `contract_ok`: bool（verifier 的 contract 判定）
    - `result_ok`: bool（verifier 的 result 判定）
    - `ci_url`: string | null
    - `created_at`: string（ISO-8601, UTC）

### P0-C1-S3（Commit / PR 命名 & 解析约定）

- Commit/PR message 固定格式：
  - 基础形式：`<LOG_ID>/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（如 `1`，即 `...-S1: ...`），也可以是同一 phase / 同一 cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2: ...`）。
  - 例如：
    - 单步提交：`S5B-3A/P2-C1-S2: membership audit coverage green evidence`；
    - 多步合并：`S0D-2A/P1-C1-S1S2: shared artifacts helper and S5B hard gates`（同时完成 P1-C1 下的 S1 和 S2）。
- Multi-step 规则：
  - 只允许在 **同一 Phase（P<phase>）+ 同一 Cycle（C<cycle>）** 下，将多个 step 一起完成时写成 `S1S2S3` 这种合并形式；
  - 一旦涉及新的 Phase（例如同时做 P1 和 P2）或不同 Cycle，必须拆成多次 commit，分别记录，例如本次将 P1-C1-S1S2 与 P2-C1-S1 拆成两条提交。
- 自动化工具可用正则解析：
  - `(?P<log_id>S\w+-\w+)/P(?P<phase>\d+)-C(?P<cycle>\d+)-S(?P<steps>\d+(?:S\d+)*):`；
  - 其中 `steps` 捕获形如 `"1"` 或 `"1S2S3"` 的字符串，可按 `"S"` 切分得到 step 列表；
  - 将解析结果与 `artifacts/<log_id>-runs.json` 条目对齐，形成完整证据链：`commit → headSha → run_dir → _result.json/_logs → write_gate 汇总`。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。

**Branch 约定（可选，但推荐遵守）**:

- 对应 scope/index 的 log（例如 `S5B-3A` 隶属于 `S5B`，`S0D-2A` 隶属于 `S0D`）优先在同名前缀的工作分支上推进 P* 的代码与文档变更：
  - 例如：`S5B-3A` 相关改动优先落在 `S5B-...` 系列分支（如 `S5B-security-governance-hard-gates`）；
  - `S0D-2A` 这类 meta/docs/automation 改动优先落在 `S0D-...` 系列分支（如 `S0D-docs-management-v4`）。
- 如果一次 PR 同时涉及多个 scope/index（例如同时修改 `S5B-3A` 和 `S0D-2A`），建议拆成多条 PR：每条 PR 聚焦一个 scope/index 与对应分支，便于后续自动化按 scope 做聚合与回溯。

## Plan（draft）

### P1（实现：通用 helper + 适配）

- P1-C1-S1：抽取 `_artifact_run_dir` / run_dir 正则 / mtime fallback 等通用 helper（可放在 `scripts/drills/_shared_artifacts.py` 或等价模块）。
- P1-C1-S2：为 S5B-1A/S5B-2A/S5B-3A 的 runner/hard gate 入口接入上述 helper，统一 stdout run_dir 行和目录布局。

### P2（drill/verify：S5B-3A 流水线接入）

- P2-C1-S1：新增 `s5b3a_p4_hard_gate.py`，负责：
  - 运行 `membership_audit_coverage` drills；
  - 自动解析 run_dir；
  - 调用 `s5b1a_verify_artifacts.py`；
  - 将结果写入 `artifacts/s5b3a-runs.json`。
- P2-C1-S2：在 S5B-3A 的 Evidence 区记录至少 1 条通过 S0D-2A 入口跑出来的 run（headSha + run_dir + artifacts 条目索引），并根据结果勾选/更新 S5B-3A 的 P2 checklist。

### P3（hard gate：CI 集成，可选）

- P3-C1-S1：新增或扩展 CI workflow：
  - 在适当环境下启动 API + DB；
  - 调用 `python scripts/drills/s5b3a_p4_hard_gate.py`；
  - 将 `docs/labs/_snapshot/auto/S5B-3A/...` 和 `artifacts/s5b3a-runs*.json` 作为 CI artifacts 上传；
  - 以 hard gate 脚本 exit code 作为 CI 成功/失败依据。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：Artifacts 目录 + runner 输出约定固定
- [x] `P0-C1-S2`：Evidence & 汇总 JSON schema 固化
- [x] `P0-C1-S3`：Commit/PR 命名 & 解析约定固化

### P1（实现：通用 helper + 适配）

- [x] `P1-C1-S1`：抽取 shared artifacts helper
- [x] `P1-C1-S2`：S5B-1A/S5B-2A/S5B-3A 适配

### P2（drill/verify：S5B-3A 流水线接入）

- [x] `P2-C1-S1`：s5b3a hard gate 入口脚本
- [ ] `P2-C1-S2`：首条通过 S0D-2A 的 Evidence 入账

### P3（hard gate：CI 集成）

- [x] `P3-C1-S1`：CI workflow 接入（或记录不接入原因）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（S5B-3A hard gate 接入 scaffold｜2026-03-07）

- headSha：`7995b73482a1dbfd30b79af4c927c71d72ff5a61`
- artifacts：`artifacts/s5b3a-runs.json` 中对应条目 + `docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/9d3cdfc1-2fb0-43c8-8364-a00b5db4e87e/`
- env：
  - `WORDLOOM_API_BASE_URL=http://127.0.0.1:31001`
  - `DATABASE_URL=postgresql://wordloom:wordloom@127.0.0.1:5435/wordloom_test`
- 期望（expected）：
  - hard gate 入口 exit code=0；
  - verifier `contract_ok=true` 且 `_result.json.ok=true`。
- 观测（observed）：
  - 首次 hard gate 运行：
    - `runner_rc=0`，drills runner 能完整产出 artifacts；
    - `verify_rc=1`，`contract_ok=true` 但 `_result.json.ok=false`（5 个 case 均为红），写入 `artifacts/s5b3a-runs.json` 时记录为 `ok=false / result_ok=false`；
    - 由于底层 membership_audit_coverage 仍为 red evidence，本条仅视为 S0D-2A 接入 scaffold，不作为 green evidence；`P2-C1-S2` 将在首次 green hard gate run（ok=true）之后单独入账。

### P2-C1-S2（S5B-3A hard gate 首次 green run｜TBD）

- 预期执行路径：
  - 由 CI workflow（hard-gate-s5b3a-membership-audit.yml）在 devtest DB + 本地 uvicorn backend 环境下调用 `python scripts/drills/s5b3a_p4_hard_gate.py`；
  - hard gate 入口 exit code=0，`artifacts/s5b3a-runs.json` 追加一条 `ok=true / contract_ok=true / result_ok=true` 记录；
  - `_result.json.ok=true` 且 5 个 membership_audit_coverage cases 全部通过。
- 当前本地多次试跑仍受环境约束（API 端口/网络连通性问题）导致 red evidence：
  - 最近一次运行 headSha=`2d2468f191ed2e4effabf2b9e8d07e99dd6e3966`；
  - run_dir=`docs/labs/_snapshot/auto/S5B-3A/membership_audit_coverage/15590d54-9b20-4a8c-b164-06f0ea474bbb/`；
  - `_result.json.summary={"total":5,"passed":0,"failed":5}`，`ok=false`，failure_reason=`unexpected_error`（ConnectError）；
  - 该条记录已写入 `artifacts/s5b3a-runs.json`，用于证明 S0D-2A wiring 生效，但仍不视为 P2-C1-S2 的 green evidence。

### P3-C1-S1（CI hard gate wiring｜2026-03-08）

- 新增 reusable workflow：`.github/workflows/hard-gate-s5b3a-membership-audit.yml`：
  - 触发：对 backend、S5B-3A drills、S0D-2A log 等相关文件的 PR 变更，或 `workflow_dispatch` 手动触发；
  - 步骤：
    - 使用 `docker-compose.devtest-db.yml` 启动 devtest Postgres，并确保存在 `wordloom_test` 库；
    - 安装 backend 依赖并通过 Alembic 将 `wordloom_test` 迁移到最新；
    - 以 `uvicorn api.app.main:app --host 127.0.0.1 --port 31001` 启动 backend；
    - 在同一 job 中设置 `WORDLOOM_API_BASE_URL` 和 `DATABASE_URL`，调用 `python scripts/drills/s5b3a_p4_hard_gate.py`；
    - 上传 `docs/labs/_snapshot/auto/S5B-3A/**` 与 `artifacts/s5b3a-runs*.json` 作为 CI artifacts，便于后续审计与取证；
  - hard gate 语义：job 直接以 S5B-3A hard gate 脚本 exit code 作为通过/失败标准（0=通过，非 0=fail）。

## Recent changes（for traceability，可选）

- 2026-03-07：scaffold S0D-2A Phase 2 log skeleton（drills/evidence 自动化结构）。
