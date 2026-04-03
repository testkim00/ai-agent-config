---
name: git-monthly-report
description: Draft monthly achievement reports from activity across one or more Git repositories. Use when the user wants a monthly report, asks for 실적 only, provides topic lists or outline bullets, wants to select multiple repositories, or needs Git changes from a date range summarized into a report draft.
---

# Git Monthly Report

## Overview

Use this skill to turn recent Git activity from multiple repositories into a concise monthly achievements report. The skill is strongest when the user already has reporting topics, but it can also derive provisional topics from Git activity when needed.

## Workflow

### 1. Lock The Reporting Inputs

- Resolve the reporting period to exact dates before collecting Git activity.
- If the user says `지난달`, `이번달`, or `최근 한달`, restate the resolved dates explicitly.
- Collect the topic list first when possible.
- If the user does not give topics, derive provisional topics from repository names, hot paths, and representative commit clusters after activity collection.

### 2. Show Repository Candidates

If the user did not already specify repositories, list candidate repositories first:

```bash
python3 scripts/list_git_repos.py /path/to/search-root --max-depth 4
```

- Use the user's workspace root when they specify it.
- Otherwise start from the most relevant parent directory, not the entire home directory.
- Present the indexed list and let the user choose multiple repositories.

### 3. Collect Git Activity

After repository selection, collect activity for the exact date range:

```bash
python3 scripts/collect_git_activity.py \
  --since 2026-03-01 \
  --until 2026-03-31 \
  /path/to/repo-a /path/to/repo-b
```

- Use JSON output by default so the result can be analyzed programmatically.
- Exclude merge-only noise unless the user explicitly wants release-level history.
- If a repository is very noisy, lower `--max-commits` and rely more on top areas and representative commits.

### 4. Resolve Output Location

- If the user wants the draft saved to disk and does not specify a path, default to `~/Workspace/Works/실적보고`.
- If `~/Workspace/Works/실적보고` does not exist, fall back to `~/Workspace/Works`.
- If neither directory exists, ask the user where to save or keep the result in chat only.
- Prefer a predictable file name such as `2026-03_실적보고.md`.

## Drafting Rules

- Read [references/monthly-report-template.md](references/monthly-report-template.md) before writing the report.
- Group the report by the user's topics, not by repository.
- Merge related changes across repositories into one topic-level summary.
- Turn low-level commit messages into work-level statements. Do not paste raw commit subjects unless they are already report-ready.
- Keep `실적` evidence-backed. Prefer work completed, fixes shipped, flows stabilized, screens added, APIs integrated, or refactors with visible impact.
- If topic mapping is ambiguous, show the best draft and call out the uncertain topic assignment instead of pretending certainty.

## Output Expectations

- Always show the exact reporting period in the final draft.
- Keep the final report compact and readable in Korean unless the user asks otherwise.
- Prefer 1-3 flat bullets per topic rather than long narrative paragraphs.
- If the user did not provide topics, draft provisional topic names from Git activity and let the user rename or merge them afterward.
- When saving a draft without an explicit user path, use the default output location rule above.

## Resources

- `scripts/list_git_repos.py`: discover repositories for multi-select
- `scripts/collect_git_activity.py`: extract structured Git activity for a date range
- `references/monthly-report-template.md`: report structure, mapping rules, and example wording
