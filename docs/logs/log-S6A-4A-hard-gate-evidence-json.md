# log-S6A-4A-hard-gate-evidence-json（P4：Hard-gate + evidence JSON｜CI 失败自解释 v1）

---

**id**: `S6A-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `fault suite hard-gate + evidence JSON (CI self-explaining artifacts) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Artifacts, CI, HardGate, FailureContract, epic/s6, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/169`
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **previous_log**: `docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md`
  **reference_log_1**: `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
  **reference_log_2**: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**created**: `2026-03-05`
**updated**: `2026-03-06`

---

## Decision / Outcome（结论区）

**Decision**:

- 将 `fault/obs_infra/*` drills 的“CI 关卡”产品化为 hard-gate：**PASS/FAIL 必须机器可判定**，并且失败时 artifacts 必须自解释（无需靠截图/猜日志）。
- 将 artifacts 的最小输出收口为一套稳定 contract：每次 run/verify 至少写出 `snapshot_dir/_result.json`，并允许可选的 `artifacts/summary.json`、`artifacts/logs.txt`、`artifacts/traces.json` 与（可选）zip。

**Default choices（本 phase 默认决策 / v1）**:

- 事实源以 `snapshot_dir/_result.json` 为准；CI 只需围绕它做 gate 与上传。
- artifacts 以“最小可复盘集”为准：默认不追求全量日志，只保证失败时能定位到 *哪一步失败、期望/观测差异是什么、关键 run 参数是什么*。
- 证据 JSON 字段以低基数为原则：高基数内容（URL、堆栈、UUID 列表、完整日志）只能进入 artifacts 文件，不进入 reason 维度或固定 label。

## Definitions（概念定义，可选）

- `hard-gate`：CI 中对 drills 的强制关卡；失败即阻断合入/发布（或至少阻断“可切写”阶段）。
- `evidence JSON`：用于机器判定与快速复盘的结构化 JSON（本阶段默认指 `_result.json`）。
- `self-explaining artifacts`：失败时无需额外手动操作即可定位原因（含最小日志、关键参数、期望 vs 观测）。
- `snapshot_dir`：drills 的运行目录（包含 `_recipe.json`、`_result.json`、metrics dumps、worker logs 等）。

## Constraints（约束）

- 不引入第二套事实源：CI 的 gate 以 `_result.json.ok` 为准，不再引入“另一个 summary 标准”。
- 不让 artifacts 失控：禁止把无限增长的 dump 入仓库；zip/上传在 CI 侧处理，本地只落 snapshot。
- 保持 stable entry：worker spawn 与 env wiring 的稳定入口继续由 S6A-1A 的 helper 保障，不在 CI 层重复拼装。
- reason 仍必须低基数：P3 的 reason contract 是 P4 gate 的输入之一，但 gate 不应要求 reason 细节高基数化。

## Scope（本 log 范围）

- `P0`：contract（CI gate 语义 + evidence JSON 最小字段 + artifacts 最小集合）
- `P1`：runner/CLI 层统一输出（保证所有场景都写 `_result.json`，失败时附带最小 logs/metrics dumps）
- `P2`：GitHub Actions hard-gate（run + verify + upload artifacts；失败自解释）
- `P3`：guardrails（入口漂移/输出漂移零容忍：缺 `_result.json` 直接 FAIL）
- `P4`（可选）：本地一键复刻 CI gate（单命令跑 suite + 产出同样 artifacts）

## Success Criteria（DoD）

- CI 对至少 1 个 `fault/obs_infra/*` 场景形成 hard-gate：
  - `verify` 失败时 workflow 失败
  - artifacts 上传包含 `snapshot_dir/_result.json` 与最小排障材料
- 每个被纳入 gate 的场景都满足 artifacts contract：
  - **必有**：`_result.json`（包含 `ok: true|false`、scenario、run_id/outdir、expected/observed）
  - **建议有**：worker log 路径（或 logs.txt）、metrics dumps（before/after）、`_recipe.json`
- 失败自解释：仅靠 artifacts 可回答：
  - 失败发生在 run 还是 verify？
  - 期望与观测差异是什么？（metrics delta / DB rows / reason_contract）
  - 关键注入/knobs 是什么？

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - 至少 1 个 fault scenario 在 CI 中作为 hard-gate 长期运行
  - artifacts contract 在 workflow 层被制度化（缺 `_result.json` 直接 FAIL）
  - 失败 artifacts 可自解释（最小排障材料齐全且路径稳定）

## P0（Contract｜v1）

### P0-C1-S1（Hard-gate semantics｜v1）

- gate 的 PASS/FAIL：以 `labs verify <scenario>` 的退出码与 `_result.json.ok` 为准。
- gate 的“不可判定”视为失败：例如 `_result.json` 缺失/无法解析、verify 未输出结果等。

### P0-C1-S2（Evidence JSON schema｜v1）

- `_result.json`（最小字段建议）：
  - `scenario`（string）
  - `run_dir`（string）
  - `ok`（bool）
  - `checks`（object，描述判定阈值）
  - `observed`（object，观测值/统计）
  -（按场景可选）`reason_contract`、`supply_db_check`、`worker`、`supply`

### P0-C1-S3（Artifacts contract｜v1）

- 最小必需：
  - `snapshot_dir/_result.json`
- 推荐（用于失败自解释）：
  - `snapshot_dir/_recipe.json`
  - `snapshot_dir/_logs/*`（或聚合到 `artifacts/logs.txt`）
  - `snapshot_dir/_metrics/*`（before/after dumps）
- 可选（CI 上传优化）：
  - `snapshot_dir.zip`（仅 CI 上传；本地可不开启）

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S6A-4A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（输出统一：runner/CLI 层）

- P1-C1-S1：梳理所有 `fault/obs_infra/*` verify 是否都写 `_result.json`（缺失则补齐）
- P1-C1-S2：失败时最小排障材料落盘（logs/metrics/recipe），避免“只有 FAIL 没原因”

### P2（CI hard-gate：workflow）

- P2-C1-S1：新增/调整 workflow：run → verify → upload artifacts（按 scenario 组织目录）
- P2-C1-S2：将 `_result.json.ok=false` 或 verify 非零退出码视为 workflow failure
- P2-C1-S3：首次 CI run 记账：补齐 `headSha + CI run URL + artifacts` 到本 log 的 Evidence
- P2-C2-S1：为 gate 的场景建立最小运行矩阵（避免 flake，确保 determinism）

### P3（Guardrails）

- P3-C1-S1：在 workflow 或 runner 中增加“contract check”：缺 `_result.json` 直接 FAIL
- P3-C1-S2：记录 `headSha + run_id + artifacts path` 到对应领域 log（保持可追溯）

### P4（可选：本地一键复刻 CI gate）

- P4-C1-S1：提供一个单命令入口（脚本/任务）运行一个 suite 并生成同构 artifacts

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：Hard-gate semantics（PASS/FAIL/不可判定）
- [x] `P0-C1-S2`：Evidence JSON schema（最小字段）
- [x] `P0-C1-S3`：Artifacts contract（最小自解释集）

### P1（输出统一）

- [ ] `P1-C1-S1`：覆盖检查：所有 gate 场景都产出 `_result.json`
- [ ] `P1-C1-S2`：失败自解释：最小 logs/metrics/recipe 落盘

### P2（CI hard-gate）

- [x] `P2-C1-S1`：workflow：run + verify + upload artifacts
- [x] `P2-C1-S2`：workflow gate：verify 失败直接失败（阻断）
- [x] `P2-C1-S3`：首次 CI run 记账：补齐 `headSha + CI run URL + artifacts` 到 Evidence

### P3（Guardrails）

- [x] `P3-C1-S1`：contract check：缺 `_result.json` 或 `_result.json.ok!=true` 直接 FAIL
- [x] `P3-C1-S2`：可追溯性：headSha + run_id + artifacts path 落 log

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S2（CI hard-gate｜<scenario>｜YYYY-MM-DD）

- headSha：`<git sha>`
- CI run：`<workflow url>`
- artifacts：`<artifact link or path>`
- 期望（expected）：
  - `_result.json.ok=true`
- 观测（observed）：
  - `_result.json.ok=<...>`

### P2-C1-S2（CI hard-gate｜fault/obs_infra/es_timeout｜2026-03-05）

- workflow：`.github/workflows/hard-gate-fault-es-timeout.yml`
- scenario_id：`fault/obs_infra/es_timeout`（catalog-driven）
- PR：`https://github.com/samuelhu324-dev/wordloom-v3/pull/169`
- headSha：`df56af5ac10ce9b64c01086f6b08178e7f2fdc1a`
- CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22743038743`
- artifacts：`labs-evidence-fault_obs_infra_es_timeout-22743038743-1`（包含 `docs/labs/_snapshot/auto/` 下的 `_result.json` 等）
- 期望（expected）：
  - `labs verify es_timeout` exit code = `0`
  - `_result.json.ok=true`

- 观测（observed）：
  - `_result.json.ok=true`
  - `outbox_retry_scheduled_total{reason="es_timeout"}` delta = `1`
  - `outbox_failed_total{reason="es_timeout"}` delta = `1`
  - DB `outbox_events.error_reason=es_timeout` 且 family=`timeout`

## Recent changes（for traceability，可选）

- 2026-03-05：创建本 log，开始将 drills 推进为 CI hard-gate（evidence JSON + 自解释 artifacts）。
