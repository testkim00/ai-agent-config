#!/usr/bin/env python3

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


AREA_PREFIXES = {
    "app",
    "apps",
    "client",
    "clients",
    "lib",
    "libs",
    "package",
    "packages",
    "server",
    "servers",
    "service",
    "services",
    "src",
}


def run_git(repo_path, *args):
    result = subprocess.run(
        ["git", "-C", str(repo_path), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def resolve_repo_root(repo_path):
    code, output, error = run_git(repo_path, "rev-parse", "--show-toplevel")
    if code != 0:
        raise RuntimeError(error.strip() or f"Not a Git repository: {repo_path}")
    return Path(output.strip())


def derive_area(file_path):
    normalized = file_path.replace("\\", "/")
    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return "(root)"
    if len(parts) == 1:
        return parts[0]
    if parts[0] in AREA_PREFIXES:
        return "/".join(parts[:2])
    return parts[0]


def parse_name_status_line(line):
    parts = line.split("\t")
    if not parts:
        return None

    token = parts[0].strip()
    if not token:
        return None

    status = token[0]
    if status in {"R", "C"} and len(parts) >= 3:
        return {
            "status": status,
            "path": parts[2],
            "old_path": parts[1],
        }
    if len(parts) >= 2:
        return {
            "status": status,
            "path": parts[1],
        }
    return None


def collect_repo_activity(repo_path, since, until, include_merges, max_commits, max_files_per_commit):
    repo_root = resolve_repo_root(repo_path)
    branch_code, branch_output, _ = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    branch = branch_output.strip() if branch_code == 0 else "UNKNOWN"

    rev_list_args = ["rev-list", "--count", f"--since={since}", f"--until={until}"]
    if not include_merges:
        rev_list_args.append("--no-merges")
    rev_list_args.append("HEAD")
    count_code, count_output, count_error = run_git(repo_root, *rev_list_args)
    if count_code != 0:
        raise RuntimeError(count_error.strip())
    total_commits = int((count_output or "0").strip() or "0")

    log_args = [
        "log",
        f"--since={since}",
        f"--until={until}",
        "--date=short",
        "--find-renames",
        f"--max-count={max_commits}",
        "--pretty=format:%x1e%H%x1f%ad%x1f%an%x1f%s",
        "--name-status",
    ]
    if not include_merges:
        log_args.insert(3, "--no-merges")

    log_code, log_output, log_error = run_git(repo_root, *log_args)
    if log_code != 0:
        raise RuntimeError(log_error.strip())

    commits = []
    authors = Counter()
    status_counts = Counter()
    path_counts = Counter()
    area_counts = Counter()

    for raw_record in log_output.split("\x1e"):
        record = raw_record.strip()
        if not record:
            continue

        lines = [line for line in record.splitlines() if line.strip()]
        if not lines:
            continue

        meta = lines[0].split("\x1f")
        if len(meta) != 4:
            continue

        sha, date, author, subject = meta
        authors[author] += 1

        files = []
        hidden_files = 0
        for line in lines[1:]:
            parsed = parse_name_status_line(line)
            if not parsed:
                continue

            status = parsed["status"]
            path = parsed["path"]
            status_counts[status] += 1
            path_counts[path] += 1
            area_counts[derive_area(path)] += 1

            if len(files) < max_files_per_commit:
                files.append(parsed)
            else:
                hidden_files += 1

        commits.append(
            {
                "sha": sha,
                "short_sha": sha[:8],
                "date": date,
                "author": author,
                "subject": subject,
                "files": files,
                "hidden_file_count": hidden_files,
            }
        )

    return {
        "repo_name": repo_root.name,
        "repo_path": str(repo_root),
        "branch": branch or "UNKNOWN",
        "period": {"since": since, "until": until},
        "commit_count": total_commits,
        "returned_commit_count": len(commits),
        "truncated": total_commits > len(commits),
        "authors": [
            {"name": name, "commit_count": count}
            for name, count in authors.most_common()
        ],
        "file_status_counts": dict(status_counts),
        "top_areas": [
            {"area": name, "changes": count}
            for name, count in area_counts.most_common(10)
        ],
        "top_paths": [
            {"path": name, "changes": count}
            for name, count in path_counts.most_common(15)
        ],
        "commits": commits,
    }


def build_text_output(payload):
    lines = []
    for repo in payload["repositories"]:
        lines.append(
            f"{repo['repo_name']} ({repo['repo_path']}) | branch:{repo['branch']} | "
            f"period:{repo['period']['since']}~{repo['period']['until']} | "
            f"commits:{repo['commit_count']}"
        )
        if repo["top_areas"]:
            areas = ", ".join(
                f"{item['area']}:{item['changes']}" for item in repo["top_areas"][:5]
            )
            lines.append(f"  top areas: {areas}")
        if repo["commits"]:
            lines.append("  representative commits:")
            for commit in repo["commits"][:5]:
                lines.append(
                    f"  - {commit['date']} {commit['short_sha']} {commit['subject']}"
                )
        if repo["truncated"]:
            lines.append(
                f"  note: showing {repo['returned_commit_count']} of {repo['commit_count']} commits"
            )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Collect structured Git activity for one or more repositories."
    )
    parser.add_argument("--since", required=True, help="Start date, for example 2026-03-01")
    parser.add_argument("--until", required=True, help="End date, for example 2026-03-31")
    parser.add_argument(
        "--include-merges",
        action="store_true",
        help="Include merge commits",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=200,
        help="Maximum commits to return per repository",
    )
    parser.add_argument(
        "--max-files-per-commit",
        type=int,
        default=50,
        help="Maximum file entries returned per commit",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format",
    )
    parser.add_argument("repos", nargs="+", help="Repository paths")
    args = parser.parse_args()

    repositories = []
    for raw_repo in args.repos:
        repositories.append(
            collect_repo_activity(
                Path(raw_repo).expanduser(),
                args.since,
                args.until,
                args.include_merges,
                args.max_commits,
                args.max_files_per_commit,
            )
        )

    payload = {
        "period": {"since": args.since, "until": args.until},
        "repository_count": len(repositories),
        "repositories": repositories,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(build_text_output(payload))


if __name__ == "__main__":
    main()
