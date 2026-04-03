#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
REVIEW_SCRIPTS_DIR = Path("/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/scripts")
for candidate in (SCRIPT_DIR, REVIEW_SCRIPTS_DIR):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import feedback_context as feedback_state  # noqa: E402
import propose_feedback_improvements as proposer  # noqa: E402


SCHEMA_VERSION = "feedback-loop-apply-plan/v1"
DEFAULT_APPLY_PLANS_DIR = Path.home() / ".codex" / "logs" / "feedback-loop" / "apply-plans"


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select and prepare one safe feedback-loop improvement for application.")
    parser.add_argument("--proposal-report", help="Existing proposal report path.")
    parser.add_argument("--report", help="Existing analyzer report path.")
    parser.add_argument("--events-dir", default=str(proposer.analyzer.DEFAULT_EVENTS_DIR))
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--date")
    parser.add_argument("--all-history", action="store_true")
    parser.add_argument("--session-id")
    parser.add_argument("--feedback-origin")
    parser.add_argument("--feedback-run-kind")
    parser.add_argument("--feedback-cycle-id")
    parser.add_argument("--exclude-feedback-runs", action="store_true")
    parser.add_argument("--skills-root", default=str(proposer.DEFAULT_SKILLS_ROOT))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--proposal-id")
    parser.add_argument("--activate-context", action="store_true")
    parser.add_argument("--origin", default="feedback-loop-apply")
    parser.add_argument("--run-kind", default="feedback_apply")
    parser.add_argument("--cycle-id")
    parser.add_argument("--notes")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--save", action="store_true")
    return parser.parse_args()


def build_proposal_report(args: argparse.Namespace) -> Dict[str, Any]:
    if args.proposal_report:
        return json.loads(Path(args.proposal_report).expanduser().read_text(encoding="utf-8"))

    namespace = SimpleNamespace(
        report=args.report,
        events_dir=args.events_dir,
        days=args.days,
        date=args.date,
        all_history=args.all_history,
        session_id=args.session_id,
        feedback_origin=args.feedback_origin,
        feedback_run_kind=args.feedback_run_kind,
        feedback_cycle_id=args.feedback_cycle_id,
        exclude_feedback_runs=args.exclude_feedback_runs,
        skills_root=args.skills_root,
        limit=args.limit,
        format="json",
        save=False,
    )
    return proposer.build_proposal_report(namespace)


def select_proposal(report: Dict[str, Any], proposal_id: Optional[str]) -> Optional[Dict[str, Any]]:
    items = report.get("proposal_items", [])
    if proposal_id:
        for item in items:
            if item["id"] == proposal_id:
                return item
        return None

    for item in items:
        if item.get("auto_apply", {}).get("eligible"):
            return item
    return None


def infer_validation_hints(selected: Optional[Dict[str, Any]]) -> List[str]:
    if not selected:
        return []

    hints: List[str] = []
    safe_candidates = selected.get("auto_apply", {}).get("safe_candidate_paths", [])
    paths = [candidate["path"] for candidate in safe_candidates]

    if any(path.endswith(".py") for path in paths):
        hints.append("Run `python3 -m py_compile` on the touched Python files.")
    if any(path.endswith(".json") for path in paths):
        hints.append("Run `python3 -m json.tool` on the touched JSON files.")
    if any("/hooks/" in path for path in paths):
        hints.append("Run one synthetic hook payload through the changed hook path before stopping.")
    if any(path.endswith(".md") for path in paths):
        hints.append("Read the changed markdown end-to-end once to confirm the new workflow still reads cleanly.")

    if not hints:
        hints.append("Run the smallest targeted validation that proves the selected improvement works.")

    return hints


def build_feedback_context(args: argparse.Namespace, proposal_report_path: Optional[str], selected: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not selected:
        return None

    cycle_id = args.cycle_id or f"feedback-{datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z')}"
    proposal_path = Path(args.proposal_report).expanduser() if args.proposal_report else proposal_report_path
    context = {
        "active": True,
        "origin": args.origin,
        "run_kind": args.run_kind,
        "cycle_id": cycle_id,
        "experiment_id": cycle_id,
        "proposal_id": selected["id"],
        "source_report_path": str(Path(args.report).expanduser()) if args.report else None,
        "source_proposal_path": str(proposal_path) if proposal_path else None,
        "notes": args.notes,
        "activated_at": iso_now(),
        "updated_at": iso_now(),
    }
    return context


def activate_feedback_context(context: Dict[str, Any]) -> None:
    feedback_state.write_context(context)


def build_next_actions(selected: Optional[Dict[str, Any]]) -> List[str]:
    if not selected:
        return [
            "No auto-applyable proposal was available in the selected report window.",
            "Inspect the manual-only proposals and choose one for manual application if needed.",
        ]

    safe_candidates = selected.get("auto_apply", {}).get("safe_candidate_paths", [])
    candidate_text = ", ".join(candidate["path"] for candidate in safe_candidates[:3])
    return [
        f"Patch the selected safe candidate paths: {candidate_text}.",
        "Switch the feedback context to `feedback_recheck` before validation.",
        "Run one targeted validation for the touched files or hook path.",
        "Clear the feedback context after the recheck completes.",
    ]


def build_plan(args: argparse.Namespace) -> Dict[str, Any]:
    proposal_report = build_proposal_report(args)
    selected = select_proposal(proposal_report, args.proposal_id)
    context = build_feedback_context(args, Path(args.proposal_report).expanduser() if args.proposal_report else None, selected)

    if args.activate_context and context:
        activate_feedback_context(context)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "source_summary": {
            "proposal_schema_version": proposal_report.get("schema_version"),
            "window": proposal_report.get("source_summary", {}).get("window"),
            "turns": proposal_report.get("source_summary", {}).get("turns", 0),
            "backlog_items": proposal_report.get("source_summary", {}).get("backlog_items", 0),
            "proposals_seen": len(proposal_report.get("proposal_items", [])),
        },
        "selected_proposal": selected,
        "feedback_context": context,
        "next_actions": build_next_actions(selected),
        "validation_hints": infer_validation_hints(selected),
    }


def format_markdown(plan: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Feedback Loop Apply Plan")
    lines.append("")
    lines.append(f"- Generated: `{plan['generated_at']}`")
    lines.append(f"- Source turns: `{plan['source_summary']['turns']}`")
    lines.append(f"- Proposals seen: `{plan['source_summary']['proposals_seen']}`")
    lines.append("")

    selected = plan.get("selected_proposal")
    if not selected:
        lines.append("- No auto-applyable proposal was selected.")
        return "\n".join(lines)

    lines.append(f"## {selected['id']}")
    lines.append("")
    lines.append(
        f"- Severity: `{selected['severity']}`  Target: `{selected['target']}`  Confidence: `{selected['confidence']}`"
    )
    lines.append(f"- Summary: {selected['summary']}")
    lines.append(f"- Auto-apply scope: `{selected['auto_apply']['scope']}`")
    if selected["auto_apply"]["safe_candidate_paths"]:
        lines.append("- Safe candidate paths:")
        for candidate in selected["auto_apply"]["safe_candidate_paths"]:
            lines.append(f"  - `{candidate['mode']}` `{candidate['path']}`: {candidate['reason']}")
    if selected["auto_apply"]["blocked_candidate_paths"]:
        lines.append("- Blocked candidate paths:")
        for candidate in selected["auto_apply"]["blocked_candidate_paths"]:
            lines.append(f"  - `{candidate['mode']}` `{candidate['path']}`: {candidate['block_reason']}")

    lines.append("")
    lines.append("## Context")
    if plan["feedback_context"]:
        context = plan["feedback_context"]
        lines.append(
            f"- origin=`{context['origin']}` run_kind=`{context['run_kind']}` cycle_id=`{context['cycle_id']}` proposal_id=`{context['proposal_id']}`"
        )
    else:
        lines.append("- No feedback context was created because no proposal was selected.")

    lines.append("")
    lines.append("## Next Actions")
    for action in plan["next_actions"]:
        lines.append(f"- {action}")

    lines.append("")
    lines.append("## Validation Hints")
    for hint in plan["validation_hints"]:
        lines.append(f"- {hint}")
    return "\n".join(lines)


def save_plan(plan: Dict[str, Any]) -> Path:
    DEFAULT_APPLY_PLANS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    report_path = DEFAULT_APPLY_PLANS_DIR / f"{timestamp}.json"
    latest_path = DEFAULT_APPLY_PLANS_DIR / "latest.json"
    payload = json.dumps(plan, ensure_ascii=False, indent=2)
    report_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return report_path


def main() -> int:
    args = parse_args()
    plan = build_plan(args)

    if args.save:
        saved_path = save_plan(plan)
        print(f"Saved apply plan to {saved_path}", file=sys.stderr)

    if args.format == "json":
        json.dump(plan, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(format_markdown(plan))
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
