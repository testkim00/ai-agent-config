---
description: 변경사항 스테이징하고 커밋
allowed-tools: Bash(git:*), Task
---

# 현재 상태
- 변경 파일: !`git status --short`
- 최근 커밋: !`git log --oneline -3`

# 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

## 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 커밋 여부 판단, 최종 확인 |
| **실행** | Sonnet subagent | 변경사항 분석, 커밋 메시지 생성, git 명령 실행 |

## Phase 1: 판단 (Opus)

변경사항 없으면 "커밋할 내용이 없습니다" 출력하고 종료.

## Phase 2: 커밋 실행 (Sonnet Subagent)

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    Git 커밋 작업:

    1. 변경사항 상세 확인
       - git diff --stat
       - git diff (내용 확인)

    2. 커밋 메시지 생성 (conventional commit 형식)
       - feat: 새 기능
       - fix: 버그 수정
       - docs: 문서 변경
       - style: 포맷팅
       - refactor: 리팩토링
       - test: 테스트
       - chore: 기타

    3. 스테이징 및 커밋
       - git add -A
       - git commit -m "{메시지}"

    4. 결과 반환
       - 커밋 해시
       - 변경 파일 수
    """
)
```

## Phase 3: 결과 확인 (Opus)

- 커밋 결과 확인
- 사용자에게 응답