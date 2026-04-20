from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from body_contract import validate_pr_body_contract
from create_pr_from_plan import _ensure_branch_absent, _has_placeholder_summary
from gen_issue_draft import (
    _derive_repo_slug,
    _fetch_existing_labels,
    _fetch_existing_milestones,
    _repo_rel,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
)
from plan_lifecycle_pre_gate import plan_lifecycle_pre_gate
from plan_pr_prep import plan_pr_prep


@dataclass
class PreflightCheck:
    name: str
    status: str
    details: str


@dataclass
class PrCreatePreflightResult:
    mode: str
    result: str
    repository: str
    gate_input_kind: str
    gate_input_path: str
    gate_decision_path: str
    pr_prep_input_kind: str
    pr_prep_input_path: str
    pr_prep_plan_path: str
    item_index: int
    requested_id: str
    source_log_path: str
    candidate_pr_branch: str
    selected_commit_count: int
    summary_bullet_count: int
    gate_decision: str
    gate_apply_allowed: bool
    preflight_decision: str
    preflight_allowed: bool
    stopped_before_stage: str
    warnings: list[str]
    checks: list[PreflightCheck]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan a bounded PR-create front-half preflight behind the lifecycle pre-gate")
    parser.add_argument("gate_input_path", help="Path to a lifecycle-audit manifest JSON file or frozen lifecycle-audit plan JSON file")
    parser.add_argument("pr_prep_input_path", help="Path to a PR-prep manifest JSON file or PR-prep plan JSON file")
    parser.add_argument("--gate-input-kind", dest="gate_input_kind", choices=["manifest", "audit-plan"], default="manifest", help="Interpret the lifecycle gate input as a manifest or as a frozen audit plan")
    parser.add_argument("--pr-prep-input-kind", dest="pr_prep_input_kind", choices=["manifest", "plan"], default="manifest", help="Interpret the PR-prep input as a manifest or as an existing plan")
    parser.add_argument("--item-index", dest="item_index", type=int, default=0, help="PR-prep plan item index to evaluate")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--gate-audit-plan-path", dest="gate_audit_plan_path", help="Override output path for the lifecycle-audit plan when gate input is a manifest")
    parser.add_argument("--gate-remediation-plan-path", dest="gate_remediation_plan_path", help="Override output path for the lifecycle-remediation plan")
    parser.add_argument("--gate-decision-path", dest="gate_decision_path", help="Override output path for the lifecycle pre-gate decision JSON")
    parser.add_argument("--pr-prep-plan-path", dest="pr_prep_plan_path", help="Override output path for the PR-prep plan when PR-prep input is a manifest")
    parser.add_argument("--result-path", dest="result_path", help="Override output path for the preflight result JSON")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_json(path: Path, error_label: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse {error_label} JSON: {exc}") from exc


def _default_gate_decision_path(gate_result: object, explicit_path: str | None, repo_root: Path) -> str:
    if explicit_path:
        return _repo_rel(_coerce_path(explicit_path, repo_root))
    audit_plan_path = str(gate_result.audit_plan_path)
    return audit_plan_path.replace("lifecycle-audit-", "lifecycle-gate-").replace("-plan.json", "-decision.json")


def _default_result_path(pr_plan_path: Path) -> Path:
    stem = pr_plan_path.stem.removesuffix("-plan")
    return pr_plan_path.with_name(f"{stem}-front-half-preflight-result.json")


def _load_pr_prep_plan(args: argparse.Namespace, repo_root: Path) -> tuple[dict, Path]:
    input_path = _coerce_path(args.pr_prep_input_path, repo_root)
    if not input_path.is_file():
        raise SystemExit(f"PR-prep input file not found: {input_path}")

    if args.pr_prep_input_kind == "manifest":
        plan_path = _coerce_path(args.pr_prep_plan_path, repo_root) if args.pr_prep_plan_path else input_path.with_name(f"{input_path.stem}-plan.json")
        with contextlib.redirect_stdout(io.StringIO()):
            plan_result = plan_pr_prep(
                argparse.Namespace(
                    manifest_path=_repo_rel(input_path),
                    plan_path=_repo_rel(plan_path),
                )
            )
        return asdict(plan_result), plan_path

    if args.pr_prep_plan_path:
        raise SystemExit("--pr-prep-plan-path cannot be used when --pr-prep-input-kind plan is selected")
    plan_data = _load_json(input_path, "PR-prep plan")
    if plan_data.get("mode") != "pr-prep-dry-run":
        raise SystemExit("PR-prep plan input must be a pr-prep-dry-run result")
    return plan_data, input_path


def _evaluate_preflight_item(*, repo: str, item: dict, gate_allowed: bool, repo_root: Path) -> tuple[str, bool, list[PreflightCheck], list[str]]:
    checks: list[PreflightCheck] = []
    warnings: list[str] = []

    if not gate_allowed:
        checks.append(PreflightCheck("lifecycle-pre-gate", "fail", "lifecycle pre-gate did not allow create-time continuation"))
        checks.extend(
            [
                PreflightCheck("plan-item-state", "skipped", "create-specific preflight checks skipped because lifecycle pre-gate blocked the sample"),
                PreflightCheck("gh-prerequisites", "skipped", "create-specific preflight checks skipped because lifecycle pre-gate blocked the sample"),
                PreflightCheck("branch-availability", "skipped", "create-specific preflight checks skipped because lifecycle pre-gate blocked the sample"),
                PreflightCheck("preview-integrity", "skipped", "create-specific preflight checks skipped because lifecycle pre-gate blocked the sample"),
                PreflightCheck("body-shape-contract", "skipped", "create-specific preflight checks skipped because lifecycle pre-gate blocked the sample"),
            ]
        )
        return "stop-before-local-materialization", False, checks, warnings

    checks.append(PreflightCheck("lifecycle-pre-gate", "pass", "lifecycle pre-gate allowed the issue-created sample to continue into create-time preflight"))

    item_status = str(item.get("status") or "")
    if item_status == "planned":
        checks.append(PreflightCheck("plan-item-state", "pass", "PR-prep item is in planned state"))
    else:
        checks.append(PreflightCheck("plan-item-state", "fail", f"PR-prep item is not planned: {item_status or '<blank>'}"))

    selected_commits = item.get("selected_commits") or []
    if selected_commits:
        checks.append(PreflightCheck("selected-commits", "pass", f"selected commit count = {len(selected_commits)}"))
    else:
        checks.append(PreflightCheck("selected-commits", "fail", "PR-prep item selected no commits"))

    try:
        _require_gh_cli()
        _require_gh_auth()
        checks.append(PreflightCheck("gh-prerequisites", "pass", "gh CLI and auth are available for preflight reads"))
    except SystemExit as exc:
        checks.append(PreflightCheck("gh-prerequisites", "fail", str(exc)))

    labels = list(item.get("pr_labels") or [])
    missing_labels: list[str] = []
    if labels:
        try:
            existing_labels = _fetch_existing_labels(repo)
            missing_labels = [label for label in labels if label not in existing_labels]
        except SystemExit as exc:
            checks.append(PreflightCheck("label-existence", "fail", str(exc)))
        else:
            if missing_labels:
                checks.append(PreflightCheck("label-existence", "fail", f"missing pre-created PR labels: {', '.join(missing_labels)}"))
            else:
                checks.append(PreflightCheck("label-existence", "pass", "all requested PR labels exist"))
    else:
        checks.append(PreflightCheck("label-existence", "skipped", "pr_labels left blank by contract"))

    milestone = item.get("pr_milestone")
    if milestone:
        try:
            milestones = _fetch_existing_milestones(repo)
        except SystemExit as exc:
            checks.append(PreflightCheck("milestone-existence", "fail", str(exc)))
        else:
            if milestone in milestones:
                checks.append(PreflightCheck("milestone-existence", "pass", f"PR milestone exists: {milestone}"))
            else:
                checks.append(PreflightCheck("milestone-existence", "fail", f"PR milestone does not exist: {milestone}"))
    else:
        checks.append(PreflightCheck("milestone-existence", "skipped", "pr_milestone left blank by contract"))

    candidate_branch = str(item.get("candidate_pr_branch") or "")
    if candidate_branch:
        try:
            _ensure_branch_absent(candidate_branch)
        except SystemExit as exc:
            checks.append(PreflightCheck("branch-availability", "fail", str(exc)))
        else:
            checks.append(PreflightCheck("branch-availability", "pass", f"prepared branch name is currently free: {candidate_branch}"))
    else:
        checks.append(PreflightCheck("branch-availability", "fail", "candidate_pr_branch is blank"))

    preview_body_rel = str(item.get("preview_body_path") or "")
    if not preview_body_rel:
        checks.append(PreflightCheck("preview-integrity", "fail", "preview body path is blank"))
    else:
        preview_body_path = _coerce_path(preview_body_rel, repo_root)
        if not preview_body_path.is_file():
            checks.append(PreflightCheck("preview-integrity", "fail", f"preview body file not found: {preview_body_rel}"))
        else:
            preview_body = preview_body_path.read_text(encoding="utf-8")
            summary_bullet_count = int(item.get("summary_bullet_count") or 0)
            if _has_placeholder_summary(preview_body) or summary_bullet_count <= 0:
                checks.append(PreflightCheck("preview-integrity", "fail", "preview body still contains placeholder Summary content or zero summary bullets"))
            else:
                checks.append(PreflightCheck("preview-integrity", "pass", f"preview body is create-ready with summary_bullet_count = {summary_bullet_count}"))

            source_log_rel = str(item.get("source_log_path") or "")
            if source_log_rel:
                source_log_path = _coerce_path(source_log_rel, repo_root)
                contract_result = validate_pr_body_contract(
                    body_markdown=preview_body,
                    source_log_text=source_log_path.read_text(encoding="utf-8"),
                    pr_development_issue=str(item.get("pr_development_issue") or "").strip() or None,
                )
                failed = [check.details for check in contract_result.checks if check.status == "fail"]
                if failed:
                    checks.append(PreflightCheck("body-shape-contract", "fail", "; ".join(failed)))
                else:
                    checks.append(PreflightCheck("body-shape-contract", "pass", "preview body matches the canonical PR body contract"))
            else:
                checks.append(PreflightCheck("body-shape-contract", "fail", "source_log_path is blank so PR body contract cannot be validated"))

    failing = [check for check in checks if check.status == "fail"]
    if failing:
        warnings.extend(check.details for check in failing)
        return "stop-before-local-materialization", False, checks, warnings
    return "allow-front-half-preflight", True, checks, warnings


def plan_pr_create_preflight_with_gate(args: argparse.Namespace) -> PrCreatePreflightResult:
    repo_root = _repo_root()
    gate_input_path = _coerce_path(args.gate_input_path, repo_root)
    if not gate_input_path.is_file():
        raise SystemExit(f"Lifecycle gate input file not found: {gate_input_path}")

    pr_plan_data, pr_plan_path = _load_pr_prep_plan(args, repo_root)
    items = pr_plan_data.get("items") or []
    if args.item_index < 0 or args.item_index >= len(items):
        raise SystemExit(f"PR-prep plan item index out of range: {args.item_index}")
    item = items[args.item_index]

    with contextlib.redirect_stdout(io.StringIO()):
        gate_result = plan_lifecycle_pre_gate(
            argparse.Namespace(
                input_path=_repo_rel(gate_input_path),
                input_kind=args.gate_input_kind,
                repo=args.repo,
                audit_plan_path=args.gate_audit_plan_path,
                remediation_plan_path=args.gate_remediation_plan_path,
                decision_path=args.gate_decision_path,
            )
        )

    repo = _derive_repo_slug(args.repo)
    preflight_decision, preflight_allowed, checks, check_warnings = _evaluate_preflight_item(
        repo=repo,
        item=item,
        gate_allowed=gate_result.apply_allowed,
        repo_root=repo_root,
    )

    result = PrCreatePreflightResult(
        mode="pr-create-front-half-preflight",
        result="ok",
        repository=repo,
        gate_input_kind=args.gate_input_kind,
        gate_input_path=_repo_rel(gate_input_path),
        gate_decision_path=_default_gate_decision_path(gate_result, args.gate_decision_path, repo_root),
        pr_prep_input_kind=args.pr_prep_input_kind,
        pr_prep_input_path=str(args.pr_prep_input_path),
        pr_prep_plan_path=_repo_rel(pr_plan_path),
        item_index=args.item_index,
        requested_id=str(item.get("requested_id") or ""),
        source_log_path=str(item.get("source_log_path") or ""),
        candidate_pr_branch=str(item.get("candidate_pr_branch") or ""),
        selected_commit_count=len(item.get("selected_commits") or []),
        summary_bullet_count=int(item.get("summary_bullet_count") or 0),
        gate_decision=gate_result.decision,
        gate_apply_allowed=gate_result.apply_allowed,
        preflight_decision=preflight_decision,
        preflight_allowed=preflight_allowed,
        stopped_before_stage="S4-local-branch-materialization",
        warnings=list(gate_result.warnings or []) + check_warnings,
        checks=checks,
    )

    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else _default_result_path(pr_plan_path)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_pr_create_preflight_with_gate(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())