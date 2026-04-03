#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


SCHEMA_VERSION = "feedback-loop-evaluation/v1"
DEFAULT_EVENTS_DIR = Path.home() / ".codex" / "logs" / "feedback-loop" / "events"
MAPPING_PATH = Path(__file__).resolve().parent.parent / "references" / "findings-action-map.json"
RECENCY_WEIGHT_POLICY = {
    "0_7_days": 1.0,
    "8_30_days": 0.6,
    "31_90_days": 0.3,
    "91_plus_days": 0.15,
}

HIGH_RISK_TURN_TYPES = {"implementation", "bugfix", "refactor", "ops"}
PRIORITY_ORDER = {"P1": 0, "P2": 1, "P3": 2}

TURN_TYPE_KEYWORDS = {
    "docs": [
        r"\bdocs?\b",
        r"\bdocumentation\b",
        r"\breadme\b",
        r"\bspec\b",
        r"\bproposal\b",
        r"문서",
        r"명세",
    ],
    "bugfix": [
        r"\bfix\b",
        r"\bbug\b",
        r"\berror\b",
        r"\bbroken\b",
        r"\bfail(?:ed|ure)?\b",
        r"깨짐",
        r"실패",
        r"안 됨",
        r"수정",
    ],
    "refactor": [
        r"\brefactor\b",
        r"\bcleanup\b",
        r"\brename\b",
        r"\brestructure\b",
        r"정리",
        r"구조 변경",
    ],
    "ops": [
        r"\bdeploy\b",
        r"\bkubectl\b",
        r"\bdocker\b",
        r"\bterraform\b",
        r"\baz\b",
        r"\bgh pr\b",
        r"\bgit push\b",
        r"배포",
    ],
    "review": [
        r"\breview\b",
        r"\baudit\b",
        r"리뷰",
        r"점검",
    ],
    "analysis": [
        r"\banaly[sz]e\b",
        r"\binvestigate\b",
        r"\borient\b",
        r"\bsummarize\b",
        r"\bcompare\b",
        r"분석",
        r"파악",
        r"비교",
        r"요약",
    ],
}

OPS_COMMAND_PATTERNS = [
    r"\bkubectl\b",
    r"\bdocker\b",
    r"\bterraform\b",
    r"\baz\b",
    r"\bgh pr\b",
    r"\bgit push\b",
    r"\bdeploy\b",
]


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze Codex feedback-loop hook logs.")
    parser.add_argument("--events-dir", default=str(DEFAULT_EVENTS_DIR))
    parser.add_argument("--days", type=int, default=7, help="Number of recent days to load.")
    parser.add_argument("--date", help="Single day to analyze in YYYY-MM-DD format.")
    parser.add_argument("--all-history", action="store_true", help="Load all event files under the events directory.")
    parser.add_argument("--session-id", help="Filter to one session_id.")
    parser.add_argument("--feedback-origin", help="Only include events tagged with this feedback origin.")
    parser.add_argument("--feedback-run-kind", help="Only include events tagged with this feedback run kind.")
    parser.add_argument("--feedback-cycle-id", help="Only include events tagged with this feedback cycle id.")
    parser.add_argument(
        "--exclude-feedback-runs",
        action="store_true",
        help="Exclude events that were explicitly tagged as feedback-loop runs.",
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    return parser.parse_args()


def load_action_map() -> Dict[str, Dict[str, Any]]:
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def normalize_command(value: str) -> str:
    normalized = normalize_text(value).lower()
    normalized = re.sub(r"/var/folders/[^\s]+", "<tmp>", normalized)
    normalized = re.sub(r"/tmp/[^\s]+", "<tmp>", normalized)
    normalized = re.sub(r"\b\d{4,}\b", "<n>", normalized)
    return normalized


def parse_recorded_at(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def normalize_feedback_context(feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    feedback = feedback or {}
    is_feedback_run = bool(feedback.get("is_feedback_run"))
    return {
        "is_feedback_run": is_feedback_run,
        "origin": feedback.get("origin") or ("feedback-loop-apply" if is_feedback_run else "direct"),
        "run_kind": feedback.get("run_kind") or ("feedback_apply" if is_feedback_run else "baseline"),
        "cycle_id": feedback.get("cycle_id"),
        "experiment_id": feedback.get("experiment_id"),
        "proposal_id": feedback.get("proposal_id"),
    }


def matches_feedback_filters(record: Dict[str, Any], args: argparse.Namespace) -> bool:
    feedback = normalize_feedback_context(record.get("feedback"))

    if args.exclude_feedback_runs and feedback["is_feedback_run"]:
        return False
    if args.feedback_origin and feedback["origin"] != args.feedback_origin:
        return False
    if args.feedback_run_kind and feedback["run_kind"] != args.feedback_run_kind:
        return False
    if args.feedback_cycle_id and feedback["cycle_id"] != args.feedback_cycle_id:
        return False
    return True


def list_event_files(events_dir: Path, selected_date: Optional[str], days: int, all_history: bool) -> List[Path]:
    if selected_date:
        return [events_dir / f"{selected_date}.jsonl"]

    if all_history:
        return sorted(events_dir.glob("*.jsonl"))

    today = date.today()
    return [
        events_dir / f"{(today - timedelta(days=offset)).isoformat()}.jsonl"
        for offset in range(max(days, 1))
    ]


def load_events(files: Iterable[Path], args: argparse.Namespace) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for path in files:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if args.session_id and record.get("session_id") != args.session_id:
                continue
            if not matches_feedback_filters(record, args):
                continue
            events.append(record)
    events.sort(key=lambda item: (item.get("recorded_at") or "", item.get("event") or ""))
    return events


def group_turns(events: List[Dict[str, Any]]) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    turns: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for event in events:
        session_id = event.get("session_id")
        turn_id = event.get("turn_id")
        if not session_id or not turn_id:
            continue
        turns[(session_id, turn_id)].append(event)
    for turn_events in turns.values():
        turn_events.sort(key=lambda item: (item.get("recorded_at") or "", item.get("event") or ""))
    return turns


def extract_prompt(turn_events: List[Dict[str, Any]]) -> Optional[str]:
    for event in turn_events:
        if event.get("event") == "user_prompt_submit":
            return event.get("event_data", {}).get("prompt_preview")
    return None


def command_entries(turn_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for event in turn_events:
        if event.get("event") != "post_tool_use":
            continue
        event_data = event.get("event_data", {})
        analysis = event.get("analysis", {})
        entries.append(
            {
                "command": event_data.get("command") or "",
                "category": analysis.get("command_category") or "other",
                "tags": analysis.get("command_tags") or [],
                "is_validation": bool(analysis.get("is_validation")),
                "status": event_data.get("status") or "completed",
                "exit_code": event_data.get("exit_code"),
                "duration_ms": event_data.get("duration_ms"),
                "tool_use_id": event.get("tool_use_id"),
            }
        )
    return entries


def classify_turn(prompt: Optional[str], commands: List[Dict[str, Any]]) -> str:
    prompt_text = normalize_text(prompt).lower()

    for turn_type in ("docs", "bugfix", "refactor", "ops", "review"):
        patterns = TURN_TYPE_KEYWORDS.get(turn_type, [])
        if any(re.search(pattern, prompt_text) for pattern in patterns):
            return turn_type

    if any(re.search(pattern, entry["command"].lower()) for entry in commands for pattern in OPS_COMMAND_PATTERNS):
        return "ops"

    if prompt_text and any(re.search(pattern, prompt_text) for pattern in TURN_TYPE_KEYWORDS["analysis"]):
        return "analysis"

    if not commands:
        return "analysis"

    return "implementation"


def repeated_commands(commands: List[Dict[str, Any]]) -> Dict[str, int]:
    counter = Counter(normalize_command(entry["command"]) for entry in commands if entry["command"])
    return {command: count for command, count in counter.items() if count > 1}


def failed_repeated_commands(commands: List[Dict[str, Any]]) -> Dict[str, int]:
    counter = Counter(
        normalize_command(entry["command"])
        for entry in commands
        if entry["status"] == "error" and entry["command"]
    )
    return {command: count for command, count in counter.items() if count > 1}


def bool_score(score: int, rationale: str) -> Dict[str, Any]:
    return {"score": score, "rationale": rationale}


def evaluate_scores(turn_type: str, commands: List[Dict[str, Any]], has_stop: bool) -> Dict[str, Dict[str, Any]]:
    command_count = len(commands)
    categories = {entry["category"] for entry in commands}
    validations = [entry for entry in commands if entry["is_validation"]]
    failed_commands = [entry for entry in commands if entry["status"] == "error"]
    failed_validations = [entry for entry in validations if entry["status"] == "error"]
    repeated_all = repeated_commands(commands)
    repeated_failed = failed_repeated_commands(commands)
    last_validation_success = bool(validations and validations[-1]["status"] == "success")

    if turn_type in {"analysis", "docs", "review"} and command_count <= 3:
        task_focus = bool_score(2, "The turn stayed narrow for a low-command task.")
    elif command_count <= 5 and len(categories) <= 3:
        task_focus = bool_score(2, "The command flow stayed within a small relevant working set.")
    elif command_count <= 8 and len(categories) <= 4:
        task_focus = bool_score(1, "The turn had some sprawl but stayed partially focused.")
    else:
        task_focus = bool_score(0, "Too many commands or categories were used for a tight loop.")

    if turn_type in HIGH_RISK_TURN_TYPES:
        if not validations:
            verification = bool_score(0, "High-risk work ended without visible validation.")
        elif last_validation_success:
            verification = bool_score(2, "High-risk work ended with successful validation.")
        else:
            verification = bool_score(1, "Validation ran, but the last visible result was not successful.")
    else:
        if not validations:
            verification = bool_score(2, "This turn type did not require strong validation signals.")
        elif last_validation_success:
            verification = bool_score(2, "Validation was present and ended successfully.")
        else:
            verification = bool_score(1, "Validation exists, but the outcome stayed inconclusive.")

    if any(count >= 3 for count in repeated_failed.values()) or command_count > 12:
        efficiency = bool_score(0, "The turn repeated failed work or used an excessive number of commands.")
    elif repeated_all or command_count > 6:
        efficiency = bool_score(1, "The turn converged, but with noticeable repetition or overhead.")
    else:
        efficiency = bool_score(2, "The turn used a compact command sequence.")

    if not failed_commands:
        recovery = bool_score(2, "No visible failures required recovery.")
    elif last_validation_success:
        recovery = bool_score(2, "The turn recovered from failure and ended with successful validation.")
    elif validations or command_count > len(failed_commands):
        recovery = bool_score(1, "There was some recovery activity, but it remained unresolved.")
    else:
        recovery = bool_score(0, "Failures occurred without a convincing recovery step.")

    if turn_type in HIGH_RISK_TURN_TYPES:
        if validations and last_validation_success and has_stop:
            completion = bool_score(2, "The turn stopped after a visible successful validation.")
        elif validations or not has_stop:
            completion = bool_score(1, "The stop point is arguable but not fully clean.")
        else:
            completion = bool_score(0, "The turn stopped without expected verification discipline.")
    else:
        if has_stop:
            completion = bool_score(2, "The turn has a normal visible stop.")
        else:
            completion = bool_score(1, "The turn lacks a clear stop signal.")

    if command_count >= 5 or len(repeated_all) >= 2 or len(validations) >= 2:
        automation = bool_score(2, "The workflow is repetitive enough to standardize.")
    elif command_count >= 3:
        automation = bool_score(1, "The workflow shows some reuse potential.")
    else:
        automation = bool_score(0, "No strong standardization signal appears in this turn.")

    return {
        "task_focus": task_focus,
        "verification": verification,
        "efficiency": efficiency,
        "recovery": recovery,
        "completion_discipline": completion,
        "automation_potential": automation,
    }


def make_finding(code: str, mapping: Dict[str, Any], evidence: str, target: Optional[str] = None) -> Dict[str, Any]:
    return {
        "code": code,
        "severity": mapping["priority"],
        "title": mapping["title"],
        "evidence": evidence,
        "impact": mapping["impact"],
        "suggested_action": mapping["suggested_action"],
        "target": target or mapping["target"],
        "confidence": mapping["confidence"],
        "_action_type": mapping["action_type"],
    }


def evaluate_findings(
    turn_type: str,
    commands: List[Dict[str, Any]],
    scores: Dict[str, Dict[str, Any]],
    action_map: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    validations = [entry for entry in commands if entry["is_validation"]]
    failed_validations = [entry for entry in validations if entry["status"] == "error"]
    repeated_failed = failed_repeated_commands(commands)
    repeated_all = repeated_commands(commands)
    command_count = len(commands)
    categories = sorted({entry["category"] for entry in commands})
    last_validation_success = bool(validations and validations[-1]["status"] == "success")

    if turn_type in HIGH_RISK_TURN_TYPES and not validations:
        findings.append(
            make_finding(
                "validation_missing_high_risk",
                action_map["validation_missing_high_risk"],
                f"Turn type `{turn_type}` had {command_count} commands and 0 validation commands.",
            )
        )

    if failed_validations and not last_validation_success:
        findings.append(
            make_finding(
                "failed_validation_at_stop",
                action_map["failed_validation_at_stop"],
                f"{len(failed_validations)} validation command(s) failed and no later successful validation was observed.",
            )
        )

    max_repeated_failed = max(repeated_failed.values(), default=0)
    if max_repeated_failed >= 3:
        repeated_command = max(repeated_failed, key=repeated_failed.get)
        findings.append(
            make_finding(
                "repeated_failed_command",
                action_map["repeated_failed_command"],
                f"Normalized command `{repeated_command}` failed {max_repeated_failed} times in the same turn.",
            )
        )

    if command_count >= 10 or len(categories) >= 5:
        findings.append(
            make_finding(
                "low_focus_command_sprawl",
                action_map["low_focus_command_sprawl"],
                f"The turn used {command_count} commands across categories {categories}.",
            )
        )

    if failed_validations and not last_validation_success and max_repeated_failed < 3:
        findings.append(
            make_finding(
                "weak_recovery_after_failure",
                action_map["weak_recovery_after_failure"],
                "Failures were visible, but the turn did not show a successful re-check or strong pivot.",
            )
        )

    automation_score = scores["automation_potential"]["score"]
    if automation_score == 2 and (len(repeated_all) >= 1 or len(validations) >= 2 or command_count >= 5):
        findings.append(
            make_finding(
                "automation_candidate_repeated_workflow",
                action_map["automation_candidate_repeated_workflow"],
                f"The turn repeated validation or command steps enough to suggest standardization. Repeated commands: {sorted(repeated_all)}.",
            )
        )

    for finding in findings:
        finding.pop("_action_type", None)

    findings.sort(key=lambda item: (PRIORITY_ORDER[item["severity"]], -item["confidence"], item["code"]))
    return findings


def collect_evidence(turn_events: List[Dict[str, Any]], commands: List[Dict[str, Any]], prompt: Optional[str]) -> Dict[str, Any]:
    repeated_all = repeated_commands(commands)
    transcript_paths = sorted(
        {
            event.get("codex", {}).get("transcript_path")
            for event in turn_events
            if event.get("codex", {}).get("transcript_path")
        }
    )
    artifact_paths = [event.get("artifact_path") for event in turn_events if event.get("artifact_path")]
    stop_preview = None
    for event in turn_events:
        if event.get("event") == "stop":
            stop_preview = event.get("event_data", {}).get("assistant_preview")
            break

    return {
        "prompt_preview": prompt,
        "command_count": len(commands),
        "validation_count": sum(1 for entry in commands if entry["is_validation"]),
        "failed_command_count": sum(1 for entry in commands if entry["status"] == "error"),
        "command_categories": sorted({entry["category"] for entry in commands}),
        "repeated_commands": sorted(repeated_all),
        "final_message_preview": stop_preview,
        "artifact_paths": artifact_paths[:10],
        "transcript_paths": transcript_paths[:5],
    }


def latest_turn_timestamp(turn_events: List[Dict[str, Any]]) -> Optional[str]:
    timestamps = [event.get("recorded_at") for event in turn_events if event.get("recorded_at")]
    return max(timestamps) if timestamps else None


def recency_weight_for_days(age_days: Optional[int]) -> float:
    if age_days is None:
        return RECENCY_WEIGHT_POLICY["31_90_days"]
    if age_days <= 7:
        return RECENCY_WEIGHT_POLICY["0_7_days"]
    if age_days <= 30:
        return RECENCY_WEIGHT_POLICY["8_30_days"]
    if age_days <= 90:
        return RECENCY_WEIGHT_POLICY["31_90_days"]
    return RECENCY_WEIGHT_POLICY["91_plus_days"]


def turn_recency_profile(turn_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    latest_recorded_at = latest_turn_timestamp(turn_events)
    latest_dt = parse_recorded_at(latest_recorded_at)
    age_days = None
    if latest_dt is not None:
        age_days = max(0, (datetime.now().astimezone().date() - latest_dt.date()).days)
    return {
        "latest_recorded_at": latest_recorded_at,
        "age_days": age_days,
        "recency_weight": recency_weight_for_days(age_days),
    }


def resolve_turn_feedback_context(turn_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    contexts = [normalize_feedback_context(event.get("feedback")) for event in turn_events]
    active_contexts = [
        context
        for context in contexts
        if context["is_feedback_run"] or context.get("cycle_id") or context.get("proposal_id")
    ]
    if active_contexts:
        return active_contexts[-1]
    if contexts:
        return contexts[-1]
    return normalize_feedback_context(None)


def overall_quality(scores: Dict[str, Dict[str, Any]]) -> int:
    quality_keys = [
        "task_focus",
        "verification",
        "efficiency",
        "recovery",
        "completion_discipline",
    ]
    total = sum(scores[key]["score"] for key in quality_keys)
    return int(round((total / (len(quality_keys) * 2)) * 100))


def evaluate_turn(
    session_id: str,
    turn_id: str,
    turn_events: List[Dict[str, Any]],
    action_map: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    prompt = extract_prompt(turn_events)
    commands = command_entries(turn_events)
    turn_type = classify_turn(prompt, commands)
    has_stop = any(event.get("event") == "stop" for event in turn_events)
    scores = evaluate_scores(turn_type, commands, has_stop)
    findings = evaluate_findings(turn_type, commands, scores, action_map)
    recency = turn_recency_profile(turn_events)

    return {
        "session_id": session_id,
        "turn_id": turn_id,
        "turn_type": turn_type,
        "feedback_context": resolve_turn_feedback_context(turn_events),
        "latest_recorded_at": recency["latest_recorded_at"],
        "age_days": recency["age_days"],
        "recency_weight": recency["recency_weight"],
        "overall_quality_score": overall_quality(scores),
        "scores": scores,
        "evidence": collect_evidence(turn_events, commands, prompt),
        "findings": findings,
    }


def aggregate_backlog(turn_evaluations: List[Dict[str, Any]], action_map: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for turn in turn_evaluations:
        turn_key = f"{turn['session_id']}:{turn['turn_id']}"
        for finding in turn["findings"]:
            code = finding["code"]
            target = finding["target"]
            mapping = action_map[code]
            key = (code, target)
            if key not in grouped:
                grouped[key] = {
                    "code": code,
                    "severity": mapping["priority"],
                    "target": target,
                    "action_type": mapping["action_type"],
                    "suggested_action": mapping["suggested_action"],
                    "occurrences": 0,
                    "weighted_occurrences": 0.0,
                    "confidence_values": [],
                    "example_turns": [],
                    "latest_seen_at": None,
                }
            grouped[key]["occurrences"] += 1
            grouped[key]["weighted_occurrences"] += turn.get("recency_weight", 0.0)
            grouped[key]["confidence_values"].append(finding["confidence"])
            turn_latest = turn.get("latest_recorded_at")
            if turn_latest and (not grouped[key]["latest_seen_at"] or turn_latest > grouped[key]["latest_seen_at"]):
                grouped[key]["latest_seen_at"] = turn_latest
            if len(grouped[key]["example_turns"]) < 3:
                grouped[key]["example_turns"].append(turn_key)

    backlog = []
    for item in grouped.values():
        backlog.append(
            {
                "code": item["code"],
                "severity": item["severity"],
                "target": item["target"],
                "action_type": item["action_type"],
                "suggested_action": item["suggested_action"],
                "occurrences": item["occurrences"],
                "weighted_occurrences": round(item["weighted_occurrences"], 2),
                "confidence": round(sum(item["confidence_values"]) / len(item["confidence_values"]), 2),
                "example_turns": item["example_turns"],
                "latest_seen_at": item["latest_seen_at"],
            }
        )

    backlog.sort(
        key=lambda item: (
            PRIORITY_ORDER[item["severity"]],
            -item["weighted_occurrences"],
            -item["occurrences"],
            -item["confidence"],
            item["code"],
        )
    )
    return backlog


def build_summary(events: List[Dict[str, Any]], turn_evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    finding_counter = Counter()
    severity_counter = Counter({"P1": 0, "P2": 0, "P3": 0})
    turn_type_counter = Counter(turn["turn_type"] for turn in turn_evaluations)
    feedback_run_kind_counter = Counter(
        turn["feedback_context"]["run_kind"]
        for turn in turn_evaluations
        if turn["feedback_context"]["is_feedback_run"]
    )
    feedback_origin_counter = Counter(
        turn["feedback_context"]["origin"]
        for turn in turn_evaluations
        if turn["feedback_context"]["is_feedback_run"]
    )
    sessions = {turn["session_id"] for turn in turn_evaluations}

    for turn in turn_evaluations:
        for finding in turn["findings"]:
            finding_counter[finding["code"]] += 1
            severity_counter[finding["severity"]] += 1

    top_finding_codes = [
        {"code": code, "count": count}
        for code, count in finding_counter.most_common(5)
    ]

    return {
        "sessions": len(sessions),
        "turns": len(turn_evaluations),
        "high_risk_turns": sum(1 for turn in turn_evaluations if turn["turn_type"] in HIGH_RISK_TURN_TYPES),
        "feedback_turns": sum(1 for turn in turn_evaluations if turn["feedback_context"]["is_feedback_run"]),
        "baseline_turns": sum(1 for turn in turn_evaluations if not turn["feedback_context"]["is_feedback_run"]),
        "feedback_run_kinds": dict(sorted(feedback_run_kind_counter.items())),
        "feedback_origins": dict(sorted(feedback_origin_counter.items())),
        "turn_types": dict(sorted(turn_type_counter.items())),
        "recency_weighting": dict(RECENCY_WEIGHT_POLICY),
        "findings_by_severity": {
            "P1": severity_counter["P1"],
            "P2": severity_counter["P2"],
            "P3": severity_counter["P3"],
        },
        "top_finding_codes": top_finding_codes,
    }


def build_report(args: argparse.Namespace) -> Dict[str, Any]:
    events_dir = Path(args.events_dir).expanduser()
    all_history = bool(getattr(args, "all_history", False))
    files = list_event_files(events_dir, args.date, args.days, all_history)
    events = load_events(files, args)
    turns = group_turns(events)
    action_map = load_action_map()

    turn_evaluations = [
        evaluate_turn(session_id, turn_id, turn_events, action_map)
        for (session_id, turn_id), turn_events in sorted(turns.items())
    ]
    turn_evaluations.sort(key=lambda item: (item["overall_quality_score"], item["session_id"], item["turn_id"]))

    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "window": {
            "mode": "date" if args.date else ("all_history" if all_history else "days"),
            "days": None if (args.date or all_history) else args.days,
            "date": args.date,
            "session_id": args.session_id,
            "events_dir": str(events_dir),
            "files": [str(path) for path in files if path.exists()],
            "recency_weighting": dict(RECENCY_WEIGHT_POLICY),
            "feedback_filters": {
                "exclude_feedback_runs": args.exclude_feedback_runs,
                "feedback_origin": args.feedback_origin,
                "feedback_run_kind": args.feedback_run_kind,
                "feedback_cycle_id": args.feedback_cycle_id,
            },
        },
        "limitations": [
            "Current Codex hook interception is effectively Bash-focused, so command behavior is better observed than direct edit quality.",
            "A high score does not prove code correctness; it only reflects observed workflow quality.",
            "For edit-aware judgment, inspect raw artifacts and transcript paths before escalating confidence.",
        ],
        "summary": build_summary(events, turn_evaluations),
        "improvement_backlog": aggregate_backlog(turn_evaluations, action_map),
        "turn_evaluations": turn_evaluations,
    }
    return report


def format_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    summary = report["summary"]
    backlog = report["improvement_backlog"]

    lines.append("# Feedback Loop Evaluation")
    lines.append("")
    lines.append(f"- Generated: `{report['generated_at']}`")
    lines.append(f"- Turns: `{summary['turns']}` across `{summary['sessions']}` session(s)")
    lines.append(f"- High-risk turns: `{summary['high_risk_turns']}`")
    lines.append(f"- Baseline turns: `{summary['baseline_turns']}`  Feedback-tagged turns: `{summary['feedback_turns']}`")
    lines.append(f"- Window mode: `{report['window']['mode']}`")
    lines.append(
        f"- Findings: `P1={summary['findings_by_severity']['P1']}`, `P2={summary['findings_by_severity']['P2']}`, `P3={summary['findings_by_severity']['P3']}`"
    )
    if summary["turn_types"]:
        lines.append(
            "- Turn types: "
            + ", ".join(f"`{key}={value}`" for key, value in summary["turn_types"].items())
        )
    if summary["feedback_run_kinds"]:
        lines.append(
            "- Feedback run kinds: "
            + ", ".join(f"`{key}={value}`" for key, value in summary["feedback_run_kinds"].items())
        )
    if summary["feedback_origins"]:
        lines.append(
            "- Feedback origins: "
            + ", ".join(f"`{key}={value}`" for key, value in summary["feedback_origins"].items())
        )

    feedback_filters = report["window"].get("feedback_filters", {})
    active_filters = [
        f"{key}={value}"
        for key, value in feedback_filters.items()
        if value not in (None, False, "")
    ]
    if active_filters:
        lines.append("- Active feedback filters: " + ", ".join(f"`{value}`" for value in active_filters))

    lines.append("")
    lines.append("## Top Backlog")
    if backlog:
        for item in backlog[:5]:
            examples = ", ".join(f"`{value}`" for value in item["example_turns"])
            lines.append(
                f"- `{item['severity']}` `{item['code']}` -> `{item['target']}`: {item['suggested_action']} "
                f"(weighted: `{item['weighted_occurrences']}`, occurrences: `{item['occurrences']}`, confidence: `{item['confidence']}`, examples: {examples})"
            )
    else:
        lines.append("- No backlog items were produced for the selected window.")

    lines.append("")
    lines.append("## Lowest-Scoring Turns")
    if report["turn_evaluations"]:
        for turn in report["turn_evaluations"][:5]:
            evidence = turn["evidence"]
            lines.append(
                f"- `{turn['session_id']}:{turn['turn_id']}` `{turn['turn_type']}` quality=`{turn['overall_quality_score']}` "
                f"commands=`{evidence['command_count']}` validations=`{evidence['validation_count']}` "
                f"failed=`{evidence['failed_command_count']}` feedback=`{turn['feedback_context']['run_kind']}` "
                f"age_days=`{turn['age_days'] if turn['age_days'] is not None else 'n/a'}` weight=`{turn['recency_weight']}` "
                f"prompt=`{evidence['prompt_preview'] or 'n/a'}`"
            )
            for finding in turn["findings"][:3]:
                lines.append(
                    f"  - `{finding['severity']}` `{finding['code']}`: {finding['evidence']}"
                )
    else:
        lines.append("- No turns were available in the selected window.")

    lines.append("")
    lines.append("## Limitations")
    for limitation in report["limitations"]:
        lines.append(f"- {limitation}")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    report = build_report(args)

    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(format_markdown(report))
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
