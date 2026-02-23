# Labs Registry

快速入口：如何查找/填写 GitHub Actions suite 的 `scenario_id` → `../runbook/run-S0C-docs-management-v3.md`

目标：提供一个很轻量的“实验登记表”，解决“我到底有没有跑过 lab/test？”的焦虑。

约定：每个 lab 一行，关注四件事：目标、最近一次运行、CI workflow、状态。

| lab | 目标 | last run | CI workflow | status |
| --- | --- | --- | --- | --- |
| `lab-S3A-2A-3A-observability-failure-drills` | 失败观测演练菜单（metrics → trace → logs） | — | `.github/workflows/drill-failures.yml` | draft |
| `lab-S2B-1A-1A-shadow-chronicle-concurrent-handling` | Chronicle：shadow verify + read switch 样板闭环 | 2026-02-18 (CI ok) | `.github/workflows/drill-shadow-verify-entries.yml` | draft |
| `lab-S2B-1A-2A-shadow-search-concurrent-handling` | Search：shadow verify（search_index）最小闭环 | 2026-02-18 (local ok x5) | — | draft |
| `lab-S2B-2A-1A-shadow-verify-write-gate` | Search：write-gate（search_index 唯一性） | 2026-02-18 (CI ok, local ok x5) | `.github/workflows/drill-write-gate.yml` | draft |
| `lab-S2B-2A-2A-dual-run-cutover-closure` | v2：分页稳定性 + 共享键 + dual-run/cutover 收口 | 2026-02-20 (CI/window 语义已验证：mismatch fail `22210563050-1`, match pass `22210619481-1`; CI ok baseline: paging `22164058062-1`, shared-keys `22164060556-1`, stage1 `22174370696-1`, stage2 `22178056521-1`, window `22181124988-1`) | `.github/workflows/drill-write-gate.yml` | stable |
