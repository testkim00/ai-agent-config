#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "target",
    ".venv",
    "venv",
    "__pycache__",
}
PRESETS_DIR = Path(__file__).resolve().parents[1] / "presets"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List repo harness status for git repositories.")
    parser.add_argument("roots", nargs="*", default=["."], help="Roots to scan")
    parser.add_argument("--max-depth", type=int, default=4, help="Maximum directory depth to scan")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    return parser.parse_args()


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def load_harness(repo_root: Path) -> Dict[str, object]:
    path = repo_root / ".codex" / "harness.json"
    if not path.exists():
        return {
            "exists": False,
            "path": str(path),
            "valid": False,
            "error": None,
            "preset": None,
            "name": None,
            "enforce": None,
            "required_all_count": 0,
            "required_any_count": 0,
        }

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {
            "exists": True,
            "path": str(path),
            "valid": False,
            "error": str(exc),
            "preset": None,
            "name": None,
            "enforce": None,
            "required_all_count": 0,
            "required_any_count": 0,
        }

    if not isinstance(payload, dict):
        return {
            "exists": True,
            "path": str(path),
            "valid": False,
            "error": "harness.json is not an object",
            "preset": None,
            "name": None,
            "enforce": None,
            "required_all_count": 0,
            "required_any_count": 0,
        }

    preset_name = payload.get("preset") if isinstance(payload.get("preset"), str) and payload.get("preset").strip() else None
    preset_payload: Dict[str, object] = {}
    if preset_name:
        preset_path = PRESETS_DIR / f"{preset_name}.json"
        if preset_path.exists():
            loaded = json.loads(preset_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                preset_payload = loaded
    required_all = payload.get("required_all", preset_payload.get("required_all"))
    required_any = payload.get("required_any", preset_payload.get("required_any"))
    enforce = payload.get("enforce", preset_payload.get("enforce"))
    return {
        "exists": True,
        "path": str(path),
        "valid": True,
        "error": None,
        "preset": preset_name,
        "name": payload.get("name"),
        "enforce": enforce,
        "required_all_count": len(required_all) if isinstance(required_all, list) else 0,
        "required_any_count": len(required_any) if isinstance(required_any, list) else 0,
    }


def scan_repos(roots: Iterable[str], max_depth: int) -> List[Path]:
    found: List[Path] = []
    seen = set()

    for root_text in roots:
        root = Path(root_text).expanduser().resolve()
        if not root.exists():
            continue
        if root.is_file():
            root = root.parent

        if is_git_repo(root):
            if root not in seen:
                seen.add(root)
                found.append(root)
            continue

        base_depth = len(root.parts)
        for current_root, dirnames, _filenames in os.walk(root):
            current = Path(current_root)
            depth = len(current.parts) - base_depth
            dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
            if depth > max_depth:
                dirnames[:] = []
                continue
            if is_git_repo(current):
                if current not in seen:
                    seen.add(current)
                    found.append(current)
                dirnames[:] = [name for name in dirnames if name != ".git"]

    found.sort()
    return found


def build_rows(repos: Iterable[Path]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for repo in repos:
        harness = load_harness(repo)
        rows.append(
            {
                "repo_name": repo.name,
                "repo_root": str(repo),
                **harness,
            }
        )
    return rows


def print_text(rows: List[Dict[str, object]]) -> None:
    if not rows:
        print("No git repositories found.")
        return

    header = f"{'repo':30} {'harness':7} {'valid':5} {'enforce':7} {'preset':18} {'all':3} {'any':3} path"
    print(header)
    print("-" * len(header))
    for row in rows:
        repo_name = str(row["repo_name"])[:30].ljust(30)
        harness = ("yes" if row["exists"] else "no").ljust(7)
        valid = ("yes" if row["valid"] else "no").ljust(5)
        enforce_value = row["enforce"]
        enforce = ("yes" if enforce_value is True else "no" if enforce_value is False else "-").ljust(7)
        preset = str(row.get("preset") or "-")[:18].ljust(18)
        all_count = str(row["required_all_count"]).rjust(3)
        any_count = str(row["required_any_count"]).rjust(3)
        path = str(row["path"])
        print(f"{repo_name} {harness} {valid} {enforce} {preset} {all_count} {any_count} {path}")
        if row["error"]:
            print(f"  error: {row['error']}")


def main() -> int:
    args = parse_args()
    repos = scan_repos(args.roots, args.max_depth)
    rows = build_rows(repos)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_text(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
