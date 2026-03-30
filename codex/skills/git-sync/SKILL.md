---
name: git-sync
description: 현재 브랜치를 원격 또는 기준 브랜치와 rebase 방식으로 동기화할 때 사용한다. Claude의 `/git:sync` 대응 스킬이다. pull --rebase, 기준 브랜치 rebase, stash 복구, 충돌 보고가 필요할 때 사용한다.
---

# Git Sync

## 언제 사용하나

- 현재 브랜치를 최신 기준으로 rebase 동기화할 때
- `origin/main`, `origin/master`, 또는 특정 로컬 브랜치 기준으로 맞출 때

## source mapping

- Claude command: `/git:sync`

## 기본 규칙

- uncommitted change가 있으면 먼저 stash 여부를 판단한다.
- 인자가 없으면 현재 브랜치의 추적 원격에 대해 `git pull --rebase`를 우선 본다.
- 인자가 로컬 브랜치면 `git rebase <branch>`를 사용한다.
- 인자가 `origin/main` 같은 원격 브랜치면 fetch 후 rebase 한다.
- 충돌이 나면 상태를 보여주고 다음 행동을 사용자와 정한다.

## 실행 절차

1. 현재 브랜치와 working tree 상태를 확인한다.
2. 필요하면 stash 한다.
3. 기준 대상을 해석한다.
4. 아래 중 하나를 수행한다.
   - 인자 없음: `git pull --rebase`
   - 로컬 브랜치: `git rebase <branch>`
   - 원격 브랜치: `git fetch <remote>` 후 `git rebase <remote>/<branch>`
5. stash가 있으면 복구한다.
6. 결과 또는 충돌 상태를 보고한다.

## 사용자에게 물어봐야 하는 경우

- stash가 필요한데 사용자가 유지 방식을 명확히 주지 않았을 때
- 충돌이 발생했을 때

## 하지 말아야 할 것

- 충돌을 임의로 자동 해결했다고 가정하지 않는다.
- force push를 후속 단계로 자동 제안하지 않는다.

