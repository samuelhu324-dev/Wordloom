# run-S4A-4A-hybrid-runtime-awareness

---

**id**: `S4A-4A-hybrid-runtime-awareness`
**kind**: `runbook`
**title**: `Hybrid runtime awareness (local dev/test, Vercel demo, WSL vs Windows)`
**status**: `draft`
**scope**: `S4A-4A`
**decision_date**: `2026-03-21`
**context_issue**:
  **DoD**: `S4A-4A P0–P3`
  **Labs**: `Vercel demo deployment, local dev/test ops baseline, WSL2 vs Windows dev tooling`
**decision**: `Provide a thin, operator-facing guide to reason about and verify hybrid runtime behavior for the Wordloom demo route (/demo) and dev tooling across WSL2 and Windows PowerShell.`
  **positive**: `Clear local vs cloud behavior examples, concrete dev shell/tooling contrast, reusable checklist for common hybrid issues`
  **negative**: `Does not implement full multi-cloud runtime management, limited to current repo + Vercel + local dev tooling`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 帮助 systems/platform operations 在以下场景下有一套可复述、可检查的 hybrid runtime 视角：
  - 同一条 `/demo` 入口，在本地 dev/test 与 Vercel 部署上的静态资源行为不一致；
  - 同一份前端代码，在 WSL2 dev shell 下可以启动，而在 Windows PowerShell + `npm run dev:dev` 下失败。
- 为值班/运行支持提供最小 checklist：
  - 如何判断“这是 hybrid runtime 问题（配置/构建/工具链差异）而不是纯业务 bug”；
  - 在哪里看 config / logs / HTTP 行为差异来支撑结论。

## 2) Scope

- 覆盖内容：
  - 本地 dev/test 前端（Next.js app router）与 Vercel demo 部署（`/demo` 路由）的对比；
  - WSL2 + bash + `scripts/ops/start.sh` vs Windows PowerShell + `npm run dev:dev` 的 dev tooling 对比；
  - 使用轻量证据：HTTP 响应头/体快照、stderr 片段、health check 结果，而非完整 JSON drills。
- 不覆盖内容：
  - 全量云产品矩阵、多云路由、统一配置平台；
  - 生产级日志聚合与 observability 方案；
  - 它们只在 `S4A-4A` 的 contract 中被提到为未来扩展方向。
- 关键参考：
  - [docs/logs/log-S4A-4A-hybrid-runtime-awareness.md](docs/logs/log-S4A-4A-hybrid-runtime-awareness.md)
  - [docs/demo/VERCEL-DEPLOY.md](docs/demo/VERCEL-DEPLOY.md)

## 3) Evidence Bundle (lightweight)

### 3.1 HTTP behavior snapshots

- 本地 dev/test 与 Vercel demo 的 `/demo` 静态资源对比：
  - 记录下列 URL 的 HTTP 行为差异（至少选 1–2 个）：
    - 本地：`http://localhost:<dev-port>/demo/DEMO-main-content-model.png`
    - 云端：`https://<your-wordloom-site>.vercel.app/demo/DEMO-main-content-model.png`
  - 关注字段：
    - `status`（是否 200）；
    - `Content-Type`（`image/png` vs `text/plain` 等）；
    - `Content-Length` 或近似 size（几十 KB–MB vs 几十字节）；
    - body 前几行（正常二进制不能直接读，LFS pointer 则是带 `version https://git-lfs.github.com/spec v1` 的文本）。

### 3.2 Dev tooling behavior snapshots

- WSL2 vs Windows PowerShell dev env：
  - 记录以下命令的退出码与 stderr 片段：
    - WSL2（bash）：`./scripts/ops/start.sh dev all --no-worker` + `./scripts/ops/health.sh dev`；
    - Windows PowerShell：在 repo 根或 frontend 目录下执行 `npm run dev:dev`，再用 `bash scripts/ops/health.sh dev` 观察前端健康情况。
  - 关注点：
    - WSL2 路径下，start/health 是否成功；
    - Windows 路径下，是否出现 `cross-env` 或 PATH 相关错误，health 是否失败。

## 4) Check 1 — Vercel demo static assets vs local dev/test

### 4.1 Local dev/test

- 前置：
  - 已按照 README 或 S4A-1A / S4A-2A runbook 启动本地前端 dev/test 环境；
  - 记下前端端口（示例：`http://localhost:30001` 或 `http://localhost:31002`）。
- 步骤：
  1. 打开本地 `/demo` 页面：
     - 浏览器访问 `http://localhost:<dev-port>/demo`；
     - 期望：页面文字与截图/视频区都正常渲染。
  2. 检查至少一个静态资源：
     - 例如：`http://localhost:<dev-port>/demo/DEMO-main-content-model.png`；
     - 使用浏览器 devtools 或 curl 记录：
       - `status` 应为 200；
       - `Content-Type` 类似 `image/png`；
       - `Content-Length` 较大（几十 KB 以上）。

### 4.2 Vercel demo deployment

- 前置：
  - 已根据 [docs/demo/VERCEL-DEPLOY.md](docs/demo/VERCEL-DEPLOY.md) 配置并部署项目；
  - 记下 Vercel 站点域名，例如：`https://wordloom-v3.vercel.app` 或自己的自定义域。
- 步骤：
  1. 打开云端 `/demo` 页面：
     - 浏览器访问 `https://<your-wordloom-site>.vercel.app/demo`；
     - 观察媒体区域是否正常显示截图与视频预览。
  2. 检查与本地相同的静态资源：
     - 例如：`https://<your-wordloom-site>.vercel.app/demo/DEMO-main-content-model.png`；
     - 使用浏览器 devtools 查看：
       - `status` 是否为 200；
       - `Content-Type` 是否为预期图片类型；
       - `Content-Length` 是否与本地量级相近。
  3. 若怀疑出现 Git LFS pointer：
     - 通过 “在新标签页打开图片” 或 curl 下载响应体，检查前几行是否为：
       - `version https://git-lfs.github.com/spec v1`
       - `oid sha256:...`
       - `size ...`

### 4.3 Interpretation

- 若本地行为正常而 Vercel 上出现 LFS pointer 文本：
  - 这说明构建/部署管线对 `frontend/public/demo/**` 的 LFS 资源处理不完整；
  - operator 动作：
    - 检查 [.gitattributes](.gitattributes) 中针对 demo 资源的 LFS 配置；
    - 检查 Vercel 项目设置 / CI 流程中是否有 `git lfs install` / `git lfs pull` 或等价步骤；
    - 评估是否需要将公开 demo 媒体从 LFS 改为常规 Git 文件，减轻云端依赖。
- 若本地和 Vercel 都正常：
  - 说明当前 hybrid 行为健康；可在 S4A-4A Evidence 区记录一次“正常样本”。

## 5) Check 2 — WSL2 dev shell vs Windows PowerShell dev tooling

### 5.1 WSL2 baseline

- 步骤：
  1. 在 WSL2 终端内：
     - `cd /mnt/d/Project/wordloom-v3`；
     - `./scripts/ops/start.sh dev all --no-worker`；
  2. 等待服务拉起后，运行：
     - `./scripts/ops/health.sh dev`；
  3. 期望：
     - `start.sh` 与 `health.sh` 退出码均为 0；
     - health 输出显示前端/后端/DB 等组件处于 healthy 状态。

### 5.2 Windows PowerShell + npm dev

- 步骤：
  1. 在 Windows PowerShell：
     - `cd D:\Project\wordloom-v3` 或 `cd D:\Project\wordloom-v3\frontend`；
     - 运行：`npm run dev:dev`；
  2. 另开一个终端窗口，在仓库根目录执行：
     - `bash scripts/ops/health.sh dev`；
  3. 观察：
     - `npm run dev:dev` 是否失败并打印 `cross-env` 或 PATH 相关错误；
     - `health.sh dev` 是否无法通过前端健康检查。

### 5.3 Interpretation

- 若 WSL2 路径成功而 Windows PowerShell + npm 路径失败：
  - 说明当前 dev tooling 在不同 shell/runtime 下存在差异；
  - operator 动作：
    - 优先推荐 WSL2 + bash + `start.sh` 作为标准 dev path；
    - 如确有需要在 Windows 原生路径下运行：
      - 确认 `node_modules/.bin` 在 PATH 中；
      - 如缺失 `cross-env`，可在 frontend 目录执行 `npm install --save-dev cross-env`；
      - 或为 Windows 增加一个薄包装脚本，统一调用 WSL2 侧 `start.sh`。

## 6) Troubleshooting

- 症状：Vercel `/demo` 页面文字正常，但截图/视频全部空白或报错。
  - 动作：
    - 按 4.2 / 4.3 步骤检查静态资源请求；
    - 如看到 Git LFS pointer 文本，优先检查 `.gitattributes` 与构建/部署管线；
    - 如静态资源本身 404，则检查 Next basePath / vercel.json / 部署路径配置。
- 症状：本地和 Vercel `/demo` 正常，但 API 路由异常（与本 runbook 无关）。
  - 动作：
    - 参考 S4A-2A / 相关 ADR 中的 API proxy / backend 集成说明；
    - 本 runbook 仅关注 demo 静态资源与 hybrid 行为。
- 症状：在 Windows PowerShell 下反复 `npm run dev:dev` 失败，health 也失败。
  - 动作：
    - 检查 `node_modules/.bin` 是否存在 `cross-env`；
    - 运行 `Get-ChildItem node_modules\.bin\cross-env*` 确认二进制是否就位；
    - 如缺失，`npm install --save-dev cross-env`；
    - 仍不稳定时，回退到 WSL2 + `start.sh` 路径作为主 dev 方式。

## 7) Notes and Boundaries

- 本 runbook 仅作为 hybrid runtime awareness 的 v1：
  - 展示了“本地 vs 云”与“WSL2 vs Windows dev tooling”两类差异的代表性样本；
  - 不试图覆盖所有可能的 runtime 组合。
- 当问题超出本 runbook 范围时（例如：
  - 复杂的多云流量调度；
  - 生产级日志聚合与审计；
  - 涉及安全策略、secret 管理、合规性），
  - 应回到 S4A spine 以及 `S5A` / `S5B` / `S6A` 等相关 phase 设计。