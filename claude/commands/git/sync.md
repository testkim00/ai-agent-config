---
description: 원격과 동기화 (pull + rebase)
allowed-tools: Bash(git:*)
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- 변경 파일: !`git status --short`

# 파라미터
- $ARGUMENTS: 동기화 대상 (예: origin/master). 없으면 현재 브랜치의 원격과 동기화

# 작업
1. 커밋 안 된 변경사항 있으면 stash
2. 동기화 실행
   - **인자 없음**: `git pull --rebase` (현재 브랜치의 원격과 동기화)
   - **로컬 브랜치** (예: `master`): `git rebase master` (로컬 브랜치 기준으로 rebase)
   - **원격 브랜치** (예: `origin/master`): `git fetch origin` → `git rebase origin/master` (원격 브랜치 기준으로 rebase)
3. stash 있었으면 pop

충돌 나면 내용 보여주고 어떻게 할지 물어봐.
