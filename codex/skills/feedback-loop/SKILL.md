---
name: feedback-loop
description: Run the full Codex feedback loop from one entry point by reviewing baseline hook logs, generating improvement proposals, selecting one safe apply plan, and optionally activating a tagged feedback cycle for the next patch. Use when the user wants one top-level skill instead of separately calling feedback-loop-review and feedback-loop-apply.
---

# Feedback Loop

## Overview

This is the top-level entry point for the local feedback-loop system.

It wraps:

- [$feedback-loop-review](/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-review/SKILL.md)
- [$feedback-loop-apply](/Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/SKILL.md)

Use it when the user wants one command surface for:

1. reviewing recent baseline behavior
2. checking long-term historical patterns when needed
3. generating proposals
4. preparing one safe application pass
5. optionally tagging the next patch as a feedback cycle

## Quick Start

Default end-to-end planning pass:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/scripts/run_feedback_loop.py --days 7 --format markdown`

Add a historical audit across the whole event history:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/scripts/run_feedback_loop.py --days 7 --all-history --format markdown`

Prepare the same pass and activate the feedback context for the next patch:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/scripts/run_feedback_loop.py --days 7 --activate-context --format markdown`

Review one tagged feedback cycle after the patch and recheck are done:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/scripts/run_feedback_loop.py --cycle-review feedback-20260403T010000+0900 --format markdown`

## Default Behavior

The wrapper defaults to baseline analysis.

That means:

- feedback-tagged runs are excluded unless you explicitly ask to inspect a cycle
- the default decision window is global recent history, not one thread and not all-time history
- the script produces a recent evaluation report
- the script can optionally add a historical all-files section with `--all-history`
- the script produces proposal candidates from the recent window
- the script produces one safe apply plan for the top eligible proposal

## Workflow

### 1. Run The Wrapper

Start with the wrapper script instead of calling the lower-level scripts directly.

### 2. Read The Three Sections

The wrapper returns these layers:

- `Recent Signals`
- `Historical Signals` when `--all-history` is used
- `Top Proposal`
- `Apply Plan`

Treat the recent signals as the decision surface, the historical signals as long-term context, the proposal as the candidate, and the apply plan as the next move.

### 3. Activate Context Only When You Are About To Patch

Use `--activate-context` only when you are actually about to make the patch.

That writes the active feedback context file so hooks can tag the next events with:

- `feedback.origin`
- `feedback.run_kind`
- `feedback.cycle_id`
- `feedback.proposal_id`

### 4. Patch And Recheck

Follow the selected safe candidate paths.

Before validation, switch the run kind:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/scripts/feedback_context.py update --run-kind feedback_recheck`

After validation, clear the context:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop-apply/scripts/feedback_context.py stop`

### 5. Inspect The Tagged Cycle

Once the apply and recheck pass are done, review the tagged cycle:

`python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/feedback-loop/scripts/run_feedback_loop.py --cycle-review <cycle-id> --format markdown`

## Output Expectations

When reporting back from this skill:

1. summarize the strongest baseline signals
2. name the selected proposal
3. state whether a feedback context was activated
4. give the exact next command or validation step
