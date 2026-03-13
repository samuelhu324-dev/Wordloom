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
  **phase_log_2**: `docs/logs/log-S2D-1B-projection-onboarding-skeleton-second-sample.md`
  **phase_log_3**: `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`
  **phase_log_4**: `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`
  **phase_log_5**: `docs/logs/log-S2D-1C-projection-onboarding-skeleton-third-sample.md`
**created**: `2026-03-08`
**updated**: `2026-03-11`

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
- `S2D-1B`（Phase 1B）：Second projection onboarding skeleton for legacy → platformized（为一条 legacy 投影搭建与 S2D-1A 同结构的 onboarding skeleton，占位即可）
  - 详见：`docs/logs/log-S2D-1B-projection-onboarding-skeleton-second-sample.md`
 - `S2D-1C`（Phase 1C）：Third projection onboarding skeleton for legacy → platformized（为第三条 legacy projection 搭建与 S2D-1A/S2D-1B 同结构的 onboarding skeleton，并为后续批量迁移提供可复制模板）
   - 详见：`docs/logs/log-S2D-1C-projection-onboarding-skeleton-third-sample.md`
- `S2D-2A`（Phase 2）：Onboarding coverage metrics & catalog rules（统计多少 projection 已按 S2D 落地，并在 catalog 中收紧规则）
  - 详见：`docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`
- `S2D-3A`（Phase 3）：S2D hard gate entrypoint & CI wiring（把 S2D onboarding 检查挂到统一 hard gate 和 CI workflow）
  - 详见：`docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：S2D contract/indexing（目标边界 + 默认基线 + links/index）
- [x] `P1`：Phase 1（projection onboarding contract + first sample projection 落地）
- [x] `P2`：Phase 2（onboarding coverage & catalog 规则；区分 legacy vs platformized，首次 coverage drill 已在 devtest 环境跑通，详见 `log-S2D-2A-onboarding-coverage-and-catalog-rules.md`）
- [x] `P3`：Phase 3（S2D hard gate 入口脚本 + CI workflow + 基本 adoption/skip/waiver 规则）

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

- `2026-03-09` / Phase 3（S2D-3A local hard gate dry run）
  - headSha：`2fd5d5e8bfb92c2ca92c12bcdc2d27ac0058badf`
  - log_id/phase/cycle/step：`S2D-3A / P1 / C1 / S1`
  - runner：`scripts/s2d_hard_gate.py`
  - run_id：`20260309-194740`
  - artifacts：
    - 汇总记录：`artifacts/s2d-runs.json`（追加记录，`log_id="S2D-1A"`，`run_id="20260309-194740"`，`ok=true`）
    - backfill smoke：`docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_backfill_smoke/20260309-194740`
    - harness drill：`docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_harness_drill/20260309-194740`
  - 说明：
    - 通过 `python scripts/s2d_hard_gate.py --database-url $DATABASE_URL` 在 devtest DB 下调用 S2D-1A onboarding 套餐，完成首个 green dry run；
    - hard gate 根据 `artifacts/s2d-runs.json` 中的记录计算 `overall_ok=true` 并以 `exit_code=0` 结束，为后续 CI hard gate 提供本地基线。

- `2026-03-09 ~ 2026-03-10` / Phase 3（S2D-3A CI hard gate workflow red → green）
  - log_id/phase/cycle/step：`S2D-3A / P2 / C1 / S1`
  - 首轮 CI run（red）：
    - headSha：`5ccf5bb96fd6669282ddc46079414b3e942d8c88`
    - CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22852965555`
    - 说明：首轮 `s2d-hard-gate` workflow 在 Start DB / artifacts 上传阶段失败，未能产出预期的 `_snapshot/auto` 与 `artifacts/s2d-runs.json`，`hard_gate` job `exit_code=2`。
  - first green CI run：
    - headSha：`894e6bad7554f53ae9ac39bc6770b256568ea271`
    - CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22853943302`
    - artifacts：`s2d-hard-gate-22853943302-1`（包含本次 hard gate 运行生成的 `_snapshot/auto/...` 与 `artifacts/s2d-runs.json` 片段）
    - 说明：修复 DB wait loop 语法后，`s2d-hard-gate` workflow 在 CI 中成功跑通，完成首个 green CI hard gate run，并作为后续扩展多投影时的基线样板；具体细节见 `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md` 的 Evidence 区。

- `2026-03-10` / Phase 2（S2D-2A onboarding coverage drill 首次快照）
  - headSha：`7784e72b2f46bcefa7886ecea8644bb599172e26`
  - log_id/phase/cycle/step：`S2D-2A / P2 / C1 / S1`
  - runner：`backend/scripts/labs/s2d_2a_p1c1s2_dump_coverage.py`
  - artifacts：`artifacts/s2d-coverage-20260310-001.json`
  - 说明：在 devtest 环境运行 coverage drill，基于 `compute_coverage_snapshot()` 生成首个 onboarding coverage JSON 快照，枚举出 1 条 platformized projection（`chronicle_daily_stats`）与 2 条 legacy 投影，详细 Evidence 见 `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`。

- `2026-03-11` / Phase 1C（S2D-1C optional suite：devtest → CI）
  - headSha：`f34585ce1a8a9dfeb40bbca9c18b3b5fb2a0d5c2`
  - log_id/phase/cycle/step：`S2D-1C / P3 / C1 / S2`
  - suite_id：`s2d-1c-third-onboarding-minimal-real`（`required=false`）
  - devtest hard gate run：
    - runner：`scripts/s2d_hard_gate.py`
    - 参数：`--database-url postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test --suite s2d-1c-third-onboarding-minimal-real`
    - 概要：在 devtest DB 下通过 hard gate 调用 S2D-1C onboarding runner，backfill/harness 两个 minimal real drills 均 `ok=true && exit_code=0`，`artifacts/s2d-runs.json` 中追加一条 `log_id="S2D-1C"` 的 green 记录，`suite.required=false`，`overall_ok=true`；详细 Evidence 见 `docs/logs/log-S2D-1C-projection-onboarding-skeleton-third-sample.md`。
  - CI hard gate run（optional suite observer）：
    - CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22955152198`
    - job（s2d-hard-gate）：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22955152198/job/66629768993`
    - 说明：在 `s2d-hard-gate` workflow 中将 S2D-1C 以 optional suite（`required=false`）形式挂入 `SUITE_CATALOG` 后，CI 首次完整运行包含 S2D-1C 的 hard gate，S2D-1A/S2D-1B required 套餐与 S2D-1C optional 套餐全部 `ok=true`，overall hard gate 仍以 required suites 为准但从本次开始持续记录 S2D-1C 的 Evidence。

## Current Status（进展摘要）

- S2C 已经提供 spec/registry/harness/writer/rebuild/backfill/drills 模板以及 Search harness migration，具备 Route A 的平台化前置条件，但缺少“新增 projection 必须按模板 & 有 CI gate”的约束层。
- S2D-1A 已在代码与文档层面完成 P0-P3：定义 onboarding contract、接入 sample projection（`chronicle_daily_stats`）、补齐 drills/labs，并提供单命令 onboarding 套餐脚本与 runbook；其 rebuild/backfill/drills 与 onboarding package 已在 devtest DB 中完成 red → green 的首轮演练，Evidence 记录在 `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`。
- S2D-3A 已完成 P0-P3 v1：实现本地 hard gate runner（`scripts/s2d_hard_gate.py`）、`s2d-hard-gate` CI workflow 以及基于 `SUITE_CATALOG` 的 required/optional 标记；同时提供 `S2D_HARD_GATE_SKIP_SUITES`/`S2D_HARD_GATE_WAIVE_SUITES` 环境变量，用于 legacy projection 的 skip/waiver 升级路径，首个 CI hard gate 已在 PR `#197` 上获得 green run。
- Phase 2（S2D-2A）已完成 P0-P3 v1：在 catalog/registry 层面补齐 `onboarding_status/onboarding_phase/owner_team` 标记，提供可复跑的 coverage drill 脚本并在 devtest 环境与 CI 中生成 onboarding coverage JSON 快照（区分 platformized 与 legacy 投影），并通过 `suggest_suite_catalog` + `diff_suite_catalog` helper 建立从 coverage → `SUITE_CATALOG` 的只读 guardrail；P3-C2 已在 `.github/workflows/s2d-hard-gate.yml` 中落地 coverage diff soft gate（包括“clean baseline”和人工制造 `mismatched_entries` 的实验 run），在 CI 日志中以 `[S2D-2A][info] ... soft gate clean` 或 `[S2D-2A][warning] mismatched_entries_suite_ids=[...]` 的形式提示配置与 coverage 视角的偏差，详细 contract 与 Evidence 记录在 `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md` / `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`；hard gate 仍以 `SUITE_CATALOG` 的 required/optional 为准，soft gate 只做告警、不改变退出码，为后续多投影收紧提供基线样例。
 - Phase 1B（S2D-1B）目前已走完 skeleton → C2 minimal real onboarding → P3-C2 CI 观测 → P3-C3 required 化落地：
   - skeleton 阶段在 devtest 环境完成 known-red drills 和 onboarding package run，并以 optional suite 形式接入 S2D hard gate/CI（CI run `22936588614`）；
   - C2 阶段补齐 `chronicle_events_to_entries` 的最小真实 backfill/harness labs 与 runner，完成 devtest green run（run_id=`20260311-125958`）以及启用 C2 逻辑后的多次 CI green hard gate run（例如 CI run `22937728894`、`22938862615`），在一段时间内以 optional/observer 身份稳定随 S2D-1A 一起运行；
   - P3-C3 阶段按 S2D-1B/S2D-3A log 中的设计路径，将该 projection 从“legacy skeleton + C2 optional”升级为“platformized + required”：`scripts/s2d_hard_gate.SUITE_CATALOG['s2d-1b-second-onboarding-skeleton'].required` 由 `False` 调整为 `True`，在 devtest 本地 hard gate（multi-required suites 全绿）与 CI `s2d-hard-gate` workflow 的首轮 required 语义 run（CI run `22940030372`，PR `#208`）中均获得 green，完成从 legacy skeleton → C2 → required 的闭环；更多细节与 Evidence 见 `docs/logs/log-S2D-1B-projection-onboarding-skeleton-second-sample.md` / `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`。
 - Phase 1C（S2D-1C）目前已完成 P0-P3-C1 v1：在 `search_index_to_elastic` 这条 legacy projection 上完成 skeleton → C2 minimal real drills（DB-only backfill smoke + unified outbox harness drill）并在 devtest 环境获得多轮 green Evidence（包括 runner 级别的 `ok=true` 记录），随后通过 `scripts/s2d_hard_gate.SUITE_CATALOG` 将该套餐以 optional suite（`suite_id='s2d-1c-third-onboarding-minimal-real'，required=false`）形式挂载到 S2D hard gate，本地 hard gate 与 `s2d-hard-gate` CI workflow 已开始在每次运行中一起观测该 optional suite 的行为而不改变 overall 退出码；后续是否将其升级为 required 将视 projection 完全 platformized 的进度与业务优先级再在 S2D-1C/S2D-3A log 中决策。

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
- 2026-03-09：完成 S2D-1A sample projection 的 P1/P2（spec/adapter/writer + rebuild/backfill/drills）与 P3 单命令 onboarding 套餐首轮 red→green 演练，在 devtest DB 与本地 hard gate/首个 CI `s2d-hard-gate` run 中产出 Evidence，并在本 log 与 [docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md](docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md) 入账。
