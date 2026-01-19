---
description: 커밋하고 원격에 푸시
allowed-tools: Bash(git:*)
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- 변경 파일: !`git status --short`
- 원격: !`git remote -v`

# 파라미터
- $1: 원격 저장소 (기본값: origin)

# 작업
1. 변경사항 있으면 스테이징 + 커밋
2. $1 또는 origin으로 푸시
3. upstream 없으면 자동 설정

main/master 브랜치면 경고하고 확인 요청.