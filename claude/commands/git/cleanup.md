---
description: 머지된 브랜치 정리
allowed-tools: Bash(git:*)
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- 로컬 브랜치 목록: !`git branch`

# 작업
1. `git fetch --prune`으로 원격 정보 동기화
2. gone 브랜치 확인 (`git branch -vv | grep 'gone]'`)
3. 삭제할 브랜치 목록 보여주고 확인 요청
4. 확인 후 `git branch -d {브랜치명}`으로 삭제
5. main/master 브랜치는 절대 삭제하지 않음
6. 현재 체크아웃된 브랜치는 삭제 불가 → master로 먼저 전환

# 워크플로우
```
PR 머지 → GitHub에서 "Delete branch" → git fetch --prune → /git:cleanup
```

# 주의사항
- 삭제 전 반드시 사용자 확인
- 원격 브랜치 삭제는 GitHub에서 직접 처리

# 예시
```
/git:cleanup
→ gone 브랜치 확인 → 목록 표시 → 확인 후 로컬 삭제
```
