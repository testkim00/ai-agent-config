---
name: feedback-loop-review
description: Review Codex feedback-loop hook logs in `~/.codex/logs/feedback-loop`, score recent turns, detect repeated failure patterns, and convert them into concrete improvements for skills, hooks, agents, prompts, scripts, and checklists. Use when the user asks to analyze Codex usage quality, inspect 반복 실수, build or tune a feedback loop, summarize recent work patterns, or identify what should be standardized next.
---

# Feedback Loop Review

## Overview

Use this skill to turn Codex hook logs into an improvement backlog. Prefer evidence-backed findings over abstract quality judgments. The goal is not to say whether the agent was "good" or "bad"; it is to identify repeated behaviors that should become better skills, stronger hooks, tighter prompts, or reusable commands.

If the user wants one top-level entry point instead of separate review/apply stages, use [$feedback-loop](/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/SKILL.md) first.

## Quick Start

1. Run the analyzer for the requested window.
   `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/scripts/analyze_feedback_loop.py --days 7 --format markdown`
2. If the user wants raw structured output, use:
   `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/scripts/analyze_feedback_loop.py --days 7 --format json`
3. If the user wants a full-history audit instead of a recent window:
   `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/scripts/analyze_feedback_loop.py --all-history --format markdown`
4. Turn the backlog into patch candidates:
   `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/scripts/propose_feedback_improvements.py --days 7 --format markdown`
5. If a high-risk finding looks ambiguous, inspect the raw artifact paths and transcript paths referenced in the report before recommending changes.
6. If the user wants an actual safe application pass, hand off to [$feedback-loop-apply](/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/SKILL.md).

## Workflow

### 1. Choose The Evaluation Window

- Default to the last 7 days when the user does not specify a window.
- Treat this as the main decision surface for actual feedback-loop changes.
- Narrow by `--session-id` when the user wants to inspect one thread or one experiment.
- Use `--date YYYY-MM-DD` for a single-day audit.
- Use `--all-history` only for long-term pattern analysis or periodic audits.

### 2. Read The Rules Only Once

Before interpreting scores, read:

- [references/turn-evaluator-rules.md](references/turn-evaluator-rules.md)
- [references/findings-action-map.json](references/findings-action-map.json)

Use the rules document to explain why a finding exists. Use the action map to turn repeated findings into concrete next steps.

### 3. Generate The Baseline Report

Run the analyzer first and let it produce:

- turn classification
- rubric scores
- findings with severity and confidence
- aggregated improvement backlog

Do not manually rebuild these counts from raw JSONL unless the script output is clearly inconsistent.

### 4. Escalate Only When Needed

The current hook set observes `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, and validation notifications, but current Codex hook runtime is effectively Bash-focused.

That means:

- command behavior is well observed
- validation discipline is reasonably observed
- direct edit quality is only partially observed

If a recommendation depends on edit quality, inspect:

- raw hook artifacts under `~/.codex/logs/feedback-loop/artifacts/`
- the `transcript_path` values surfaced in the report

### 5. Convert Findings Into Improvements

Always turn findings into one of these targets:

- `skill`
- `hook`
- `agent`
- `prompt`
- `script`
- `checklist`
- `docs`

Prefer the smallest change that prevents recurrence.

Examples:

- repeated missing validation -> strengthen the relevant implementation or bugfix skill
- repeated long manual validation sequences -> extract a reusable command or script
- repeated failed command loops -> teach a pivot rule in the relevant skill or agent guidance
- repeated stop-after-failure behavior -> add a stronger stop-stage reminder or hook

### 6. Generate Patch Candidates

When the user wants the next step beyond diagnosis, run:

- [scripts/propose_feedback_improvements.py](scripts/propose_feedback_improvements.py)

This script converts the improvement backlog into concrete patch candidates with:

- likely files to edit
- implementation notes
- an `apply_prompt` string another Codex run can use directly

Treat those proposals as implementation candidates, not guaranteed truth. Confirm the top 1-3 proposals against the evidence before editing.

## Output Expectations

When reporting back, structure the response in three parts:

1. `Signals`
   Mention the strongest observed patterns, with counts and confidence.
2. `Improvement Backlog`
   List the highest-value changes to skills, hooks, agents, prompts, scripts, or checklists.
3. `Next Changes`
   Recommend the next 1-3 concrete edits to make first.

Keep a strict line between:

- direct evidence from logs
- inference from patterns
- recommendations for change

## References

- Rubric schema: [references/evaluation-rubric.schema.json](references/evaluation-rubric.schema.json)
- Evaluator rules: [references/turn-evaluator-rules.md](references/turn-evaluator-rules.md)
- Action map: [references/findings-action-map.json](references/findings-action-map.json)
- Proposal schema: [references/improvement-proposal.schema.json](references/improvement-proposal.schema.json)
- Proposal playbook: [references/proposal-playbook.json](references/proposal-playbook.json)
