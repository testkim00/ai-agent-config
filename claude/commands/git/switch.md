---
description: 새 브랜치 생성 및 전환
allowed-tools: Bash(git:*)
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- 변경 파일: !`git status --short`

# 파라미터
- $ARGUMENTS: 브랜치명 (필수)

# 브랜치명 컨벤션
| 접두사 | 용도 |
|--------|------|
| feature/ | 새 기능 |
| fix/ | 버그 수정 |
| docs/ | 문서 작업 |
| refactor/ | 리팩토링 |
| hotfix/ | 긴급 수정 |
| chore/ | 잡일 (설정, 의존성 등) |
| test/ | 테스트 추가 |

# 작업
1. $ARGUMENTS 없으면 브랜치명 입력 요청
2. 변경사항 있으면 stash 또는 커밋 여부 확인
3. 접두사 없으면 `feature/` 자동 추가
4. `git switch -c {브랜치명}` 으로 브랜치 생성 및 전환
5. 이미 존재하는 브랜치면 해당 브랜치로 전환만

# 예시
```
/git:switch 로그인추가
→ feature/로그인추가 브랜치 생성

/git:switch fix/validation-error
→ fix/validation-error 브랜치 생성

/git:switch docs/api-guide
→ docs/api-guide 브랜치 생성
```
