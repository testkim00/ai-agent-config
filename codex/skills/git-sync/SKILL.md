---
name: git-sync
description: 현재 브랜치, 현재 저장소의 전체 로컬 브랜치, 또는 특정 폴더 아래 여러 저장소의 전체 로컬 브랜치를 원격과 동기화할 때 사용한다. Claude의 `/git:sync` 대응 스킬이다. 기본 current-branch sync, `--all-branches` bulk sync, 디렉터리 단위 recursive sync를 안전하게 수행할 때 사용한다.
---

# Git Sync

## 언제 사용하나

- 현재 브랜치를 최신 기준으로 rebase 동기화할 때
- `origin/main`, `origin/master`, 또는 특정 로컬 브랜치 기준으로 맞출 때
- 현재 저장소의 로컬 브랜치들을 checkout/switch 없이 원격 브랜치들과 맞출 때
- `~/Projects` 같은 상위 폴더 아래 여러 저장소의 모든 로컬 브랜치를 원격과 일괄 동기화할 때

## source mapping

- Claude command: `/git:sync`

## 기본 규칙

- 기본 대상 저장소는 현재 작업 디렉터리(`cwd`)의 Git 저장소다.
- 실제 디렉터리 경로가 인자로 주어졌을 때만 대상 저장소를 그 경로 아래의 Git 저장소들로 확장한다.
- uncommitted change가 있으면 먼저 stash 여부를 판단한다.
- 인자가 없으면 현재 브랜치의 추적 원격에 대해 `git pull --rebase`를 우선 본다.
- 인자가 로컬 브랜치면 `git rebase <branch>`를 사용한다.
- 인자가 `origin/main` 같은 원격 브랜치면 fetch 후 rebase 한다.
- `--all-branches`가 있으면 현재 저장소의 모든 로컬 브랜치를 각 upstream 또는 같은 이름의 `origin/<branch>`와 동기화한다.
- 첫 인자가 실제 디렉터리 경로면, 그 디렉터리와 하위 디렉터리에서 Git 저장소를 재귀 탐색하고 각 저장소의 모든 로컬 브랜치를 원격과 동기화한다.
- bulk 모드(`--all-branches` 또는 디렉터리 모드)는 branch switch를 하지 않는다.
- bulk 모드는 먼저 `fetch --all --prune` 후 저장소별 preflight를 수행한다.
- 로컬 브랜치가 configured upstream보다 ahead면 먼저 upstream 후보를 버리고, 같은 이름의 `origin/<branch>` 또는 다른 same-name remote branch를 다시 찾는다.
- 한 브랜치가 모든 후보 remote보다 ahead면 그 저장소만 skip하고, 다른 저장소 sync는 계속 진행한다.
- bulk 모드는 auto-stash를 하지 않는다. dirty worktree, detached HEAD, upstream 없음도 blocker로 본다.
- 충돌이 나면 상태를 보여주고 다음 행동을 사용자와 정한다.

## bulk sync helper

- 반복 실행은 helper script를 우선 사용한다.
- Script: `/Users/honeychaser/Projects/ai-agent-config/codex/skills/git-sync/scripts/sync_all_branches.py`
- 현재 저장소 전체 브랜치 sync:
  `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/git-sync/scripts/sync_all_branches.py .`
- 상위 폴더 전체 repo sync:
  `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/git-sync/scripts/sync_all_branches.py ~/Projects`
- dry run:
  `python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/git-sync/scripts/sync_all_branches.py ~/Projects --dry-run`

## 실행 절차

1. 요청을 세 가지 모드 중 하나로 분류한다.
   - current-branch mode: 인자 없음, 로컬 브랜치, 원격 브랜치
   - current-repo bulk mode: `--all-branches`
   - directory bulk mode: 첫 인자가 실제 디렉터리 경로
2. current-branch mode면 기존 절차를 유지한다.
   - 현재 브랜치와 working tree 상태 확인
   - 필요하면 stash
   - 기준 대상 해석
   - 인자 없음: `git pull --rebase`
   - 로컬 브랜치: `git rebase <branch>`
   - 원격 브랜치: `git fetch <remote>` 후 `git rebase <remote>/<branch>`
   - stash 복구
3. bulk mode면 helper script 또는 같은 절차를 따른다.
   - 대상 repo 목록 확정
   - 각 repo에서 `git fetch --all --prune`
   - 각 로컬 브랜치의 configured upstream, `origin/<branch>`, 기타 same-name remote branch 후보를 순서대로 해석
   - ahead/behind, dirty, detached HEAD, missing upstream를 전수 점검
   - configured upstream에서 로컬이 ahead면 upstream 후보를 버리고 다음 remote 후보로 이동
   - 어떤 브랜치가 모든 remote 후보보다 ahead면 그 저장소만 skip
   - blocker가 없는 저장소만 적용
   - 현재 checkout된 브랜치는 switch 없이 fast-forward로 갱신
   - checkout되지 않은 브랜치는 ref move로 갱신
4. 결과를 repo/branch 단위로 요약하고, skip된 저장소는 blocker 사유와 함께 따로 보고한다.

## 사용자에게 물어봐야 하는 경우

- stash가 필요한데 사용자가 유지 방식을 명확히 주지 않았을 때
- 충돌이 발생했을 때
- bulk mode에서 skip된 저장소를 어떻게 처리할지 후속 결정이 필요한데 사용자가 예외 처리 방식을 명시하지 않았을 때

## 하지 말아야 할 것

- 충돌을 임의로 자동 해결했다고 가정하지 않는다.
- force push를 후속 단계로 자동 제안하지 않는다.
- ahead 상태인 로컬 브랜치를 원격 기준으로 덮어쓰지 않는다.
- skip된 저장소를 숨기고 전체 성공처럼 보고하지 않는다.
