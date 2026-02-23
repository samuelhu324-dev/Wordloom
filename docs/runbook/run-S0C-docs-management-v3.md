# Run-S0C: docs management v3（scenario id 查找 + catalog-driven suite 操作）

---

**id**: `S0C-docs-management-v3`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S0C-docs-management-v3`
**status**: `draft`          # draft | stable | archived
**scope**: `S0C`
**decision_date**: `2026-02-23`
**context_issue**:
  **DoD**: `#83, #66`
**decision**: `Use scenario catalog as single source of truth; suite workflows accept only scenario_id (string) to reduce maintenance; provide a simple listing tool for operators.`
  **positive**: `"Less workflow churn", "Catalog is audit-able", "Operators can discover ids quickly"`
  **negative**: `"GitHub UI loses dropdown options", "Need a tiny helper script"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 让操作者在 GitHub Actions 运行 suite 时，能快速知道应该填写什么 `scenario_id`。
- 把“场景清单”的真相收敛到 `docs/labs/scenarios/catalog.yml`。
- 提供最小的查询工具：`list-scenarios`（按 intent/关键字过滤）。

## 2) Single Source of Truth

- Scenario catalog：`docs/labs/scenarios/catalog.yml`
  - `scenarios[].id`：canonical（`intent/pipeline/topic`）
  - `scenarios[].aliases[]`：legacy（仍可作为输入，runner 会解析）

## 3) Tool: list-scenarios

脚本位置：`backend/scripts/ci/list_scenarios.py`

### 3.1 Prerequisites

- Python 3
- 依赖：`PyYAML`

安装：

- `python -m pip install PyYAML`

### 3.2 Usage

列出全部场景：

- `python backend/scripts/ci/list_scenarios.py`

只看某个 intent（例如 verify）：

- `python backend/scripts/ci/list_scenarios.py --intent verify`

按关键字搜索（例如 paging）：

- `python backend/scripts/ci/list_scenarios.py --grep paging`

组合过滤：

- `python backend/scripts/ci/list_scenarios.py --intent dual_run --grep window`

输出格式（每行）：

- `<scenario_id>\taliases=a,b\t<cli 摘要>`

## 4) Operator workflow (GitHub Actions)

suite workflows 现在统一使用 `scenario_id: string` 输入（不再维护下拉 `options`）。

操作建议：

1) 先用 `list-scenarios` 找到你要的 `scenario_id`
2) 在 Actions 里打开对应 suite（例如 `drill-verify` / `drill-dual-run`）
3) 把 `scenario_id` 填进去（或直接用默认值先跑通）

## 5) Fallback: grep catalog directly

如果你不想装 PyYAML，也可以直接在 repo 里 grep：

- 列出所有 id（PowerShell）：
  - `rg "^\s*id:\s*" docs/labs/scenarios/catalog.yml`
- 按前缀过滤：
  - `rg "^\s*id:\s*verify/" docs/labs/scenarios/catalog.yml`
- 通过 legacy alias 反查 canonical：
  - `rg "shadow_verify_search_index" docs/labs/scenarios/catalog.yml`

## 6) References

- Scenario catalog：`docs/labs/scenarios/catalog.yml`
- Guardrails：`backend/scripts/ci/validate_scenario_catalog.py`
- Suites：`.github/workflows/drill-*.yml`
