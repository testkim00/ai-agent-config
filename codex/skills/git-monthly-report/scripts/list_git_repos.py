#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".idea",
    ".next",
    ".nuxt",
    ".venv",
    ".vscode",
    "__pycache__",
    "bin",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "obj",
    "out",
    "target",
    "tmp",
    "vendor",
}


def run_git(repo_path, *args):
    result = subprocess.run(
        ["git", "-C", str(repo_path), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def discover_repos(root_path, max_depth):
    root_path = root_path.resolve()
    base_depth = len(root_path.parts)
    repos = []

    for current, dirs, files in os.walk(root_path):
        current_path = Path(current)
        depth = len(current_path.parts) - base_depth
        git_marker = ".git" in dirs or ".git" in files

        if depth > max_depth:
            dirs[:] = []
            continue

        if git_marker:
            repos.append(current_path)
            dirs[:] = []
            continue

        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]

    return repos


def get_repo_metadata(repo_path):
    top_code, top_level, _ = run_git(repo_path, "rev-parse", "--show-toplevel")
    if top_code != 0:
        return None

    repo_root = Path(top_level)
    _, branch, _ = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    _, last_commit_date, _ = run_git(repo_root, "log", "-1", "--format=%cs")
    _, dirty_output, _ = run_git(repo_root, "status", "--porcelain")

    return {
        "name": repo_root.name,
        "path": str(repo_root),
        "branch": branch or "UNKNOWN",
        "last_commit_date": last_commit_date or "",
        "dirty": bool(dirty_output),
    }


def sort_key(item):
    return (item["last_commit_date"] or "", item["name"].lower(), item["path"])


def build_text_output(repos):
    lines = []
    for index, repo in enumerate(repos, start=1):
        dirty = "yes" if repo["dirty"] else "no"
        lines.append(
            f"[{index}] {repo['name']} | {repo['path']} | branch:{repo['branch']} | "
            f"last:{repo['last_commit_date'] or '-'} | dirty:{dirty}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="List Git repositories under one or more roots."
    )
    parser.add_argument(
        "roots",
        nargs="*",
        default=[os.getcwd()],
        help="Root directories to search",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=4,
        help="Maximum directory depth to search under each root",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    seen = set()
    repos = []

    for raw_root in args.roots:
        root_path = Path(raw_root).expanduser()
        if not root_path.exists():
            continue

        for repo_path in discover_repos(root_path, args.max_depth):
            metadata = get_repo_metadata(repo_path)
            if not metadata:
                continue
            if metadata["path"] in seen:
                continue
            seen.add(metadata["path"])
            repos.append(metadata)

    repos.sort(key=sort_key, reverse=True)

    if args.format == "json":
        print(json.dumps(repos, indent=2, ensure_ascii=False))
        return

    print(build_text_output(repos))


if __name__ == "__main__":
    main()
