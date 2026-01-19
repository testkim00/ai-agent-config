---
description: 공유 모듈 변경사항을 원격 저장소에 푸시
allowed-tools: Bash(git:*)
---

# 공유 모듈 푸시

현재 프로젝트의 _shared 모듈 변경사항을 원격 저장소에 푸시합니다.

## 사용법
- `/project:push-shared` - 변경된 모듈 모두 푸시
- `/project:push-shared ui-shell` - ui-shell만 푸시
- `/project:push-shared components` - components만 푸시
- `/project:push-shared core` - core만 푸시

## 인자
$ARGUMENTS

## 주의사항
- 공유 모듈을 수정한 경우에만 사용
- 다른 프로젝트에도 영향을 미치므로 신중하게 사용

---

# 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

## 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 사용자 확인, 커밋 상태 체크 |
| **실행** | Sonnet subagent | git subtree push 명령 |

## Phase 1: 판단 (Opus)

1. 변경사항 표시
2. 커밋 안 됐으면 먼저 커밋 요청
3. "공유 모듈을 원격에 푸시하시겠습니까? 다른 프로젝트에도 영향을 미칩니다." 확인
4. 사용자 승인 후 진행

## Phase 2: 푸시 (Sonnet Subagent)

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    공유 모듈 푸시 작업:

    푸시할 모듈: {all/ui-shell/components/core}

    1. 변경사항 확인
       - src/_shared/ 하위 변경 파일 확인

    2. Subtree Push
       all인 경우:
       - git subtree push --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main
       - git subtree push --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main
       - git subtree push --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main

       개별 모듈인 경우 해당 명령만 실행

    3. 결과 반환
       - 푸시 성공/실패
       - 푸시된 모듈 목록
    """
)
```

## Phase 3: 결과 안내 (Opus)

- 푸시 성공 여부 표시
