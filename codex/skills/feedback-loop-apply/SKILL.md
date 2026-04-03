---
name: feedback-loop-apply
description: Apply the safest feedback-loop improvements by selecting one auto-applyable proposal, tagging the run with feedback metadata, patching only local Codex config or skill files, then rechecking and clearing the tag. Use when the user wants the feedback loop to go beyond diagnosis and actually reflect the top improvement candidate.
---

# Feedback Loop Apply

## Overview

Use this skill after [$feedback-loop-review](/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/SKILL.md) has already shown repeated patterns and proposal candidates.

If the user wants one top-level entry point that already includes review plus apply planning, use [$feedback-loop](/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/SKILL.md) first.

The goal is to complete one closed loop safely:

1. select the top auto-applyable proposal
2. tag the run so the new logs are distinguishable from baseline behavior
3. patch only safe local files
4. run a targeted recheck
5. clear the feedback tag

Do not auto-apply changes to normal product repositories with this skill. The safe scope is limited to:

- `~/.codex/...`
- `/Users/honeychaser/Projects/ai-agent-config/codex/...`

## Workflow

### 1. Build Or Load A Proposal Report

Run:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/scripts/apply_feedback_improvements.py --days 7 --format markdown`

If the user already has a saved proposal report, pass `--proposal-report /path/to/report.json`.

### 2. Activate Feedback Context

When you are about to patch files, activate the context so the hook logs mark this run as a feedback-application cycle:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/scripts/apply_feedback_improvements.py --days 7 --activate-context --format markdown`

This writes `~/.codex/logs/feedback-loop/state/feedback-context.json`.

The hooks will then attach `feedback.origin`, `feedback.run_kind`, `feedback.cycle_id`, and `feedback.proposal_id` to new events.

### 3. Patch Only Safe Candidate Paths

Follow the selected proposal's `safe_candidate_paths`.

- Keep the patch minimal.
- Prefer the first safe candidate unless the evidence clearly points elsewhere.
- Preserve existing logging and validation behavior unless the proposal explicitly changes that behavior.

### 4. Switch To Recheck Phase

Before running validation, change the active feedback context from apply to recheck:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/scripts/feedback_context.py update --run-kind feedback_recheck`

This keeps the logs separated inside the same cycle.

### 5. Run A Targeted Validation

Choose the smallest validation that proves the patch works.

Examples:

- Python changes: `python3 -m py_compile ...`
- JSON changes: `python3 -m json.tool ...`
- hook logic changes: run one synthetic payload through the affected hook path

### 6. Clear The Context

After validation, clear the feedback tag:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/scripts/feedback_context.py stop`

Do not leave the feedback context active after the task.

## Output Expectations

When you report back:

1. mention which proposal was selected
2. mention which files were patched
3. state the validation result
4. state whether the feedback context was activated and cleared

If no safe proposal exists, stop and report that the remaining candidates are manual-only.
