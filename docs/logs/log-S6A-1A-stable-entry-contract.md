# log-S6A-1A-stable-entry-contract（P1：Stable Entry contract｜入口漂移零容忍 v1）

---

**id**: `S6A-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `stable entry contract for fault drills (centralize worker spawn + env wiring) v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, FailureContract, Scenarios, Worker, CLI, epic/s6, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_1**: `docs/logs/log-S2B-1A-failure-contract-v1.md`
  **reference_log_2**: `docs/logs/log-S2B-2A-failure-contract-v2.md`
  **reference_log_3**: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
**created**: `2026-03-04`
**updated**: `2026-03-04`

---

## Decision / Outcome（结论区）

**Decision**:

- 将 `fault/obs_infra/*`（以及同类 fault scenarios）的 worker 启动方式收口为一个“稳定入口 contract”：**禁止在场景里硬编码 worker 路径/命令行**。
- 将 “worker spawn + env wiring（环境变量拼装）” 集中到共享 helper，作为 drills 的稳定面：未来 refactor/迁移不应再打断 drills。

**Default choices（v1 默认）**:

- 稳定入口以 **repo 内脚本**为准（当前 baseline：`backend/scripts/search_outbox_worker.py`）。
- 场景只描述“意图”（要启动哪个 worker / 要注入哪些 knobs），helper 负责拼装命令、统一超时、统一日志与退出码语义。

## Constraints（约束）

- 不引入第二套入口：helper 只是“拼装与约束层”，不替代既有的 worker 主脚本。
- 不扩大场景 UX：不新增额外参数/花活；先保证“入口不漂移 + 可复用 + 易排障”。
- 证据优先机器可判定：场景失败时的最小输出需能被 runner/CI 采集（见 Evidence contract）。

## Scope（本 log 范围）

- `P0`：contract（稳定入口 + helper 接口 + 迁移规则 + 证据口径）
- `P1`：实现 helper（spawn + env wiring）并迁移至少 1 个场景作为样板
- `P2`：将 `fault/obs_infra/*` 场景全量迁移到 helper（做到入口漂移零容忍）

## Success Criteria（DoD）

- 所有 `fault/obs_infra/*` 场景：不再直接拼 `python .../search_outbox_worker.py` 或硬编码路径；统一调用 helper。
- helper 具备最小能力：
  - 统一 cwd（repo root）
  - 统一 env 合并（继承进程 env + 场景覆盖）
  - 统一超时与退出码处理
  - 统一日志落地（stdout/stderr 至少可被 artifacts 收集）
- 有 1 份可追溯 evidence：
  - headSha + 至少 1 次 drill artifacts 路径（或 CI run URL）

## Stability（stable 口径）

- 本 log 标记为 `stable` 的最低门槛：
  - helper 已落地，并被 `fault/obs_infra/*` 全量复用
  - 入口漂移的历史坑（路径不存在/命令不一致）在代码结构上被制度化规避
  - 至少 1 个场景在 CI 中可重复跑通（失败也能自解释：能定位是 worker 没起来、还是依赖故障注入没生效）

## P0（Contract｜v1）

### P0-C1-S1（Stable Entry contract｜v1）

- 场景代码中：
  - **禁止**硬编码 worker 文件路径（例如 `backend/.../worker.py` 的字符串拼装）。
  - **禁止**在每个场景里复制粘贴一套 `subprocess.Popen`/`asyncio.create_subprocess_exec` 逻辑。
- 场景代码应调用：共享 helper（见 P0-C1-S2），并只提供：
  - worker 类型（当前：search outbox worker）
  - 场景需要的 env 覆盖（knobs）
  -（可选）启动后 readiness 等待策略（最小：sleep/health probe；后续演进）

### P0-C1-S2（Helper interface｜v1）

- helper 的职责边界：
  - 负责拼装 worker command（稳定入口脚本 + 参数）
  - 负责 env 合并、timeout、日志重定向与退出码处理
  - 返回一个可被 verify 使用的句柄/结果（例如 pid、log 路径、退出原因）
- helper **不**负责：
  - 注入故障的业务逻辑（那是 scenario 本身）
  - 替代 worker 的核心实现

### P0-C1-S3（Evidence contract｜v1）

- 每个场景在 run/verify 的最小 evidence 中应包含：
  - 使用的 worker “stable entry id”（例如 `search_outbox_worker@v1`）
  - helper 输出的 worker 启动摘要（命令、env keys、pid、log 路径）
  - PASS/FAIL 的判定要点（至少 1 条可机器判定的断言来源：DB/metrics/artifacts）

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。

**Commit / PR 命名**:

- `S6A-1A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P1（实现 helper + 样板迁移）

- P1-C1-S1：创建 helper（spawn + env wiring + timeout + logs）
- P1-C1-S2：迁移 1 个代表性场景（建议：`es_429_inject` 或 `collector_down`）
- P1-C1-S3：补齐最小 evidence 输出（写入 artifacts JSON 或 runner 可采集位置）

### P2（全量迁移 + hardening）

- P2-C1-S1：`fault/obs_infra/*` 场景全量替换为 helper 调用
- P2-C1-S2：统一 readiness 等待策略（最小可用即可）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：Stable Entry contract（禁止路径硬编码）
- [x] `P0-C1-S2`：Helper interface（职责边界）
- [x] `P0-C1-S3`：Evidence contract（最小字段）

### P1（实现 + 样板）

- [x] `P1-C1-S1`：helper 落地（spawn + env + logs + timeout）
- [x] `P1-C1-S2`：迁移 1 个场景（样板：`es_429_inject`）
- [x] `P1-C1-S3`：产出 1 份可追溯 evidence（见下方 Evidence；本次 run 因 inserter timeout 失败，但证据可自解释）

### P2（全量迁移）

- [ ] `P2-C1-S1`：`fault/obs_infra/*` 全量迁移
- [ ] `P2-C1-S2`：readiness 策略统一

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + 关键参数 + artifacts 路径（或 CI run URL）。

### P1-C1-S3（sample scenario migrated｜2026-03-04）

- headSha：`3766bd7b`（S6A-1A/P1-C1-S1: centralize worker spawn helper）
- scenario：`es_429_inject`
- run_dir：`docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/20260304T195127/`
- result：`docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/20260304T195127/_result.json`
- worker entry：`search_outbox_worker@v1`（见 `_worker_start.json` / `_result.json.worker`）
- helper logs：`docs/labs/_snapshot/auto/S3A-2A-3A/es_429_inject/20260304T195127/_logs/worker-20260304T195127.log`
- expected：
  - inserter 成功插入 outbox event；worker 消费；metrics delta 满足 verify 阈值
- observed：
  - inserter 超时：`_trigger_insert_outbox.timeout.txt`
  - verify 结果：`ok=false`（metrics delta 为 0）

## Recent changes（for traceability，可选）

- 2026-03-04：在 P0 修复中已将若干场景的 worker 入口统一到稳定脚本；本切片把该修复制度化为 helper + contract。
