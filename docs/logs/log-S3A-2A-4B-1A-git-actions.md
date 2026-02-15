# Log-S3A/2A/4B：automation/failure-drills-&-gitactions-&-dashboard

---

**id**: `S3A-2A-4B`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `automation/failure drills & git actions & dashboard`
**status**: `stable`          # draft | stable | archived
**scope**: `S3A`
**tags**: `EVOLOTION, Observability, lab, sub/3`
**links**: ``
  **issue**: `#49`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-14`
**updated**: `2026-02-15`

---

## Background

本文聚焦“同一套演练/脚本在本地可跑，但在 GitHub Actions 里跑不通/不一致”的典型差异源与对齐方法。

约束：这里先沉淀可复用的排查与对齐框架；`**archived**` 后续再补齐。

## Malfunction

**draft**:

- 现象：本地跑 OK，Actions 跑失败或结果不一致。
- 影响：导致 failure-drills 的“按钮化回归入口”不可复验、难以交接。

**stable**:

- 结论：本地与 GitHub Actions 的关键差异已被“单一入口 + CI 自包含”消除；failure-drills 支持 `scenario=all` 端到端跑通（run→verify→export→clean），并稳定上传证据包 artifact。

**archived**:

## What/How to do

1) 先搞清楚：它们到底哪里不一样（最常见 8 个差异源）

**draft**:

A. 工作目录不同

Actions 默认在 GITHUB_WORKSPACE，但你脚本可能假设在 repo 根目录 / 或者在 backend/。

解决：每一步显式 working-directory: 或 cd.

B. Shell 不同（WSL/bash vs ubuntu bash vs powershell）

Copilot 你可能是 WSL bash；Actions 是 ubuntu bash（或 windows runner）。

解决：统一跑 ubuntu-latest，并在 steps 里指定 shell: bash。

C. 环境变量来源不同

Copilot workspace 可能自动加载了 .env.test、你本机 shell profile、甚至你之前 export 过的变量。

Actions 默认不会自动读 .env*。

解决：Actions 里明确 source .env.test 或用 --env-file（docker compose）或写进 $GITHUB_ENV。

D. 依赖安装不同

Copilot workspace 可能残留 pip/npm 缓存、editable install、本地全局包。

Actions 是干净机器。

解决：workflow 里固定安装步骤（pip/poetry/uv、pnpm/npm）、并锁版本（requirements/lockfile）。

E. 服务依赖不同（DB/ES/Jaeger/Collector）

Copilot 可能你本机 docker compose 已经起着；Actions 里啥都没有。

解决：Actions 用 services:（postgres/elastic）或 docker compose up -d。

F. 网络/端口/host 不同

Copilot 里你访问 localhost:4318 OK；Actions 里容器间要用 service name。

解决：在 Actions 里用 http://<service>:port，别用 localhost（除非同一进程）。

G. 权限/密钥不同

Copilot 可能能读你本机的私密配置；Actions 里需要 secrets。

解决：所有 token、密码走 secrets + env: 注入。

H. 时间/随机性

实验依赖时间窗口 lookback、timestamp、随机 UUID → 两边结果自然不同。

解决：实验脚本增加 --seed、--freeze-time 或固定 lookback。

**stable**:

- 统一入口与执行环境：workflow 固定 `ubuntu-latest` + `bash`，并显式从 repo root 执行（避免 cwd 假设）。
- 环境变量来源：CI 自动生成并 `source` `.env.test`（且对输入 `env_file` 做存在性兜底），避免“本地自动加载 .env*、CI 不加载”的分叉。
- 服务依赖：CI 通过 `docker compose` 自包含启动 DB/ES/Jaeger，并在运行 labs 前等待依赖 ready + 执行 alembic migrate。
- 网络与端口：CI 侧统一通过 `localhost` 端口映射访问容器服务（与 `.env.test` 保持一致）。

**archived**:

2) “咋搞”：用一个“单一真相入口”把两边统一起来

**draft**:

你现在最缺的是：同一个入口，在本地/Actions 都能跑出同样效果。

做法：建一个 repo 级的 单一入口脚本，比如：

backend/scripts/cli.py（你已经有了）

或 backend/scripts/run_failure_drill.sh

要求它做到：

- 自己定位 repo root（不依赖当前目录）
- 明确加载 env（.env.test/.env.ci）
- 明确启动依赖（可选：检查 DB/ES/Collector 是否可达）
- 运行实验：lab run + lab verify
- 输出 artifacts 到固定目录 artifacts/

然后：

- Copilot：只运行这个入口
- Actions：也只运行这个入口

这样你就不会出现“Copilot 跑的是 A 路径，Actions 跑的是 B 路径”。

**stable**:

- 单一真相入口已收敛到 `backend/scripts/cli.py`（`labs run/verify/export/clean <scenario>`）。
- GitHub Actions 只调用这一入口（不再拼散落脚本与相对路径），并在 `scenario=all` 时循环跑完 A–H。

**archived**:

3) 在 Actions 里加一个“环境指纹打印”（10 分钟定位分叉点）

**draft**:

在 workflow 里加一个 step，直接把差异打印出来：

- pwd
- ls
- python --version
- pip freeze | head
- env | sort | grep -E 'WORDLOOM|OTEL|DATABASE|ELASTIC|ENV'
- cat .env.test | sed（注意别泄露敏感）
- curl -sS http://localhost:4318（或 service name）
- docker ps（如果用 compose）

然后把这些输出写进 $GITHUB_STEP_SUMMARY，你点进一次 run 就能看到“Actions 到底在啥环境里”。

**stable**:

- 已在 workflow 中落地 `Environment fingerprint (CI)`：把 `pwd/versions/pip-freeze(head)/关键 env(脱敏)/.env.test(脱敏)/docker ps/compose ps/endpoint probe` 写入 `GITHUB_STEP_SUMMARY`。
- 目标：一次 run 即可肉眼确认“Actions 到底在什么环境/依赖状态下运行”。

**archived**:

4) 你现在最可能踩的坑（结合你前面的观测链）

**draft**:

结合你之前的情况（OTLP 4317/4318、Collector 可达性、搬家后路径变化），我赌概率最高的是这三类：

- Actions 没加载 .env.test，导致 tracing/metrics/endpoint 和你本机不一致
- Actions 没把 Jaeger/Collector/ES/DB 起起来，你本机起着所以 Copilot 跑“对”
- 工作目录/路径被搬家后变化，Copilot 用你本机相对路径凑巧能跑，Actions 严格失败

**stable**:

- `.env.test` 缺失 / 未加载：已通过“CI 生成 + 显式 source”解决。
- 依赖未起 / 未 ready：已通过 compose up + wait + migrate 解决。
- 路径与工作目录漂移：已通过“默认 repo root 执行 + 单入口”解决。
- 时序/竞态导致 verify flaky（例如 scrape delta）：对关键场景补了更可解释的失败输出；`collector_down` 进一步增加 DB 兜底断言以降低 CI 抖动。

**archived**:

5) 你应该用的“对齐策略”（最省脑）

**draft**:

我建议你选一个最稳的路线：

路线 1：本地和 CI 都用 docker compose（最一致）

- 所有依赖（db/es/jaeger/collector/api/worker）都在 compose
- Copilot、Actions 都执行同一套 compose + 同一条 cli
- 优点：一致性最高
- 缺点：CI 会慢一点

路线 2：CI 用 services，本地随意（更快但容易分叉）

- CI 用 services: 起 postgres/es
- jaeger/collector 可选（或只跑不需要 tracing 的场景）
- 你要花更多力气维护“本地/CI 两套差异”

你现在在做“失败演练资产化”，我会选路线 1（少掉头发）。

**stable**:

- 已选并落地“路线 1：本地与 CI 都用 docker compose 起依赖”，CI 侧不依赖外部常驻环境。

**archived**:

6) 立刻可执行的最小修复（不改架构也能救）

**draft**:

你可以先做这 3 件事（立刻显著一致）：

- workflow 固定 shell: bash + 固定 runner ubuntu-latest
- 显式加载 env：set -a; source .env.test; set +a（把 env 文件全 export）
- 所有命令都从 repo root 跑：不要依赖“我当前在 backend/”

入口脚本里自己 cd "$(git rev-parse --show-toplevel)"

你现在不用猜。把你 failure-drills.yml 里“运行实验”的那几步（steps 部分）贴出来，我可以直接指出是哪一个差异源在作妖，并给你一版对齐 Copilot/本地/CI 的最小改动（通常 10～20 行就够把世界线合并）。

**stable**:

- workflow 统一 runner/shell：job 默认 `bash`。
- 显式加载 env：`source $env_file` 后再运行 labs。
- 固定从 repo root 执行：避免相对路径与 cwd 假设。
- 自包含依赖：compose 起 DB/ES/Jaeger + ready wait；并执行 `alembic upgrade head`。
- 结果：`scenario=all` 可完整跑通并上传证据包 artifact。

**archived**: