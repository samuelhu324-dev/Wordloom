# run-S4B-1A (From-zero-to-dev/test runtime bring-up)

---

**id**: `run-S4B-1A-from-zero-to-devtest-runtime`
**kind**: `runbook`
**scope**: `S4B-1A`
**status**: `draft`
**related_log**: `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
**last_verified_headSha**: `f66aad9167757de2bb8dd6340a4aae984016832b`

---

## Scenario

- 目标：在一台已经具备 Docker Desktop + WSL2 的开发机器上，从零（没有容器在跑）把 `wordloom-v3` 的 dev/test runtime 拉起来，并用脚本检查健康。
- 适用环境：
  - Windows + Docker Desktop（启用 WSL2 integration）；
  - WSL2 Ubuntu（或等价发行版）。

## Preconditions

- 已安装：
  - Docker Desktop（WSL2 integration 打开）；
  - WSL2 Ubuntu，并可以访问互联网；
- Git 仓库：
  - 在 WSL 中已 clone `wordloom-v3` 至某个目录，例如 `/mnt/d/Project/wordloom-v3`；
- 配置：
  - 在 repo 根目录存在 `.env.dev`，且已填入最小必需字段（DB URL、API/ES 端口等）。

## Steps (from-zero-to-dev/test)

在 WSL 终端中：

1. 进入仓库根目录：

   ```bash
   cd /mnt/d/Project/wordloom-v3
   ```

2. 预备环境与依赖：

   ```bash
   ./scripts/ops/env_prep.sh dev
   ```

   - 说明：如出现端口占用告警（例如 api 端口），可以先参考“故障排查”进行清理，再重试；

3. 启动 infra 组件（ES 等）：

   ```bash
   ./scripts/ops/start.sh dev infra es
   ```

4. 启动 devtest 数据库：

   ```bash
   ./scripts/ops/start.sh dev db
   ```

   - 预期输出中应包含 `DB is healthy (localhost:5435)`。

5. 启动应用 runtime（不启 worker）：

   ```bash
   ./scripts/ops/start.sh dev app --no-worker
   ```

   - 预期：api + ui 进程正常启动，无端口冲突错误；

6. 检查 runtime 状态：

   ```bash
   bash scripts/ops/status.sh dev
   ```

   - 关键字段示例（理想状态）：
     - `db_container       healthy`
     - `infra_es           healthy`
     - `api_health         200`
     - `ui_http            200`
     - `es_http            200`

7. 运行 health 检查：

   ```bash
   bash scripts/ops/health.sh dev
   ```

   - 预期：exit code 为 0，并输出 db/api/ui/es 均 OK。

## Evidence

- 若需要为本次 bring-up 记录 evidence，可参考：
  - `artifacts/_tmp_s4b1a_from_zero_to_devtest.json`（首次 FAIL drill）；
  - `artifacts/_tmp_s4b1a_from_zero_to_devtest_v2.json`（第二次 PASS drill）；
- 建议在每次完整 from-zero-to-dev/test 演练后，记录：
  - `headSha`、`env`、`path_kind=from_zero_to_devtest`；
  - 执行的命令序列；
  - `status.sh` 摘要与 `health.sh` 结果；
  - 最终 `result=PASS|FAIL` 与简要 notes。

## Troubleshooting

- 端口占用（api/db）：
  - 使用 `ss -ltnp` 检查占用对应端口的进程；
  - 如为残留容器，可通过 `docker ps` / `docker stop` / `docker rm` 清理；
  - 必要时，使用 compose 的 `--remove-orphans` 清理孤儿容器后重试。
- DB 容器不健康：
  - 通过 `docker logs wordloom-devtest-db_devtest-1` 查看启动日志；
  - 确认 `.env.dev` 中的 DB 相关配置与 compose 定义一致。
- health.sh FAIL：
  - 先看 `status.sh dev` 输出，确认是哪一项探针不通过（db/api/ui/es）；
  - 针对对应服务检查容器状态、进程日志与端口占用。

## Notes

- 本 runbook 对应的 from-zero-to-dev/test 路径详情见：
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md` 中的 P2 描述与 Evidence 小节。
