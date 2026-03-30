---
name: git-switch
description: 새 브랜치를 만들거나 기존 브랜치로 전환할 때 사용한다. Claude의 `/git:switch` 대응 스킬이다. 브랜치명을 정규화하고, dirty worktree가 있으면 stash 또는 커밋 여부를 먼저 확인한 뒤 안전하게 `git switch`를 수행해야 할 때 사용한다.
---

# Git Switch

## 언제 사용하나

- 새 작업 브랜치를 만들 때
- 기존 브랜치로 전환할 때

## source mapping

- Claude command: `/git:switch`

## 기본 규칙

- 브랜치명이 없으면 짧게 물어본다.
- 접두사가 없으면 기본 접두사를 붙인다.
- dirty worktree가 있으면 stash 또는 커밋 여부를 먼저 정한다.
- 이미 존재하는 브랜치면 생성하지 말고 전환만 한다.

## 브랜치 접두사

- `feature/`
- `fix/`
- `docs/`
- `refactor/`
- `hotfix/`
- `chore/`
- `test/`

## 실행 절차

1. 현재 브랜치와 working tree 상태를 확인한다.
2. 브랜치명을 정규화한다.
3. dirty worktree가 있으면 어떻게 처리할지 정한다.
4. 브랜치가 없으면 `git switch -c <branch>`를 실행한다.
5. 이미 있으면 `git switch <branch>`로 전환한다.
6. 결과 브랜치를 요약한다.

## 사용자에게 물어봐야 하는 경우

- 브랜치명이 비어 있을 때
- dirty worktree가 있어 stash와 commit 중 선택이 필요할 때

## 하지 말아야 할 것

- 이름 없이 임의 브랜치를 만들지 않는다.
- 사용자 변경을 임의 stash/pop으로 흐리게 만들지 않는다.

