#!/usr/bin/env python3

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analyze_feedback_loop as analyzer  # noqa: E402


SCHEMA_VERSION = "feedback-loop-proposals/v1"
PLAYBOOK_PATH = SCRIPT_DIR.parent / "references" / "proposal-playbook.json"
DEFAULT_SKILLS_ROOT = Path("/Users/honeychaser/Projects/ai-agent-config/codex/skills")
DEFAULT_PROPOSALS_DIR = Path.home() / ".codex" / "logs" / "feedback-loop" / "proposals"
SAFE_AUTO_APPLY_ROOTS = [
    Path.home() / ".codex",
    Path("/Users/honeychaser/Projects/ai-agent-config/codex"),
]

TARGET_ORDER = {"hook": 0, "skill": 1, "agent": 2, "prompt": 3, "script": 4, "checklist": 5, "docs": 6}
STOPWORD_TOKENS = {
    "a",
    "an",
    "and",
    "bug",
    "error",
    "failed",
    "failing",
    "fix",
    "for",
    "in",
    "issue",
    "of",
    "on",
    "task",
    "test",
    "tests",
    "the",
    "to",
    "with",
}
TURN_TYPE_SKILL_BOOSTS = {
    "analysis": ["project-orient", "codex"],
    "implementation": ["codex", "git-workflow"],
    "bugfix": ["codex", "git-workflow"],
    "refactor": ["codex", "git-workflow"],
    "docs": ["tidy-md", "project-orient"],
    "ops": ["git-workflow", "git-push", "git-pr", "az-app", "az-swa", "az-db"],
    "review": ["codex", "consult"],
}


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Turn feedback-loop findings into patch candidates.")
    parser.add_argument("--report", help="Existing analyzer JSON report path.")
    parser.add_argument("--events-dir", default=str(analyzer.DEFAULT_EVENTS_DIR))
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--date")
    parser.add_argument("--all-history", action="store_true")
    parser.add_argument("--session-id")
    parser.add_argument("--feedback-origin")
    parser.add_argument("--feedback-run-kind")
    parser.add_argument("--feedback-cycle-id")
    parser.add_argument("--exclude-feedback-runs", action="store_true")
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of proposal items to emit.")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--save", action="store_true", help="Write a JSON proposal artifact under ~/.codex/logs/feedback-loop/proposals.")
    return parser.parse_args()


def load_playbook() -> Dict[str, Dict[str, Any]]:
    return json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8"))


def build_report_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    if args.report:
        return json.loads(Path(args.report).expanduser().read_text(encoding="utf-8"))

    namespace = SimpleNamespace(
        events_dir=args.events_dir,
        days=args.days,
        date=args.date,
        all_history=getattr(args, "all_history", False),
        session_id=args.session_id,
        feedback_origin=getattr(args, "feedback_origin", None),
        feedback_run_kind=getattr(args, "feedback_run_kind", None),
        feedback_cycle_id=getattr(args, "feedback_cycle_id", None),
        exclude_feedback_runs=getattr(args, "exclude_feedback_runs", False),
        format="json",
    )
    return analyzer.build_report(namespace)


def expand_path(path: str) -> str:
    return str(Path(path).expanduser())


def normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip().lower()


def tokenize(value: str) -> List[str]:
    text = normalize_text(value)
    return [
        token
        for token in re.split(r"[^a-z0-9가-힣_-]+", text)
        if len(token) >= 2 and token not in STOPWORD_TOKENS
    ]


def slugify(value: str) -> str:
    tokens = tokenize(value)[:5]
    normalized = "-".join(tokens) if tokens else normalize_text(value)
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return slug or "workflow"


def load_skill_index(skills_root: Path) -> List[Dict[str, str]]:
    skills: List[Dict[str, str]] = []
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
        name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        name = (name_match.group(1).strip() if name_match else skill_md.parent.name).strip('"')
        description = (desc_match.group(1).strip() if desc_match else "").strip('"')
        skills.append(
            {
                "name": name,
                "description": description,
                "skill_dir": str(skill_md.parent),
                "skill_md": str(skill_md),
            }
        )
    return skills


def build_turn_lookup(report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    lookup: Dict[str, Dict[str, Any]] = {}
    for turn in report.get("turn_evaluations", []):
        lookup[f"{turn['session_id']}:{turn['turn_id']}"] = turn
    return lookup


def query_text_for_turns(turns: Sequence[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for turn in turns:
        evidence = turn.get("evidence", {})
        parts.extend(
            [
                evidence.get("prompt_preview") or "",
                " ".join(evidence.get("command_categories") or []),
                " ".join(evidence.get("repeated_commands") or []),
                turn.get("turn_type") or "",
            ]
        )
    return " ".join(part for part in parts if part)


def score_skill_candidates(
    skills: Sequence[Dict[str, str]],
    query_text: str,
    turn_types: Sequence[str],
    target: str,
) -> List[Dict[str, str]]:
    query_norm = normalize_text(query_text)
    query_tokens = set(tokenize(query_text))
    boosted_names = set()
    for turn_type in turn_types:
        boosted_names.update(TURN_TYPE_SKILL_BOOSTS.get(turn_type, []))

    scored: List[Dict[str, Any]] = []
    for skill in skills:
        combined = normalize_text(f"{skill['name']} {skill['description']}")
        score = 0
        reasons: List[str] = []

        if skill["name"] in query_norm:
            score += 5
            reasons.append("skill name appears directly in the observed query")

        overlap = sorted(token for token in query_tokens if token in combined)
        if overlap:
            score += min(len(overlap), 4)
            reasons.append(f"overlapping query tokens: {', '.join(overlap[:4])}")

        if skill["name"] in boosted_names:
            score += 3
            reasons.append("boosted for this turn type")

        if target in {"agent", "prompt"} and skill["name"] in {"codex", "git-workflow"}:
            score += 2
            reasons.append("broad execution guidance skill")

        if target == "skill" and skill["name"] == "codex":
            score += 1
            reasons.append("safe fallback for general workflow changes")

        if score > 0:
            scored.append(
                {
                    "score": score,
                    "reason": "; ".join(reasons),
                    **skill,
                }
            )

    scored.sort(key=lambda item: (-item["score"], item["name"]))
    if scored:
        return scored[:3]

    fallback_names = ["codex", "git-workflow", "project-orient"]
    fallback = [skill for skill in skills if skill["name"] in fallback_names]
    return [
        {
            "score": 0,
            "reason": "fallback candidate because no stronger match was found",
            **skill,
        }
        for skill in fallback[:3]
    ]


def dedupe_candidate_paths(candidates: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    unique: List[Dict[str, str]] = []
    for candidate in candidates:
        key = (candidate["path"], candidate["mode"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def path_is_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def is_safe_auto_apply_path(path_str: str) -> bool:
    path = Path(path_str).expanduser()
    probe = path if path.exists() else path.parent
    return any(path_is_within_root(probe, root) for root in SAFE_AUTO_APPLY_ROOTS)


def build_auto_apply_summary(candidate_paths: Sequence[Dict[str, str]]) -> Dict[str, Any]:
    safe_candidates: List[Dict[str, str]] = []
    blocked_candidates: List[Dict[str, str]] = []

    for candidate in candidate_paths:
        if is_safe_auto_apply_path(candidate["path"]):
            safe_candidates.append(dict(candidate))
            continue

        blocked = dict(candidate)
        blocked["block_reason"] = "path is outside the configured local auto-apply roots"
        blocked_candidates.append(blocked)

    return {
        "eligible": bool(safe_candidates),
        "scope": "local_config_only" if safe_candidates else "manual_only",
        "safe_roots": [str(root) for root in SAFE_AUTO_APPLY_ROOTS],
        "safe_candidate_paths": safe_candidates,
        "blocked_candidate_paths": blocked_candidates,
    }


def propose_script_paths(query_text: str, matched_skills: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    slug = slugify(query_text)[:40]
    candidates: List[Dict[str, str]] = []
    if matched_skills:
        skill_dir = Path(matched_skills[0]["skill_dir"])
        candidates.append(
            {
                "path": str(skill_dir / "scripts" / f"{slug}.sh"),
                "mode": "create",
                "reason": f"the top matched skill `{matched_skills[0]['name']}` can host a reusable helper script",
            }
        )
    candidates.append(
        {
            "path": expand_path(f"~/.codex/bin/{slug}.sh"),
            "mode": "create",
            "reason": "a user-local utility is a low-friction place to standardize a repeated workflow",
        }
    )
    return candidates


def propose_checklist_paths(query_text: str, matched_skills: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    slug = slugify(query_text)[:40]
    candidates: List[Dict[str, str]] = []
    if matched_skills:
        skill_dir = Path(matched_skills[0]["skill_dir"])
        candidates.append(
            {
                "path": str(skill_dir / "references" / f"{slug}-checklist.md"),
                "mode": "create",
                "reason": f"the top matched skill `{matched_skills[0]['name']}` can reference a reusable checklist",
            }
        )
    candidates.append(
        {
            "path": expand_path(f"~/.codex/checklists/{slug}.md"),
            "mode": "create",
            "reason": "a global checklist is the smallest reusable standardization artifact",
        }
    )
    return candidates


def build_candidate_paths(
    backlog_item: Dict[str, Any],
    playbook_item: Dict[str, Any],
    matched_skills: Sequence[Dict[str, str]],
    query_text: str,
) -> List[Dict[str, str]]:
    target = backlog_item["target"]
    candidates: List[Dict[str, str]] = []

    for candidate in playbook_item.get("default_candidates", {}).get(target, []):
        candidates.append(
            {
                "path": expand_path(candidate["path"]),
                "mode": candidate["mode"],
                "reason": candidate["reason"],
            }
        )

    if target in {"skill", "agent", "prompt", "docs"}:
        for skill in matched_skills:
            candidates.append(
                {
                    "path": skill["skill_md"],
                    "mode": "edit",
                    "reason": skill["reason"],
                }
            )

    if target == "script":
        candidates.extend(propose_script_paths(query_text, matched_skills))

    if target == "checklist":
        candidates.extend(propose_checklist_paths(query_text, matched_skills))

    return dedupe_candidate_paths(candidates)[:5]


def build_evidence_lines(turns: Sequence[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    for turn in turns[:3]:
        evidence = turn.get("evidence", {})
        lines.append(
            f"{turn['session_id']}:{turn['turn_id']} type={turn['turn_type']} quality={turn['overall_quality_score']} "
            f"commands={evidence.get('command_count')} validations={evidence.get('validation_count')} "
            f"failed={evidence.get('failed_command_count')} prompt={evidence.get('prompt_preview') or 'n/a'}"
        )
    return lines


def build_apply_prompt(
    backlog_item: Dict[str, Any],
    playbook_item: Dict[str, Any],
    candidate_paths: Sequence[Dict[str, str]],
    evidence_lines: Sequence[str],
) -> str:
    candidate_text = ", ".join(candidate["path"] for candidate in candidate_paths[:3]) or "the most relevant target files"
    evidence_text = "; ".join(evidence_lines[:2])
    base = playbook_item.get("apply_prompt_template", backlog_item["suggested_action"])
    return (
        f"{base} Candidate paths: {candidate_text}. "
        f"Evidence from the feedback loop: {evidence_text}."
    )


def build_proposals(
    report: Dict[str, Any],
    playbook: Dict[str, Dict[str, Any]],
    skills_index: Sequence[Dict[str, str]],
    limit: int,
) -> List[Dict[str, Any]]:
    turn_lookup = build_turn_lookup(report)
    proposals: List[Dict[str, Any]] = []

    for index, backlog_item in enumerate(report.get("improvement_backlog", [])[: max(limit, 0)], start=1):
        playbook_item = playbook.get(backlog_item["code"], {})
        example_turns = [turn_lookup[key] for key in backlog_item.get("example_turns", []) if key in turn_lookup]
        turn_types = [turn["turn_type"] for turn in example_turns]
        query_text = query_text_for_turns(example_turns)
        matched_skills = score_skill_candidates(skills_index, query_text, turn_types, backlog_item["target"])
        candidate_paths = build_candidate_paths(backlog_item, playbook_item, matched_skills, query_text)
        evidence_lines = build_evidence_lines(example_turns)

        summary = playbook_item.get("summary", backlog_item["suggested_action"])
        implementation_notes = playbook_item.get("implementation_notes", [])
        apply_prompt = build_apply_prompt(backlog_item, playbook_item, candidate_paths, evidence_lines)

        proposals.append(
            {
                "id": f"{backlog_item['severity'].lower()}-{index:02d}-{backlog_item['code']}",
                "severity": backlog_item["severity"],
                "finding_code": backlog_item["code"],
                "target": backlog_item["target"],
                "action_type": backlog_item["action_type"],
                "summary": summary,
                "confidence": backlog_item["confidence"],
                "candidate_paths": candidate_paths,
                "implementation_notes": implementation_notes,
                "evidence": evidence_lines,
                "apply_prompt": apply_prompt,
                "auto_apply": build_auto_apply_summary(candidate_paths),
            }
        )

    proposals.sort(
        key=lambda item: (
            analyzer.PRIORITY_ORDER[item["severity"]],
            TARGET_ORDER.get(item["target"], 99),
            -item["confidence"],
            item["finding_code"],
        )
    )
    return proposals


def build_proposal_report(args: argparse.Namespace) -> Dict[str, Any]:
    report = build_report_from_args(args)
    playbook = load_playbook()
    skills_index = load_skill_index(Path(args.skills_root).expanduser())
    proposals = build_proposals(report, playbook, skills_index, args.limit)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "source_summary": {
            "report_schema_version": report.get("schema_version"),
            "window": report.get("window"),
            "turns": report.get("summary", {}).get("turns", 0),
            "backlog_items": len(report.get("improvement_backlog", [])),
        },
        "proposal_items": proposals,
    }


def format_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Feedback Improvement Proposals")
    lines.append("")
    lines.append(f"- Generated: `{report['generated_at']}`")
    lines.append(f"- Source turns: `{report['source_summary']['turns']}`")
    lines.append(f"- Backlog items seen: `{report['source_summary']['backlog_items']}`")
    lines.append(f"- Proposals emitted: `{len(report['proposal_items'])}`")
    lines.append("")

    if not report["proposal_items"]:
        lines.append("- No proposal items were generated from the selected report window.")
        return "\n".join(lines)

    for proposal in report["proposal_items"]:
        lines.append(f"## {proposal['id']}")
        lines.append("")
        lines.append(
            f"- Severity: `{proposal['severity']}`"
            f"  Target: `{proposal['target']}`"
            f"  Confidence: `{proposal['confidence']}`"
        )
        lines.append(f"- Summary: {proposal['summary']}")
        lines.append(
            f"- Auto-apply: `eligible={str(proposal['auto_apply']['eligible']).lower()}`"
            f"  scope=`{proposal['auto_apply']['scope']}`"
        )
        if proposal["candidate_paths"]:
            lines.append("- Candidate paths:")
            for candidate in proposal["candidate_paths"]:
                lines.append(
                    f"  - `{candidate['mode']}` `{candidate['path']}`: {candidate['reason']}"
                )
        if proposal["auto_apply"]["blocked_candidate_paths"]:
            lines.append("- Blocked auto-apply paths:")
            for candidate in proposal["auto_apply"]["blocked_candidate_paths"]:
                lines.append(
                    f"  - `{candidate['mode']}` `{candidate['path']}`: {candidate['block_reason']}"
                )
        if proposal["implementation_notes"]:
            lines.append("- Implementation notes:")
            for note in proposal["implementation_notes"]:
                lines.append(f"  - {note}")
        if proposal["evidence"]:
            lines.append("- Evidence:")
            for evidence in proposal["evidence"]:
                lines.append(f"  - {evidence}")
        lines.append(f"- Apply prompt: {proposal['apply_prompt']}")
        lines.append("")

    return "\n".join(lines).rstrip()


def save_report(report: Dict[str, Any]) -> Path:
    DEFAULT_PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    report_path = DEFAULT_PROPOSALS_DIR / f"{timestamp}.json"
    latest_path = DEFAULT_PROPOSALS_DIR / "latest.json"
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    report_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return report_path


def main() -> int:
    args = parse_args()
    report = build_proposal_report(args)

    if args.save:
        saved_path = save_report(report)
        print(f"Saved proposal report to {saved_path}", file=sys.stderr)

    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(format_markdown(report))
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
