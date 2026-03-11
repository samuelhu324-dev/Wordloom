# log-S2D-1B-projection-onboarding-skeleton-second-sample（Phase 1：Second projection onboarding skeleton for legacy → platformized）

---

**id**: `S2D-1B`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `second projection onboarding skeleton for legacy → platformized (drills/evidence) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S2D`
**tags**: `EVOLUTION, Projection, Onboarding, Drills, Evidence, epic/s2d, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2D-projection-onboarding-hard-gates.md`
  **previous_log**: `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
  **reference_log_1**: `docs/logs/log-S2C-1A-projection-spec-registry-harness.md`
  **reference_log_2**: `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`
**created**: `2026-03-10`
**updated**: `2026-03-10`

---

## Decision / Outcome（结论区）

**Decision**:

- 在 S2D-1A 的 sample projection 基础上，为一条代表性的 legacy projection 搭一套“最小 onboarding skeleton”（log + labs + scripts 占位），为后续逐步 platformize 其它投影提供模板。
- 沿用 S2D-1A 的 onboarding contract 与 Evidence 口径，但允许本 phase 只交付 skeleton 与占位脚本（可以先跑不通），重点是结构/入口统一、证据 JSON 口径对齐。

**Default choices（本 phase 默认决策 / v1）**:

- 仅选择 1 条当前在 catalog 中标记为 legacy 的投影作为试点，优先选简单、风险可控的 DB→DB 或统计类投影，避免一次性迁移所有 legacy 投影。
- v1 可以只提供“可运行但功能不完整”的 labs/script 占位（例如 TODO/skip 标记），但需保证：入口命名、Evidence JSON schema、run_dir 布局与 S2D-1A 基本一致，便于后续按相同 pattern 补齐实现。
- 所有 drills 与 scripts 默认只在 dev/test 环境执行，不直接改动生产配置；任何需要 hard gate 的 CI 接入仍由 S2D-3A/S2D-2A 的后续 phase 决策。

## Definitions（概念定义）

- **Second onboarding skeleton**：在 S2D-1A 之外，为另一条 legacy projection 搭建的一套最小 onboarding 结构（log + labs + scripts），可以暂时是半成品，但结构上与 sample projection 一致。
- **Legacy projection（试点）**：当前在 coverage/catalog 中被标记为 `legacy`，尚未按 S2D onboarding contract 补齐 spec/adapter/drills 的投影，本 phase 选定 `chronicle_events_to_entries` 作为首条目标投影。
- **Skeleton labs/scripts**：复用 S2D-1A 的脚本命名和 Evidence 口径，但允许内部逻辑先以 TODO/skip 形式存在，只要能产出占位 `_recipe.json/_result.json` 即可。

## Constraints（约束）

- 不在本 phase 内强行完成该 legacy projection 的全部重构；重点是结构/命名统一，确保未来补齐实现时无需再改动入口或 Evidence 口径。
- 不修改现有 S2D-1A sample projection 的语义或 artifacts；S2D-1B 只能在其基础上“复制/裁剪”，避免引入新的耦合。
- 所有新增加的 labs/scripts 默认只写入 dev/test 环境依赖；如需 database 访问，应沿用现有 devtest 配置，不引入额外的 secret/权限面。

## Scope（本 log 范围）

- `P0`：contract（为第二条投影定义最小 onboarding skeleton 的命名/字段/证据口径，保证与 S2D-1A 对齐）。
- `P1`：实现（在现有 S2C/S2D 框架上复制并裁剪 S2D-1A 的 labs/scripts，形成新的 projection onboarding skeleton 占位）。
- `P2`：drills（在 dev/test 环境中至少跑通一次 skeleton labs，哪怕是 "known red"，并记录 Evidence）。
- `P3`：小范围验证（可选，将 skeleton 挂到 S2D-3A 的 SUITE_CATALOG 中作为 optional/experimental suite，观察 hard gate 行为，但不强制 green）。

## Success Criteria（DoD）

- 有一份明确的 S2D-1B onboarding skeleton contract（本 log），说明：
  - 目标 legacy projection 的基本信息（例如本 phase 的首个目标为 `chronicle_events_to_entries`，当前在 coverage JSON 中标记为 `legacy/none`，owner_team=unknown）；
  - 需要提供的 spec/adapter/writer/drills 占位列表，以及与 S2D-1A 的差异点。
- 代码仓库中存在一套与 S2D-1A 类似的 labs/scripts 占位（例如 backfill smoke + correctness drill + onboarding package runner），命名和 artifacts 结构与 S2D-1A 对齐。
- 至少 1 次 skeleton labs 在 dev/test 环境实际执行：
  - 即便结果为 red 或 `ok=false`，也能产出合法的 Evidence JSON（包含 projection_name、输入参数、run_dir、ok 字段）；
  - Evidence 记录在本 log 的 Evidence 区，便于后续追踪该 legacy projection 的 platformization 进度。
- 为 S2D spine 提供一条可链接的 S2D-1B 条目，说明“第二条投影的 onboarding skeleton 已搭好，可按 S2D-1A 模板逐步补齐实现”。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - P0-P2 的 onboarding skeleton contract + 占位实现 + 至少 1 次 skeleton drills 已经跑通（可 red，可 partial），并具备可复跑的入口；
  - 若启用 P3，则该 legacy projection 至少以 optional/experimental 形式被纳入 S2D-3A hard gate 套餐，并在 Evidence 中记录对应 suite_id 与 run artifacts。

## P0（Contract｜v1）

### P0-C1-S1（Second projection onboarding skeleton：最小字段与工件）

- 在 S2D-1A 的 onboarding contract 基础上，为目标 legacy projection 约定：
  - `ProjectionSpec`：
    - `projection_name`：该 legacy projection 的唯一标识（本 phase 首选 `chronicle_events_to_entries`，后续如需可扩展到其它 legacy 投影）；
    - `scope_keys`：用于限定重建/回填范围的主维度，优先沿用 sample projection 的风格（如 `tenant_id` + `date`），如不适用需在本 log 中说明；
    - `requires`：依赖的 SoT / outbox 事件源，需在 S2C registry 中可枚举；
    - `payload_schema_version`：与 outbox payload_contract 对齐的 schema 版本；
    - `apply`：处理单条事件或一个 batch 的函数入口，可以先以 TODO/"not implemented" 抛错形式存在；
  - writer 端入口：沿用统一的 outbox enqueue 函数（带 projection/op/scope/trace），禁止新增裸 SQL/INSERT；
  - harness 注册：在 projection registry 中注册 spec 与 adapter，保证该 projection 能被统一 harness 枚举（即便目前仍为 legacy）。

### P0-C1-S2（Second projection onboarding skeleton：rebuild/backfill & drills）

- 约定本 legacy projection 在完全 platformize 之前，至少要预留以下 drills 占位：
  - 至少 1 条 rebuild/backfill smoke 占位脚本，参数结构与 S2D-1A 类似（tenant/日期/范围），可以先以 TODO/skip 实现；
  - 至少 1 条 correctness drill 占位脚本，验证 outbox→projection 的端到端路径，当前可以只验证“脚本入口可运行并产出 `_result.json.ok=false` + reason`”；
  - 至少 1 个 onboarding package runner 占位脚本，将上述 scenario 串联为一条 `suite_id`，输出 `artifacts/s2d-runs.json` 风格的 summary。

### P0-C1-S3（证据口径 contract｜v1）

- evidence JSON 必须包含：
  - 投影标识：projection_name / spec id（例如 `chronicle_events_to_entries` 或未来扩展的其它 legacy projection 名称）；
  - 输入参数：租户/时间范围/事件 id 范围等（可先约定必填字段，但允许 placeholder 值）；
  - 输出产物路径：rebuild/backfill/drills 的 `run_dir` 或 artifacts 根目录；
  - PASS/FAIL 字段：`_result.json.ok` 与 failure taxonomy，兼容 S6A-4A/S2C 的 schema_version，哪怕当前大多数 run 是 `ok=false`。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S2D-1B/P<phase>-C<cycle>-S<steps>: <summary>`，例如：`S2D-1B/P1-C1-S1: scaffold second projection onboarding skeleton`。

## Plan（draft）

### P1（实现：复制 S2D-1A 结构并为第二条投影占位）

- P1-C1-S1：在 `docs/logs` 中落地本 log，并在 S2D spine 中挂上 `S2D-1B` 这一 phase id（仅说明“second projection onboarding skeleton”，目标 projection 为 `chronicle_events_to_entries`）。
- P1-C1-S2：在 `backend/scripts/labs` 与 `scripts/projections` 下，参考 S2D-1A 的脚本命名复制一套 skeleton（backfill smoke + correctness drill + onboarding package），仅替换 projection_name 与 suite_id，内部实现允许 TODO/skip 且以 `chronicle_events_to_entries` 为目标投影。

### P2（drill/verify：首轮 skeleton runs）

- P2-C1-S1：在 devtest 环境中执行 skeleton backfill smoke 与 correctness drill，允许 run 以 `ok=false` 或 known red 结束，但需保证 Evidence JSON 与 artifacts 结构正确。
- P2-C1-S2：新增 1 条 onboarding package skeleton run，写入 `artifacts/s2d-runs.json`，并在本 log 的 Evidence 区记录 headSha、suite_id、run_dir。

### P2-C2（drill/verify：skeleton → minimal real onboarding）

- P2-C2-S1：为 `chronicle_events_to_entries` 补齐最小可用的 backfill smoke / correctness drill 逻辑（可以先限定单租户/小时间窗），让 `s2d1b_*` labs 至少有一条 happy path 可以在 devtest 环境下得到 `ok=true`；
- P2-C2-S2：在 devtest 环境执行 C2 版本的 backfill/harness drills，记录新的 run_id 与 Evidence，并在本 log 的 Evidence 区增补对应记录（包括 `headSha/run_id/run_dir/ok` 等关键信息）。

### P3（可选：挂载到 hard gate 套餐）

- P3-C1-S1：在 `scripts/s2d_hard_gate.py` 的 `SUITE_CATALOG` 中新增 1 条 optional/experimental suite，对应第二条投影的 onboarding skeleton（例如 `suite_id=s2d-1b-second-onboarding`），默认 `required=false`；
- P3-C1-S2：在 CI 的 `s2d-hard-gate` workflow 中观察该 suite 的 run 行为，并在 S2D-2A coverage diff 中确认该 projection 仍标记为 legacy，仅作为试验项存在。

### P3-C2（adoption：C2 行为在 CI 上的长期观测）

- P3-C2-S1：在 `s2d-hard-gate` workflow 上持续观测 S2D-1B suite 的 C2 行为（仍标记为 optional），确保在典型变更路径上 S2D-1B labs/runner 能稳定保持 `ok=true` 或给出可解释的 `ok=false`；按需在本 log 与 S2D-3A log 中补充 CI Evidence 与告警约定。

### P3-C3（upgrade：从 legacy skeleton 升级为 platformized + required）

- P3-C3-S1（catalog/coverage upgrade plan）：定义 `chronicle_events_to_entries` 从 `legacy` → `platformized` 的升级条件与路径，包括：
  - 覆盖视角：在 S2D-2A coverage JSON 中，将该投影从 `legacy` 升级为 `platformized`，并在 `suggested_suite_catalog` 中标记其 onboarding suite 为 `required=true`；
  - 行为视角：要求 S2D-1B C2 labs/runner 在典型 devtest/CI 路径上连续若干次（例如 N≥3）保持 green，且无未解释的 `ok=false`；
  - 文档视角：在本 log / S2D-2A / S2D-3A / S2D spine 中增加“该 projection 已 platformized + required”的稳定叙述，并记录最后一次从 optional → required 的具体 commit/headSha。
- P3-C3-S2（SUITE_CATALOG & suite_id 升级）：在满足 P3-C3-S1 升级条件后，按以下步骤调整 hard gate 配置：
  - 将 `scripts/s2d_hard_gate.SUITE_CATALOG` 中 `s2d-1b-second-onboarding-skeleton` 的 `required` 字段由 `False` 调整为 `True`；
  - 如有需要，可将 suite id 从带有 `-skeleton` 的命名收敛为更稳定的正式名称（例如 `s2d-1b-chronicle-events-to-entries-onboarding`），同时保证：
    - S2D-1B log 与 S2D-3A log 中的 suite_id 叙述更新；
    - S2D-2A coverage diff helper 与 `suggested_suite_catalog` 中的 suite id 一致；
  - 在 CI workflow `.github/workflows/s2d-hard-gate.yml` 中确认所有显式引用的 suite id 已同步更新（如有）。
- P3-C3-S3（required suite 行为验证 & guardrail）：在 SUITE_CATALOG 升级为 required 后，通过一轮本地 + CI hard gate run 验证：
  - 当 S2D-1A 与 S2D-1B 两个 required suites 均 `ok=true` 时，`hard_gate` job 以 Success 结束；
  - 当仅 S2D-1B 出现 `ok=false` 时，`hard_gate` job 应以非 0 退出，并在 S2D-3A summary JSON 与 CI 日志中明确指向 S2D-1B failure 原因；
  - S2D-2A coverage diff / soft gate 的 `missing_in_hard_gate`/`mismatched_entries` 字段在该升级后保持 clean（或仅包含可接受的 warning），避免出现“coverage 认为应 required 但 SUITE_CATALOG 配置为 optional/absent”的不一致。
- P3-C3-S4（waiver/exception 机制约定）：为避免在升级早期因 S2D-1B 短期不稳定造成大面积 CI 阻塞，在 S2D-3A/S2D-2A 中为该 projection 约定有限的 waiver 策略，例如：
  - 针对特定分支或短期维护窗口，允许通过 `S2D_HARD_GATE_WAIVE_SUITES=s2d-1b-...` 暂时豁免该 suite 的失败；
  - 为长期策略记录“何种场景下可以使用 waiver”“waiver 生效的最大时长/次数”，并要求在 S2D spine 中登记，避免 silent failure；
  - 明确“恢复 required 行为”的步骤（撤销 waiver、确认最近若干次 run 均为 green 并更新 Evidence）。

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 second projection onboarding skeleton 的最小字段与工件 contract，并在本 log 固化（首个目标为 `chronicle_events_to_entries`）
- [x] `P0-C1-S2`：定义 second projection 的 rebuild/backfill & drills skeleton 要求
- [x] `P0-C1-S3`：定义 second projection onboarding skeleton 的 evidence JSON 口径

### P1（实现：skeleton 落地）

- [x] `P1-C1-S1`：在 docs/logs 中落地本 log，并在 S2D spine 中挂上 S2D-1B
- [x] `P1-C1-S2`：复制并裁剪 S2D-1A 的 labs/scripts，为第二条投影生成 skeleton 占位（v1：`s2d1b_chronicle_events_to_entries_*` labs + `s2d_1b_p2c1s2_second_onboarding_skeleton.py` runner）

### P2（drill/verify：skeleton runs）

- [x] `P2-C1-S1`：在 devtest 环境执行 skeleton backfill smoke & correctness drill，并记录 Evidence（v1：run_id=20260311-1，known red）
- [x] `P2-C1-S2`：执行 skeleton onboarding package run，写入 `artifacts/s2d-runs.json` 并在本 log 中登记（v1：run_id=20260311-1，ok=false）

### P2（drill/verify：C2 实装 & 演练）

- [x] `P2-C2-S1`：为 `chronicle_events_to_entries` 补齐最小可用 backfill smoke / correctness drill 逻辑（至少一条 happy path 在 devtest 环境下 `ok=true`）
- [x] `P2-C2-S2`：在 devtest 环境运行 C2 版本的 labs/runner，并将新的 run_id 与 Evidence 记账到 `_snapshot/auto` 与 `artifacts/s2d-runs.json` 以及本 log 的 Evidence 区

### P3（可选：hard gate 挂载）

- [x] `P3-C1-S1`：在 `SUITE_CATALOG` 中新增 optional/experimental suite 对应第二条投影 skeleton
- [x] `P3-C1-S2`：在 CI 中观测该 suite 的行为，并按需在 S2D-2A/3A 中记录相关 Evidence

### P3（adoption & upgrade：C2/C3）

- [x] `P3-C2-S1`：在 CI 的 `s2d-hard-gate` workflow 中持续观测 S2D-1B suite 的 C2 行为（仍 optional），并在本 log / S2D-3A 中补充长期 Evidence 与必要的 warning/info 约定（v1：记录 CI run=`22937728894` 的行为）
- [ ] `P3-C3-S1`：在 `chronicle_events_to_entries` 表现稳定后，将其从 legacy 升级为 platformized，并将本 suite 升级为 required（含 suite_id / SUITE_CATALOG / coverage diff 预期的更新），完成从“legacy skeleton”到“正式 platformized projection onboarding”的闭环

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P2-C1-S1（second projection skeleton drills｜2026-03-11）

- headSha：`a5888e8c6da80e59909184c5a7328928014d792c`
- artifacts：
  - 脚本：`backend/scripts/labs/s2d1b_chronicle_events_to_entries_backfill_smoke.py`
  - run_dir：`docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_backfill_smoke/20260311-1`
  - 脚本：`backend/scripts/labs/s2d1b_chronicle_events_to_entries_harness_drill.py`
  - run_dir：`docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_harness_drill/20260311-1`
- 期望（expected）：
  - skeleton drills 至少能够跑出 `_result.json.ok=false` + 合理的 failure reason；
  - artifacts 结构与 S2D-1A 保持一致。
- 观测（observed）：
  - 2026-03-11 在 devtest 环境执行：
    - `c:/python314/python.exe backend/scripts/labs/s2d1b_chronicle_events_to_entries_backfill_smoke.py --database-url postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test --run-id 20260311-1 --outdir docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_backfill_smoke/20260311-1`
    - `c:/python314/python.exe backend/scripts/labs/s2d1b_chronicle_events_to_entries_harness_drill.py --database-url postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test --run-id 20260311-1 --outdir docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_harness_drill/20260311-1`
  - 两条 skeleton lab 均成功产出 `_result.json`，`ok=false` 且 `notes.reason="skeleton_not_implemented_yet"`，符合 P0 约定的 "known red" skeleton 预期。

### P2-C1-S2（second projection skeleton onboarding package｜2026-03-11）

- headSha：`a5888e8c6da80e59909184c5a7328928014d792c`
- log_id/phase/cycle/step：`S2D-1B / P2 / C1 / S2`
- runner：`scripts/projections/s2d_1b_p2c1s2_second_onboarding_skeleton.py`
- runs：
  - C1（首跑）：
    - run_id：`20260311-1`
    - scenarios：
      - backfill smoke：`docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_backfill_smoke/20260311-1`
      - correctness drill：`docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_harness_drill/20260311-1`
    - summary：`artifacts/s2d-runs.json` 中新增一条记录（`log_id="S2D-1B"`，`phase="P2"`，`cycle="C1"`，`step="S2"`，`run_id="20260311-1"`，`ok=false`，两个 scenario 均 `exit_code=2 && ok=false`）

### P2-C2-S1/S2（second projection minimal real onboarding drills｜2026-03-11）

- headSha：`6eed5e54caedd001f35201d16b29827544ae5e7b`
- log_id/phase/cycle/step：`S2D-1B / P2 / C2 / S2`
- runner：`scripts/projections/s2d_1b_p2c1s2_second_onboarding_skeleton.py`
- runs（devtest DB｜`postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test`）：
  - C2（minimal real onboarding｜首轮）：
    - run_id：`20260311-125958`
    - backfill smoke：
      - 脚本：`backend/scripts/labs/s2d1b_chronicle_events_to_entries_backfill_smoke.py`
      - run_dir：`docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_backfill_smoke/20260311-125958`
      - `_result.json`：`ok=true`，`outbox.rows_for_event=1`；chronicle_event 通过 `SQLAlchemyChronicleRepository.save()` 写入，并成功在 unified `outbox_events` 中产生一条 `projection="chronicle_events_to_entries"` 的行。
    - harness drill：
      - 脚本：`backend/scripts/labs/s2d1b_chronicle_events_to_entries_harness_drill.py`
      - run_dir：`docs/labs/_snapshot/auto/s2d1b_chronicle_events_to_entries_harness_drill/20260311-125958`
      - `_result.json`：`ok=true`，`projection_state.entries_for_event=1 && outbox_rows_for_event=1`，`harness_exit_code=0`；projection framework harness 在该 projection 上跑到 idle，生成并验证对应的 `chronicle_entries` 行。
    - summary：`artifacts/s2d-runs.json` 中追加一条新的记录（`log_id="S2D-1B"`，`phase="P2"`，`cycle="C2"`，`step="S2"`，`run_id="20260311-125958"`，`ok=true`，两个 scenario 均 `exit_code=0 && ok=true`），标记本投影在 devtest 环境下完成了首轮“最小真实 onboarding”演练。

### P3-C1-S1（second projection skeleton wired into hard gate｜2026-03-11）

- headSha：`c51f51573e9388539575a700041bb66dc6c8eedb`
- suite_id：`s2d-1b-second-onboarding-skeleton`
- suite_catalog：
  - `scripts/s2d_hard_gate.py.SUITE_CATALOG["s2d-1b-second-onboarding-skeleton"] = {log_id="S2D-1B", required=False}`
- 期望（expected）：
  - 本 suite 作为 optional/experimental skeleton 存在：即便 `ok=false`，也不会影响 `hard_gate` 对 required suites 的整体退出码判断；
  - local runner / CI 均可通过 `--suite s2d-1b-second-onboarding-skeleton` 显式拉起该 skeleton onboarding package；
  - 每次 run 会向 `artifacts/s2d-runs.json` 追加一条新的 `log_id="S2D-1B"` 记录，用于后续追踪该 legacy projection 的 platformization 进度。
- 观测（observed）：
  - 2026-03-11 在本地使用 `scripts/s2d_hard_gate.py --database-url <devtest> --suite s2d-1a-sample-onboarding --suite s2d-1b-second-onboarding-skeleton` 进行试跑：
    - S2D-1A 套餐保持 green；
    - S2D-1B skeleton 套餐以 `ok=false` 结束，但由于其在 SUITE_CATALOG 中 `required=False`，整体 `overall_ok` 仍由 S2D-1A 的结果决定；
  - CI workflow `.github/workflows/s2d-hard-gate.yml` 已更新为在 `Run S2D hard gate` 步骤中同时传入 `--suite s2d-1a-sample-onboarding --suite s2d-1b-second-onboarding-skeleton`，具体 CI 行为见下方 `P3-C1-S2` 记录。

### P3-C1-S2（second projection skeleton suite on CI hard gate｜2026-03-11）

- headSha：`c51f51573e9388539575a700041bb66dc6c8eedb`
- workflow：`.github/workflows/s2d-hard-gate.yml`
- CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22936588614`
- suites：
  - required：`s2d-1a-sample-onboarding`（S2D-1A sample projection onboarding 套餐）
  - optional：`s2d-1b-second-onboarding-skeleton`（本 log 对应的 legacy projection skeleton 套餐）
- 期望（expected）：
  - CI 中的 `s2d-hard-gate` workflow 在 devtest DB 上同时拉起 S2D-1A sample 与 S2D-1B skeleton 两个 suite；
  - 当 S2D-1A `ok=true` 且所有 required suites 通过时，即便 S2D-1B skeleton 仍为 `ok=false`，整体 `hard_gate` job 依然以 Success 结束；
  - 本次 run 结束后，`artifacts/s2d-runs.json` 中存在一条新的 `log_id="S2D-1B"` 记录，对应 CI 环境下的 skeleton onboarding 套餐 run，用于长期观测该 legacy projection 的 platformization 进度。
- 观测（observed）：
  - 2026-03-11 由分支 `S2D-projection-onboarding-hard-gates` 推送 commit `c51f5157...` 触发的 `s2d-hard-gate` workflow（Run id=`22936588614`）以 Success 结束：
    - workflow 日志显示 `Run S2D hard gate (S2D-1A sample + S2D-1B skeleton)` 步骤成功执行，`hard_gate` job 退出码为 0；
    - `artifacts/s2d-runs.json` 中追加了新的 `S2D-1B` 记录，`ok=false` 且 scenarios 来自 CI 环境下的 skeleton backfill/harness labs，符合“optional/known red skeleton 不 gate CI”的 v1 约定；
    - coverage diff / soft gate 步骤继续作为只读 guardrail 存在，不改变本次 run 的退出码。

### P3-C2-S1（C2 suite behavior on CI hard gate｜2026-03-11）

- headSha：`03ac1b355db8cff074a249fb4a3ee06ffd433225`
- workflow：`.github/workflows/s2d-hard-gate.yml`
- CI run：`https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22937728894`
- suites（按 SUITE_CATALOG 角色）：
  - required：`s2d-1a-sample-onboarding`（S2D-1A sample projection onboarding 套餐，仍然是唯一 required suite）
  - optional：`s2d-1b-second-onboarding-skeleton`（本 log 对应的 legacy projection C2 套餐，仍标记为 optional）
- 期望（expected）：
  - `s2d-hard-gate` workflow 在 CI 上沿用与本地一致的配置：同时拉起 S2D-1A 与 S2D-1B 两个 suites，并根据 required/optional 语义只用 S2D-1A 的结果决定 `exit_code`；
  - 在 C2 之后，S2D-1B labs/runner 已具备“最小真实 onboarding”能力，因此在 devtest DB 的 CI 环境下应当可以稳定产出结构正确且可解释的 `_result.json` 与 `artifacts/s2d-runs.json` 记录；
  - 本轮 run 作为 P3-C2 的首个 CI 观测点，用于验证：在真实 CI 路径上启用 C2 逻辑后，hard gate job 仍然保持 Success，且 optional suite 不会意外交叉影响 required suite 的行为。
- 观测（observed）：
  - 2026-03-11，由 PR `#206 (S2D-projection-onboarding-hard-gates)` 触发的 `s2d-hard-gate` workflow（Run id=`22937728894`）以 Success 结束，`hard_gate` job 用时约 42s；
  - 从 workflow 配置与本地同日 hard gate dry run 可知，本次 CI 仍然通过 `--suite s2d-1a-sample-onboarding --suite s2d-1b-second-onboarding-skeleton` 调用了同一入口脚本，并在 devtest DB 上完成 required+optional 两个 suites 的执行；
  - 结合本地 devtest C2 run（`run_id=20260311-125958`，两个 S2D-1B labs `ok=true`）与本次 CI run 的整体 Success，可将其视为“C2 逻辑在 CI 上首轮 green 行为”的确认样本，后续 P3-C2 可继续追加更多 CI Evidence 作为长期观测；
  - 2026-03-11，后续由 PR `#207 (S2D-projection-onboarding-hard-gates)` 触发的 `s2d-hard-gate` workflow（Run id=`22938862615`）同样以 Success 结束，`hard_gate` job 用时约 51s，使用相同的 required+optional suite 配置并成功产出 `s2d-hard-gate-22938862615-1` artifacts，可视为 C2 行为在 CI 上的第二个稳定样本，为未来 P3-C3 升级 required 提供了额外信心。

## Recent changes（for traceability，可选）

- 2026-03-10：scaffold S2D-1B log，定义 second projection onboarding skeleton 的 contract 与执行计划（基于 S2D-1A 的 sample projection 模板）。
- 2026-03-11：完成首轮 S2D-1B skeleton drills 与 onboarding package run（run_id=20260311-1，known red），并将 Evidence 记账到本 log 与 `artifacts/s2d-runs.json`。
- 2026-03-11：在 `scripts/s2d_hard_gate.py` 中将 `s2d-1b-second-onboarding-skeleton` 作为 optional suite 纳入 `SUITE_CATALOG`，并更新 CI workflow `s2d-hard-gate.yml` 使其在 `Run S2D hard gate` 步骤中同时拉起 S2D-1A sample 与 S2D-1B skeleton 套餐；同日首个包含该改动的 CI run（Run id=`22936588614`，headSha=`c51f5157...`）成功通过，证据已在本 log 的 `P3-C1-S1/S2` 与 S2D-3A log 中补齐。
- 2026-03-11：在 WSL + devtest DB（5435）环境下完成 C2 版 labs/runner 的首轮实装演练（run_id=20260311-125958），backfill smoke 与 harness drill 均 `ok=true`，并在 `artifacts/s2d-runs.json` 中新增 `phase="P2"/cycle="C2"/step="S2"` 记录，标记本投影已具备最小可复跑的 real onboarding 能力。
- 2026-03-11：由 PR `#206` 触发 CI `s2d-hard-gate` workflow（Run id=`22937728894`，headSha=`03ac1b35...`）在 devtest DB 上再次并行执行 S2D-1A required suite 与 S2D-1B C2 optional suite，`hard_gate` job 以 Success 结束，为 P3-C2 提供了首个“C2 行为在 CI 上 green”的 Evidence 记录。
