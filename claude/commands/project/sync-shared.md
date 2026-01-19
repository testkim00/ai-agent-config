---
description: 공유 모듈(ui-shell, components, core) 최신 버전으로 업데이트
allowed-tools: Bash(git:*)
---

# 공유 모듈 동기화

원격 저장소의 최신 변경사항을 현재 프로젝트로 가져옵니다.

## 사용법
- `/project:sync-shared` - 3개 모듈 모두 동기화
- `/project:sync-shared ui-shell` - ui-shell만 동기화
- `/project:sync-shared components` - components만 동기화
- `/project:sync-shared core` - core만 동기화

## 인자
$ARGUMENTS

---

# 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

## 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 사용자 확인, 변경사항 체크 |
| **실행** | Sonnet subagent | git subtree pull 명령 |

## Phase 1: 판단 (Opus)

1. 현재 상태 표시
2. 커밋 안 된 변경사항 있으면 경고
3. "공유 모듈을 원격에서 동기화하시겠습니까?" 확인
4. 사용자 승인 후 진행

## Phase 2: 동기화 (Sonnet Subagent)

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    공유 모듈 동기화 작업:

    동기화할 모듈: {all/ui-shell/components/core}

    1. Subtree Pull
       all인 경우:
       - git subtree pull --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main --squash
       - git subtree pull --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main --squash
       - git subtree pull --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main --squash

       개별 모듈인 경우 해당 명령만 실행

    2. 결과 확인
       - git status
       - 업데이트된 파일 목록

    3. 결과 반환
       - 동기화된 모듈
       - 변경된 파일 수
    """
)
```

## Phase 3: 결과 안내 (Opus)

- 업데이트된 파일 목록 표시
