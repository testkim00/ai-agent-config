---
name: git-cleanup
description: 머지된 로컬 브랜치를 정리할 때 사용한다. Claude의 `/git:cleanup` 대응 스킬이다. gone 브랜치를 확인하고, 삭제 후보를 사용자에게 보여준 뒤 안전하게 `git branch -d`로 정리해야 할 때 사용한다.
---

# Git Cleanup

## 언제 사용하나

- PR 머지 후 로컬 브랜치를 정리할 때
- 원격에서 이미 삭제된 브랜치의 로컬 찌꺼기를 정리할 때

## source mapping

- Claude command: `/git:cleanup`

## 기본 규칙

- 먼저 `git fetch --prune`으로 원격 상태를 갱신한다.
- 삭제 전 후보 목록을 보여주고 사용자 확인을 받는다.
- `main`/`master` 계열은 삭제하지 않는다.
- 현재 체크아웃된 브랜치는 삭제하지 않는다.
- `git branch -D`는 명시 요청 없이는 사용하지 않는다.

## 실행 절차

1. `git branch --show-current`와 `git branch -vv`로 현재 상태를 확인한다.
2. `git fetch --prune`을 실행한다.
3. `gone` 상태인 브랜치를 추린다.
4. 삭제 후보와 제외 대상을 구분해 사용자에게 보여준다.
5. 확인을 받으면 각 브랜치에 대해 `git branch -d <branch>`를 실행한다.
6. 실패한 브랜치가 있으면 이유를 함께 보고한다.

## 사용자에게 물어봐야 하는 경우

- 삭제 후보가 1개 이상일 때
- 현재 브랜치가 삭제 후보일 때 어떤 브랜치로 옮길지

## 하지 말아야 할 것

- 원격 브랜치를 임의로 삭제하지 않는다.
- `main`, `master`, 기본 브랜치 추정값을 삭제하지 않는다.
- 미머지 브랜치를 강제로 지우지 않는다.

