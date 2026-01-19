---
description: Pull Request 생성
allowed-tools: Bash(git:*), Bash(gh:*), Task
---

# 현재 상태
- 브랜치: !`git branch --show-current`
- main과 차이: !`git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline 2>/dev/null || echo "비교 불가"`
- 변경 파일: !`git diff main --stat 2>/dev/null || git diff master --stat 2>/dev/null || echo "비교 불가"`

# 파라미터
- $ARGUMENTS: PR 설명 (선택)

# 사전 체크
1. 현재 브랜치가 main 또는 master면 **중단**하고 안내:
   - "main/master 브랜치에서는 PR을 생성할 수 없습니다."
   - "/git:switch {브랜치명}으로 feature 브랜치를 먼저 생성하세요."

---

# 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

## 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 브랜치 체크, PR 가능 여부 판단 |
| **실행** | Sonnet subagent | 커밋 분석, PR 제목/본문 작성, gh 명령 실행 |

## Phase 1: 판단 (Opus)

- main/master 브랜치면 중단
- 커밋 없으면 중단

## Phase 2: PR 생성 (Sonnet Subagent)

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    Pull Request 생성 작업:

    브랜치: {현재 브랜치}
    추가 설명: {$ARGUMENTS 또는 없음}

    1. 커밋 분석
       - git log main..HEAD (또는 master)
       - git diff main --stat

    2. PR 제목 생성
       - conventional commit 형식
       - 변경사항 요약

    3. PR 본문 작성
       ## 변경 사항
       - 커밋 내역 기반 bullet points

       ## 변경 이유
       - 추가 설명 있으면 포함

    4. 브랜치 푸시 및 PR 생성
       - git push -u origin {브랜치}
       - gh pr create --title "{제목}" --body "{본문}"

    5. 결과 반환
       - PR URL
    """
)
```

## Phase 3: 결과 확인 (Opus)

- PR URL 확인
- 사용자에게 응답