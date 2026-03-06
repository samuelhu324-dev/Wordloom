# Log-S6A: evidence & drills spine（S6：Evidence & Drills 主题索引 / SoT 编织层）

---

**id**: `S6A-evidence-drills-spine`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `evidence & drills spine (indexing + contracts + hard-gates)`
**status**: `stable`          # draft | stable | archived
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Artifacts, FailureContract, Scenarios, epic/s6, sub/6a`
**links**: ``
  **roadmap_v2**: `docs/ROADMAP v2.md`
  **runbook_s2b**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-03-04`
**updated**: `2026-03-06`

---

## Decision / Outcome（结论区）

- 本 log 是 S6 的“主题索引/Spine log”：**不搬家旧 SoT**，只负责把“散落的 contracts + drills + evidence 入口”串成可持续演进的索引。
- S6A 的目标不是再造一份新 SoT，而是让后续演进（Route B / outbox / worker / CI drills）有一个稳定的“目录页 + 任务脊椎”。
- 执行落点仍遵守“真实改动归真实模块”：
  - outbox/worker/reason/状态机 → `S2B`/代码实现
  - catalog/runner/workflows/CI → `S0C`/自动化体系
  - drills 按钮化与误差/故障复盘 → `S3A`
  - 备份/脱敏/恢复等证据流水线 → `S5A`

## Constraints（约束）

- 不搬运旧内容：旧 log 仍是单点事实源（SoT）；S6A 只做索引与“跨域 contract 的收口”。
- 不新增第二套入口：对外稳定入口优先是既有的 runbook/CLI/workflows；S6A 不创造“第三条路”。
- reason 必须低基数：禁止把高基数信息写进 metrics labels / reason 字段；reason 是契约而不是日志。
- 证据优先机器可判定：尽量避免“靠截图/靠肉眼判断”；PASS/FAIL 以 `_result.json`/evidence JSON 为准。

## Scope（本 log 范围）

- 本 log 负责：
  - S6 主题的索引（哪些 log/哪些入口/哪些 contracts 是 S6 的骨架）
  - P1+ 的执行清单（把后续要做的深化点拆成可以逐步打勾的 checklist）
- 本 log 不负责：
  - 取代任何既有 log 的细节内容
  - 记录每一次具体 drill run 的证据（证据应进入对应领域 log 或 artifacts）

## Success Criteria（DoD）

- 结构层面：
  - INDEX 能一眼找到 S6 相关旧 SoT，并能导航到稳定入口（CLI/workflow/runbook）。
  - S6A 能持续增长而不变成“第二份 SoT”（以链接与 checklist 为主）。
- 工程层面（可演进）：
  - worker/refactor/表迁移不再轻易打断 drills（入口漂移零容忍）。
  - fault drills 能形成 hard gate：CI 可判定 PASS/FAIL，失败 artifacts 自解释。
  - reason taxonomy（DB `error_reason` + metrics `reason`）能被 verify 断言，且保持低基数。

## Background

历史上很多 evidence/drills 都是“寄生型演进”：在合表/迁移/事故复盘时顺手做出来。
这本身很正常；问题在于：当这些能力形成规模后，缺少一个索引会造成：入口漂移、合约漂移、证据口径不一致、无法形成 hard gate。

因此 S6A 先做两件事：

1) 把既有 SoT 全部索引化（P0）
2) 把下一阶段要深化的点变成可执行 checklist（P1+）

## Phases（切片 / 里程碑）

### P0（Indexing / Mapping）：旧 SoT → 当前 S6A 的关系

> 规则：P0 只做“链接 + 关系说明 + 未来切片入口”，不重写旧内容。

- `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
  - 关系：定义 CI artifacts 的打包/上传口径，是 S6 的“Artifacts Contract”基线。
  - S6A 复用：作为 hard gate 的证据产物形态（summary / zip / 失败必带排障材料）。

- `docs/logs/log-S0C-4A-scenarios-taxonomy.md` + `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
  - 关系：定义 scenario taxonomy、catalog 单一事实源、suite/runner 结构与 guardrails。
  - S6A 复用：S6 的 drills 入口与“场景编排产品化”的底盘。

- `docs/logs/log-S0C-5A-Git-commit+push-descriptions.md`
  - 关系：把“commit/PR 描述 + 证据入口 + headSha 可追溯性”固定成纪律，降低 evidence 漂移。
  - S6A 复用：S6 的 hard gate 需要可追溯到 headSha/commit message（尤其是 artifacts 与 scenario 的映射）。

- `docs/logs/log-S2B-1A-failure-contract-v1.md` + `docs/logs/log-S2B-2A-failure-contract-v2.md`
  - 关系：Failure Contract（稳定入口/共享键/证据链/可回滚窗口）的 SoT。
  - S6A 复用：S6 的“可审计 evidence pipeline”必须以 Failure Contract 的共享键与 `_result.json` 作为事实源。

- `docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md` + `docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`
  - 关系：write-gate/dual-run/cutover 的 drills 体系与 evidence 口径（含 artifacts contract 段落）。
  - S6A 复用：把“可切写”演练的验收方式推广为 fault drills 的 hard gate（机器可判定）。

- `docs/logs/log-S2B-3A-unified-consumer-framework.md`
  - 关系：outbox_core 抽取与 rollout，包含低基数 reason、状态机不变量与对外稳定面约束。
  - S6A 复用：reason taxonomy 是 drills PASS/FAIL 的核心输入之一（metrics label + DB error_reason）。

- `docs/logs/log-S3A-2A-3B-automated-failure-drills.md`
  - 关系：把 failure drills 做成按钮化（run/verify/export/clean）并记录真实 malfunction。
  - S6A 复用：把“可重复 + 可判定 + 可取证”的流程迁移到 Route B/fault suite，并逐步补齐 hard gate。

- `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - 关系：把 failure drills 与 GitHub Actions/可观测面串起来，形成“CI 可跑 + 可看 + 可复盘”的闭环习惯。
  - S6A 复用：S6 的目标不是多写几条脚本，而是把 drills 变成持续可执行的质量闸门。

- `docs/logs/log-S2C-4A-projection-drills-template.md` + `docs/logs/log-S2C-projection-framework-platformization.md`
  - 关系：projection drills 的模板化/平台化路径。
  - S6A 复用：后续新增投影/新增故障场景时的模板与 DoD 参考。

- `docs/logs/log-S5A-security-governance.md`（以及 phase logs：`S5A-2A/3A/3B`）
  - 关系：把安全/治理的演进用 drills+artifacts 固化为证据流水线（含“单命令 pipeline drill”思路）。
  - S6A 复用：S6 把“证据流水线化”抽成横切方法论：单命令、结构化 evidence JSON、稳定入口。

- `docs/logs/log-S5A-1A-authcontext-policy-audit.md`
  - 关系：S5 的早期 drills/evidence 形态（tenant boundary/policy/audit）与“共享键/证据 JSON”习惯的起点之一。
  - S6A 复用：用它做“领域类 drills（policy/audit）”与“平台类 drills（outbox/fault）”的对照样本。

### P1（Draft）：把“入口漂移”做成零容忍

目标：未来 worker refactor / 表迁移 / CLI 调整，不能再把 drills 打断。

- Stable Entry contract：所有场景启动 worker 必须走“稳定入口脚本”，禁止硬编码 legacy 路径。
- Centralize worker spawn + env wiring：把 worker command/环境变量拼装集中到一个 helper，被所有场景复用。

- 子 log（P1 落地）：`docs/logs/log-S6A-1A-stable-entry-contract.md`

### P2（Draft）：Unify supply creation（只走 unified outbox）

目标：fault scenarios 不再往旧表插入导致“触发与消费不一致”。

- 场景供给（seed/insert）优先插入 `outbox_events`（带 projection），旧表仅作为迁移窗口 fallback。
- verify 在 DB 侧也要双兼容，直到 legacy 下线。

- 子 log（P2 落地）：`docs/logs/log-S6A-2A-unify-supply-creation.md`（stable）

### P3（Draft）：Failure taxonomy hard interface（reason = contract）

目标：reason 不是“日志字符串”，而是：低基数、可聚合、可被 verify 断言的稳定接口。

- 将 `error_reason`（DB）与 Prometheus `reason` label 视为同一 contract。
- verify 既要看 metrics delta，也要看 DB 终态（terminal vs retry_scheduled）与 reason family。

- 子 log（P3 落地）：`docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md`（stable）

### P4（Draft）：Hard-gate + evidence JSON（让 CI 失败自解释）

- 每个 `fault/obs_infra/*` 场景导出一个小的 evidence JSON：expected vs observed（retry/failed/reclaimed/replayed）。
- CI 失败时 artifacts 中必须包含：evidence JSON + 最小 logs/metrics dumps（避免“只能看图/看日志猜”）。

- 子 log（P4 落地）：`docs/logs/log-S6A-4A-hard-gate-evidence-json.md`（draft）

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：S6 旧 SoT 索引化（INDEX 清单 + S6A mapping）
- [x] `P1`：Stable Entry contract（入口漂移零容忍 + helper 复用）
- [x] `P2`：Supply creation 统一到 `outbox_events`（legacy 退场计划）
- [x] `P3`：reason taxonomy contract（metrics + DB + verify 对齐）
- [x] `P4`：fault suite hard-gate（evidence JSON + 自解释 artifacts）

## Current Status（进展摘要）

- P0：已完成索引化骨架（S6A spine log + INDEX 的 old logs 清单）。
- Route B/fault drills：已修复一次“入口漂移/表不一致”风险（见 Recent changes）。
- P1：Stable Entry contract 已落地（见子 log：`docs/logs/log-S6A-1A-stable-entry-contract.md`，含 shadow_verify 证据）。
- P2：Supply creation contract 已落地并标记 stable（见子 log：`docs/logs/log-S6A-2A-unify-supply-creation.md`）。
- P3：reason taxonomy contract 已闭环（DB + metrics + verify）并产出多份 evidence（见子 log：`docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md`）。
- P4：已完成 fault suite hard-gate（CI 可判定 PASS/FAIL + 自解释 artifacts），记账见子 log：`docs/logs/log-S6A-4A-hard-gate-evidence-json.md`。

## Stability（stable 口径）

- 本 log 标记为 `stable`：表示 P0–P4 的骨架里程碑已闭环（索引 + contract + hard-gate）。
- 进入 `stable` 的最低门槛已满足：
  - P1：入口漂移防护落地（共享 helper 复用）
  - P3：reason contract 闭环（metrics + DB + verify 对齐）
  - P4：fault drills 已形成 hard-gate，且 artifacts 最小集可自解释

## Recent changes (for traceability)

- 2026-03-04：修复 fault scenarios 依赖的 Search worker 入口漂移；并让插入脚本优先写 unified outbox（存在时）。
  - 代码变更落在对应脚本与 scenarios 中（由 git commit 追溯）。
- 2026-03-04：完成 Stable Entry contract（helper 复用 + evidence 口径），并产出一份 shadow_verify 证据（见 `docs/logs/log-S6A-1A-stable-entry-contract.md`）。
