# run-S4D-4C (Agent Context Navigation)

---

**id**: `run-S4D-4C-agent-context-navigation`
**kind**: `runbook`
**title**: `run/S4D-4C-agent-context-navigation`
**status**: `stable`
**scope**: `S4D-4C`
**decision_date**: `2026-03-26`
**context_issue**:
  **DoD**: `P3 narrows the default retrieval surface for S4D/drill/workflow investigations so Agent/Copilot does not need to load the largest logs and scenario modules first.`
  **Labs**: ``
**decision**: `Use this quick index as the default entry for S4D timeout, release-gate, and drill-scenario triage; only open the exact phase log, script, or scenario module that matches the current symptom.`
  **positive**: `"Smaller default context", "Less blind retrieval of large files", "Faster drill/runtime triage"`
  **negative**: `"Requires operators to follow the index first", "Needs maintenance when new scenario clusters appear"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 给 S4D / drill / workflow 相关排障一条更窄的默认入口，避免一上来就把大 log、大脚本、大 scenario 模块整段装入上下文。
- 把当前最容易拉爆 Copilot/Agent 上下文的 5 个高压 surface 固定下来，并给出更小的首读路径。
- 明确一个简单规则：先按 gate / scenario / symptom 缩小范围，再打开具体文件；父级 spine 只用于 phase 记账，不作为第一检索入口。

## 2) Ranked High-Pressure Surfaces

### 2.1 `scripts/ops/cloud_release_workflow.sh`

- 当前约 `663` 行，是 cloud runtime release 的主编排器。
- 高压原因：同一文件承载 preflight、deploy、verify、rollback、summary 聚合；一旦 gate 失败，检索很容易把整个 orchestrator 拉进来。
- 默认做法：
  - 先看 `summary.json` 的 `terminalGate` / `failureClass`
  - 再看 `docs/runbook/run-S4D-cloud-runtime-release-operations.md` 的故障类别
  - 只有 gate 逻辑仍不清楚时，才打开这个脚本

### 2.2 `docs/logs/log-S4D-4C-408-timeout-eradication.md` + `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`

- 这是 S4D timeout/runtime 的热路径聚合面。
- 高压原因：phase 历史、当前状态、evidence、priority contract 都集中在同一检索面；一旦同时打开 parent spine + phase log，很容易重复装载大量上下文。
- 默认做法：
  - 先读本 quick index
  - 只在需要 phase ledger 时打开 `S4D-4C`
  - 只在需要顶层历史边界时打开 `S4D` spine

### 2.3 `backend/scripts/cli_app/scenarios/_failure_drill_shared.py`

- 当前约 `889` 行，是 failure drills 共享逻辑的最大 scenario helper。
- 高压原因：多个 failure 场景复用这里的注入、验证、导出与 contract，检索一个 failure drill 时容易把共享实现整段带入。
- 默认做法：
  - 先确定当前是不是 failure drill 家族
  - 只在具体 scenario 已经定位到 `collector_down` / `es_timeout` / `es_bulk_partial` 等 failure 路径后，再补读这个 shared helper

### 2.4 `backend/scripts/cli_app/scenarios/shadow_verify_dual_run_window.py` + `shadow_verify_dual_run_stage2.py`

- 当前约 `707` 行和 `660` 行，是 dual-run / shadow-verify 家族最重的两个 scenario 模块。
- 高压原因：参数多、窗口逻辑长、与 outbox / ES / compare contract 交叉；若问题只是单个 scenario 入口或命令行参数，整段加载收益很低。
- 默认做法：
  - 先从 scenario 名定位到精确模块
  - `window` 问题只看 `shadow_verify_dual_run_window.py`
  - `stage2` 问题只看 `shadow_verify_dual_run_stage2.py`
  - 不再把 dual-run 家族整包检索作为默认入口

### 2.5 `backend/scripts/cli_app/registry.py`

- 文件本身不大，但它是 builtin scenarios 的高扇出 discovery surface。
- 高压原因：一个入口会引出全部 builtin scenario 名称，随后触发更大的二次检索面。
- 默认做法：
  - 先确认 scenario 名
  - 再打开对应 scenario 文件
  - 不把 registry 当成“先看全量再定位”的默认入口

## 3) Minimal Read Paths

### 3.1 Cloud runtime release / stable-runner / approval

- 先看：`summary.json`、`preflight.log`、`verify.log`
- 再看：`docs/runbook/run-S4D-cloud-release-gate-map.md`
- 再看：`docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- 最后才看：`scripts/ops/cloud_release_workflow.sh`

### 3.2 S4D-4C timeout taxonomy / current status / evidence bookkeeping

- 先看：`docs/logs/log-S4D-4C-408-timeout-eradication.md`
- 只有在需要 parent boundary、phase lineage 或顶层路线时，才补看：`docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`

### 3.3 Drill / scenario triage

- 先看：scenario 名本身
- 再看：`backend/scripts/cli_app/registry.py` 确认 builtin registration
- 然后只打开对应 scenario 模块
- 如果属于 failure drill 共享 contract，再补看：`backend/scripts/cli_app/scenarios/_failure_drill_shared.py`

## 4) Practical Rules

- 若当前问题已经有 `terminalGate` 或 `failureClass`，不要先打开大 log；先按 gate 缩小到对应脚本或 runbook 段落。
- 若当前问题已经有 scenario 名，不要先打开 `backend/scripts/cli.py`；它现在只是薄入口壳，不再是主要上下文压力源。
- 若当前问题属于 S4D phase 记账，优先读 `S4D-4C` 当前状态与对应 evidence block，不要同时加载整个 S4D spine 与多个 phase log。
- 若当前问题只涉及 failure drill contract，先看具体 scenario，再决定是否需要 shared helper。

## 5) What Changed Since Earlier 408 Reports

- `backend/scripts/cli.py` 已从早期的超大入口收口为薄 dispatch shell，当前不再是第一高压对象。
- 当前主要风险已经转移到：
  - S4D runtime 聚合日志面
  - release workflow orchestrator
  - failure drill shared helper
  - dual-run 大 scenario 模块
  - scenario discovery fan-out 面

## 6) Related References

- `docs/logs/log-S4D-4C-408-timeout-eradication.md`
- `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
- `docs/runbook/run-S4D-cloud-release-gate-map.md`
- `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- `docs/logs/log-S0C-3A-cli-breakdown.md`
- `backend/scripts/cli_app/registry.py`