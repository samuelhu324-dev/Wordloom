from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _derive_repo_slug, _repo_rel, _repo_root, _require_gh_auth, _require_gh_cli, _run_command
from plan_lifecycle_pre_gate import plan_lifecycle_pre_gate
from raw_live_mutation_guard import require_raw_live_mutation_guard
from rewrite_pr_body_scope_from_log import rewrite_pr_body_scope


@dataclass
class PrBodyRewriteApplyResult:
    mode: str
    result: str
    repository: str
    pr_number: int
    pr_url: str
    pr_title: str
    pr_state: str
    source_log_path: str
    requested_id: str
    live_body_path: str
    rewritten_body_path: str
    body_changed: bool
    warnings: list[str]


@dataclass
class GuardedPrBodyRewriteResult:
    mode: str
    result: str
    gate_input_kind: str
    gate_input_path: str
    gate_decision_path: str
    gate_decision: str
    apply_allowed: bool
    pr_create_result_path: str
    guarded_action: str
    apply_result_path: str | None
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite a live PR body behind the lifecycle pre-gate")
    parser.add_argument("gate_input_path", help="Path to a lifecycle-audit manifest JSON file or frozen lifecycle-audit plan JSON file")
    parser.add_argument("pr_create_result_path", help="Path to a pr-create result JSON file that identifies the live PR and source log")
    parser.add_argument("--gate-input-kind", dest="gate_input_kind", choices=["manifest", "audit-plan"], default="manifest", help="Interpret the gate input as a manifest or as a frozen audit plan")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--gate-audit-plan-path", dest="gate_audit_plan_path", help="Override output path for the lifecycle-audit plan when gate input is a manifest")
    parser.add_argument("--gate-remediation-plan-path", dest="gate_remediation_plan_path", help="Override output path for the lifecycle-remediation plan")
    parser.add_argument("--gate-decision-path", dest="gate_decision_path", help="Override output path for the lifecycle pre-gate decision")
    parser.add_argument("--live-body-path", dest="live_body_path", help="Override output path for the fetched live PR body")
    parser.add_argument("--rewritten-body-path", dest="rewritten_body_path", help="Override output path for the rewritten PR body")
    parser.add_argument("--apply-result-path", dest="apply_result_path", help="Override output path for the PR-body rewrite apply result")
    parser.add_argument("--guarded-result-path", dest="guarded_result_path", help="Override output path for the guarded apply result")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_json(path: Path, error_label: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse {error_label} JSON: {exc}") from exc


def _default_decision_path(gate_result: object, explicit_path: str | None, repo_root: Path) -> str:
    if explicit_path:
        return _repo_rel(_coerce_path(explicit_path, repo_root))
    audit_plan_path = str(gate_result.audit_plan_path)
    return audit_plan_path.replace("lifecycle-audit-", "lifecycle-gate-").replace("-plan.json", "-decision.json")


def _fetch_pr(repo: str, pr_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "pr",
        "view",
        pr_ref,
        "--repo",
        repo,
        "--json",
        "number,url,title,state,body",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view PR {pr_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR view JSON: {exc}") from exc


def _edit_pr_body(repo: str, pr_ref: str, body_path: Path) -> None:
    cmd = _run_command([
        "gh",
        "pr",
        "edit",
        pr_ref,
        "--repo",
        repo,
        "--body-file",
        str(body_path),
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"gh pr edit failed: {cmd.stderr.strip()}")


def apply_pr_body_scope(args: argparse.Namespace) -> PrBodyRewriteApplyResult:
    require_raw_live_mutation_guard(
        args,
        canonical_surface="scripts/issues/apply_pr_body_scope_with_pre_gate.py or scripts/issues/plan_publish_verify_remediation_gate.py --delegate-apply pr-body-rewrite",
    )
    repo_root = _repo_root()
    create_result_path = _coerce_path(args.pr_create_result_path, repo_root)
    if not create_result_path.is_file():
        raise SystemExit(f"PR create result file not found: {create_result_path}")

    create_result = _load_json(create_result_path, "pr-create result")
    if create_result.get("mode") != "pr-create":
        raise SystemExit("PR body rewrite apply requires a pr-create result JSON input")

    pr_number = int(create_result.get("pr_number") or 0)
    if not pr_number:
        raise SystemExit("PR create result is missing pr_number")

    pr_title = str(create_result.get("pr_title") or "")
    requested_id = str(create_result.get("requested_id") or "")
    source_log_rel = str(create_result.get("source_log_path") or "")
    if not requested_id or not source_log_rel or not pr_title:
        raise SystemExit("PR create result is missing requested_id, source_log_path, or pr_title")

    source_log_path = _coerce_path(source_log_rel, repo_root)
    repo = _derive_repo_slug(args.repo)
    _require_gh_cli()
    _require_gh_auth()

    base_slug = create_result_path.stem.removesuffix("-create-result")
    live_body_path = _coerce_path(args.live_body_path, repo_root) if args.live_body_path else create_result_path.with_name(f"{base_slug}-live-body.md")
    rewritten_body_path = _coerce_path(args.rewritten_body_path, repo_root) if args.rewritten_body_path else create_result_path.with_name(f"{base_slug}-rewritten-body.md")
    apply_result_path = _coerce_path(args.apply_result_path, repo_root) if args.apply_result_path else create_result_path.with_name(f"{base_slug}-rewrite-apply-result.json")

    before = _fetch_pr(repo, str(pr_number))
    live_body_text = str(before.get("body") or "")
    live_body_path.parent.mkdir(parents=True, exist_ok=True)
    live_body_path.write_text(live_body_text, encoding="utf-8")

    rewrite_pr_body_scope(
        source_log_path=source_log_path,
        existing_body_path=live_body_path,
        requested_id=requested_id,
        pr_title=pr_title,
        output_path=rewritten_body_path,
    )

    rewritten_body_text = rewritten_body_path.read_text(encoding="utf-8")
    _edit_pr_body(repo, str(pr_number), rewritten_body_path)
    after = _fetch_pr(repo, str(pr_number))

    warnings: list[str] = []
    body_changed = live_body_text != rewritten_body_text
    if not body_changed:
        warnings.append("rewritten PR body matched the fetched live body; guarded apply still verified the live edit path")

    result = PrBodyRewriteApplyResult(
        mode="pr-body-rewrite-apply",
        result="ok",
        repository=repo,
        pr_number=int(after["number"]),
        pr_url=str(after.get("url") or create_result.get("pr_url") or ""),
        pr_title=str(after.get("title") or pr_title),
        pr_state=str(after.get("state") or ""),
        source_log_path=source_log_rel,
        requested_id=requested_id,
        live_body_path=_repo_rel(live_body_path),
        rewritten_body_path=_repo_rel(rewritten_body_path),
        body_changed=body_changed,
        warnings=warnings,
    )
    apply_result_path.parent.mkdir(parents=True, exist_ok=True)
    apply_result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def guarded_pr_body_scope_apply(args: argparse.Namespace) -> GuardedPrBodyRewriteResult:
    repo_root = _repo_root()
    gate_input_path = _coerce_path(args.gate_input_path, repo_root)
    create_result_path = _coerce_path(args.pr_create_result_path, repo_root)
    if not gate_input_path.is_file():
        raise SystemExit(f"Lifecycle gate input file not found: {gate_input_path}")
    if not create_result_path.is_file():
        raise SystemExit(f"PR create result file not found: {create_result_path}")

    guarded_result_path = _coerce_path(args.guarded_result_path, repo_root) if args.guarded_result_path else create_result_path.with_name(f"{create_result_path.stem.removesuffix('-create-result')}-guarded-pr-body-rewrite-result.json")

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

    warnings: list[str] = []
    apply_result_rel: str | None = None
    if not gate_result.apply_allowed:
        guarded_action = "stopped-before-apply"
        warnings.append(f"mutation blocked by lifecycle pre-gate decision: {gate_result.decision}")
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            apply_result = apply_pr_body_scope(
                argparse.Namespace(
                    gate_input_path=args.gate_input_path,
                    pr_create_result_path=args.pr_create_result_path,
                    gate_input_kind=args.gate_input_kind,
                    repo=args.repo,
                    gate_audit_plan_path=args.gate_audit_plan_path,
                    gate_remediation_plan_path=args.gate_remediation_plan_path,
                    gate_decision_path=args.gate_decision_path,
                    live_body_path=args.live_body_path,
                    rewritten_body_path=args.rewritten_body_path,
                    apply_result_path=args.apply_result_path,
                    guarded_result_path=args.guarded_result_path,
                    allow_raw_live_mutation_internal=True,
                )
            )
        apply_result_rel = _repo_rel(_coerce_path(args.apply_result_path, repo_root)) if args.apply_result_path else create_result_path.with_name(f"{create_result_path.stem.removesuffix('-create-result')}-rewrite-apply-result.json").relative_to(repo_root).as_posix()
        guarded_action = "applied-after-pre-gate"
        warnings.extend(list(apply_result.warnings or []))

    result = GuardedPrBodyRewriteResult(
        mode="guarded-pr-body-rewrite-apply",
        result="ok",
        gate_input_kind=args.gate_input_kind,
        gate_input_path=_repo_rel(gate_input_path),
        gate_decision_path=_default_decision_path(gate_result, args.gate_decision_path, repo_root),
        gate_decision=gate_result.decision,
        apply_allowed=gate_result.apply_allowed,
        pr_create_result_path=_repo_rel(create_result_path),
        guarded_action=guarded_action,
        apply_result_path=apply_result_rel,
        warnings=warnings,
    )
    guarded_result_path.parent.mkdir(parents=True, exist_ok=True)
    guarded_result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        guarded_pr_body_scope_apply(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())