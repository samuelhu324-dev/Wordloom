# log-S2D-projection-onboarding-hard-gates（S2D：Projection onboarding hard gates / adoption）

---

**id**: `S2D-projection-onboarding-hard-gates`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection onboarding hard gates (templates adoption + CI) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S2D`
**tags**: `EVOLUTION, Projection, Platform, HardGate, Drills, Evidence, epic/s2d, sub/0`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: `docs/ROADMAP.md`
  **reference_log_1**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_2**: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
  **phase_log_1**: `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
  **phase_log_2**: ``
  **phase_log_3**: `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`
**created**: `2026-03-08`
**updated**: `2026-03-09`

---

## Decision / Outcome（结论区）

**Decision**:

- 在现有 S2C Projection 平台（spec/registry/harness/templates）的基础上，引入一条独立的 `S2D` epic，专门负责“新增/迁移 projection 的 onboarding contract + drills + CI hard gate”。
- 把路线 A 的 DoD 具体化为：任何标记为 platformized 的 projection，都必须通过统一的 spec + adapter.apply + writer + rebuild/backfill smoke + drills + CI hard gate 路径落地，并由 Evidence 记账。

**Default choices（默认基线 / v1）**:

- 环境以 dev/test 为主，复用现有 outbox devtest DB 与 projection harness，不直接触碰生产投影流量。
- 优先在新投影上强制执行 S2D onboarding contract，已有 legacy 投影允许通过标签区分，逐步迁移而非一次性推倒。
- Evidence 与 hard gate 复用 S6A-4A/S2C 的 JSON contract：`_recipe.json/_result.json/_metrics/*.json` + `artifacts/s2d-runs.json` 为事实源。

## Background（背景）

- S2C 已经把 Projection 平台化的“框架骨架”搭好：有统一的 `ProjectionSpec`、worker harness、writer/rebuild/backfill/drills 模板以及 Search harness migration 记录；但“是否真的按模板新增 projection”目前更多依赖工程自觉和 code review。
- 随着投影数量增加，如果新增 projection 仍然允许手搓 worker 循环或跳过 rebuild/backfill/drills，将导致运行特性与运维契约漂移（难以排障，也难以做全局 hard gate）。
- S2D 的目标是把这件事产品化：像 S5B 之于 S5A 一样，为 Projection 引入一条 onboarding hard gate spine，让“新增/迁移 projection 是否合规”可以被 CI 机械判定。

## Constraints（约束）

- 不破坏 S2B/S2C 已有稳定面：既有 stable entrypoints（scripts/runbook/workflows）不随意改名；迁移时优先通过 shim 和新入口并存的方式推进。
- 不改变 outbox payload contract 与 failure taxonomy：S2D 只能在现有 contract 上增加校验/模板，不能引入新的高基数 reason 或不兼容字段。
- S2D 的 hard gate 以 dev/test 环境为事实源，Evidence JSON 必须可被脚本和 CI 机械判定（PASS/FAIL），不依赖人工解释日志。

## Scope（本 log 范围）

- 本 log 负责：
  - 定义 `S2D` 的目标边界、默认基线、Phase 拆分与里程碑清单（execution checklist）。
  - 作为 Route A 在“onboarding + hard gate”维度的 spine log，索引到各个 phase log（例如 `S2D-1A`）。
- 本 log 不负责：
  - 具体某条 projection 的业务逻辑细节；
  - S2C 框架自身的实现演进（落在现有 S2C-* 子 log 中）。

## Success Criteria（DoD）

- 结构层面：
  - 读者 30 秒内能理解：S2D 要解决什么问题、目前哪些 projection 已经按 S2D onboarding 落地、下一条示范链路是哪一条。
  - 从本 log 的 links/index 能跳转到 S2C 框架说明、S2D-1A 等 phase log，以及对应 runbook / hard gate 入口脚本。
- 工程层面：
  - 至少 1 条示范 projection（S2D-1A）完整走通 S2D onboarding 流程：spec + adapter.apply + writer + rebuild/backfill smoke + drills + catalog 注册。
  - Projection harness 与 writer 在运行时会校验 schema_version/scope_keys/requires 等关键字段，新增 projection 即使代码能编译，若不满足 contract 也会在 dev/test 立即 FAIL。
  - 对标记为 platformized 的 projection，可以通过单命令或 CI workflow 复跑最小 rebuild/backfill/drills 套餐，并得到 PASS/FAIL 结果。
- 证据层面：
  - 每个 S2D phase 至少 1 条 Evidence 记录：`headSha + suite_id + run_dir` 或 CI run URL，落在本 log 的 Evidence 区。
  - 至少 1 条 S2D 专属 hard gate workflow 在 CI 中启用，并有一次 green run 被记账到 `artifacts/s2d-runs.json`。

## Phases（切片）

- `S2D-1A`（Phase 1）：Projection onboarding contract + first sample projection（用一条新投影跑通 S2D onboarding 全链路）
  - 详见：`docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
- `S2D-2A`（Phase 2，预留）：Onboarding coverage metrics & catalog rules（统计多少 projection 已按 S2D 落地，并在 catalog 中收紧规则）
  - 详见：`docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`（预留）
- `S2D-3A`（Phase 3）：S2D hard gate entrypoint & CI wiring（把 S2D onboarding 检查挂到统一 hard gate 和 CI workflow）
  - 详见：`docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：S2D contract/indexing（目标边界 + 默认基线 + links/index）
- [x] `P1`：Phase 1（projection onboarding contract + first sample projection 落地）
- [ ] `P2`：Phase 2（onboarding coverage & catalog 规则；区分 legacy vs platformized）
- [ ] `P3`：Phase 3（S2D hard gate 入口脚本 + CI workflow）

## Evidence（示范 Phase 记录）

- `2026-03-09` / Phase 1（S2D-1A sample projection onboarding package 首次 run）
  - headSha：`6513ebf4997e488385ce3074c93aadd284fa17af`
  - log_id/phase/cycle/step：`S2D-1A / P3 / C1 / S1`
  - run_id：`20260309-160839`
  - artifacts：
    - `docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_backfill_smoke/20260309-160839`
    - `docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_harness_drill/20260309-160839`
    - 汇总记录：`artifacts/s2d-runs.json`（首条记录，`ok=false`，两个 scenario 均失败）
  - 说明：
    - 本次为 S2D-1A onboarding 套餐脚本的首次集成运行，成功写入 Evidence JSON；
    - 运行结果为 red（`ok=false`），失败原因为 harness drill 在导入 `api.app.shared.deps`/`api.app.config.security` 时触发 circular import（`ImportError: cannot import name 'get_db' ...`）。

## Current Status（进展摘要）

- S2C 已经提供 spec/registry/harness/writer/rebuild/backfill/drills 模板以及 Search harness migration，具备 Route A 的平台化前置条件，但缺少“新增 projection 必须按模板 & 有 CI gate”的约束层。
- S2D-1A 已在代码与文档层面完成 P0-P3：定义 onboarding contract、接入 sample projection（`chronicle_daily_stats`）、补齐 drills/labs，并提供单命令 onboarding 套餐脚本与 runbook。
- 2026-03-09 已通过 `scripts/projections/s2d_1a_p3c1s1_sample_onboarding.py` 在 devtest DB 上完成首次 Phase 1 onboarding 套餐运行，并将结果写入 `artifacts/s2d-runs.json`；本次 run 为 red（`ok=false`），失败原因为 harness drill 触发 `api.app.shared.deps`/`api.app.config.security` 之间的 circular import（`ImportError: cannot import name 'get_db'`）。
- 后续 S2D-1A/S2D-3A 需要在修复该 circular import 并获得首个 green run 后，进一步把 S2D onboarding 套餐挂载到统一 hard gate / CI workflow 上。

## Notes（落地原则）

- 优先让 onboarding contract 与 hard gate 在“新投影”上先行收紧，避免对现有业务投影造成大面积回归压力；legacy 投影可以通过标签和 skip 机制过渡。
- 所有与 S2D 相关的脚本和 workflow，命名应尽量保持稳定且显式（例如 `s2d_*` 前缀），方便后续在 S0D/S6A 的 automation log 中引用。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - S2D 的默认基线、Phase 拆分与 Evidence 口径已稳定；
  - 至少 `S2D-1A` 已完成示范 projection 的 onboarding 全链路，并有一条 S2D hard gate workflow 的 green run 记录在 Evidence 区。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`S2D-<phase>/P<phase>-C<cycle>-S<steps>: <summary>`；
  - 例如：`S2D-1A/P0-C1-S1: scaffold onboarding contract log`。
- 分支约定：
  - 与 S2D 相关的改动优先落在 `S2D-*` 前缀的工作分支（例如 `S2D-projection-onboarding-hard-gates`），便于后续聚合与回溯；
  - 若一次改动同时涉及多个 scope/index（如 S2C 与 S2D），推荐拆成多条 PR，每条聚焦一个 scope。

## Recent changes（for traceability，可选）

- 2026-03-08：scaffold S2D spine log，定义 Projection onboarding hard gates 的目标/基线/Phase 切分。
