from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from body_contract import normalize_issue_short_ref, ordered_parent_child_issue_refs
from gen_issue_draft import _derive_repo_slug, _parse_fields, _repo_root, _require_gh_auth, _require_gh_cli, _run_command
from raw_live_mutation_guard import add_raw_live_mutation_guard_arg, require_raw_live_mutation_guard


FETCH_PARENT_ISSUE_QUERY = (
    "query($owner:String!,$repo:String!,$number:Int!){"
    "repository(owner:$owner,name:$repo){"
    "issue(number:$number){"
    "id number url title subIssues(first:100){nodes{id number url title}}"
    "}"
    "}"
    "}"
)

REPRIORITIZE_SUB_ISSUE_MUTATION = (
    "mutation($issueId:ID!,$subIssueId:ID!,$afterId:ID,$beforeId:ID){"
    "reprioritizeSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId,afterId:$afterId,beforeId:$beforeId}){"
    "issue{id number url title}"
    "}"
    "}"
)


@dataclass
class ReprioritizeAction:
    action: str
    sub_issue_number: int
    anchor_issue_number: int | None


@dataclass
class ParentSubissueReprioritizeResult:
    mode: str
    result: str
    apply: bool
    repository: str
    parent_log_path: str
    parent_issue_number: int
    parent_issue_url: str
    parent_issue_title: str
    expected_subissue_numbers: list[int]
    before_subissue_numbers: list[int]
    final_subissue_numbers: list[int]
    actions: list[ReprioritizeAction]
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan or apply canonical GitHub parent sub-issue reprioritization from a parent source log"
    )
    parser.add_argument("parent_log_path", help="Path to the parent source log that owns the canonical child ordering")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--apply", dest="apply", action="store_true", help="Apply the planned reprioritize mutations")
    parser.add_argument("--result-path", dest="result_path", help="Override output result JSON path")
    add_raw_live_mutation_guard_arg(parser)
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _repo_rel(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _split_repo_slug(repo: str) -> tuple[str, str]:
    parts = repo.split("/")
    if len(parts) != 2:
        raise SystemExit(f"Repository slug must be owner/repo: {repo}")
    return parts[0], parts[1]


def _run_graphql(query: str, variables: dict[str, str | int | None]) -> dict:
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for name, value in variables.items():
        if value is None:
            continue
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


def _fetch_parent_issue(repo: str, issue_number: int) -> dict:
    owner, repo_name = _split_repo_slug(repo)
    data = _run_graphql(
        FETCH_PARENT_ISSUE_QUERY,
        {"owner": owner, "repo": repo_name, "number": issue_number},
    )
    issue = (((data.get("repository") or {}).get("issue")) or None)
    if not issue:
        raise SystemExit(f"Issue not found in {repo}: #{issue_number}")
    return issue


def _reprioritize_sub_issue(parent_issue_id: str, sub_issue_id: str, *, after_id: str | None, before_id: str | None) -> None:
    data = _run_graphql(
        REPRIORITIZE_SUB_ISSUE_MUTATION,
        {
            "issueId": parent_issue_id,
            "subIssueId": sub_issue_id,
            "afterId": after_id,
            "beforeId": before_id,
        },
    )
    payload = data.get("reprioritizeSubIssue") or {}
    if not payload:
        raise SystemExit("GraphQL reprioritizeSubIssue returned no payload")


def _move_to_front(order: list[int], target: int) -> None:
    order.remove(target)
    order.insert(0, target)


def _move_after(order: list[int], target: int, anchor: int) -> None:
    order.remove(target)
    anchor_index = order.index(anchor)
    order.insert(anchor_index + 1, target)


def _plan_actions(current_order: list[int], expected_order: list[int]) -> list[ReprioritizeAction]:
    simulated = list(current_order)
    actions: list[ReprioritizeAction] = []
    if not expected_order:
        return actions

    first_expected = expected_order[0]
    if simulated and simulated[0] != first_expected:
        _move_to_front(simulated, first_expected)
        actions.append(ReprioritizeAction(action="move-to-front", sub_issue_number=first_expected, anchor_issue_number=None))

    for index in range(1, len(expected_order)):
        expected_number = expected_order[index]
        previous_number = expected_order[index - 1]
        previous_index = simulated.index(previous_number)
        expected_index = simulated.index(expected_number)
        if expected_index == previous_index + 1:
            continue
        _move_after(simulated, expected_number, previous_number)
        actions.append(
            ReprioritizeAction(
                action="move-after",
                sub_issue_number=expected_number,
                anchor_issue_number=previous_number,
            )
        )
    return actions


def reprioritize_parent_subissues(args: argparse.Namespace) -> ParentSubissueReprioritizeResult:
    if args.apply:
        require_raw_live_mutation_guard(
            args,
            canonical_surface="scripts/issues/reprioritize_parent_subissues.py --apply --allow-raw-live-mutation-internal",
        )

    repo_root = _repo_root()
    parent_log_path = _coerce_path(args.parent_log_path, repo_root)
    if not parent_log_path.is_file():
        raise SystemExit(f"Parent log file not found: {parent_log_path}")

    fields = _parse_fields(parent_log_path.read_text(encoding="utf-8"))
    parent_issue_ref = normalize_issue_short_ref(fields.get("issue"))
    if not parent_issue_ref:
        raise SystemExit(f"Parent log is missing a canonical issue reference: {parent_log_path}")
    parent_issue_number = int(parent_issue_ref.removeprefix("#"))

    expected_refs = ordered_parent_child_issue_refs(repo_root, fields)
    expected_numbers = [int(ref.removeprefix("#")) for ref in expected_refs]

    repo = _derive_repo_slug(args.repo)
    _require_gh_cli()
    _require_gh_auth()

    parent_issue = _fetch_parent_issue(repo, parent_issue_number)
    live_nodes = [
        node for node in (((parent_issue.get("subIssues") or {}).get("nodes")) or []) if isinstance(node, dict) and node.get("number")
    ]
    live_numbers = [int(node["number"]) for node in live_nodes]
    live_ids = {int(node["number"]): str(node["id"]) for node in live_nodes}

    if sorted(live_numbers) != sorted(expected_numbers):
        raise SystemExit(
            "Parent sub-issue reprioritize requires the live child set to match the canonical expected child set; "
            f"live={live_numbers}, expected={expected_numbers}"
        )

    actions = _plan_actions(live_numbers, expected_numbers)
    warnings: list[str] = []
    if not actions:
        warnings.append("parent sub-issue order already matches the canonical source-log-owned order")

    if args.apply:
        parent_issue_id = str(parent_issue["id"])
        simulated = list(live_numbers)
        for action in actions:
            sub_issue_id = live_ids[action.sub_issue_number]
            if action.action == "move-to-front":
                before_id = live_ids[simulated[0]]
                _reprioritize_sub_issue(parent_issue_id, sub_issue_id, after_id=None, before_id=before_id)
                _move_to_front(simulated, action.sub_issue_number)
                continue

            if action.anchor_issue_number is None:
                raise SystemExit(f"move-after action missing anchor: {action}")
            anchor_id = live_ids[action.anchor_issue_number]
            _reprioritize_sub_issue(parent_issue_id, sub_issue_id, after_id=anchor_id, before_id=None)
            _move_after(simulated, action.sub_issue_number, action.anchor_issue_number)

        refreshed_parent = _fetch_parent_issue(repo, parent_issue_number)
        final_numbers = [
            int(node["number"])
            for node in ((((refreshed_parent.get("subIssues") or {}).get("nodes")) or []))
            if isinstance(node, dict) and node.get("number") is not None
        ]
        if final_numbers != expected_numbers:
            raise SystemExit(
                "Parent sub-issue reprioritize did not converge to the canonical expected order; "
                f"final={final_numbers}, expected={expected_numbers}"
            )
        parent_issue = refreshed_parent
    else:
        final_numbers = list(live_numbers)

    default_result_path = repo_root / "artifacts" / f"parent-subissue-reprioritize-{fields.get('id', parent_log_path.stem)}.json"
    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else default_result_path
    result_path.parent.mkdir(parents=True, exist_ok=True)

    result = ParentSubissueReprioritizeResult(
        mode="parent-subissue-reprioritize",
        result="ok",
        apply=bool(args.apply),
        repository=repo,
        parent_log_path=_repo_rel(parent_log_path, repo_root),
        parent_issue_number=parent_issue_number,
        parent_issue_url=str(parent_issue["url"]),
        parent_issue_title=str(parent_issue.get("title") or ""),
        expected_subissue_numbers=expected_numbers,
        before_subissue_numbers=live_numbers,
        final_subissue_numbers=final_numbers,
        actions=actions,
        warnings=warnings,
    )
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        reprioritize_parent_subissues(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())