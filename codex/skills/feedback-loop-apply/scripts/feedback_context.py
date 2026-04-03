#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


STATE_PATH = Path.home() / ".codex" / "logs" / "feedback-loop" / "state" / "feedback-context.json"


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_context() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {"active": False}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def write_context(payload: Dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_path(value: str) -> str:
    return str(Path(value).expanduser())


def base_context() -> Dict[str, Any]:
    return {
        "active": False,
        "origin": "direct",
        "run_kind": "baseline",
        "cycle_id": None,
        "experiment_id": None,
        "proposal_id": None,
        "source_report_path": None,
        "source_proposal_path": None,
        "notes": None,
        "activated_at": None,
        "updated_at": None,
    }


def merge_fields(context: Dict[str, Any], args: argparse.Namespace, default_origin: str = "", default_run_kind: str = "") -> Dict[str, Any]:
    updated = dict(context)

    if getattr(args, "origin", None):
        updated["origin"] = args.origin
    elif default_origin and updated.get("origin") in (None, "", "direct"):
        updated["origin"] = default_origin

    if getattr(args, "run_kind", None):
        updated["run_kind"] = args.run_kind
    elif default_run_kind and updated.get("run_kind") in (None, "", "baseline"):
        updated["run_kind"] = default_run_kind

    for field in ("cycle_id", "experiment_id", "proposal_id", "notes"):
        value = getattr(args, field, None)
        if value:
            updated[field] = value

    if getattr(args, "report_path", None):
        updated["source_report_path"] = normalize_path(args.report_path)
    if getattr(args, "proposal_path", None):
        updated["source_proposal_path"] = normalize_path(args.proposal_path)

    return updated


def command_start(args: argparse.Namespace) -> Dict[str, Any]:
    context = base_context()
    context = merge_fields(context, args, default_origin="feedback-loop-apply", default_run_kind="feedback_apply")
    context["active"] = True
    context["cycle_id"] = context.get("cycle_id") or f"feedback-{datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z')}"
    context["experiment_id"] = context.get("experiment_id") or context["cycle_id"]
    context["activated_at"] = context.get("activated_at") or iso_now()
    context["updated_at"] = iso_now()
    write_context(context)
    return context


def command_update(args: argparse.Namespace) -> Dict[str, Any]:
    context = base_context()
    context.update(read_context())
    context = merge_fields(context, args)
    context["active"] = True
    context["cycle_id"] = context.get("cycle_id") or f"feedback-{datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z')}"
    context["experiment_id"] = context.get("experiment_id") or context["cycle_id"]
    context["activated_at"] = context.get("activated_at") or iso_now()
    context["updated_at"] = iso_now()
    write_context(context)
    return context


def command_stop(_: argparse.Namespace) -> Dict[str, Any]:
    if STATE_PATH.exists():
        STATE_PATH.unlink()
    return {"active": False}


def command_show(_: argparse.Namespace) -> Dict[str, Any]:
    context = base_context()
    context.update(read_context())
    return context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage feedback-loop run context for hook logging.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--origin")
        subparser.add_argument("--run-kind")
        subparser.add_argument("--cycle-id")
        subparser.add_argument("--experiment-id")
        subparser.add_argument("--proposal-id")
        subparser.add_argument("--report-path")
        subparser.add_argument("--proposal-path")
        subparser.add_argument("--notes")
        subparser.add_argument("--format", choices=("json", "markdown"), default="json")

    add_common(subparsers.add_parser("start", help="Create and activate a feedback context."))
    add_common(subparsers.add_parser("update", help="Update the active feedback context."))

    stop_parser = subparsers.add_parser("stop", help="Clear the active feedback context.")
    stop_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    show_parser = subparsers.add_parser("show", help="Show the current feedback context.")
    show_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser


def format_markdown(context: Dict[str, Any]) -> str:
    if not context.get("active"):
        return "- Feedback context is inactive."

    lines = [
        f"- active=`{str(context.get('active')).lower()}`",
        f"- origin=`{context.get('origin')}` run_kind=`{context.get('run_kind')}`",
        f"- cycle_id=`{context.get('cycle_id')}` proposal_id=`{context.get('proposal_id') or 'n/a'}`",
    ]
    if context.get("source_report_path"):
        lines.append(f"- report=`{context['source_report_path']}`")
    if context.get("source_proposal_path"):
        lines.append(f"- proposal_report=`{context['source_proposal_path']}`")
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "start":
        context = command_start(args)
    elif args.command == "update":
        context = command_update(args)
    elif args.command == "stop":
        context = command_stop(args)
    else:
        context = command_show(args)

    if args.format == "json":
        json.dump(context, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(format_markdown(context))
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
