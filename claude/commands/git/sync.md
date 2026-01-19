---
description: 원격과 동기화 (pull + rebase)
allowed-tools: Bash(git:*)
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- 변경 파일: !`git status --short`

# 작업
1. 커밋 안 된 변경사항 있으면 stash
2. `git pull --rebase`
3. stash 있었으면 pop

충돌 나면 내용 보여주고 어떻게 할지 물어봐.