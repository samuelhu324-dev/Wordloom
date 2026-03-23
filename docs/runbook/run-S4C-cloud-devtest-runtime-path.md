# run-S4C (Cloud-dev/test runtime path)

---

**id**: `run-S4C-cloud-devtest-runtime-path`
**kind**: `runbook`
**title**: `run/S4C-cloud-devtest-runtime-path`
**status**: `stable`
**scope**: `S4C`
**decision_date**: `2026-03-23`
**context_issue**:
  **DoD**: `S4C P3: wordloom-v3 local runtime can connect to cloud-dev RDS through a dedicated env and pass minimal smoke checks.`
  **Labs**: ``
**decision**: `Use a dedicated repo-root .env.cloud.dev plus Terraform-managed allowlist and Alembic migration as the canonical operator path for local runtime -> cloud-dev RDS drills.`
  **positive**: `"Repeatable operator entry", "Machine-verifiable evidence", "Stable troubleshooting path"`
  **negative**: `"Windows launcher differs from WSL path", "Operator must keep public IP allowlist and DB password fresh"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 给操作者一条最小、稳定、可重复的路径：从本机把 wordloom-v3 runtime 接到 AWS cloud-dev RDS，并验证 DB / API / app-level read 三层 smoke。
- 明确这条路径的三个组成部分：Terraform 网络白名单、repo-root `.env.cloud.dev` runtime config、Alembic schema migration。
- 提供 Windows 下的 canonical 命令序列和最有价值的故障排查入口。

## 2) Scope

- 覆盖内容：
  - cloud-dev RDS 的本机连通性验证；
  - Windows 下启动 API 的 canonical 命令；
  - cloud-dev schema migration；
  - 最小 app-level read smoke；
  - 白名单 IP 漂移、Region 误判、Windows event loop、未迁移 schema 等高频问题的处理。
- 不覆盖内容：
  - 生产级部署、remote Terraform state、bastion / SSM private access 路径；
  - 最小业务写入 smoke 与数据回收策略；
  - RDS 密码 rotation 的具体 AWS 控制台步骤。
- 深层历史与契约来源：
  - `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  - `docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
  - `infra/terraform/aws/network/main.tf`
  - `infra/terraform/aws/devtest-db/main.tf`

## 3) Evidence Bundle

### 3.1 Output roots

- 运行证据主索引：`docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
- 本地 env 配置入口：`.env.cloud.dev`
- DB smoke 工具：`backend/scripts/ops/cloud_dev_db_smoke.py`
- Windows API 启动入口：`backend/scripts/legacy/run_api_win.py`
- 关键最小证据：
  - DB smoke JSON（`ok/current_database/current_user/ping_ok`）
  - API health `200`
  - app-level read smoke `GET /api/v1/libraries -> 200`
  - Terraform allowlist apply 输出

### 3.2 Summary or ledger

- 本 scope 不单独维护 runbook ledger；
- 每次 cloud-dev drill 的最小摘要直接追加到 `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`；
- 最低字段：`headSha`、env 文件名、endpoint 类型、关键命令、结果摘要。

## 4) One-click Automation

- 当前无稳定 one-click 按钮或 wrapper；
- canonical operator path 仍然是本地 PowerShell 命令序列。

## 5) Local Operation

### 5.1 Prerequisites

- AWS 资源位于 `ap-southeast-2`；AWS Console 若切到其他 region（例如 `us-east-1`）会显示 `Databases (0)`，这不代表资源不存在；
- repo 根目录存在可用的 `.env.cloud.dev`，其中 `DATABASE_URL` 指向当前 live 的 `db_endpoint`；
- Windows Python 环境具备 `psycopg`、`SQLAlchemy`、`alembic`、`httpx`；
- Terraform 本地 state 已存在于：
  - `infra/terraform/aws/network/`
  - `infra/terraform/aws/devtest-db/`
- 若本机公网 IP 有变化，需要先更新 `infra/terraform/aws/network/terraform.tfvars` 中的 `allowed_postgres_cidrs`。

### 5.2 Commands

- 1. 如本机公网 IP 变更，先更新 PostgreSQL allowlist：

```powershell
Set-Location d:/Project/wordloom-v3/infra/terraform/aws/network
terraform apply -auto-approve
```

- 2. 验证 DB connectivity：

```powershell
Set-Location d:/Project/wordloom-v3
c:/python314/python.exe backend/scripts/ops/cloud_dev_db_smoke.py --env-file .env.cloud.dev
```

- 3. 迁移 cloud-dev schema：

```powershell
Set-Location d:/Project/wordloom-v3
Get-Content .env.cloud.dev | ForEach-Object {
  if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
  $name,$value = $_ -split '=',2
  [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim().Trim('"').Trim("'"), 'Process')
}
Set-Location backend
c:/python314/python.exe -m alembic -c alembic.ini upgrade head
```

- 4. Windows 下启动 API（canonical path）：

```powershell
Set-Location d:/Project/wordloom-v3
Get-Content .env.cloud.dev | ForEach-Object {
  if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
  $name,$value = $_ -split '=',2
  [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim().Trim('"').Trim("'"), 'Process')
}
[System.Environment]::SetEnvironmentVariable('PORT', $env:API_PORT, 'Process')
c:/python314/python.exe backend/scripts/legacy/run_api_win.py
```

- 5. 最小 app-level read smoke：

```powershell
Set-Location d:/Project/wordloom-v3
c:/python314/python.exe -c "import httpx; r=httpx.get('http://127.0.0.1:30021/api/v1/health', timeout=5.0); print(r.status_code); print(r.text)"
c:/python314/python.exe -c "import httpx; r=httpx.get('http://127.0.0.1:30021/api/v1/libraries', timeout=10.0); print(r.status_code); print(r.text[:1000])"
```

- 6. 停止与清理：
  - API：在 `run_api_win.py` 所在终端 `Ctrl+C`；
  - 若要回收临时公网 DB：进入 `infra/terraform/aws/devtest-db` 执行 `terraform destroy`；
  - 若要撤回白名单入口：进入 `infra/terraform/aws/network` 调整 `allowed_postgres_cidrs` 后再 `terraform apply`。

## 6) Troubleshooting

- 症状：AWS RDS 控制台显示 `Databases (0)`
  - 先检查右上角 region；本练习资源在 `ap-southeast-2`，若控制台停在 `us-east-1` 会看到空列表。

- 症状：`cloud_dev_db_smoke.py` 超时
  - 先看 `infra/terraform/aws/network/terraform.tfvars` 里的 `allowed_postgres_cidrs` 是否仍是当前公网 IP；
  - 再执行 `terraform apply -auto-approve` 把 SG allowlist 推到 AWS。

- 症状：Windows 下直接 `uvicorn ...` 启动失败，报 `ProactorEventLoop`
  - 不要直跑 `uvicorn`；改用 `backend/scripts/legacy/run_api_win.py`。

- 症状：`/api/v1/health` 返回 200，但业务 GET 返回 `relation ... does not exist`
  - 这说明网络通了，但 schema 还没迁移；执行 `c:/python314/python.exe -m alembic -c alembic.ini upgrade head`。

- 症状：startup 报 `InFailedSqlTransaction`
  - 当前仓库已修复 `backend/infra/database/env_guard.py`；若再次出现，优先检查是否回到了旧 commit 或未使用最新代码。

## 7) Notes and Boundaries

- 这份 runbook 是 operator path，不是 phase 历史备份；详细证据和演进原因仍以 `log-S4C-2A` / `log-S4C-3A` 为准。
- 当前 canonical path 假设本机 runtime 直连临时公网 RDS；未来若切换到 bastion/SSM/private access，应更新 runbook，而不是在这里叠加分叉命令。
- 下一步最自然的扩展点是最小业务写入 smoke，验证 cloud-dev runtime 的读写闭环；另一条并行收口项是尽快做 RDS password rotation。