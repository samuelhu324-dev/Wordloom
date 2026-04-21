# run-S4A-3A-backup-recovery-operator-path

---

**id**: `S4A-3A-backup-recovery-operator-path`
**kind**: `runbook`
**title**: `Backup / recovery / disaster readiness operator path (dev/test)`
**status**: `draft`
**scope**: `S4A-3A`
**decision_date**: `2026-03-21`
**context_issue**:
  **DoD**: `S4A-3A P0–P3`
  **Labs**: `S5A-3A / S5A-3B drills, S6A evidence spine`
**decision**: `Provide a thin, operator-facing entry to run and verify a backup+restore+sanitize drill in dev/test using existing S5A-3A/3B tooling and S6A evidence semantics.`
  **positive**: `Repeatable operator entry, machine-verifiable evidence, clear dev/test-only boundaries`
  **negative**: `Extra maintenance for commands and evidence paths, does not cover production RPO/RTO`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 帮助 systems/platform operations 在本地 dev/test 环境下完成一件事：
  - 证明“我们最近至少有一条从 backup -> object storage -> restore+verify -> sanitize+verify 的可演练路径”。
- 为值班/运行支持提供最小入口：如何触发一次样例性质的 `backup_pipeline_drill`，以及在哪里查看 drills/evidence JSON。
- 不重新实现 backup 平台，只是把 `S5A-3A` / `S5A-3B` / `S6A` 的 drill 能力用 operator 语言包装成一条可复跑路径。

## 2) Scope

- 覆盖内容：
  - dev/test 环境下，基于 `docker-compose.devtest-db.yml` 与 MinIO 的数据库备份与恢复样本；
  - 使用现有 scripts：
    - `scripts/drills/s5a3a_p1c1s2_backup_drill.py`
    - `scripts/drills/s5a3b_p1c1s3_upload_drill.py`
    - `scripts/drills/s5a3b_p2c1s2_restore_verify_from_minio_drill.py`
    - `scripts/drills/s5a3b_p3c1s2_restore_sanitize_verify_from_minio_drill.py`
    - `scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`
  - 使用 `S6A` 的 evidence 语义记录 drills_json（低基数字段、明确 PASS/FAIL）。
- 不覆盖内容：
  - 生产环境数据库、跨 region、多租户、多 AZ 场景；
  - RPO/RTO 设计与容量规划；
  - 将 dev/test backup 直接推广为生产灾备方案。
- 关键参考：
  - `docs/logs/log-S4A-3A-backup-recovery-operator-path.md`
  - `docs/logs/log-S5A-3B-object-storage-backup.md`
  - `docs/logs/log-S6A-evidence-drills-spine.md`

## 3) Evidence Bundle

### 3.1 Output roots

- 主要 evidence 根目录：
  - `artifacts/_tmp_s5a3a_p1c1s2/`：本地 backup drill evidence（包括 dump 路径、sha256、size_bytes）。
  - `artifacts/_tmp_s5a3b_p1c1s3/`：upload drill evidence（bucket / dump_object_key / sha256 / size_bytes）。
  - `artifacts/_tmp_s5a3b_p2c1s2/`：restore+verify drill evidence（download + pg_restore + verify SQL）。
  - `artifacts/_tmp_s5a3b_p3c1s2/`：restore+sanitize+verify drill evidence（脱敏验证）。
  - `artifacts/_tmp_s5a3b_p4c1s1/`：pipeline drill 汇总 evidence（聚合上述各步骤配置与结果）。
- 最小检查集：
  - pipeline evidence：`artifacts/_tmp_s5a3b_p4c1s1/drills_<ts>.json`
    - `summary.bucket`
    - `summary.object_key`
    - `summary.sha256`
    - `summary.size_bytes`
    - `summary.p3_verify`（含脱敏验证 stats 与 failures）。

### 3.2 Summary or ledger

- 当前没有单独的 ledger 文件；每次 pipeline drill 会生成一份新的 `drills_<ts>.json`。
- 建议操作：
  - 保留最近几次 drills JSON，按文件名时间戳或 `meta.started_at` 排序；
  - 在 `log-S4A-3A-backup-recovery-operator-path.md` 的 Evidence 区记录关键样本（headSha + drills JSON 路径）。

## 4) One-click Automation

### 4.1 What it does

- 一条命令执行以下步骤：
  - 在 devtest DB 上运行 backup drill，生成本地 dump 与 backup evidence JSON；
  - 将 dump 上传到 MinIO 对象存储，记录 bucket / object_key / sha256 / size_bytes；
  - 从对象存储下载 dump，并恢复到 `wordloom_restore_dev` 数据库，执行最小 SQL verify；
  - 再从对象存储下载同一 dump，恢复到 `wordloom_restore_sanitized_dev`，执行脱敏与 verify；
  - 生成一份 pipeline evidence JSON，聚合上述各 drill 的 config 和结果，并在终端最后一行输出相对路径。

### 4.2 Operator instructions

- 入口命令（在仓库根目录）：
  - `python scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`
- 必要前置：
  - Docker 引擎已启动；
  - `docker-compose.devtest-db.yml` 和 `docker-compose.infra.yml` 可用；
  - devtest Postgres 端口（默认 5435）未被其他进程占用；
  - MinIO / MinIO mc 容器已按 repo 约定启动（通常通过 `scripts/ops/start.sh dev infra es` + `start.sh dev db` 间接拉起）；
  - Windows 上建议使用已配置好的 Python 解释器（例如本仓库的 system Python）运行命令。
- 运维可调参数（高级）：
  - 通过环境变量覆盖默认 bucket/prefix：
    - `WORDLOOM_S5A3B_BUCKET`
    - `WORDLOOM_S5A3B_PREFIX`
  - 如需仅跑局部 drill，可参考 phase log 中的拆分命令。
- 成功判定：
  - 命令退出码为 0；
  - 终端最后一行打印一条类似：`artifacts/_tmp_s5a3b_p4c1s1/drills_1774063161.json`；
  - 打开该 JSON，满足：
    - `summary.bucket` 与预期 devtest bucket 一致（如 `wordloom-backups-devtest`）；
    - `summary.object_key` 指向最近一次 dump；
    - `drills.s5a3a_backup.status` / `drills.s5a3b_upload.status` / `drills.s5a3b_restore_verify.status` / `drills.s5a3b_restore_sanitize_verify.status` 均为 `ok`；
    - `summary.p3_verify.failures` 为空数组；
    - `summary.p3_verify.stats` 中受控字段的 `non_redacted_count` 为 0。
- 失败判定：
  - 命令非 0 退出；
  - 或 evidence JSON 中任何一个 drill 的 `status` 不是 `ok`；
  - 或脱敏验证 `failures` 非空、`non_redacted_count` > 0。

## 5) Local Operation

### 5.1 Prerequisites

- OS：Windows + Docker Desktop；
- Shell：PowerShell（用于启动 Docker/MinIO，Python 命令同样可在 PowerShell 中运行）；
- 依赖：
  - Docker / docker compose
  - MinIO / MinIO mc（由 repo 的 infra compose 管理）
  - PostgreSQL 客户端在容器镜像中已内置
  - Python（与 repo 一致的版本）
- 建议先通过 `S4A-1A` / `S4A-2A` 的 runbook 确认本地 ops baseline 正常（env_prep / start / status / health）。

### 5.2 Commands

- 推荐完整演练：
  - 在仓库根目录：
    - `python scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`
- 如果需要拆分执行：
  - 本地备份：
    - `python scripts/drills/s5a3a_p1c1s2_backup_drill.py`
  - 上传到对象存储：
    - `python scripts/drills/s5a3b_p1c1s3_upload_drill.py`
  - 从对象存储恢复并验证：
    - 设置 `WORDLOOM_S5A3B_UPLOAD_EVIDENCE=<upload evidence 相对路径>`；
    - `python scripts/drills/s5a3b_p2c1s2_restore_verify_from_minio_drill.py`
  - 带脱敏的恢复：
    - 同样设置 `WORDLOOM_S5A3B_UPLOAD_EVIDENCE`；
    - `python scripts/drills/s5a3b_p3c1s2_restore_sanitize_verify_from_minio_drill.py`。

## 6) Troubleshooting

- 症状：pipeline drill 一开始就失败，stderr 提示 `docker compose up failed` 或端口已占用（如 5435）。
  - 动作：
    - `docker ps` 检查是否已有 devtest DB 容器占用端口；
    - 如有，先 `docker stop <相关容器>` 再重跑 pipeline drill；
    - 查看 `docker-compose.devtest-db.yml` 中端口映射是否与宿主机冲突。
- 症状：download 步骤失败或 evidence 中 `download` drill 不是 `ok`。
  - 动作：
    - 检查 MinIO 容器是否运行；
    - 检查 `WORDLOOM_S5A3B_BUCKET` / `WORDLOOM_S5A3B_PREFIX` 是否被错误覆盖；
    - 确认对象存储中存在对应的 dump；
    - 重跑 upload drill 生成新 evidence 后再试。
- 症状：restore 步骤失败，stderr 中出现 `pg_restore` 相关错误。
  - 动作：
    - 检查 devtest DB 容器日志；
    - 确认目标数据库名（`wordloom_restore_dev` / `wordloom_restore_sanitized_dev`）未被其他进程占用；
    - 必要时手动清理残留数据库后重试。
- 症状：pipeline 成功，但 `p3_verify` 中 `non_redacted_count` > 0 或 `failures` 非空。
  - 动作：
    - 这表示脱敏策略未完全覆盖现有数据；
    - 升级或修复脱敏 SQL 后，重新执行 pipeline drill，产生新的 evidence；
    - 在 `log-S4A-3A` 中记录新的 evidence 路径与结论。

## 7) Notes and Boundaries

- 本 runbook 仅作为 dev/test 场景下的 `disaster readiness sample`：
  - 证明“我们可以从最近一次样本备份恢复到新的 dev/test 库，并完成脱敏与验证”；
  - 不等同于生产级灾备方案。
- 不提供“就地恢复生产库”的一键脚本；
- 当需求涉及：
  - 生产 RPO/RTO；
  - 跨 region or 多 AZ 架构；
  - 多租户数据隔离；
  - 更严格的合规性要求；
  - 请回到 `S4A` spine / roadmap，与后续 phase 或其他 epic（如 `S5B` 安全治理）协同设计。
