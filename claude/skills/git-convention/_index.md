# Git 컨벤션 스킬 인덱스

> **수정 시 필수 확인**
>
> Git 컨벤션 수정 전:
> 1. 이 파일의 관련 문서 목록 확인
> 2. 관련 Git 커맨드들 (`commands/git/`) 확인
> 3. 커밋 메시지/브랜치명 일관성 유지

## 문서 구조

```
skills/git-convention/
├── _index.md       ← 현재 파일
└── SKILL.md        ← Git 컨벤션 정의
```

## 문서 목록

| 파일 | 설명 |
|------|------|
| `SKILL.md` | 커밋 메시지 형식, 브랜치 네이밍 규칙 |

## 관련 커맨드

| 커맨드 | 경로 | 적용 규칙 |
|--------|------|-----------|
| `/git:save` | `commands/git/save.md` | 커밋 메시지 형식 |
| `/git:push` | `commands/git/push.md` | 커밋 메시지 형식 |
| `/git:switch` | `commands/git/switch.md` | 브랜치 네이밍 |
| `/git:pr` | `commands/git/pr.md` | PR 제목/본문 형식 |

## 컨벤션 요약

### 커밋 메시지

```
<type>: <subject>

type: feat, fix, refactor, docs, style, test, chore
subject: 한국어, 명령형
```

### 브랜치 네이밍

```
<type>/<description>

type: feature, fix, refactor, docs
description: 케밥 케이스
```

## 수정 시 체크리스트

- [ ] 커밋 타입 변경 → `SKILL.md`, `/git:save`, `/git:push` 확인
- [ ] 브랜치 타입 변경 → `SKILL.md`, `/git:switch` 확인
- [ ] 메시지 형식 변경 → `SKILL.md`, 모든 git 커맨드 확인

## 의존성 관계

```
SKILL.md (컨벤션 정의)
    │
    ├──► commands/git/save.md (커밋)
    ├──► commands/git/push.md (커밋)
    ├──► commands/git/switch.md (브랜치)
    └──► commands/git/pr.md (PR)
```
