---
name: git-push
description: 현재 브랜치를 원격에 push할 때 사용한다. Claude의 `/git:push` 대응 스킬이다. 필요하면 먼저 커밋 여부를 확인하고, 기본 원격은 origin으로 보며, upstream이 없으면 안전하게 설정해야 할 때 사용한다.
---

# Git Push

## 언제 사용하나

- 현재 브랜치를 원격에 올릴 때
- 커밋 후 바로 publish까지 진행할 때

## source mapping

- Claude command: `/git:push`

## 기본 규칙

- 기본 원격은 `origin`으로 본다.
- uncommitted change가 있으면 먼저 커밋할지 확인한다.
- 현재 브랜치가 `main`/`master`면 경고하고 확인을 받는다.
- upstream이 없으면 `-u`를 붙여 설정한다.
- force push는 명시 요청 없이는 금지다.

## 실행 절차

1. `git branch --show-current`, `git status --short`, `git remote -v`를 본다.
2. 변경사항이 있으면 `git-save` 성격의 절차를 먼저 수행할지 판단한다.
3. push 대상 원격을 정한다.
4. upstream 존재 여부를 확인한다.
5. `git push` 또는 `git push -u <remote> <branch>`를 실행한다.
6. 결과를 요약한다.

## 사용자에게 물어봐야 하는 경우

- uncommitted change가 있는데 사용자가 push만 말했을 때
- `main`/`master`에 직접 push하려고 할 때
- 원격 저장소가 여러 개라 목적지가 불분명할 때

## 하지 말아야 할 것

- 자동 force push
- unrelated change까지 묶어서 임의 커밋 후 push

