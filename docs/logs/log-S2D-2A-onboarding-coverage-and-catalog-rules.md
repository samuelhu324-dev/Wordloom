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

- P1-C1-S1：在 projection catalog/registry 中增加 `onboarding_status/onboarding_phase/owner_team` 字段或标签，并为现有 sample projection（chronicle_daily_stats）写入 `platformized` 标记。
- P1-C1-S2：新增 1~2 条 SQL/JSON 查询脚本，用于导出 coverage metrics 与逐 projection 摘要。

### P2（Drills：定期 coverage 统计）

- P2-C1-S1：在 devtest 环境运行 coverage drill（例如 `scripts/labs/s2d_2a_p2c1s1_coverage_snapshot.py`），产出 `artifacts/s2d-coverage-*.json`。
- P2-C1-S2：为 coverage drill 增加简单的 CI 或定时任务入口（可选），并在本 log 的 Evidence 区记录首次 run。

### P3（Integration：回填 hard gate 决策）

- P3-C1-S1：定义从 coverage JSON 映射到 S2D-3A `SUITE_CATALOG` 的规则，例如：哪些 projection 需要新增 suite，哪些可以继续作为 optional/legacy。
- P3-C1-S2：在后续 phase（或 S2D-3A 的演进）中，将 coverage 结果实际接入 hard gate 配置（本 log 仅定义 contract 与计划）。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 catalog 标记字段与 platformized/legacy 枚举规则
- [x] `P0-C1-S2`：定义 coverage metrics 与 JSON 输出 schema
- [x] `P0-C1-S3`：定义 coverage drill 的 Evidence JSON contract

### P1（Implementation：catalog & queries）

- [ ] `P1-C1-S1`：在 catalog/registry 中增加字段/标签并填充示例数据
- [ ] `P1-C1-S2`：实现导出 coverage metrics 的查询脚本

### P2（Drills）

- [ ] `P2-C1-S1`：实现并跑通首个 coverage drill，产出 JSON 快照
- [ ] `P2-C1-S2`：在本 log 的 Evidence 区记录 coverage drill 首次 run

### P3（Integration）

- [ ] `P3-C1-S1`：定义 coverage → hard gate 决策映射规则的具体实现方案
- [ ] `P3-C1-S2`：在后续 phase 中将 coverage 结果写回 S2D-3A 的 SUITE_CATALOG/配置

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（onboarding coverage drill snapshot｜YYYY-MM-DD）

- headSha：`<git sha>`
- artifacts：`artifacts/s2d-coverage-YYYYMMDD-HHMMSS.json`
- 期望（expected）：
-  - 至少包含 1 条 platformized projection（例如 S2D-1A 的 sample projection），其余 projection 标记为 legacy/unknown；
- 观测（observed）：
-  - （首轮 run 完成后补充）。

## Recent changes（for traceability，可选）

- 2026-03-10：scaffold S2D-2A log，定义 onboarding coverage metrics & catalog rules 的 contract 与计划，等待后续 P1/P2/P3 实现。
