#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List


SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = Path("/Users/honeychaser/Projects/ai-agent-config/codex/skills")
REVIEW_SCRIPTS_DIR = SKILLS_ROOT / "feedback-loop-review" / "scripts"
APPLY_SCRIPTS_DIR = SKILLS_ROOT / "feedback-loop-apply" / "scripts"

for candidate in (SCRIPT_DIR, REVIEW_SCRIPTS_DIR, APPLY_SCRIPTS_DIR):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import analyze_feedback_loop as analyzer  # noqa: E402
import apply_feedback_improvements as applyer  # noqa: E402
import propose_feedback_improvements as proposer  # noqa: E402


SCHEMA_VERSION = "feedback-loop-run/v1"
DEFAULT_RUNS_DIR = Path.home() / ".codex" / "logs" / "feedback-loop" / "runs"


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the top-level Codex feedback loop.")
    parser.add_argument("--events-dir", default=str(analyzer.DEFAULT_EVENTS_DIR))
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--date")
    parser.add_argument(
        "--all-history",
        action="store_true",
        help="Also load every historical event file for a separate historical-signals section. Proposal selection still uses the recent baseline window.",
    )
    parser.add_argument("--session-id")
    parser.add_argument("--proposal-id")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--skills-root", default=str(proposer.DEFAULT_SKILLS_ROOT))
    parser.add_argument("--activate-context", action="store_true")
    parser.add_argument("--origin", default="feedback-loop-apply")
    parser.add_argument("--run-kind", default="feedback_apply")
    parser.add_argument("--cycle-id")
    parser.add_argument("--notes")
    parser.add_argument("--cycle-review", help="Review a specific tagged feedback cycle instead of producing a new baseline/apply plan.")
    parser.add_argument("--include-feedback-runs", action="store_true", help="Include feedback-tagged runs in the default baseline analysis.")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--save", action="store_true")
    return parser.parse_args()


def build_baseline_args(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        events_dir=args.events_dir,
        days=args.days,
        date=args.date,
        all_history=False,
        session_id=args.session_id,
        feedback_origin=None,
        feedback_run_kind=None,
        feedback_cycle_id=None,
        exclude_feedback_runs=not args.include_feedback_runs,
        format="json",
    )


def build_historical_args(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        events_dir=args.events_dir,
        days=args.days,
        date=None,
        all_history=True,
        session_id=args.session_id,
        feedback_origin=None,
        feedback_run_kind=None,
        feedback_cycle_id=None,
        exclude_feedback_runs=not args.include_feedback_runs,
        format="json",
    )


def build_cycle_review_args(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        events_dir=args.events_dir,
        days=args.days,
        date=args.date,
        all_history=False,
        session_id=args.session_id,
        feedback_origin="feedback-loop-apply",
        feedback_run_kind=None,
        feedback_cycle_id=args.cycle_review,
        exclude_feedback_runs=False,
        format="json",
    )


def build_proposal_args(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        report=None,
        events_dir=args.events_dir,
        days=args.days,
        date=args.date,
        all_history=False,
        session_id=args.session_id,
        feedback_origin=None,
        feedback_run_kind=None,
        feedback_cycle_id=None,
        exclude_feedback_runs=not args.include_feedback_runs,
        skills_root=args.skills_root,
        limit=args.limit,
        format="json",
        save=False,
    )


def build_apply_args(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        proposal_report=None,
        report=None,
        events_dir=args.events_dir,
        days=args.days,
        date=args.date,
        all_history=False,
        session_id=args.session_id,
        feedback_origin=None,
        feedback_run_kind=None,
        feedback_cycle_id=None,
        exclude_feedback_runs=not args.include_feedback_runs,
        skills_root=args.skills_root,
        limit=args.limit,
        proposal_id=args.proposal_id,
        activate_context=args.activate_context,
        origin=args.origin,
        run_kind=args.run_kind,
        cycle_id=args.cycle_id,
        notes=args.notes,
        format="json",
        save=False,
    )


def top_backlog_items(report: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
    return report.get("improvement_backlog", [])[:limit]


def current_context_hint(plan: Dict[str, Any]) -> str:
    context = plan.get("feedback_context")
    if not context:
        return "inactive"
    return f"{context['run_kind']}:{context['cycle_id']}"


def build_full_run(args: argparse.Namespace) -> Dict[str, Any]:
    evaluation = analyzer.build_report(build_baseline_args(args))
    historical_evaluation = analyzer.build_report(build_historical_args(args)) if args.all_history else None
    proposals = proposer.build_proposal_report(build_proposal_args(args))
    apply_plan = applyer.build_plan(build_apply_args(args))

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "mode": "full",
        "baseline_evaluation": evaluation,
        "historical_evaluation": historical_evaluation,
        "proposal_report": proposals,
        "apply_plan": apply_plan,
        "summary": {
            "recent_turns": evaluation.get("summary", {}).get("turns", 0),
            "historical_turns": historical_evaluation.get("summary", {}).get("turns", 0) if historical_evaluation else 0,
            "top_backlog_items": len(top_backlog_items(evaluation)),
            "proposals_seen": len(proposals.get("proposal_items", [])),
            "selected_proposal_id": (apply_plan.get("selected_proposal") or {}).get("id"),
            "feedback_context": current_context_hint(apply_plan),
        },
    }


def build_cycle_run(args: argparse.Namespace) -> Dict[str, Any]:
    evaluation = analyzer.build_report(build_cycle_review_args(args))
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "mode": "cycle_review",
        "cycle_id": args.cycle_review,
        "cycle_evaluation": evaluation,
        "summary": {
            "turns": evaluation.get("summary", {}).get("turns", 0),
            "feedback_turns": evaluation.get("summary", {}).get("feedback_turns", 0),
            "top_backlog_items": len(top_backlog_items(evaluation)),
        },
    }


def format_full_markdown(report: Dict[str, Any]) -> str:
    evaluation = report["baseline_evaluation"]
    historical = report.get("historical_evaluation")
    proposals = report["proposal_report"]
    apply_plan = report["apply_plan"]
    summary = evaluation["summary"]
    backlog = top_backlog_items(evaluation)
    historical_backlog = top_backlog_items(historical) if historical else []
    selected = apply_plan.get("selected_proposal")

    lines: List[str] = []
    lines.append("# Feedback Loop")
    lines.append("")
    lines.append(f"- Generated: `{report['generated_at']}`")
    lines.append(f"- Recent turns: `{report['summary']['recent_turns']}`")
    lines.append(f"- Recent high-risk turns: `{summary['high_risk_turns']}`")
    if historical:
        lines.append(f"- Historical turns: `{report['summary']['historical_turns']}`")
    lines.append(f"- Proposals seen: `{len(proposals.get('proposal_items', []))}`")
    lines.append(f"- Selected proposal: `{(selected or {}).get('id', 'none')}`")
    lines.append(f"- Feedback context: `{report['summary']['feedback_context']}`")
    lines.append("")

    lines.append("## Recent Signals")
    if backlog:
        for item in backlog:
            lines.append(
                f"- `{item['severity']}` `{item['code']}` -> `{item['target']}` "
                f"(weighted: `{item['weighted_occurrences']}`, occurrences: `{item['occurrences']}`, confidence: `{item['confidence']}`)"
            )
    else:
        lines.append("- No backlog items were produced from the recent baseline window.")

    if historical:
        lines.append("")
        lines.append("## Historical Signals")
        lines.append("- This section scans all event files and is advisory. Proposal selection still uses the recent baseline window.")
        if historical_backlog:
            for item in historical_backlog:
                lines.append(
                    f"- `{item['severity']}` `{item['code']}` -> `{item['target']}` "
                    f"(weighted: `{item['weighted_occurrences']}`, occurrences: `{item['occurrences']}`, confidence: `{item['confidence']}`)"
                )
        else:
            lines.append("- No backlog items were produced from full history.")

    lines.append("")
    lines.append("## Top Proposal")
    if selected:
        lines.append(
            f"- `{selected['id']}` `{selected['target']}` confidence=`{selected['confidence']}`: {selected['summary']}"
        )
        lines.append(
            f"- Auto-apply scope: `{selected['auto_apply']['scope']}` eligible=`{str(selected['auto_apply']['eligible']).lower()}`"
        )
        safe_candidates = selected["auto_apply"]["safe_candidate_paths"]
        if safe_candidates:
            lines.append("- Safe candidate paths:")
            for candidate in safe_candidates[:3]:
                lines.append(f"  - `{candidate['mode']}` `{candidate['path']}`")
    else:
        lines.append("- No safe proposal was selected.")

    lines.append("")
    lines.append("## Apply Plan")
    for action in apply_plan.get("next_actions", []):
        lines.append(f"- {action}")
    if apply_plan.get("validation_hints"):
        lines.append("- Validation hints:")
        for hint in apply_plan["validation_hints"]:
            lines.append(f"  - {hint}")

    if apply_plan.get("feedback_context"):
        cycle_id = apply_plan["feedback_context"]["cycle_id"]
        lines.append("")
        lines.append("## Follow-up")
        lines.append(
            f"- After patch + recheck, inspect the cycle with: `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/scripts/run_feedback_loop.py --cycle-review {cycle_id} --format markdown`"
        )

    return "\n".join(lines)


def format_cycle_markdown(report: Dict[str, Any]) -> str:
    evaluation = report["cycle_evaluation"]
    summary = evaluation["summary"]
    backlog = top_backlog_items(evaluation)

    lines: List[str] = []
    lines.append("# Feedback Loop Cycle Review")
    lines.append("")
    lines.append(f"- Generated: `{report['generated_at']}`")
    lines.append(f"- Cycle id: `{report['cycle_id']}`")
    lines.append(f"- Feedback turns: `{summary['feedback_turns']}`")
    lines.append(f"- Findings: `P1={summary['findings_by_severity']['P1']}`, `P2={summary['findings_by_severity']['P2']}`, `P3={summary['findings_by_severity']['P3']}`")
    lines.append("")
    lines.append("## Cycle Backlog")
    if backlog:
        for item in backlog:
            lines.append(
                f"- `{item['severity']}` `{item['code']}` -> `{item['target']}` "
                f"(occurrences: `{item['occurrences']}`, confidence: `{item['confidence']}`)"
            )
    else:
        lines.append("- No backlog items were produced for this tagged cycle.")
    return "\n".join(lines)


def save_report(report: Dict[str, Any]) -> Path:
    DEFAULT_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    path = DEFAULT_RUNS_DIR / f"{timestamp}.json"
    latest_path = DEFAULT_RUNS_DIR / "latest.json"
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    report = build_cycle_run(args) if args.cycle_review else build_full_run(args)

    if args.save:
        saved_path = save_report(report)
        print(f"Saved feedback loop report to {saved_path}", file=sys.stderr)

    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        formatter = format_cycle_markdown if args.cycle_review else format_full_markdown
        sys.stdout.write(formatter(report))
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
