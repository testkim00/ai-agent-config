#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
}


@dataclass
class BranchState:
    name: str
    upstream: Optional[str]
    is_current: bool
    target_ref: Optional[str] = None
    ahead: int = 0
    behind: int = 0
    skipped_targets: List[str] = field(default_factory=list)
    blocker: Optional[str] = None

    @property
    def needs_update(self) -> bool:
        return bool(self.target_ref) and self.behind > 0


@dataclass
class RepoPlan:
    path: Path
    current_branch: str
    dirty: bool
    branches: List[BranchState] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)

    @property
    def has_blockers(self) -> bool:
        return bool(self.blockers)

    @property
    def update_count(self) -> int:
        return sum(1 for branch in self.branches if branch.needs_update)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync all local branches in one repo, or in every repo under a directory, "
            "to their upstream or same-name remote branch without switching branches."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Git repo path or a root directory that contains multiple repos. Defaults to the current directory.",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Fallback remote name for branches that do not already have an upstream. Default: origin.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the preflight plan without updating any local branches.",
    )
    return parser.parse_args()


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def git_output(repo: Path, *args: str) -> str:
    result = run_git(repo, *args)
    return result.stdout.strip()


def is_git_repo(path: Path) -> bool:
    try:
        run_git(path, "rev-parse", "--show-toplevel")
        return True
    except subprocess.CalledProcessError:
        return False


def discover_repos(root: Path) -> List[Path]:
    root = root.resolve()
    if is_git_repo(root):
        return [root]

    repos: List[Path] = []
    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        if (current_path / ".git").exists():
            repos.append(current_path)
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
    return sorted(repos)


def fallback_upstream(repo: Path, branch_name: str, remote_name: str) -> Optional[str]:
    candidate = f"{remote_name}/{branch_name}"
    try:
        run_git(repo, "show-ref", "--verify", "--quiet", f"refs/remotes/{candidate}")
        return candidate
    except subprocess.CalledProcessError:
        return None


def parse_branch_line(line: str) -> BranchState:
    name, upstream, head_flag = line.split("|", 2)
    return BranchState(
        name=name,
        upstream=upstream or None,
        is_current=(head_flag == "*"),
    )


def list_remotes(repo: Path) -> List[str]:
    output = git_output(repo, "remote")
    if not output:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def remote_ref_exists(repo: Path, ref_name: str) -> bool:
    try:
        run_git(repo, "show-ref", "--verify", "--quiet", f"refs/remotes/{ref_name}")
        return True
    except subprocess.CalledProcessError:
        return False


def candidate_refs(repo: Path, branch: BranchState, remote_name: str) -> List[str]:
    refs: List[str] = []
    seen = set()

    def add(ref_name: Optional[str]) -> None:
        if not ref_name or ref_name in seen:
            return
        if remote_ref_exists(repo, ref_name):
            refs.append(ref_name)
            seen.add(ref_name)

    add(branch.upstream)
    add(fallback_upstream(repo, branch.name, "origin"))
    add(fallback_upstream(repo, branch.name, remote_name))
    for remote in list_remotes(repo):
        add(f"{remote}/{branch.name}")
    return refs


def resolve_target(repo: Path, branch: BranchState, remote_name: str) -> None:
    refs = candidate_refs(repo, branch, remote_name)
    if not refs:
        branch.blocker = (
            f"branch `{branch.name}` has no usable remote target "
            f"(missing upstream and same-name remote branches)"
        )
        return

    for ref_name in refs:
        counts = git_output(repo, "rev-list", "--left-right", "--count", f"{branch.name}...{ref_name}")
        ahead_text, behind_text = counts.split()
        ahead = int(ahead_text)
        behind = int(behind_text)
        if ahead > 0:
            branch.skipped_targets.append(f"{ref_name} (local ahead by {ahead})")
            continue
        branch.target_ref = ref_name
        branch.ahead = ahead
        branch.behind = behind
        return

    branch.blocker = (
        f"branch `{branch.name}` is ahead of every candidate remote target: "
        + ", ".join(branch.skipped_targets)
    )


def build_repo_plan(repo: Path, remote_name: str) -> RepoPlan:
    run_git(repo, "fetch", "--all", "--prune")

    current_branch = git_output(repo, "branch", "--show-current")
    dirty = bool(git_output(repo, "status", "--porcelain"))
    plan = RepoPlan(path=repo, current_branch=current_branch, dirty=dirty)

    if not current_branch:
        plan.blockers.append("detached HEAD is not supported for bulk branch sync")

    if dirty:
        plan.blockers.append("working tree is dirty; bulk sync does not auto-stash")

    branch_lines = git_output(
        repo,
        "for-each-ref",
        "--format=%(refname:short)|%(upstream:short)|%(HEAD)",
        "refs/heads",
    ).splitlines()

    if not branch_lines:
        plan.blockers.append("no local branches were found")
        return plan

    for line in branch_lines:
        branch = parse_branch_line(line)
        resolve_target(repo, branch, remote_name)
        if branch.blocker:
            plan.blockers.append(branch.blocker)
        plan.branches.append(branch)

    return plan


def print_plan(plans: List[RepoPlan], dry_run: bool) -> None:
    mode_label = "Dry run" if dry_run else "Preflight"
    print(f"{mode_label}: {len(plans)} repo(s)")
    for plan in plans:
        print(f"- {plan.path}")
        print(f"  current={plan.current_branch or 'DETACHED'} dirty={'yes' if plan.dirty else 'no'}")
        for branch in plan.branches:
            upstream = branch.target_ref or branch.upstream or "missing"
            marker = "*" if branch.is_current else "-"
            print(
                f"  {marker} {branch.name} -> {upstream} ahead={branch.ahead} behind={branch.behind}"
            )
            for skipped in branch.skipped_targets:
                print(f"    skipped_target: {skipped}")
            if branch.blocker:
                print(f"    branch_blocker: {branch.blocker}")
        if plan.blockers:
            for blocker in plan.blockers:
                print(f"  blocker: {blocker}")
        else:
            print(f"  update_count: {plan.update_count}")


def apply_plan(plan: RepoPlan) -> None:
    ordered_branches = sorted(plan.branches, key=lambda branch: (not branch.is_current, branch.name))
    for branch in ordered_branches:
        if not branch.needs_update:
            continue
        if branch.is_current:
            run_git(plan.path, "merge", "--ff-only", branch.target_ref)
        else:
            run_git(plan.path, "branch", "-f", branch.name, branch.target_ref)


def main() -> int:
    args = parse_args()
    requested_path = Path(args.path).expanduser()
    if not requested_path.exists():
        print(f"Path does not exist: {requested_path}", file=sys.stderr)
        return 2

    repos = discover_repos(requested_path)
    if not repos:
        print(f"No git repos found under {requested_path}", file=sys.stderr)
        return 2

    plans = [build_repo_plan(repo, args.remote) for repo in repos]
    print_plan(plans, args.dry_run)

    if args.dry_run:
        return 0

    applicable = [plan for plan in plans if not plan.has_blockers]
    blocked = [plan for plan in plans if plan.has_blockers]
    if not applicable:
        print("\nStopped before applying any local branch updates because every repo had blockers.", file=sys.stderr)
        return 1

    for plan in applicable:
        apply_plan(plan)

    print("\nApplied updates successfully.")
    for plan in applicable:
        print(f"- {plan.path}: updated {plan.update_count} branch(es)")
    if blocked:
        print("\nSkipped repos with blockers:")
        for plan in blocked:
            print(f"- {plan.path}")
            for blocker in plan.blockers:
                print(f"  blocker: {blocker}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
