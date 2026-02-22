# Log-S0C-3A: tools/cli breakdown

---

**id**: `S0C-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `tools/cli breakdown`
**status**: `draft`          # draft | stable | archived
**scope**: `S0C`
**tags**: `EVOLOTION, Docs, Projection, Search, lab, sub/1`
**links**: ``
  **issue**: `#83, #66`
  **pr**: `null`
  **adr**: ``
  **runbook**: `null`
**created**: `2026-02-20`
**updated**: `2026-02-22`

---

## Decision / Outcome（结论区）

- 将超大 `backend/scripts/cli.py` 拆分为“薄入口壳 + 场景模块（scenario handlers）”；入口文件 **100~300 行** 作为目标线（非硬性门槛），用于降低工具/Agent 将其整段吞入上下文导致的请求体膨胀风险。
- 验收口径：以 **dispatch-only + CLI/CI 合约稳定** 为准（命令/参数/help/exit code/evidence contract 不漂移），而不是“卡行数”。
- 采用“按 scenario 插件化”的拆分方式：
  - `cli.py` 仅负责：参数解析 → 选择 scenario/command → 调用 handler → 统一 exit code 与产物（artifacts）落盘。
  - 场景/handler 在 `backend/scripts/cli_app/scenarios/*` 注册到 registry；CLI 命令簇的“实现侧”逐步落在 `backend/scripts/cli_app/labs/*`，入口只做薄委托（避免 `cli.py` 长胖）。
- 拆分策略遵循“先抽共性、再搬场景”的最小可行路径：先抽出 artifacts contract，再逐个 scenario 搬家，确保 **CLI 对外参数/场景名不变**（只搬家、不改行为）。
- 可选：把聚合型 workflow（如 `drill-write-gate.yml`）按 scenario 拆开，以降低 CI 配置复杂度并提升证据可读性。
- 类型与校验分层采用组合方案：`cli_app/types.py` 用 **pydantic** 承接来自 GitHub Actions/ENV/CLI flags 的“外部输入解析与校验”；`cli_app/scenarios/*` 内部执行层使用 **dataclasses**（或普通函数参数）承载运行期上下文，保持轻量。
- 一句话选择：当你要把“外部世界的字符串泥浆”变成“类型干净、可审计的 config”，选 pydantic；当你只是在内部打包数据、不做复杂外部输入校验，选 dataclasses。

## Background

近期 `cli.py` 演进到 **8000+ 行**后，在你处理 drill/workflow/cli 相关任务时，Copilot Chat/Agent 很容易将其识别为“核心入口文件”并尝试整段读取或检索引用，导致：

- 上下文体积暴涨（请求体像“巨鲸”一样膨胀）
- 交互出现超时（例如 408）

这不是需要回退功能的问题，而是需要对 CLI 做结构化拆分，使其更符合“稳定证据链（evidence contract）+ drills/runbook”的工程形态。

## Problem / Malfunction

- **症状**：Copilot Chat/Agent 在 drill/workflow/cli 问题上频繁超时、响应不稳定。
- **根因**：入口文件过大且承担了大量场景逻辑，工具侧倾向把它当作“关键上下文”进行整段加载/检索，从而触发请求体/上下文限制。
- **风险**：
  - 为了“能聊下去”被迫减少上下文或改问法，影响效率。
  - 入口文件继续增长，拆分成本随时间上升。
  - workflow 继续集中化后变成“航天飞机控制面板”，难维护、难排错。

## What/How to do（落地规则）

### 1) 目标架构：薄 CLI + 场景插件化

目标是让 `cli.py` 只做三件事：

- 解析参数
- 选择 scenario/command
- 调用对应模块函数（并处理 exit code + artifacts 输出）

推荐目录（示例）：

```
backend/scripts/
  cli.py                 # 100~300 行：入口壳（parser + dispatch）
  cli_app/
    __init__.py
    common.py            # run_id、paths、artifacts contract、logger setup
    registry.py          # scenario 注册表（字符串 -> handler）
    types.py             # dataclasses / pydantic configs
    scenarios/
      __init__.py
      shadow_verify_shared_keys.py
      shadow_verify_paging_stability.py
      shadow_verify_search_index_write_gate.py
      dual_run_window.py
      canary_dual_write.py
    labs/
      shadow_verify.py
      failure_drills.py
      collector_down.py
```

拆分标准（避免拆歪）：

- 一个 scenario 一个文件
- 一个文件暴露一个 `run(config) -> Result`
- artifacts contract（例如 `_result.json` / `summary.json` / `meta.json` / `zip`）统一封装在 `common.py`
- `cli.py` 里只保留 `parser + registry.get(scenario).run(cfg)`

补充：为什么这个项目更适合 pydantic（入口层）

你的 CLI/drill 场景有几个典型特征：

- 输入来自：GitHub Actions `workflow_dispatch`、ENV、CLI flags（都是外部输入）
- 你非常重视：failure contract / artifacts contract / 可重现证据链
- 你需要：UUID/int/bool/enum 这类类型从字符串稳定解析
- 你会做：范围约束（例如 max_writes）、window 参数、timeout、sampling 与语义校验

这些几乎就是 pydantic 的主场。因此建议采用“工程上最舒服”的组合拳：

- `cli_app/types.py`：用 pydantic 定义 `InputModel`（CLI/ENV/JSON 的入口）
- `cli_app/scenarios/*`：内部逻辑用 dataclasses（或普通函数参数）承载执行期上下文，避免把执行层绑死在 pydantic 上

### 2) 最小可行拆分顺序（不改行为，只减体积）

按下面顺序做，风险最低：

- **Step A：先抽出 artifacts contract**（立刻减几百行）
  - 把写 `_result.json`、写 `summary.json`、打包 zip、`meta.json` 等移动到 `cli_app/common.py`
  - 从此 `cli.py` 不再关心这些细节
- **Step B：按 scenario 搬家**（每搬一个就删一坨）
  - 从最常跑的 verify 场景开始（例如 shared keys / paging stability）
  - 每搬一个：本地跑一遍 + GitHub Actions 跑一遍，确保行为一致
- **Step C：再搬 window/canary 等更容易“长胖”的场景**
  - dual run window
  - canary dual write

### 3)（可选）workflow 拆分建议

如果当前存在“一个 workflow 承载多个 scenario”的聚合配置，建议两种姿势二选一：

- **姿势 1：一个 scenario 一个 workflow**（最清晰）
  - 优点：inputs 少、超时/权限/环境隔离清楚、artifact 更聚焦、排错更快
  - 缺点：workflow 数量增多（但通常是可接受的工程成本）
- **姿势 2：入口 workflow + reusable workflow_call**（更工程化）
  - 外层负责选择 scenario/输入参数
  - 内层复用执行模板

## Next

- 先落地“Step A：抽 artifacts contract”，快速把入口文件降维。
- 然后按“最常跑的 verify 场景”优先级逐个迁移。
- 若 CI 复杂度/排错成本仍高，再拆 workflow（优先采用“一个 scenario 一个 workflow”先落地）。

## Implementation Status（当前落地情况）

已落地（代码中已存在）：

- `backend/scripts/cli_app/common.py`：evidence paths + `write_json`/`zip_directory` 等基础能力
- `backend/scripts/cli_app/parser.py`：argparse surface 单一事实来源（命令/参数/help 定义集中）
- `backend/scripts/cli_app/callbacks.py`：`_cmd_labs_*` 回调集中注册（保持 key 稳定，入口进一步变薄）
- `backend/scripts/cli_app/types.py`：`DrillInputs` / `DrillResult` 输入输出边界
- `backend/scripts/cli_app/registry.py`：scenario 注册表 + `load_builtin_scenarios()`
- `backend/scripts/cli_app/scenarios/*`：已迁移并可注册的场景模块（供 registry/handlers 使用）：
  - `shadow_verify_canary_dual_write`
  - `shadow_verify_chronicle_entries`
  - `shadow_verify_dual_write_sampling`
  - `shadow_verify_search_index`
  - `shadow_verify_search_index_write_gate`
  - `shadow_verify_search_index_paging_stability`
  - `shadow_verify_shared_keys`
  - `shadow_verify_dual_run_readiness_gate`
  - `shadow_verify_dual_run_stage1`
  - `shadow_verify_dual_run_stage2`
  - `shadow_verify_dual_run_window`
- `backend/scripts/cli_app/labs/*`：已落地的“命令簇实现侧”（`cli.py` 对其薄委托）：
 - `backend/scripts/cli_app/labs/*`：已落地的“命令簇实现侧”（`cli.py` 对其薄委托）：
  - `failure_drills.py`
  - `collector_down.py`
  - `jaeger_export.py`
  - `shadow_verify.py`

仍在进行（与本文目标一致，但未完全收口）：

- `backend/scripts/cli.py` 已显著收口为 **dispatch-only 薄入口**：
  - argparse surface 已抽离到 `backend/scripts/cli_app/parser.py`
  - `_cmd_labs_*` 回调集中注册已抽离到 `backend/scripts/cli_app/callbacks.py`
  - 当前行数约 **112 行**（已不再受“入口过大导致上下文膨胀/超时”的主要风险影响）
- Step A（artifacts contract 全量收敛）仍需持续推进：目前已有 `cli_app/common.py::pack_artifacts()`，但并非所有 legacy 命令都已统一切到同一套写盘/打包路径（需要按命令簇逐步收敛）

## References

- `backend/scripts/cli.py`
- `backend/scripts/cli.py` 所承载的各 drill/scenario 命令
- 相关 workflow：`.github/workflows/*`（若存在聚合型 drill workflow）