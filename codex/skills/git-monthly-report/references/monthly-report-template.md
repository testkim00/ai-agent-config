# Monthly Report Template

## Inputs To Lock First

- Reporting period with exact dates
- Selected repositories
- Topic list or reporting outline from the user
- Output path if the user wants a saved file

If the user gives relative dates such as `지난달`, resolve them to exact dates in the response and in any generated draft.

## Default Output Path

- Default save directory: `~/Workspace/Works/실적보고`
- Fallback directory when the default does not exist: `~/Workspace/Works`
- Suggested filename: `YYYY-MM_실적보고.md`

## Drafting Rules

- Group the report by the user's topics, not by repository names.
- Use Git evidence to support `실적`, but rewrite it into work language.
- Deduplicate the same work when it appears in multiple repositories.
- De-emphasize housekeeping-only changes unless they affected delivery, stability, or release readiness.
- Prefer concrete nouns and outcomes: screen, API, batch, auth flow, data sync, validation, bug fix, performance, deployment.

## Suggested Output Shape

```md
# YYYY-MM Monthly Report

Period: 2026-03-01 ~ 2026-03-31

## 실적

### Topic A
- ...
- ...

### Topic B
- ...
```

## Mapping Git Activity To Report Language

Prefer work-level phrasing over raw commit summaries.

Examples:

- Raw Git signal:
  - `feat: add retry logic to settlement batch`
  - `fix: rounding mismatch in invoice summary`
  - touched paths: `services/settlement`, `controllers/invoice`
- Report phrasing:
  - `정산 배치 재처리 로직을 보강하고 청구 요약 금액 계산 오류를 수정해 운영 안정성을 높였습니다.`

- Raw Git signal:
  - `refactor: split auth middleware`
  - `feat: add role guard to admin routes`
- Report phrasing:
  - `인증 미들웨어 구조를 정리하고 관리자 경로 권한 검사를 추가해 접근 제어를 강화했습니다.`

## If Topics Are Missing

- Draft provisional topic names from repo names, hot paths, or repeated commit themes.
- Ask the user to rename or merge those sections into final report topics.

## If Git Evidence Is Weak

- Say that the topic had limited Git-visible changes for the period.
- Avoid inventing completion claims.
- Use cautious language such as `관련 정리 작업 진행`, `기반 작업 수행`, or `안정화 작업 반영`.
