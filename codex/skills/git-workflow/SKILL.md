---
name: git-workflow
description: 로컬 Git 작업 흐름. 변경사항 검토, dirty worktree 분류, 선택 staging, 안전한 브랜치/커밋/푸시, diff 요약, 충돌 최소화가 필요할 때 사용한다. 기존 git-convention 스킬이 있으면 커밋 메시지와 브랜치 규칙은 그 스킬을 따른다.
---

# Git Workflow

## 언제 사용하나

- 사용자가 변경사항을 검토해 달라고 할 때
- 어떤 파일을 커밋해야 할지 정리해야 할 때
- 관련 변경만 골라 stage/commit 해야 할 때
- 새 브랜치를 만들거나 현재 브랜치 상태를 확인해야 할 때
- push, PR 준비, diff 요약이 필요할 때

## 기본 원칙

- 먼저 `git status --short --branch`로 상태를 고정한다.
- 사용자 요청 범위와 무관한 변경은 절대 되돌리지 않는다.
- 기본적으로 선택 staging을 사용하고, 범위가 명확할 때만 전체 staging을 쓴다.
- destructive 명령은 사용하지 않는다.
- interactive git 명령 대신 비대화형 명령을 우선한다.

## 권장 절차

### 1. 상태 파악

다음 순서로 현재 상태를 본다.

1. `git status --short --branch`
2. `git diff --stat`
3. 필요 시 `git diff -- <path>` 또는 `git diff --cached -- <path>`
4. 필요 시 `git log --oneline --decorate -n 10`

### 2. 변경 분류

변경을 아래 세 부류로 나눈다.

- 이번 요청에 직접 해당하는 변경
- 같은 파일에 섞여 있지만 함께 이해해야 하는 변경
- 이번 요청과 무관한 변경

무관한 변경이 있으면 그대로 둔다. 같은 파일에 섞여 있으면 함부로 되돌리지 말고 충돌 가능성을 먼저 설명한다.

### 3. staging

- 기본은 `git add <file>`처럼 명시적 staging이다.
- 여러 파일이지만 범위가 명확하면 파일 목록을 나열해서 stage 한다.
- hunk 단위 분리가 꼭 필요할 때만 신중하게 처리한다.
- `git add .`는 작업 범위가 저장소 전체일 때만 쓴다.

### 4. 브랜치

- 사용자가 별도 규칙을 주지 않으면 `codex/<topic>`를 기본 브랜치명으로 본다.
- 이미 작업 브랜치가 있으면 그 브랜치에서 이어간다.
- 브랜치를 새로 만들기 전 현재 dirty worktree와 추적 브랜치 상태를 먼저 확인한다.

### 5. 커밋

- 커밋 전 `git diff --cached --stat` 또는 `git diff --cached`로 staged 내용만 다시 확인한다.
- 메시지와 브랜치 규칙은 `git-convention` 스킬이 있으면 그 규칙을 따른다.
- 커밋 메시지에는 결과를 쓰고, 구현 과정 나열은 최소화한다.

### 6. push와 publish

- push는 사용자가 publish 의도를 보였을 때만 진행한다.
- 기본은 현재 브랜치를 원격에 업로드하는 수준으로 제한한다.
- force push는 명시 요청 없이는 하지 않는다.

## 안전 규칙

- `git reset --hard`, `git checkout --`, `git clean -fd`, `git push --force`는 명시 요청 없이는 금지다.
- rebase, merge, cherry-pick이 현재 dirty worktree와 충돌할 가능성이 크면 먼저 설명하고 범위를 좁힌다.
- 다른 사람이 만든 변경이나 사용자가 아직 확인하지 않은 변경은 임의로 합치거나 버리지 않는다.

## 응답 형식 가이드

### 상태 보고

- 현재 브랜치
- 추적 브랜치 대비 상태
- 수정/추가/삭제 파일 수
- 이번 요청 범위에 포함되는 파일
- 남겨둔 파일이 있으면 그 이유

### 커밋 준비 보고

- stage 한 파일
- 커밋 제목 초안
- 아직 검토가 필요한 파일 또는 리스크

### diff 요약

- 사용자 영향
- 핵심 파일
- 위험한 변경
- 검증 여부

## 자주 쓰는 명령

```bash
git status --short --branch
git diff --stat
git diff -- path/to/file
git diff --cached --stat
git add path/to/file
git commit -m "..."
git push -u origin <branch>
```

## 이 스킬이 하지 않는 것

- 저장소 규칙을 무시한 임의 force push
- unrelated change 정리라는 이름의 강제 되돌리기
- 커밋 규칙을 새로 발명하는 일

