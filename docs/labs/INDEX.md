# Labs Registry

目标：提供一个很轻量的“实验登记表”，解决“我到底有没有跑过 lab/test？”的焦虑。

约定：每个 lab 一行，关注四件事：目标、最近一次运行、CI workflow、状态。

| lab | 目标 | last run | CI workflow | status |
| --- | --- | --- | --- | --- |
| `lab-S3A-2A-3A-observability-failure-drills` | 失败观测演练菜单（metrics → trace → logs） | — | `.github/workflows/failure-drills.yml` | draft |
| `lab-S2B-1A-1A-shadow-concurrent-handling` | Chronicle：shadow verify + read switch 样板闭环 | 2026-02-15 14:42 (GMT+8) | `.github/workflows/drill-shadow-verify-entries.yml` | draft |
