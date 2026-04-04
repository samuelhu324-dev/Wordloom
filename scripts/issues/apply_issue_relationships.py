from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _derive_repo_slug, _repo_root, _require_gh_auth, _require_gh_cli, _run_command
from raw_live_mutation_guard import add_raw_live_mutation_guard_arg, require_raw_live_mutation_guard


FETCH_ISSUE_QUERY = (
    "query($owner:String!,$repo:String!,$number:Int!){"
    "repository(owner:$owner,name:$repo){"
    "issue(number:$number){"
    "id number url title "
    "parent{id number url title} "
    "subIssues(first:100){nodes{id number url title}}"
    "}"
    "}"
    "}"
)

ADD_SUB_ISSUE_MUTATION = (
    "mutation($issueId:ID!,$subIssueId:ID!){"
    "addSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}){"
    "issue{id number url title} "
    "subIssue{id number url title}"
    "}"
    "}"
)


@dataclass
class IssueRelationshipApplyResult:
    mode: str
    result: str
    plan_path: str
    item_index: int
    relationship_type: str
    repository: str
    parent_issue_number: int
    parent_issue_url: str
    parent_issue_title: str
    child_issue_number: int
    child_issue_url: str
    child_issue_title: str
    previous_parent_issue_number: int | None
    final_parent_issue_number: int | None
    applied_action: str
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a real child-parent issue relationship from a relationship dry-run plan")
    parser.add_argument("plan_path", help="Path to an issue-relationship plan JSON file")
    parser.add_argument("--item-index", dest="item_index", type=int, default=0, help="Plan item index to apply")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--result-path", dest="result_path", help="Override output result JSON path")
    add_raw_live_mutation_guard_arg(parser)
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _repo_rel(path: Path) -> str:
    return path.relative_to(_repo_root()).as_posix()


def _load_plan(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse issue-relationship plan JSON: {exc}") from exc


def _split_repo_slug(repo: str) -> tuple[str, str]:
    parts = repo.split("/")
    if len(parts) != 2:
        raise SystemExit(f"Repository slug must be owner/repo: {repo}")
    return parts[0], parts[1]


def _run_graphql(query: str, variables: dict[str, str | int]) -> dict:
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for name, value in variables.items():
        command.extend(["-F", f"{name}={value}"])
    cmd = _run_command(command)
    if cmd.returncode != 0:
        raise SystemExit(f"GitHub GraphQL call failed: {cmd.stderr.strip()}")
    try:
        payload = json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse GraphQL JSON: {exc}") from exc
    if payload.get("errors"):
        raise SystemExit(f"GraphQL returned errors: {json.dumps(payload['errors'], ensure_ascii=True)}")
    return payload.get("data") or {}


def _fetch_issue(repo: str, issue_number: int) -> dict:
    owner, repo_name = _split_repo_slug(repo)
    data = _run_graphql(
        FETCH_ISSUE_QUERY,
        {"owner": owner, "repo": repo_name, "number": issue_number},
    )
    issue = (((data.get("repository") or {}).get("issue")) or None)
    if not issue:
        raise SystemExit(f"Issue not found in {repo}: #{issue_number}")
    return issue


def _add_sub_issue(parent_issue_id: str, child_issue_id: str) -> dict:
    data = _run_graphql(
        ADD_SUB_ISSUE_MUTATION,
        {"issueId": parent_issue_id, "subIssueId": child_issue_id},
    )
    payload = data.get("addSubIssue") or {}
    if not payload:
        raise SystemExit("GraphQL addSubIssue returned no payload")
    return payload


def apply_issue_relationships(args: argparse.Namespace) -> IssueRelationshipApplyResult:
    require_raw_live_mutation_guard(
        args,
        canonical_surface="scripts/issues/apply_issue_relationships_with_pre_gate.py or scripts/issues/plan_publish_verify_remediation_gate.py --delegate-apply issue-relationship",
    )
    repo_root = _repo_root()
    plan_path = _coerce_path(args.plan_path, repo_root)
    if not plan_path.is_file():
        raise SystemExit(f"Issue-relationship plan file not found: {plan_path}")

    plan = _load_plan(plan_path)
    items = plan.get("items") or []
    if args.item_index < 0 or args.item_index >= len(items):
        raise SystemExit(f"Plan item index out of range: {args.item_index}")

    item = items[args.item_index]
    if item.get("status") != "planned":
        raise SystemExit(f"Selected plan item is not in planned state: {item.get('status')}")

    parent_issue_number = int(item["parent_issue_number"])
    child_issue_number = int(item["child_issue_number"])
    relationship_type = str(item.get("relationship_type") or "child-of")

    repo = _derive_repo_slug(args.repo)
    _require_gh_cli()
    _require_gh_auth()

    warnings: list[str] = []
    parent_issue = _fetch_issue(repo, parent_issue_number)
    child_issue = _fetch_issue(repo, child_issue_number)
    previous_parent = child_issue.get("parent") or None
    previous_parent_issue_number = int(previous_parent["number"]) if previous_parent else None

    if previous_parent_issue_number == parent_issue_number:
        warnings.append("child issue was already attached to the requested parent issue")
        applied_action = "already-linked-child-to-parent"
    elif previous_parent_issue_number is not None:
        raise SystemExit(
            f"Child issue #{child_issue_number} is already attached to a different parent issue #{previous_parent_issue_number}"
        )
    else:
        parent_sub_issue_numbers = {
            int(node["number"])
            for node in (((parent_issue.get("subIssues") or {}).get("nodes")) or [])
            if isinstance(node, dict) and node.get("number") is not None
        }
        if child_issue_number in parent_sub_issue_numbers:
            warnings.append("parent issue already lists the requested child issue in subIssues")
            applied_action = "already-linked-child-to-parent"
        else:
            _add_sub_issue(str(parent_issue["id"]), str(child_issue["id"]))
            applied_action = "link-child-to-parent" if relationship_type == "child-of" else "link-parent-to-child"

    refreshed_child_issue = _fetch_issue(repo, child_issue_number)
    final_parent = refreshed_child_issue.get("parent") or None
    final_parent_issue_number = int(final_parent["number"]) if final_parent else None
    if final_parent_issue_number != parent_issue_number:
        raise SystemExit(
            f"Relationship apply did not converge to the requested parent issue #{parent_issue_number}; current parent is {final_parent_issue_number}"
        )

    plan_slug = plan_path.stem.removesuffix("-plan")
    default_result_path = plan_path.with_name(
        f"{plan_slug}-parent-{parent_issue_number}-child-{child_issue_number}-apply-result.json"
    )
    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else default_result_path
    result_path.parent.mkdir(parents=True, exist_ok=True)

    result = IssueRelationshipApplyResult(
        mode="relationship-apply",
        result="ok",
        plan_path=_repo_rel(plan_path),
        item_index=args.item_index,
        relationship_type=relationship_type,
        repository=repo,
        parent_issue_number=int(parent_issue["number"]),
        parent_issue_url=str(parent_issue["url"]),
        parent_issue_title=str(parent_issue.get("title") or ""),
        child_issue_number=int(refreshed_child_issue["number"]),
        child_issue_url=str(refreshed_child_issue["url"]),
        child_issue_title=str(refreshed_child_issue.get("title") or ""),
        previous_parent_issue_number=previous_parent_issue_number,
        final_parent_issue_number=final_parent_issue_number,
        applied_action=applied_action,
        warnings=warnings,
    )
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        apply_issue_relationships(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())