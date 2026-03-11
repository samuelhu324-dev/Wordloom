# log-S2D-1C-projection-onboarding-skeleton-third-sample（Phase 1C：Third projection onboarding skeleton for legacy → platformized）

---

**id**: `S2D-1C`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `third projection onboarding skeleton for legacy → platformized (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S2D`
**tags**: `EVOLUTION, Projection, Onboarding, Drills, Evidence, epic/s2d, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2D-projection-onboarding-hard-gates.md`
  **previous_log**: `docs/logs/log-S2D-1B-projection-onboarding-skeleton-second-sample.md`
  **reference_log_1**: `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
  **reference_log_2**: `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`
**created**: `2026-03-11`
**updated**: `2026-03-11`

---

## Decision / Outcome（结论区）

**Decision**:

- 在 S2D-1A / S2D-1B 形成的“sample + second legacy projection”链路基础上，继续为下一条 legacy projection 搭建一套最小 onboarding skeleton（log + labs + scripts 占位），作为批量迁移 legacy 投影的第三个样本；
- 沿用 S2D-1A/S2D-1B 的 onboarding contract 与 Evidence 口径，但允许本 phase 只交付 skeleton 与占位脚本（可以先跑不通），重点是结构/入口统一、证据 JSON 口径对齐，并在 S2D-2A coverage 视角下为该投影预留从 `legacy` → `platformized` 的升级路径。

**Default choices（本 phase 默认决策 / v1）**:

- 仅选择 1 条当前在 onboarding coverage 中被标记为 `legacy` 的投影作为 S2D-1C 目标（具体 projection 可在 P0-C1-S1 里通过 coverage JSON/业务优先级协商确认），避免一次性并行迁移过多 legacy 投影；
- v1 仍以 dev/test 环境为主，只要求 skeleton labs/scripts 在 devtest DB 下可以产出结构正确的 `_result.json` 与 `artifacts/s2d-runs.json` 记录，不强制立刻接入 hard gate/CI（是否接入由后续 S2D-3A/S2D-2A cycle 决定）；
- 复用 S2D-1A/S2D-1B 的命名/目录布局（labs 在 `backend/scripts/labs`，runner 在 `scripts/projections`，log 在 `docs/logs`），使后续新增第 4/5 条 legacy projection 时可以简单复制本 log 与脚本作为模板。

## Definitions（概念定义）

- **Third onboarding skeleton**：继 S2D-1A sample 和 S2D-1B second projection 之后，为第三条 legacy projection 搭建的一套最小 onboarding 结构（log + labs + scripts），可以暂时是半成品，但结构与前两条样本保持一致。
- **Target legacy projection（S2D-1C）**：当前在 S2D-2A coverage JSON 中被标记为 `legacy`、尚未按 S2D onboarding contract 补齐 spec/adapter/drills 的投影，具体名称待在 P0-C1-S1 中通过 coverage/owner 讨论确认。
- **Skeleton labs/scripts**：复用 S2D-1A/S2D-1B 的脚本命名和 Evidence 口径，但允许内部逻辑先以 TODO/skip 或简单占位实现存在，只要能产出合法 `_result.json.ok` 与 `artifacts/s2d-runs.json` 记录即可。

## Constraints（约束）

- 不在本 phase 内强行完成该 legacy projection 的全部重构；重点是结构/命名统一，确保未来补齐实现时无需再改动入口或 Evidence 口径；
- 不修改现有 S2D-1A/S2D-1B onboarding 的语义或 artifacts；S2D-1C 只能在其基础上“复制/裁剪”，避免引入新的耦合；
- 所有新增加的 labs/scripts 默认只写入 dev/test 环境依赖；如需 database 访问，应沿用现有 devtest 配置，不引入额外的 secret/权限面；
- evidence JSON 必须保持机器可判定：至少包含 projection 标识、输入参数、run_dir/输出路径以及 `ok`/`reason` 字段，与 S6A-4A/S2C contract 兼容。

## Scope（本 log 范围）

- `P0`：contract & candidate selection（基于 coverage/owner 确定 S2D-1C 目标投影，并固化最小 skeleton contract + 证据口径）；
- `P1`：实现（在现有 S2C/S2D 框架上复制并裁剪 S2D-1A/S2D-1B 的 labs/scripts，形成新的 projection onboarding skeleton 占位）；
- `P2`：drills（在 dev/test 环境中至少跑通一次 skeleton labs/runner，哪怕是 "known red"，并记录 Evidence）；
- （可选）`P3`：小范围验证（根据需要，将该 skeleton 挂到 S2D-3A 的 SUITE_CATALOG 中作为 optional/experimental suite，观察 hard gate 行为，但不强制 green）。

## Success Criteria（DoD）

- 已在本 log 中明确记录 S2D-1C 目标投影的基本信息（projection 名称、当前 onboarding_status=legacy、owner 团队等），以及与 S2D-1A/S2D-1B 在维度/依赖上的主要差异；
- 代码仓库中存在一套与 S2D-1A/S2D-1B 类似的 labs/scripts 占位（例如 backfill smoke + correctness drill + onboarding package runner），命名和 artifacts 结构与前两条样本对齐；
- 至少 1 次 skeleton labs 在 dev/test 环境实际执行：
  - 即便结果为 red 或 `ok=false`，也能产出合法的 Evidence JSON（包含 projection_name、输入参数、run_dir、ok 字段）；
  - Evidence 记录在本 log 的 Evidence 区，便于后续追踪该 legacy projection 的 platformization 进度；
- 在 S2D spine 的 Current Status 中，可以用一句话解释“第三条 legacy projection 已经完成 onboarding skeleton 搭建，并具备按 S2D 模板继续演进的入口”，并提供链接指向本 log 与相关 labs/scripts。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0-P2 的 onboarding skeleton contract + 占位实现 + 至少 1 次 skeleton drills 已经跑通（可 red，可 partial），并具备可复跑的入口；
  - （若启用 P3）该 legacy projection 至少以 optional/experimental 形式被纳入 S2D-3A hard gate 套餐，并在 Evidence 中记录对应 suite_id 与 run artifacts；
  - Evidence 区有可追溯的 `headSha` + `run_id` + artifacts 路径（或 CI run URL）。

## P0（Contract｜v1）

### P0-C1-S1（Candidate selection & basic contract）

- 基于 S2D-2A onboarding coverage 首次快照 `artifacts/s2d-coverage-20260310-001.json`，当前 catalog 中共有 3 条投影，其中：
  - `chronicle_daily_stats`：`onboarding_status=platformized, onboarding_phase=S2D-1A`；
  - `chronicle_events_to_entries`：`onboarding_status=legacy`（已在 S2D-1B 中作为第二条 legacy projection 处理）；
  - `search_index_to_elastic`：`onboarding_status=legacy, onboarding_phase=none`；
- 为避免与 S2D-1B 重复，本 phase 选择 `search_index_to_elastic` 作为 S2D-1C 的目标 legacy projection：
  - 该 projection 负责将 search index 相关事件从统一 outbox 写入 Elastic（详见 S2B runbook 与现有 outbox 指标，如 `projection="search_index_to_elastic"` 的 processed/lag 系列）；
  - 目前运行路径仍然停留在 legacy worker + table merge 模式，尚未按 S2D onboarding contract 建立统一的 labs/runner 套餐；
- 在本 log 中将目标投影记为：
  - `projection_name=search_index_to_elastic`；
  - `onboarding_status=legacy`（来自 S2D-2A coverage）；
  - `owner_team` 暂记为 `TBD`（待与 search/infra 责任人确认后再在 catalog 中补齐），本 log 先聚焦技术侧 skeleton；
- 约定本投影在完全 platformize 之前的最小 skeleton 套餐为：
  - 一条 backfill smoke lab（最小范围写入/重建有限数量的 index 文档）；
  - 一条 correctness/harness drill（验证 outbox → Elastic 的端到端路径，初期可以只检查 events 计数/基础字段）；
  - 一条 onboarding package runner，将上述 labs 汇总为 `log_id="S2D-1C"` 的单条 suite，写入 `artifacts/s2d-runs.json` 供 S2D-2A/3A/6A 消费。

### P0-C1-S2（Skeleton fields & scripts contract）

- 为 `search_index_to_elastic` 这一目标投影约定 S2D-1C skeleton 的命名与脚本入口：
  - labs：
    - `backend/scripts/labs/s2d1c_search_index_to_elastic_backfill_smoke.py`
    - `backend/scripts/labs/s2d1c_search_index_to_elastic_harness_drill.py`
    - 两个脚本均接受 `--database-url/--run-id/--outdir` 参数，输出 `_result.json`，并在 devtest 环境下仅操作测试数据或受控时间窗；
  - onboarding runner：
    - `scripts/projections/s2d_1c_p2c1s2_third_onboarding_skeleton.py`
    - 负责按固定顺序调用上述两个 labs，并向 `artifacts/s2d-runs.json` 追加一条 `log_id="S2D-1C"` 的 summary 记录（`phase="P2"/cycle="C1"/step="S2"/run_id=<ts>`）；
  - Evidence JSON schema：
    - 复用 S2D-1A/S2D-1B 的结构：`log_id/phase/cycle/step/head_sha/run_id/database_url/ok/scenarios[]`，scenarios 中包含 `scenario_id/script/run_dir/ok/exit_code` 等字段；
    - scenario_id 建议固定为：`s2d1c_search_index_to_elastic_backfill_smoke` 与 `s2d1c_search_index_to_elastic_harness_drill`，便于后续在 S6A-4A 侧聚合。

### P0-C1-S3（证据口径 contract｜v1）

- evidence JSON 必须包含：
  - 输入参数：projection_name、租户/时间范围或等价 scope_keys、devtest DB URL；
  - 输出产物路径：每个 scenario 的 `run_dir`、onboarding runner 的 summary 记录在 `artifacts/s2d-runs.json` 中的位置；
  - PASS/FAIL 字段：scenario 级别与汇总级别的 `ok/exit_code/reason`，reason 需保持低基数，便于后续在 S6A-4A hard gate evidence JSON 中聚合。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2D-1C/P<phase>-C<cycle>-S<steps>: <summary>`，例如：`S2D-1C/P1-C1-S1: scaffold third projection onboarding skeleton labs`。

**Branch 约定**:

- S2D-1C 相关改动优先落在 `S2D-*` 前缀的工作分支（例如 `S2D-projection-onboarding-hard-gates`），便于与 S2D spine 聚合；
- 若一次 PR 同时涉及多个 scope/index（如 S2C 与 S2D），建议拆成多条 PR，每条聚焦一个 scope/index 与对应分支。

## Plan（draft）

### P1（实现：skeleton 落地）

- P1-C1-S1：基于 S2D-1C P0 合同，在 `backend/scripts/labs` 下复制并裁剪 S2D-1B 的 labs，生成 `s2d1c_*` skeleton 脚本，占位实现允许 `ok=false` 或 TODO；
- P1-C1-S2：在 `scripts/projections` 下新增 S2D-1C onboarding runner（例如 `s2d_1c_p2c1s2_third_onboarding_skeleton.py`），串联上述 labs 并写入一条 `log_id="S2D-1C"` 的 `artifacts/s2d-runs.json` 记录。

### P2（drill/verify：首轮 skeleton runs）

- P2-C1-S1：在 devtest 环境下执行 S2D-1C backfill smoke & correctness drill，占位实现可以 `ok=false`，但需保证 `_result.json` 与 run_dir 结构正确；
- P2-C1-S2：执行 S2D-1C onboarding runner，写入第一条 `S2D-1C` 记录到 `artifacts/s2d-runs.json`，并在本 log 的 Evidence 区登记 headSha/run_id/run_dir。
  
（C2：minimal real drills｜已完成）

- P2-C2-S1：在 devtest 环境实现并执行 `search_index_to_elastic` 的最小真实 backfill smoke（DB-only backfill → unified outbox），保证首轮插入 1 条 outbox、第二轮幂等；
- P2-C2-S2：在 devtest 环境实现并执行最小真实 harness drill（SearchOutboxRepository enqueue → unified outbox pending row），并通过 S2D-1C onboarding runner 记录一条 `cycle="C2"` 的绿灯 Evidence。

### P3（可选：hard gate 挂载）

- P3-C1-S1：视实际需要，在 `scripts/s2d_hard_gate.SUITE_CATALOG` 中为 S2D-1C 目标投影新增 optional/experimental suite，suite_id 命名与 S2D-1B 对齐；
- P3-C1-S2：在 CI 的 `s2d-hard-gate` workflow 中观察该 suite 的行为，视稳定性与业务优先级决定是否在后续 cycle 推进 C2/required 升级。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：基于 coverage/owner 选择 S2D-1C 目标 legacy projection 并在本 log 中记录基本信息与最小 skeleton 套餐 contract
- [x] `P0-C1-S2`：约定 labs/runner 命名与 Evidence JSON 字段口径
- [x] `P0-C1-S3`：补齐 evidence JSON 输入/输出/PASS-FAIL 字段 contract

### P1（实现：skeleton 落地）

- [x] `P1-C1-S1`：在 labs 目录中复制/裁剪 S2D-1B labs，生成 `s2d1c_*` skeleton 脚本（v1：backfill/harness skeleton，known red）
- [x] `P1-C1-S2`：新增 S2D-1C onboarding runner 并成功写入 `artifacts/s2d-runs.json`（v1：记录 skeleton 套餐，ok=false）

### P2（drill/verify：首轮 skeleton runs）

- [x] `P2-C1-S1`：在 devtest 环境执行 S2D-1C skeleton labs 并产出 `_result.json`（v1：known red，`ok=false`）
- [x] `P2-C1-S2`：在 devtest 环境执行 S2D-1C onboarding runner 并在本 log 记录 Evidence（v1：首条 skeleton 记录）
- [x] `P2-C2-S1`：在 devtest 环境实现并执行 S2D-1C C2 最小真实 backfill smoke（DB-only backfill → unified outbox），确保 outbox 插入/幂等行为符合预期（ok=true）
- [x] `P2-C2-S2`：在 devtest 环境实现并执行 S2D-1C C2 最小真实 harness drill + onboarding runner（cycle="C2"），记录一条 `ok=true` 的 S2D-1C Evidence

### P3（可选：hard gate 挂载）

- [ ] `P3-C1-S1`：如有需要，将 S2D-1C 套餐以 optional suite 形式挂到 S2D hard gate
- [ ] `P3-C1-S2`：在 CI 中观测该 optional suite 的行为并在本 log 中补充 Evidence

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（third projection skeleton drills｜YYYY-MM-DD）

- 日期：`2026-03-11`
- headSha：`469501f4beb81c291a62cbfcad8de88944650bbc`
- artifacts：
  - backfill skeleton：
    - 脚本：`backend/scripts/labs/s2d1c_search_index_to_elastic_backfill_smoke.py`
    - run_dir：`docs/labs/_snapshot/auto/s2d1c_search_index_to_elastic_backfill_smoke/20260311-151831`
  - harness skeleton：
    - 脚本：`backend/scripts/labs/s2d1c_search_index_to_elastic_harness_drill.py`
    - run_dir：`docs/labs/_snapshot/auto/s2d1c_search_index_to_elastic_harness_drill/20260311-151831`
- 期望（expected）：
  - skeleton drills 至少能够跑出 `_result.json.ok=false` + 低基数 failure reason；
  - artifacts 结构与 S2D-1A/S2D-1B 保持一致。
- 观测（observed）：
  - 在 devtest DB（`postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test`）下执行两条 skeleton labs：
    - 均成功在对应 run_dir 下生成 `_result.json`，字段包含 `ok=false`、`reason="skeleton_not_implemented_yet"` 与数据库 URL 等元信息；
    - run_exit_code 均为 2，符合 "known red skeleton" 预期。

### P2-C1-S2（third projection skeleton onboarding package｜YYYY-MM-DD）

- 日期：`2026-03-11`
- headSha：`469501f4beb81c291a62cbfcad8de88944650bbc`
- log_id/phase/cycle/step：`S2D-1C / P2 / C1 / S2`
- runner：`scripts/projections/s2d_1c_p2c1s2_third_onboarding_skeleton.py`
- runs：
  - C1（首跑，skeleton known red）：
    - run_id：`20260311-151831`
    - scenarios：
      - backfill smoke：`docs/labs/_snapshot/auto/s2d1c_search_index_to_elastic_backfill_smoke/20260311-151831`
      - correctness drill：`docs/labs/_snapshot/auto/s2d1c_search_index_to_elastic_harness_drill/20260311-151831`
    - summary：`artifacts/s2d-runs.json` 中新增一条记录（`log_id="S2D-1C"`，`phase="P2"`，`cycle="C1"`，`step="S2"`，`run_id="20260311-151831"`，`ok=false`，两个 scenario 均 `exit_code=2 && ok=false`，reason 为 `"skeleton_not_implemented_yet"`）。

### P2-C2-S1/S2（third projection minimal real drills｜2026-03-11）

- 日期：`2026-03-11`
- headSha：`8faa57e433f4e7025721c807ab6e4d003db39adc`
- log_id/phase/cycle/step：`S2D-1C / P2 / C2 / S2`
- runner：`scripts/projections/s2d_1c_p2c1s2_third_onboarding_skeleton.py`
- runs：
  - C2（C2 最小真实 drills，期望 green）：
    - run_id：`20260311-193445`
    - scenarios：
      - backfill smoke（minimal real）：`docs/labs/_snapshot/auto/s2d1c_search_index_to_elastic_backfill_smoke/20260311-193445`
      - harness drill（minimal real）：`docs/labs/_snapshot/auto/s2d1c_search_index_to_elastic_harness_drill/20260311-193445`
    - summary：`artifacts/s2d-runs.json` 中新增一条记录（`log_id="S2D-1C"`，`phase="P2"`，`cycle="C2"`，`step="S2"`，`run_id="20260311-193445"`，`ok=true`，两个 scenario 均 `exit_code=0 && ok=true`）。

## Recent changes（for traceability，可选）

- 2026-03-11：scaffold S2D-1C log，基于 S2D-1A/S2D-1B 的经验，为第三条 legacy projection onboarding skeleton 定义最小 contract/Plan，等待在 P0 阶段确认具体目标投影与 labs/runner 命名。
- 2026-03-11：完成 `search_index_to_elastic` 的 S2D-1C skeleton labs/runner 首次 devtest 演练（known red），在本 log 与 `artifacts/s2d-runs.json` 中记录 P2-C1-S1/S2 Evidence。
- 2026-03-11：为 `search_index_to_elastic` 补齐 S2D-1C C2 最小真实实现（DB-only backfill smoke + unified outbox harness drill），在 devtest 环境获得首条 `cycle="C2"` 绿灯 Evidence（backfill/harness 双场景 `ok=true`），并在本 log 记录 P2-C2-S1/S2 Evidence。