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
- P3-C1-S2：基于 `suggested_suite_catalog` 与现有 `SUITE_CATALOG` 做只读 diff 校验，输出 JSON 方便人工或 CI 检查当前 hard gate 配置是否与 coverage 视角一致；v1 通过 `backend/scripts/labs/s2d_2a_p3c1s2_diff_suite_catalog.py` 落地，仅打印 diff，不自动修改配置。
- P3-C2-S1：定义 diff 结果到 gate 策略的分类规则（contract），把 diff 拆成严重级别（info / warning / fail-candidate），并约定每一类在 CI 中的默认行为：
  - `extra_in_hard_gate`：视为 **info/warning 级别** —— hard gate 中存在但 coverage 中暂时没有出现的 suite（例如 legacy suite 尚未在 catalog 中打 tag，或临时实验 suite）；默认行为：仅在 CI log 与 diff JSON 中提示，不 gate；
  - `missing_in_hard_gate`：视为 **warning 级别（未来的 hard fail 候选）** —— coverage 认为某些 platformized projection 应当有对应 suite，但当前 `SUITE_CATALOG` 尚未配置；默认行为：在 CI 中打印明确的 warning 列表，提示“这些 projection 需要考虑纳入 required/新增 suite”；后续可以基于白名单/关键 projection 清单，将其中一部分升级为 hard fail；
  - `mismatched_entries`：视为 **高优先级 warning / fail-candidate** —— hard gate 中已有 suite，但 `log_id` 或 `required` 标记与 coverage 建议不一致；默认行为：在 CI 中高亮打印（带有 `suggested/current` 对比），仍保持 soft gate；后续可对关键 projection 的 mismatch 直接视为 hard fail；
  - 所有 diff 类型的最终 hard fail 策略，统一在 S2D-3A 的 P3-C2 中声明由 S2D spine 决策，不在本 log 中直接要求立即启用，以便为多投影扩展保留迭代空间。
- P3-C2-S2：在 CI/workflow 侧补充基于 diff 结果的策略 hook（例如在 `.github/workflows/s2d-hard-gate.yml` 中解析 diff JSON 的 `has_diff/missing_in_hard_gate/extra_in_hard_gate/mismatched_entries` 字段），v1 仅实现 soft gate：
  - 当 `missing_in_hard_gate` 或 `mismatched_entries` 非空时，在 CI 日志中打印带前缀的 warning（例如 `[S2D-2A][warning] missing_in_hard_gate=...`）；
  - 保持 diff helper 本身 `exit_code=0`，不改变 `hard_gate` job 的整体退出码，只作为 guardrail 提示；
  - 后续 cycle 再按 S2D-3A/P3-C2-S1 中的规则选择性将特定 diff 类型升级为 hard fail。

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
- [x] `P3-C1-S2`：实现 coverage → SUITE_CATALOG diff 校验 helper（`backend/scripts/labs/s2d_2a_p3c1s2_diff_suite_catalog.py`），基于首个 coverage 快照对比 `suggested_suite_catalog` 与现有 `SUITE_CATALOG`，并记录 Evidence
 - [x] `P3-C2-S1`：梳理并固化 diff 结果分类与 gate 策略 contract（diff 类型 → 严重级别 → 默认 CI 行为），作为后续启用 warning/hard fail 的前置约定
 - [ ] `P3-C2-S2`：在 CI/workflow 中落地基于 diff 结果的 warning/soft gate 逻辑，并视需要在后续 cycle 升级为 hard gate

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

### P3-C1-S2（coverage vs SUITE_CATALOG diff helper｜2026-03-10）

- headSha：`e89a031df79e52ffbf977c7dc227e56142758c7a`
- scripts：`backend/scripts/labs/s2d_2a_p3c1s2_diff_suite_catalog.py`
- 输入 artifacts：`artifacts/s2d-coverage-20260310-001.json`
- 期望（expected）：
  - helper 读取 coverage JSON 并基于与 P3-C1-S1 相同的规则重建 `suggested_suite_catalog`；
  - 能从 `scripts/s2d_hard_gate.py` 中导入当前 `SUITE_CATALOG`，并计算出缺失、新增或配置不一致的 suite 列表；
  - 首次运行时，由于目前只有一条示例 suite，预期 `has_diff=false`，`missing_in_hard_gate/extra_in_hard_gate/mismatched_entries` 均为空。
- 观测（observed）：
  - 2026-03-10 在仓库根目录执行 `python backend/scripts/labs/s2d_2a_p3c1s2_diff_suite_catalog.py --coverage-path artifacts/s2d-coverage-20260310-001.json`，脚本成功解析 coverage JSON 并导入 `scripts.s2d_hard_gate.SUITE_CATALOG`；
  - 输出 JSON 中 `suggested_suite_catalog` 与 `current_suite_catalog` 都为 `{ "s2d-1a-sample-onboarding": {"log_id": "S2D-1A", "required": true} }`，`has_diff=false`，`missing_in_hard_gate=[]`，`extra_in_hard_gate=[]`，`mismatched_entries={}`；
  - helper 以只读方式工作，返回码为 0，后续可以在 CI 中将 `has_diff=true` 视为 warning 或手动 review 的信号。

## Recent changes（for traceability，可选）

- 2026-03-10：scaffold S2D-2A log，定义 onboarding coverage metrics & catalog rules 的 contract 与计划，等待后续 P1/P2/P3 实现。
- 2026-03-10：完成 P1/P2 实现与 Evidence 记账，并在 P3-C1-S1 中引入基于 coverage JSON 的 SUITE_CATALOG 建议 helper（`backend/scripts/labs/s2d_2a_p3c1s1_suggest_suite_catalog.py`）。
- 2026-03-10：完成 P3-C1-S2 diff helper 实现与首轮运行，校验 coverage 视角与现有 SUITE_CATALOG 一致，并将结果记录在本 log 的 Evidence 区。
