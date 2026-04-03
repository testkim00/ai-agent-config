---
description: 원격과 동기화 (current branch sync + all-branches bulk sync)
allowed-tools: Bash(git:*)
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- 변경 파일: !`git status --short`

# 파라미터
- `$ARGUMENTS`: 동기화 대상
  - 없음: 현재 브랜치의 원격과 동기화
  - `origin/master`: 현재 브랜치를 지정한 원격 브랜치 기준으로 동기화
  - `--all-branches`: 현재 저장소의 모든 로컬 브랜치를 checkout 없이 upstream 또는 같은 이름의 `origin/<branch>`와 동기화
  - `~/Projects` 같은 디렉터리 경로: 해당 폴더와 하위의 Git 저장소들을 찾아 각 저장소의 모든 로컬 브랜치를 원격과 동기화

# 모드
1. **current branch mode**
   - 기존 동작 유지
2. **bulk mode**
   - `--all-branches` 또는 디렉터리 경로
   - auto-stash 없음
   - configured upstream에서 local ahead면 upstream은 버리고 `origin/<branch>` 같은 same-name remote fallback을 시도
   - 어떤 브랜치가 모든 remote 후보보다 ahead면 그 저장소만 skip
   - dirty worktree, detached HEAD, missing remote target도 그 저장소의 skip 사유

# 작업
1. 인자를 해석해 current branch mode인지 bulk mode인지 결정
2. **current branch mode**
   - 커밋 안 된 변경사항 있으면 stash
   - **인자 없음**: `git pull --rebase`
   - **로컬 브랜치** (예: `master`): `git rebase master`
   - **원격 브랜치** (예: `origin/master`): `git fetch origin` → `git rebase origin/master`
   - stash 있었으면 pop
3. **bulk mode**
   - 대상 repo 목록 확정
   - 각 repo에서 `git fetch --all --prune`
   - 각 로컬 브랜치의 configured upstream, `origin/<branch>`, 기타 same-name remote 후보 확인
   - ahead/behind 전수 검사
   - configured upstream이 막히면 origin fallback 시도
   - 모든 후보가 막힌 브랜치가 있으면 그 저장소만 skip
   - blocker 없는 저장소만 current branch는 fast-forward, non-current branch는 ref update로 sync

충돌 나면 내용 보여주고 어떻게 할지 물어봐.
