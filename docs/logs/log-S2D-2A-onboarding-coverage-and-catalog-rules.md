# log-S2D-2A-onboarding-coverage-and-catalog-rules（Phase 2：Onboarding coverage metrics & catalog rules）

---

**id**: `S2D-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `onboarding coverage metrics & catalog rules (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S2D`
**tags**: `EVOLUTION, Projection, Onboarding, Catalog, Drills, Evidence, epic/s2d, sub/2`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2D-projection-onboarding-hard-gates.md`
  **previous_log**: `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
  **reference_log_1**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_2**: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
**created**: `2026-03-10`
**updated**: `2026-03-10`

---

## Decision / Outcome（结论区）

**Decision**:

- 为 S2D 定义一套“onboarding coverage & catalog 规则”：在 projection catalog 中显式标记哪些投影已经按 S2D onboarding 落地（platformized），哪些仍为 legacy/experimental。
- 提供可重复的 drills/queries，用 JSON/SQL 方式统计 onboarding 覆盖率，并为 S2D hard gate（S2D-3A）提供 required/optional suites 的决策依据。

**Default choices（本 phase 默认决策 / v1）**：

- 以 dev/test catalog 为主（例如 projection registry / catalog tables），优先在非生产环境中验证规则与查询口径。
- 首批仅覆盖少量示范投影（例如 S2D-1A 的 sample projection），其余投影默认视为 legacy 或 optional，不强行纳入 required 集。
- 覆盖率计算口径尽量简单、可机械判定：例如“满足 onboarding contract + drills + 在 catalog 中标记为 platformized”即可认定为已 onboarding。

## Definitions（概念定义）

- **Platformized projection**：在 S2C/S2D 框架下，满足 onboarding contract、具备 drills/CI hard gate，并在 catalog 中显式标记为 platformized 的 projection。
- **Legacy projection**：尚未按 S2D onboarding contract 重构的既有 projection，可以通过 skip/waiver 机制暂时绕过 hard gate。
- **Coverage metrics**：用于衡量 onboarding 进度的度量，例如“platformized 投影数量 / 全部投影数量”、“按业务域/团队的覆盖率”等。

## Constraints（约束）

- 不直接修改生产 catalog 的语义；v1 仅在 dev/test 或 shadow catalog 中试跑规则与统计口径。
- 覆盖率口径必须与 S2D-1A/S2D-3A 的 contract 保持一致：只认“真的按 S2D onboarding 跑通并有 Evidence 记账”的 projection，不接受手动勾选。
- 所有关联脚本与查询应能通过单命令或 notebook 复跑，输出 JSON/表格，便于在 S0D/S6A 的汇总报表中引用。

## Scope（本 log 范围）

- `P0`：contract（定义 onboarding coverage 的统计口径、catalog 标记字段与 JSON/SQL 输出结构）。
- `P1`：implementation（在 catalog/registry 层面补充标记字段与查询脚本）。
- `P2`：drills（在 dev/test 环境定期跑 coverage drills，并记录 Evidence）。
- `P3`：integration（将 coverage 结果回填到 S2D-3A 的 SUITE_CATALOG / hard gate 默认 required 集中）。

## Success Criteria（DoD）

- 有一份明确的 onboarding coverage contract：
  - catalog 中用于标记 platformized/legacy 的字段或标签约定；
  - 至少 1 条用于统计覆盖率的 SQL/JSON 查询模板；
  - 输出 schema 能够被 S0D/S6A 的报表或自动化消费。
- 至少 1 次 coverage drill 在 dev/test 环境成功执行：
  - 能枚举出 S2D-1A sample projection 这一条 platformized projection；
  - 对其它 projection 给出明确的 legacy/unknown 状态。
- Evidence 区记录至少 1 条 coverage drill run：包含 headSha、查询脚本/路径、输出 JSON 或快照路径。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0-P2 的 coverage contract + catalog 字段 + drills 已经稳定，并可通过单命令复跑；
  - P3 已将 coverage 结果集成进 S2D-3A 的 required/optional suites 决策流程（例如自动生成 SUITE_CATALOG 或校验配置）。

## P0（Contract｜v1）

### P0-C1-S1（Catalog 标记与枚举规则）

- 在 projection catalog/registry 中为每条 projection 增加 S2D 相关标记字段（示意）：
  - `onboarding_status`：`platformized | legacy | experimental | unknown`；
  - `onboarding_phase`：`S2D-1A | S2D-2A | S2D-3A | none`；
  - `owner_team`：可选，用于按团队维度汇总覆盖率。
- 规定“认定为 platformized”的最小条件：
  - 具备 S2D-1A 要求的 onboarding contract（spec/adapter/writer/rebuild/backfill/drills）；
  - 在 S2D-1A/S2D-3A 的 Evidence 中出现过至少 1 条 green run 记录；
  - catalog 中 `onboarding_status=platformized`。

### P0-C1-S2（Coverage metrics & 输出 schema）

- 定义最小 coverage metrics：
  - `total_projections`：catalog 中全部投影数量；
  - `platformized_projections`：`onboarding_status=platformized` 的投影数量；
  - `legacy_projections`：`onboarding_status=legacy` 的投影数量；
  - 以及可选的按业务域/团队聚合指标。
- 约定 coverage drill 的 JSON 输出 schema（示意）：
  - `generated_at`：UTC 时间戳；
  - `total_projections` / `platformized_projections` / `legacy_projections`；
  - `by_team`：按团队聚合的覆盖率列表；
  - `projections`：每条投影的 `name/onboarding_status/onboarding_phase/owner_team` 摘要列表。

### P0-C1-S3（Evidence JSON contract）

- 每次 coverage drill 至少需要写出：
  - 1 份 JSON 快照文件（例如 `artifacts/s2d-coverage-YYYYMMDD-HHMMSS.json`），包含上述 schema；
  - 可选的表格/metrics 导出（例如 CSV 或 metrics 表）。
- Evidence 记录需包含：headSha、drill 脚本路径、输出 JSON 路径，以及 key metrics 的摘要（例如 platformized 数量）。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2D-2A/P<phase>-C<cycle>-S<steps>: <summary>`，例如：`S2D-2A/P0-C1-S1: scaffold onboarding coverage contract`。

## Plan（draft）

### P1（Implementation：catalog 字段与查询脚本）

- P1-C1-S1：在 projection catalog/registry 中增加 `onboarding_status/onboarding_phase/owner_team` 字段或标签，并为现有 sample projection（chronicle_daily_stats）写入 `platformized` 标记；v1 通过 `backend/infra/projection_framework/catalog.py` 中的 `ProjectionCatalogEntry` 与 `build_catalog_entries()` 落地，默认将 `chronicle_daily_stats` 标记为 `onboarding_status=platformized, onboarding_phase=S2D-1A`，其余注册投影默认为 `legacy/none`。
- P1-C1-S2：新增 1~2 条 SQL/JSON 查询脚本，用于导出 coverage metrics 与逐 projection 摘要；v1 通过 `backend/scripts/labs/s2d_2a_p1c1s2_dump_coverage.py` 实现，调用 `compute_coverage_snapshot()` 输出符合本 log contract 的 JSON（可输出到 stdout，亦可通过 `--output` 写入文件）。

### P2（Drills：定期 coverage 统计）

- P2-C1-S1：在 devtest 环境运行 coverage drill（例如 `scripts/labs/s2d_2a_p2c1s1_coverage_snapshot.py`），产出 `artifacts/s2d-coverage-*.json`。
- P2-C1-S2：为 coverage drill 增加简单的 CI 或定时任务入口（可选），并在本 log 的 Evidence 区记录首次 run。

### P3（Integration：回填 hard gate 决策）

- P3-C1-S1：定义从 coverage JSON 映射到 S2D-3A `SUITE_CATALOG` 的规则，并提供一个小 helper/脚本用于生成建议集；v1 规则为：
  - 仅考虑 coverage JSON 中 `onboarding_status=platformized` 的 projection；
  - 使用静态映射 `projection_name → suite_id/log_id`，目前只支持 S2D-1A 的示例投影 `chronicle_daily_stats → {suite_id="s2d-1a-sample-onboarding", log_id="S2D-1A"}`；
  - 对于未出现在静态映射中的 platformized 投影，先不自动生成 suite，仅在后续演进中扩展映射表；
  - helper 输出的结构为 `suggested_suite_catalog` JSON 片段，供人工或后续 phase 回填到 `scripts/s2d_hard_gate.py` 的 `SUITE_CATALOG` 中；v1 通过 `backend/scripts/labs/s2d_2a_p3c1s1_suggest_suite_catalog.py` 落地。
- P3-C1-S2：在后续 phase（或 S2D-3A 的演进）中，将 coverage 结果实际接入 hard gate 配置（例如：对照 `suggested_suite_catalog` 与现有 `SUITE_CATALOG` 做 diff，自动/半自动地收紧 required 集），本 log 仅定义 contract 与计划。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 catalog 标记字段与 platformized/legacy 枚举规则
- [x] `P0-C1-S2`：定义 coverage metrics 与 JSON 输出 schema
- [x] `P0-C1-S3`：定义 coverage drill 的 Evidence JSON contract

### P1（Implementation：catalog & queries）

- [x] `P1-C1-S1`：在 catalog/registry 中增加字段/标签并填充示例数据（v1：`backend/infra/projection_framework/catalog.py` 中落地 `ProjectionCatalogEntry` + `build_catalog_entries()`，为 `chronicle_daily_stats` 写入 `platformized/S2D-1A` 示例，其余投影默认为 `legacy/none`）
- [x] `P1-C1-S2`：实现导出 coverage metrics 的查询脚本（v1：`backend/scripts/labs/s2d_2a_p1c1s2_dump_coverage.py` 调用 `compute_coverage_snapshot()` 输出 JSON）

### P2（Drills）

- [x] `P2-C1-S1`：实现并跑通首个 coverage drill，产出 JSON 快照（v1：通过 `s2d_2a_p1c1s2_dump_coverage.py` 在 devtest 环境生成 `artifacts/s2d-coverage-20260310-001.json`）
- [x] `P2-C1-S2`：在本 log 的 Evidence 区记录 coverage drill 首次 run（见下方 `P2-C1-S1` Evidence 条目）

### P3（Integration）

- [x] `P3-C1-S1`：定义 coverage → hard gate 决策映射规则的具体实现方案，并提供 v1 helper 脚本（`backend/scripts/labs/s2d_2a_p3c1s1_suggest_suite_catalog.py`）从 coverage JSON 生成 `suggested_suite_catalog` 片段
- [ ] `P3-C1-S2`：在后续 phase 中将 coverage 结果写回 S2D-3A 的 SUITE_CATALOG/配置

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（onboarding coverage drill snapshot｜2026-03-10）

- headSha：`7784e72b2f46bcefa7886ecea8644bb599172e26`
- artifacts：`artifacts/s2d-coverage-20260310-001.json`
- 期望（expected）：
  - coverage snapshot JSON 至少包含 1 条 platformized projection（例如 S2D-1A 的 sample projection `chronicle_daily_stats`），其余 projection 标记为 legacy/unknown；
  - 输出中包含 `total_projections/platformized_projections/legacy_projections/by_team/projections` 等字段，满足本 log P0 约定的 schema。
- 观测（observed）：
  - 2026-03-10 在 devtest 环境执行 `python backend/scripts/labs/s2d_2a_p1c1s2_dump_coverage.py --output artifacts/s2d-coverage-20260310-001.json`，脚本内部调用 `compute_coverage_snapshot()` 并成功连接 devtest 数据库；
  - JSON 输出显示 `total_projections=3`，其中 `platformized_projections=1`、`legacy_projections=2`，by_team 维度下 `data-platform` 拥有 1 条 platformized 投影，其余 2 条投影归类为 `legacy/unknown`；
  - projections 列表中明确包含 `chronicle_daily_stats` （`onboarding_status=platformized, onboarding_phase=S2D-1A`）以及 `chronicle_events_to_entries`、`search_index_to_elastic` 两条 legacy 投影，符合 P2 的预期。

### P3-C1-S1（coverage → SUITE_CATALOG 建议 helper｜2026-03-10）

- headSha：`c68ab2288a10bbafa945e588dbb99ab01abf597b`
- scripts：`backend/scripts/labs/s2d_2a_p3c1s1_suggest_suite_catalog.py`
- 输入 artifacts：`artifacts/s2d-coverage-20260310-001.json`
- 期望（expected）：
  - helper 仅基于 coverage JSON 中 `onboarding_status=platformized` 的 projection 给出 suite 建议；
  - 对于 S2D-1A 示例投影 `chronicle_daily_stats`，能生成与现有 hard gate 一致的 SUITE_CATALOG 片段：`{"s2d-1a-sample-onboarding": {"log_id": "S2D-1A", "required": true}}`；
  - 输出结果以 JSON 形式给出 `platformized_projections` 与 `suggested_suite_catalog`，便于后续与 `scripts/s2d_hard_gate.py` 的配置做 diff。
- 观测（observed）：
  - 2026-03-10 在仓库根目录执行 `python backend/scripts/labs/s2d_2a_p3c1s1_suggest_suite_catalog.py --coverage-path artifacts/s2d-coverage-20260310-001.json`，脚本成功读取首个 coverage 快照并识别出 1 条 platformized 投影 `chronicle_daily_stats`；
  - 输出 JSON 中 `platformized_projections=["chronicle_daily_stats"]`，`suggested_suite_catalog` 为 `{ "s2d-1a-sample-onboarding": {"log_id": "S2D-1A", "required": true} }`，与现有 `scripts/s2d_hard_gate.py` 中的 SUITE_CATALOG 配置保持一致；
  - `suggestions` 列表给出按 projection 维度的说明字段（projection_name/suite_id/log_id/reason），作为后续扩展更多投影映射规则的基础。

## Recent changes（for traceability，可选）

- 2026-03-10：scaffold S2D-2A log，定义 onboarding coverage metrics & catalog rules 的 contract 与计划，等待后续 P1/P2/P3 实现。
- 2026-03-10：完成 P1/P2 实现与 Evidence 记账，并在 P3-C1-S1 中引入基于 coverage JSON 的 SUITE_CATALOG 建议 helper（`backend/scripts/labs/s2d_2a_p3c1s1_suggest_suite_catalog.py`）。
