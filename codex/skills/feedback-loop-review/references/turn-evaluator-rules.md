# Turn Evaluator Rules

## Goal

Turn recent Codex hook logs into operational improvement signals. The evaluator is meant to answer:

- Where does the workflow repeatedly lose quality?
- Which failures should become better skills, hooks, agents, prompts, scripts, or checklists?
- Which turns should be treated as high-risk even if the raw output looked acceptable?

The evaluator optimizes for repeatable process quality, not subjective code quality.

## Observed Inputs

The current hook set observes:

- `SessionStart`
- `UserPromptSubmit`
- `PreToolUse`
- `PostToolUse`
- `Stop`
- synthetic `validation_notification` events

The current Codex hook runtime is effectively Bash-focused for tool interception, so the evaluator sees command behavior clearly but does not directly see every edit. Use `artifact_path` and `transcript_path` for deeper review when edit-aware judgment is required.

## Turn Segmentation

Evaluate one turn at a time using:

- `session_id`
- `turn_id`

Events without `turn_id` are session-level context and are not scored as turns.

## Turn Type Classifier

Classify each scored turn before applying weights.

### `analysis`

Use when:

- prompt asks to inspect, summarize, orient, investigate, or compare
- command volume is minimal
- validation is not central to the task

### `implementation`

Default for build-oriented work when:

- commands are present
- the prompt does not strongly match another type
- the turn appears to move toward a concrete change

### `bugfix`

Use when the prompt or command flow strongly suggests error correction:

- `fix`, `bug`, `error`, `broken`, `깨짐`, `실패`, `안 됨`

### `refactor`

Use when the prompt emphasizes code cleanup or structural change:

- `refactor`, `rename`, `cleanup`, `정리`, `구조 변경`

### `docs`

Use when the prompt emphasizes documentation:

- `docs`, `documentation`, `readme`, `spec`, `proposal`, `문서`

### `ops`

Use when commands or prompt emphasize deployment or environment operations:

- `deploy`, `kubectl`, `docker`, `terraform`, `az`, `gh pr`, `git push`

### `review`

Use when the prompt emphasizes review or audit:

- `review`, `audit`, `리뷰`, `점검`

## High-Risk Turn Types

Treat these as verification-sensitive:

- `implementation`
- `bugfix`
- `refactor`
- `ops`

For these types, missing or failed validation is a stronger signal.

## Scoring Dimensions

All dimensions score `0-2`.

### `task_focus`

- `2`: Command flow stays narrow and relevant. Few categories, low sprawl, no obvious wandering.
- `1`: Some detours or mild over-exploration, but still converges.
- `0`: High command sprawl, many unrelated categories, or obvious wandering.

### `verification`

- `2`: Verification level matches turn risk; high-risk turns end with successful validation.
- `1`: Some validation exists but is weak, partial, or unresolved.
- `0`: High-risk turn has no validation, or validation fails without recovery.

### `efficiency`

- `2`: Few commands, low repetition, good convergence.
- `1`: Some repeated attempts or mildly inflated command count.
- `0`: Same or similar failures repeat, or command volume becomes excessive.

### `recovery`

- `2`: Failures are followed by a clear pivot or a successful re-check.
- `1`: Partial recovery exists but remains inconclusive.
- `0`: Failure loops continue without a meaningful strategy change.

### `completion_discipline`

- `2`: Turn stops at a sensible point. High-risk work ends after successful validation.
- `1`: Stop point is arguable but not clearly unsafe.
- `0`: Turn stops after failed validation, or stops without expected verification.

### `automation_potential`

This is an opportunity score, not a quality score.

- `2`: Strong candidate for a script, skill, checklist, or hook.
- `1`: Some reuse potential exists.
- `0`: No obvious standardization gain.

## Quality Score

`overall_quality_score` is computed from:

- `task_focus`
- `verification`
- `efficiency`
- `recovery`
- `completion_discipline`

It excludes `automation_potential`.

## Primary Finding Rules

### `validation_missing_high_risk`

Trigger when:

- turn type is high-risk
- validation count is `0`

### `failed_validation_at_stop`

Trigger when:

- at least one validation command fails
- no later successful validation appears before stop

### `repeated_failed_command`

Trigger when:

- the same normalized command fails at least `3` times in one turn

### `low_focus_command_sprawl`

Trigger when either:

- command count is high for the turn type
- unique command categories exceed a narrow working set

### `weak_recovery_after_failure`

Trigger when:

- failures exist
- there is no convincing pivot or successful re-check
- repeated failure is present but below the stronger `repeated_failed_command` threshold

### `automation_candidate_repeated_workflow`

Trigger when:

- the workflow is repetitive enough that a script, command, checklist, or skill would reduce future friction

## Backlog Generation

Aggregate findings across turns by:

- finding code
- target
- action type

Sort backlog priority by:

1. severity
2. recurrence count
3. confidence

## Interpretation Constraints

- Do not equate low command count with high quality.
- Do not equate many tests with high quality.
- Do not claim code correctness from hook logs alone.
- Separate direct evidence from inference.
- If a recommendation depends on edit quality, inspect raw artifacts or transcript paths before escalating confidence.
